# ruleclass design documents (rescued 2026-09-27)

These five files were written 2026-09-27 00:07-02:21 EDT in a Claude session scratchpad while the SUPER DETECTOR RUN
(`/rs/rs_grp_oschome/go2432/ruleclass/`) was being built, and existed nowhere else - not in any repository and not on
the grid (only `TIERS.md` was copied there). The discovery pass of the same day found that the rule definitions for the
pelvis cue (`ARM_B_pelvis.md` sections 7-8), the stump / lowest-rib ratio rule (`STUMP_RULE.md` section 8) and the
sixth-body morphology proposal (`MORPH_API.md` section 6) live only here, and that `CLASSIFIERS.md` is the only
inventory of every transitional classifier tried (R1-R33). They are copied verbatim; nothing was edited.

| file | bytes | what it is |
|---|---:|---|
| `CLASSIFIERS.md` | 282,039 | every classifier / screen tried on the census, R1-R33, with numbers |
| `STUMP_RULE.md` | 43,741 | the stump-rib and lowest-rib / rib-above ratio rule, its literature (Wigh 1980, Moller 2026, Nagata 2025), and the thresholds proposed for `PREREG_rules.md` |
| `MORPH_API.md` | 38,079 | the morphology API over SPINEPS subregions and the T-vs-L shape proposal (Schinz 2026) |
| `ARM_B_pelvis.md` | 22,422 | the Dataset803 pelvis arm: the TTA decision rule, the sacral-anchor rule (f < 0.10 free, 0.10-0.50 contact, >= 0.50 absorbed), the iliac-crest cue |
| `TIERS.md` | 18,559 | how tier 1 / tier 2 / untiered were built (also on the grid at `ruleclass/tiers/TIERS.md`) |

The rule set itself, as Greg stated it on 2026-09-26 23:00, is in `docs/RESUME_2026-09-22_PM.md` L116-122; the two
additions of 2026-09-27 (the lowest-rib / rib-above ratio; the MDPA thoraco-lumbar AUC) are in `PREREG_rules.md`
beside this file once written.
