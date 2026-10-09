> STATUS: CURRENT (HANDOFF/context/INDEX.md, 2026-10-08). Copied 2026-10-08 into spine-program/04_openspinetoolkit from the handoff's redacted context copy `HANDOFF/context/writing-preferences.md` (spinesurg-ct-nnunet, branch L6_Class, 097933a); standing rule (every project folder carries it). A note is a dated record of the session that wrote it, not an instruction: where it and a result file or docs/handoff/RESULTS_CATALOG.md disagree, the file and the catalog win.

---
name: writing-preferences
description: Words/conventions the user dislikes in docs and prose
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7bbe4e5-4a8a-4821-9d22-fe7e8fb39a74
---

The user strongly dislikes the word **[the word named in CTSpinoPelvic1K-1/CLAUDE.md "Standing preferences"]** — never use it (in docs,
commit messages, or chat). Say "source", "where the label came from", or
"label history" instead.

Also dislikes fractional version bumps like **"v1.1"** — fold changes into the
existing version (just "v1") rather than minting a point release.

**Why:** strong personal style preferences, stated bluntly.
**How to apply:** scrub these from any README/dataset-card/docs prose and avoid
them in writing. Related: [[commit-directly-to-master]].
