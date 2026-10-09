# Transitional registry -- COBRA2026 arm

Built by `tools/harvest_cobra.py collect` on 2026-09-24 06:49 from 692 per-case records (grid: `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/cobra/cases_v5/`, one json and one MIP per planning CT, `tools/harvest_cobra.py case`). Rows: `rows.csv` / `rows.json`, the shared registry schema, one row per CT. Review queue: `review_queue/review_queue.csv` and one render per queued CT.

**Every COBRA2026 person has REAL kV projections. A transitional person found here is a TEST subject and is never rendered for training** (`real_frames` = True on every row).

Two labellers, both on `ct_def` (the planning CT deformed to the CBCT; the image SPINEPS already read), so a disagreement is a labeller disagreement and not a different image:

- **A = SPINEPS + VERIDAH.** Level names come only from the ctd POI file, bound to instances by position and checked for one-to-one binding and strict S-I order (`tools/cobra_lstv_screen.py ctd_names`); the mask then passes the project's id guard (`tools/spineps_ids.py`; VERIDAH's T12 skip is let through with the guard's allow_skipped_names switch, because B gates the count -- refusing it cost six CTSpinoPelvic1K L6). A mask id is never a name. A's count is the number of lumbar names between the thoracic names and a named sacrum. The thoracolumbar junction counts as in the field only with two thoracic names (the VerSe stream's rule: a single 'T12' at the top edge is often an L1 named from shape). A lumbar name whose SPINEPS instance is a sliver refuses the count (names and bodies disagree).
- **B = TotalSegmentator 2.18 `total`**, counted geometrically by `tools/transitional_ts_count.py`: the vertebra union split into bodies at the discs, TS ribs attached by their head, V = the last rib-bearing body, n_lumbar = free bodies between V and the S1 body. TS names are never a level. V is a reference only if it lies wholly inside the field and the body directly above it bears ribs too (added 2026-09-24, below).
- A count needs BOTH junction references in the field. A cut field is `no_count`, never normal. T13 needs the rib cage counted from T1.

## Denominators

| quantity | CTs |
|---|---:|
| planning CTs on disk | 692 |
| with a per-case record | 692 |
| labeller A usable (SPINEPS ran, ctd names pass their checks and the id guard) | 674 |
| labeller B usable (TotalSegmentator mask on the CT grid) | 692 |
| lumbosacral junction in the field (either labeller) | 692 |
| thoracolumbar junction established in the field (either labeller) | 198 |
| **junction-only: sacrum in the field, thoracolumbar reference not** | **494** |
| A made a lumbar count | 189 |
| B made a lumbar count | 131 |
| both counted / agree on the count | 125 / 118 |
| T1 in the field (A: C7 and T1 named / B: two rib-free bodies above the rib cage) | 3 / 1 |

## Rows by subtype and tier

One CT is one person here (patient key `cobra:<case>`, below), so rows = distinct patients. Tier `` (empty) = no truth: `no_count` (neither labeller could count) or `unresolved` (the two counts disagree; in review).

| subtype | two-labeller | single-labeller | no tier | rows = patients |
|---|---:|---:|---:|---:|
| L6 | 2 | 1 | 0 | 3 |
| unassigned | 4 | 2 | 0 | 6 |
| unresolved | 0 | 0 | 11 | 11 |
| normal_lumbar_count | 112 | 63 | 0 | 175 |
| no_count | 0 | 0 | 497 | 497 |

No COBRA row is `read` (no radiologist has read these CTs) and none is `morphology-only` (the one morphology this arm has, the mask Castellvi screen, fails its outside check on CTSpinoPelvic1K; below). `castellvi` is empty on every row for the same reason. `four_lumbar` rows: 6; `lumbar_rib` candidates: 1.

### Transitional rows (9)

| case | subtype | tier | A | B | four_lumbar | looked |
|---|---|---|---|---|---|---|
| A270 | L6 | single-labeller | L6 (6) | no_count (None) | False | credible |
| B127 | L6 | two-labeller | L6 (6) | L6 (6) | False | credible |
| D238 | L6 | two-labeller | L6 (6) | L6 (6) | False | credible |
| B084 | unassigned | single-labeller | unassigned (4) | no_count (None) | True | credible |
| B091 | unassigned | single-labeller | unassigned (4) | no_count (None) | True | credible |
| D014 | unassigned | two-labeller | unassigned (4) | unassigned (4) | True | credible |
| D484 | unassigned | two-labeller | unassigned (4) | unassigned (4) | True | credible |
| F058 | unassigned | two-labeller | unassigned (4) | unassigned (4) | True | credible |
| F089 | unassigned | two-labeller | unassigned (4) | unassigned (4) | True | doubtful |

### Unresolved: the two counts disagree (11)

| case | A (n) | B (n) | looked |
|---|---|---|---|
| A026 | unassigned (4) | normal_lumbar_count (5) | looked |
| A072 | unassigned (4) | no_count (None) | looked |
| A283 | normal_lumbar_count (5) | L6 (6) | looked |
| B002 | normal_lumbar_count (5) | L6 (6) | looked |
| B005 | normal_lumbar_count (5) | unassigned (4) | looked |
| B054 | failed (None) | unassigned (4) | rejected |
| B126 | unassigned (4) | no_count (None) | looked |
| C156 | unassigned (4) | normal_lumbar_count (5) | looked |
| D154 | normal_lumbar_count (5) | unassigned (4) | looked |
| D405 | unassigned (4) | no_count (None) | looked |
| F118 | normal_lumbar_count (5) | unassigned (4) | looked |

**both_L6_T13 and T13 were looked for on every CT** (either labeller counting 13 rib-bearing from T1, with or without six lumbar). T1 is in the field on 3 CTs by A's names and 1 by B's bodies; found: T13 0, both_L6_T13 0. VERIDAH names a T13 on 45 COBRA CTs; none can be counted (notes carry them).

## Screenable at the lumbosacral junction only

The pelvic RT planning fields stop low: **494 of 692** CTs have the sacrum in the field but no established thoracolumbar reference. On these no count exists -- an L6, a sacralised L5 and an ordinary spine look the same without the last rib-bearing vertebra -- so every one is `no_count`, never normal. What CAN be read there is the junction itself: VERIDAH's shape name for the lowest mobile vertebra, TS's S1 separating from its sacrum (a lumbarised S1), and Castellvi morphology. None is a count, so none makes a row subtype; each is a CANDIDATE for a reader and sits in the review queue at priority 5.

- VERIDAH named an L6 at the junction: **35** CTs (A158, A162, A172, A213, B015, B041, B067, C129, D004, D015, D244, D271, F108, G010, G055, G061, G095, G096, G103, G111, G113, G127, G143, G155, G159, G161, G163, G164, G178, G190, G193, G194, G202, G203, G206).
- VERIDAH named an L6 that SPINEPS gives no body (a sliver, or its point inside the sacrum instance), so A refuses to count: **8** CTs (A302, B081, C178, D018, F052, G091, G122, G192). On CTSpinoPelvic1K two of the four such spines were L6 (the transitional segment inside SPINEPS's sacrum) and two were slivers on ordinary spines.
- TS's S1 barely touches its sacrum: **0** CTs (none); the flag never fired on the 800 CTSpinoPelvic1K CTs either, reader L6 included, so its absence says nothing.
- How much a junction-only VERIDAH L6 is worth is NOT measured: on CTSpinoPelvic1K 15 of its 18 L6 names were L6, but every CTSP field held the rib cage, so VERIDAH had context it lacks here. The per-centre rate below says the COBRA names are not taken at face value: centre G's rate is far above any published L6 prevalence.

| centre | CTs | junction-only | VERIDAH L6 at the junction |
|---|---:|---:|---:|
| A | 120 | 84 | 4 |
| B | 107 | 41 | 3 |
| C | 120 | 110 | 1 |
| D | 120 | 63 | 4 |
| F | 92 | 66 | 1 |
| G | 133 | 130 | 22 |

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

## Labeller A (rows) x labeller B (columns)

| A \ B | L6 | no_count | normal_lumbar_count | unassigned | unresolved |
|---|---:|---:|---:|---:|---:|
| L6 | 2 | 1 | 0 | 0 | 0 |
| failed | 0 | 22 | 5 | 1 | 0 |
| no_count | 0 | 475 | 0 | 0 | 0 |
| normal | 0 | 0 | 0 | 0 | 1 |
| normal_lumbar_count | 2 | 58 | 111 | 3 | 0 |
| unassigned | 0 | 5 | 2 | 4 | 0 |

Lumbar counts where both labellers count (A, B): (4, 4) 4, (4, 5) 2, (5, 4) 3, (5, 5) 112, (5, 6) 2, (6, 6) 2

## The SPINEPS+VERIDAH screen before the field-of-view rule

`tools/cobra_lstv_screen.py` (ctd-named) reported {"ordinary": 344, "L6": 38, "T13": 45, "both": 0, "four_lumbar": 8, "unreadable": 257} over 692 CTs. Its L6 and T13 calls include cut fields: VERIDAH names levels by appearance, so a field holding L2-S1 still gets an 'L5' or an 'L6'. Under the count rule used here those are `no_count` (junction-only candidates if L6).

## How far the labellers can be trusted: CTSpinoPelvic1K

Against reader truth (two-reader Castellvi consensus + release lumbar ids; 18 L6):

| | before | after |
|---|---|---|
| CTs | 802 | 802 |
| A counts | 789 | 772 |
| B counts | 799 | 732 |
| B: six / of them L6 | 51 / 11 | 19 / 10 |
| B: ordinary counted 5 / 4 / 6 | 657/747 / 48 / 40 | 668/686 / 8 / 9 |
| A: six / of them L6 | 18 / 9 | 13 / 7 |
| A: ordinary counted 5 / 4 / 6 | 712/739 / 18 / 9 | 700/724 / 18 / 6 |
| both count / agree | 786 / 664 | 719 / 667 |
| **two-labeller L6 / of them L6** (Wilson 95 %) | **12 / 6** ([25.4, 74.6]) | **7 / 5** ([35.9, 91.8]) |
| two-labeller L6 that are not L6 | 0105, 0419, 0474, 0672, 0895, 1151 | 0090, 0474 |
| L6 reaching the two-labeller tier | 6 of 18 ([16.3, 56.3]) | 5 of 18 ([12.5, 50.9]) |
| two-labeller four / on ordinary spines | 13 / 1 ({'sacralised_L5_fused': 3, 'lumbar_rib': 6, 'ordinary': 1, 'unassigned': 3}) | 9 / 1 ({'sacralised_L5_fused': 2, 'ordinary': 1, 'lumbar_rib': 4, 'unassigned': 2}) |
| ordinary: both count / agree on 5 | 736 / 630 | 677 / 643 |

The reader truth names only the release's own L6 ids and the readers' Castellvi calls. The CTSP stream found eleven more L6 in it (nine with six rib-free vertebrae by the release's own voxels, two hidden by release labelling defects: SchwingNet/results/transitional_registry/ctsp/SUMMARY.md), so a 'two-labeller L6 that is not L6' above can be a registry L6; the registry table below is the better reference.

Against the CTSP registry (reads + release + three body labellers on the release's student-reviewed ribs; 29 L6):

| | before | after |
|---|---|---|
| CTs | 802 | 802 |
| A counts | 789 | 772 |
| B counts | 799 | 732 |
| B: six / of them L6 | 51 / 20 | 19 / 15 |
| B: ordinary counted 5 / 4 / 6 | 655/735 / 47 / 31 | 667/679 / 7 / 4 |
| A: six / of them L6 | 18 / 15 | 13 / 12 |
| A: ordinary counted 5 / 4 / 6 | 707/727 / 17 / 3 | 695/713 / 17 / 1 |
| both count / agree | 786 / 664 | 719 / 667 |
| **two-labeller L6 / of them L6** (Wilson 95 %) | **12 / 11** ([64.6, 98.5]) | **7 / 7** ([64.6, 100.0]) |
| two-labeller L6 that are not L6 | 0419 | none |
| L6 reaching the two-labeller tier | 11 of 29 ([22.7, 56.0]) | 7 of 29 ([12.2, 42.1]) |
| two-labeller four / on ordinary spines | 13 / 0 ({'sacralised_L5_fused': 3, 'lumbar_rib': 6, 'unassigned': 4}) | 9 / 0 ({'sacralised_L5_fused': 2, 'unassigned': 3, 'lumbar_rib': 4}) |
| ordinary: both count / agree on 5 | 724 / 629 | 670 / 642 |

On CTSpinoPelvic1K after the change, B's split-pair rule fired on 93 CTs, the stub rule on 19; B refused an unestablished reference on 55 and a split body on 12. The stub rule was DERIVED on CTSpinoPelvic1K (19 of B's false sixes carried a short TS rib piece on the first free body), so its share of the improvement is not an independent test. The split-pair, reference and fragment rules and A's two rules were written from COBRA failures; the fragment rule's thresholds were checked here before adoption, so that one is only half independent.

**Castellvi mask morphology fails its outside check** (after the change): of 33 spines with a reader Castellvi grade above 0, A marks 15, B 29, both 15; of the reader-ordinary spines, A marks 379 of 741 measured, B 676 of 747, both 370. A screen that marks most ordinary spines assigns no subtype here.


## What the renders showed

Claude looked at the renders listed here (the `looked` column of the queue and of `notes`). This is not a radiologist read.

- **A026**: The vertebra VERIDAH names T12 carries only a 16 mm TS rib stub; B counts it free (five), VERIDAH counts four below it. Under the 38 mm rule it is lumbar with a rudimentary rib. An anomaly of the last rib either way (hypoplastic 12th rib or lumbar rib).
- **A072**: VERIDAH counts four below 'T12'; TS draws no rib on that body, and B counts five below its last rib-bearing object, which is cut by the top of the field (T11).
- **A260**: The body VERIDAH calls T13 carries only a short TS rib piece. B's stub rule counts it as a hypoplastic 12th rib (five); without the rule, or under the 38 mm rule, it is lumbar and the count is six. A read decides.
- **A270**: [credible] VERIDAH names T8-T11 and then six lumbar vertebrae, skipping T12 (its 11-thoracic encoding); A's sagittal MIP shows six separate bodies between the last rib-bearing vertebra (T11 on both labellers) and the sacrum. B's own count was refused (two of its pieces 14 mm apart). On CTSpinoPelvic1K all six spines where VERIDAH skipped T12 and named six lumbar were registry L6 (0068, 0302, 0672, 0895, 0950, 1151). A thoracolumbar-type L6 candidate from one labeller.
- **A283**: Both labellers see the same bodies. VERIDAH names the first body below T12 'T13', with five lumbar under it; TS draws no rib on it, so B counts six free (regular 28-37 mm steps). A rib on that body makes five below it (a T13, not countable here: T1 is not in the field); none makes six (L6 by the rib convention).
- **A302**: VERIDAH's 'L6' point lies at the top of the sacrum, inside SPINEPS's sacrum, with a 'T13' above five lumbar names; B sees five free bodies below its (cut) last rib-bearing object. It reads as VERIDAH's names running one level long, not an L6.
- **B002**: Same pattern as A283: VERIDAH's 'T13' has no TS rib, so B counts six. An unattached 32 mm TS rib piece lies 23 mm from the column beside it; if it is that vertebra's rib, it is under 38 mm (lumbar under the published rule, six) but rib-bearing by contact (five).
- **B005**: The vertebra VERIDAH names L1 carries a 36 mm TS rib and is B's reference, so B counts four. Under the 38 mm rule it is lumbar: a lumbar-rib candidate with five lumbar, as A counts. VERIDAH also names a T13 above it.
- **B054**: [rejected] Severe degenerative scoliosis with osteophytes. SPINEPS crashed. B's last rib-bearing object and its first free body overlap at one level on the coronal MIP, so its four cannot be read from these masks.
- **B084**: [credible] VERIDAH names four lumbar below a 'T13', and TS attaches ribs to that same vertebra (B's last rib-bearing object). B's own count is refused because its disc split cut L3-L4 into fragments. Both labellers see four bodies between the last rib-bearing vertebra and a broad sacral top.
- **B091**: [credible] VERIDAH names four lumbar below a 'T13'. B also counts four free bodies below its last rib-bearing object, but that object (two TS vertebra labels in one piece) touches the top of the field, so B's count is refused. TS ribs reach the vertebra VERIDAH calls T13.
- **B117**: B's former six held a 17 ml piece split from L2 (body steps 20-23 mm); the fragment rule now refuses B's count and A's five matches the MIP.
- **B126**: VERIDAH names 'T13' then four lumbar; TS draws no rib on 'T13', and B counts five free bodies below its last rib-bearing object (refused: the object above that one is cut by the field and carries no rib). Same question as C156.
- **B127**: [credible] Six mobile bodies between T12 (the last pair of long ribs) and the sacrum on both labellers; the lowest sits between the iliac crests and looks free on the sagittal MIP; B's body centres step regularly (26-32 mm). A credible L6.
- **C108**: Degenerative collapse of the lumbar spine; B's former L6 had body centres 10 mm apart (split pieces side by side); refused by the fragment rule. SPINEPS crashed on this CT.
- **C156**: VERIDAH names 'T13' and then four lumbar; TS draws no rib on 'T13', so B counts five. A rib on it gives four lumbar (T13 or a rib-bearing L1); none gives an ordinary five.
- **D004**: Junction only. The field is cut through the top vertebra (VERIDAH's T12); A's sagittal MIP shows six bodies between it and the sacrum, but B's bodies are malformed (tall and small pieces). If the cut top vertebra bears the 12th ribs this is an L6; the field cannot say.
- **D014**: [credible] Four free bodies below a vertebra with long ribs (64-75 mm) on both labellers; TS stretched its five lumbar labels over four bodies (two bodies hold two TS labels each). VERIDAH names that vertebra T13. The sacral top is broad between the iliac crests. A rib-bearing first lumbar (T13 or lumbar rib) and a sacralised L5 cannot be told apart without T1.
- **D015**: Junction only, the strongest such candidate: six separate bodies between a cut top vertebra (VERIDAH's T12) and the sacrum on A's sagittal MIP. B's last rib-bearing object is that cut vertebra merged with the next one, and B finds four free pieces below it. Whether the cut vertebra or the next one bears the 12th ribs decides L6 versus ordinary.
- **D034**: B's former six held an 18 ml piece of T12 (a 17 mm step); refused by the fragment rule.
- **D154**: A's L5 sits deep between the iliac crests; TS's L5 body lies at the level of its S1 body, so B leaves it out and counts four. The four-versus-five pattern of a sacralised L5 (CTSpinoPelvic1K 0094 reads the same way): a sacralisation candidate for a reader.
- **D238**: [credible] Six mobile bodies below T12 on both labellers, body steps regular (32-43 mm). The lowest (VERIDAH's L6) is overlapped by the sacral ala on the coronal MIP: an L6 by count whose junction may be a lumbarised S1 or a Castellvi segment; the morphology is for a reader.
- **D404**: B's former six held two 35-39 ml pieces (L1 and L4/L5 split); refused by the fragment rule. A's five below T12 is what the MIP shows.
- **D405**: As B126: VERIDAH's 'T13' shows no TS rib, B counts five below a cut reference, VERIDAH four.
- **D484**: [credible] Four bodies between T12 and the sacrum on both labellers; the sacrum starts broad at the iliac crests. T12's TS ribs are 34 mm (left) and 50 mm (right): one over 38 mm, so T12 stays thoracic under the published rule. Four-lumbar or a sacralised L5.
- **F058**: [credible] Whole-spine field, C6 to the sacrum. VERIDAH names C7, T1-T12 and four lumbar vertebrae; B's four free bodies agree, but TS merged T3-T5 into one object and left T6 rib-free, so B has no thoracic count. The last ribs are short (39 mm). A four-lumbar spine with twelve thoracic names: a numerical reduction or a sacralised L5 (the lowest mobile body sits at the iliac crests).
- **F089**: [doubtful] Four free bodies on both labellers, but the last rib-bearing vertebra's TS ribs are 31 mm and a 20 mm stub, both under 38 mm: under the published rule it is lumbar and the count is five with rudimentary ribs (lumbar_rib). Also B's third free body is 1.8 x the others' volume and holds two TS labels (L4 51 %, L3 49 %), possibly two bodies. A read decides four-lumbar versus lumbar rib.
- **F118**: B merged two bodies (L2-L3) into one 81 mm object, flagged: its four is a merge error, and A's five below the last rib-bearing vertebra is what the MIP shows. VERIDAH names that vertebra T13 and TS gives it ribs; T1 is not in the field, so no thoracic count.
- **G010**: Junction only: three mobile bodies in the field. VERIDAH's 'L6' is the lowest mobile body, which looks like an ordinary L5 between the iliac crests on this MIP. Nothing here supports a sixth lumbar vertebra.

## Review queue

`review_queue/review_queue.csv`: **79** CTs, 79 renders (`<case>.jpg`: top row labeller A, SPINEPS instances with their ctd names; bottom row labeller B, TS bodies by role -- orange = last rib-bearing, cyan = free, gold = rib-bearing, yellow = TS ribs, green = sacrum; left a sagittal slab MIP, right a coronal slab MIP). Fill in `greg_verdict`.

| priority | meaning | CTs |
|---|---|---:|
| 1 | confirm a two-labeller transitional call (real-frame TEST subject) | 6 |
| 2 | the two labellers count differently | 11 |
| 3 | a transitional call from one labeller; the other could not count | 3 |
| 4 | labeller B raised a flag that can move its count; the two labellers put the thoracolumbar boundary at different levels | 16 |
| 5 | junction-only: no count; a shape or S1 sign at the lumbosacral junction | 43 |

## People

Patient key `cobra:<case>` from `tools/patient_keys.py key_any` (scheme leak_check:cobra.frame); 0 CTs could not be keyed. docs/DATA_ACCOUNTING.md declares no alias class joining COBRA2026 to another collection. Two case ids holding one CT would be one person: the first 8 MB of every ct_original.mha pixel block were hashed (692 of 692); identical groups: 0. A patient treated twice under two case ids with two different planning CTs would not be caught; not tested further.

## What is not known

- **No COBRA row has a reader's truth.** `two-labeller` means two models that fail differently agree. Its worth is measured on CTSpinoPelvic1K (above), whose colonography CTs are not these RT planning CTs (older patients, 2-3 mm slices, deformed to the CBCT, fields cut at the thoracolumbar junction). The review queue is the safeguard, not a formality.
- The rules added on 2026-09-24 (B: split rib pair, established reference, fragment refusal; A: two thoracic names, sliver refusal, T12 skip allowed) were written after looking at COBRA failures, and scored on CTSpinoPelvic1K before and after (above). None was tuned there, except that the fragment rule's two thresholds were checked there before adoption. Other COBRA-only failure modes may remain.
- Labeller A failed on 28 CTs (SPINEPS crashed, the ctd failed its one-to-one / order checks, or a lumbar name had no SPINEPS body); those rows rest on B alone or are `no_count`.
- Labeller B's rib length threshold is 30 mm; the published rule (Loffler et al. 2021) is 38 mm from the costovertebral joint, and TS rib masks often lack the head, so TS lengths under-estimate. Where the last rib-bearing vertebra's longest TS rib is under 38 mm the row says so (`lumbar_rib` candidate or a note).
- Four-lumbar rows cannot be split into a sacralised L5 (Castellvi III/IV), a rib-bearing L1 (lumbar rib) or a true numerical reduction without a read: they are `unassigned` + `four_lumbar`, as the subtype definitions require.
- T13 cannot be assessed on COBRA: T1 is almost never in the field.
- Whether the junction-only VERIDAH L6 names are L6 is not known (above).
- Both labellers read ct_def, the planning CT deformed to the CBCT. The deformation cannot change a count, but the images are not the undeformed anatomy.
