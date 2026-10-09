# Readers A and B of the automated reference, one table per corpus

Written by `tools/auto_reference_ab_summary.py` from `tables/*.csv`, `lists/*.csv` and `summary_numbers.json` of `tools/auto_reference_readers_ab.py` (grid tree `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readersAB/`; the frozen copies of the reader code and their md5s are in its `code/`). Governing text: `SchwingNet/LEVELCHECK_MODEL.md` section 14 (R1: the readers; R2: the calibration this table feeds; R3: how it is used) with sections 4 and 9. This step assembles the two readers; it chooses no consensus rule and reads no test person's truth.

## The readers, in one sentence each

- **A**: SPINEPS + VERIDAH, read only through the ctd names, behind `tools/spineps_ids.py` `assert_verse_monotonic` (VerSe alphabet, cranio-caudal in world S, agreement with the ctd, no skipped T12, ctd required). Only post-fix or ctd-relabelled masks are offered. Count: `harvest_verse_registry.call_a` (thoracolumbar junction needs two thoracic names above a lumbar one, the lumbosacral junction a sacrum name, a thoracic count needs C7 and T1 named; a wide spacing gap voids the count across it).
- **B**: TotalSegmentator `total` bodies and ribs counted geometrically (`harvest_verse_census.labeller_b`, `harvest_verse_registry.count_b`, rib attachment `seq2:skip+same`, the 38 mm rule for the lumbar count). TotalSegmentator's level names are never used. B abstains where the thoracolumbar reference is not established inside the field (the last thoracic-type body cut, most cranial, or under a rib-less body; a rib pair split across two bodies) and where its 38 mm count and its rib-contact count disagree (the count then turns on the length of a junction rib TotalSegmentator's mask cannot give).
- **Rib convention** (`transitional_subtypes.md`): L6 = six rib-free vertebrae above the sacrum; T13 = thirteen rib-bearing vertebrae counted from T1; a four-lumbar count is `four_lumbar`, never `sacralised_fused`, because neither reader can tell a fused L5 from a numerical reduction. A count needs its junction reference in the field: a cut field is `no_count`, never `ordinary`.
- **Reader column on the COBRA CBCT table.** Rows are `A` and `B` run on the CBCT (`corpus = cobra_cbct`); section 14's reader D is their agreement with the same reader on the planning CT, tabulated below, not a third implementation.

## Schema

`corpus, case, person_key, reader (A|B), junction_tl_in_fov, junction_ls_in_fov, n_rib_bearing, n_rib_free_above_sacrum, subtype_call (ordinary|L6|T13|both|four_lumbar|no_count), lumbar_names, refusal_reason, source_file` plus `g3_side` (the person's side in `~/split_final.json`: train/val/test/hold), `volume` and `notes`. One row per person per reader: a VerSe person with several series is collapsed to the series that counts (a count first, then both junctions in the field, then an anchored thoracic count, then the series name; fixed before any truth was read), the others named in `notes`. `lumbar_names` is filled only when the lumbosacral count was made (A: VERIDAH's names of the rib-free bodies; B: L1..Ln).

## Denominators

| corpus | volumes | persons | persons by side (train/val/test/hold) | A input (mask + ctd offered) | B input (TS total on the volume's grid) |
|---|---:|---:|---:|---:|---:|
| ctsp | 802 | 802 | 636/73/93/0 | 802 | 802 |
| verse | 374 | 355 | 252/35/68/0 | 369 | 374 |
| cobra_ct | 692 | 692 | 445/71/159/17 | 689 | 692 |
| cobra_cbct | 692 | 692 | 445/71/159/17 | 527 | 692 |
| carmlspine | 149 | 149 | 123/13/13/0 | 149 | 149 |

Inputs: **ctsp**: CTSpinoPelvic1K (802 CTs; A = post-fix SPINEPS `spineps/ctsp`, B = TotalSegmentator `total` in `~/bench/totalsegmentator/native`, with the 0533/0921 re-runs). **verse**: VerSe / VerSeFusion (374 series, 355 people; A = ctd-relabelled or post-fix pass-through masks in `spineps/ctd_relabel/bench_ts_native`, B = TotalSegmentator 2.18.0 `anomaly_harvest/verse/ts`). **cobra_ct**: COBRA2026 planning CT, `ct_def` (692; A = the LSTV screen's post-fix SPINEPS run, or the cc3d-patched ladder where that run crashed; B = TotalSegmentator `anomaly_harvest/cobra/ts`). **cobra_cbct**: COBRA2026 CBCT (692; `cbct_clinical.mha`, else `cbct_rtk.mha`; A = SPINEPS run for this table on the CBCT (stock, then the cc3d-patched ladder); B = TotalSegmentator written for reader C, `auto_reference/ts/cobra_cbct`). **carmlspine**: C-ArmLSpine CBCT (149; A = `carmlspine/spineps` (+ the case134 retry), B = TotalSegmentator `auto_reference/ts/carmlspine`).

## Calls per corpus and reader (persons)

| corpus | reader | ordinary | L6 | T13 | both | four_lumbar | no_count | tl in field | ls in field | thoracic anchored (T1) | B withheld: reference / rib conventions / split pair |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ctsp | A | 681 | 17 | 0 | 0 | 43 | 61 | 741 | 747 | 0 |  |
| ctsp | B | 623 | 26 | 0 | 0 | 12 | 141 | 720 | 800 | 0 | 69 / 54 / 11 |
| verse | A | 172 | 32 | 16 | 0 | 21 | 114 | 258 | 254 | 130 |  |
| verse | B | 157 | 40 | 1 | 0 | 10 | 147 | 259 | 290 | 14 | 30 / 29 / 8 |
| cobra_ct | A | 167 | 3 | 0 | 0 | 12 | 510 | 182 | 630 | 2 |  |
| cobra_ct | B | 93 | 4 | 0 | 0 | 7 | 588 | 121 | 672 | 0 | 160 / 6 / 2 |
| cobra_cbct | A | 1 | 0 | 0 | 0 | 0 | 691 | 1 | 504 | 0 |  |
| cobra_cbct | B | 0 | 0 | 0 | 0 | 0 | 692 | 1 | 247 | 0 | 1 / 0 / 0 |
| carmlspine | A | 0 | 0 | 0 | 0 | 0 | 149 | 0 | 139 | 0 |  |
| carmlspine | B | 0 | 0 | 0 | 0 | 0 | 149 | 2 | 145 | 0 | 4 / 0 / 0 |

`both` = L6 and T13 in one spine (looked for on every person with both counts; the column says how often it was found). `thoracic anchored` = the rib cage was counted from T1, the only way a T13 can be called or excluded; where it is 0 every `ordinary` row carries the note 'T13 not excluded'.

### Calls by G3 side

| corpus | reader | side | persons | ordinary | L6 | T13 | both | four_lumbar | no_count |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ctsp | A | train | 636 | 559 | 10 | 0 | 0 | 22 | 45 |
| ctsp | A | val | 73 | 59 | 2 | 0 | 0 | 4 | 8 |
| ctsp | A | test | 93 | 63 | 5 | 0 | 0 | 17 | 8 |
| ctsp | B | train | 636 | 504 | 16 | 0 | 0 | 7 | 109 |
| ctsp | B | val | 73 | 54 | 3 | 0 | 0 | 2 | 14 |
| ctsp | B | test | 93 | 65 | 7 | 0 | 0 | 3 | 18 |
| verse | A | train | 252 | 131 | 18 | 7 | 0 | 10 | 86 |
| verse | A | val | 35 | 18 | 2 | 2 | 0 | 2 | 11 |
| verse | A | test | 68 | 23 | 12 | 7 | 0 | 9 | 17 |
| verse | B | train | 252 | 117 | 24 | 1 | 0 | 3 | 107 |
| verse | B | val | 35 | 16 | 4 | 0 | 0 | 2 | 13 |
| verse | B | test | 68 | 24 | 12 | 0 | 0 | 5 | 27 |
| cobra_ct | A | train | 445 | 98 | 0 | 0 | 0 | 0 | 347 |
| cobra_ct | A | val | 71 | 11 | 0 | 0 | 0 | 0 | 60 |
| cobra_ct | A | test | 159 | 54 | 3 | 0 | 0 | 11 | 91 |
| cobra_ct | A | hold | 17 | 4 | 0 | 0 | 0 | 1 | 12 |
| cobra_ct | B | train | 445 | 63 | 1 | 0 | 0 | 2 | 379 |
| cobra_ct | B | val | 71 | 9 | 0 | 0 | 0 | 1 | 61 |
| cobra_ct | B | test | 159 | 16 | 3 | 0 | 0 | 4 | 136 |
| cobra_ct | B | hold | 17 | 5 | 0 | 0 | 0 | 0 | 12 |
| cobra_cbct | A | train | 445 | 1 | 0 | 0 | 0 | 0 | 444 |
| cobra_cbct | A | val | 71 | 0 | 0 | 0 | 0 | 0 | 71 |
| cobra_cbct | A | test | 159 | 0 | 0 | 0 | 0 | 0 | 159 |
| cobra_cbct | A | hold | 17 | 0 | 0 | 0 | 0 | 0 | 17 |
| cobra_cbct | B | train | 445 | 0 | 0 | 0 | 0 | 0 | 445 |
| cobra_cbct | B | val | 71 | 0 | 0 | 0 | 0 | 0 | 71 |
| cobra_cbct | B | test | 159 | 0 | 0 | 0 | 0 | 0 | 159 |
| cobra_cbct | B | hold | 17 | 0 | 0 | 0 | 0 | 0 | 17 |
| carmlspine | A | train | 123 | 0 | 0 | 0 | 0 | 0 | 123 |
| carmlspine | A | val | 13 | 0 | 0 | 0 | 0 | 0 | 13 |
| carmlspine | A | test | 13 | 0 | 0 | 0 | 0 | 0 | 13 |
| carmlspine | B | train | 123 | 0 | 0 | 0 | 0 | 0 | 123 |
| carmlspine | B | val | 13 | 0 | 0 | 0 | 0 | 0 | 13 |
| carmlspine | B | test | 13 | 0 | 0 | 0 | 0 | 0 | 13 |

### Lumbar names where a count was made

| corpus | reader | lumbar_names | persons |
|---|---:|---:|---:|
| ctsp | A | L1 L2 L3 L4 L5 | 681 |
| ctsp | A | L1 L2 L3 L4 | 43 |
| ctsp | A | L1 L2 L3 L4 L5 L6 | 17 |
| ctsp | B | L1 L2 L3 L4 L5 | 623 |
| ctsp | B | L1 L2 L3 L4 L5 L6 | 26 |
| ctsp | B | L1 L2 L3 L4 | 12 |
| verse | A | L1 L2 L3 L4 L5 | 184 |
| verse | A | L1 L2 L3 L4 L5 L6 | 32 |
| verse | A | L1 L2 L3 L4 | 25 |
| verse | B | L1 L2 L3 L4 L5 | 158 |
| verse | B | L1 L2 L3 L4 L5 L6 | 40 |
| verse | B | L1 L2 L3 L4 | 10 |
| cobra_ct | A | L1 L2 L3 L4 L5 | 167 |
| cobra_ct | A | L1 L2 L3 L4 | 12 |
| cobra_ct | A | L1 L2 L3 L4 L5 L6 | 3 |
| cobra_ct | B | L1 L2 L3 L4 L5 | 93 |
| cobra_ct | B | L1 L2 L3 L4 | 7 |
| cobra_ct | B | L1 L2 L3 L4 L5 L6 | 4 |
| cobra_cbct | A | L1 L2 L3 L4 L5 | 1 |

Reader A's names are VERIDAH's; where they are not `L1..Ln` in order the row's `notes` say so, and the calibration step decides what such a row is worth. A T13 row with four lumbar names, or eleven rib-bearing above six rib-free, adds up to the ordinary 17 thoracolumbar bodies; the `notes` column says so on every such row.

## Refusals (`no_count`) by reason

**ctsp, reader A** (61 persons):

| reason (first clause) | persons |
|---|---:|
| guard refused: [veridah_skipped_name] VERIDAH's ctd skips T# between T# and L# at a normal spacing (# mm, loca | 54 |
| thoracolumbar junction not named inside the field (fewer than two thoracic names) | 6 |
| no post-fix SPINEPS mask in spineps/ctsp | 1 |

**ctsp, reader B** (141 persons):

| reason (first clause) | persons |
|---|---:|
| thoracolumbar reference not established inside the field | 69 |
| B's two rib conventions disagree at the junction (rib-free count # by the # mm rule, # by rib contact): a stum | 54 |
| thoracolumbar reference not established inside the field: split pair at the junction | 11 |
| lowest body # mm above the sacral body (an unsegmented level between?) | 2 |
| stump ribs at the junction with no thoracic-type body above in field | 2 |
| no rib-bearing body in field | 2 |
| spacing gap below the rib cage (a body may be missing) | 1 |

**verse, reader A** (114 persons):

| reason (first clause) | persons |
|---|---:|
| thoracolumbar junction not named inside the field (fewer than two thoracic names) | 59 |
| guard refused: [veridah_skipped_name] VERIDAH's ctd skips T# between T# and L# at a normal spacing (# mm, loca | 33 |
| only the thoracic count (#) was made: the lumbosacral junction is not in the field, so L# and four-lumbar are  | 9 |
| no sacrum point | 8 |
| ctd relabel refused: L# point lies in instance # whose centroid is # mm away in S, # mm in #-D | 3 |
| ctd relabel refused: ctd sacrum point lies # mm above the lowest named vertebra | 1 |
| ctd relabel refused: ctd names out of S order: T# lies # mm above T# | 1 |

**verse, reader B** (147 persons):

| reason (first clause) | persons |
|---|---:|
| no sacrum in field | 64 |
| thoracolumbar reference not established inside the field | 31 |
| B's two rib conventions disagree at the junction (rib-free count # by the # mm rule, # by rib contact): a stum | 26 |
| no rib-bearing body in field | 8 |
| thoracolumbar reference not established inside the field: split pair at the junction | 8 |
| stump ribs at the junction with no thoracic-type body above in field | 6 |
| B's two rib conventions disagree at the junction (rib-free count # by the # mm rule, # by rib contact | 3 |
| # rib-bearing and # rib-free: a count outside the subtype vocabulary | 1 |

**cobra_ct, reader A** (510 persons):

| reason (first clause) | persons |
|---|---:|
| thoracolumbar junction not named inside the field (fewer than two thoracic names) | 450 |
| guard refused: [veridah_skipped_name] VERIDAH's ctd skips T# between T# and L# at a normal spacing (# mm, loca | 57 |
| SPINEPS failed on this volume (TPTBox cc#dstatistics error, the failure CTSpinoPelvic#K # shows | 3 |

**cobra_ct, reader B** (588 persons):

| reason (first clause) | persons |
|---|---:|
| no rib-bearing body in field | 381 |
| thoracolumbar reference not established inside the field | 165 |
| lowest body is cut by the field | 19 |
| stump ribs at the junction with no thoracic-type body above in field | 10 |
| B's two rib conventions disagree at the junction (rib-free count # by the # mm rule, # by rib contact): a stum | 6 |
| the body below the last rib-bearing body is cut by the field | 3 |
| thoracolumbar reference not established inside the field: split pair at the junction | 2 |
| lowest body # mm above the sacral body (an unsegmented level between?) | 1 |
| spacing gap below the rib cage (a body may be missing) | 1 |

**cobra_cbct, reader A** (691 persons):

| reason (first clause) | persons |
|---|---:|
| thoracolumbar junction not named inside the field (fewer than two thoracic names) | 516 |
| SPINEPS produced no vertebra instance mask on this CBCT | 164 |
| guard refused: [verse_ok_no_ctd] no ctd to show the ids are VERIDAH's names (a raw #..N enumeration looks the  | 5 |
| guard refused: [veridah_size_contradiction] VERIDAH names vertebrae cervical whose median volume is # ml (> #) | 3 |
| guard refused: [not_verse_order] read as VerSe names the ids are not cranio-caudal: [('L#', 'L#', #)]. Read th | 1 |
| guard refused: [veridah_skipped_name] VERIDAH's ctd skips T# between T# and L# at a normal spacing (# mm, loca | 1 |
| SPINEPS failed on this CBCT: RuntimeError('spineps exited #: ^^^^^^^^^^^^^\n File "/wsu/home/go/go#/go#/mambaf | 1 |

**cobra_cbct, reader B** (692 persons):

| reason (first clause) | persons |
|---|---:|
| no rib-bearing body in field | 246 |
| lowest body is cut by the field | 243 |
| no vertebral body in field | 176 |
| no sacrum in field | 26 |
| thoracolumbar reference not established inside the field | 1 |

**carmlspine, reader A** (149 persons):

| reason (first clause) | persons |
|---|---:|
| thoracolumbar junction not named inside the field (fewer than two thoracic names) | 139 |
| guard refused: [veridah_skipped_name] VERIDAH's ctd skips T# between T# and L# at a normal spacing (# mm, loca | 10 |

**carmlspine, reader B** (149 persons):

| reason (first clause) | persons |
|---|---:|
| no rib-bearing body in field | 141 |
| thoracolumbar reference not established inside the field | 5 |
| no sacrum in field | 3 |

## A against B where both count

| corpus | both count | same call | same lumbar names | A \ B pairs (A|B: n) |
|---|---:|---:|---:|---:|
| ctsp | 633 | 576 | 576 | ordinary|ordinary: 566, four_lumbar|ordinary: 21, ordinary|L6: 18, L6|ordinary: 11, four_lumbar|four_lumbar: 7, ordinary|four_lumbar: 5, L6|L6: 3, four_lumbar|L6: 2 |
| verse | 196 | 156 | 158 | ordinary|ordinary: 129, L6|L6: 22, ordinary|L6: 9, L6|ordinary: 9, four_lumbar|ordinary: 6, T13|L6: 6, T13|ordinary: 5, four_lumbar|four_lumbar: 5, ordinary|four_lumbar: 3, L6|four_lumbar: 1, ordinary|T13: 1 |
| cobra_ct | 99 | 91 | 91 | ordinary|ordinary: 87, ordinary|four_lumbar: 4, ordinary|L6: 2, four_lumbar|four_lumbar: 2, L6|L6: 2, four_lumbar|ordinary: 2 |
| cobra_cbct | 0 | 0 | 0 | - |
| carmlspine | 0 | 0 | 0 | - |

### A against B by side (persons where both count / agree)

| corpus | side | both count | agree | A only counts | B only counts | neither |
|---|---:|---:|---:|---:|---:|---:|
| ctsp | train | 507 | 473 | 84 | 20 | 25 |
| ctsp | val | 55 | 46 | 10 | 4 | 4 |
| ctsp | test | 71 | 57 | 14 | 4 | 4 |
| verse | train | 140 | 118 | 26 | 5 | 81 |
| verse | val | 22 | 15 | 2 | 0 | 11 |
| verse | test | 34 | 23 | 17 | 7 | 10 |
| cobra_ct | train | 63 | 61 | 35 | 3 | 344 |
| cobra_ct | val | 10 | 9 | 1 | 0 | 60 |
| cobra_ct | test | 23 | 19 | 45 | 0 | 91 |
| cobra_ct | hold | 3 | 2 | 2 | 2 | 10 |
| cobra_cbct | train | 0 | 0 | 1 | 0 | 444 |
| cobra_cbct | val | 0 | 0 | 0 | 0 | 71 |
| cobra_cbct | test | 0 | 0 | 0 | 0 | 159 |
| cobra_cbct | hold | 0 | 0 | 0 | 0 | 17 |
| carmlspine | train | 0 | 0 | 0 | 0 | 123 |
| carmlspine | val | 0 | 0 | 0 | 0 | 13 |
| carmlspine | test | 0 | 0 | 0 | 0 | 13 |

## Reader D: the same reader on the planning CT and on the CBCT of one COBRA person

| reader | persons with both acquisitions read | CT counts | CBCT counts | both count | same call | same lumbar names | CBCT: lumbosacral junction in field | CBCT: thoracolumbar reference in field |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 692 | 182 | 1 | 1 | 1 | 1 | 504 | 1 |
| B | 692 | 104 | 0 | 0 | 0 | 0 | 247 | 1 |

| reader | case | side | CT call | CT names | CBCT call | CBCT names |
|---|---:|---:|---:|---:|---:|---:|
| A | F155 | train | ordinary | L1 L2 L3 L4 L5 | ordinary | L1 L2 L3 L4 L5 |

The COBRA CBCT is a pelvic field: it holds the lumbosacral junction on most persons and the last rib-bearing vertebra on almost none, so a CBCT count is rare and D as a count check is nearly empty. What the CBCT does carry for every person with a SPINEPS mask is VERIDAH's shape name of the lowest mobile vertebra; comparing that with the planning-CT name is a junction check, not a count, and is left to the calibration step to weigh.

## Development-side check against read truth (train and val persons only; no test person's truth is read)

**CTSpinoPelvic1K**, 709 development persons (release truth: `transitional_subtypes.csv`, `L6` = release id 25 with the two-reader Castellvi consensus; `sacralised_L5_fused`, `castellvi_I_II`, `lumbar_rib`, `unassigned` as there; everything else `none`, with the caveat of `transitional_registry/ctsp/SUMMARY.md` that nine release-ordinary spines have six rib-free bodies by the release's own voxels). Reader call (rows) against read subtype (columns):

Reader A:

| call \ read | L6 | sacralised_L5_fused | castellvi_I_II | lumbar_rib | unassigned | none |
|---|---:|---:|---:|---:|---:|---:|
| ordinary | 5 | 1 | 2 | 3 | 1 | 606 |
| L6 | 4 | 0 | 0 | 0 | 0 | 8 |
| T13 | 0 | 0 | 0 | 0 | 0 | 0 |
| both | 0 | 0 | 0 | 0 | 0 | 0 |
| four_lumbar | 0 | 6 | 0 | 4 | 1 | 15 |
| no_count | 2 | 0 | 0 | 1 | 0 | 50 |

Reader A on these persons: `L6`: 12 calls, 4 with a read of L6; of 11 such reads 4 called; `four_lumbar`: 26 calls, 7 with a read of sacralised_L5_fused/unassigned; of 9 such reads 7 called. (`unassigned` here is the release's four-lumbar-id spines without a Castellvi read.)

Reader B:

| call \ read | L6 | sacralised_L5_fused | castellvi_I_II | lumbar_rib | unassigned | none |
|---|---:|---:|---:|---:|---:|---:|
| ordinary | 2 | 4 | 2 | 3 | 1 | 546 |
| L6 | 7 | 0 | 0 | 0 | 0 | 12 |
| T13 | 0 | 0 | 0 | 0 | 0 | 0 |
| both | 0 | 0 | 0 | 0 | 0 | 0 |
| four_lumbar | 0 | 1 | 0 | 1 | 0 | 7 |
| no_count | 2 | 2 | 0 | 4 | 1 | 114 |

Reader B on these persons: `L6`: 19 calls, 7 with a read of L6; of 11 such reads 7 called; `four_lumbar`: 9 calls, 1 with a read of sacralised_L5_fused/unassigned; of 9 such reads 1 called. (`unassigned` here is the release's four-lumbar-id spines without a Castellvi read.)

**VerSe**, 287 development persons (read truth: `transitional_registry/verse/rows.csv`, the Loffler 2021 consensus read; a person with no registry row is `none`, an ordinary read). Reader call (rows) against read subtype (columns):

Reader A:

| call \ read | L6 | T13 | sacralised_L5_fused | castellvi_I_II | lumbar_rib | unassigned | none |
|---|---:|---:|---:|---:|---:|---:|---:|
| ordinary | 13 | 1 | 4 | 16 | 6 | 15 | 94 |
| L6 | 20 | 0 | 0 | 0 | 0 | 0 | 0 |
| T13 | 5 | 3 | 0 | 0 | 1 | 0 | 0 |
| both | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| four_lumbar | 5 | 0 | 4 | 0 | 1 | 1 | 1 |
| no_count | 9 | 0 | 0 | 1 | 4 | 4 | 79 |

Reader A on these persons: `L6`: 20 calls, 20 with a read of L6; of 52 such reads 20 called; `T13`: 9 calls, 3 with a read of T13; of 4 such reads 3 called; `four_lumbar`: 12 calls, 4 with a read of sacralised_L5_fused; of 8 such reads 4 called. (A read of `sacralised_L5_fused` is a Castellvi III/IV body the VerSe mask leaves unlabelled, so a four-lumbar count there is the reader seeing what the read describes; `unassigned` is mostly a hypoplastic last rib on a thoracic vertebra, an ordinary count.)

Reader B:

| call \ read | L6 | T13 | sacralised_L5_fused | castellvi_I_II | lumbar_rib | unassigned | none |
|---|---:|---:|---:|---:|---:|---:|---:|
| ordinary | 21 | 1 | 2 | 11 | 7 | 5 | 86 |
| L6 | 21 | 1 | 0 | 1 | 0 | 0 | 5 |
| T13 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| both | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| four_lumbar | 0 | 0 | 3 | 1 | 0 | 1 | 0 |
| no_count | 10 | 2 | 3 | 4 | 5 | 14 | 82 |

Reader B on these persons: `L6`: 28 calls, 21 with a read of L6; of 52 such reads 21 called; `T13`: 1 calls, 0 with a read of T13; of 4 such reads 0 called; `four_lumbar`: 5 calls, 3 with a read of sacralised_L5_fused; of 8 such reads 3 called. (A read of `sacralised_L5_fused` is a Castellvi III/IV body the VerSe mask leaves unlabelled, so a four-lumbar count there is the reader seeing what the read describes; `unassigned` is mostly a hypoplastic last rib on a thoracic vertebra, an ordinary count.)

These crosstabs are printed so that the reader behaviour known from the registries (VERIDAH's shape-named T13 and four-lumbar calls; TotalSegmentator's L6 from a split label) is visible on the development side before calibration. They are not the calibration: the rule, its per-subtype PPV with Wilson bounds and its coverage are chosen and frozen by the next step on these same persons (section 14, R2).

## What was run for this table, and what is not known

- **SPINEPS on the COBRA CBCTs** had never been run. It was run for this table on all 692 (the CBCT written to NIfTI by SimpleITK with its direction cosines, nothing reoriented; stock SPINEPS on GPU where a GPU could be had and on CPU with a job-local `torch.cuda.mem_get_info` shim otherwise; then the cc3d-patched ladder on every CBCT the stock run left without a vertebra mask). The `lists/cobra_cbct.csv` `a_note` column records, per CBCT, why there is no mask where there is none.
- **SPINEPS on 11 COBRA planning CTs** had crashed in TPTBox `cc3dstatistics` in the LSTV screen; the cc3d-patched ladder was run on them for this table (`spineps/cobra_ct_patch`), and the rows say whether it produced a mask.
- **Reader A refusals are loud.** `guard refused: [veridah_skipped_name]` is VERIDAH's T12 skip, which was one level off every time it could be checked (`spineps_ids/REPAIRS.md` section 4); such a mask gives no names here. `ctd relabel refused` (VerSe) is a VERIDAH order or binding error the relabel would not paper over.
- **No count on a lumbar-only field.** Every C-ArmLSpine CBCT and almost every COBRA CBCT holds no thoracolumbar reference: both readers return `no_count` with the reason, never `ordinary`. Section 14 R3 then excludes the person from the automated reference and counts the reason in the flow diagram. The three real C-ArmLSpine L6 patients stay excluded from the primary analysis by section 4 whatever this table says.
- **What A and B cannot tell apart**: a fused L5 (Castellvi III/IV) from a true four-lumbar spine; a rib-less 20th vertebra with thoracic-type processes (VERIDAH names it T13, the rib convention calls the spine L6); a stump rib under 38 mm at the junction (B abstains, A does not see ribs at all). Reader C reads the CT's own rib bone and is the reader for the last two.
- **Persons are the unit.** Every row is keyed by `~/split_final.json` (`raw_to_group` folds VerSe series to the subject; nobody was keyed from `~/patient_keys_final.json`). G3 test persons appear in the tables with their side so that the calibration step can exclude them; their truth was not read here.

## Reproduce

```
sbatch -D $ROOT --export=ALL,MODE=lists auto_reference_ab.sh
sbatch -D $ROOT --array=0-15 --export=ALL,MODE=a,CORPUS=<corpus> auto_reference_ab.sh   # per corpus
sbatch -D $ROOT --array=0-15 --export=ALL,MODE=b,CORPUS=<corpus> auto_reference_ab.sh
sbatch -D $ROOT --array=0-47 auto_reference_ab_spineps_cbct_cpu.sh                       # SPINEPS on the CBCTs
sbatch -D $ROOT --array=0-10 --export=ALL,MODE=ct   auto_reference_ab_spineps_patch.sh   # cc3d-patched ladder
sbatch -D $ROOT --array=0-41 --export=ALL,MODE=cbct auto_reference_ab_spineps_patch.sh
sbatch -D $ROOT --export=ALL,MODE=table auto_reference_ab.sh
python tools/auto_reference_ab_summary.py --tables <tables> --lists <lists> --out .../SUMMARY.md
```
`$ROOT = /rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readersAB`; every step runs the frozen copies in `$ROOT/code` and refuses to start if their md5s changed.
