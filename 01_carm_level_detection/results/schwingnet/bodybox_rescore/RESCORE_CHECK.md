# Adversarial check of the A28 body-box rescore

Date 2026-09-23. Checked: `rescore.json` (69 rows), `RESCORE.md`, the grid outputs of job 40419582
(mirrored in `grid/`), and the raw dumps and truth banks on the grid. Every re-derivation below is an
**independent implementation** (own IoU, own greedy matching, own case-clustered bootstrap; no import of
`tools/lcurve_score.py` or `tools/rigor_fixes.py`), run as grid jobs 40419699/40419717/40419728 from
`/rs/rs_grp_oschome/go2432/data/or_ready/bodybox_rescore/check/rescore_check_verify.py`; machine output in
`RESCORE_CHECK_rederivation.json` here. Conventions as in RESCORE.md: WV = whole-vertebra outline, BODY =
SPINEPS vertebral body.

## Item 1 — three rows re-derived independently from the raw score files: PASS (one flag on A1)

**Row C_cobra_ar_pooled_real (computed; the headline COBRA control).** From the raw dump
`or_ready/lodo/sweeps/pooled__cobra_test.json` plus the two truth banks, nothing read from the scored files:

| quantity | rescore.json | my re-derivation | verdict |
|---|---|---|---|
| BODY 0.74 | 35.8 % (306/855) [29.5, 42.0] | 35.79 % (306/855), CI seed0 [29.52, 42.05], seed1234 [29.85, 42.43] | exact |
| BODY 0.25 | 36.3 % (310/855) [30.1, 42.3] | 36.26 % (310/855) [30.10, 42.28] | exact |
| WV 0.74 | 93.2 % (832/893) [86.4, 97.7] | 93.17 % (832/893) [86.43, 97.74] | exact |
| WV 0.25 | 97.4 % (870/893) [93.3, 99.8] | 97.42 % (870/893) [93.26, 99.78] | exact |
| WV on the 855 body subset, 0.74 | 93.7 % (801/855) | 93.68 % (801/855) [86.92, 98.28] | exact |
| WV on the 855 body subset, 0.25 | 97.8 % (836/855) | 97.78 % (836/855) | exact |

Per-case truth counts also reproduce the job log exactly (D152 = 0 body boxes, A280 48, B005 89, C042 64,
B131 43; 855 = 893 − 22 body_too_small − 16 visible_frac).

**Row F3 (computed; COBRA counting on body truth).** Recounted from the 648 per-frame records of
`grid/counting/lodo_cobra__cobra_test__bodytruth__0.25.json`, ignoring the pooled block: frames with a truth
sacrum 609, defined 111, matched bodies 45, ordinal-correct 25 (55.6 %), within-one 44/45, truth bodies 855 —
all exact. My own case-clustered bootstrap of 25/45: seed0 [28.2, 71.6], seed1234 [28.6, 71.7] against the
quoted [28.6, 72.5] — agreement within bootstrap noise (my cluster list holds the 25 cases with defined
frames; theirs all 27, which only perturbs the resample distribution). The 0.74 file likewise reproduces
F3_0.74: 5/11, defined 22/609, within-one 9/11.

**Row A1 (stored; the 80.5 % headline).** From the raw dump `or_ready/lodo/sweeps/lodo_carm__carm_test.json`
against `realxray/carmlspine/meta`: on 55 of 56 frames the stored numbers reproduce exactly — outline 231 and
body 14 of 281, and the stored file's own blocks (a1.json `cross_device_0.74`) carry WV 231/287 [74.08, 86.76]
and BODY 15/287 [2.41, 8.48], which `rescore.json` transcribes correctly. **Flag:** the 56th frame is the one
the dump calls `case118_LAT`; its meta was renamed `case118_OBL` and **re-posed on 2026-09-23** (the oblique
repair, `tools/carmlspine_pose.py`) — after a1.json was computed (2026-09-22 21:12). Against today's truth the
same dump reads **WV 236/287 = 82.2 % and BODY 14/287 = 4.9 % at 0.74** (old truth: 0 outline + 1 body match
on that frame; repaired truth: 5 outline + 0 body). So every A-row and C-ArmLSpine number quoted from files
computed before the repair is stale by one frame (~1.7 pp WV at 0.74). This is drift of the truth bank after
the freeze, not an error in the rescore; it belongs on the fix list beside the stale-citation-path items.

## Item 2 — the two conventions genuinely differ where the table claims they do: PASS

- Direct box comparison, COBRA: each of the 855 body-truth boxes paired to the released WV box of the same
  level in the same frame — IoU median 0.4996, p90 0.648, max 0.840, **none ≥ 0.9** (and `truth_check` in the
  counting file independently reports 855/855 below its 0.9 check). The body bank is not a relabelled copy of
  the WV bank, yet level identity is kept (0 unpaired).
- C-ArmLSpine meta: IoU(body `box`, `outline_box`) median 0.4159, only 6/281 ≥ 0.9.
- Where the table claims a difference, the raw counts differ (306 vs 832; 15 vs 231; 45 matched vs 76); where
  it claims "unchanged" (sacrum rows A1s/A2s/A3s, B1), the stored sacrum body and outline blocks are
  bit-identical in a1.json, as expected since the sacrum keeps one box in both conventions.
- The conventions genuinely cross: arms trained on real C-arm frames score body ≫ WV on C-ArmLSpine and
  WV ≫ body on COBRA, in both my re-derivations and the stored cells.

## Item 3 — denominators and case-clustered intervals: PASS

- Bootstrap code read end to end: `tools/rigor_fixes.ratio_ci` → `tools/stats_compare._boot_ratios` resamples
  **clusters** (`rng.integers(0, C, (n_boot, C))`, ratio of sums), N_BOOT=2000, SEED=0, percentile + BCa;
  `lcurve_score.rows()` aggregates per **case** before the bootstrap, and the counting tool pools per case the
  same way. DeepFluoro's one-specimen exception is handled by refusing a cluster interval (`C < 2`).
- Every scored COBRA file declares `bootstrap: {cluster: case, n_boot: 2000, seed: 0}` and 27 clusters; my own
  independent bootstrap reproduces the quoted percentile CIs to 0.1 pp at seed 0 and stays within ~0.5 pp at a
  different seed.
- Denominators: 287 (C-ArmLSpine vertebrae, 56 frames, 28 cases), 893 WV / 855 BODY (COBRA test, 648 frames,
  27 cases), 609 sacrum frames, 45/14 matched bodies, 111/609 defined — all recounted from raw records and
  correct, and each rescore.json row carries both k and n. D5/D6's body column openly states it has no paired
  interval (derived difference) — acceptable and declared.

## Item 4 — no row silently reuses a whole-vertebra truth bank: PASS

- All 32 `scored_body/*.json` are pinned to `bodybox_rescore/truth/cobra_elekta/meta` with truth_mode=body,
  855 truth vertebrae, 0 missing meta; all 32 `scored_wv/*.json` are pinned to the released
  `realxray/cobra_elekta/meta` with 893. The wrapper (`bin/bodybox_rescore_score.py`) overrides the meta
  lookup precisely because `lcurve_score` would otherwise silently fall back to the released meta beside the
  images — the override is present and the 855/0-missing outputs prove it took effect.
- The known trap was handled, not repeated: the stored fig3 COBRA files carry only a `body` block that is in
  fact WV (`truth_vertebrae` 893, `has_outline_truth` false — confirmed in `fig3_detection/scored/`), and the
  rescore rows E2/E3 take those stored numbers as the WV column and put the genuine 855-denominator body
  values from job 40419582 beside them.
- Row-to-file mapping spot-checked: C1 = lcurve `points[0]` (`at` body 36/287, `alt/outline` WV 181/287 —
  the "stale citation path" claim is true as stated); C_cobra_stage1 = `dc_B_held_elekta_xvi` (90/893, 11/855);
  C_cobra_N48_s0 = `lc_elekta_xvi_N50_s0` (220/893, 104/855); C_cobra_N408_s1 = `lc_elekta_xvi_N400_s1`
  (406/893, 75/855); "renders + all real" = `dc_P_pooled` (842/893, 344/855) = J2; F1/F2 = the four
  `counting/lodo_carm__carm_test__{body,outline}__{0.74,0.25}.json` cells (188/197, 13/14, 199/235, 11/14);
  C_ar_* = lcurve `all_real` (241/258/116/119, 235/260/115/117, 244/257/111/112); D7 = `seed_spread`
  (body held-out 21.6 vs 14.3 = 7.3 pp; outline 4.2; COBRA ~1.1; DF 3.3–5.6). All agree.

## Observations (not failures)

1. **Eight scorings failed and RESCORE.md does not mention it.** `failures.txt` lists the four `ends__*`
   dumps (body and wv modes) that crashed in `lcurve_score.load` — they are summary-only dumps (`frames` is an
   int), so they could never be rescored. No quoted row depends on them: every rescore.json value maps to a
   succeeded sweeps/lcdumps/devcorpus scored file (the mapping above). Worth one line in RESCORE.md.
2. **The A-row staleness flag from Item 1**: a1/a3 (and any other C-ArmLSpine file scored before 2026-09-23)
   predate the case118 oblique repair; at 0.74 the WV headline moves 80.5 → 82.2 % and BODY 5.2 → 4.9 % on
   re-run. The rescore's "stored" columns transcribe the frozen files correctly; the manuscript numbers those
   files feed inherit the drift.

## Verdict

| item | result |
|---|---|
| 1. three rows re-derived from raw files | **PASS** (A1 exact vs its frozen truth; flagged 1-frame truth drift dated 2026-09-23) |
| 2. conventions genuinely differ where claimed | **PASS** |
| 3. denominators + case-clustered 2,000-resample intervals | **PASS** |
| 4. no silent whole-vertebra truth reuse | **PASS** |

Evidence: `RESCORE_CHECK_rederivation.json` (this dir), grid `or_ready/bodybox_rescore/check/`
(`rescore_check_verify.py`, `verify_out.json`, logs for jobs 40419699/40419717/40419728).
