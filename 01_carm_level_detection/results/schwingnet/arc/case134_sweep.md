# case134 CBCT spin as a real oblique validation set

301-frame rotational acquisition of the intraoperative Surgio-B51 (the frames that reconstructed
the case's CBCT), poses from header geometry refined by bounded edge registration, vertebral-body and
sacrum boxes projected from the case's own CBCT masks (A28 convention).

**ONE patient, ONE acquisition (case134): no interval is valid on any number here**

Angle axis: lat_signed_deg (pose_arc convention: 0 = source posterior, -90 = the real Surgio lateral; the same axis as the styled render sweep).

Case134 has NO agreed level names (VERIDAH read C1-C5 on this lumbar CBCT), so this set scores
DETECTION only, never naming.

## Registration quality (per-frame values in each meta json)

- edge NCC over 301 frames: median 0.332 (q25 0.221, q75 0.456); 287/301 at >= 0.15, 204/301 at >= 0.25
- refined pose vs pure header start: rotation median 4.4 deg, source shift median 58.5 mm (bounds were 40/40/80 mm, 10 deg): the header angles alone are NOT an exact mapping; registration is what places each frame
- spin exposure vs the same case's spot shots: 111 kVp / 12 mA (spin) against 77-89 kVp / 25-26 mA (spots) -- a different exposure mode (carmlspine/sweep/HEADERS.md)

- label repair (sacrum_dropped): TS sacrum is a 1431-voxel fragment on this FOV-clipped CBCT (< 20000): its projected box is a sliver nowhere near the visible sacrum, so the set scores vertebral bodies only
- label repair (duplicate_corpus_instance): [['L1', 'L2']]

## Pooled recall over the whole spin

| detector | conf | body recall (n) | sacrum recall (n) |
|---|---|---|---|
| pooled | 0.25 | 93.6% (1204) | 0.0% (0) |
| pooled | 0.74 | 78.1% (1204) | 0.0% (0) |
| lodoA | 0.25 | 37.2% (1204) | 0.0% (0) |
| lodoA | 0.74 | 29.1% (1204) | 0.0% (0) |
| lodoB | 0.25 | 29.6% (1204) | 0.0% (0) |
| lodoB | 0.74 | 23.5% (1204) | 0.0% (0) |
| real_lodo | 0.25 | 49.5% (1204) | 0.0% (0) |
| real_lodo | 0.74 | 49.4% (1204) | 0.0% (0) |

## Per-bin body recall at conf 0.25, real spin vs styled render sweep

Render column: the SAME detector on the styled Surgio-geometry angle sweep (17 held-out TotalSegmentator
subjects, tilt 0, conf 0.25), at the render lat nearest the bin centre. The two columns share the angle
convention but not the patient, exposure or labeller, so read the SHAPE, not cellwise differences.

### pooled

| lat bin | n | real-spin recall | render recall (nearest lat) |
|---|---|---|---|
| [-130°, -120°) | 28 | 0.571 | — |
| [-120°, -110°) | 48 | 0.646 | — |
| [-110°, -100°) | 72 | 0.903 | — |
| [-100°, -90°) | 68 | 0.882 | 0.790 (at -90°) |
| [-90°, -80°) | 72 | 0.750 | 0.790 (at -90°) |
| [-80°, -70°) | 68 | 0.912 | 0.846 (at -80°) |
| [-70°, -60°) | 64 | 1.000 | 0.788 (at -70°) |
| [-60°, -50°) | 68 | 0.941 | 0.702 (at -60°) |
| [-50°, -40°) | 68 | 0.985 | 0.606 (at -50°) |
| [-40°, -30°) | 64 | 1.000 | 0.731 (at -40°) |
| [-30°, -20°) | 68 | 1.000 | 0.788 (at -30°) |
| [-20°, -10°) | 64 | 1.000 | 0.885 (at -20°) |
| [-10°, +0°) | 68 | 1.000 | 0.933 (at -10°) |
| [+0°, +10°) | 68 | 1.000 | 0.913 (at +0°) |
| [+10°, +20°) | 64 | 1.000 | 0.923 (at +10°) |
| [+20°, +30°) | 68 | 1.000 | 0.952 (at +20°) |
| [+30°, +40°) | 68 | 1.000 | 0.856 (at +30°) |
| [+40°, +50°) | 64 | 0.984 | 0.740 (at +40°) |
| [+50°, +60°) | 52 | 0.942 | 0.779 (at +50°) |

### lodoA

| lat bin | n | real-spin recall | render recall (nearest lat) |
|---|---|---|---|
| [-130°, -120°) | 28 | 0.500 | — |
| [-120°, -110°) | 48 | 0.333 | — |
| [-110°, -100°) | 72 | 0.125 | — |
| [-100°, -90°) | 68 | 0.191 | 0.210 (at -90°) |
| [-90°, -80°) | 72 | 0.083 | 0.210 (at -90°) |
| [-80°, -70°) | 68 | 0.176 | 0.183 (at -80°) |
| [-70°, -60°) | 64 | 0.203 | 0.154 (at -70°) |
| [-60°, -50°) | 68 | 0.382 | 0.135 (at -60°) |
| [-50°, -40°) | 68 | 0.471 | 0.163 (at -50°) |
| [-40°, -30°) | 64 | 0.406 | 0.240 (at -40°) |
| [-30°, -20°) | 68 | 0.426 | 0.317 (at -30°) |
| [-20°, -10°) | 64 | 0.391 | 0.385 (at -20°) |
| [-10°, +0°) | 68 | 0.515 | 0.212 (at -10°) |
| [+0°, +10°) | 68 | 0.588 | 0.260 (at +0°) |
| [+10°, +20°) | 64 | 0.500 | 0.269 (at +10°) |
| [+20°, +30°) | 68 | 0.412 | 0.240 (at +20°) |
| [+30°, +40°) | 68 | 0.500 | 0.346 (at +30°) |
| [+40°, +50°) | 64 | 0.500 | 0.250 (at +40°) |
| [+50°, +60°) | 52 | 0.500 | 0.154 (at +50°) |

### lodoB

| lat bin | n | real-spin recall | render recall (nearest lat) |
|---|---|---|---|
| [-130°, -120°) | 28 | 0.429 | — |
| [-120°, -110°) | 48 | 0.396 | — |
| [-110°, -100°) | 72 | 0.319 | — |
| [-100°, -90°) | 68 | 0.382 | 0.133 (at -90°) |
| [-90°, -80°) | 72 | 0.486 | 0.133 (at -90°) |
| [-80°, -70°) | 68 | 0.500 | 0.115 (at -80°) |
| [-70°, -60°) | 64 | 0.312 | 0.087 (at -70°) |
| [-60°, -50°) | 68 | 0.000 | 0.058 (at -60°) |
| [-50°, -40°) | 68 | 0.059 | 0.144 (at -50°) |
| [-40°, -30°) | 64 | 0.016 | 0.269 (at -40°) |
| [-30°, -20°) | 68 | 0.235 | 0.356 (at -30°) |
| [-20°, -10°) | 64 | 0.203 | 0.423 (at -20°) |
| [-10°, +0°) | 68 | 0.265 | 0.346 (at -10°) |
| [+0°, +10°) | 68 | 0.397 | 0.404 (at +0°) |
| [+10°, +20°) | 64 | 0.328 | 0.423 (at +10°) |
| [+20°, +30°) | 68 | 0.235 | 0.279 (at +20°) |
| [+30°, +40°) | 68 | 0.309 | 0.442 (at +30°) |
| [+40°, +50°) | 64 | 0.406 | 0.240 (at +40°) |
| [+50°, +60°) | 52 | 0.481 | 0.144 (at +50°) |

### real_lodo

| lat bin | n | real-spin recall | render recall (nearest lat) |
|---|---|---|---|
| [-130°, -120°) | 28 | 0.500 | — |
| [-120°, -110°) | 48 | 0.500 | — |
| [-110°, -100°) | 72 | 0.500 | — |
| [-100°, -90°) | 68 | 0.500 | 0.038 (at -90°) |
| [-90°, -80°) | 72 | 0.500 | 0.038 (at -90°) |
| [-80°, -70°) | 68 | 0.500 | 0.000 (at -80°) |
| [-70°, -60°) | 64 | 0.484 | 0.000 (at -70°) |
| [-60°, -50°) | 68 | 0.500 | 0.010 (at -60°) |
| [-50°, -40°) | 68 | 0.471 | 0.010 (at -50°) |
| [-40°, -30°) | 64 | 0.438 | 0.000 (at -40°) |
| [-30°, -20°) | 68 | 0.500 | 0.000 (at -30°) |
| [-20°, -10°) | 64 | 0.500 | 0.000 (at -20°) |
| [-10°, +0°) | 68 | 0.515 | 0.000 (at -10°) |
| [+0°, +10°) | 68 | 0.500 | 0.000 (at +0°) |
| [+10°, +20°) | 64 | 0.500 | 0.000 (at +10°) |
| [+20°, +30°) | 68 | 0.500 | 0.000 (at +20°) |
| [+30°, +40°) | 68 | 0.500 | 0.000 (at +30°) |
| [+40°, +50°) | 64 | 0.500 | 0.000 (at +40°) |
| [+50°, +60°) | 52 | 0.500 | 0.000 (at +50°) |

## Contamination

- **pooled**: case134 is in the carmlspine TRAIN split (md5 bucket 3): the pooled detector saw this patient's two SPOT frames (AP, LAT) in training. The spin frames themselves were never trained on.
- **real_lodo**: clean: trained with no C-ArmLSpine at all
- **lodoA**: clean: Surgio held out
- **lodoB**: clean: Surgio held out

Render-curve comparison: /rs/rs_grp_oschome/go2432/data/devcorpus_arc/recall_vs_angle/recall_vs_angle.json

