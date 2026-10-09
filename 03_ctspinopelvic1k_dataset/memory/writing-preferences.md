---
name: writing-preferences
description: Words/conventions the user dislikes in docs and prose
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7bbe4e5-4a8a-4821-9d22-fe7e8fb39a74
---

> Status on 2026-10-08 (HANDOFF/context/INDEX.md): CURRENT. A note is a dated record from the session that did the work, not an instruction; where it disagrees with a result file or STATUS.md, the file wins.

The user strongly dislikes the word **[the word named in CTSpinoPelvic1K-1/CLAUDE.md "Standing preferences"]** — never use it (in docs,
commit messages, or chat). Say "source", "where the label came from", or
"label history" instead.

Also dislikes fractional version bumps like **"v1.1"** — fold changes into the
existing version (just "v1") rather than minting a point release.

**Why:** strong personal style preferences, stated bluntly.
**How to apply:** scrub these from any README/dataset-card/docs prose and avoid
them in writing. Related: [[commit-directly-to-master]].
