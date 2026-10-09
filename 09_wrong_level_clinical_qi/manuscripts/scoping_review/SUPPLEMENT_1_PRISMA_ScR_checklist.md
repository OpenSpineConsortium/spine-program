# Supplement 1 — PRISMA-ScR checklist

For: *Wrong-level and wrong-site spine surgery: mechanisms, the imaging step that fails, and decision support — a
scoping review*. Draft of 15 September 2026, against manuscript version 0.2.

Each item gives where it is reported and, where the item is not yet satisfiable, says so plainly rather than
pointing at a section that does not answer it. Seven items are open at this draft; they are listed again at the
end so that none is lost at submission.

| # | Item | Where reported | State |
|---|---|---|---|
| 1 | **Title** identifies the report as a scoping review | Title | done |
| 2 | **Structured summary** (background, objectives, eligibility, sources, charting methods, results, conclusions) | Abstract | **open** — written last, to the PRISMA-ScR abstract checklist |
| 3 | **Rationale** for the review in the context of what is already known | Introduction, paragraphs 1–4 | done |
| 4 | **Objectives**, with the question stated in terms of population, concept and context | Introduction, final paragraph; Protocol §2 | done |
| 5 | **Protocol and registration**: whether a protocol exists, where it can be accessed, and registration details | Methods, *Protocol and registration*; Supplement 2 | done — and it states that the protocol is **post hoc** and **not prospectively registered** |
| 6 | **Eligibility criteria**, with rationale | Methods, *Eligibility criteria*; machine-readable form in `criteria.json` | done |
| 7 | **Information sources**, with date last searched | Methods, *Information sources and search*: Europe PMC and Semantic Scholar, both searched 15 September 2026 | done |
| 8 | **Search**: the full electronic search strategy for at least one database, repeatable | Supplement 3, verbatim query; also the constant `QUERY_EXTRA` in the released code | done |
| 9 | **Selection of sources of evidence**: the process, and how many reviewers | Methods, *Selection of sources of evidence*; ledger in Supplement 4 | **partly open** — the three-stage process is described, but stages 2 and 3 have not been executed |
| 10 | **Data charting process**, including whether it was independent and in duplicate | Methods, *Data charting* | **open** — the form is defined and an automated first pass exists; human charting has not been done |
| 11 | **Data items**: what was charted and how defined | Methods, *Data charting*; field list in `extraction.jsonl` | done |
| 12 | **Critical appraisal of individual sources** | Methods, *Synthesis of results*: none performed | done — PRISMA-ScR does not require it; the consequence is stated in Limitations |
| 13 | **Synthesis of results**: methods of handling and summarising the data | Methods, *Synthesis of results* | done, including the pre-stated condition under which no pooled estimate would be reported |
| 14 | **Selection of sources of evidence**: numbers screened, assessed and included, with reasons, ideally with a flow diagram | Results, *Selection of sources of evidence*; Figure 1; Table 1 | done — 12,294 identified, 11,980 screened, 665 included |
| 15 | **Characteristics of sources of evidence** | Table 2 | **partly open** — design mix is computed; country, era and setting await human charting |
| 16 | **Critical appraisal within sources** | not applicable | done |
| 17 | **Results of individual sources of evidence** relevant to the question | Tables 3–6 | **open** — automated first pass exists, human charting pending |
| 18 | **Synthesis of results** | Results, *Reported frequency, and why it is not pooled*; Tables 3–6; Figure 2 | **partly open** — the decision not to pool is reported with its reasoning; the descriptive tables await charting |
| 19 | **Summary of evidence**: main results including their relevance to key groups | Discussion | drafted against the expected findings, to be rewritten from the charted table |
| 20 | **Limitations** | Limitations | done |
| 21 | **Conclusions**, including implications | Discussion, final section; *What this review cannot do* | done |
| 22 | **Funding**: sources of funding and role of funders | Declarations | **open** |

## The seven open items, restated

1. **Item 2** — abstract, written last.
2. **Item 9** — the 200-record validation sample has not been screened by two humans, so no screening performance
   can be stated, and the corpus re-screen that a sensitivity below 0.90 would trigger has not been ruled out.
3. **Item 10** — no human charting has been performed; every charted value is currently a first pass by pattern.
4. **Item 15** — country, era and setting are not yet charted.
5. **Item 17** — per-source results await charting.
6. **Item 18** — the descriptive tables await charting; the non-pooling decision is already reported.
7. **Item 22** — funding statement.

## A note on machine assistance, for the editor

Screening and the first charting pass were performed by explicit pattern-matching code, not by a language model,
and every decision is stored with the exact strings that produced it, so any reader can audit why a record was
kept or dropped. This is described in the Methods rather than only acknowledged. Four extraction defects found
during development are recorded in the released code's history: veterinary papers admitted because they use the
same clinical vocabulary as human studies; a year read as an event count; a seven-figure denominator truncated;
and counts drawn from neighbouring cells of flattened tables. Each was found by reading output rather than by a
test passing, which is the reason the validation sample and human charting are treated as required rather than
optional.
