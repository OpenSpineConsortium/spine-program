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

| detector | gate | conf | body recall (n) | sacrum recall (n) |
|---|---|---|---|---|
| cov_surgio_b51_dr_low_s0 | held out | 0.25 | 7.8% (1204) | 0.0% (0) |
| cov_surgio_b51_dr_low_s0 | held out | 0.74 | 0.0% (1204) | 0.0% (0) |

## Per-bin body recall at conf 0.25, real spin vs styled render sweep

Render column: none drawn (REFUSED: /rs/rs_grp_oschome/go2432/data/or_ready/arc/recall_vs_angle_unseen/recall_vs_angle.json: UnverifiedDump: eval_gate: tools/case134_sweep.py score <- render curve /rs/rs_grp_oschome/go2432/data/or_ready/arc/recall_vs_angle_unseen/recall_vs_angle.json: (in memory): check 0 ('/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt') records no evaluation keys and digest (written ).

### cov_surgio_b51_dr_low_s0 (held out)

| lat bin | n | real-spin recall | render recall (nearest lat) |
|---|---|---|---|
| [-130°, -120°) | 28 | 0.036 | — |
| [-120°, -110°) | 48 | 0.000 | — |
| [-110°, -100°) | 72 | 0.028 | — |
| [-100°, -90°) | 68 | 0.044 | — |
| [-90°, -80°) | 72 | 0.069 | — |
| [-80°, -70°) | 68 | 0.059 | — |
| [-70°, -60°) | 64 | 0.016 | — |
| [-60°, -50°) | 68 | 0.015 | — |
| [-50°, -40°) | 68 | 0.000 | — |
| [-40°, -30°) | 64 | 0.078 | — |
| [-30°, -20°) | 68 | 0.206 | — |
| [-20°, -10°) | 64 | 0.094 | — |
| [-10°, +0°) | 68 | 0.029 | — |
| [+0°, +10°) | 68 | 0.015 | — |
| [+10°, +20°) | 64 | 0.219 | — |
| [+20°, +30°) | 68 | 0.132 | — |
| [+30°, +40°) | 68 | 0.044 | — |
| [+40°, +50°) | 64 | 0.266 | — |
| [+50°, +60°) | 52 | 0.115 | — |

## Contamination

- **cov_surgio_b51_dr_low_s0**: held out: case134 is in no train or val set of these weights or their initialisation chain

Render-curve comparison: REFUSED: /rs/rs_grp_oschome/go2432/data/or_ready/arc/recall_vs_angle_unseen/recall_vs_angle.json: UnverifiedDump: eval_gate: tools/case134_sweep.py score <- render curve /rs/rs_grp_oschome/go2432/data/or_ready/arc/recall_vs_angle_unseen/recall_vs_angle.json: (in memory): check 0 ('/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt') records no evaluation keys and digest (written 

