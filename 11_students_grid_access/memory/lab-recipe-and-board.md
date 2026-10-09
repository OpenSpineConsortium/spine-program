---
name: lab-recipe-and-board
description: "The lab method is written down — Student_Projects/RECIPE.md (+ Claude Doc \"The Lab Recipe\") and the project board board.json → BOARD.md via tools/render_board.py; every lead on the board is a proposal until Greg confirms; Student_Projects commit is local, not pushed"
metadata:
  node_type: memory
  type: project
  originSessionId: f1bdbd78-151f-470b-b703-dd9af9b3fecc
  modified: 2026-09-27T21:15:57.779Z
---

> **Copy record (11_students_grid_access, 2026-10-08).** Status in `HANDOFF/context/INDEX.md`: CURRENT (location and count errors, section 13 rows 1-2). Source: HANDOFF/context (redacted copy set) (context/lab-recipe-and-board.md). Redactions by kind: laptop path (1). Laptop paths are replaced by kind with the placeholders [laptop home], [laptop Desktop] and [laptop project slug]; the live reference is the repository at the commit named. Known errors (INFRASTRUCTURE.md section 13 rows 1-2): the clone is Student_Projects inside the CTSpinoPelvic1K checkout, not a Desktop folder; 10 of 12 cards are unstaffed, not 11.


On 2026-09-27 Greg asked for "the formula I've created for doing AI assisted computational research
with end-to-end papers" as a recipe medical students can run, with leads / co-leads / members who
can move in and out of projects. It is written:

- `[laptop Desktop]\Student_Projects\RECIPE.md` — 12 sections + 2 appendices:
  roles, project shape, PREREG freeze, data rules, refuse-early code + `run_record()`, grid rules
  (14, each with its incident), Nextflow (grid.config, cache-invalidation table, untested DSL2
  skeleton), results → manifest → `\RESULT` → strict build, checking a number, Claude session
  checkpoints, handover/credit, checklists, SchwingNet as the worked example, "what is not yet true".
- `board.json` + `tools/render_board.py` → `BOARD.md`: 12 cards (ctsp1k, schwingnet,
  transitional-review, u251, litt, meded, annotation, toolkit, polypose, website, demo-study,
  fluoro-reading). Validator refuses a card without lead/contact/known state; no co-lead renders
  as UNSTAFFED (11 of 12 are). Ashley Schehr's and Dr Tech's emails are null (not on disk);
  Dr Tech's full name is unknown.
- Claude Doc (living copy for the lab): https://claude.ai/code/artifact/03a25fb6-b679-4386-bb04-31f0a965e587
  — private until Greg shares it.
- Student templates were brought to the house rules in the same commit (reqp --qos=requeue,
  /dev/shm scratch, `set -uo pipefail` with explicit checks, afterany, any-GPU gres). Identifier
  text stays v10 because the public mirror is v10 ([[hf-mirror-is-v10]]).

**Why:** Greg wants students, leads and co-leads to transition in and out of projects seamlessly, and
the method to be reusable across papers; before this, projects were listed in five unlinked places
with no lead/member/contact field.

**How to apply:** New project → card in `board.json`, `python tools/render_board.py`, commit. Point
students at RECIPE.md §0 (join), §2 (PREREG), §5 (grid), §9 (checkpoints), §10 (leave). The commit
`Student_Projects` (main) is LOCAL ONLY — pushing a public repo is Greg's call. Every lead
assignment on the board is a draft for Greg to confirm (meded lead = Ashley per byline order).
Related: [[student-onboarding-structure]], [[submit-and-sleep-orchestration]], [[writing-preferences]].
