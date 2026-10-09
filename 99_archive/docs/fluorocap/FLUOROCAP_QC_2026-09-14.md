# FluoroCap corpus QC, 2026-09-14

Produced by `tools/fluorocap_qc.py` against `decode_v2_v2.jsonl`, `panels.jsonl`, `hardware_constraints.jsonl`,
`region_preds.jsonl` and the CT render directories. Everything below is either counted off disk or computed from
those files. No number here is a human-verified accuracy, because no human-verified set exists yet; that is the
single most important gap and it is stated plainly in section 6.

## 1. How big it is

| quantity | count |
|---|---|
| panel images on disk | 11,349 |
| — figure panels | 10,870 |
| — video frames (YouTube) | 479 |
| figures split into panels | 5,853 high confidence, 1,730 medium, 3,287 not split |
| panels carrying a caption that names a level | 2,815 |
| panels run through the decoder | 3,294 |
| panels with at least one vertebra box | 2,528 (766 decoded panels found no box) |
| panels with three or more boxes | 1,707 |
| vertebra labels assigned | 11,929 |
| effective unique decoded panels after de-duplication | 3,027 (243 duplicate groups, 267 redundant copies) |

Route mix: Europe PMC 8,190, PMC-18M 2,034, Open-i 582, YouTube 479, Wikimedia Commons 35, Openverse 27.

Only **29% of known panels produced a vertebra box**. Some of that is correct behaviour — the corpus deliberately
keeps non-radiograph panels from multi-panel figures — but the modality head scored 10,863 panels at 93% held-out
accuracy, so a large share of the 71% is detector miss rather than "not a spine film". The self-training run
(`detect_v6f`) exists to attack exactly this and has not yet been folded into a decode.

### 1b. The self-trained detector did not raise the box rate (measured later the same day)

On the same 2,815 captioned panels, the deployed detector (v5z) found at least one vertebra box on 69.5% and the
round-one self-trained detector (v6f) on 68.7%, with fewer boxes in total (7,845 against 9,077), 125 panels
gained and 147 lost. Self-training on its own pseudo-labels is a wash; the box rate is a resolution problem
(section 2) before it is a detector problem, and the publisher refetch is the lever that is being pulled.

## 2. Image quality

| metric | p5 | p25 | p50 | p75 | p95 |
|---|---|---|---|---|---|
| width (px) | 139 | 205 | 280 | 462 | 756 |
| height (px) | 153 | 220 | 279 | 387 | 691 |
| short side (px) | 128 | 181 | 231 | 328 | 600 |
| megapixels | 0.03 | 0.05 | 0.08 | 0.14 | 0.44 |
| contrast (intensity SD) | 28 | 44 | 55 | 66 | 82 |
| sharpness (Laplacian variance) | 55 | 222 | 475 | 969 | 2,554 |

45.8% of panels have a short side under 224 px; only 7.9% reach 512 px. 61% are greyscale, 1.0% are low contrast,
5.1% are blown out and 1.3% crushed black.

**This is the corpus's worst measured property.** The level model crops a 320 px window around a target scaled to a
fixed vertebra height; on a 231 px panel that window is mostly upsampled interpolation. Resolution, not count, is
the binding constraint on what these images can teach. The lever is the publisher's own copy of each figure: on corpus figures, Cureus serves 16x the pixels of the
PMC copy, MDPI 9-20x, Elsevier's CDN 12x, Frontiers 6x, Springer/BMC/Nature 4x, all by deterministic URLs with
no login (`tools/fluorocap_refetch_hires.py`, running over all 2,880 PMC figures on 2026-09-14: 414 of the
first 816 replaced, median gain 9x). The unfixed remainder is Wiley, SAGE, JNS and Wolters Kluwer, which block
non-browser clients, and a dozen small society journals whose pages need their own rule.

## 3. Level coverage

| level | panels | level | panels | level | panels | level | panels |
|---|---|---|---|---|---|---|---|
| C1 | 124 | C2 | 223 | C3 | 360 | C4 | 427 |
| C5 | 434 | C6 | 400 | C7 | 306 | T1 | 172 |
| T2 | 146 | T3 | 148 | T4 | 151 | T5 | 155 |
| T6 | 180 | T7 | 203 | T8 | 236 | T9 | 263 |
| T10 | 291 | T11 | 368 | T12 | 745 | **T13** | **0** |
| L1 | 1,036 | L2 | 1,218 | L3 | 1,515 | L4 | 1,412 |
| L5 | 1,216 | **L6** | **0** | sacrum | 593 | | |

By region: lumbar 1,737 panels, thoracic 802, cervical 657, sacral 525.

**T13 and L6 have never been assigned to a single real panel.** Both are in the model's 27-class output
(`make_context_crops.LEVEL_ORDER`), so this is not a missing class — the model simply never predicts them and no
caption forced one. Only 2 of 2,815 captioned panels mention any transitional term at all. The transitional
thesis, which is the project's headline claim, currently has **no real-image evidence whatsoever**.

The CT render banks show why: across 1,175 renders the training distribution holds ~1,100 of each lumbar level
against 68 L6 and 6 T13 vertebrae. The instrumented builds are similarly skewed (L6 7, sacrum 237, T12 700).

## 4. How accurate are the pseudolabels

The decoder is allowed to read the caption. When it does (`hard_caption` true), agreeing with the caption
afterwards proves nothing. The corpus splits cleanly and only the second row is a test:

| rows | panels | caption containment | mean Jaccard |
|---|---|---|---|
| caption constrained the search | 1,678 | 100% (by construction) | 0.52 |
| **caption held out** | **389** | **56.8%** | **0.34** |

Caption-free accuracy by which evidence term moved the answer:

| decided by | panels | containment |
|---|---|---|
| figure mate | 10 | 80.0% |
| caption (soft) | 44 | 79.5% |
| vision-language model | 94 | 73.4% |
| caption hardware constraint | 23 | 69.6% |
| printed level OCR | 13 | 53.8% |
| **level model alone** | **175** | **38.3%** |

Per-level recall on the caption-held-out rows: L3 70.4%, L2 68.3%, L4 68.8%, L1 63.5%, C4 56.9%, C3 56.5%, L5
51.8%, T12 48.5%, C5 47.1%, T6 41.9%, C6 39.6%, T1 32.0%, T9 30.3%, C7 23.8%, T8 21.1%, T7 16.7%, T10 17.1%,
T11 15.0%, C1 14.3%, sacrum 11.6%, T3 10.7%, C2 9.8%, T2 8.5%, T4 0.0%.

The region head (four-way) scores 63.2% against the caption's region: lumbar 76.6%, cervical 55.0%, thoracic
44.8%, sacral 12.6%. Thoracic panels are called lumbar 203 times out of 478; sacral panels are called lumbar 90
times out of 135.

**Read together: the model is a lumbar model.** It is usable from L1 to L4, weak at L5 and T12, and close to
useless in the thoracic spine, at C1–C2, and at the sacrum. The decoder's other evidence terms are each better
than the model, which is the correct signal that the constraint decoding is doing real work — and it is also why
the corpus should not be used to train the next model without re-weighting.

## 5. Does the decoder help without any caption?

Figure mates are panels from the same figure, which almost always show the same region. With no caption used:

| labeller | pairs | same region | Jaccard ≥ 0.5 |
|---|---|---|---|
| level model run alone | 468 | 52.1% | 30.8% |
| constraint decoder | 519 | **91.5%** | **68.2%** |

This is the strongest result in the QC. The decoder nearly doubles caption-free agreement, and it does so on a
measure the caption cannot contaminate.

## 6. Hardware

1,886 of 2,815 captioned panels carry a device-to-level constraint parsed from the caption (body 633, disc 453,
span 416, near 230; 929 have none). On the caption-held-out rows:

| subset | panels | containment |
|---|---|---|
| hardware present | 286 | 55.2% |
| no hardware | 103 | 61.2% |

Hardware costs about six points, but with 103 panels in the control arm the interval is wide and this should be
treated as "no evidence of robustness" rather than "a measured 6-point penalty". The zero-shot implant detector
(OWLv2 at threshold 0.2) was hand-checked at 33% recall with 28% false positives; there is no labelled implant
set on real panels.

## 7. The synthetic side

| arm | count |
|---|---|
| anchor DRRs (parallel) | 5,185 |
| CTSpinoPelvic1K DRRs | 801 |
| VerSeFusion DRRs | 374 |
| instrumented CTs, CTSpinoPelvic1K | 1,518 constructs |
| instrumented CTs, VerSeFusion | 478 and building |
| instrumented CTs, TotalSegmentator | 1,456 and building |

Constructs: pedicle screws and rods 1,358, cement 978, screws with an interbody cage 700, lumbosacral fixation to
S1 237, cervical lateral mass 154, anterior odontoid screw 64. Instrumented levels run C2 64 through L2 772 and
sacrum 237, so no region of the spine is now hardware-free in the synthetic data — which was not true this
morning.

The cone-beam physics renderer produces frames with divergent-beam magnification, beam hardening, scatter,
quantum noise, round and rectangular collimation and image-intensifier vignetting. Two defects were found and
fixed: `grid_sample` pads outside the volume with HU 0, which is soft tissue, so every ray accumulated 300 mm of
phantom water and the frame came out uniformly white; and a local name collision put a tensor where the
source-image distance belonged and killed the shard mid-write.

## 8. What is not known

- **No panel has been read by a human.** Every accuracy figure above is agreement between two automatic sources.
  Settling the true rate costs 196 adjudicated panels for ±5% or 545 for ±3% around 85%.
- **Box recall is unmeasured.** There is no annotated box ground truth on FluoroCap, so the only detection number
  available is the fraction of panels with any box at all.
- **Rare-level accuracy cannot be estimated.** C1, C2, T13, L6 and the sacrum have too few caption-held-out
  panels, and T13 and L6 have none.

## 8b. Root cause of the thoracic and sacral collapse, found the same day

`tools/diag_level_model.py` scores one level model three ways through the same code path: its own bank's
validation split, the same crops read by the recurrent head, and crops cut live from the CT renders. The result
overturns the reading in section 4.

| | overall |
|---|---|
| own bank, single crop | **98.7%** |
| own bank, recurrent head over the run | **99.4%** |
| CT renders, single crop | 35.7% |

Per level, with the bank's own training counts beside the render score:

| level | crops in training | own-bank accuracy | render accuracy | render confusion |
|---|---|---|---|---|
| C3-C7 | ~4,300 each | 98.7-99.7% | no renders scored | |
| T1 | 22 | 100% | | |
| **T10** | **0** | none | **0.0%** | L1 147, T12 97 |
| **T11** | **0** | none | **0.0%** | L1 174, T12 84 |
| T12 | 132 | 94.9% | 4.3% | L1 247 |
| L1 | 3,843 | 85.4% | 43.0% | L2 159 |
| L2 | 3,847 | 91.5% | 78.7% | |
| L5 | 3,850 | 97.6% | 69.7% | |
| **L6** | **0** | none | **0.0%** | L5 6 |
| sacrum | 124 | 95.7% | 5.3% | C4 79, L5 63 |

The bank is `films_all2_fov96_ctx`, and its cases are CSXA cervical films and NHANES lumbar films. **There are no
thoracic films in it at all.** T2 through T11, T13 and L6 have exactly zero training crops; T12, the sacrum, C1,
C2 and T1 have between 22 and 190. The model is not biased toward the lumbar spine by an imbalanced loss - it was
never shown the rest of the spine.

This changes the fix. Logit adjustment and class-balanced sampling re-weight classes that exist; they do nothing
for a class with no examples. The corpus already holds what is missing: the CT render banks carry about 1,000
crops each of T10, T11 and T12 and 800 of the sacrum, VerSeFusion covers C1 to L6, and 55 VerSeFusion cases carry
an L6 or a T13. `tools/make_context_crops.py` now takes `--rungs` and a `--group-regex`, so renders of one CT
under several poses stay on one side of the split, and the all-spine bank merging films with every CT render
source is building.

The residual gap is separate and smaller: at L1, where the bank holds 3,843 crops, own-bank accuracy is 85.4% and
render accuracy 43.0%. That difference is domain, not coverage, and is what the cone-beam physics renders and a
resolution-degradation augmentation are for.

## 9. What this says to do next, in order

1. **Read 400 panels.** Nothing else converts an agreement number into an accuracy number, and the reader pages
   already exist (`reading_v2`, 64 pages built). Stratify by decided-by and by region so the rare arms get read.
2. **Build the all-spine bank and retrain** (building now). The thoracic spine and the sacrum are ABSENT
   from training, not under-weighted, so re-weighting cannot help. Merge the films with the CTSpinoPelvic1K,
   VerSeFusion and physics render banks, split by patient, and retrain rung 1.
3. **Oversample T13 and L6 by two orders of magnitude** in every render arm (`tools/find_rare_cases.py` lists the
   cases; the physics renderer takes `--cases-file`). Until a real panel carries one of these labels the
   transitional claim is unsupported.
4. **Raise resolution**: refetch publisher-original figures and finish the 1080p video refetch. Half the corpus is
   below the model's own crop window.
5. **Fold the self-trained detector into a decode** and re-measure the 29% box rate.
