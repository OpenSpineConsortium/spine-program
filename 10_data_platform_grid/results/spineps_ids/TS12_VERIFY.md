# TS12 — adversarial check of the "2 L6 / 3 T13 / 7 normal" finding (F1, 2026-09-23)

The finding under test (render agent, ~16:30): the bench_ts SPINEPS masks `~/bench_ts/spineps/native/TS_<s>_seg-vert_msk.nii.gz`
carry spatially scrambled ids, "id 25 present" never meant L6, and by the VERIDAH ctd the twelve are L6 = s1089, s1178;
T13 = s0616, s1088, s1123; normal = the other seven (`SchwingNet/results/rare_class/ts12_ctd_subtypes.json`).

## Verdict

| claim | result |
|---|---|
| The native ids are not VerSe names | **Confirmed.** In all 12 masks the id set is exactly {1..25} (a raw enumeration of 25 instances). No mask is S-I monotonic (discordant-pair fraction 0.38–0.69; 0.5 = random). Only 0–4 of 24–25 ctd points land in the instance with that label, which is chance level. |
| Why "id 25 present" picked these 12 | A raw 1..N enumeration contains 25 exactly when there are ≥ 25 instances. That picked **whole-spine fields of view** (C1 + 23 presacral + a sacrum piece, or C1 + 24 presacral), not L6 spines. |
| `tools/rare_class_ts_fixids.py` (z-rank relabel) mapped every vertebra correctly | **Confirmed**, by a lookup that does not use z rank. For each ctd point I took the instance that physically contains it (the method of `tools/spineps_relabel_from_poi.py`). **280 of 280 vertebra points agree** with the fixids pair. In every staged, relabelled mask, each vertebra point reads its own label. Weaknesses and the sacrum label are covered in the "`rare_class_ts_fixids.py`" section below. |
| The ctd subtypes (VERIDAH naming) | **Not all confirmed.** 8 agree with an independent count. **s1178 is refuted.** It is not L6: it is a normal 24-presacral spine, and VERIDAH skipped T12. **s1088 and s1123** do have 25 presacral vertebrae, but their 20th vertebra has **no rib on either side**, so "T13" is VERIDAH's morphological name for a rib-less transitional vertebra. By the rib criterion these two are six-lumbar-type ("L6") spines. |

Corrected tally over the 12. Lumbosacral ends were read on slices: s1171's cannot be read (the CT stops inside it), and s0224 and s1380 carry the † caveat below.

- **25 presacral vertebrae (transitional): 4.** s0616 has 13 rib pairs (T13). s1089 has 12 rib pairs and 6 free lumbar vertebrae (L6). s1088 and s1123 have 12 rib pairs and a rib-less 20th vertebra with short, thoracic-type transverse processes.
- **24 presacral (normal count): 8.** The 7 ctd normals plus s1178.
- Under the rib criterion the count is **3 L6-pattern (s1089, s1088, s1123), 1 T13 (s0616), 8 normal**. Under VERIDAH's naming with s1178 corrected it is **1 L6, 3 T13, 8 normal**. Neither gives the "2 L6 / 3 T13 / 7 normal" now recorded.

## Per-case table

The independent count uses **no VERIDAH output**. It rests on three kinds of evidence:
- **SPINEPS instances as objects.** These come from the instance model, taken in S-I order from the top. Their names are shown, never used.
- **TotalSegmentator GT objects of the same CT.**
- **Ribs found in the CT itself.** These are bone (HU ≥ 200) outside every TS label except the ribs, and not in a SPINEPS instance, attached to the instance they reach through bone.

"#k" is the k-th instance from the top (#1 = C1). C/T/L is the count of cervical, rib-bearing and free lumbar-type vertebrae.

| case | ctd subtype | independent count C/T/L (presacral) | ribs: first … last rib-bearing instance (VERIDAH name of the last) | lumbosacral end | agree? |
|---|---|---|---|---|---|
| s0224 | none | 7/12/5 (24) | #8 … #19 (T12), bilateral | L5 free (disc). The S1 below it shows an S1–S2 remnant line on the mid-sagittal slice (†) | **yes** |
| s0616 | T13 | 7/**13**/5 (25) | #8 … **#20 (T13)**. Ribs meet #20's transverse processes on both sides (TP-level axial). CT rib components on #20 L+R, 883/920 voxels | L5 free, S1 fused | **yes** |
| s0790 | none | 7/12/5 (24) | #8 … #19 (T12) | L5 free, S1 fused | **yes** |
| s1088 | T13 | 7/12/**6** (25) | #8 … #19 (T12). **#20 ("T13") has no rib either side** at body or TP level; its TPs are short and thoracic-type, and #21's are long and lumbar | L5 free; FOV ends in the lower sacrum | **count yes (25), subtype no**: rib-less 20th vertebra |
| s1089 | L6 | 7/12/**6** (25) | #8 … #19 (T12) | **L6 free: disc above and below**, sacrum fused below it | **yes** |
| s1123 | T13 | 7/12/**6** (25) | #8 … #19 (T12). **#20 ("T13") has no articulating rib**; its TPs are short. A 202-voxel left nubbin at #20 is the same size as the non-rib fragments seen at L1/L2 in normal spines, so it is not called a rib | L5 free (thin disc below). The FOV stops about 10 mm into the sacrum | **count yes (25), subtype no**: rib-less 20th vertebra |
| s1124 | none | 7/12/5 (24) | #8 … #19 (T12) | L5 free, S1 fused | **yes** |
| s1171 | none | 7/12/5 (24 seen) | #8 … #19 (T12) | L5 has a disc below. The CT stops about 10 mm into the next bone, so "S1" versus a free 25th vertebra **cannot be read** | **yes (field-of-view-limited)** |
| s1178 | **L6** | 7/12/5 (24) | #8 … **#19, which VERIDAH calls "L1"**. The ctd has no T12. At body level (axial) the 12th ribs meet #19 on both sides, and #20 has no rib | Osteopenic and scoliotic; not read with confidence. This does not matter: an L6 needs 12 rib pairs plus 6 lumbar-type, and here at most 5 remain | **NO**: normal spine; VERIDAH L1..L6 are really T12, L1..L5 |
| s1304 | none | 7/12/5 (24) | #8 … #19 (T12) | L5 free (disc). The S1 has an S1–S2 remnant line, but on the coronal it widens into the alae, so it is sacral (†) | **yes** |
| s1350 | none | 7/12/5 (24) | #8 … #19 (T12) | L5 free, S1 fused | **yes** |
| s1380 | none | 7/12/5 (24) | #8 … #19 (T12) | L5 free on the slice (osteopenic, so HU disc contrast is weak). The S1 shows an S1–S2 remnant line (†) | **yes** |

(†) The lumbosacral ends were looked at on full-resolution mid-sagittal slices (`_ls.png`) for all twelve. For the three S1s with a remnant line, the alae were checked on the coronal for s1304 only. A lumbarised S1 in s0224 or s1380 is unlikely but not excluded by a single slice, and it would turn that case into a 25-presacral spine.

s1178 is a 57-year-old woman with severe thoracolumbar scoliosis. That explains its 428 mm C2-to-sacrum span and its ~20 mm lumbar centroid spacing. The misnaming sits exactly where the curve is.

## The relabel tool (`tools/rare_class_ts_fixids.py`)

Findings from reading the code, checked against the lookup:

- **It is correct on these 12.** Every vertebra point lies inside the instance the tool gave its name to (23/23 or 24/24 per case). Max |dz| over vertebra pairs is 4.8–10.7 mm, median 1.8–4.7 mm.
- **It uses z only, and its 25 mm tolerance cannot see a one-level shift in part of the spine.** Vertebral spacing is 15–20 mm in the cervical and upper thoracic spine and in s1178's scoliotic lumbar spine. In s1124, s1380, s1350 and s1123 some upper-thoracic instance centroids sit **nearer a neighbouring ctd point than their own**; rank order carried them. The assert would only fire where spacing exceeds 25 mm. The tool should also run the point-in-mask lookup and fail when the two disagree.
- **SAC (26).** In 6 of the 8 cases where the tool assigned 26, the sacrum ctd point lies in no instance, and the staged mask reads 0 there. In s1171 and s1178 the 26 instance does hold the point. The tool gave 26 to one of two kinds of object (|dz| 22–35 mm):
  - a 380–684-voxel fragment in **s0790, s1124, s1350**;
  - an S1-sized piece (15–20k voxels) sitting 24–29 mm above the point in **s0224, s1304, s1380**.

  Any sacrum box rendered from label 26 sits on that object.
- **Tool version drift.** 8 of the 12 `subtype_fix.json` files were written by the version before the sacrum-drop edit (they lack a `sacrum_poi_dropped` key). Their counts matched, so the current code gives the same mapping, and the lookup confirms it.
- **Its "subtype" is only the ctd's label set,** so it cannot catch a VERIDAH naming error (s1178).

## TotalSegmentator GT defects met on the way (relevant wherever TS GT is used as level truth)

TS has only 24 presacral names plus S1, and **every 25-presacral spine here is distorted to fit them**:

| case | how TS fit 25 presacral vertebrae into 24 names |
|---|---|
| s0616 | T9 + T10 merged into one "T9" object (18,184 voxels), with 12 rib names spread over 13 rib levels |
| s1088 | Four merged objects (T5+T6, T7/T8, T8/T9, T10/T11), and only 11 rib labels per side |
| s1089 | L3 + L4 merged into one "L3" object (41,774 voxels) |
| s1123 | The free L5 is labelled "S1", and the rib-less 20th vertebra is labelled "L1" |

Outside the transitional spines, s1350 has C4/C5/C6 labels lying in the thorax. s1178 has no L2–L5 labels, and its T6/T7 labels are out of order. Every TS rib mask also stops 10–20 mm short of the costovertebral joint.

## How the independent count was reached

Earlier passes were wrong and are kept on the grid only (`/rs/rs_grp_oschome/go2432/data/or_ready/spineps_ids/ts12_pass{1,2,3}_*`):

1. **Rib = TS rib label within 6 mm of a vertebra.** The 12th ribs were dropped as "floating" because the TS masks stop short, and 10 of 12 spines read 11/6.
2. **Rib attached to the vertebra nearest its medial end.** This was biased by one level at the lowest rib: the steep 12th rib passes beside L1's transverse process. It called three normal spines 13/4.
3. **Bone-path attachment**, growing through HU ≥ 150 bone from the rib's medial part to the first instance touched. This fixed the normals. It still inherits TS's rib labels, which cannot hold a 13th rib under its own name.
4. **(Final)** Rib components found in the CT independent of TS rib labels, plus axial slabs at each vertebra's transverse-process level. The calls in the table rest on the renders, not the numbers. HU disc profiles are reported in the json; they are weak in osteopenic spines (s1380, s1088) and were not used alone.

## Must change elsewhere (owned by other workflows; not edited here)

- `SchwingNet/results/rare_class/ts12_ctd_subtypes.json`:
  - **s1178 must not be "L6".** It is a normal count, with VERIDAH skipping T12.
  - s1088 and s1123 need the note "20th vertebra rib-less; T13 by VERIDAH, L6-pattern by ribs".
  - The finding sentence "only 2 of 12 are L6, 3 are T13, and 7 are normal" must change.
- `SchwingNet/results/rare_class/stratify.json`: `ts:s1178` must not remain L6. `transitional_subtypes.csv` still lists all 12 as L6, and `anomalous_inventory.json`'s TS section needs the same fix.
- **Rendered TS_s1178 frames** (rcts2 array 40424662, task 8), relabelled from the ctd:
  - Every name from #19 down is one level off. VERIDAH "L1..L6" are T12, L1..L5.
  - The anns carry subtype L6.
  - Relabel them or exclude them.
- **s1088/s1123 frames:** the names below T12 (VERIDAH "T13, L1..L5") depend on the convention chosen. Pick one and state it.
- Sacrum boxes, if any are drawn from label 26, are on fragments in the s0790, s1124 and s1350 renders.
- Any manuscript/NUMBERS sentence quoting the TS "2 L6 / 3 T13 / 7 normal".

## Re-run

`sbatch -D $HOME/spinesurg-ct-nnunet SchwingNet/slurm/ts12_verify.sh` (array 0-11, `tools/ts12_verify_ids.py`)
writes `/rs/rs_grp_oschome/go2432/data/or_ready/spineps_ids/ts12/TS_<s>_{verify.json,full.png,zoom.png,ls.png,axial.png,axial_tp.png}`.
Local copies are in `SchwingNet/results/spineps_ids/ts12/`. The decisive views are
`TS_s1178_axial.png`, `TS_s0616_axial_tp.png`, `TS_s1088_axial_tp.png`, `TS_s1123_axial_tp.png`, `TS_s1089_ls.png` and `TS_s1123_ls.png`.

What is not known: whether s1171's bone below L5 is a fused S1 or a free 25th vertebra (the field of view ends inside it), and
whether s1178's lowest vertebra is free (osteopenic, scoliotic), and whether the S1s of s0224 and s1380 (remnant S1–S2 line) are
lumbarised (alae not checked). No radiologist has read any of the twelve. Grid jobs: 40424776, 40424853, 40424880 (superseded passes), 40424902 (final).
