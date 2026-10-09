# Transitional registry -- other_ct stream (every CT on the grid that no other stream covers)

Built by `tools/other_ct_screen.py` (grid: `slurm/other_ct_seg.sh` for SPINEPS + TotalSegmentator, `slurm/other_ct_cpu.sh` for cases / analyse / aggregate / render), `tools/other_ct_dedupe.py` (CTSpine1K <-> CTSpinoPelvic1K <-> VerSe crosswalk, header refusals, Dataset815), `tools/other_ct_look.py` (closer renders for a person to count on) and `tools/other_ct_summary.py` (the generated tables below and `review_queue/index.csv`). Grid outputs: `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/`; this folder is a byte-for-byte copy of its aggregate (08:47 EDT, 2026-09-24) plus the review-queue and look renders.

**Unit.** One CT scan per row, keyed by `tools/patient_keys.py` (`<source>:<case>`). CTSpine1K persons are the TCIA PatientID (COLONOG) or the sub-collection case; RibFrac and RSNA persons are the case / study (no patient field is shipped); C-ArmLSpine "case" is an acquisition, not a proven person (day-grouped folds). Where a scan is another stream's person it is an ALIAS and gets no row here (`alias_rows.csv`).

**Labeller A** = SPINEPS + VERIDAH, read ONLY through the ctd POI names (monotonic cranio-caudal order asserted, > 5 mm inversion refuses the labeller; the mask beside the ctd goes through `tools/spineps_ids.check_ids`). A SPINEPS mask id is never read as a level. **Labeller B** = TotalSegmentator (fresh inference, or the existing v2 predictions on the CTSpinoPelvic1K bench) read by GEOMETRY: one object per vertebra label, rib-bearing bodies by rib-to-vertebra contact through bone, free bodies from the lowest rib-bearing one to the sacrum. No TotalSegmentator vertebra name is used to count (it has no T13 class and squeezes a 25th body into 24 names); its rib NUMBERS are used only at the bottom of the cage to order and pair ribs 10-12.

**A transitional call needs a count, and a count needs both references in the field.** Lumbosacral (L6 / four-lumbar): the last rib-bearing vertebra AND the sacrum. Thoracolumbar (T13 / lumbar rib): the cage counted from T1 (a cervical or T1 name above the highest rib, two free bodies below the lowest). A cut field is `no_count`, never normal; a reference sitting on the field edge is refused (the reference-at-edge and sacrum-at-edge guards, added 07:39 and applied to every case, `cases/stale.csv`). A VERIDAH L6/T13 name with no count in the field stays at tier `morphology-only` (an appearance call). Rib convention (`../../rare_class/transitional_subtypes.md`): L6 = six rib-free bodies between the last rib-bearing vertebra and the sacrum; T13 = thirteen rib-bearing bodies counted from T1, with five free below (four free = a rib on L1, `lumbar_rib`).

**Tiers.** `read` = a release expert list names it (CTSpine1K README); `two-labeller` = A and B count a common junction and agree; `single-labeller` = one counts; `morphology-only` = appearance with no count. Discordant counts stay `unassigned` with no tier and go to the review queue.

## Checkpoint (10:40 EDT, 2026-09-24) and what this pass did

The screen was complete on the grid at 08:47: every case in `cases/all.csv` has an analysis json (the 734 cases in `cases/stale.csv` were re-analysed after the 07:39 guard change, jobs `oct_anH` 40436435, `oct_anI` 40436621), every review-list case was rendered (`oct_rend` 40436437, 232 MIPs) and the aggregate ran (`oct_agg` 40436622). What was missing was the local mirror (rows, evidence, 232 MIPs, 23 look renders), this file, and a check of the find sweep against what the streams cover (`find/tally.txt`, job 40436865). Nothing was re-screened and no call changed in this pass.

**The acquisition-space review (`SchwingNet/lit/acquisition_space_review_2026-09-24.pdf`) changes nothing in this stream.** Its claims (a fluoroscopy accuracy plateau as sampling-density saturation of the C-arm acquisition space rather than a sample-count limit; coverage / normalised-entropy metrics over positioner angles, SID and patient position; pairwise domain adaptation; anchoring against level-jumping; patient-specific N = 1 pipelines) bear on how the CTs this stream names are RENDERED and on how the fluoro models are trained and scored. No row, count, tier or refusal here depends on any of them; the registry carries no pose. The two places where the review touches this stream's downstream use are recorded in the section "The acquisition-space review and this stream" below; nothing was requeued.

## Denominators

| source | CTs on disk | alias of another stream | screened (rows) | persons | A run | B run | TL countable | LS countable | no count | analysis pending / error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| carmlspine | 149 | 0 | 149 | 149 | 149 | 149 | 0 | 6 | 140 | 0 |
| ctspine1k | 1005 | 782 | 223 | 223 | 216 | 220 | 93 | 138 | 57 | 0 |
| deepfluoro | 6 | 0 | 6 | 6 | 6 | 6 | 0 | 0 | 6 | 0 |
| deepfluoro_vendor | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| geneva | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 0 |
| ljubljana | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| ribfrac | 660 | 0 | 660 | 660 | 655 | 660 | 626 | 9 | 34 | 0 |
| rsna_cspine | 2022 | 0 | 2022 | 2022 | 0 | 0 | 0 | 0 | 2022 | 0 |
| spinesac | 3 | 0 | 3 | 3 | 2 | 3 | 0 | 0 | 3 | 0 |
| **all** | 3848 | 782 | 3066 | 3066 | 1029 | 1039 | 719 | 153 | 2265 | 0 |

- **CTSpine1K, 1,005 volumes on disk (HF mirror, all of it).** 782 COLONOG volumes are CTSpinoPelvic1K persons (TCIA PatientID tail = the CTSpinoPelvic1K manifest token, `crosswalk_report.json`: 784 COLONOG, 782 in CTSP, 2 not) and belong to the ctsp stream; the 223 screened here are MSD-T10 150, COVID-19 40, HNSCC-3DCT-RT 31, COLONOG 2. HNSCC is head-and-neck (31/31 no count); COVID-19 is chest (26 none, 12 no count, 2 unassigned).
- **RibFrac, 660 chest CTs** (train 420 + val 80 + test 160, every image the archives hold). 626 have the cage countable from T1; only 9 reach the sacrum, so a RibFrac lumbosacral count is the exception.
- **RSNA 2022 cervical-spine, 2,022 studies**, refused from the DICOM header census (`rsna/rsna_headers.jsonl`): the longest study is 334 mm craniocaudal, below the 350 mm a scan starting at the skull base needs to reach the thoracolumbar junction (adult cervical ~120 mm + thoracic ~280 mm). None was segmented; none can hold a junction.
- **Real-frame CT sets**: C-ArmLSpine 149 lumbar CBCTs (real intraop frames, TEST only), DeepFluoro 6 cadaveric pelvis CTs (no rib cage in the field, no count), Geneva hip phantom and SpineSAC sawbones (phantoms, not persons), the DeepFluoro vendor sawbones pelvis (phantom), the Ljubljana specimen (five isolated lumbar vertebrae, no junction).
- **Dataset815 ("the L6 set", 1,176 cases)** is not a new collection: 802 CTSpinoPelvic1K + 374 VerSeFusion persons, 0 persons outside those two streams (`d815_summary.json`). Its manifest flags (L6 62, T13 4; 68 / 6 after the 2026-09-23 repair) are a second reading for the ctsp and verse streams, set beside their rows in the cross-reference below. The repair was not written into the manifest because the corpus does not fully decompress.

## Calls (rows.csv)

| source | L6 | T13 | both_L6_T13 | sacralised_L5_fused | castellvi_I_II | lumbar_rib | unassigned | none | no_count |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| carmlspine | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 140 |
| ctspine1k | 3 | 0 | 0 | 2 | 0 | 0 | 15 | 146 | 57 |
| deepfluoro | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| deepfluoro_vendor | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| geneva | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| ljubljana | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| ribfrac | 1 | 4 | 0 | 0 | 0 | 0 | 30 | 591 | 34 |
| rsna_cspine | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2022 |
| spinesac | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

| subtype | tier | source | cases | real frames (TEST only) |
|---|---|---|---:|---:|
| L6 | morphology-only | carmlspine | 3 | 3 |
| L6 | morphology-only | ribfrac | 1 | 0 |
| L6 | read | ctspine1k | 1 | 0 |
| L6 | two-labeller | ctspine1k | 2 | 0 |
| T13 | single-labeller | ribfrac | 4 | 0 |
| sacralised_L5_fused | read | ctspine1k | 2 | 0 |
| unassigned | - | ctspine1k | 15 | 0 |
| unassigned | - | ribfrac | 29 | 0 |
| unassigned | single-labeller | carmlspine | 1 | 1 |
| unassigned | single-labeller | ribfrac | 1 | 0 |

Modifiers: four_lumbar {'ctspine1k': 2}; lumbar_rib 0. **both_L6_T13:** looked for on the 73 CTs with both junctions in the field (ctspine1k 65, ribfrac 8) and on every labeller string; no CT where either labeller counts thirteen rib-bearing AND six free bodies. Castellvi grades: none (no read gives one; the two CTSpine1K sacralisations are release-named only).

### The thirteen positive rows, one by one (rendered and looked at; `looks/`, `looked.json`)

Every positive was rendered at the CT's own resolution (sagittal slab with VERIDAH names and TotalSegmentator objects; posterior coronal slab with the TS ribs; the same slab bone-only) and looked at. Five were looked at again in this pass (liver_119, liver_106, liver_83, RibFrac101, RibFrac482); the notes below held on every one.

**L6, ctspine1k, MSD-T10 (3).** `liver_119` and `liver_95` (two-labeller): eleven rib pairs on VERIDAH T1-T11 (TotalSegmentator's rib 7 is fragments lying on other ribs, so its L1-L12 labels are twelve names on eleven ribs), then six rib-free bodies to the sacrum: L6 by the rib convention, 24 presacral if the top is C5-C7 as named. The CTSpine1K annotation names the rib-less body T12 (12 + 5). These are the TotalSegmentator s1088/s1123 pattern (a rib-less 20th vertebra), an L6 under the project's convention and not a supernumerary segment. B's count in both is built from broken objects (a spurious object between T6 and T7, a merged L3+L4 split back by height) that happen to sum to the same answer; A's is clean. `liver_106` (read): the CTSpine1K README lists it under "Sacral Lumbarization" and its annotation labels 19 bodies C7-L6; VERIDAH names 18 (C7-L5) and both labellers put the 19th in the sacrum (TotalSegmentator's S1 object is a separate, lumbar-shaped body on the render). B's "L6" is a T11/T12 merge signature, not the body it missed. The row stands on the release read, and it is the one CTSpine1K L6 the labellers do NOT reproduce.

**sacralised_L5_fused, ctspine1k, MSD-T10 (2, tier read, four_lumbar).** `liver_83` and `liver_93`: twelve rib pairs (on `liver_83` the 12th are ~3 cm stubs), four rib-free bodies and a tall sacral block; the README lists both under "Lumbar Sacralization" and the annotation carries four lumbar ids and no sacrum id for the fused body (`fused_mask_representation` = unlabelled). A counts four lumbar on both; B says normal on both because a TotalSegmentator label split into two objects (T11/T12 on `liver_83`, L1 on `liver_93`) gave it a fifth body. If `liver_83`'s stubs were read as lumbar ribs (38 mm rule) its count would be 11 + 5.

**T13, ribfrac (4, single-labeller).** `RibFrac101` (the strongest): C5-C7 rib-free, thirteen regularly spaced rib-bearing bodies, the 13th with a long rib on one side and a ~4-5 cm rib on the other; TotalSegmentator's objects 8-10 span VERIDAH's T5-T8 (one vertebra missed), which is why B counts twelve and stays `unresolved`. `RibFrac93`: thirteen rib levels, the 13th with one ~5 cm rib and a process on the other side; TS misses one body near T6-T7 and splits T11/T12. `RibFrac322` and `RibFrac539`: twelve long pairs and ~3-4 cm stubs on both sides of a 13th body, which B leaves rib-free: T13 by the rib count, a lumbar rib by the VerSe 38 mm rule. All four scans end at L2-L3 with the sacrum out of the field, so 25 presacral (T13) versus 24 (a rib on L1) is open on all four; the subtype T13 here means "thirteen rib-bearing bodies counted from C7", and `review_list.jsonl` carries them as "T13 vs lumbar rib open".

**L6, morphology-only (4).** `RibFrac482`: twelve rib pairs A and B agree on one to one, then six bodies VERIDAH names L1-L6 at regular 31-35 mm spacing, the sixth on the caudal edge with the sacrum only at the edge (TotalSegmentator merged L3+L4). A genuine 25-presacral candidate that a longer field would settle; here it has no count. C-ArmLSpine `case42`, `case121`, `case136` (real intraop frames, TEST only): five mobile bodies VERIDAH names L2-L6 under a partial top body, then the sacrum; no rib head in the field (only rib tips at the top corners on case136), so L6 versus a transitional L5 cannot be counted. On case42 the lowest mobile segment has broad transverse processes against the ala. These are the same three CBCTs `transitional_subtypes.md` lists as the only real intraop L6 patients; the CBCT labels remain the truth there. `case134` (also named L6 by VERIDAH) is dropped: its L6 point lies 7 mm below its L5 on the same body.

### Unassigned (46): the two counts disagree, no subtype until a person reads it

| source | A | B | CTs | what it is on the renders looked at |
|---|---|---|---:|---|
| ribfrac | TL=T13 | TL=normal | 16 | B's first rib attached one body up or down (`RibFrac8`: is the first rib on T1; `RibFrac100`: TS's rib 1 head at the C7/T1 disc, likely normal) or B missing a mid-cage body |
| ribfrac | TL=normal | TL=ribs:11 | 8 | B missing a 12th rib TS did not attach (`RibFrac55`: ~3 cm hypoplastic 12th ribs on both sides, a B miss, not an 11-rib spine) |
| ribfrac | TL=normal | TL=T13 | 3 | B's 13th rib-bearing object: a rib fragment or a duplicate object; not looked at |
| ribfrac | other (odd count, T13 by appearance, mixed) | | 3 | `RibFrac377`: both labellers' "four lumbar" was a field-edge artefact (sacrum on the last slices), now refused by the sacrum-at-edge guard |
| ctspine1k | TL=no_count | LS: A=normal, B=L6 | 3 | B alone counts six free bodies with the cage cut (not looked at) |
| ctspine1k | TL=T13; LS=four_lumbar | normal / normal | 3 | A shifts every name by one (T13 above, four lumbar below) against a B that counts 12 + 5: a naming shift, not two anomalies |
| ctspine1k | other | | 9 | `liver_104`: twelve rib pairs, VERIDAH's "T13" carries no rib, six rib-free bodies follow (the rib-less-20th pattern again; B broken by a duplicate object at T8), left unassigned because A's TL count and B's are both off |
| carmlspine | no_count | LS=odd:3 | 1 | `case97`: lateral lowest-lumbar / sacrum contact (a Castellvi II-IV candidate) with no count |

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

## Labeller A x labeller B

| source | labellers agree | disagree | only one counts / neither |
|---|---:|---:|---:|
| carmlspine | 0 | 0 | 149 |
| ctspine1k | 127 | 18 | 78 |
| deepfluoro | 0 | 0 | 6 |
| ribfrac | 533 | 29 | 98 |
| rsna_cspine, ljubljana, deepfluoro_vendor, geneva, spinesac | 0 | 0 | 2028 |

## How far the two labellers can be trusted (validation arms; truth held outside both labellers; never registry rows)

**CTSpinoPelvic1K bench, n = 802** (truth = the release labels `benchmark/cases.csv` and the two-reader Castellvi table; B on the existing TotalSegmentator v2 inference, A on the post-fix VERIDAH ctds -- the same inputs a new CT gets). 799 of 802 were re-analysed after the 07:39 guard change; 3 were not.

| labeller | variant | TP | FP | FN | PPV | sensitivity |
|---|---|---:|---:|---:|---:|---:|
| A | L6 | 10 | 8 | 8 | 0.556 | 0.556 |
| A | four_lumbar | 9 | 35 | 0 | 0.205 | 1.0 |
| B | L6 | 12 | 22 | 6 | 0.353 | 0.667 |
| B | four_lumbar | 2 | 8 | 7 | 0.2 | 0.222 |
| combined (registry row) | L6 | 7 | 6 | 11 | 0.538 | 0.389 |
| combined (registry row) | four_lumbar | 3 | 4 | 6 | 0.429 | 0.333 |
| A and B agree | L6 | 7 | 3 | - | 0.7 | - |
| A and B agree | four_lumbar | 2 | 3 | - | 0.4 | - |

LS junction countable: A 799, B 758 of 802. A lumbosacral confusion (truth|call: n): L6|L6 10; L6|four_lumbar 1; L6|normal 7; four_lumbar|four_lumbar 9; normal|L6 8; normal|four_lumbar 34; normal|no_count 2; normal|normal 730. B: L6|L6 12; L6|four_lumbar 1; L6|normal 5; four_lumbar|L6 2; four_lumbar|four_lumbar 2; four_lumbar|no_count 1; four_lumbar|normal 4; normal|L6 20; normal|four_lumbar 7; normal|no_count 43; normal|normal 705.

Second reading of the same 802 CTs: truth = the CTSP stream's registry (`../ctsp/rows.csv`, rib convention, looked-at renders; L6 there = 29, four-lumbar = 14). Not independent of A and B (that stream also runs SPINEPS and TotalSegmentator), so it is a second reading of the bench, not a cleaner truth.

| labeller | variant | TP | FP | FN | PPV | sensitivity |
|---|---|---:|---:|---:|---:|---:|
| A | L6 | 16 | 2 | 13 | 0.889 | 0.552 |
| A | four_lumbar | 13 | 31 | 1 | 0.295 | 0.929 |
| B | L6 | 18 | 16 | 11 | 0.529 | 0.621 |
| B | four_lumbar | 2 | 8 | 12 | 0.2 | 0.143 |
| combined (registry row) | L6 | 12 | 1 | 17 | 0.923 | 0.414 |
| combined (registry row) | four_lumbar | 3 | 4 | 11 | 0.429 | 0.214 |
| A and B agree | L6 | 9 | 1 | - | 0.9 | - |
| A and B agree | four_lumbar | 2 | 3 | - | 0.4 | - |

What this says about the rows above. A two-labeller L6 row is right about 7 in 10 times against the release names and 9 in 10 against the rib-convention reading (the difference is the 29-vs-18 disagreement between the release names and the rib convention on the same spines, `../ctsp/SUMMARY.md`); a two-labeller L6 finds fewer than half of the L6 spines. A four-lumbar count from A alone is wrong four times in five (35 false positives in 802: VERIDAH's naming shifts by one), which is why the two `sacralised_L5_fused` rows here stand on the release read and not on A. B misses hypoplastic 12th ribs (TS attaches nothing to a 3 cm stub) and invents or merges bodies where a TS label splits or spans; on the bench, B's stub detection marked 8 of 16 lumbar-rib spines and 159 of 786 without one, so no lumbar-rib row is called anywhere in this stream. Against the twelve hand-counted TotalSegmentator CTs (`val_tsgt` on the dataset's masks, `val_ts12` on a fresh inference), the combined call is right on the T13 (s0616), the L6 (s1089) and eight of nine normals, calls one normal (s1178) L6 on the dataset's masks, and leaves both rib-less-20th spines (s1088, s1123) unassigned because A names the rib-less body T13 while B counts it free.

## Every other CT on the grid: what the find sweep holds and who covers it

`slurm/other_ct_find.sh` (2026-09-23 18:38) listed every `*.nii.gz / *.nii / *.mha / *.mhd / *.nrrd / *.h5 / *.npz` (429,345), every archive (301) and every directory with > 100 DICOM files (149) under `$HOME` and `/rs/rs_grp_oschome/go2432`; `find/tally.txt` (this pass, job 40436865) groups them by collection root. Every root that holds CT volumes of a person is one of:

| root | CT-like files | who covers it |
|---|---:|---|
| ~/data/TotalSegmentator_v3, ~/data/TotalSegmentator | 1,939 + 1,228 | totalsegmentator stream |
| ~/VerSeFusion, ~/vf_813 (Dataset813 images of the same scans) | 1,293 + 748 | verse stream |
| ~/data/CTSpinoPelvic1K, ~/bench/fov (FOV crops of the same CTs), ~/bench/vista3d (predictions, not CTs) | 802 + 687 + 1,120 | ctsp stream |
| /rs/.../data/cobra2026 (6,228 mha: CBCT + planning CT + projections) | 6,858 | cobra stream |
| /rs/.../data/carmlspine (149 CBCT nifti, 148 DICOM series dirs) | 745 | this stream |
| /rs/.../data/realxray_work (DeepFluoro 6, Geneva 1), /rs/.../data/or_ready (SpineSAC 3), /rs/.../data/ljubljana, /rs/.../data/deepfluoro_vendor (archives) | | this stream |
| ~/implant_ts (1,629), ~/implant_verse (1,119), ~/postop_smoke, ~/implant_*_smoke | 2,780 | synthetic-hardware copies of TotalSegmentator and VerSe CTs: the same persons, not screened again |
| ~/spinesurg-ct-nnunet (Dataset813/815 image links, nnU-Net validation predictions), ~/CTSpinoPelvic1K/.scratch | 23 + 5 | Dataset815 is CTSP + VerSeFusion persons (cross-reference below); the rest are predictions and nnU-Net temp parts |
| everything else (~/devcorpus, ~/model_night, *_ctx, ~/scaling, ~/ablate, /rs/.../data/realxray, gallery, polypose, ctsp_drr) | | rendered frames and results (.npz), not CTs |
| ~/NV-Segment-CTMR/NV-Segment-CT/example (4 nii.gz, e.g. spleen_03) | 4 | **not screened**: example volumes shipped inside a model repository (MSD spleen examples), no person identity; the one remainder |

Archives: the RSNA zip (203 GB) is the header-refused 2,022 studies; the four RibFrac zips are the 660 images; TotalSegmentator v201/v300 and C-ArmLSpine zips are the collections above; the seven DeepFluoro vendor zips are the six DeepFluoro specimens and the sawbones phantom; `ipcai_2020_*.h5` is DeepFluoro; XRSpinoPelvic1K, NHANES, AASCE, Mendeley, CSXA, Spinal-AI zips are radiographs; the rest are models, labels and software. Collections fetched after the sweep -- CTSpine1K (1,005) and RibFrac (660) by `slurm/other_ct_fetch.sh`, and the scoping-review downloads under `anomaly_harvest/<source>/` (amos22, abdomenatlas3_mini, idc, curvas, curvas_pdacvi, deep_psma, aortaseg60, barts_crl, quadra_hc, pengwin2026, nlst_pilot, csi2014, ctpelvic1k_clinic; `acq_*` jobs) -- are known by construction: the first two are rows here, the rest belong to the acquisition stream.

### Cross-reference: Dataset815 flags and the CTSpine1K README lists, beside the owning stream's own call

| owning stream | Dataset815 flag (repaired) | that stream's subtype for the person | persons |
|---|---|---|---:|
| ctsp | L6 | L6 | 18 |
| ctsp | manifest:lumb | no registry row | 1 |
| ctsp | manifest:sacralization | castellvi_I_II | 2 |
| ctsp | manifest:sacralization | sacralised_L5_fused | 3 |
| verse | L6 | L6 | 48 |
| verse | L6 | no registry row (screened: none; release mask carries an L6, id 25, against a normal read) | 1 |
| verse | L6 | no registry row (screened: none, no transitional call) | 1 |
| verse | T13 | T13 | 6 |

Dataset815-flagged persons with NO registry row in the owning stream (for that stream to resolve): COLONOG_500 (ctsp:0706, manifest "lumb"), VERSE_gl279 (verse:gl279, L6), VERSE_verse707 (verse:verse707, L6).

| owning stream | CTSpine1K README list | that stream's subtype for the person | persons |
|---|---|---|---:|
| ctsp | L6 | L6 | 16 |
| ctsp | sacralisation | sacralised_L5_fused | 9 |
| other_ct | L6 | this stream (row at tier read) | 1 |
| other_ct | sacralisation | this stream (row at tier read) | 2 |
| verse | L6 | L6 | 8 |
| verse | sacralisation | no registry row (screened: none, read normal) | 1 |
| verse | sacralisation | sacralised_L5_fused | 2 |

Of the CTSpine1K README's 25 L6 and 14 sacralisation cases, 24 and 11 are persons another stream owns and agree with that stream except one VerSe sacralisation read normal there; 1 and 2 are the rows at tier `read` here (all three MSD-T10); the remaining L6 names fall on the six COLONOG cases whose names are not in the release spreadsheet (`crosswalk_report.json` name_not_in_xlsx 6) and are not resolved.

## Review queue (`review_queue/`, `review_list.jsonl`, `review_queue/index.csv`)

87 registry cases and 103 validation-arm cases, every one rendered as a sagittal + coronal MIP carrying both labellings (`<source>__<case>.png`, 232 files); the 21 registry cases that were looked at more closely also have a `__look.png` (three panels at the CT's own resolution) beside the MIP and in `looks/`. `index.csv` has one line per case with its reasons and the look note.

| review reason (registry) | cases |
|---|---:|
| B count implausible (segmentation failure until a person says otherwise) | 31 |
| lateral lowest-lumbar / sacrum contact (Castellvi II-IV candidate) | 18 |
| DISCORDANT A=T13 B=normal | 16 |
| DISCORDANT A=normal B=ribs:11 | 11 |
| L6 call (every positive is looked at) | 7 |
| B count uncertain | 7 |
| DISCORDANT A=four_lumbar B=normal | 6 |
| L6 at tier morphology-only | 4 |
| B cage count uncertain | 4 |
| T13 at tier single-labeller / T13 call / T13 vs lumbar rib open | 4 each |
| DISCORDANT A=normal B=L6 | 3 |
| DISCORDANT A=T13 B=normal; A=four_lumbar B=normal | 3 |
| DISCORDANT A=normal B=T13 | 3 |
| release annotation has 4 lumbar ids where the labellers call L5 / release read vs labellers DISCORDANT | 2 + 2 + 1 |
| odd counts, mixed discordances, a possible rib outside the TS rib classes | 1 each (6) |

For Greg to adjudicate first: the four RibFrac T13 candidates (RibFrac101, 93, 322, 539: is the 13th body's rib a rib or a lumbar-type stub), the two rib-less-20th spines called L6 (liver_119, liver_95: L6 by convention or a rib-less T12), RibFrac482 (a sixth body at the field edge), and the 18 lateral lumbosacral contacts (16 carmlspine among them) that no count can grade.

## People and duplicates

- 782 CTSpine1K COLONOG volumes are CTSpinoPelvic1K persons and are rows of the ctsp stream, not here; two COLONOG volumes are not in the release and are screened here (one none, one no count); six COLONOG names are not in the release spreadsheet and are keyed as their own persons.
- No CTSpine1K MSD-T10 / COVID-19 / HNSCC person is known to be in another collection (`docs/DATA_ACCOUNTING.md` alias classes); none is claimed.
- RibFrac ships no patient identifier: a case is a person. RSNA: a study is a person.
- C-ArmLSpine: 149 acquisitions from day-grouped surgical lists; a case is not a proven person, and all 149 carry REAL frames (TEST only, never rendered for training). The three morphology-only L6 rows and case97 are therefore TEST people only.
- DeepFluoro's six specimens appear twice on disk (the IPCAI h5 and the vendor zips): one row each.

## The acquisition-space review and this stream

Nothing here is requeued. Two notes for the streams downstream of this one:

1. The review names CTSpine1K as the CT-only source that X23D rendered 17,420 views from, and lists DeepFluoro, the Ljubljana set and SpineWeb's paired CT + calibrated-fluoroscopy sub-cohorts as the public paired sets. CTSpine1K is 78 % CTSpinoPelvic1K persons (above): any render corpus that draws on both must split by the alias key in `alias_rows.csv`, or one person lands on both sides. SpineWeb's paired sub-cohorts are not on the grid; if they are wanted as real-frame TEST material, that is a request for the acquisition stream, not a row here.
2. The review's coverage / normalised-entropy argument is about the POSE distribution of rendered frames, which this registry does not carry. The CT-only positives here (MSD-T10 L6 x3, sacralised x2, RibFrac T13 x4 and L6 x1) are render inputs; how their poses are sampled is measured by the review-integration workflow (`results/coverage/`), and the real-frame rows (C-ArmLSpine) are TEST only whatever the pose sampling.

## What is not known

- Whether the four RibFrac "T13" spines have 25 or 24 presacral vertebrae: the sacrum is out of every one of those fields. Two of them (RibFrac322, 539) carry only 3-4 cm stubs on the 13th body, which the VerSe 38 mm rule would call lumbar ribs.
- Whether `liver_119` and `liver_95` should count as L6 for a fluoroscopy naming task: they are 24-presacral spines whose 12th thoracic body carries no rib. Under the rib convention the render bank will name that body L1 and the lowest lumbar body L6; the CTSpine1K annotation names them T12 and L5.
- The sixteen RibFrac "A=T13, B=normal" discordances were not all looked at; on the two that were, one is B's first rib on C7 (normal) and one is unresolved on thick slices.
- 3 of the 802 bench cases were not re-analysed after the 07:39 guard change; the bench tables include their earlier analysis.
- The four NV-Segment-CTMR example volumes were not screened.
- The DeepFluoro-vendor fiducial zip (09_ftrac_fiducial) holds fiducial data, not a further CT; not opened.

## Reproduce

```
# grid (sbatch -D /rs/rs_grp_oschome/go2432/tmp; outputs under /rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct)
sbatch slurm/other_ct_find.sh                                   # find/vol.tsv arc.tsv dcm.tsv
sbatch slurm/other_ct_fetch.sh                                  # CTSpine1K, RibFrac, RSNA headers
sbatch -J oct_cases slurm/other_ct_cpu.sh cases                 # cases/all.csv (+ EXTRA=<csv> for anything the find turns up)
sbatch -J oct_seg --array=0-9 slurm/other_ct_seg.sh             # SPINEPS + TotalSegmentator (GPU)
sbatch -J oct_an --array=0-79 slurm/other_ct_cpu.sh analyse     # per-CT json (CASES=cases/stale.csv REDO=1 after a rule change)
sbatch -J oct_agg slurm/other_ct_cpu.sh aggregate               # rows.csv rows.json evidence.jsonl denominators.json review_list.jsonl
sbatch -J oct_rend --array=0-23 slurm/other_ct_cpu.sh render    # review_queue/*.png
sbatch -J oct_d815 slurm/other_ct_cpu.sh d815                   # d815_crosswalk.csv d815_summary.json
# local
python tools/other_ct_summary.py --dir SchwingNet/results/transitional_registry/other_ct --registry SchwingNet/results/transitional_registry
```
