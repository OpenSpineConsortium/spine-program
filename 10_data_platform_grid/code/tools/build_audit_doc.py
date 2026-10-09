# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/build_audit_doc.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Build docs/DATA_COMPLETENESS_AUDIT.md from the audit workflow's journal.

The synthesis agent died on the model limit with 13 of 25 agents finished, so the eight dataset audits and five
verifications are on disk with nothing written from them. This rebuilds the document the synthesis would have
written, from the structured results themselves, and marks what is missing (the verifications and repairs that
never ran) rather than pretending the audit is complete.
"""
import json
import pathlib

J = pathlib.Path(r"<laptop Claude project folder; not a dependency>/subagents/workflows/wf_ba41fa74-07e/journal.jsonl")
OUT = pathlib.Path(r"<repo spinesurg-ct-nnunet 097933a>/docs/DATA_COMPLETENESS_AUDIT.md")

rows = [json.loads(l) for l in J.open(encoding="utf-8")]
audits, verifies = [], []
for r in rows:
    if r.get("type") != "result":
        continue
    v = r.get("result") or {}
    if "gaps" in v:
        audits.append(v)
    elif "recounts" in v:
        verifies.append(v)

ORDER = {"bug": 0, "budget": 1, "unfinished": 2, "unknown": 3, "criterion": 4}
short = lambda s, n=300: " ".join(str(s or "").split())[:n]

gaps = []
for a in audits:
    for g in a.get("gaps", []):
        gaps.append((a.get("dataset", "?"), g))
gaps.sort(key=lambda t: (ORDER.get(t[1].get("reason_class", "unknown"), 5), t[0]))

L = ["# Data completeness audit — what the releases hold, what is on disk, what is used, and why the difference",
     "",
     "Greg, 2026-09-23: *\"are there any more datasets I am truncating because of stupid fucking reasons?\"* — then:",
     "*\"literally every instance of these stupid mistakes should be fixed or justified why they aren't included",
     "before rerunning, except FluoroCap.\"* Eight dataset groups were audited against their release pages and the",
     "grid; five were independently re-counted by a second agent. **The run hit the model limit: the twelve",
     "verification and repair agents named at the end never ran, and the synthesis is this file, written from the",
     "structured results.** No repair job was launched by the audit itself.",
     "",
     "Reason classes: **bug** (a defect in our code or a truncated file), **budget** (a download or compute cut with",
     "no criterion), **unfinished** (a job or push that never completed), **unknown** (nobody can say), **criterion**",
     "(a scientific reason written down somewhere — quoted).",
     "",
     "## Every gap, worst first",
     "",
     "| dataset | gap | missing | class | why | repairable | repair |",
     "|---|---|---|---|---|---|---|"]
for ds, g in gaps:
    L.append("| {} | {} | {} | **{}** | {} | {} | {} |".format(
        short(ds, 60), short(g.get("what"), 220), short(g.get("n_missing"), 60),
        g.get("reason_class", "?"), short(g.get("reason"), 220),
        "yes" if g.get("repairable") else "no", short(g.get("repair_plan"), 220)))

L += ["", "## Truncated for no good reason (bug / budget / unfinished) — these must be repaired or justified", ""]
for ds, g in gaps:
    if g.get("reason_class") in ("bug", "budget", "unfinished"):
        L += ["### {} — {}".format(short(ds, 80), short(g.get("what"), 400)),
              "- missing: {}".format(short(g.get("n_missing"), 200)),
              "- class: {} — {}".format(g.get("reason_class"), short(g.get("reason"), 600)),
              "- repair: {}".format(short(g.get("repair_plan"), 900)), ""]

L += ["## Held back by a written criterion (quoted)", ""]
for ds, g in gaps:
    if g.get("reason_class") == "criterion":
        L += ["- **{}** — {} ({}). Criterion: {} {}".format(
            short(ds, 60), short(g.get("what"), 300), short(g.get("n_missing"), 60),
            short(g.get("reason"), 400), ("QUOTE: " + short(g.get("criterion_quote"), 300)) if g.get("criterion_quote") else "")]

L += ["", "## Unknown — nobody can say why", ""]
n_unknown = 0
for ds, g in gaps:
    if g.get("reason_class") == "unknown":
        n_unknown += 1
        L.append("- **{}** — {} ({}): {}".format(short(ds, 60), short(g.get("what"), 300),
                                                 short(g.get("n_missing"), 60), short(g.get("reason"), 400)))
if not n_unknown:
    L.append("None: every gap found was classed.")

L += ["", "## What each dataset holds, on disk, and in use", ""]
for a in audits:
    L += ["### " + short(a.get("dataset"), 200), "", "| | what | count | source or command |", "|---|---|---|---|"]
    for row in a.get("release", []):
        L.append("| release | {} | {} | {} |".format(short(row.get("what"), 150), short(row.get("count"), 80), short(row.get("source"), 200)))
    for row in a.get("on_disk", []):
        L.append("| on disk | {} | {} | `{}` |".format(short(row.get("path"), 150), short(row.get("count"), 80), short(row.get("command"), 200)))
    for row in a.get("used", []):
        L.append("| used | {} | {} | {} |".format(short(row.get("where"), 150), short(row.get("count"), 80), short(row.get("evidence"), 200)))
    L.append("")
    if a.get("doc_disagreements"):
        L.append("Documents that disagree with the disk:")
        L += ["- " + short(d, 400) for d in a["doc_disagreements"]]
        L.append("")

L += ["## Independent re-counts (the verifications that ran)", ""]
for v in verifies:
    L += ["### " + short(v.get("dataset"), 200), "", "**Verdict.** " + short(v.get("verdict"), 1200), ""]
    dis = [r for r in v.get("recounts", []) if not r.get("agrees")]
    if dis:
        L.append("Re-counts that DISAGREE with the auditor:")
        L += ["- {} → verifier got {} (`{}`)".format(short(r.get("claim"), 200), short(r.get("my_count"), 80), short(r.get("command"), 200)) for r in dis]
        L.append("")
    if v.get("reclassified"):
        L.append("Reclassified gaps:")
        L += ["- {}: auditor **{}** → verifier **{}** — {}".format(short(r.get("gap"), 200), r.get("auditor_class"), r.get("my_class"), short(r.get("why"), 400)) for r in v["reclassified"]]
        L.append("")
    if v.get("missed_gaps"):
        L.append("Gaps the auditor missed:")
        L += ["- " + short(m, 400) for m in v["missed_gaps"]]
        L.append("")

verified = {short(v.get("dataset"), 40) for v in verifies}
L += ["## What this audit still owes", "",
      "- Verification did not run for the groups not listed above (the model limit stopped them): their gap",
      "  classes rest on one agent's reading.",
      "- No repair job was launched by the audit. Every repair above is a plan, not a running job.",
      "- FluoroCap is dropped from training by PI decision, so its gaps need no repair — only the datasheet line.",
      ""]
OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("wrote", OUT, len(gaps), "gaps;", len(audits), "audits,", len(verifies), "verifications")
from collections import Counter
print(Counter(g.get("reason_class") for _, g in gaps))
print("datasets:", [short(a.get("dataset"), 50) for a in audits])
