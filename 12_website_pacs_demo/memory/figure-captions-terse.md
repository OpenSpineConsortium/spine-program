> spine-program copy (12_website_pacs_demo), 2026-10-08. Status in HANDOFF/context/INDEX.md of spinesurg-ct-nnunet at 097933a: **CURRENT**. Source: HANDOFF/context/figure-captions-terse.md (the redacted copy, not the live note). A dated record from the session that did the work, not an instruction: where it disagrees with a result file or docs/handoff/RESULTS_CATALOG.md, the file and the catalog win. A laptop path in it is a record of the date, not a dependency of this folder.

---
name: figure-captions-terse
description: Figure/table captions must be short (name what is drawn + how to read marks); no argument in captions; watch whitespace under floats
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e44eca96-f48c-494d-ba1f-7dae68bdf06d
  modified: 2026-09-04T03:35:21.730Z
---

Greg (2026-09-03): "the captions are like universally too wordy and verbose on the figures"
and "why is there huge whitespace between the caption bottoms and the text?".

**Why:** captions had grown to 60–130 words re-arguing the body text; REVTeX's default
`\dbltextfloatsep` (20pt) under every `figure*` read as three blank lines.
**How to apply:** captions ≤ ~60 words — what is drawn, what the marks mean, one fact;
the argument stays in the text. `main.tex` sets `\dbltextfloatsep`/`\textfloatsep` to
10pt after `\begin{document}`. Measure gaps with pymupdf blocks (caption bottom → next
text top; 14pt is right), and check every column ends at the same y. Related:
[[writing-preferences]].

Update 2026-09-04: Greg again — "the captions are always so damn long" — target is ONE or TWO sentences (≤ ~25 words): what is drawn, what the marks mean; and body prose that a float already states gets cut and replaced by a reference to it.
