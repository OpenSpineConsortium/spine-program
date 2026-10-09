# Transitional registry -- TotalSegmentator stream (v2.0.1 + v3.0.0)

Built by `tools/ts_transitional_screen.py` (grid, one json + one render per CT: `slurm/ts_registry_screen.sh`, `ts_registry_rescreen.sh`, `ts_registry_rescreen_patch.sh`) and `tools/ts_transitional_registry.py` (this table, `slurm/ts_registry_aggregate.sh`). Every number below is computed by the second script from the first one's case jsons; `SUMMARY_numbers.json` holds the same numbers unrounded.

**Unit.** One distinct CT scan, keyed `ts:<v300 id>` (`tools/patient_keys.py`). TotalSegmentator ships no patient identifier (docs/PATIENT_IDENTITY_SPEC.md, ts row), so a person is a scan and the scan count is an upper bound on persons. v201 is the same scans under older masks: every v201 CT is joined to its v300 scan by the md5 of `ct.nii.gz`, or, where only the gzip stream differs, by identical shape + zooms + affine; v201 s1406..s1429 are 24 different v300 ids (alias 6) and are never matched by number.

**Labeller A** = SPINEPS + VERIDAH, read ONLY through the ctd POI names (monotonic S-I order asserted; a ctd whose points do not land on this CT's vertebrae is discarded). A SPINEPS mask id is never read as a level. **Labeller B** = the dataset's own TotalSegmentator masks read by GEOMETRY: rib-bearing bodies by rib-to-vertebra contact through bone (TS rib masks and rib-shaped CT bone, so a 13th rib TS has no name for is still seen), free bodies from the lowest rib-bearing one down to the sacrum. TotalSegmentator has no T13 class and v201 no L6 class, so its NAMES are never used to count. Rib convention (transitional_subtypes.md): L6 = six rib-free vertebrae between the last rib-bearing one and the sacrum; T13 = thirteen rib-bearing vertebrae.

**Field of view.** A lumbar count needs the lowest rib-bearing body with two whole bodies below it AND >= 45 mm of sacrum (>= 90 mm when the FOV cuts the sacroiliac joint -- TS_s1123's v300 `sacrum` label swallowed a free vertebra); a thoracic count needs the body above the highest rib (C7) in the field. A cut junction is `no_count`, never normal. Counts outside lumbar 4-6 / rib-bearing 11-13 / total 16-19 void labeller B for that CT.

**Tiers.** both labellers count a common junction and agree -> `two-labeller`; one counts -> `single-labeller`; they disagree -> subtype `unresolved`, tier `none`, review queue (the positive it was claimed for is in `notes` and `review_queue.csv`); nobody counts -> `no_count`, tier `none`. No row is `read` (no radiologist read exists for TotalSegmentator) and none is `morphology-only`: the two morphology signals failed the CTSpinoPelvic1K check below and call nothing. `castellvi` is empty on every row for the same reason. A positive in a child is never two-labeller (an unfused S1 looks free to both labellers).

## Denominators

| quantity | CTs |
|---|---:|
| v300 folders | 1,939 |
| duplicate v300 folders folded into their twin (alias 18: s1446=s1445, s2109=s2110=s2107, s2094~s2093) | 4 |
| **distinct CT scans screened (= rows)** | **1,935** |
| v201 folders screened (a second read of labeller B on the older masks) | 1,228 |
| v201 folders joined to their v300 scan (md5 1226, geometry 2); v201 scans with no v300 scan | 1,228; 0 |
| no vertebra in the TS masks (no spine in the field) | 162 |
| labeller A usable (SPINEPS ctd present and on this CT) | 1,630 |
| thoracolumbar junction in the field (after the guards) | 770 |
| lumbosacral junction in the field (after the guards) | 815 |
| both junctions in the field | 725 |
| labeller B made a lumbar count / a thoracic (from C7-T1) count | 685 / 185 |
| labeller B made any count / labeller A made any count | 701 / 733 |
| **CTs with a countable junction (either labeller)** | **748** |
| both labellers counted a common junction: agree / disagree | 612 / 74 |
| labeller B voided as implausible (a segmentation defect until a person says otherwise) | 50 |

SPINEPS coverage of the 1,935 scans (labeller A):

- 1,613: SPINEPS: mask from the four-rung ladder (or the linked v201 mask)
- 274: SPINEPS: no vertebra mask after the four-rung ladder; fifth attempt not tried (TS names < 4 vertebrae)
- 24: SPINEPS: mask only from the fifth (cropped) attempt
- 23: SPINEPS: mask only from the sixth attempt (cropped CT, cc3d-patched command)
- 1: SPINEPS: no vertebra mask after the four-rung ladder and the fifth (cropped) attempt and the sixth (cc3d-patched) attempt
  - what the fifth-attempt masks decided: no_count / none 10, none / two-labeller 6, none / single-labeller 3, unassigned / single-labeller 2, L6 / single-labeller 2, unresolved / none 1
  - what the sixth-attempt masks decided: no_count / none 13, none / two-labeller 7, none / single-labeller 2, unresolved / none 1
- ctd discarded because its points do not land on this CT's vertebrae: 10 (only 1/3 ctd points land on this CT's vertebrae: 3; only 0/1 ctd points land on this CT's vertebrae: 2; only 2/5 ctd points land on this CT's vertebrae: 1; only 1/4 ctd points land on this CT's vertebrae: 2; only 0/6 ctd points land on this CT's vertebrae: 1; only 2/6 ctd points land on this CT's vertebrae: 1)

The scans with fewer than four TS vertebrae cannot be counted by either labeller (a lumbar count needs the last rib-bearing body, the free bodies and the sacrum; a thoracic count needs C7 to below the last rib), so the fifth and sixth SPINEPS attempts were spent only where a count was possible. The sixth attempt (`benchmark/spineps_cc3d_patched.py`, `slurm/ts_spineps_patch.sh`) is stock SPINEPS with one TPTBox crash removed: cc3d refuses to count a label map with fewer voxels than its largest label; the patch pads that array with zeros past its last index, which changes no label's count (a selftest against np.bincount runs before any CT). It ran on CPU (`--cpu`, which also needs TPTBox's GPU-busy wait disarmed on the cpu device) because the GPU partitions were held by the Figure 6 work.

## Calls (rows.csv): one row per CT scan; persons <= scans

| subtype | CTs | two-labeller | single-labeller, B only | single-labeller, A only | single-labeller, a child both labellers agree on | of these paediatric | both junctions in the field |
|---|---:|---:|---:|---:|---:|---:|---:|
| L6 | 22 | 14 | 4 | 3 | 1 | 6 | 22 |
| T13 | 4 | 3 | 0 | 1 | 0 | 0 | 2 |
| both_L6_T13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| lumbar_rib | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| unassigned | 26 | 8 | 2 | 14 | 2 | 12 | 21 |
| sacralised_L5_fused | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| castellvi_I_II | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| none | 622 | 584 | 9 | 29 | 0 | 35 | 607 |
| unresolved | 74 | 0 | 0 | 0 | 0 | 8 | 72 |
| no_count | 1,187 | 0 | 0 | 0 | 0 | 223 | 1 |

`unassigned` = 13 four-lumbar counts (a fused L5 inside the TS sacrum label, or a true four-lumbar spine; no read separates them here; `fused_mask_representation` = merged-into-sacrum) and 13 with 11 rib-bearing bodies (23 presacral, or a 12th rib neither mask holds).

`unresolved` (the two labellers disagree; no subtype until a person reads it), by the positive one of them claimed: L6 39, unassigned 31, T13 3, lumbar_rib 1.
In 13 of them both labellers count the same number of thoracolumbar bodies and disagree only on which one carries the last rib (VERIDAH names by shape, B counts rib contact): a naming disagreement, not a count disagreement.

**Positive rows:** 52 (single-labeller 27, two-labeller 25). **both_L6_T13:** looked for on every CT with both junctions counted; found 0. `sacralised_L5_fused` and `castellvi_I_II` need a Castellvi read, which no TotalSegmentator scan has: none is called, and a fused L5 can only surface here as a four-lumbar `unassigned` count.

**Lumbar-rib / rudimentary-rib candidates** (`lumbar_rib_candidates.csv`, notes only, no call): 39 CTs whose lowest rib is < 40 mm, 87 whose first free body carries 15-40 mm of rib-shaped bone the CT holds outside every TS label. On CTSpinoPelvic1K the short-lowest-rib signal marked 5 of 16 lumbar-rib spines and 26 of 746 ordinary ones, so neither is a call. `lumbar_rib` rows: 0 (13 rib-bearing over four free).

### Where labeller B's sixth free body comes from

Read off TotalSegmentator's own names for B's objects (never used to count). On the curated v300 masks B's rib-to-vertebra attachment gives a T10-T12 body the rib TotalSegmentator numbers the same on 6219/6363 (98 %) of attached ribs, so a free body TS names T12 is one TS's own annotation gives no rib. The CTSpinoPelvic1K columns are the same screen on TotalSegmentator-tool PREDICTIONS, which carry no L6 class, scored against the release truth.

| origin of the sixth free body | TS: L6 two-labeller | TS: L6 single-labeller | TS: unresolved | CTSP: truth L6 (A also L6) | CTSP: truth not L6 (A also L6) |
|---|---:|---:|---:|---:|---:|
| the dataset's own masks name it vertebrae_L6 (TS annotation also counts six below T12) | 9 | 0 | 6 | 0 (0) | 0 (0) |
| TS names it T12 and gives it no rib (11 TS rib pairs): an L6 by the rib convention, a rib-less T12 by TS's count -- 24 or 25 presacral depending on the thoracic count | 3 | 4 | 13 | 0 (0) | 0 (0) |
| TS names it T12, but TS's rib_12 sits on the body above it: TS's rib and vertebra numbering disagree by one | 1 | 0 | 2 | 0 (0) | 2 (0) |
| one TS label holds two bodies (B split it by height/disc) | 1 | 1 | 1 | 5 (4) | 12 (4) |
| one TS label is two separate bone pieces, each counted as a body (e.g. L3 and L3') | 0 | 0 | 0 | 5 (2) | 4 (0) |
| a free body inside the top of TS's sacrum label (or TS's S1 is free) | 0 | 0 | 0 | 0 (0) | 0 (0) |
| TS names five lumbar and none of the above explains the sixth | 0 | 0 | 0 | 0 (0) | 0 (0) |

A reader would weigh these differently: TS's own annotators also counted six below T12 (strongest); TS's annotation calls the body a rib-less T12 (the rib convention says L6, but with C7 out of the field the spine may hold an ordinary 24 presacral bodies); TS's rib and vertebra numbering disagree; a TS label B split. On CTSpinoPelvic1K, where the TS-tool predictions have no L6 class, 26 of 28 B L6 calls come from a split TS label, right and wrong alike, so a split is not evidence either way.

**Children.** Positive or claimed-positive among countable CTs: paediatric 26/61 (43 %), adult 100/682 (15 %). An unfused S1 (or S1-S2) is a free body to both labellers, so a child's positive is never two-labeller and always goes to review.

## Refusals (`no_count` rows) by reason

| reason | CTs |
|---|---:|
| thoracolumbar reference not in FOV | 988 |
| no vertebra in the TS masks | 162 |
| sacrum reference not in FOV | 15 |
| only 1 whole body below the lowest rib-bearing one | 13 |
| sacrum cut by the FOV at the sacroiliac joint with # mm of sacrum label | 6 |
| implausible count | 3 |

## The five TotalSegmentator calls named before this screen (SPINEPS ctd), confirmed or refuted

TS12_VERIFY (`SchwingNet/results/spineps_ids/TS12_VERIFY.md`) is a third, independent count on renders (SPINEPS instances as objects, CT rib components; no VERIDAH name, no radiologist). It is quoted, not used by any rule.

| CT | ctd claim | labeller A (VERIDAH names) | labeller B (geometry) | TS12_VERIFY | registry row | verdict on the claim |
|---|---|---|---|---|---|---|
| TS_s1089 | L6 | L6 (lumbar L6, rib-bearing 12) | L6 (lumbar L6, rib-bearing 12) | 7/12/6 L6 (disc above and below the sixth) | L6 / two-labeller | **confirmed** by B's count (12 rib-bearing / 6 free) |
| TS_s1178 | L6 | L6 (lumbar L6, rib-bearing 11) | none (lumbar 5, rib-bearing 12) | 7/12/5 normal count; VERIDAH skipped T12 (its L1..L6 are T12, L1..L5) | unresolved / none | **refuted**: B counts 5 free below 12 rib-bearing |
| TS_s0616 | T13 | T13 (lumbar 5, rib-bearing T13) | T13 (lumbar 5, rib-bearing T13) | 7/13/5 T13 (ribs meet the 20th vertebra's transverse processes on both sides) | T13 / two-labeller | **confirmed** by B's count (13 rib-bearing / 5 free) |
| TS_s1088 | T13 | T13 (lumbar 5, rib-bearing T13) | L6 (lumbar L6, rib-bearing 12) | 7/12/6: rib-less 20th vertebra, VERIDAH T13, L6 pattern by ribs | unresolved / none | **refuted** at the thoracolumbar junction: B counts 12 rib-bearing and 6 free (an L6 by the rib convention) |
| TS_s1123 | T13 | T13 (lumbar -, rib-bearing T13) | none (lumbar -, rib-bearing 12) | 7/12/6: rib-less 20th vertebra, VERIDAH T13, L6 pattern by ribs; the FOV ends ~10 mm into the sacrum | unresolved / none | **refuted** at the thoracolumbar junction: B counts 12 rib-bearing |

## Outside check: both labellers on CTSpinoPelvic1K against its release truth

The same screen run on 800 CTSpinoPelvic1K CTs (TotalSegmentator-tool predictions for B, SPINEPS on the release CT for A) and scored against the release labels (L6 = id 25; four = four lumbar ids) and the two-reader Castellvi consensus. CTSpinoPelvic1K is abdominopelvic, so this checks the lumbosacral count only, and B there reads TotalSegmentator PREDICTIONS, not the curated TotalSegmentator dataset masks it reads above.

| call | truth positives | A: right / called | B: right / called | A and B: right / called | both read 5 on a truth positive |
|---|---:|---:|---:|---:|---:|
| L6 | 18 | 10/24 (PPV 0.42) | 10/28 (PPV 0.36) | 6/10 (PPV 0.60) | 2 |
| four | 13 | 12/44 (PPV 0.27) | 5/17 (PPV 0.29) | 5/12 (PPV 0.42) | 1 |

So a two-labeller L6 here is right 6 of 10 times and finds 6 of 18 truth L6 spines; ordinary spines read 5 by both: 694 of 769. **A two-labeller TotalSegmentator positive is a candidate for a read, not a truth label**, which is why every positive row is in the review queue.

Castellvi morphology (lowest-lumbar transverse process within 2 mm of the sacrum) fires on 279/748 (37 %) reader-ordinary spines and on 13/31 (42 %) spines the two readers graded II-IV: it does not separate them, so it calls nothing.

## TotalSegmentator v3.0.0's own `vertebrae_L6` label

v300 ships a `vertebrae_L6` mask (>= 1,000 voxels) in 23 scans. TotalSegmentator has no T13 class, so the label means 25 presacral bodies, not six lumbar by the rib convention. Where those scans landed: L6 / two-labeller 9, unresolved / none 6, none / two-labeller 3, no_count / none 2, L6 / single-labeller 1, T13 / two-labeller 1, T13 / single-labeller 1. Those read `none` by both labellers are in the review queue.

## Labeller B on the two mask releases of the same CT

Same subtype from the v201 and the v300 masks: 1153/1181 (98 %). Disagreements: v300 B L6 / v201 B none 5, v300 B none / v201 B no_count 5, v300 B none / v201 B T13 4, v300 B unassigned / v201 B none 4, v300 B L6 / v201 B no_count 2, v300 B unassigned / v201 B lumbar_rib 2, v300 B T13 / v201 B no_count 2, v300 B unassigned / v201 B L6 1, v300 B unassigned / v201 B no_count 1, v300 B no_count / v201 B T13 1, v300 B L6 / v201 B both_L6_T13 1.

## Review queue (`review_queue.csv`, renders in `review_queue/`)

137 CTs. Each render is the screen's figure (coronal MIP of the spine slab, sagittal slab, coronal zoom from the lowest ribs to the sacrum) with BOTH labellings drawn: cyan = B's bodies (r1.. rib-bearing up from the lowest, f1.. free up from the sacrum), grey = TotalSegmentator's names, magenta = A's VERIDAH ctd names, green = TS ribs, orange/red squares = rib bone found in the CT itself. The banner is the registry's decision; the title under it is the screen's provisional call before the registry's guards. File names are `p<priority>_<case>_<subtype>[-<claim>].jpg`; priority 1 = concordant positive, 2 = discordant, TS names L6 on a normal count, or a T13 on a short or one-sided 13th rib, 3 = B-only positive, 4 = B implausible with A positive, 5 = A-only positive, 6 = A names a variant B cannot count.

| why | CTs |
|---|---:|
| discordant | 74 |
| concordant positive (on CTSpinoPelvic1K concordant L6 is right 6 of 10 times) | 28 |
| paediatric positive | 26 |
| single-labeller positive (A only) | 18 |
| B implausible count, A positive | 18 |
| A names a variant B does not count | 11 |
| single-labeller positive (B only) | 6 |
| T13 on a short or one-sided 13th rib | 3 |
| TS v300 names L6, count says normal | 3 |

## Renders looked at before this was reported

Twenty review renders were opened and read by eye on 2026-09-24 before this was reported (Claude, not a radiologist): ten of the fourteen two-labeller L6 rows, all three two-labeller T13 rows, two two-labeller four-lumbar rows, and the five calls named from the SPINEPS ctd before this screen, plus two unresolved rows. What each render shows is written below as seen; it changes no row. Where the text names a TS label it is TotalSegmentator's own name for the body, read off the render's grey labels and the case json.

| CT | registry row | what the render shows |
|---|---|---|
| TS_s1089 | L6 / two-labeller | 12 rib pairs down to TS T12, then six free bodies (f1-f6) above an ordinary sacrum. TS's own masks name an L6; VERIDAH names L1-L6. C2 to the sacrum in the field. Looks like a true six-free-lumbar spine (TS12_VERIFY agrees). |
| TS_s0059 | L6 / two-labeller | Same pattern from C7 down: rib_12 on TS T12, six free bodies, TS names L6, VERIDAH L1-L6. Credible L6. |
| TS_s0446 | L6 / two-labeller | Same pattern from C7 down, TS names L6, VERIDAH L1-L6. Credible L6. |
| TS_s0733 | L6 / two-labeller | Same pattern from C7 down, TS names L6, VERIDAH L1-L6. Credible L6. |
| TS_s0077 | L6 / two-labeller | Field starts at T9 (T1 not seen). rib_12 on TS T12, six free bodies, TS names L6, VERIDAH L1-L6; the v201 masks of the same CT read five. Consistent L6, but nothing in the field fixes the thoracic count. |
| TS_s0049 | L6 / two-labeller | TS's L3 label covers two bodies (1.9x its neighbours' height) and B split it; six free bodies; VERIDAH independently names L1-L6. Consistent L6 whose sixth body TS merged into one label. The split is the weak link: on CTSpinoPelvic1K the split rule was right and wrong about equally often. |
| TS_s0158 | L6 / two-labeller | Field starts at T10. TS's rib_12 attaches to the body TS names T11 and TS's T12 has no rib, so TS's rib numbering and vertebra naming disagree by one. Six free bodies. If TS's rib count is right this is 12 + 6 (L6); if its vertebra names are right the spine is ordinary with the 12th rib one level high. Not decidable without T1. |
| TS_s0477 | L6 / two-labeller | Rods and pedicle screws span the thoracolumbar junction. TS T11 carries rib 11, TS T12 carries no rib (none in the TS masks), VERIDAH jumps from T11 to L1. 11 rib-bearing counted from the top plus 6 free = an ordinary 24 presacral bodies. The two labellers agree because both see the same missing 12th rib under hardware: the agreement is not independent here. Most likely an ordinary spine; needs a reader. |
| TS_s0683 | L6 / two-labeller | Field starts at T9. TS T11 carries rib 11, TS T12 rib-less, six free bodies; VERIDAH L1-L6. L6 by the rib convention; with T1 out of the field it may equally be an ordinary spine with a rib-less T12. |
| TS_s1974 | L6 / two-labeller | Poor image (arms down, lines and leads). 11 rib-bearing bodies counted from C7 plus 6 free = 24 presacral: an ordinary count with a rib-less T12, L6 by the rib convention only (the row's note says so). |
| TS_s0616 | T13 / two-labeller | 13 rib pairs, the 13th pair 69-71 mm on both sides and meeting the 20th body; five free bodies; C2 to the sacrum in the field. Credible T13 (TS12_VERIFY agrees). |
| TS_s1023 | T13 / two-labeller | Chest CT ending at L2-L3, no sacrum. The 13th rib-bearing body carries one 39 mm rib on the right only. T13 by rib contact, an L1 with a rudimentary rib by VerSe's 38 mm rule; the lumbar count is impossible here. Weak T13. |
| TS_s1329 | T13 / two-labeller | Chest CT ending at L3-L4, no sacrum. The 13th body carries one 36 mm rib on the left only. By VerSe's 38 mm rule this is a lumbar vertebra with a rudimentary rib, not a T13. Weak T13. |
| TS_s0436 | unassigned / two-labeller | 12 rib pairs (short 12th ribs), four free bodies, then a large sacrum; TS's own masks also name only L1-L4. Four-lumbar by count; sacralised L5 inside the sacrum label versus a true four-lumbar spine is open (no Castellvi read). |
| TS_s0171 | unassigned / two-labeller | 12 rib pairs, four free bodies above the sacrum, TS names L1-L4; CT rib-shaped bone flagged beside L4's transverse processes. Four-lumbar by count; sacralisation versus four-lumbar open. |
| TS_s1178 | unresolved / none | Scoliosis. B: 12 rib pairs and 5 free bodies. VERIDAH jumps from T11 to L1 (skips T12), so its L6 is B's L5: the ctd's L6 is a VERIDAH naming error (TS12_VERIFY said the same). Registry row: unresolved. |
| TS_s1088 | unresolved / none | TS's T1 label holds two bodies, so TS's thoracic names run one short; 12 rib pairs; the 20th body is rib-less; six free bodies. L6 by the rib convention (TS12_VERIFY: 7/12/6); VERIDAH names the rib-less 20th body T13. Registry row: unresolved. |
| TS_s1123 | unresolved / none | 12 rib pairs; the 20th body carries 28 mm of rib-shaped bone on the left that is not a TS rib, the likely reason VERIDAH names it T13. The field ends in the upper sacrum and TS's sacrum label holds a free body, so the lumbosacral count is cut (TS12_VERIFY read six free there). T13 refuted by the rib count; L6 not countable by rule. |
| TS_s0016 | unresolved / none | Field starts at T10. TS names six lumbar (L1-L6) below the lowest rib-bearing body; VERIDAH calls the first free body a rib-less T12 and counts five. With T1 out of the field nobody can count the total. Registry row: unresolved. |
| TS_s0086 | unresolved / none | C7 to the sacrum in the field, 12 rib pairs; the 20th body has a small rib-like fragment on one side that B does not attach; VERIDAH names it T13, B counts six free; TS's rib_12 sits on the body TS names T11. T13 with a rudimentary rib versus L6: a reader's call. Registry row: unresolved. |

Of the ten two-labeller L6 renders looked at: five look like true six-free spines on which TotalSegmentator's own annotators also named an L6 (s1089, s0059, s0446, s0733, s0077); one rests on a TS label B split (s0049); four rest on a TS T12 without a rib or on TS rib/vertebra numbering that disagree (s0158, s0477, s0683, s1974), and two of those count 11 rib-bearing from the top, an ordinary 24 presacral bodies. Of the three two-labeller T13: one credible (s0616), two resting on a single short 13th rib with no sacrum in the field (s1023, s1329). The TS-names-L6 kind is the one to trust first; the rib-less-T12 kind is L6 only by the rib convention and needs the thoracic count.

## What is not known

- No TotalSegmentator call has a radiologist read. The CTSpinoPelvic1K check says a two-labeller L6 is wrong about four times in ten there; nothing measures that rate on TotalSegmentator's own curated masks.
- Whether a four-lumbar count is a fused L5 inside the TS sacrum label or a true four-lumbar spine.
- Whether an 11-rib-bearing count is a rib-less T12, a 12th rib neither mask holds, or 23 presacral bodies.
- The thoracic count is available only where C7 is in the field (185 of 1,935 CTs), so T13 is not excluded on any other CT; its `none` means the lumbosacral count is ordinary.
- Whether two TotalSegmentator scans are one person: nothing on disk says (no identifier). Whether a TotalSegmentator scan is also a scan of another collection: no such alias is declared in docs/PATIENT_IDENTITY_SPEC.md or docs/DATA_ACCOUNTING.md section 3, and none is tested here.

