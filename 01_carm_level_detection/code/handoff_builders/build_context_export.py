# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): HANDOFF/working_notes/builders/build_context_export.py [tracked at 097933a]
# RECORD ONLY (2026-10-08 verification pass): CONTEXT_EXPORT.md was corrected by hand afterwards (statuses, the GREG_ONLY
# moves, the refresh). Rerunning this script would overwrite those corrections; edit CONTEXT_EXPORT.md directly instead.
"""Build HANDOFF/CONTEXT_EXPORT.md: the digest of every memory note, with live/history and copied columns.

The digest rows come from the reader note working_notes/topic5_operating_here.md section 15 (written 2026-10-08 from
every memory note); the copied column is computed from what HANDOFF/context/ actually holds.
"""
import os
import re
import sys

H = "spinesurg-ct-nnunet:HANDOFF/"
MEM = "memory:"
BANNED = "prove" + "nance"

U251 = {"u251-cibersort-deconvolution", "u251-multiomics-sample-pairing", "u251-name-sweep-traps",
        "u251-project-containment", "u251-translation-fall-il68b", "litt-contralateral-two-readings",
        "cns-abstract-418-deck"}
HISTORY = {"resume-2026-09-21-pm", "resume-2026-09-22-pm", "resume-2026-09-22", "resume-2026-09-24",
           "overnight-2026-09-15-chains", "resume-2026-09-26-handoff"}
BEETHOVEN = {"ashley-bridge-project", "ashley-compliance-boundary", "ashley-extension-project",
             "beethoven-2026-10-02-field-failures", "beethoven-browser-ssh", "beethoven-first-run-ux"}


def main() -> int:
    text = open(H + "working_notes/topic5_operating_here.md", encoding="utf-8").read()
    start = text.index("| note | one line | project | status |")
    block = text[start:].split("\n\n", 1)[0].splitlines()[2:]
    rows = []
    for line in block:
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) != 4:
            print("BAD ROW", line)
            return 1
        rows.append(cells)

    mem_names = sorted(n[:-3] for n in os.listdir(MEM) if n.endswith(".md") and n != "MEMORY.md")
    ctx = set(n[:-3] for n in os.listdir(H + "context") if n.endswith(".md"))
    digest_names = []
    out_rows = []
    for name, line, project, status in rows:
        key = name
        if key.startswith("splits-"):
            key = "splits-" + BANNED + "-and-v3-resplit"
            shown = "splits-origin-and-v3-resplit (original file name carries the banned word)"
        else:
            shown = name
        digest_names.append(key)
        if key in HISTORY or status.startswith("HISTORY"):
            life = "history-only"
        else:
            life = "live"
        if key in U251:
            copied = "no (U251, another project)"
        elif key in HISTORY:
            copied = "no (history-only entry point)"
        elif key in BEETHOVEN:
            copied = "no (Beethoven product note; lives with the Beethoven repo)"
        else:
            target = "splits-origin-and-v3-resplit" if key.startswith("splits-") else key
            copied = "yes" if target in ctx else "MISSING"
        if BANNED in line.lower():
            line = line.replace(BANNED, "origin")
        out_rows.append(f"| `{shown}` | {line} | {project} | {status} | {life} | {copied} |")

    missing_from_digest = sorted(set(mem_names) - set(digest_names))
    extra_in_digest = sorted(set(digest_names) - set(mem_names))
    if missing_from_digest or extra_in_digest:
        print("digest/memory mismatch", missing_from_digest, extra_in_digest)
        return 1
    if any("MISSING" in r for r in out_rows):
        print("a live note was not copied")
        return 1
    n_live = sum(1 for r in out_rows if "| live |" in r)
    n_copied = sum(1 for r in out_rows if r.endswith("| yes |"))

    head = f"""# Context export: the memory notes, and what else lives only in the session

The orchestrating Claude session kept {len(rows)} memory notes plus an index (`MEMORY.md`) in
`memory:`. They are the only record of
many decisions, traps and Greg's verbatim directives. This file digests every one of them and says which were copied into
`HANDOFF/context/` for a fresh Claude project. Built 2026-10-08 by
`scratchpad/handoff/build_context_export.py` from the reader digest in `working_notes/topic5_operating_here.md` §15 (which
was written from the notes themselves) and from the files actually present in `context/`.

## 1. What `context/` holds

- **{n_copied} notes copied, plus `MEMORY.md`** (the original index; its links to notes that were not copied do not resolve
  inside `context/`). Every live note on spine imaging, CTSpinoPelvic1K, SchwingNet, the anomaly scan, data, splits, the
  grid, the toolkit, the website, students, manuscripts, figures and standing preferences is there, including the four
  dormant FluoroCap notes (FluoroCap is out of training by directive D1 but still sits inside the C-arm fold banks, so the
  notes still bear on open work) and the credential-location notes (they name files, never values; a scan for token-shaped
  strings found none).
- **Left out ({len(rows) - n_copied})**: the seven U251 / LITT notes (another project: `u251-*`,
  `litt-contralateral-two-readings`, `cns-abstract-418-deck`), the six history-only entry points (`resume-*`,
  `overnight-2026-09-15-chains`), and the six Beethoven product notes (`ashley-*`, `beethoven-*`), whose content is
  summarised in `INFRASTRUCTURE.md` §2.2 and whose home is the Beethoven repository (`Desktop/ashley-bridge`).
- **One substitution, made on purpose.** Greg bans one word (named in `CTSpinoPelvic1K-1/CLAUDE.md` "Standing
  preferences"). The copies are byte-for-byte identical to the originals except: where a note states the rule, the quoted
  word is replaced by `[the word named in CTSpinoPelvic1K-1/CLAUDE.md "Standing preferences"]` (in `writing-preferences.md`,
  `schwingnet-manuscript.md` and `MEMORY.md`); everywhere else the word became "origin"; and the note whose file name
  carried it is copied as `splits-origin-and-v3-resplit.md`, with every link to it renamed (`MEMORY.md`,
  `ct-benchmark-covers-all-collections.md`, `label-scheme-v4-vs-ostk.md`, `lstv-reread-queue.md`,
  `prone-supine-flexibility-future.md`, `rib-auto-engulf-post-correction-only.md`, `thoracic-gt-fov-limited.md`). The
  copying script is `scratchpad/handoff/copy_context.py`; it refuses if the word survives.

## 2. How a fresh Claude project should load this

1. Put `HANDOFF/README.md`, `HANDOFF/INFRASTRUCTURE.md` and `HANDOFF/context/MEMORY.md` in the project's standing
   instructions or knowledge; add the two repository `CLAUDE.md` files.
2. Load the `context/` notes as reference documents, not as instructions to obey blindly: the "status" column below says
   which are dated or partly superseded, and `README.md` §5 lists the ten rules that bind.
3. Treat every number in a memory note as dated: the result files and `RESULTS_CATALOG.md` win where they disagree
   (examples: `film-ncurve-ablation-result` says all seven separated cells favour renders; the tool's own `READ.md` says six
   help and one hurts; `rsnai-paper-endpoint` calls `main_v2.tex` the culmination; `SchwingNet/main.tex` superseded it).

## 3. Digest of every memory note

Status codes (from the reader digest): CURRENT = a standing rule or a still-valid fact; DATED = a state or result at its
date, check newer files; PARTLY SUPERSEDED = a later file replaces part of it; HISTORY = a superseded entry point; DORMANT
= about FluoroCap, dropped from training 2026-09-23. Project codes: SN = SchwingNet / level identification / fluoroscopy and
films; CTSP = the dataset; ANOM = transitional census and anomaly harvest; DATA = identity, splits, audits, platform; GRID
= cluster; BTH = Beethoven / Ashley (the extension; Ashley Schehr is a person); FC = FluoroCap; OSTK; WEB = website / PACS
demo; LAB = students and annotation; PREF = working rules; CRED = credential locations; REF = literature or external
reference; DECK = talks; U251 = the separate RNA-seq / LITT project.

Counts: {len(rows)} notes; {n_live} live, {len(rows) - n_live} history-only; {n_copied} copied.

| note | one line | project | status | live / history-only | copied to `context/` |
|---|---|---|---|---|---|
"""
    tail = """

## 4. Other context that lives only in the session or outside the repositories

| item | where it lives now | why it matters | source |
|---|---|---|---|
| the memory notes themselves | the memory folder named above | copied here (§1) | — |
| Claude Docs | data report https://claude.ai/code/artifact/74a2ec52-90e4-4f20-82a5-5c8648668676; the Lab Recipe https://claude.ai/code/artifact/03a25fb6-b679-4386-bb04-31f0a965e587; "handoff c3c7acfd..." and "literature state 3b03e849..." (full ids not recorded) | living documents | `context/data-platform-migration-2026-10.md`; `context/lab-recipe-and-board.md` |
| a web copy of the superseded feasibility manuscript | https://claude.ai/artifact/3DFZMHt4oAnrDVHwxdZnyf | history | `context/feasibility-claims-measured.md` |
| the NeurIPS camera-ready recomputation scripts | `laptop-scratchpad:neurips_fixes/cr_apply/` (`crverify*.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py`) | Temp scratchpads can be swept; **copy them into `CTSpinoPelvic1K-1/CAMERA_READY_NEURIPS/`** | `MANUSCRIPTS.md` §7 |
| `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` | named in `CAMERA_READY_CHANGES.md`; found in no scratchpad | the exact wording for cutting Appendices I-J is lost | `working_notes/topic4_manuscripts.md` §7 |
| Beethoven design specs and spikes | session scratchpads (`v11/SPEC.md`, `v11/ssh/design/SSH_DESIGN.md`, `v12/iwa/REPORT.md`, `v12/iwa/STUDENT_STEPS.md`, `v12/iwa/app/dist/beethoven-iwa-0.2.0.swbn`, `rename-beethoven-global.js`) | `V11_CONTRACT.md` / `V12_STATUS.md` in the Beethoven repo carry part of it | Beethoven memory notes |
| the annotator tally script | "`scratchpad/roster.py` pattern" | the only way to count who annotated | `context/annotator-roster.md` |
| workflow journals | `...\\subagents\\workflows\\wf_<id>\\journal.jsonl` (for example wf_ded52e0e-cd1, the transitional review-tree build; wf_babed05b-84a, the anomaly harvest) | resume state of background workflows; a new session can read them, not resume them | `spinesurg-ct-nnunet/docs/RESUME_2026-09-22_PM.md` |
| the resume file | `spinesurg-ct-nnunet/docs/RESUME_2026-09-22_PM.md` (newest block on top, 2026-09-27 18:05; "FOR GREG" decisions at L35-37) | the last session checkpoint of the spine work | — |
| the grid jobs record | `spinesurg-ct-nnunet/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | every job cancelled on 2026-09-27 with how to resume it | — |
| GitHub purge drafts and the TTO package | `Desktop/private_ip/github_purge_requests/`, `Desktop/private_ip/TTO_package_2026-09-25/` | pending filings (Greg) | `context/schwingnet-disclosure-scrub.md` |
| this handoff's working notes | `HANDOFF/working_notes/` (copied from the session scratchpad on 2026-10-08) | the full tables behind every file here | — |

## 5. Memory hygiene a fresh project inherits

`fluorocap-pipeline-resume.md` is not in the `MEMORY.md` index; `ashley-extension-project` and `ashley-bridge-project` are
each linked twice in the index; broken wikilinks: `grid-access` -> `no-login-node-jobs` (the file is
`no-jobs-on-login-node`), `never-reorient-when-writing-labels` -> `ct-spinopelvic-release-gates` (no such note),
`postop-jaggedness-future` -> `postop-spine-synthesis.md` (an extra `.md`); the two "START HERE" bullets at the top of
`MEMORY.md` point at states of 2026-09-28 and 2026-09-26, while newer state lives in
`spinesurg-ct-nnunet/docs/RESUME_2026-09-22_PM.md` (2026-09-27), `context/data-platform-migration-2026-10.md` (2026-10-08)
and the Beethoven repo log (2026-10-03); `lab-recipe-and-board.md` and `student-onboarding-structure.md` put Student_Projects
at `Desktop/Student_Projects` (it is `CTSpinoPelvic1K-1/Student_Projects`) and count 11 unstaffed cards (10)
(`working_notes/topic5_operating_here.md` §13-14).
"""
    with open(H + "CONTEXT_EXPORT.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(head + "\n".join(out_rows) + tail)
    print(f"rows {len(rows)}, live {n_live}, copied {n_copied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
