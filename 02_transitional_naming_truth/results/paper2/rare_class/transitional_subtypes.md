# Transitional anatomy by SUBTYPE -- every case, every source, distinct patients

Built by `tools/transitional_subtypes.py` on 2026-09-23 from: the anomalous inventory (job 40416205,
raw-mask/release-label ids), `lstv_flag_labels_v2.csv` (release-mask label counts + VerSe audit reads),
CTSpinoPelvic1K `docs/castellvi_consensus.csv` (two radiologist readers), the VerSeFusion manifest,
and the v8 level-bank split (`allspine_v8_fov96_ctx/meta.json` + person keys).
Label ids: CTSP v11 L1..L5 = 20..24, **L6 = 25**, sacrum = 26 (legacy ostk map has L6 = 6 -- never mix);
VerSe raw masks L6 = 25, T13 = 28.

**Distinct patients, not renders, are the statistical power.** The split column is PERSON-level:
a person with any scan in v8 train is `train` (not evidence), `validation` only with a validation scan
and no train scan, `absent` = the model never saw them. No person sits on both sides (checked).

| subtype | cases | distinct patients | val people (evidence) | train people (not evidence) | absent | per source |
|---|---:|---:|---:|---:|---:|---|
| L6 | 112 | 110 | 22 | 85 | 3 | carmlspine_real 3, ctsp 18, totalsegmentator 3, verse 86 |
| T13 | 7 | 7 | 1 | 6 | 0 | totalsegmentator 1, verse 6 |
| castellvi_I_II | 31 | 31 | 6 | 24 | 1 | ctsp 4, verse 27 |
| lumbar_rib | 14 | 14 | 0 | 14 | 0 | ctsp 14 |
| sacralised_L5_fused | 28 | 28 | 5 | 23 | 0 | ctsp 12, verse 16 |
| unassigned | 4 | 4 | 1 | 3 | 0 | ctsp 4 |
| _four_lumbar_mask (modifier, overlaps sacralised) | 16 | 16 | - | - | - | modifier |
| _lumbar_rib (modifier incl. primary) | 16 | 16 | - | - | - | modifier |

## How the mask represents a fused (sacralised) L5 -- this decides what the detector CAN see

- CTSP, fused body **merged into the sacrum label** (only 4 lumbar ids; the detector can only ever see
  ONE body there): 9 cases -- volumes 0094, 0151, 0156, 0158, 0760, 0785, 0787, 0875, 1031. Fused elements carry the
  sacrum id 26 (docs/CASTELLVI_SCREEN_BLIND_SPOT.md: 'fused into the ala and labelled sacrum').
- CTSP, fused L5 **keeps its own id 24** (5 lumbar ids; the detector CAN see two bodies): 3
  cases -- volumes 0008, 0021, 0049.
- VerSe 'sacralization (4 lumbar)' scans (verse549, verse552, verse559): 4 lumbar ids; whether the
  fused body sits inside a sacrum label or is unlabelled was NOT checked at voxel level in this pass.
- So the two-bodies-or-one question is answerable on the CTSP side exactly as stratified above; the
  detector's behaviour must be quantified separately on the merged and own-label strata.

## Caveats and unknowns (nothing below is guessed)

- **both_L6_T13: zero cases in every source.** No spine carries both an L6 and a T13 in any truth table.
- VerSe L6: 50 scans are raw-mask verified (id 25 present); 38 more
  are audit-string only ('lumbarization (6 lumbar)') from the wider VerSe download, without a raw-mask
  id check in this pass; two id pairs are one person (verse255=verse403, verse261=verse406).
- The VerSeFusion manifest `has_T13` flag is known-wrong (says 18; raw-mask truth is 6). T13 rows here
  come from raw-mask id 28 only. Three T13 spines (verse582, verse601, verse631) ALSO carry a
  lumbosacral Castellvi audit read, recorded in their notes -- T13+LSTV co-occurs, T13+L6 does not.
- TotalSegmentator rows are the verified subtypes of `SchwingNet/results/rare_class/ts12_subtype_override.json`
  (F1, `SchwingNet/results/spineps_ids/TS12_VERIFY.md`: an independent count from SPINEPS instances and CT rib
  components, no VERIDAH name; no radiologist read, so their Castellvi subtype is unassignable). The twelve were
  once selected by 'SPINEPS mask id 25 present' on masks whose ids are a raw 1..N enumeration, and all read L6.
  Verified: TS_s0616 T13, TS_s1088 L6, TS_s1089 L6, TS_s1123 L6;
  dropped as normal spines: TS_s0224, TS_s0790, TS_s1124, TS_s1171, TS_s1178, TS_s1304, TS_s1350, TS_s1380.
- Rib convention (docs/STUDENT_FLUORO_CORRECTION_GUIDE.md: L6 = six rib-free vertebrae between the last
  rib-bearing vertebra and the sacrum; T13 = thirteen rib-bearing vertebrae). TS_s1088 and TS_s1123 have 12 rib
  pairs and a rib-less 20th vertebra with thoracic-type transverse processes, so they are L6 here; VERIDAH names
  that vertebra T13 (column `subtype_veridah`), and their rendered frames carry VERIDAH's names until relabelled.
- Only those twelve TotalSegmentator spines were examined. The VERIDAH ctd names 41 L6 and 56 T13 among the
  1,144 TS v2 bench fields and more in TS v3 (`SchwingNet/results/spineps_ids/CENSUS.md`); none of those is
  verified, and on CTSpinoPelvic1K a VERIDAH L6 call has a PPV near 42 % against the release labels.
- C-ArmLSpine case42/case121/case136 are the only REAL intraop L6 patients; truth is the CBCT labels.
- Unassigned (4): CTSP volumes 0801, 0931, 1043 and 1123 carry only 4 lumbar ids in the release mask
  but read normal at the source with no Castellvi grade; four-lumbar anatomy vs labelling artefact is
  not established by any table (1123 is a CTC-source case that also sits in v8 validation).
- CTSP volume 0172 (lumbar_rib) is in `docs/lstv_reread_queue.csv` pending a radiologist re-read for
  suspected sacralization; its subtype may change.
- Castellvi grades on CTSP L6 spines (lumbarised S1 articulating/fusing with the sacrum) are kept in
  the `castellvi` column as a modifier; 17 of the 18 CTSP L6 cases carry a consensus grade (0068 none).
- lumbar_rib people sit 14/14 in v8 TRAIN: this subtype currently has ZERO evidence-grade people.
