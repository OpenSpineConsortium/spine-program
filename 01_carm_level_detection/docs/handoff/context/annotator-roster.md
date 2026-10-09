---
name: annotator-roster
description: Who annotated what, from the private review ledgers — 13 students plus Greg, ribs and spine
metadata:
  type: project
---

The only record of who annotated what is the `slots[].reviewer` field inside each
`cases/*.json` in the private `anonymous-mlhc/CTSpinoPelvic1K-reviews-*` ledgers. Count
**done** slots, not claims: an expired claim is not work. Script:
`scratchpad/roster.py` pattern — list `cases/`, read each record, tally by reviewer.

As of 2026-08-23, 13 students completed at least one slot (plus Greg and two `auto:`
pipeline actors, which are not people):

    [per-person usernames and counts withheld here; the full note is in HANDOFF/GREG_ONLY/context/annotator-roster.md]

Ribs and spine are the two tasks with real human work; nerve, iliolumbar, classfix and
triaged have none recorded.

These are **usernames, not names**. Greg is collecting real names for the Medical Physics
author list. Completing slots does not by itself establish authorship — that needs the
journal's criteria met and each person's consent.

Related: [[review-space-repos]], [[hf-org-token-location]], [[publication-roadmap]].
