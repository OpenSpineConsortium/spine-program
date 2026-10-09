# The one transitional registry: one row per person

Built 2026-09-24 11:07 by `tools/transitional_registry.py`. Every number below is computed from the files listed here; none is typed by hand. `registry.csv` / `registry.json` carry one row per person; this file is the reading of them.

> Note on this copy (2026-10-08, `../../MANIFEST_LOCAL.md` section 2): the input, queue and contact-sheet paths under `meta` in `registry.json` are written repository-relative, `sn:results/...` (`sn:` = `SchwingNet/` in spinesurg-ct-nnunet 097933a, `../../docs/handoff/README_PREFIXES.md`); the original carried laptop paths. `persons` is untouched.

## Inputs

| stream | rows.csv | rows | written | note |
|---|---:|---:|---:|---:|
| verse | verse/rows.csv | 171 | 2026-09-23 20:36 | screened.csv adds 203 negatives (of 374 series) |
| ctsp | ctsp/rows.csv | 64 | 2026-09-24 06:17 |  |
| totalsegmentator | totalsegmentator/rows.csv | 1935 | 2026-09-24 07:19 |  |
| cobra | cobra/rows.csv | 692 | 2026-09-24 06:49 |  |
| other_ct | other_ct/rows.csv | 3066 | 2026-09-24 08:47 |  |
| acquisition | (none) |  |  | no rows.csv: not a row stream |

Today's table: `rare_class/transitional_subtypes.csv` (196 rows, 194 persons) and `rare_class/ts12_ctd_subtypes.json` (12 TotalSegmentator cases corrected by the VERIDAH ctd; 195 persons after). Aliases: `other_ct/alias_rows.csv`; VerSe series -> subject: `verse/screened.csv`.

## How persons were formed

- Rows read: 6131; persons: 6108; phantoms kept as rows but not counted as people: 5; table-only persons (no stream row): 1.
- Alias edges declared (`other_ct/alias_rows.csv`, CTSpine1K COLONOG volume -> CTSpinoPelvic1K record): 782; written on a registry person: 56; pointing at a CTSpinoPelvic1K person with no local row (a CTSP negative, on the grid census): 726. Rows re-keyed through an edge while reading: none (the other_ct stream had already left those rows to the ctsp stream). Persons carrying an alias name: 56.
- Persons with more than one scan: 18: verse:verse403 (2), verse:verse406 (2), verse:verse410 (2), verse:verse415 (2), verse:verse417 (2), verse:verse400 (2), verse:verse401 (2), verse:verse402 (2), verse:verse404 (2), verse:verse405 (3), verse:verse407 (2), verse:verse408 (2), verse:verse409 (2), verse:verse411 (2), verse:verse412 (2), verse:verse413 (2), verse:verse414 (2), verse:verse416 (2).
- Persons with rows in more than one stream: 0. Persons whose scans or streams disagree on the subtype (the higher tier won, the loser is in `other_calls`): 0. The streams partition persons: the only cross-stream overlap, the CTSpine1K COLONOG volumes, was left to the ctsp stream by the other_ct stream before it wrote rows (the edges above), and the VerSe subjects with several series agree with themselves.
- Tier order read > two-labeller > single-labeller > morphology-only > none; at equal tier a positive beats unresolved beats none beats no_count; then source order ctsp, verse, totalsegmentator, cobra2026, other_ct sources. A `no_count` row abstains and never counts as a disagreement.
- TotalSegmentator ships no patient id (a scan is a person); RibFrac ships none (a case is a person); C-ArmLSpine cases are acquisitions from day-grouped lists, not proven persons; RSNA studies are persons. These are the streams' own statements and are carried, not re-derived.

## Distinct people per subtype x truth tier x source x (CT-only | real-frames/TEST)

Every person counted once, under the subtype and tier that won. Real-frame persons (COBRA, C-ArmLSpine, DeepFluoro, Geneva, SpineSAC, Ljubljana) are TEST only and are never rendered for training.

### A. Subtype x tier (persons), CT-only / real-frames

| subtype | read | two-labeller | single-labeller | morphology-only | none | CT-only / real | persons |
|---|---:|---:|---:|---:|---:|---:|---:|
| L6 | 103 / 0 | 27 / 2 | 9 / 1 | 1 / 3 |  | 140 / 6 | 146 |
| T13 | 6 / 0 | 3 / 0 | 5 / 0 |  |  | 14 / 0 | 14 |
| sacralised_L5_fused | 27 / 0 |  |  |  |  | 27 / 0 | 27 |
| castellvi_I_II | 31 / 0 |  |  |  |  | 31 / 0 | 31 |
| lumbar_rib | 12 / 0 | 9 / 0 | 5 / 0 |  |  | 26 / 0 | 26 |
| unassigned | 23 / 0 | 13 / 4 | 19 / 3 |  |  | 55 / 7 | 62 |
| unresolved |  |  |  |  | 118 / 11 | 118 / 11 | 129 |
| none | 143 / 0 | 1231 / 112 | 128 / 68 |  | 4 / 0 | 1506 / 180 | 1686 |
| no_count | 15 / 0 |  |  |  | 3328 / 644 | 3343 / 644 | 3987 |

### B. Subtype x source (persons); a source marked TEST holds real projections

| subtype | ctsp | table:ctsp | verse | totalsegmentator | cobra2026 (TEST) | carmlspine (TEST) | ctspine1k | ribfrac | rsna_cspine | deepfluoro (TEST) | ljubljana (TEST) | persons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L6 | 29 |  | 85 | 22 | 3 | 3 | 3 | 1 |  |  |  | 146 |
| T13 |  |  | 6 | 4 |  |  |  | 4 |  |  |  | 14 |
| sacralised_L5_fused | 12 |  | 13 |  |  |  | 2 |  |  |  |  | 27 |
| castellvi_I_II | 4 |  | 27 |  |  |  |  |  |  |  |  | 31 |
| lumbar_rib | 14 |  | 12 |  |  |  |  |  |  |  |  | 26 |
| unassigned | 5 |  | 23 | 26 | 6 | 1 |  | 1 |  |  |  | 62 |
| unresolved |  |  |  | 74 | 11 |  | 15 | 29 |  |  |  | 129 |
| none |  | 1 | 146 | 622 | 175 | 5 | 146 | 591 |  |  |  | 1686 |
| no_count |  |  | 43 | 1187 | 497 | 140 | 57 | 34 | 2022 | 6 | 1 | 3987 |
| all | 64 | 1 | 355 | 1935 | 692 | 149 | 223 | 660 | 2022 | 6 | 1 | 6108 |

### C. The full cross, long form (only non-zero cells)

| subtype | tier | source | frames | persons |
|---|---:|---:|---:|---:|
| L6 | read | ctsp | CT-only | 17 |
| L6 | read | verse | CT-only | 85 |
| L6 | read | ctspine1k | CT-only | 1 |
| L6 | two-labeller | ctsp | CT-only | 11 |
| L6 | two-labeller | totalsegmentator | CT-only | 14 |
| L6 | two-labeller | cobra2026 | real-frames/TEST | 2 |
| L6 | two-labeller | ctspine1k | CT-only | 2 |
| L6 | single-labeller | ctsp | CT-only | 1 |
| L6 | single-labeller | totalsegmentator | CT-only | 8 |
| L6 | single-labeller | cobra2026 | real-frames/TEST | 1 |
| L6 | morphology-only | carmlspine | real-frames/TEST | 3 |
| L6 | morphology-only | ribfrac | CT-only | 1 |
| T13 | read | verse | CT-only | 6 |
| T13 | two-labeller | totalsegmentator | CT-only | 3 |
| T13 | single-labeller | totalsegmentator | CT-only | 1 |
| T13 | single-labeller | ribfrac | CT-only | 4 |
| sacralised_L5_fused | read | ctsp | CT-only | 12 |
| sacralised_L5_fused | read | verse | CT-only | 13 |
| sacralised_L5_fused | read | ctspine1k | CT-only | 2 |
| castellvi_I_II | read | ctsp | CT-only | 4 |
| castellvi_I_II | read | verse | CT-only | 27 |
| lumbar_rib | read | verse | CT-only | 12 |
| lumbar_rib | two-labeller | ctsp | CT-only | 9 |
| lumbar_rib | single-labeller | ctsp | CT-only | 5 |
| unassigned | read | verse | CT-only | 23 |
| unassigned | two-labeller | ctsp | CT-only | 5 |
| unassigned | two-labeller | totalsegmentator | CT-only | 8 |
| unassigned | two-labeller | cobra2026 | real-frames/TEST | 4 |
| unassigned | single-labeller | totalsegmentator | CT-only | 18 |
| unassigned | single-labeller | cobra2026 | real-frames/TEST | 2 |
| unassigned | single-labeller | carmlspine | real-frames/TEST | 1 |
| unassigned | single-labeller | ribfrac | CT-only | 1 |
| unresolved | none | totalsegmentator | CT-only | 74 |
| unresolved | none | cobra2026 | real-frames/TEST | 11 |
| unresolved | none | ctspine1k | CT-only | 15 |
| unresolved | none | ribfrac | CT-only | 29 |
| none | read | verse | CT-only | 143 |
| none | two-labeller | totalsegmentator | CT-only | 584 |
| none | two-labeller | cobra2026 | real-frames/TEST | 112 |
| none | two-labeller | ctspine1k | CT-only | 118 |
| none | two-labeller | ribfrac | CT-only | 529 |
| none | single-labeller | totalsegmentator | CT-only | 38 |
| none | single-labeller | cobra2026 | real-frames/TEST | 63 |
| none | single-labeller | carmlspine | real-frames/TEST | 5 |
| none | single-labeller | ctspine1k | CT-only | 28 |
| none | single-labeller | ribfrac | CT-only | 62 |
| none | none | verse | CT-only | 3 |
| none | none | table:ctsp | CT-only | 1 |
| no_count | read | verse | CT-only | 15 |
| no_count | none | verse | CT-only | 28 |
| no_count | none | totalsegmentator | CT-only | 1187 |
| no_count | none | cobra2026 | real-frames/TEST | 497 |
| no_count | none | carmlspine | real-frames/TEST | 140 |
| no_count | none | ctspine1k | CT-only | 57 |
| no_count | none | ribfrac | CT-only | 34 |
| no_count | none | rsna_cspine | CT-only | 2022 |
| no_count | none | deepfluoro | real-frames/TEST | 6 |
| no_count | none | ljubljana | real-frames/TEST | 1 |

Modifiers (persons): four_lumbar 38; lumbar_rib (modifier, any subtype) 65; castellvi grade recorded 142; castellvi candidate (morphology, not a grade) 131.

both_L6_T13 was looked for in every stream: 0 persons.

### D. Which of these persons sit in a review queue (a candidate until a person reads it)

| subtype | tier | persons | in a review queue | not queued |
|---|---:|---:|---:|---:|
| L6 | read | 103 | 48 | 55 |
| L6 | two-labeller | 29 | 28 | 1 |
| L6 | single-labeller | 10 | 10 | 0 |
| L6 | morphology-only | 4 | 4 | 0 |
| T13 | read | 6 | 3 | 3 |
| T13 | two-labeller | 3 | 3 | 0 |
| T13 | single-labeller | 5 | 5 | 0 |
| sacralised_L5_fused | read | 27 | 10 | 17 |
| castellvi_I_II | read | 31 | 10 | 21 |
| lumbar_rib | read | 12 | 3 | 9 |
| lumbar_rib | two-labeller | 9 | 1 | 8 |
| lumbar_rib | single-labeller | 5 | 5 | 0 |
| unassigned | read | 23 | 7 | 16 |
| unassigned | two-labeller | 17 | 17 | 0 |
| unassigned | single-labeller | 22 | 22 | 0 |
| unresolved | none | 129 | 129 | 0 |
| none | read | 143 | 9 | 134 |
| none | two-labeller | 1343 | 27 | 1316 |
| none | single-labeller | 196 | 27 | 169 |
| none | none | 4 | 2 | 2 |

## Before vs after: today's table against the registry

BEFORE = `transitional_subtypes.csv` as it stands (raw) and with `ts12_ctd_subtypes.json` applied to its TotalSegmentator cases (the TS correction). AFTER = this registry. Persons, not rows.

| subtype | table raw | table + TS corr. | registry | kept | moved to another subtype | dropped (not positive now) | new (not in table) | new here from another subtype |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| L6 | 110 | 109 | 146 | 106 | 0 | 3 | 40 | 0 |
| T13 | 7 | 9 | 14 | 7 | 0 | 2 | 7 | 0 |
| both_L6_T13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sacralised_L5_fused | 28 | 28 | 27 | 25 | 3 | 0 | 2 | 0 |
| castellvi_I_II | 31 | 31 | 31 | 31 | 0 | 0 | 0 | 0 |
| lumbar_rib | 14 | 14 | 26 | 14 | 0 | 0 | 12 | 0 |
| unassigned | 4 | 4 | 62 | 3 | 0 | 1 | 56 | 3 |
| all positive | 194 | 195 | 306 |  |  |  |  |  |

### Every person whose call changed, with the stream's reason

9 table persons changed subtype and 117 positive persons are new to the registry. Table subtype -> registry subtype (tier): reason.

- `ctsp:1043`: unassigned -> **none** (none): in today's table only, no stream row: ctsp/review_queue/review_queue.csv: priority=2-unassigned; subtype=unassigned; tier=single-labeller; why=4 lumbar ids, no read; votes A=5 B=5 C=5; RESOLVED as a labelling artefact, n
- `ts:s1088`: T13 -> **unresolved** (none): TotalSegmentator stream: [totalsegmentator:TS_s1088] DISCORDANT: A (VERIDAH ctd) T13 (lumbar 5, rib-bearing T13) vs B (TS geometry) L6 (lumbar L6, rib-bearing 12) / both count 18 thoracolumbar bodies: they disagree on WHICH body carries the last
- `ts:s1123`: T13 -> **unresolved** (none): TotalSegmentator stream: [totalsegmentator:TS_s1123] DISCORDANT: A (VERIDAH ctd) T13 (lumbar -, rib-bearing T13) vs B (TS geometry) none (lumbar -, rib-bearing 12) / claimed: T13 by A; unresolved until read / 13 rib-bearing; the lumbosacral junc
- `ts:s1178`: L6 -> **unresolved** (none): TotalSegmentator stream: [totalsegmentator:TS_s1178] DISCORDANT: A (VERIDAH ctd) L6 (lumbar L6, rib-bearing 11) vs B (TS geometry) none (lumbar 5, rib-bearing 12) / both count 17 thoracolumbar bodies: they disagree on WHICH body carries the last
- `verse:gl279`: L6 -> **none** (none): verse audit: HELD FOR REVIEW (no row until adjudicated): labellers disagree: A four_lumbar vs B normal_count; release mask L6
- `verse:verse549`: sacralised_L5_fused -> **unassigned** (read): verse audit: MOVED sacralised_L5_fused -> unassigned: read, voxel-verified: mask lumbar ids + unlabelled bodies below = 4; A counts 4 lumbar; B counts 4 lumbar (38 mm rule); B counts 4 rib-free bodies below the last rib (rib contact); A counts 12 thoracic; B counts 12 thoracic (38 mm rule); B counts 12 rib-bearing bodies from T1 (rib contact)
- `verse:verse552`: sacralised_L5_fused -> **unassigned** (read): verse audit: MOVED sacralised_L5_fused -> unassigned: read, voxel-verified: mask lumbar ids + unlabelled bodies below = 4; A counts 4 lumbar; B counts 4 lumbar (38 mm rule); B counts 4 rib-free bodies below the last rib (rib contact); A counts 12 thoracic
- `verse:verse559`: sacralised_L5_fused -> **unassigned** (read): verse audit: MOVED sacralised_L5_fused -> unassigned: read, CONTRADICTED by mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm) / 5 rib-free (contact)
- `verse:verse707`: L6 -> **none** (none): verse audit: HELD FOR REVIEW (no row until adjudicated): read NORMAL but release mask carries an L6 (id 25)
- `carmlspine:case97`: (not in table) -> **unassigned** (single-labeller): [carmlspine:case97] lumbar CBCT; case = acquisition, not proven person (day-grouped folds) / B: lowest rib-bearing body's ribs all < 38 mm ({'left': 30.9}): a stump by the VerSe convention (hypoplastic last rib or lumbar
- `cobra:A270`: (not in table) -> **L6** (single-labeller): [cobra2026:A270] only A could count; B: no_count (count refused, a split body: two bodies of the chain [T12:100%] and [L1:100%] are 14 mm apart against a median step of 3); B notes: a 60 mm body piece with no disc valley
- `cobra:B084`: (not in table) -> **unassigned** (single-labeller): [cobra2026:B084] only A could count; B: no_count (count refused, a split body: two bodies of the chain [L3:100%] and [L4:100%] are 12 mm apart against a median step of 27); B notes: a 68 mm body piece with no disc valley
- `cobra:B091`: (not in table) -> **unassigned** (single-labeller): [cobra2026:B091] only A could count; B: no_count (thoracolumbar reference not established: the last rib-bearing object [T12:73%/T11:27%] is cut by the field's cranial edg); B's free bodies below its unestablished referen
- `cobra:B127`: (not in table) -> **L6** (two-labeller): [cobra2026:B127] B notes: a 56 mm body piece split at 1 disc valley(s) / a 72 mm body piece with no disc valley was split by 3 TS labels / a 164 mm body piece split at 3 disc valley(s) / TS label objects give 5 free vert
- `cobra:D014`: (not in table) -> **unassigned** (two-labeller): [cobra2026:D014] B notes: a 60 mm body piece split at 1 disc valley(s) / TS label objects give 5 free vertebrae between the same references (disc-split objects give 4); VERIDAH named T13; T1 not in the field, so no thora
- `cobra:D238`: (not in table) -> **L6** (two-labeller): [cobra2026:D238] B notes: a 63 mm body piece with no disc valley was split by 3 TS labels / a 129 mm body piece split at 2 disc valley(s) / free object [L5:100%] has its body centre below the sacral midline top (tilted t
- `cobra:D484`: (not in table) -> **unassigned** (two-labeller): [cobra2026:D484] B notes: TS label objects give 5 free vertebrae between the same references (disc-split objects give 4) / short ribs on the last rib-bearing vertebra (longest 50 mm); Castellvi mask morphology (not a rea
- `cobra:F058`: (not in table) -> **unassigned** (two-labeller): [cobra2026:F058] B notes: a 165 mm body piece with no disc valley was split by 5 TS labels / a 186 mm body piece split at 1 disc valley(s) / a 69 mm body piece split at 2 disc valley(s) / split pair: rib_left_7 moved fro
- `cobra:F089`: (not in table) -> **unassigned** (two-labeller): [cobra2026:F089] B notes: a 60 mm body piece split at 1 disc valley(s) / TS label objects give 5 free vertebrae between the same references (disc-split objects give 4); Castellvi mask morphology (not a read; does not dis
- `ctsp:0090`: (not in table) -> **L6** (two-labeller): [ctsp:0090] release spine labels are pseudo-labels (prov_spine=pseudo), not manual / CANDIDATE the release did not call (two-labeller): votes A=no count B=6 C=6 -> review queue / release label L2 (91.79 ml) spans 2 verte
- `ctsp:0105`: (not in table) -> **L6** (two-labeller): [ctsp:0105] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:0150`: (not in table) -> **L6** (single-labeller): [ctsp:0150] CANDIDATE the release did not call (single-labeller): votes A=5 B=6 C=no count -> review queue / release label L3 (80.15 ml) spans 2 vertebra-sized SPINEPS instances (two vertebrae under one release id?) / re
- `ctsp:0349`: (not in table) -> **unassigned** (two-labeller): [ctsp:0349] CANDIDATE the release did not call (two-labeller): votes A=5 B=4 C=4 -> review queue / LOOKED (Claude, renders; not a read): SPINEPS and TotalSegmentator each find four rib-free bodies between the vertebra be
- `ctsp:0359`: (not in table) -> **L6** (two-labeller): [ctsp:0359] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:0474`: (not in table) -> **L6** (two-labeller): [ctsp:0474] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=6 -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above the sacr
- `ctsp:0544`: (not in table) -> **L6** (two-labeller): [ctsp:0544] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:0552`: (not in table) -> **L6** (two-labeller): [ctsp:0552] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:0672`: (not in table) -> **L6** (two-labeller): [ctsp:0672] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:0895`: (not in table) -> **L6** (two-labeller): [ctsp:0895] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:1000`: (not in table) -> **unassigned** (two-labeller): [ctsp:1000] CANDIDATE the release did not call (two-labeller): votes A=5 B=4 C=4 -> review queue / the rib source changes the release count: release ribs 5, TotalSegmentator ribs 6 / VERIDAH's names count 5 where SPINEPS
- `ctsp:1151`: (not in table) -> **L6** (two-labeller): [ctsp:1151] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=no count -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above t
- `ctsp:1153`: (not in table) -> **L6** (two-labeller): [ctsp:1153] CANDIDATE the release did not call (two-labeller): votes A=6 B=6 C=6 -> review queue / L6 by the rib convention: the vertebra the release names T12 carries no rib, so six rib-free vertebrae sit above the sacr
- `ctspine1k:MSD-T10:liver_106`: (not in table) -> **L6** (read): [ctspine1k:MSD-T10/liver_106] MSD-T10 / CTSpine1K README expert list: L6 / release annotation carries id 25 / B: 1 rib attachment(s) moved by the order/pair rule / B lumbar count carries an inferred gap or a possible mer
- `ctspine1k:MSD-T10:liver_119`: (not in table) -> **L6** (two-labeller): [ctspine1k:MSD-T10/liver_119] MSD-T10 / release annotation: 5 lumbar ids (L1-L5); the same bodies read 11 rib-bearing + 6 rib-free when its T12 carries no rib (L6 by the rib convention, 24 presacral) / B lumbar count car
- `ctspine1k:MSD-T10:liver_83`: (not in table) -> **sacralised_L5_fused** (read): [ctspine1k:MSD-T10/liver_83] MSD-T10 / CTSpine1K README expert list: sacralisation / B: 2 rib attachment(s) moved by the order/pair rule / the release labels no sacrum: the fused body carries no id (fused_mask_representa
- `ctspine1k:MSD-T10:liver_93`: (not in table) -> **sacralised_L5_fused** (read): [ctspine1k:MSD-T10/liver_93] MSD-T10 / CTSpine1K README expert list: sacralisation / the release labels no sacrum: the fused body carries no id (fused_mask_representation 'unlabelled', as in the VerSe stream) / Castellvi
- `ctspine1k:MSD-T10:liver_95`: (not in table) -> **L6** (two-labeller): [ctspine1k:MSD-T10/liver_95] MSD-T10 / release annotation: 5 lumbar ids (L1-L5); the same bodies read 11 rib-bearing + 6 rib-free when its T12 carries no rib (L6 by the rib convention, 24 presacral) / B lumbar count carr
- `ribfrac:RibFrac101`: (not in table) -> **T13** (single-labeller): [ribfrac:RibFrac101] sacrum not in the field: 13 rib-bearing counted from T1 is T13 (25 presacral) OR a rib on L1 (24 presacral, lumbar_rib); the lumbar count below is unknown / B rib-bearing count carries an inferred bo
- `ribfrac:RibFrac322`: (not in table) -> **T13** (single-labeller): [ribfrac:RibFrac322] sacrum not in the field: 13 rib-bearing counted from T1 is T13 (25 presacral) OR a rib on L1 (24 presacral, lumbar_rib); the lumbar count below is unknown / B rib-bearing count carries an inferred bo
- `ribfrac:RibFrac482`: (not in table) -> **L6** (morphology-only): [ribfrac:RibFrac482] B lumbar count carries an inferred gap or a possible merge / LS: VERIDAH names it; no count in the field / looked (Claude, closer render, not a radiologist read): 12 rib pairs on T1-T12 (A and B agre
- `ribfrac:RibFrac488`: (not in table) -> **unassigned** (single-labeller): [ribfrac:RibFrac488] count outside the defined subtypes (TL=normal, LS=odd:3) / LS: only B counts (A=no_count)
- `ribfrac:RibFrac539`: (not in table) -> **T13** (single-labeller): [ribfrac:RibFrac539] B: 3 rib attachment(s) moved by the order/pair rule / sacrum not in the field: 13 rib-bearing counted from T1 is T13 (25 presacral) OR a rib on L1 (24 presacral, lumbar_rib); the lumbar count below i
- `ribfrac:RibFrac93`: (not in table) -> **T13** (single-labeller): [ribfrac:RibFrac93] B: 4 rib attachment(s) moved by the order/pair rule / sacrum not in the field: 13 rib-bearing counted from T1 is T13 (25 presacral) OR a rib on L1 (24 presacral, lumbar_rib); the lumbar count below is
- `ts:s0049`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0049] thoracic count not in the FOV (T13 not excluded) / TS L3 counted as 2 bodies (height x1.89, rib2=False, dip=119.0) / B's sixth free body: one TS label holds two bodies (B split it by height/di
- `ts:s0059`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0059] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s0077`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0077] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s0098`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s0098] labeller B gave no count: implausible count (rib-bearing 1): a segmentation defect until a human says otherwise / implausible count (rib-bearing 1): a segmentation defect until a human says ot
- `ts:s0109`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s0109] labeller B gave no count: implausible count (rib-bearing 4): a segmentation defect until a human says otherwise / implausible count (rib-bearing 4): a segmentation defect until a human says ot
- `ts:s0131`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s0131] 11 rib-bearing + 5 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 1): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s0158`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0158] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: TS names it T12, but TS's rib_12 sits on the body above it: TS's rib and vertebra numbering disagree by one
- `ts:s0161`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s0161] labeller B gave no count: implausible count (rib-bearing 2): a segmentation defect until a human says otherwise / implausible count (rib-bearing 2): a segmentation defect until a human says ot
- `ts:s0171`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s0171] thoracic count not in the FOV (T13 not excluded)
- `ts:s0308`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s0308] 11 rib-bearing + 5 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 7): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s0436`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s0436] 12 rib-bearing + 4 rib-free = 23 presacral bodies / labeller B on the v201 masks of the same CT reads lumbar_rib (lumbar four, rib-bearing T13)
- `ts:s0446`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0446] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s0456`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s0456] lowest rib 37.3 mm (< 40): lumbar-rib / hypoplastic-rib candidate, morphology only / thoracic count not in the FOV (T13 not excluded) / labeller B on the v201 masks of the same CT reads no_cou
- `ts:s0461`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s0461] thoracic count not in the FOV (T13 not excluded)
- `ts:s0477`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0477] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: TS names it T12 and gives it no rib (11 TS rib pairs): an L6 by the rib convention, a rib-less T12 by TS's count -- 24 o
- `ts:s0603`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s0603] thoracic count not in the FOV (T13 not excluded) / labeller B on the v201 masks of the same CT reads none (lumbar 5, rib-bearing -)
- `ts:s0644`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s0644] lowest rib 37.4 mm (< 40): lumbar-rib / hypoplastic-rib candidate, morphology only / thoracic count not in the FOV (T13 not excluded)
- `ts:s0683`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0683] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: TS names it T12 and gives it no rib (11 TS rib pairs): an L6 by the rib convention, a rib-less T12 by TS's count -- 24 o
- `ts:s0723`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0723] B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (TS has no T13 class, so this means 25 presacral bodi
- `ts:s0733`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0733] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s0749`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0749] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s0806`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s0806] 12 rib-bearing + 4 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 7): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s0940`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s0940] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s1023`: (not in table) -> **T13** (two-labeller): [totalsegmentator:TS_s1023] 13 rib-bearing; the lumbosacral junction is not countable here / the 13th rib-bearing body: its longest rib is 38.9 mm (< 40); it carries a rib on one side only (right): T13 by rib contact, an
- `ts:s1209`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s1209] thoracic count not in the FOV (T13 not excluded) / labeller B on the v201 masks of the same CT reads none (lumbar 5, rib-bearing -)
- `ts:s1329`: (not in table) -> **T13** (two-labeller): [totalsegmentator:TS_s1329] 13 rib-bearing; the lumbosacral junction is not countable here / the 13th rib-bearing body: its longest rib is 36.4 mm (< 40); it carries a rib on one side only (left): T13 by rib contact, an 
- `ts:s1405`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s1405] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) / TS v300 names a vertebrae_L6 (T
- `ts:s1417`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1417] 11 rib-bearing + 5 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 4): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s1447`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1447] 11 rib-bearing; the lumbosacral junction is not countable here / lowest rib 30.0 mm (< 40): lumbar-rib / hypoplastic-rib candidate, morphology only / paediatric (age 2.00) / paediatric positiv
- `ts:s1487`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s1487] thoracic count not in the FOV (T13 not excluded) / TS T7 counted as 2 bodies (height x1.77, rib2=True, dip=119.0) / B's sixth free body: TS names it T12 and gives it no rib (11 TS rib pairs): 
- `ts:s1534`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1534] 11 rib-bearing + 5 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 4): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s1535`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s1535] 11 rib-bearing + 6 rib-free = 24 presacral bodies (a rib-less T12, or a 12th rib neither mask holds): L6 by the rib convention only / presacral bodies 24 (C1 to the sacrum all in the FOV) / B'
- `ts:s1538`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1538] 12 rib-bearing + 4 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 4): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s1542`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1542] 12 rib-bearing + 4 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 4): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s1597`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1597] 11 rib-bearing; the lumbosacral junction is not countable here / labeller B gave no count: implausible count (rib-bearing 14): a segmentation defect until a human says otherwise / implausible 
- `ts:s1606`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1606] 11 rib-bearing; the lumbosacral junction is not countable here / labeller B gave no count: implausible count (rib-bearing 4): a segmentation defect until a human says otherwise / implausible c
- `ts:s1636`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s1636] thoracic count not in the FOV (T13 not excluded) / TS L5 counted as 2 bodies (height x2.40, rib2=False, dip=253.0) / B's sixth free body: one TS label holds two bodies (B split it by height/di
- `ts:s1670`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1670] 11 rib-bearing + 5 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 3): a segmentation defect until a human says otherwise / implausible count (rib-bea
- `ts:s1747`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1747] 11 rib-bearing; the lumbosacral junction is not countable here / labeller B gave no count: implausible count (rib-bearing 3): a segmentation defect until a human says otherwise / implausible c
- `ts:s1762`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s1762] 11 rib-bearing + 6 rib-free = 24 presacral bodies (a rib-less T12, or a 12th rib neither mask holds): L6 by the rib convention only / B's sixth free body: TS names it T12 and gives it no rib (
- `ts:s1776`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1776] 12 rib-bearing + 4 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 14): a segmentation defect until a human says otherwise / implausible count (rib-be
- `ts:s1778`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s1778] 11 rib-bearing + 6 rib-free = 24 presacral bodies (a rib-less T12, or a 12th rib neither mask holds): L6 by the rib convention only / labeller B gave no count: implausible count (lumbar 7): a 
- `ts:s1784`: (not in table) -> **T13** (single-labeller): [totalsegmentator:TS_s1784] labeller B gave no count: implausible count (rib-bearing 15): a segmentation defect until a human says otherwise / implausible count (rib-bearing 15): a segmentation defect until a human says 
- `ts:s1845`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1845] 11 rib-bearing + 5 rib-free = 23 presacral bodies / presacral bodies 23 (C1 to the sacrum all in the FOV) / paediatric (age 16.00) / paediatric positive: an unfused S1 (or S1-S2) reads as a fr
- `ts:s1947`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1947] 11 rib-bearing; the lumbosacral junction is not countable here / paediatric (age 1.00) / paediatric positive: an unfused S1 (or S1-S2) reads as a free vertebra to both labellers; not two-label
- `ts:s1974`: (not in table) -> **L6** (two-labeller): [totalsegmentator:TS_s1974] 11 rib-bearing + 6 rib-free = 24 presacral bodies (a rib-less T12, or a 12th rib neither mask holds): L6 by the rib convention only / presacral bodies 24 (C1 to the sacrum all in the FOV) / B'
- `ts:s1984`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s1984] 11 rib-bearing + 5 rib-free = 23 presacral bodies / presacral bodies 25 (C1 to the sacrum all in the FOV) / TS T4 counted as 2 bodies (height x2.00, rib2=False, dip=115.0)
- `ts:s1998`: (not in table) -> **L6** (single-labeller): [totalsegmentator:TS_s1998] thoracic count not in the FOV (T13 not excluded) / B's sixth free body: TS names it T12 and gives it no rib (11 TS rib pairs): an L6 by the rib convention, a rib-less T12 by TS's count -- 24 o
- `ts:s2047`: (not in table) -> **unassigned** (two-labeller): [totalsegmentator:TS_s2047] thoracic count not in the FOV (T13 not excluded)
- `ts:s2075`: (not in table) -> **unassigned** (single-labeller): [totalsegmentator:TS_s2075] 11 rib-bearing + 5 rib-free = 23 presacral bodies / labeller B gave no count: implausible count (rib-bearing 14): a segmentation defect until a human says otherwise / implausible count (rib-be
- `verse:verse005`: (not in table) -> **lumbar_rib** (read): [verse:verse005] read, voxel-verified: B counts 5 lumbar (38 mm rule) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / read stump rib at L1 / Moller rib mask (verse_pred): stump at none, last rib ?
- `verse:verse008`: (not in table) -> **unassigned** (read): [verse:verse008] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read
- `verse:verse016`: (not in table) -> **unassigned** (read): [verse:verse016] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; B counts 5 rib-free bodies below the last rib (rib contact) / stump rib at T12: a rib under 38 mm on ONE side of a thoracic vertebra (
- `verse:verse022`: (not in table) -> **unassigned** (read): [verse:verse022] read, voxel-verified: B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / stump rib at T12: a rib under 38 mm on ONE side of a t
- `verse:verse026`: (not in table) -> **L6** (read): [verse:verse026] read, CONTRADICTED by mask lumbar ids + unlabelled bodies below = 5 (supported by B counts 5 rib-free bodies below the last rib (rib contact, the stump-rib L1 rib-bearing)) (consistent: A counts 5 = the 
- `verse:verse031`: (not in table) -> **lumbar_rib** (read): [verse:verse031] read, voxel-verified: B counts 5 lumbar (38 mm rule); consistent: A counts 4 = the read's 5 when VERIDAH counts the stump-rib L1 as rib-bearing (rib-contact convention) / read thoracic count 12 is ASSUME
- `verse:verse047`: (not in table) -> **unassigned** (read): [verse:verse047] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic / stump rib at T12: a rib under 3
- `verse:verse054`: (not in table) -> **lumbar_rib** (read): [verse:verse054] read, voxel-verified: B counts 5 lumbar (38 mm rule) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / read stump rib at L1 / Moller rib mask (verse_manual): stump at none, last rib ?
- `verse:verse056`: (not in table) -> **unassigned** (read): [verse:verse056] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read
- `verse:verse073`: (not in table) -> **lumbar_rib** (read): [verse:verse073] read, voxel-verified: B counts 5 lumbar (38 mm rule) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / read stump rib at L1 / Moller rib mask (verse_pred): stump at none, last rib ?
- `verse:verse091`: (not in table) -> **unassigned** (read): [verse:verse091] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic / stump rib at T12: a rib under 3
- `verse:verse108`: (not in table) -> **unassigned** (read): [verse:verse108] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic; B counts 12 rib-bearing bodies f
- `verse:verse111`: (not in table) -> **unassigned** (read): [verse:verse111] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read
- `verse:verse139`: (not in table) -> **unassigned** (read): [verse:verse139] read, voxel-verified: B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / stump rib at T12: a rib under 38 mm on ONE side of a t
- `verse:verse141`: (not in table) -> **lumbar_rib** (read): [verse:verse141] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); A counts 12 thoracic / read stump rib at L1 / Moller rib mask (verse_pred): stump a
- `verse:verse145`: (not in table) -> **unassigned** (read): [verse:verse145] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic / stump rib at T12: a rib under 3
- `verse:verse149`: (not in table) -> **lumbar_rib** (read): [verse:verse149] read, CONTRADICTED by A counts 6 lumbar (supported by mask lumbar ids + unlabelled bodies below = 5; B counts 5 lumbar (38 mm rule)) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / rea
- `verse:verse254`: (not in table) -> **lumbar_rib** (read): [verse:verse254] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); A counts 12 thoracic / read stump rib at L1 / Moller rib mask (verse_pred): stump a
- `verse:verse260`: (not in table) -> **lumbar_rib** (read): [verse:verse260] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; B counts 5 lumbar (38 mm rule); consistent: A counts 4 = the read's 5 when VERIDAH counts the stump-rib L1 as rib-bearing (rib-contact
- `verse:verse276`: (not in table) -> **lumbar_rib** (read): [verse:verse276] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); A counts 12 thoracic / read stump rib at L1 / Moller rib mask (verse_pred): stump a
- `verse:verse410`: (not in table) -> **unassigned** (read): [verse:verse227] read, not reproducible from this scan's field (thoracolumbar junction and lumbosacral junction out of view) / stump rib at T12: a rib under 38 mm on ONE side of a thoracic vertebra (the other > 38 mm, so
- `verse:verse415`: (not in table) -> **lumbar_rib** (read): [verse:verse243] read, not reproducible from this scan's field (thoracolumbar junction and lumbosacral junction out of view) / read stump rib at L1 / same person (verse415) as verse275
- `verse:verse511`: (not in table) -> **unassigned** (read): [verse:verse511] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 1
- `verse:verse531`: (not in table) -> **unassigned** (read): [verse:verse531] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic / stump rib at T12: a rib under 3
- `verse:verse533`: (not in table) -> **unassigned** (read): [verse:verse533] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 1
- `verse:verse550`: (not in table) -> **unassigned** (read): [verse:verse550] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 1
- `verse:verse640`: (not in table) -> **unassigned** (read): [verse:verse640] read, not reproducible from this scan's field (lumbosacral junction out of view) / stump rib at T12: a rib under 38 mm on ONE side of a thoracic vertebra (the other > 38 mm, so the vertebra stays thoraci
- `verse:verse646`: (not in table) -> **unassigned** (read): [verse:verse646] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic / stump rib at T12: a rib under 3
- `verse:verse708`: (not in table) -> **lumbar_rib** (read): [verse:verse708] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; B counts 5 lumbar (38 mm rule) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / read stump rib at L1 / Moller rib ma
- `verse:verse756`: (not in table) -> **unassigned** (read): [verse:verse756] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read
- `verse:verse759`: (not in table) -> **unassigned** (read): [verse:verse759] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact); A counts 12 thoracic; B counts 12 thoracic (38 mm rule
- `verse:verse807`: (not in table) -> **lumbar_rib** (read): [verse:verse807] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule) / read thoracic count 12 is ASSUMED (T1 not in the read's field) / read stump rib at
- `verse:verse824`: (not in table) -> **unassigned** (read): [verse:verse824] read, voxel-verified: mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 rib-free bodies below the last rib (rib contact) / read thoracic count 12 is ASSUMED (T1 not in the read

### Registry tier of the persons the table carried

| table basis (its `confidence` column) | registry tier | persons |
|---|---:|---:|
| VerSe audit read (lstv_flag_labels_v2) | read | 81 |
| raw VerSe mask ids | read | 52 |
| radiologist consensus (2 readers, agreement=True) | read | 27 |
| release labels | two-labeller | 13 |
| radiologist consensus (2 readers, agreement=False) | read | 6 |
| release labels | single-labeller | 5 |
| ts12_ctd_subtypes.json (VERIDAH ctd naming, no read) | none | 3 |
| CBCT labels (SPINEPS+TS agreement), real intraop frames | morphology-only | 3 |
| raw VerSe mask ids | none | 2 |
| ts12_ctd_subtypes.json (VERIDAH ctd naming, no read) | two-labeller | 2 |
| release labels | none | 1 |

57 table persons rested on a mask id (raw VerSe mask ids, or a CBCT mask carrying id 25); a mask id never names a level in this project, so each now carries the tier a stream measured for it (the VerSe rows through the published read, the C-ArmLSpine rows as morphology-only: no count in the field).

## Denominators and refusals per source

A refusal is `no_count`: no count could be made, which is never `normal`. Per stream, computed from its rows (verse from `screened.csv`; CTSpinoPelvic1K from `build_state.json`, since its negatives are on the grid census and not local).

| source | scans (rows) | persons | countable (any count) | positive | unresolved | none | no_count | real-frame scans |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ctsp | 64 | 64 | 64 | 64 | 0 | 0 | 0 | 0 |
| verse | 374 | 355 | 318 | 171 | 0 | 147 | 56 | 0 |
| totalsegmentator | 1935 | 1935 | 748 | 52 | 74 | 622 | 1187 | 0 |
| cobra2026 | 692 | 692 | 195 | 9 | 11 | 175 | 497 | 692 |
| carmlspine | 149 | 149 | 9 | 4 | 0 | 5 | 140 | 149 |
| ctspine1k | 223 | 223 | 166 | 5 | 15 | 146 | 57 | 0 |
| ribfrac | 660 | 660 | 626 | 6 | 29 | 591 | 34 | 0 |
| rsna_cspine | 2022 | 2022 | 0 | 0 | 0 | 0 | 2022 | 0 |
| deepfluoro | 6 | 6 | 0 | 0 | 0 | 0 | 6 | 6 |
| deepfluoro_vendor | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| geneva | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| spinesac | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 3 |
| ljubljana | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |

CTSpinoPelvic1K (`ctsp/build_state.json`): ct_in_release 802; censused 802; countable: A release 792; countable: B SPINEPS (release ribs) 796; countable: SPINEPS with TS ribs (check) 798; countable: C TotalSegmentator bodies (release ribs) 777; countable: TotalSegmentator bodies and ribs (check) 779; A and B both count 791; A and B agree 775; A and C both count 772; A and C agree 756; all three count 771; all three agree 752; two or more agree on a count 791; rib-bearing: A and B both have a rib-bearing vertebra 795; rib-bearing: A and B differ in the number in the FOV 160; rib-bearing: A and B differ in the LOWEST rib-bearing vertebra 1; veridah_T13_uncountable 52; reads: the readers' count differs between them or from the labellers' 13; only TotalSegmentator's ribs move the count off 5 139; release count withdrawn: a label covers two bodies 1; release merged-pair refusal withdrawn (ordinary height) 1; release label off its CT 3; B_unavailable 1; unassigned resolved as a labelling artefact 1; morphology: Castellvi screen top 25 25; morphology: type-I height pre-filter calls 214; morphology: in either screen 218; morphology: in either screen and already a registry row 10.

### Refusal tables, copied from each stream's SUMMARY.md

#### verse

## Refusals (no count), by reason

| labeller | reason | scans |
|---|---|---:|
| A | C7/T1 not named: thoracic count not anchored | 135 |
| A | thoracolumbar junction not named inside the field | 91 |
| A | no sacrum point | 18 |
| A | VERIDAH ctd missing | 8 |
| A | VERIDAH ctd order_error | 2 |
| B | the column does not reach a complete C1/C2 in TS: T1 cannot be counted | 289 |
| B | no sacrum in field | 83 |
| B | last rib-bearing body is the lowest body in field | 47 |
| B | no rib-bearing body in field | 14 |
| B | the body below the last rib-bearing body is cut by the field | 13 |
| B | stump ribs at the junction with no thoracic-type body above in field | 6 |
| B | the cervical column between TS's C1/C2 and T1 is cut or has a spacing gap | 5 |
| B | spacing gap inside the rib cage | 3 |
| B | the first rib-bearing body is 4 below T1 by count | 2 |
| B | the first rib-bearing body is 3 below T1 by count | 1 |

#### ctsp

### Refusals by reason and labeller (a refusal is 'no count', not 'normal')

| labeller: reason | CTs |
|---|---|
| C TotalSegmentator bodies (release ribs): a counted body of | 14 |
| TotalSegmentator bodies and ribs (check): a counted body of | 13 |
| TotalSegmentator bodies and ribs (check): gap in the chain between the last rib and the sacrum | 7 |
| C TotalSegmentator bodies (release ribs): gap in the chain between the last rib and the sacrum | 6 |
| A release: the lowest rib in the FOV is cut by the FOV edge | 5 |
| B SPINEPS (release ribs): the lowest rib in the FOV is cut by the FOV edge | 4 |
| C TotalSegmentator bodies (release ribs): the lowest rib in the FOV is cut by the FOV edge | 4 |
| A release: release label does not sit on its CT: only 0.66 of TotalSegmentator's spine voxels land on | 2 |
| SPINEPS with TS ribs (check): the lowest rib in the FOV is cut by the FOV edge | 2 |
| TotalSegmentator bodies and ribs (check): the lowest rib in the FOV is cut by the FOV edge | 2 |
| A release: no rib-bearing vertebra in the FOV | 1 |
| A release: release L2 covers two SPINEPS bodies and is 1.45x its neighbours' volume: two vertebrae un | 1 |
| A release: release label does not sit on its CT: only 0.69 of TotalSegmentator's spine voxels land on | 1 |
| B SPINEPS (release ribs): no SPINEPS output | 1 |
| B SPINEPS (release ribs): no rib-bearing vertebra in the FOV | 1 |
| C TotalSegmentator bodies (release ribs): no rib-bearing vertebra in the FOV | 1 |
| SPINEPS with TS ribs (check):  | 1 |
| SPINEPS with TS ribs (check): no rib-bearing vertebra in the FOV | 1 |
| TotalSegmentator bodies and ribs (check): no rib-bearing vertebra in the FOV | 1 |

#### totalsegmentator

## Refusals (`no_count` rows) by reason

| reason | CTs |
|---|---:|
| thoracolumbar reference not in FOV | 988 |
| no vertebra in the TS masks | 162 |
| sacrum reference not in FOV | 15 |
| only 1 whole body below the lowest rib-bearing one | 13 |
| sacrum cut by the FOV at the sacroiliac joint with # mm of sacrum label | 6 |
| implausible count | 3 |

#### cobra

## Refusals by reason (a refusal is 'no count', never 'normal')

Labeller A:

| reason | CTs |
|---|---:|
| thoracolumbar junction not in the field (no thoracic name) | 367 |
| thoracolumbar junction not in the field (one thoracic name, the top of the field) | 108 |
| SPINEPS crashed on this CT (TPTBox cc3d statistics) | 11 |
| VERIDAH named a lumbar level that SPINEPS has no body for (sliver) | 10 |
| ctd naming failed its one-to-one / S-I order checks | 7 |

Labeller B:

| reason | CTs |
|---|---:|
| thoracolumbar junction not in the field (no rib-bearing vertebra) | 372 |
| reference not established: last rib-bearing object cut by the field | 156 |
| reference not established: last rib-bearing object is the top object | 13 |
| reference not established: rib-free object directly above it | 10 |
| count refused: a body in two pieces (fragment rule) | 8 |
| lumbosacral junction not in the field (sacrum absent or cut) | 2 |

#### other_ct

## Refusals by reason (a refusal is 'no count', never 'normal')

| source | refusal reason | CTs |
|---|---|---:|
| carmlspine | no count in the field (TL: A=no_count B=no_count; LS: A=no_count B=no_count) | 140 |
| ctspine1k | no count in the field (TL: A=no_count B=no_count; LS: A=no_count B=no_count) | 48 |
| ctspine1k | no count in the field (TL: A=n/a B=no_count; LS: A=n/a B=no_count) | 4 |
| ctspine1k | no count in the field (TL: A=T13?morph (VERIDAH T13 by appearance); LS: A=no_count B=no_count) | 3 |
| ctspine1k | no count in the field (TL: A=n/a B=n/a; LS: A=n/a B=n/a) | 1 |
| ctspine1k | no count in the field (TL: A=no_count B=n/a; LS: A=no_count B=n/a) | 1 |
| deepfluoro | no count in the field (pelvis CT: no rib-bearing vertebra) | 6 |
| deepfluoro_vendor | PHANTOM (sawbones pelvis): not a person; manufactured anatomy | 1 |
| geneva | no count in the field (hip phantom) | 1 |
| ljubljana | FOV: five isolated lumbar vertebrae (L1-L5 volumes) | 1 |
| ribfrac | no count in the field (TL: A=no_count B=no_count; LS: A=no_count B=no_count) | 29 |
| ribfrac | no count in the field (TL: A=n/a B=no_count; LS: A=n/a B=no_count) | 2 |
| ribfrac | no count in the field (TL: A=T13?morph (VERIDAH T13 by appearance); LS: A=no_count B=no_count) | 2 |
| ribfrac | no count in the field (TL: A=n/a B=unresolved; LS: A=n/a B=no_count) | 1 |
| rsna_cspine | FOV: cervical-spine CT, craniocaudal extent < 350 mm (header census, no study segmented) | 2022 |
| spinesac | no count in the field (sawbones phantom) | 3 |

C-ArmLSpine: 140 of 149 lumbar CBCTs have neither reference whole in the field (the rib-bearing vertebra is cut or absent, the sacrum is often at the edge); 6 have a countable lumbosacral junction (5 `none`, 1 `unassigned`) and 3 are morphology-only L6.

## Review queues, per source, for Greg

| source | queued | by priority | queued CTs with a registry person | rendered | greg_verdict filled | contact sheets |
|---|---:|---:|---:|---:|---:|---:|
| verse | 71 | high: 22, low: 49 | 71 | 71 | 0 | contact_sheets/verse_1.jpg, contact_sheets/verse_2.jpg, contact_sheets/verse_3.jpg |
| ctsp | 72 | 1-candidate: 13, 2-unassigned: 4, 3-labellers-disagree: 5, 4-read-vs-labeller: 15, 5-uncertain: 6, 6-single-count: 13, 7-morphology-screen: 16 | 40 | 72 | 0 | contact_sheets/ctsp_1.jpg, contact_sheets/ctsp_2.jpg, contact_sheets/ctsp_3.jpg |
| totalsegmentator | 137 | 1: 28, 2: 78, 3: 6, 4: 17, 6: 8 | 137 | 137 | 0 | contact_sheets/totalsegmentator_1.jpg, contact_sheets/totalsegmentator_2.jpg, contact_sheets/totalsegmentator_3.jpg, contact_sheets/totalsegmentator_4.jpg, contact_sheets/totalsegmentator_5.jpg, contact_sheets/totalsegmentator_6.jpg |
| cobra | 79 | 1: 6, 2: 11, 3: 3, 4: 16, 5: 43 | 79 | 79 | 0 | contact_sheets/cobra_1.jpg, contact_sheets/cobra_2.jpg, contact_sheets/cobra_3.jpg, contact_sheets/cobra_4.jpg |
| other_ct | 87 | (none): 87 | 87 | 87 | 0 | contact_sheets/other_ct_1.jpg, contact_sheets/other_ct_2.jpg, contact_sheets/other_ct_3.jpg, contact_sheets/other_ct_4.jpg |
| other_ct (labeller-validation arm, not registry cases) | 103 |  |  |  |  | contact_sheets/other_ct_validation_1.jpg, contact_sheets/other_ct_validation_2.jpg, contact_sheets/other_ct_validation_3.jpg, contact_sheets/other_ct_validation_4.jpg, contact_sheets/other_ct_validation_5.jpg |

Each sheet tiles that source's review-queue renders (the discordances and every positive), four per row, captioned with the case, its priority and the stream's reason; `contact_sheets/index.csv` maps every tile back to its render. The queue CSVs carry a `greg_verdict` column where one exists. A queued CT with no registry person is a CTSpinoPelvic1K negative (its rows are on the grid census, not local).

## What is not known

- No person in this registry outside the `read` tier has a radiologist's read; `two-labeller` means two models that fail differently agreed. On CTSpinoPelvic1K a two-labeller L6 from the TotalSegmentator stream was right 6 of 10 times (its SUMMARY.md); every non-read positive is a candidate in a review queue.
- The TotalSegmentator collection carries no patient identifier and draws on several public sources, so a person there may also be a person elsewhere; no alias edge exists to say so, and none is claimed.
- CTSpinoPelvic1K's negatives are not local (only its 64 positive rows and the build_state denominators are), so its `none` / `no_count` persons do not appear in registry.csv.
- The VerSe negatives were added from `screened.csv` with one rule of this tool's own: a `none` series with neither junction in the field is written `no_count`; with either junction in the field, `none`.
- The acquisition stream has no rows.csv yet (its folder holds the plan, census and ranking), so its collections are not in this registry.
- `tools/transitional_subtypes.py` and its table are owned by a live workflow and were not changed; the before-vs-after section is the input for whoever updates them.
