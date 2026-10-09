# validation_ts: VERIDAH T13 against labeller B's rib heads

CTs called: 70. CTs where A (SPINEPS+VERIDAH) named a full thoracic column from T1: 38. A named T13 in 9; A's ordinary/eleven-rib calls used as controls: 29.
Level of each named body = labeller B's disc-interval level nearest A's ctd point; a rib = B's rib head at that level (whole = not cut by the field edge). No new segmentation; no name read from a mask id.

| A named T13: verdict | n | meaning |
|---|---:|---|
| rib_on_T13_body | 7 | a whole rib head (B) on the body A names T13: kept as single-labeller T13, rendered for adjudication |
| no_rib_on_T13_body | 2 | no rib on the body A names T13: by rib contact it is not a 13th thoracic body (no count) |

| A ordinary calls (control): verdict | n |
|---|---:|
| ordinary_consistent | 25 |
| ordinary_inconsistent: rib at L1 | 3 |
| ordinary_inconsistent: no rib at T12 | 1 |

Not a test: a rib head (B) on the body A names C7 occurs in 18 of 29 ordinary controls with a C7 point, so it does not detect a one-body shift (B's nearest-centre rule puts the first rib's head on the level above T1).

Per case: `t13_check.csv` (`screen_verdict` is what the `call` stage recorded once the rule was in the screen). Renders (when requested): `<case>.png`, sagittal slab with B's discs and levels counted up from the lowest disc, coronal MIP with the ribs, A's names in cyan.

