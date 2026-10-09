# J0 case list (reader E timing task)

`j0_cases.json` beside this file is the machine-readable list: 20 CTs x 3 segmenters = 60 (CT, segmenter) pairs,
per `docs/CT_LSTV_CLASSIFIER_PLAN.md` section 8. Every path in it was checked on the grid login node on 2026-09-24
(`[ -e ]` + `stat -c %s`, one ssh per batch; byte sizes recorded). No G3 test person; every person is on the G3
**train** side (`fig6/frozen/auto_truth.csv` column `g3_side`, the same split as `~/split_final.json`).

## Who is in it

| corpus | case | side | truth | why |
|---|---|---|---|---|
| CTSP | 0097 | train | read L6, Castellvi IIb | LS-L6 pool (positives_table B): two-reader Castellvi, read count 6 = release count 6, release id 25 |
| CTSP | 0234 | train | read L6, IIIb | same |
| CTSP | 0244 | train | read L6, Ib | same |
| CTSP | 0302 | train | read L6, Ib (readers disagree on grade, agree on count) | same |
| CTSP | 0366 | train | read L6, IIb | same |
| CTSP | 0029 0768 0890 0925 1138 | train | ordinary | release five lumbar, not in `transitional_subtypes.csv`, readers A/B/C unanimous ordinary, in calibration; seeded sample (seed 20260924) of a 431-case pool |
| VerSe | verse085 | train | read L6, IIIa, structure 7/12/6/5 | Loffler read; HELD by the id guard (expert mask stops at 24, no id 25); 25 presacral by the read |
| VerSe | verse502 | train | read L6, IIIb, 7/12/6/5 | same |
| VerSe | verse514 | train | read L6, IIIb, 7/12/6/5 | same |
| VerSe | verse518 | train | read L6, IV, 7/12/6/5 | same |
| VerSe | verse534 | train | read L6, IIIb, 7/12/6/5 | same |
| VerSe | verse096 verse755 verse758 verse811 verse825 | train | read normal, 7/12/5/5 | LS junction in field, readers A/B/C unanimous ordinary, in calibration; seeded sample of a 53-person pool (one series per person) |

## Where the three masks are (per corpus)

| corpus | CT | release / expert | SPINEPS (post-fix) | TotalSegmentator `total` | TS class map |
|---|---|---|---|---|---|
| CTSP | `~/data/CTSpinoPelvic1K/ct/<id>_ct.nii.gz` | `~/data/CTSpinoPelvic1K/labels/<id>_label.nii.gz` (v11; `labels_for(volume)`) | `RS/spineps/ctsp/CTSP_<id>_seg-vert_msk.nii.gz` + `CTSP_<id>_ctd.json` | `~/bench/totalsegmentator/native/COLONOG_<n>.nii.gz` (single multilabel file; the COLONOG number is NOT the case id, taken from `auto_reference/lists/ctsp.csv`) | `~/bench/totalsegmentator/class_map.json` |
| VerSe | `~/VerSeFusion/data/unified/scan-<cid>/scan-<cid>_ct.nii.gz` | `.../scan-<cid>_msk.nii.gz` (raw VerSe ids, **no sacrum id**: sacrum features NaN + mask bit) | `RS/spineps/ctd_relabel/bench_ts_native/VERSE_<cid>_seg-vert_msk.nii.gz` + `VERSE_<cid>_ctd.json` + `VERSE_<cid>_relabel.json` | `RS/anomaly_harvest/verse/ts/<cid>.nii.gz` (single multilabel file, TS 2.18.0) | `RS/anomaly_harvest/verse/class_map.json` |

The VerSe `scan-<cid>_ct` / `_msk` entries are symlinks into `~/VerSeFusion/data/raw/verse20/{01_training,02_validation,03_test}/<cid>/` (CT-iso, CT-sag or CT-ax series); the JSON records the resolved targets and their sizes (`readlink -f`, `stat -L`).

`~` = `/wsu/home/go/go24/go2432`, `RS` = `/rs/rs_grp_oschome/go2432/data`. A third copy of the class map,
`RS/anomaly_harvest/cobra/class_map.json`, is what readers A/B load for every corpus (they state the copies are
md5-identical); the extractor should hash whichever it loads into each JSON. TS `sacrum` and `vertebrae_S1` are
disjoint: the sacrum is their union.

## Who was left out and why

- CTSP contradicted (read count != release count) 0008 0021 0033 0049 0176 0179 0196, and 0068: barred until re-read.
- CTSP LS-L6 on the G3 test side: 0005 0208 0268 0376 0565 0950 1053 (never used); 0960 is val; 0486 0831 0999 are
  train but not needed for five.
- VerSe contradicted by the scan: verse026 verse512 verse540 verse571 verse612 verse765 verse814. TL-11 by the
  counting rule (24 presacral, 11 rib-bearing): verse544 verse581 verse606 verse626 verse636 verse642. Ambiguous or no
  LS junction in that series: verse406 verse403 verse559.
- Held VerSe L6 lacking a SPINEPS mask (reader A had no `seg-vert` mask): verse513 verse535 verse616 - replaced, not
  left as holes.
- Held VerSe L6 on the G3 test side: verse024 verse034 verse088 verse510 verse526 verse554 verse555 verse557 verse587
  verse592 verse609.
- verse809 (ordinary sample) replaced by verse811: the only ctd beside its SPINEPS mask is
  `VERSE_verse809_ctd_isogrid.json`, a resampled-grid centroid file, which `assert_verse_monotonic` would compare
  against a native-grid mask.

## Notes for the J0 extractor

- Segmenter names are dropped; instances are ordered by world-S centroid from the affine (CTs are P,I,R; canonicalise
  to analyse, never write).
- Each JSON carries per-stage seconds, the code sha256, the mask family and loader (`mask_families` in the case entry),
  `sacrum_source`, `sacrum_ml`, FOV flags; each run writes a midsagittal and a coronal PNG of the mask over the CT.
- The five VerSe L6 cases are exactly the ones whose expert mask cannot carry the call; on the expert segmenter the
  24th body is the read's L6 and there is no sacrum: the feature block must not read "five lumbar" from the ids.
