# Sources for every cell of Table 3 (`tab_levelcheck.tex` / `tab_levelcheck.md`), written 2026-09-23

One file: **LCM** `SchwingNet/LEVELCHECK_MODEL.md`, added by commit ecae75f (2026-09-23 19:50:36 −0400, "Pre-specify
the LevelCheck comparator"); `git log --diff-filter=A --format='%H %cI' -- SchwingNet/LEVELCHECK_MODEL.md` is the
freeze timestamp. Every frozen cell below is a transcription; nothing is computed here. The owed column is
`\PENDING{G6}` until the G6 evaluator (`SchwingNet/tools/fig6_score.py`) writes its result.

| row | cell | value | LCM section → text |
|---|---|---|---|
| H1 | stratum, test, p0, n_min | at risk pooled, superiority, 82.2, 19 | §3 table row "At risk, pooled (H1)"; §5 n_min table (0.822 → 19); §11 JSON `hypotheses[0]` |
| | source | Peh 1999 coronal localiser, most favourable, all patients | §2 "A radiologist's planning read without a count from C2" (80.2 / 82.2 / 77.9 %); §3 row text |
| | range | 20.8 (10/48) to 100 | §2 Nakagawa table "Count-changing … 10/48 20.8"; §3 row "Literature range" |
| H2 | p0, n_min, source | 97.6, 152, Manbachi 2018 Study 1 median of five, 62 films, no interval | §2 "The published surgeon + LevelCheck accuracy: 97.6 %"; §5 (0.976 → 152); §11 `hypotheses[1]` |
| H3 | range | 17.6 (6/34) | §2 Nakagawa "Lumbarised S1 (six lumbar) 6/34 17.6"; §3 row H3 |
| H4 | range | 28.6 (4/14) | §2 Nakagawa "Sacralised L5, type III 4/14 28.6"; §3 row H4 |
| H5 | source; range | borrowed from H1; 31 (31/100) | §3 row H5; §2 "Thoracolumbar variants. Yun 2018" |
| H6 | test, p0, margin, n_min, range | non-inferiority, 92.6 = 97.6 − 5, margin chosen knowing development accuracy (§8), 48, 97.6 to 100 (Manbachi OR 20/20) | §3 row H6; §5 (0.926 → 48); §2 "The operating-room series: 20 of 20" |
| naming unaffected | test; range | descriptive; 97.6–100, Nakagawa sacralisation II 23/23 | §3 last row; §2 Nakagawa table |
| footnote (a) | model; r | r(1 − e); r = 1.0, published 0.993–1.000 | §1 "The model"; §2 "Registration success, r" (Lo 2015 99.3 % at 50 multistarts, 100 % at 200) |
| | seen before the freeze | ordinary development results; three C-ArmLSpine L6; render L6 recall 56.1–72.4 %; all transitional below 82.2 % | §8 items 1–3 and its closing sentence |
| footnote (b) | strata | at risk (conventions i and ii); naming unaffected list; three C-ArmLSpine L6 excluded in advance | §3 "At risk" and "It does not flag"; §4 "Excluded from the primary analysis in advance" |
| footnote (c) | unit, draw, correct, configuration, test, multiplicity | person; ≥ 4 reference-named bodies, `numpy.random.default_rng(20260923)`; every body named; held-out-transitional arm, coupled, 0.74, whole frame, seed 0; one-sided exact binomial; Holm at 0.025 | §4, §5, §11 |
| footnote (d) | eligibility | n_min, P ≤ 0.025 at n of n | §5 "Eligibility" |
| md twin only | Holm-step n_min; power; H2 at 152 | 23/25/28, 57/63/72, 181/198/226; 0.27/0.82/0.97 at n = 60; 0.22 | §5 table; §7 first table (n = 60 row); §7 "H2 against 0.976" |

References cited in the table: `peh1999`, `nakagawa2017`, `manbachi2018`, `yun2018`, `levelcheck2012` (Otake 2012),
`levelcheck2016` (Lo 2015). Peh 1999 and Yun 2018 were added to `SchwingNet/refs.bib` on 2026-09-23 from PubMed
E-utilities (PMIDs 10488518, 30386145); they are not yet in `paper/rsnai/refs.bib`, the source `tools/make_refs.py`
copies from.

Footnote c, added 2026-09-24: the scored arm's encoder trains from ImageNet weights on the G3 training persons (`results/fig6/RUN_v2.json`, jobs.encoder: "encoder refuses without READY or without ImageNet weights"); the reference-standard sentence is `LEVELCHECK_MODEL.md` §4 (reference standard) and §14 R1-R3 (automated reference, commit b511985, 2026-09-24T05:29:51-04:00); the secondary analyses are §12 (commit 1897772, 2026-09-23T20:50:41-04:00) and §13 (commit 2993f40, 2026-09-23T20:58:29-04:00).
