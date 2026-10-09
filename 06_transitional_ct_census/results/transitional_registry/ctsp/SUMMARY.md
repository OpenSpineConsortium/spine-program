# CTSpinoPelvic1K: transitional registry rows, three labellers per CT

Built by `tools/ctsp_registry_census.py` and `tools/ctsp_registry_ts.py` (grid, one record and one render per CT each) and `tools/ctsp_registry_build.py` (this folder). A count is the number of NON-RIB-BEARING presacral vertebrae between the lowest rib-bearing vertebra and the sacrum; it needs both in the field of view, and a cut field of view is 'no count', never 'normal'. Every count is name-free. **A** is the v11 release (its bodies and ribs; scheme read by `ostk.labels.labels_for`). **B** is SPINEPS, counted by its instances (never by an id). The mask ids pass `tools/spineps_ids.py` before the sacrum instance is read. **C** is TotalSegmentator's bodies (`~/bench/totalsegmentator/native`, with 0533 and 0921 from a private re-run (finding 11); every connected component of its vertebra classes). The three body segmentations were made independently, and all three are counted with the release's student-reviewed ribs, because SPINEPS segments no ribs. The rib source is checked by re-counting all three with TotalSegmentator's own ribs. That check is reported and never votes, because TotalSegmentator's rib masks often lack the rib head (see the findings). VERIDAH's name-based count is reported and never votes. A rib is borne by the vertebra nearest to its HEAD (its medial 10 mm). A rib cut by the FOV edge establishes nothing. A counted body more than 1.6 times the median of its neighbours is two vertebrae under one label, and that count is refused.

## What the counts and the renders showed

Claude wrote this section after looking at the renders in `review_queue/`. It is not a radiologist read. The per-CT notes
are in `looked.json`, and each one also appears in that row's `notes` and in the queue's `looked` column. A second pass
on 2026-09-24 added the anterior-sacral reformats (point 4), the rib-bearing comparison (point 9), the morphology
screens (point 10), the retried labellers (point 11), the reads whose readers counted differently (point 12), and one
tier change (1090, point 6).

**The registry holds 64 CTSpinoPelvic1K people, 13 more than the release's names and reads call.** Before this pass
there were 52 subtype rows: 18 L6, 12 sacralised, 4 Castellvi I-II, 14 lumbar rib and 4 unassigned. One of the
unassigned, 1043, turned out to be a labelling artefact and is not a row (point 4 below). Thirteen are new: eleven L6
and two four-lumbar spines.

1. **Nine spines have six rib-free vertebrae although the release names them ordinary.** They are 0105, 0359, 0474,
   0544, 0552, 0672, 0895, 1151 and 1153. In each, the release's own voxels already say six: its T12 carries no rib and
   the last ribs are on T11. SPINEPS's bodies agree in all nine. TotalSegmentator's bodies agree in 0474 and 1153 and
   are refused in the rest: in four it merged two bodies under one label, and in three its chain has a gap. On the thin
   sagittal slabs of 0105, 0474 and 1151,
   each of the six bodies has a disc above and below. No rib stub sits beside the release's T12 on any of the MIPs. By
   the project's rib convention (docs/STUDENT_FLUORO_CORRECTION_GUIDE.md) these are L6. **They are not the same
   anatomy as the release's 18 L6.** In the release's cases the sixth segment is at the lumbosacral junction, and 17 of
   the 18 carry a Castellvi grade. Here the extra rib-free segment is at the thoracolumbar junction, and the thoracic
   count is unknown because no CTSP FOV reaches T1. Eleven rib pairs with five lumbar and twelve with an L6 cannot be
   told apart on these CTs. A C-arm view that shows the last rib and the sacrum would count six in both.
2. **Two L6 spines are hidden by release labelling defects.** In 0090 the release's L2 covers two bodies (92 ml
   against 50-65 ml neighbours), and its spine labels are pseudo-labels. SPINEPS and TotalSegmentator both find six.
   In 0150 the release's five lumbar labels straddle six bodies. SPINEPS finds six, and TotalSegmentator draws six
   bodies but merges two under one name. 0150 is single-labeller.
3. **Two spines have four free lumbar bodies that no reader has graded.** In 0349 and 1000, SPINEPS and TotalSegmentator
   both put the release's L5 into the sacrum. On 0349 the release's L5 looks like the top sacral segment, and the lowest
   mobile vertebra has broad transverse processes against the ala. On 1000 the release's L5 looks mobile on the MIP
   sagittal. Both need a reader. The sacral reformats (point 4) back that split: 0349 looks sacralised, and 1000's L5
   looks transitional but not fused. On that look, 1000's true count may be five, which would make its four-lumbar row
   wrong. It stays a row, with the labellers' count and this note, until a reader decides.
4. **The four 'unassigned' spines are resolved as to labelling, and the sacrum splits them.** 0801, 0931 and 1123 are
   four-lumbar by all three labellers. Their 12th ribs are on T12, four rib-free bodies follow, and then the sacrum.
   1043 is a labelling artefact: the release skips the L3 id, and all three labellers count five. It is no longer a row.
   The count cannot tell a sacralised L5 (a six-segment sacrum) from a true four-lumbar spine. For that,
   `tools/ctsp_sacrum_look.py` unrolls the anterior sacral surface as a curved reformat at three depths
   (`review_queue/sacrum/`). Twenty-eight CTs were rendered: the five four-lumbar spines, 0172, thirteen controls, and
   nine reads (point 12).
   Counting foramina automatically failed in CTSpinoPelvic1K at every setting (docs/LAB_JOURNAL.md), so the renders
   were read by eye against controls first. What separated the controls was not the number of foramen pairs, which
   could not be counted reliably on the read-sacralised spines. It was where the first anterior pair sits, measured
   down the surface from the last mobile disc (about +-5 mm by eye):

   | group | CTs | first pair below the last mobile disc |
   |---|---|---|
   | normal (the readers' reference 0016; four plain spines 0001 0319 0608 0883) and read L6 (0234 0960) | 7 | 30-42 mm, no segment above it |
   | read sacralised, fused L5 visible as an extra body-shaped segment above the first pair | 4 (0008 0094 0151 0158) | 58-84 mm |
   | read sacralised, no extra segment visible | 2 (0760 47 mm, 1031 37 mm) | in or just above the normal range |
   | **0349, 0801, 0172** | 3 | about 90, 72 and 90 mm, extra segment visible: **looks sacralised** |
   | **0931, 1123** | 2 | about 38 mm: **looks like a normal sacrum** |
   | **1000** | 1 | about 35 mm below a narrow but dark L5/S1 space: **L5 separate, transitional, not fused** |

   So 0801's four lumbar vertebrae probably include a sacralised L5 inside the release's sacrum label, as in the read
   cases 0094, 0151 and 0158. 0349 is a sacralised L5 under its own id, as in 0008. For 0931 and 1123 a true
   four-lumbar spine is the plain reading, but two of the six read-sacralised controls also look normal here, so this
   view cannot rule out sacralisation. 0172 agrees with the re-read queue's five foramina and suspected sacralization.
   None of these is a read, no subtype moved on this look, and each note is in the row and the queue.
5. **Labellers made false calls that this pass rejects.** In seven plain spines VERIDAH names an L6 that is not a
   body. It is a sliver in 0249 and 0326, shares an instance with L5 in 0489 and 0636, and sits inside the sacrum
   instance in 0133, 1009 and 1152. Four of the seven were looked at, and the other three are read from their census
   records. 0038 is a two-series CT stitched at S1, and SPINEPS split S1 at the seam into a sixth body. SPINEPS left a
   real L5 as a sliver in 0331, which was looked at, and in 1129, from its census record. An id-80 blob made a sixth
   'body' in 0217. None of these is a row. Every one that still has a 4 or 6 somewhere is in the queue at priority 6.
6. **Some release "lumbar ribs" are 12th ribs.** In 0720 the right one sits on T12 beside the left 12th rib. In 1090
   the "lumbar ribs" on L1 are long ribs, the release's thoracic names run one level high, and its label is off the CT.
   Both rows stay, because the subtype is defined by the release's label, and both are now single-labeller. 1090 was
   two-labeller in the first pass, because a TotalSegmentator rib overlaps its release lumbar rib (61 %/54 %). That
   overlap shows a rib is there. It cannot show the rib is on a lumbar level when the release label is off its CT.
   Its "lumbar ribs" are 9.5/10.3 ml, against 0.4-4.3 ml for every other release lumbar rib.
   Nine of the 14 lumbar-rib rows are two-labeller: a TotalSegmentator rib covers at least 30 % of the release's
   lumbar-rib voxels. Five are not, and 0389 is one of those, with small stubs that TotalSegmentator does not segment.
7. **SPINEPS has no body for the release's L6 in 7 of the 18.** It puts the transitional segment (Castellvi II-IV,
   articulating with or fused to the ala) inside its sacrum. This was looked at on 0097, 0268 and 0376. These rows stay
   read-tier, and the queue marks them priority 4.
8. **Three release labels do not sit on their CT.** For 0487, 0527 and 1090, only 0.66-0.69 of TotalSegmentator's spine
   voxels land on release spine voxels, against a median of 0.94, and the release contours cut through the bodies on the
   render. Partial misalignment in the lumbar region (0150, 0419) and a stray fragment on a rib (0344) were also seen on
   the renders; the overlap test does not catch those. These are defects in the v11 release to fix at the source.
   0487 and 0527 are not rows, because SPINEPS and TotalSegmentator both count five. They are now in the queue at
   priority 5, because their release labels are unusable.
9. **Rib-bearing vertebrae, release against SPINEPS.** Both use the same rib voxels, each on its own bodies. In 795 CTs
   both place a lowest rib-bearing vertebra. They put it on a different vertebra in one: 0487, whose release label is off
   its CT. They differ in the NUMBER of rib-bearing vertebrae in the FOV in 160 CTs. In 158 of those the lowest one is
   the same (one of the other two is 0487, and one has no lowest to compare). The difference lies higher up. In most of
   them one labeller keeps a vertebra cut by the FOV's top edge and the other drops it. A number that differs above the
   junction cannot change a count, so none of these is a candidate.
10. **The morphology screens are candidates for a reader, not rows.** CTSpinoPelvic1K's learned Castellvi screen ranks 25
   unread CTs (`docs/castellvi_reread_queue.csv`), and its type-I height pre-filter calls 214
   (`docs/castellvi_type1_queue.csv`). The pre-filter's own author found it over-calls about 1.7-fold against a published
   prevalence, because it tests height alone. The two screens cover 218 CTs, and 10 of them are already registry rows.
   Three of the nine thoracolumbar L6 in point 1 are in the screen's top 25: 0544, 0552 and 0672. The 16 top-25 CTs
   that nothing else queued are now at priority 7, with TotalSegmentator renders through the transverse processes and
   ala, which is what a Castellvi II read needs. Both lists are in `morphology_candidates.csv`. A deeper version of the
   sacral reformat (sheets 12-24 and 24-36 mm in) was tried for these CTs and for read Castellvi II controls, and was
   dropped. At those depths the sheets still cut the vertebral bodies, not the transverse processes, and they fold
   where the surface bends at the lumbosacral angle.
11. **The missing labellers were retried.** TotalSegmentator had never segmented two CTs. For 0533 the bench read the
   CT while the release gzip was truncated (repaired on the grid on 2026-09-23). For 0921 a config read failed at
   start-up. Both were re-run with the same model and weights into a private folder, so the shared bench's file
   count does not change (`slurm/ctsp_ts_retry.sh`). They ran on a CPU node (`tools/ctsp_ts_runner.py`, job
   40429825) because every GPU was queued. All three labellers now count five on both CTs. TotalSegmentator's spine
   voxels land on the release's at 0.953 and 0.949. SPINEPS on 0665 is still missing. Its `--cpu` flag raises
   inside TPTBox on a CPU node (torch.cuda.mem_get_info on the cpu device, job 40429826). A GPU retry that changes
   the voxel grid (1 mm isotropic, then an in-plane crop: `slurm/ctsp_spineps_0665_regrid.sh`, job 40429884) was
   still queued when this folder was built. Its recount (job 40429827) updates the grid census, and this folder has
   to be rebuilt to include it. The release and TotalSegmentator both count 0665 as five.
12. **Reads whose readers counted differently are now queued.** The two readers' worksheet gives each read CT a count of
   non-rib-bearing vertebrae, sometimes as '6 (NA 4)' when they disagree. In 13 read CTs the readers disagree with
   each other or with the labellers' count. Seven of them are new to the queue at priority 4: 0008, 0021, 0033, 0049,
   0176, 0785 and 0875. The other six were already queued (0179, 0196, 0208, 0268, 0486 and 1053), and their entries
   now carry the worksheet count. 0176 is the sharpest. Its readers wrote 'S1 lumbarization' and counted 6 and 5, and the labellers
   count 5. On the sacral reformat, a body-shaped segment separated by a bright band sits at the top of the release
   sacrum, with five lumbar vertebrae above it. That looks like a transitional S1 the release keeps inside its sacrum
   label, where its 18 L6 spines give that segment id 25. If a reader finds it mobile, 0176 is an L6 the count
   missed. 0785 and 0875 are read sacralised with four lumbar vertebrae, and every labeller counts five. On 0875 the
   readers note hypoplastic ribs at T12, which the release's rib masks lack.

**Defects in the counting itself, found by looking and fixed before these numbers.**
- A rib is now borne by the vertebra nearest its **head**. Under the old rule, the vertebra nearest any part of the rib,
  a 12th rib that slopes past L1's transverse process went to L1 (0425).
- A rib cut by the FOV edge no longer sets the reference. In 1106 the lower ends of the 12th ribs enter the top of the
  volume beside L1.
- A counted body 1.6 times the median of its neighbours is refused as two vertebrae under one label. A release body
  that is big by volume but of ordinary height (0196, a Castellvi IIa L5 with broad transverse processes) is not.
- SPINEPS's id 80 is never a vertebra.
- TotalSegmentator rib classes are reduced to their largest component.

**TotalSegmentator's own ribs are not usable at the costovertebral joint.** In 0043 its right 12th rib is the same bone
as the release's, but its mask lacks the rib head. What it has lies nearest L1, so its count reads 4. 139 CTs move off 5
on TotalSegmentator's ribs alone. That is why all three body sets vote with the release's student-reviewed ribs, and
why TotalSegmentator's ribs are reported as a check. It also means **the rib evidence is not independent of the
release**. A 12th rib that neither TotalSegmentator nor the student reviewers segmented would make every labeller say
"T12 carries no rib". The MIPs of the nine spines in point 1 show no such rib. A radiologist confirming even two of
them would settle it.

**VERIDAH's calls are not truth here.** It calls T13 on 52 CTs, and none of those can be counted. It skips T12 in 54
of its ctd files (its way of encoding 11 thoracic vertebrae), and only 6 of those 54 have six rib-free vertebrae by the
release's own voxels. It named the rib-free first vertebra "T13" in 0552, which the rib convention does not allow.

**Corrections to the first pass.** The 0179 note gave the readers' worksheet count as "6 (NA 5)". The worksheet
entry for 0179 is "6 (NA 4)". "(NA 5)" belongs to 0176.

**Not known.**
- The thoracic count of any CTSP spine, because no FOV reaches T1. No CTSP row can be T13 or both_L6_T13.
- Whether 0931 and 1123 are true four-lumbar spines or sacralisations the reformat does not show. 0801 and 0349 look
  sacralised and 1000 looks unfused on the reformats, but none of that is a read.
- The Castellvi grade of any new row. No reader has seen them.
- Whether SPINEPS can segment 0665 at all (GPU retry job 40429884 was queued at build time).

## Calls per subtype and tier

One CT is one person in CTSpinoPelvic1K (patient key `ctsp:<release id>`, `tools/patient_keys.py`), so distinct patients equal rows. 'new' = rows the release's own names and reads never called.

| subtype | read | two-labeller | single-labeller | morphology-only | rows | distinct patients | new |
|---|---|---|---|---|---|---|---|
| L6 | 17 | 11 | 1 | 0 | 29 | 29 | 11 |
| castellvi_I_II | 4 | 0 | 0 | 0 | 4 | 4 | 0 |
| lumbar_rib | 0 | 9 | 5 | 0 | 14 | 14 | 0 |
| sacralised_L5_fused | 12 | 0 | 0 | 0 | 12 | 12 | 0 |
| unassigned | 0 | 5 | 0 | 0 | 5 | 5 | 2 |
| **all** | 33 | 25 | 6 | 0 | 64 | 64 | 13 |

## Denominators

| quantity | CTs |
|---|---|
| CTs in the release (manifest) | 802 |
| CTs censused | 802 |
| census failed | 0 |
| A (release) counts | 792 |
| B (SPINEPS bodies, release ribs) counts | 796 |
| check: SPINEPS bodies with TotalSegmentator ribs count | 798 |
| C (TotalSegmentator bodies, release ribs) counts | 777 |
| check: TotalSegmentator bodies with its own ribs count | 779 |
| SPINEPS has no output | 1 |
| A and B both count / agree | 791 / 775 |
| A and C both count / agree | 772 / 756 |
| all three count / all three agree | 771 / 752 |
| two or more labellers agree on some count (a countable junction) | 791 |
| VERIDAH calls T13 or both (never countable: no CTSP FOV reaches T1) | 52 |
| release label off its CT (release count withdrawn) | 3 |
| 'unassigned' four-lumbar-id spines resolved as labelling artefacts (not rows) | 1 |
| only TotalSegmentator's ribs move the count off 5 (rib-source note, not a candidate) | 139 |
| A and B both place a lowest rib-bearing vertebra | 795 |
| ... and put it on a different vertebra (moves the junction; queued) | 1 |
| A and B differ in the number of rib-bearing vertebrae in the FOV (finding 9) | 160 |
| morphology screens: Castellvi screen top 25 / type-I height pre-filter / either (candidates, not rows) | 25 / 214 / 218 |
| ... of those in either screen, already a registry row | 10 |
| read CTs whose two readers' counts differ, or differ from the labellers' count (queued) | 13 |

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

### Release count (rows) x SPINEPS count (columns)

| A \ B | 4 | 5 | 6 | no count |
|---|---|---|---|---|
| 4 | 9 | 1 | 0 | 0 |
| 5 | 5 | 746 | 2 | 1 |
| 6 | 0 | 8 | 20 | 0 |
| no count | 0 | 3 | 2 | 5 |

### Release count (rows) x TotalSegmentator bodies count (columns), both with the release ribs

| A \ C | 4 | 5 | 6 | 7 | 8 | no count |
|---|---|---|---|---|---|---|
| 4 | 8 | 2 | 0 | 0 | 0 | 0 |
| 5 | 6 | 740 | 1 | 0 | 0 | 7 |
| 6 | 0 | 4 | 8 | 2 | 1 | 13 |
| no count | 0 | 3 | 2 | 0 | 0 | 5 |

### The rib-source check: TotalSegmentator bodies with the release ribs (rows) x with its own ribs (columns)

| C \ C_ts | 3 | 4 | 5 | 6 | 7 | 8 | no count |
|---|---|---|---|---|---|---|---|
| 4 | 1 | 9 | 4 | 0 | 0 | 0 | 0 |
| 5 | 0 | 124 | 618 | 5 | 2 | 0 | 0 |
| 6 | 0 | 0 | 3 | 8 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| 8 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| no count | 0 | 2 | 0 | 0 | 0 | 0 | 23 |

### Release lumbar ids (rows) x the count two or more labellers agree on (columns)

| names \ consensus | 4 | 5 | 6 | no count |
|---|---|---|---|---|
| 4 | 9 | 3 | 0 | 1 |
| 5 | 2 | 751 | 11 | 7 |
| 6 | 0 | 4 | 11 | 3 |

VERIDAH's own call across the censused CTs: none 725, T13 52, L6 24, None 1.

## Release labels that do not sit on their CT

TotalSegmentator and SPINEPS were both run on the release CT. The share of TotalSegmentator's spine voxels that land on release spine voxels has median 0.94 (5th percentile 0.92, minimum 0.66, n=802). Below 0.80 the release's contours visibly cut through the vertebral bodies on the render (0487, 0527 and 1090 were looked at). The release count is withdrawn for these CTs, and it is a defect in the v11 release to fix at the source: 0487 (0.66), 0527 (0.69), 1090 (0.66).

## Morphology screens: candidates, not rows

CTSpinoPelvic1K carries two screens for the Castellvi grades a vertebra count cannot reach. `docs/castellvi_reread_queue.csv` is the top 25 of a learned ranking (`scripts/screen_missed_castellvi.py`; leave-one-out median rank, of 760, 4 for IIb, 25 for IIIa and 442 for IIIb against the 33 graded cases). `docs/castellvi_type1_queue.csv` is Castellvi's 19 mm height criterion applied to the released transverse processes. Its author measured it against an external prevalence (Hanhivaara et al., Castellvi I in about 19.7 % of adults) and found it calls about 1.7 times too many, because it tests one of the criterion's three conditions (height, not dysplastic or triangular shape). Neither is a grade, so neither makes a registry row, and the `morphology-only` tier is empty for CTSpinoPelvic1K. Both lists are in `morphology_candidates.csv`, with the registry row or queue priority each CT already has. The screen's top 25 are in the review queue (priority 7 when nothing else put them there), because a reader's grade is what would turn them into rows.

## Review queue

`review_queue/review_queue.csv` holds 72 CTs. Each has two renders. `<id>.jpg`: coronal bone MIP and mid-sagittal MIP, release labels then SPINEPS+VERIDAH, ribs dashed and coloured by the vertebra each labeller's geometry assigns them to. `<id>_ts.jpg`: TotalSegmentator bodies and ribs, a thin curved coronal slab through the transverse processes, and a thin curved mid-sagittal slab with the release names on the left and SPINEPS bodies counted up from the sacrum on the right. `review_queue/sacrum/<id>_sacrum.jpg` (`tools/ctsp_sacrum_look.py`): the anterior sacral surface unrolled as a curved reformat at three depths, for judging whether the sacrum carries an extra segment (finding 4). They exist for the four-lumbar spines, 0172, the reads queued for their readers' counts (finding 12) and the controls they are all judged against, and the `render_sacrum` column names them. The `looked` column is what Claude saw on the renders. It is not a read. Fill in `greg_verdict`.

| priority | meaning | CTs |
|---|---|---|
| 1-candidate | a count the release did not call | 13 |
| 2-unassigned | four lumbar ids with no read: anatomy or labelling? | 4 |
| 3-labellers-disagree | a registry row whose labellers disagree | 5 |
| 4-read-vs-labeller | a read row the labellers' count does not match, or whose two readers counted differently | 15 |
| 5-uncertain | re-read pending, a release label oddity (incl. a release label off its CT), or the rib source changes the count | 6 |
| 6-single-count | not a registry row: one labeller's count is 4 or 6 while the others say 5 or refuse | 13 |
| 7-morphology-screen | not a registry row: an unread CT the CTSpinoPelvic1K Castellvi screen ranks in its top 25 (a ranking for Castellvi I/II, not a grade) | 16 |

## Columns

- `n_thoracic_rib_bearing`: vertebrae bearing a whole rib **inside the FOV** (release ribs 1-13; lumbar ribs 60/61 and ribs cut by the FOV edge excluded). It is not a thoracic count, because no CTSP FOV reaches T1.
- `n_lumbar`: rib-free presacral vertebrae, the count two or more of A/B/C agree on. Blank when no two agree. The release's lumbar-id count is in `labeller_a`.
- `agree`: A's count equals B's count. Empty when either has none. TotalSegmentator's count is in `labeller_b`.
- `junction_tl_in_fov`: the release's lowest rib-bearing vertebra is established. A rib cut by the FOV edge does not establish it. `junction_ls_in_fov`: the release sacrum is in the FOV.
- `real_frames`: False for every row. CTSpinoPelvic1K is CT only, so these people may feed renders.
- Cross-collection duplicates: CTSpine1K's colonography subset holds CT-Colonography scans that are also CTSpinoPelvic1K records. The join is the manifest's spine series, which is not printed here. A CTSpine1K stream must drop those people or key them `ctsp:<release id>`.
