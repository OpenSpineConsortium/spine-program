# Open gate 40438004 -- record for paper 2 (NOT paper 1)

Released 2026-09-24T21:56:12Z (RELEASE_OPEN_GATE.json), ran 2026-09-25 04:22-06:02Z (1 h 40 on a GPU node), F6EVAL_END gate=open.
Scope: ordinary-stratum G3 test persons only (T1 renders 42 persons / 248 frames; T2 COBRA 32 persons / 768 frames;
T3 C-ArmLSpine 10 persons / 20 frames). No transitional stratum was scored; the blinded gate 40438005 stays held.

**Paper 1 never prints anything from this directory** (SchwingNet/PAPER1_SCOPE.md). If paper 2 uses the ordinary
stratum (H6, non-inferiority within 5 points), its ledger must record that the open gate was seen on 2026-09-25 before
the blinded unblinding.

## What was written

- `RUN_CONFIG_open.json`, `AUTO_REFERENCE_USED_open.json`, `truth_join_open.json` (the s14 reference join: T1 42 persons
  with release truth; T2 -- 103 COBRA test persons have no automated reference; T3 13 persons, none), the job log.
- Per head (6 heads: lam0 seeds 0-2, lam1.0 seeds 0-2): `fig6_score_open_harvest.json` + `fig6_bodies_open_harvest.csv`
  -- the HARVEST-name scores (SPINEPS+VERIDAH / CBCT labellers), labelled secondary, not a reference standard.
  The primary head's copy is here (`fig6_score_open_harvest.json`, 3.7 MB).

## Defect to fix before paper 2 scores anything

The REFERENCE-standard score (`fig6_score_open.json`) was **not written for any head**: the scorer looked for the truth
meta of the wrong gate -- log lines 46/75/103/131/159/187:
`no truth meta .../sets_v2/T1/blinded/meta_ref/ctsp_0005_ap_p0.json (run fig6_truth_join.py for this gate first)`.
`fig6_score.py --truth-join` (or its `--meta-subdir meta_ref` path resolution) reads `T1/blinded/meta_ref/` while the open
gate's join wrote `T1/open/meta_ref/`. Fix the gate-aware path in SchwingNet/tools/fig6_score.py, then re-score the
existing open-gate prototype dumps (no model re-run needed: `eval_v2_g3/<head>/<set>/open/<variant>/proto/` are on disk).

## Harvest-name summary lines from the log (per head, per set; persons, not frames)

lam0 s0 / s1 / s2 and lam1.0 s0 / s1 / s2 -- T3 ordinary (10 persons): network 6-8/10, count 9/10, coupled 9/10;
T1 render ordinary (3): network 3/3, count 1/3, coupled 1/3; T2 ordinary (4 with harvest names in the draw): network 1/4,
count 2/4, coupled 2/4; "draws: primary 24 persons, T1 42". These are small-n harvest-name numbers; paper 2 interprets
them after the reference scoring exists.
