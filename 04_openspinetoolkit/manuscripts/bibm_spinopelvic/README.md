# BIBM wrap-up paper — "From Segmented CT to Spinopelvic Measurement"

One paper covering everything built **on top of** CTSpinoPelvic1K (the descriptor itself
stays at MLHC): the geometric spinopelvic engine (OpenSpineToolkit), the CT→radiograph
bridge (2D port + label-carrying DRRs / XRSpinoPelvic1K), and the deployable NiiVue viewer.
Target: **BIBM §6.d** (Biomedical Image Analysis) / §6.n (Clinical Decision Support).

## Files
- `main.tex` — full draft (IEEEtran conference). Honest scope is baked in; `\TODO{}` marks
  the few things to drop in.
- `tools/cohort_stats.py` — fills Table 1 from an OpenSpineToolkit summary CSV.

## To finish (the `\TODO`s), in priority order
1. **Table 1 numbers** (the one real result):
   ```bash
   python -m ostk all --labels <CTSpinoPelvic1K v4 labels> --out summary.csv --workers 8
   python tools/cohort_stats.py summary.csv      # paste mean±SD / range / valid-rate + QC %
   ```
2. **Two figures**: (a) a rendered lateral DRR + projected level labels (from the
   XRSpinoPelvic1K example case `0003`); (b) a viewer screenshot with an animated angle +
   the report panel (https://openspineconsortium.com/pacs/).
3. **2D–3D ε**: read the tolerance asserted in OpenSpineToolkit `test_metrics2d.py`.
4. **Citations**: a DRR reference; the CTSpinoPelvic1K descriptor id once known; repo URLs.

## Compile
Overleaf → IEEE BIBM template (`\documentclass[conference]{IEEEtran}`), drop in `main.tex`.

## DO NOT overclaim (already enforced in the text)
- No trained XR localizer (framework only); no full 1k XR release yet (pipeline + example);
  no AR; no live dual-engine swap (contract designed); post-op synthesis is a prototype;
  SS/PT/LL on supine CT are surrogates; PI is posture-invariant; SVA/TPA out of scope;
  manual-measurement validation is ongoing (next step).
