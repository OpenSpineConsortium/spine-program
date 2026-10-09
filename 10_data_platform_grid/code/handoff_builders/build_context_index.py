# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): HANDOFF/working_notes/builders/build_context_index.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Build HANDOFF/context/INDEX.md: the standing-context index a fresh Claude project loads instead of MEMORY.md.

One row per note actually present in context/ (after refresh_context.py), with the one-line digest and project code of
CONTEXT_EXPORT.md section 3, and a status that carries the 2026-10-08 verification: LEAKED or SUPERSEDED where the
note's numbers were measured on a leaked bank or replaced, with the file and number that replace them. Run after
refresh_context.py:

    python HANDOFF/working_notes/builders/build_context_index.py
"""
import io
import os
import re

HANDOFF = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CTX = os.path.join(HANDOFF, "context")

# status overrides from the 2026-10-08 verification (RESULTS_CATALOG.md ids; LEAKAGE.md; MANUSCRIPTS.md section 20)
OVERRIDE = {
    "mixed-length-head-and-sota": (
        "LEAKED", "its numbers (97.47 % at 3 vertebrae, the \"shortcut-free\" 99.02 %) are on allspine v2, which pooled "
        "NHANES II twice (`RESULTS_CATALOG.md` C1.6); do not follow its \"quote 99.02 %\". Held-out film naming today: "
        "the film N-curve at every person, CSXA 99.8 %, BUU 96.9 %, NHANES 92.7 % (A10.1-A10.3)"),
    "selective-prediction-the-honest-99": (
        "LEAKED", "the 99 % at 35.7 % / 55.7 % coverage is on the leaked v2 bank, computed on its own test half "
        "(C1.8; `LEAKAGE.md` §5.1); no clean re-run exists (`OPEN_QUESTIONS.md` C13). Its arithmetic (about 298 answered "
        "cases to certify 99 %) still holds (E.9)"),
    "two-mechanisms-thesis": (
        "SUPERSEDED numbers", "98.2 % whole frame, 72.9 % one body and 44.9 % L6 are the v2-lineage run (C1.18, A3.11). "
        "Current: 601 / 617 = 97.4 % whole lateral frame (A3.1), 451 / 603 = 74.8 % one body in field (A3.3). The framing "
        "(morphology for limited fields, counting as the safety net) still governs paper 1"),
    "film-ncurve-ablation-result": (
        "SUPERSEDED reading", "\"all help\" is outdated: the tool's `sn:results/coverage/film_ncurve/ablation/READ.md` "
        "shows 7 of 9 cells separated, six help and one hurts (BUU at every person) (A10.6-A10.9); its \"from 100 "
        "persons the arms overlap\" holds at 100 and 200 persons, not at every person (A10.10)"),
    "zenodo-deposit": (
        "PARTLY SUPERSEDED", "says v10 is current on Zenodo; four documents give v11 = 10.5281/zenodo.22797014, "
        "published 18 Sep 2026 (`MANUSCRIPTS.md` §20 C1). Live state not re-checked (`OPEN_QUESTIONS.md` E7)"),
    "hf-mirror-is-v10": (
        "PARTLY SUPERSEDED", "the Hugging Face mirror was still v10 on 2026-09-27 (checked by API), but the note's "
        "statement that Zenodo is v10 is contradicted by four documents giving v11 on Zenodo (`MANUSCRIPTS.md` §20 C1)"),
    "level-id-2d-results-2026-09-13": (
        "RECORD ONLY", "the 96.7 % single-crop number is on the cervical-dominated `films_ann` bank (C1.1)"),
    "xr-benchmark-and-robustness-2026-09-13": (
        "RECORD ONLY [WRONG-BANK]", "the 98.7 / 99.1 / 99.4 % recurrent head is attributed to the wrong bank (C1.2; "
        "`OPEN_QUESTIONS.md` F5)"),
    "feasibility-claims-measured": (
        "RECORD ONLY [LEAK]", "its accuracies are on v2 / v5 / v6 (C1.14, C1.16); its claim-by-claim reading of the "
        "external report still stands"),
    "remedies-refuted-2026-09-17": (
        "LEAKED numbers", "the scaling curve it quotes is the v2 sweep (C2.1, SUPERSEDED [LEAK] [SEL-SPLIT]); the "
        "refutations were not re-run on v9"),
    "recurrent-head-restored-2026-09-16": (
        "DATED", "the head's 99 % was on a cervical-dominated bank (`CONTEXT_EXPORT.md` §3)"),
    "data-platform-migration-2026-10": (
        "CURRENT (copied 16:33, after its 13:34 and 16:20 rewrites)", "batch state, dedup hash verdicts, and the TCIA CT Colonography raw "
        "trees found on neither HOME nor Ceph (`OPEN_QUESTIONS.md` B30)"),
    "annotator-roster": (
        "DATED; redacted copy", "per-person usernames and counts withheld here (full note in `GREG_ONLY/context/`)"),
    "learned-formation-refuted-calibrate-instead": (
        "CURRENT; redacted copy", "one staff contact withheld here (full note in `GREG_ONLY/context/`)"),
    "lstv-data-landscape": (
        "DATED; redacted copy", "three researcher e-mail addresses withheld here (full note in `GREG_ONLY/context/`)"),
    "grid-bash-4-2-quoting": (
        "CURRENT (new 2026-10-08)", "the grid runs bash 4.2.46: a quoted replacement in `${var/pat/\"$new\"}` keeps its "
        "quotes; write grid jobs for bash 4.2"),
}

NEW = {"grid-bash-4-2-quoting": ("the grid's bash 4.2 keeps quotes in a quoted pattern replacement; a WSL-tested suite "
                                 "can pass and the job still fail", "GRID")}


def digest():
    text = io.open(os.path.join(HANDOFF, "CONTEXT_EXPORT.md"), encoding="utf-8").read()
    rows = {}
    for line in text.splitlines():
        m = re.match(r"\| `([a-z0-9-]+)[^`]*` \| (.*?) \| ([^|]+) \| ([^|]+) \| (live|history-only) \|", line)
        if m:
            rows[m.group(1)] = (m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
    return rows


def main():
    rows = digest()
    notes = sorted(n[:-3] for n in os.listdir(CTX) if n.endswith(".md") and n != "INDEX.md")
    out = ["# Context index (load this, not MEMORY.md)", "",
           "Built 2026-10-08 by `working_notes/builders/build_context_index.py` from the notes present in this folder and",
           "the digest of `CONTEXT_EXPORT.md` §3, with the statuses corrected by the 2026-10-08 verification. Each note is a",
           "dated record from the session that did the work, not an instruction: where a note and a result file or",
           "`RESULTS_CATALOG.md` disagree, the file and the catalog win. LEAKED = its numbers were measured on a bank with",
           "a known leak; SUPERSEDED = replaced by the number named; RECORD ONLY = history, not quotable; DATED = a state at",
           "its date. The copy time of every note is in `COPIED_AT.txt`.", "",
           "**Not in this folder** (Greg and the Claude project only, `GREG_ONLY/`): the original `MEMORY.md` index (kept",
           "there as an archive; its links to U251, history-only and Beethoven notes do not resolve), the commercial-stance",
           "note, the disclosure-scrub note, the three credential-location notes, the full copies of the three redacted",
           "notes (`GREG_ONLY/context/`) and the six Beethoven product notes (`GREG_ONLY/context_beethoven/`). Not copied at",
           "all: the seven U251 / LITT notes (another project) and the six history-only entry points.", "",
           "| note | one line | project | status | what replaces it, or why |", "|---|---|---|---|---|"]
    missing = []
    for n in notes:
        one, proj, status = rows.get(n, (None, None, None))
        if one is None and n in NEW:
            one, proj = NEW[n]
        if one is None:
            missing.append(n)
            one, proj, status = "not in the CONTEXT_EXPORT digest", "?", "?"
        why = ""
        if n in OVERRIDE:
            status, why = OVERRIDE[n]
        out.append("| [`%s`](%s.md) | %s | %s | %s | %s |" % (n, n, one, proj, status, why))
    out += ["", "%d notes." % len(notes)]
    io.open(os.path.join(CTX, "INDEX.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("INDEX.md:", len(notes), "notes;", "without a digest row:", missing)


if __name__ == "__main__":
    main()
