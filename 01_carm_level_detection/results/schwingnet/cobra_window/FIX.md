# A31 fix: the display window's field, and the half-fan truth accounting

2026-09-23. The diagnosis is `DIAGNOSIS.md` in this directory (computed over all 3,480 exported cobra_elekta
frames of 150 cases); this file records what was changed, where the same defect lived elsewhere, and what is
still gated on grid jobs. Greg's complaint (07:20): the Elekta XVI and Ljubljana renders in fig4_formation
"look like shit". Two defects, neither in the formation model:

1. **The window's field included air.** `deepfluoro_anchor.window_or` maps attenuation percentiles
   1/5/50/95/99 over `field` onto grey 27/47/126/216/239; the COBRA export passed `field` = every pixel with
   signal, which on a half-fan lateral is up to 57 % air (median air share 0.071 AP over 542 frames, 0.152
   oblique over 2,207, 0.258 lateral over 731). Air collapsed p1/p5 and squeezed the body into grey 126–239
   (shipped lateral body p5/p50/p95 = 69/175/222).
2. **The eval charged off-panel truth as misses.** 864 of 1,502 test truth boxes carry `visible_frac` < 1
   (the offset half-fan panel sees a 56.8 mm band on its short side at the isocentre, median over 150 cases);
   `realxray_eval.py` never read the field, so every partly visible box stood in the recall denominator.

## What changed (committed 7631a1c, and this commit)

**Export** — `tools/realxray_cobra_export.py --window-region body` (7631a1c): percentiles over attenuation
>= 0.25 inside the exposed field, falling back to the field when the body region is under
max(2000 px, 2 % of the field); the region is stated in every frame's meta. The v1 bank the arms trained on
is untouched; the rebuild writes `realxray/cobra_elekta_v3` — same 150 cases, same 24 frames per case, same
splits, same truth and geometry. Export state at this writing: **150/150 case JSONs on disk**, finalize
(40418922) pending on the shards.

**Eval** — `tools/realxray_eval.py --min-vis` (7631a1c): truth boxes below the threshold become IGNORE — out
of the denominator, and predictions matching them are not false positives; `pooled.ignored_truth` reports the
count. Default 0.0 reproduces the old scoring. **The pre-existing visibility threshold is 0.5**: every
real-frame exporter keeps a truth box only when `visible_frac >= 0.5` (`MIN_VIS` in
`realxray_{cobra,deepfluoro,geneva}_export.py`; the keep rule in `docs/REAL_XRAY_DATASETS_SPEC.md`), so
`--min-vis 0.5` is scoring agreeing with the corpus's own stated rule, not a new number. The already-chained
rescore (40418931) sweeps {0.0, 0.75}; 0.75 ("at least three-quarters visible") was chosen in the diagnosis
and is kept as the sensitivity reading, and a follow-on job (40419583, `slurm/realxray_v3_eval_minvis05.sh`,
afterany:40418931) adds the 0.5 accounting for the same 3 detectors x {v1, v3}.

## The same defect, everywhere the grep found it (this commit)

Rule applied: change only where the window's field can include air; defaults preserve every shipped bank;
the 0.25 threshold is validated only on physical −log(I/I0) attenuation (the diagnosis's air/body split), so
exporters on a normalised scale say so and demand a LOOK before anyone ships a body-window bank.

| site | field today | includes air? | change |
|---|---|---|---|
| `tools/realxray_cobra_export.py` | every pixel with signal | yes, up to 57 % (lateral half-fan) | `--window-region body` (7631a1c); v3 uses it |
| `tools/realxray_deepfluoro_export.py` | exposed panel | yes (specimen edges; frames read as radiographs today) | `--window-region` added, default `field`; meta records the region; attenuation is normalised (p98−r)/(p98−p2), threshold unvalidated there — stated in the help |
| `tools/realxray_geneva_export.py` | intensifier circle | yes (air around the cadaveric hip) | same flag, default `field`; validated on the neg_log conv only — stated |
| `tools/carmlspine_labels.py` | central 7/8 rectangle | can (collimated border, flank air) | same flag, default `field` |
| `tools/spinesac_inventory.py` | largest exposed component | yes (sawbones in air) | same flag, default `field`; body applies only on the linear→−log conversion |
| `tools/device_style.py` (styled renders) | exposed field ∩ hit | yes (air beside the patient on oblique/lateral renders) | `style(..., window_region=)` param, default `field`; a styled set paired with cobra_elekta_v3 must pass `body` so real and styled get identical treatment |
| `tools/device_fit.py` `fig_pairs` (Figure 4 tiles) | field ∩ hit | yes — the Ljubljana turntable frame is a small specimen in a large exposed field | `DF_WINDOW_REGION=body` env opt-in, panels only; the region comes from the real frame and is applied to both tiles |
| `tools/device_fit.py` `display_from_images` (card statistics) | field ∩ hit | yes | **deliberately untouched**: the A32 refit (40418162, running) scores old and new cards under these statistics; changing the region mid-flight would break that comparability. Revisit after A32 lands. |

Shared helper: `deepfluoro_anchor.window_region_body(atten, field)` (returns region + description), the same
rule and guard the COBRA exporter inlines.

## (d) The card's R² over the body region — both numbers, refit nothing

Recomputed on the same 335 calibration pairs (`r2_body_vs_field.json`): median R² **0.976 body-only** vs
**0.980 full-field** (card as published, its own field: 0.977; air-only, on the 87 frames with >= 500 air
pixels in the model's support: 0.050). The fit was never an air artifact; Figure 4's R² 0.979 survives. The
Elekta card refit that IS pending (A10/A32) is for the noiseless-least-squares defect, not this.

## (e) Looked at

Before/after strips per view angle: `strips/strip_{A,B}_{ap,obl45,lat}.png` (two cases x three angles;
sources in `strips/strips.json`) plus the four-case, six-angle series in `../window_probe/` (A002, A004,
B013, C045 at frames 0000–0300). Verdict by eye: on laterals the field-window tile is a washed slab with
mid-grey air; the body-window tile has black air, a wider tissue span and readable cortical edges; the spine
stays off-panel on half-fan laterals because the offset panel physically does not see it — no window fixes
that, which is why Figure 4a must be re-picked from an AP/full-fan frame. AP tiles change modestly (7 %
median air). Two live v3 frames (A002 lateral 0178, AP 0089) were pulled and read as proper radiographs.

## (f) LANDED (40418931 + 40419583, 2026-09-23 14:00): the delta table

Same 648 test frames throughout; conf 0.25 (a1.json's "as quoted" operating point); vertebra recall, with the
sacrum in parentheses. **The min-vis 0.5 rows equal the min-vis 0.0 rows exactly and ignore zero boxes** — the
exporter's own MIN_VIS 0.5 keep rule already governs the shipped truth, so the corpus's stated accounting IS
the old accounting, and the "panel bias at the corpus's own rule" is zero by construction. Only the 0.75
sensitivity reading sheds boxes (893 → 764 vertebrae, 609 → 553 sacra).

| detector | v1 field window (baseline) | v3 body window (same truth) | window delta | v3 at min-vis 0.75 |
|---|---|---|---|---|
| render (never a real frame) | 338/893 = 37.8 % (188/609 = 30.9 %) | 373/893 = 41.8 % (186/609 = 30.5 %) | **+3.9 pts** | 325/764 = 42.5 % |
| lodo_cobra (COBRA never seen) | 165/893 = 18.5 % (81/609 = 13.3 %) | 190/893 = 21.3 % (82/609 = 13.5 %) | **+2.8 pts** | 173/764 = 22.6 % |
| pooled (COBRA in training) | 870/893 = 97.4 % (596/609 = 97.9 %) | 870/893 = 97.4 % (595/609 = 97.7 %) | 0.0 pts | 745/764 = 97.5 % |

Reading: the display window alone moves detectors that never saw a real Elekta frame by +3–4 recall points on
identical frames and truth; the arm trained on Elekta frames is indifferent to it. The 13:35 parallel
computation's pooled conf-0.74 numbers (832/893 = 93.2 %) are consistent and remain that computation's.
Source: /rs/rs_grp_oschome/go2432/data/or_ready/cobra_window/v3_eval/*.json.

## Figures rebuilt from this (2026-09-23, the REGENERATE pass)

Figure 4a: `SchwingNet/tools/fig4_pairs_pull.py` re-picks per device over the BODY-region R² (fit mask &
water-equivalent path > 5 mm) — Elekta from near-AP frames with the truth vertebrae inside the half-fan panel,
Ljubljana cropped to the specimen, both tiles displayed through the body-region window (grid job 40419698 →
or_ready/fig4_pairs_v2, pulled to results/fig4_pairs). Figure 3d: the COBRA example is re-picked from the v3
bank with every truth vertebra + sacrum at visible_frac >= 0.95 and the view angle stated on the tile
(`tools/fig3_example_cobra_v3.py`, jobs 40419692/40419701/40419719 → or_ready/fig3_detection_v3); all other
panels are unchanged.

## (superseded by the section above) Gated — nothing Elekta is quotable yet

The rescore is a scoring correction, not a retrain: 3 detectors (render, lodo_cobra, pooled) x {v1, v3} x
min-vis {0.0, 0.75} in 40418931, plus {0.5} in 40419583, all on the same test frames (648 frames, 893 truth
vertebrae, 609 sacra at min-vis 0). The baseline for the delta is each detector's own v1/min-vis-0.0 row —
the old accounting reproduced in the same run — scored at conf 0.25 (a1.json's "as quoted" operating point;
a1.json itself is the C-ArmLSpine held-out cell and holds no Elekta recall). The parallel 13:35 computation
over the same shards read pooled conf 0.74: 832/893 = 93.2 % vertebra recall, 333/349 = 95.4 % on
whole-panel truth, 45 of 61 misses off-panel — consistent with the diagnosis but not independently
recomputed here. When 40418931 + 40419583 land: re-pick Figure 4a, rebuild Figure 3d from v3 at the stated
threshold, rescore the learning curve's Elekta arm the same way.
