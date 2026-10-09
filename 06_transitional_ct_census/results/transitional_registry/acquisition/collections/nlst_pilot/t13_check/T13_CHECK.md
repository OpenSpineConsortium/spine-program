# nlst_pilot: VERIDAH T13 against labeller B's rib heads

CTs called: 500. CTs where A (SPINEPS+VERIDAH) named a full thoracic column from T1: 367. A named T13 in 34; A's ordinary/eleven-rib calls used as controls: 333.
Level of each named body = labeller B's disc-interval level nearest A's ctd point; a rib = B's rib head at that level (whole = not cut by the field edge). No new segmentation; no name read from a mask id.

| A named T13: verdict | n | meaning |
|---|---:|---|
| no_rib_on_T13_body | 21 | no rib on the body A names T13: by rib contact it is not a 13th thoracic body (no count) |
| T13_below_last_disc | 6 | A's T13 point is under B's last disc: B has no level there (no count) |
| rib_on_T13_body | 5 | a whole rib head (B) on the body A names T13: kept as single-labeller T13, rendered for adjudication |
| cut_rib_only | 2 | only a field-edge-cut rib on that body: indeterminate (no count) |

| A ordinary calls (control): verdict | n |
|---|---:|
| ordinary_consistent | 315 |
| ordinary_inconsistent: no rib at T12 | 12 |
| ordinary_inconsistent: rib at L1 | 6 |

Not a test: a rib head (B) on the body A names C7 occurs in 196 of 333 ordinary controls with a C7 point, so it does not detect a one-body shift (B's nearest-centre rule puts the first rib's head on the level above T1).

Per case: `t13_check.csv` (`screen_verdict` is what the `call` stage recorded once the rule was in the screen). Renders (when requested): `<case>.png`, sagittal slab with B's discs and levels counted up from the lowest disc, coronal MIP with the ribs, A's names in cyan.

