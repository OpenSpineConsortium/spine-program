# Transitional registry -- VerSe / VerSeFusion stream

Built by `tools/harvest_verse_census.py` (grid, one json per scan) and `tools/harvest_verse_registry.py` (this table). Source: the raw VerSeFusion unified masks `~/VerSeFusion/data/unified/scan-*/` in VerSe ids (NOT the converted vf_813/Dataset813 maps, which drop C1-T9). Read: Loffler et al., Sci Data 8:284 (2021), Supplementary Table 1 (two-neuroradiologist consensus). Labeller A: SPINEPS+VERIDAH, through its ctd POI names only, never a SPINEPS mask id. Labeller B: TotalSegmentator 2.18.0 `total` run for this stream on every scan, counted geometrically (rib attachment `seq2:skip+same`); TS vertebra names are not used to count.

## The two rules in the paper that decide every VerSe call

> "vertebrae with at least one rib measuring more than 38 mm from the costovertebral joint to the osseous tip and showing a typical diagonal downward alignment were classified as thoracic vertebrae. In cases with both ribs smaller than 38 mm ... the vertebra was considered lumbar."

> "we did not segment vertebrae that showed partial fusion with the sacrum (Castellvi grades III and IV)" ... "If T1 was not visible within the scan's field-of-view, the thoracic spine was considered to have 12 vertebrae".

So: a *stump rib at T12* is one short rib on a thoracic vertebra (normal count); a *stump rib at L1* is a lumbar vertebra with rudiments (lumbar rib); a Castellvi III/IV body is **background** in the release mask (no own id, and there is no sacrum label at all). Of the old table's 38 audit-only L6 rows, 35 are Castellvi III/IV reads -- an L6 the mask was never going to carry as id 25. `fused_mask_representation` therefore carries a VerSe-only value, `unlabelled`, beside `own-id` / `n/a` (VerSe never has `merged-into-sacrum`: it labels no sacrum).

## Denominators

| quantity | scans | subjects |
|---|---:|---:|
| series in VerSeFusion / screened here | 374 / 374 | 355 / 355 |
| with a published read (table row for the subject) | 344 | 325 |
| labeller A usable (ctd present, names in S-I order) | 364 | |
| labeller B usable (TS output on the CT grid) | 374 | |
| thoracolumbar junction in the field (any source) | 306 | |
| lumbosacral junction in the field (A or B) | 292 | |
| both junctions in the field | 284 | |
| A made a lumbar count / B made one | 255 / 277 | |
| A made a thoracic count (T1 named) / B made one (T1 by count from C1/C2) | 138 / 17 | |

## Calls (rows.csv): one row per SCAN; persons are the statistical unit

| subtype | scans | persons | read | two-labeller | single-labeller | voxel-verified | consistent only | contradicted by mask or A -> review | B alone disagrees | not reproducible in the scan |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L6 | 87 | 85 | 87 | 0 | 0 | 66 | 9 | 7 | 8 | 5 |
| T13 | 6 | 6 | 6 | 0 | 0 | 4 | 0 | 2 | 1 | 0 |
| both_L6_T13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sacralised_L5_fused | 13 | 13 | 13 | 0 | 0 | 8 | 4 | 0 | 0 | 1 |
| castellvi_I_II | 28 | 27 | 28 | 0 | 0 | 24 | 0 | 3 | 3 | 1 |
| lumbar_rib | 13 | 12 | 13 | 0 | 0 | 11 | 0 | 1 | 0 | 1 |
| unassigned | 24 | 23 | 24 | 0 | 0 | 21 | 0 | 1 | 1 | 2 |

**Renderable as a countable example** (both junctions in THIS scan's field -- a render cut above the sacrum or below the rib cage cannot show the count; before this pass 56 VerSe scans were rendered, 50 L6 + 6 T13): L6 82/87 scans (82 persons); T13 6/6 scans (6 persons); sacralised_L5_fused 12/13 scans (12 persons); castellvi_I_II 27/28 scans (27 persons); lumbar_rib 12/13 scans (12 persons); unassigned 22/24 scans (22 persons). A T13 needs T1 as well: 6/6 T13 scans show C7-T1 (release mask or VERIDAH).


Of 134 voxel-verified rows, 131 are supported by at least one INDEPENDENT labeller (A or B); the other 3 rest on the release mask alone (id 25/28 or its lumbar ids), which the same neuroradiologists approved -- they confirm the scan carries the read's anatomy as annotated, not a second opinion.


Modifiers: four_lumbar 3 scans; lumbar_rib 50 scans. Fused-body representation over rows with a Castellvi III/IV body: {'unlabelled': 49}.

`unassigned` by reason: stump rib at T12/T13 on a thoracic vertebra (hypoplastic last rib, normal count): 18; six-segment sacrum: 3; four lumbar, no fusion (numerical reduction): 3. The hypoplastic-last-rib rows are kept because Greg asked for every anomaly, but they are NOT transitional by the paper's own rule (the vertebra stays thoracic); a consumer that wants count variants only should drop them.

**both_L6_T13:** looked for in every scan (read T=13 with L=6; A or B counting 13 and 6; mask ids 25 and 28 together). Found: 0.

## Outside checks on the two labellers (the VerSe expert mask and the read, which the labellers never see)

Two subsets, both with 12 thoracic and no Castellvi III/IV: **ordinary** reads (7/12/5/5, no stump) and **variant** reads (stump T12 or L1, six lumbar, Castellvi II, six-segment sacrum) -- the second is where a rule tuned on ordinary spines could still be wrong. The paper's rule makes VerSe T12 the last thoracic-type body in both. 'Either convention' = B's 38 mm count equals the read's L (not used where the read puts a stump rib at T12/T13: the read keeps that vertebra thoracic, TS's short ribs there push the 38 mm count one high, and on verse524 a fused L5 one low cancelled it), or its rib-contact count equals L (L - 1 for a stump at L1). The calls use exactly this rule.

| labeller B rib attachment | subset | body enumeration matches the mask | last thoracic-type body is VerSe T12 | lumbar count = read (38 mm) | lumbar count, either convention |
|---|---|---:|---:|---:|---:|
| census | ordinary | 182/186 | 108/133 | 110/135 | 110/135 |
| census | variant | 93/97 | 59/81 | 58/92 | 78/92 |
| centroid | ordinary | 182/186 | 108/133 | 110/135 | 110/135 |
| centroid | variant | 93/97 | 59/81 | 58/92 | 78/92 |
| seq | ordinary | 182/186 | 110/133 | 112/135 | 112/135 |
| seq | variant | 93/97 | 60/81 | 59/92 | 79/92 |
| seq2:skip | ordinary | 182/186 | 121/134 | 121/135 | 121/135 |
| seq2:skip | variant | 93/97 | 62/82 | 60/92 | 77/92 |
| seq2:skip+same (used) | ordinary | 182/186 | 121/134 | 121/135 | 121/135 |
| seq2:skip+same (used) | variant | 93/97 | 64/82 | 60/92 | 80/92 |
| seq2:skip+readmit | ordinary | 182/186 | 118/134 | 116/136 | 116/136 |
| seq2:skip+readmit | variant | 93/97 | 62/83 | 61/92 | 77/92 |
| seq2 | ordinary | 182/186 | 123/134 | 121/136 | 121/136 |
| seq2 | variant | 93/97 | 63/83 | 60/92 | 78/92 |

B enumeration errors (seq2:skip+same, ordinary): {'a VerSe vertebra appears as two B bodies': 3, 'a VerSe vertebra has no B body': 1, "a B body inside the mask's range is mostly outside every VerSe vertebra": 1}.

| labeller A (VERIDAH names) | lumbar = read | lumbar, with a stump-rib L1 counted rib-bearing (L - 1) | thoracic = 12 where the read saw T1 | same, under the convention |
|---|---:|---:|---:|---:|
| ordinary | 120/120 | 120/120 | 47/47 | 47/47 |
| variant | 62/80 | 76/80 | 28/36 | 34/36 |

So A is the stronger labeller: exact on ordinary spines, and its misses on variant spines are mostly its own naming convention. B's thoracolumbar junction is its weak point -- TotalSegmentator cuts rib heads and short 12th ribs, so a B count is evidence beside a read or beside A, never a call on its own.

**A test that failed, reported rather than used.** If TS paints an L6 (or a fused L5/L6) as its 'S1', a disc under that body should leave little S1-to-sacrum contact across the body midline. Midline contact (mm2), ordinary reads n=184, median 190, IQR 127-283, range 0-760; non-fused L6 reads n=50, median 306, IQR 195-452, range 65-2090; Castellvi III/IV reads n=47, median 518, IQR 372-670, range 17-1215. The groups overlap almost completely, so this contact does not identify a transitional body and verifies nothing here.

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

## The old subtype table's VerSe rows, one by one (audit_resolution.csv)

| resolution | rows |
|---|---:|
| VERIFIED | 104 |
| KEPT (read); CONSISTENT, not verified | 13 |
| KEPT (read) but CONTRADICTED -> review | 11 |
| KEPT (read); not verifiable in this scan | 7 |
| MOVED sacralised_L5_fused -> unassigned | 3 |
| HELD FOR REVIEW (no row until adjudicated) | 2 |

Of the 84 audit-string-only rows: VERIFIED 56; KEPT (read); CONSISTENT, not verified 13; KEPT (read); not verifiable in this scan 6; KEPT (read) but CONTRADICTED -> review 6; MOVED sacralised_L5_fused -> unassigned 3.

- `verse278` (castellvi_I_II -> castellvi_I_II): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by mask lumbar ids + unlabelled bodies below = 4; B counts 4 lumbar (38 mm) / 4 rib-free (contact) (supported by A counts 5 lumbar)
- `verse507` (castellvi_I_II -> castellvi_I_II): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 6 lumbar (supported by mask lumbar ids + unlabelled bodies below = 5; B counts 5 rib-free bodies below the last rib (rib contact))
- `verse512` (L6 -> L6): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 4 lumbar; A counts 13 thoracic (consistent: mask lumbar ids + unlabelled bodies below = 5: the read's 6 with its Castellvi IIIb body unsegmented (paper's rule) and not separated from the sacrum by TS; B counts 5 lumbar (38 mm) / 5 rib-free (contact) = the read's 6 when the Castellvi IIIb body sits in the sacral complex)
- `verse540` (L6 -> L6): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 11 thoracic; B counts 5 lumbar (38 mm) / 5 rib-free (contact) (supported by release mask id 25; mask lumbar ids + unlabelled bodies below = 6; A counts 6 lumbar)
- `verse549` (sacralised_L5_fused -> unassigned): MOVED sacralised_L5_fused -> unassigned: read, voxel-verified: mask lumbar ids + unlabelled bodies below = 4; A counts 4 lumbar; B counts 4 lumbar (38 mm rule); B counts 4 rib-free bodies below the last rib (rib contact); A counts 12 thoracic; B counts 12 thoracic (38 mm rule); B counts 12 rib-bearing bodies from T1 (rib contact)
- `verse552` (sacralised_L5_fused -> unassigned): MOVED sacralised_L5_fused -> unassigned: read, voxel-verified: mask lumbar ids + unlabelled bodies below = 4; A counts 4 lumbar; B counts 4 lumbar (38 mm rule); B counts 4 rib-free bodies below the last rib (rib contact); A counts 12 thoracic
- `verse559` (sacralised_L5_fused -> unassigned): MOVED sacralised_L5_fused -> unassigned: read, CONTRADICTED by mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm) / 5 rib-free (contact)
- `verse571` (L6 -> L6): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 11 thoracic (supported by release mask id 25; mask lumbar ids + unlabelled bodies below = 6; A counts 6 lumbar; B counts 6 lumbar (38 mm rule); B counts 6 rib-free bodies below the last rib (rib contact))
- `verse588` (T13 -> T13): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 12 thoracic (supported by mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm rule); B counts 5 rib-free bodies below the last rib (rib contact); release mask id 28)
- `verse601` (T13 -> T13): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 12 thoracic (supported by release mask id 28) (consistent: mask lumbar ids + unlabelled bodies below = 4: the read's 5 with its Castellvi IIIa body unsegmented (paper's rule) and not separated from the sacrum by TS; A counts 4 = the read's 5 when the Castellvi IIIa body sits in the sacral complex; B counts 6 lumbar (38 mm) / 4 rib-free (contact) = the read's 5 when the Castellvi IIIa body sits in the sacral complex)
- `verse612` (L6 -> L6): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 5 lumbar (supported by release mask id 25; mask lumbar ids + unlabelled bodies below = 6; B counts 6 lumbar (38 mm rule); B counts 6 rib-free bodies below the last rib (rib contact))
- `verse615` (castellvi_I_II -> castellvi_I_II): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 4 lumbar; B counts 5 lumbar (38 mm) / 4 rib-free (contact) (supported by mask lumbar ids + unlabelled bodies below = 5)
- `verse765` (L6 -> L6): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by mask lumbar ids + unlabelled bodies below = 5; A counts 4 lumbar (supported by B counts 5 rib-free bodies below the last rib (rib contact, the stump-rib L1 rib-bearing))
- `verse814` (L6 -> L6): KEPT (read) but CONTRADICTED -> review: read, CONTRADICTED by A counts 4 lumbar (consistent: mask lumbar ids + unlabelled bodies below = 5: the read's 6 with its Castellvi IIIb body unsegmented (paper's rule) and not separated from the sacrum by TS; B counts 5 lumbar (38 mm) / 5 rib-free (contact) = the read's 6 when the Castellvi IIIb body sits in the sacral complex)
- `gl279` (L6 -> none): HELD FOR REVIEW (no row until adjudicated): labellers disagree: A four_lumbar vs B normal_count; release mask L6
- `verse707` (L6 -> none): HELD FOR REVIEW (no row until adjudicated): read NORMAL but release mask carries an L6 (id 25)

## The 56 raw-mask scans the render bank already holds (release-mask id 25 or 28)

| status now | scans |
|---|---:|
| verified | 48 |
| contradicted by the mask count or A -> review | 5 |
| no row: held for review | 2 |
| other: read, not reproducible from this scan's field (tho | 1 |

No row (drop or hold these renders): `gl279` (mask L6, read none: labellers disagree: A four_lumbar vs B normal_count; release mask L6); `verse707` (mask L6, read 7/12/5/5 castellvi 0/I: read NORMAL but release mask carries an L6 (id 25)).

## The three 'sacralization (4 lumbar)' scans, at voxel level

- `verse549` read 7/12/4/5 castellvi 0/I: mask `C1 C2 C3 C4 C5 C6 C7 T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 L1 L2 L3 L4`; unlabelled bodies below the mask's lowest vertebra (B) 0; A four_lumbar [nT=12 nL=4; C2..S]; B four_lumbar [nT=12 nL=4]; -> **unassigned** (read, voxel-verified: mask lumbar ids + unlabelled bodies below = 4; A counts 4 lumbar; B counts 4 lumbar (38 mm rule); B counts 4 rib-free bodies below the last rib (rib contact); A counts 12 thoracic; B counts 12 thoracic (38 mm rule); B counts 12 rib-bearing bodies from T1 (rib contact))
- `verse552` read 7/12/4/5 castellvi 0/I: mask `T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 L1 L2 L3 L4`; unlabelled bodies below the mask's lowest vertebra (B) 0; A four_lumbar [nT=12 nL=4; C6..S]; B four_lumbar [nT=None nL=4]; the column does not reach a complete C1/C2 in TS: T1 cannot be counted; -> **unassigned** (read, voxel-verified: mask lumbar ids + unlabelled bodies below = 4; A counts 4 lumbar; B counts 4 lumbar (38 mm rule); B counts 4 rib-free bodies below the last rib (rib contact); A counts 12 thoracic)
- `verse559` read 7/11/4/5 castellvi 0/I stump L1: mask `C3 C4 C5 C6 C7 T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 L1 L2 L3 L4 L5`; unlabelled bodies below the mask's lowest vertebra (B) 0; A thoracic_11 [nT=11 nL=5; C2..S]; VERIDAH skips T12 at a normal spacing (its count call); B thoracic_11 [nT=11 nL=5]; -> **unassigned** (read, CONTRADICTED by mask lumbar ids + unlabelled bodies below = 5; A counts 5 lumbar; B counts 5 lumbar (38 mm) / 5 rib-free (contact))

## One person, several series (verse400-417)

5 persons carry more than one row; every row carries `patient_key` = `verse:<subject>` from the VerSeFusion manifest (`tools/patient_keys.verse_subjects`), so counting persons, not rows, removes them. The old table listed verse403 and verse406 (subject ids) beside their own series verse255 and verse261: two people counted twice.

- verse:verse403: verse208 (L6, TL False, LS False), verse255 (L6, TL True, LS True)
- verse:verse406: verse214 (L6, TL False, LS False), verse261 (L6, TL True, LS True)
- verse:verse410: verse227 (unassigned, TL False, LS False), verse267 (unassigned, TL True, LS True)
- verse:verse415: verse243 (lumbar_rib, TL False, LS False), verse275 (lumbar_rib, TL True, LS True)
- verse:verse417: verse277 (castellvi_I_II, TL True, LS False), verse278 (castellvi_I_II, TL True, LS True)

## Transitional subjects no table has

Rows without a published read: 0 (none). Candidates against a NORMAL read (kept out of rows.csv, in the review queue for adjudication): 1 (verse707).

## Review queue

**22 high priority** (the mask or labeller A contradicts the read, a numerical variant with no subtype, a conflict with no read, or a held case) and 49 low priority (labeller B alone disagrees with a read the mask or A supports -- B's measured junction error, most likely). The queue is sorted high first.

71 scans (`review_queue/queue.csv`; renders `review_queue/<case>.jpg`, 71 rendered: left = sagittal bone MIP with the VerSe mask (cyan names) and VERIDAH's ctd names (orange); right = coronal MIP with TS bodies coloured by the registry's rib type, red thoracic / yellow stump / blue none, TS ribs outlined, TS sacral complex green).

| reason | scans |
|---|---:|
| labellers A and B disagree | 44 |
| a voxel count from the mask or labeller A contradicts the published read | 14 |
| labeller B alone disagrees with a verified read | 13 |
| numerical variant with no fitting subtype | 6 |
| labeller B alone counts L6 against a normal read and labeller A | 5 |
| labeller B alone counts four_lumbar against a normal read and labeller A | 2 |
| labellers disagree | 1 |
| read NORMAL but release mask carries an L6 (id 25) | 1 |
| release mask id order broken | 1 |
| labeller B alone counts T13 against a normal read and labeller A | 1 |

## What the renders show (looked at, not inferred)

`spot_check/` holds 25 renders: 23 positive calls outside the queue (up to four per subtype, verified first, by case id -- `spot_check/render_cases.csv`) and 2 extra named below. `spot_check/looked.csv` records what was seen in the renders opened, queue renders included.

| case | render | what it shows |
|---|---|---|
| verse559 | review_queue | 11 rib-bearing bodies (red), then 5 rib-less lumbar-type bodies (blue) sitting directly on the sacral complex (green); no body between the last lumbar and the sacrum. Mask, VERIDAH and TS agree: 23 presacral, 11 thoracic + 5 lumbar-type. The read's 7/11/4/5 with a stump at L1 leaves the stump vertebra out of both columns; this is not a sacralisation at voxel level. |
| verse549 | review_queue | 12 rib pairs, 4 rib-less lumbar bodies, the sacrum directly under L4; no fused or unlabelled body anywhere. A true four-lumbar spine (23 presacral), as read. |
| verse552 | review_queue | 12 rib pairs, 4 lumbar bodies, sacrum directly under L4: a true four-lumbar spine, as read. |
| verse707 | review_queue | The release mask's 'L1' carries full-length ribs in the coronal MIP (TS body B2, thoracic). The mask's naming is shifted one level, so its id-25 body is an L5. Read normal, VERIDAH L1-L5, TS 5 rib-less bodies. The old raw-mask L6 row and its renders are wrong. |
| gl279 | review_queue | Release mask T2-L6 with a thin (collapsed?) L3 about 15 mm tall; VERIDAH has no points on two lumbar bodies and TS merges the thin one. No read. The mask's L6 is not reproduced by either labeller: held. |
| verse601 | review_queue | T13 read with a fused L5 (IIIa): the unsegmented L5 is visible between the mask's L4 and the sacrum; TS gives both T12 and T13 only short ribs (both yellow), so B's 38 mm count puts the junction a level high. |
| verse113 | spot_check (extra; row not reproducible in this scan) | Lumbar-only field (mask L2-L6), no rib in view: VERIDAH's 'T12' is the partial top-edge body. The field cannot show the count; the row stands on the read. |
| verse024 | spot_check (extra; row consistent) | Castellvi IIIb L6: an unsegmented body sits between the mask's L5 and the sacrum, fused laterally; both labellers fold it into the sacral complex (count 5 = the read's 6 with the fused body there). |
| verse255 | spot_check | Six rib-less bodies on the sacrum below 12 rib pairs; last ribs at T12. A clean L6 (verified by mask, VERIDAH and TS). |
| verse502 | spot_check | Castellvi IIIb L6: the unlabelled fused body lies between the mask's L5 and the sacrum, VERIDAH's S point below it. |
| verse547 | spot_check | 12 full rib pairs and a 13th rib-bearing vertebra whose TS ribs are short on both sides: by the 38 mm rule on TS's ribs it reads L6, by rib contact T13; the read (one side over 38 mm) says T13. |
| verse602 | spot_check | 12 rib pairs plus a 13th vertebra with short ribs above five lumbar bodies: T13 as read. |
| verse524 | spot_check | Castellvi IIIb L5 fused between the mask's L4 and the sacrum; T12's TS ribs are short. B's 38 mm count of 5 was T12 + L1-L4, a coincidence the stump-level rule now excludes. |
| verse016 | spot_check | T12 with short TS ribs (hypoplastic last rib), then L1-L5 on the sacrum: normal count, as read. |
| verse141 | spot_check | 12 rib-bearing bodies then L1-L5 on the sacrum; TS did not segment the L1 rudiment, so the lumbar-rib label rests on the read while the count is confirmed. |
| verse015 | spot_check | Five lumbar bodies on the sacrum under a short-ribbed T12; posterior instrumentation across L3-L5. |

## Reproduce

```
# grid (sbatch -D ~/spinesurg-ct-nnunet; outputs under /rs/rs_grp_oschome/go2432/data/anomaly_harvest/verse)
sbatch --array=0-15 slurm/harvest_verse_ts.sh                 # labeller B input: TS 2.18.0 total on 374 CTs
SHARDS="14 15" sbatch --array=0-11 slurm/harvest_verse_ts_cpu.sh   # CPU fallback for pending GPU shards
CENSUS_OUT=$H/census_v3 FORCE=1 sbatch --array=0-31 slurm/harvest_verse_census.sh   # then once more without FORCE
CENSUS=$H/census_v3 CASES_FILE=... OUT_PNG=... sbatch --array=0-19 slurm/harvest_verse_render.sh
# local
python tools/harvest_verse_registry.py --census <census_v3> --table SchwingNet/results/polypose/inputs/verse_suppl_table1.csv \
    --manifest <VerSeFusion manifest.csv> --moller ~/lstv_flag/sources/moller_stump_ribs.csv \
    --old SchwingNet/results/rare_class/transitional_subtypes.csv --out SchwingNet/results/transitional_registry/verse
```
The census is `census_v3` (374 json, every scan with both labellers); `census`, `census_v2`, `census_test` beside it are superseded drafts.

## Cross-collection identity

- Every row is keyed `verse:<subject>`. CTSpinoPelvic1K render banks name 314 VerSe series `CTSP_VERSE_<series>` (DATA_ACCOUNTING alias 8): those are these subjects, not CTSpinoPelvic1K patients.
- CTSpine1K redistributes VerSe scans; the other_ct stream's `alias.json` (read 2026-09-23) holds 782 colonography aliases and **no** `verse:` alias, so a CTSpine1K VerSe scan screened there would enter as a new person. The coordinator should key those to `verse:<subject>` before counting persons across streams.
- VerSe has no real projections: `real_frames` is False on every row; all rows may feed renders.

## What is not known

- Labeller B's rib attachment fails where TotalSegmentator stops a rib short of its head; the outside check above is its measured error, and a B count is never used alone to make or break a read row.
- A Castellvi III/IV body is invisible to the release mask by the paper's rule; where neither labeller separates it from the sacrum the row is 'consistent', not 'verified'.
- The table's thoracic count is assumed (12) wherever T1 is outside the field; T13 is therefore only as complete as the scans that reach T1.
- Castellvi grade I shares a cell with grade 0 in the table, so castellvi_I_II holds grade II only.

