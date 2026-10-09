# COBRA Elekta window and half-fan panel diagnosis (A31)

2026-09-23. Greg (07:20): the Elekta XVI and Ljubljana renders in fig4_formation "look like shit — you're not
using a weird window on the X-rays, right?" Answer: yes and no. The attenuation, the geometry and the card fit
are sound — **the display window is fed the wrong region, and the eval charges the detector for anatomy the
half-fan panel physically cannot see.** Numbers below are computed over every exported cobra_elekta frame
(3,480 frames, 150 cases; per-frame rows in `frames_shard*.csv`, geometry in `panel_geometry.csv`, R² in
`r2_body_vs_field.json`, aggregation in `aggregates.json`).

## 1. The window's field is air, and more of it the more lateral the view

`deepfluoro_anchor.window_or` maps attenuation percentiles 1/5/50/95/99 over `field` onto 27/47/126/216/239;
the export passes `field = I > 0` — every pixel with signal. Air fraction of that field (attenuation < 0.25),
by view angle:

| view (|lat_deg| folded) | frames | air share of field, median | p90 | max | I0 saturated at 65535 |
|---|---|---|---|---|---|
| AP (< 15°) | 542 | 0.071 | 0.197 | 0.356 | 503/542 |
| oblique (15–75°) | 2,207 | 0.152 | 0.307 | 0.522 | 2,059/2,207 |
| lateral (≥ 75°) | 731 | 0.258 | 0.399 | 0.573 | 697/731 |

Fifteen-degree bins rise monotonically: 0.071 (0–15°) → 0.082 → 0.125 → 0.173 → 0.233 → 0.258 (75–90°).
On an air-heavy frame p1/p5 of the field collapse to ~0 attenuation, so grey 27–47 is spent on air and the
body is squeezed into the top of the ladder. That is the washed-out slab Greg saw. (I0 is the saturation
value on 3,259/3,480 frames — a lower bound, stated in every meta; window_or is percentile-based and
invariant to the constant offset this puts on attenuation.)

## 2. The half-fan panel, the truth boxes, and what the eval does with them

Geometry (from `geometry.xml`, 150 cases): **145/150 half-fan**, detector offset median **−114.3 mm**
(range −117.7 to +2.1). One frame sees a transverse band at the isocentre of (panel/2 ± |offset|) × SID/SDD:
median **56.8 mm** on the short side, **205.7 mm** on the long side. A single lateral frame therefore
physically cannot hold the spine and the flank at once; the reconstruction FOV (262.5 mm) exists only over
the full orbit. The Figure-4a example was such a frame — an unrepresentative pick, not a formation defect.

The export measures this and writes it: at build time it dropped 3,528 projected structures incomplete in the
CT and 10,493 with visible_frac < 0.5 (MIN_VIS), and wrote `visible_frac` on every kept box. What ships:

| split | frames | truth boxes | vertebrae | sacra | boxes with visible_frac < 1 |
|---|---|---|---|---|---|
| train | 2,640 | 6,085 | 3,691 | 2,394 | 3,281 (53.9 %) |
| val | 192 | 280 | 129 | 151 | 207 (73.9 %) |
| test | 648 | 1,502 | 893 | 609 | 864 (57.5 %) |

Test vertebrae by visibility: 349 whole, 254 at 0.95–1, 161 at 0.75–0.95, **129 at 0.5–0.75**. Test sacra:
289 whole, 152, 112, **56**.

**`tools/realxray_eval.py` applied NO visibility threshold**: it never read `visible_frac` (grep: the only
gates are `--conf` and IoU ≥ 0.5). Every one of the 864 partly visible test boxes stood in the recall
denominator, and each one the detector failed to find counted as a full miss — the Elekta recall on the
detection figure is biased DOWN by up to 290 vertebrae (vf < 0.95) of 893, 32.5 % of the denominator. The
parallel rescore over these shards (checkpoint 13:35) puts numbers on it: at pooled conf 0.74 the detector
finds 832/893 = 93.2 % of test vertebrae, 333/349 = 95.4 % on whole-panel truth only, and **45 of the 61
misses are off-panel (visible_frac < 1) truth** — three quarters of the "misses" are anatomy the panel did
not fully see. Fixed 2026-09-23: `--min-vis` moves boxes below it from truth to
IGNORE (out of the denominator; predictions on them are not false positives; `pooled.ignored_truth` reports
the count). At `--min-vis 0.75` the test denominator sheds 129 vertebrae + 56 sacra = 185 boxes (12.3 % of
1,502).

## 3. The grey range the body occupies in the shipped 8-bit frames

Median over frames of the body pixels' grey percentiles (p5/p50/p95) and span (p95−p5):

| view | shipped export (field window) | body window | shipped span | body-window span |
|---|---|---|---|---|
| AP | 74 / 133 / 217 | 47 / 126 / 216 | 145 | 169 |
| oblique | 70 / 152 / 219 | 47 / 126 / 216 | 150 | 169 |
| lateral | 69 / **175** / 222 | 47 / 126 / 216 | 153 | 169 |

The shipped lateral body sits with its median at grey 175, pressed into the top quarter of the ladder — the
exact "squeezed into 126–239" mechanism — while the body window puts the body's own percentiles on the
ladder's anchors by construction, at every angle.

## 4. The card's R² is NOT an air artifact — that part of the worry reverses

Recomputed on the same 335 calibration pairs the Elekta card was scored on:

| region | n | median R² | p10 | min |
|---|---|---|---|---|
| card as published (its own field) | 335 | 0.977 | 0.933 | 0.727 |
| fitted region, recomputed | 335 | 0.979 | 0.941 | 0.727 |
| **body pixels only (attenuation ≥ 0.25)** | 335 | **0.976** | 0.935 | 0.727 |
| air pixels only | 87* | 0.050 | 0.006 | 0.002 |
| full field | 335 | 0.980 | 0.949 | 0.844 |

*88 % of air-only rows have too few air pixels to score; n is frames with enough.

Body-only R² 0.976 vs full-field 0.980: **the fit is genuinely good over anatomy**; flat air adds almost
nothing (it has no variance to explain — alone it scores 0.05). The R² 0.979 in Figure 4 survives. What was
wrong with Figure 4a was the pick (a half-fan lateral flank frame) and the display window, not the fit. The
Ljubljana panel is the same display defect on a small specimen in a large black canvas.

## 5. Look at them

`strips/strip_{A,B}_{ap,obl45,lat}.png`, exported | body-window, cases B140 and A053 (test split), looked at
frame by frame 2026-09-23:

- **B140 AP** (1.9°, air 0.07): proper pelvis radiograph in both; near identical.
- **B140 45°** (air 0.18): exported milky; body window resolves lumbar bodies, endplates, hip.
- **B140 lateral** (89.8°, air 0.17): exported washed out; body window recovers the spine profile at the
  panel edge and the marker plate.
- **A053 AP** (0.2°, air 0.002): both fine — where there is no air, the two windows coincide.
- **A053 45°** (air 0.20): body window clearly better (acetabulum, sacrum readable).
- **A053 lateral** (89.6°, air 0.52): exported is an unreadable white slab; body window recovers the flank
  anatomy. This is the frame class Greg complained about; its second truth box has visible_frac 0.54 — the
  spine is beyond the panel, and no window puts it back.

## The fix, and what must be re-run

1. `tools/realxray_cobra_export.py --window-region body` (attenuation ≥ 0.25 inside the field; falls back to
   the field window below a 2,000-px floor, stated in the meta) → **`realxray/cobra_elekta_v3`**, a new
   directory; v1, which arms trained on, is untouched. Submitted: `slurm/realxray_cobra_export_v3.sh`.
2. `tools/realxray_eval.py --min-vis` (ignore-region handling as above). Every Elekta detection number in
   Figure 3 and the learning curve's Elekta arm must be rescored on v3 with `--min-vis 0.75`, and Figure 4a
   re-picked from an AP or a full-fan frame. Those numbers do not exist yet; nothing here is quotable in
   their place.
3. The Elekta card refit (A32, array 40418162) is independent of this: the window is display-only and the
   refit's loss works in attenuation, not grey.
