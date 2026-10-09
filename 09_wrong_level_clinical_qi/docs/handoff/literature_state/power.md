# Topic 4: power and sample size, per comparison the programme makes or plans

Written 2026-10-08 from files on this laptop only (no grid, no network). Every cell names the file it comes from.
A study's n or result taken from a prior report is marked "as recorded in" that report and was not re-verified.
Where no file holds a calculation, the cell says so and lists what a student would need. Where this note did its
own arithmetic, the cell says **calc**. That arithmetic uses the repository's own code, copied verbatim:
the exact-binomial functions of `LCM` section 11 and the two-proportion functions of `ssn:tools/stats_compare.py`.
The script is `scratchpad/litstate/power_calc.py`, and its output is `scratchpad/litstate/power_calc.json`. Where a
file states the same quantity, calc reproduces it (checks in section 7).

## Citation keys

| key | path |
|---|---|
| `ssn:` | `<spinesurg-ct-nnunet 097933a>/` |
| `sn:` | `ssn:SchwingNet/` |
| `ctsp:` | `<CTSpinoPelvic1K 7ddfe38>/` |
| `mem:` | `<the memory folder; copies in memory/ of this project, statuses in docs/handoff/context/INDEX.md>/` |
| `LCM` | `sn:LEVELCHECK_MODEL.md` (the frozen paper-2 comparator; section numbers as §) |
| `PJ` | `sn:results/power/power.json` (Figure 5; `sn:tools/fig_power.py`, generated 2026-09-25 13:41) |
| `PT` | `sn:results/power_table.json` (`sn:tools/fig_claim.py`) |
| `SR1` | `sn:results/stats_review/recompute.json` (first statistical review) |
| `SR2` | `sn:results/stats_review2/recompute.json` (second statistical review, 2026-09-24) |
| `RS1`, `RS2` | `sn:REVIEW_STATS.md`, `sn:REVIEW2_STATS.md` |
| `T2` | `sn:tables/tab4_transitional.md` (paper 1 Table 2, transitional persons by subtype) |
| `NUM` | `sn:NUMBERS.md` (line numbers as `NUM:n`) |
| `FITN` | `sn:results/indomain/FIT_N.md` (Figueroa inverse-power-law fits, 2026-09-24) |
| `ABL` | `sn:results/coverage/film_ncurve/ablation/READ.md` (render rows against film only) |
| `FP` | `ssn:docs/FLAGSHIP_PLAN.md` (gates G0 to G7) |
| `AP` | `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| `RANK` | `sn:results/transitional_registry/acquisition/ranking.csv` |
| `FOV` | `sn:results/transitional_registry/acquisition/fov_calibration.json` |
| `CEN` | `ssn:docs/CENSUS_TABLE_2026-09-25.md` |
| `REG` | `sn:results/transitional_registry/REGISTRY.md` (built 2026-09-24 11:07) |
| `TIERS` | `ssn:docs/ruleclass/TIERS.md` (ruleclass census, 2026-09-27) |
| `COBS` | `sn:results/power/inputs/cobra_lstv_screen.grid.md` (COBRA2026 one-labeller screen, 2026-09-23) |
| `RATIO` | `ssn:reports/Synthetic real ratio X-ray detectors.md` (deep research report, 2026-09-23) |
| `ART` | `ctsp:paper/mpda/main.tex` (the CTSpinoPelvic1K dataset article; line numbers as `ART:n`) |
| `RES22` | `ssn:docs/RESUME_2026-09-22_PM.md` |
| `calc` | this note's arithmetic, `scratchpad/litstate/power_calc.py` |

---

## 1. Every power or sample-size calculation found on disk

Searched with grep for power, sample size, n_min, underpowered and 80 % power across `sn:results`, `ssn:docs`,
`ssn:tools`, `sn:tools`, `ssn:paper`, `ssn:reports`, `ssn:research_notes` and `ctsp:docs`, `ctsp:paper/mpda`.
Hits for "power law", tube power and PowerShell are excluded.

| # | file | what it computes | test, alpha | true accuracy or effect assumed, and where that comes from | result as the file states it |
|---|---|---|---|---|---|
| 1 | `PT` | Wilson 95 % lower bound by errors k and test persons n | Wilson score interval, z 1.959964 | none (bounds, not power) | 0 errors: 88.65 % at 30, 92.13 at 45, 93.98 at 60, 96.3 at 100 (`PT` lower_bound_pct_by_k_then_n). Its inventory (89 persons, 37 test persons, bound 90.59 %) is superseded (section 7, row 2) |
| 2 | `PJ` panel_a | smallest n at which the Wilson bound meets the pre-stated targets | Wilson | targets 90 % exact level and 85 % variant sensitivity, from `FP` G6 item 4 | 90 % bound: 35 / 53 / 69 / 113 persons at 0 / 1 / 2 / 5 errors; 85 % bound: 22 / 34 / 45 / 74 carriers (`PJ` crossings_n) |
| 3 | `SR1` R4_wilson | probability the Wilson target is met, and n for 80 % probability | Wilson | true 95, 97, 98, 99 %, planning values with no cited measurement (`SR1` R4; `RS1` F17) | 80 % power for the 90 % bound needs 99 persons at a true 97 % and 69 at 98 % (`SR1` smallest_n_for_80pct_power) |
| 4 | `LCM` §5, §7, §13 | n_min, power tables, break-even p*, accepted-person power for the LevelCheck comparison | one-sided exact binomial, alpha 0.025, Holm | true 90, 95, 97 % (§7); 99.0 to 99.9 % for accepted persons (§13); the transitional values are planning values, and §8 states that every transitional development measurement seen was below 82.2 % | §5: n_min 19 / 48 / 152 for p0 0.822 / 0.926 / 0.976; §7 and §13 tables (section 2 rows 11 to 15) |
| 5 | `SR2` S1 to S4, S9, S12 | independent recomputation of the paper-2 numbers; power at the development accuracies; H6 feasibility; COBRA call yield; comparator sampling error | as `LCM` | as `LCM`, plus the development accuracies 56.1 %, 72.4 %, 80 % (S2) | the printed powers, n_min and Wilson numbers reproduced (`RS2` verdict; `SR2` S1 agrees_with_power_json), with one exception found here (section 7, row 3); power cannot exceed 0.025 at any true accuracy at or below 0.822 (S2) |
| 6 | `RS2` N1, N8, N10, N11 | review of the power paragraph | as `LCM` | notes that the 95 % planning accuracy "no transitional measurement supports" (`RS2` N1) | as frozen, H1 and H6 "cannot pass as specified, however well the network names vertebrae" (`RS2` N1) |
| 7 | `RS1` F17 | review of the first sample-size paragraph | Wilson | as row 3 | "not a power calculation"; per subtype only the mobile L6 row can reach 22 carriers (`RS1` F17) |
| 8 | `FITN` | persons or frames needed to reach an accuracy target, from a fitted learning curve | Figueroa 2012 inverse power law, case-clustered bootstrap, 2,000 resamples | none; fitted to measured points | section 2 rows 2 and 3 |
| 9 | `ssn:tools/stats_compare.py` | two-proportion power, n per arm, minimum detectable difference, exact one-sample power, prospective arm planning | two-sided arcsine (Cohen's h) and exact binomial | supplied by the user at run time | tool only: no saved output of these subcommands was found (repository grep for their output keys returned nothing) |
| 10 | `AP` §2 to §3; `ssn:tools/acquisition_census.py` | expected transitional people per collection, and a stopping rule of 20 expected people per TB | expectation, not a test | prevalence priors (section 4) | tier 1: E_low 831, E_high 1,703, E_count 460; late tier 1: 163 / 336 / 91 (`AP` header table) |
| 11 | `CEN` | the same expectations per screened collection, beside what the screen called | expectation | as row 10 | section 4 |
| 12 | `ssn:paper/qi_universal_protocol/main.tex:229-231` | QI protocol on localisation | none | wrong-level events at 0.12 % | "powered to estimate, not to detect a change in wrong-level events, which at 0.12 % would need tens of thousands of cases" |
| 13 | `mem:selective-prediction-the-honest-99.md` | n to certify 99 % selective accuracy | one-sided 95 % confidence | zero errors | about 298 answered cases; class-conditional 99 % needs at least 99 real calibration cases per class, 2,673 at 27 classes (as recorded there) |
| 14 | `NUM:52` (marked SUPERSEDED 2026-09-24) | older Figure 5 panel b | exact binomial | planning accuracy 98.2 % (606/617) | 80 % power for the 90 % bound at 69; exceeding 97.6 % first at 4,276 |
| 15 | `ssn:tools/anomaly_cooccurrence_from_labels.py:3-6` | thoracolumbar and lumbosacral anomaly co-occurrence in CTSpinoPelvic1K | odds ratio | none | manifest odds ratio 4.00 (1.00 to 16.03) on a both-cell of two cases, "underpowered on its own" |
| 16 | `ssn:docs/MORNING_BRIEF_2026-09-16.md:79,123` | BUU label noise; 33 shifted films | none | none | "n=80, no power"; "no power" |
| 17 | `ssn:docs/FLUORO_DATASET_STRATEGY.md:177` | SyntheX parity reading | none | none | the landmark difference P = 0.14 is "an underpowered null" (as recorded there) |
| 18 | `ART` | the dataset article | none | none | no power calculation; the only mention is ART:919-921 "would test the co-occurrence ... at full power" |

---

## 2. Per comparison: effect assumed, n today, power today, n required

"First n" is the smallest n at which power reaches the level; exact-test power is sawtoothed in n, so `LCM` §13
and `SR2` also give the n from which it always holds, quoted here as "always from".

| # | comparison | effect size or true accuracy assumed, and its source | n available today, and its source | power at today's n | n for 80 % power | n for 90 % power |
|---|---|---|---|---|---|---|
| 1 | **Per-device accuracy difference, device level** (fitted nine-term card against uncalibrated physics) | no assumed effect in any file. Observed: card gain, frame-weighted mean 0.025 over 835 frames; all four device means positive (BV Pulsera 0.042, Cios Fusion 0.015, Elekta XVI 0.023, PIXIUM 4600 0.070) (`NUM:146`; `SR1` R2_card) | 4 devices, 24 folds (`NUM:146`) | no file computes it. Exact sign-flip over the four device means gives P 0.125, printed P = .13 (`NUM:146`). That is the smallest two-sided P four devices can give (2/2^4, **calc**), so power at alpha 0.05 is 0 whatever the effect. Fold level: P 0.00023 over 24 folds (`NUM:146`) | not computed in any file. **calc**: the exact sign-flip test can first reach two-sided P at or below 0.05 at 6 devices (2/2^6 = 0.031) | not computed in any file |
| 2 | **Per-device: same-device frames needed for detection** (C-ArmLSpine, body rule, confidence 0.74) | none assumed; fitted asymptote 81.7 % [76.7, 86.6] lateral and 85.3 % [81.0, 90.7] AP (`FITN`) | up to 200 real frames per arm, 28 test patients (`FITN`) | not a power calculation. 95 % of the asymptote is reached at 10.0 [5.1, 23.5] lateral and 11.9 [6.7, 33.5] AP frames; 90 % absolute recall "not reached" in 100 % (lateral) and 96 % (AP) of resamples (`FITN`) | not applicable (learning curve) | not applicable |
| 3 | **Per-device: same-device persons needed for naming** (C-ArmLSpine, whole frame) | none assumed; fitted (`FITN`) | 87 lateral, 87.6 AP training persons at N = all (`PJ` panel_b_carm) | not a power calculation. AP: N to 97 % = 67.6 persons [11.6, 669]; to 99 % = 1,071 [86.9, 74,458]. Lateral: N to 97 % = 12.1 [0.0, 7,580]; to 99 % = 1,064. Asymptote not identified on either view (`FITN`) | not applicable | not applicable |
| 4 | **LODO versus pooled** (held-out-device detector against same-device detector, sacrum found at 0.25) | none assumed. Observed: 98.2 % against 83.9 %, +14.3 points [5.4, 23.2] (`NUM:131`) | 28 C-ArmLSpine test cases; sign test 8 cases better, 0 worse (`NUM:131`). Real test devices: C-ArmLSpine 28 patients, COBRA2026 27, DeepFluoro 1 specimen (`mem:pooled-vs-lodo-device-designs.md`; DeepFluoro "one cluster", `NUM:303`) | no a priori power calculation. Holm-adjusted P printed 0.0078 (`NUM:131`); 0.016 once the card test is counted as the fourth member (`RS2` N9; `SR2` S8). **calc**: an exact sign test needs at least 6 discordant cases, all one way, for two-sided P at or below 0.05, and 8 for 0.0125 (the first Holm step over four) | not computed in any file; inputs: per-device discordant-case rate, cases per device | not computed |
| 5 | **Synthetic-to-real ratio** | none. No DRR or fluoroscopy paper has swept the ratio; the joint-mix window from other modalities is 4:1 to 10:1 (`RATIO` §1, as recorded there). The flagship fixes real frames at 10 to 20 % of the mix (`FP`, corpus section) | no ratio sweep has been run. The only in-house test is render rows against film only: +21.9 / +11.1 / +18.7 points at N = 5 persons and +12.2 / +6.0 / +6.2 at N = 25 (NHANES II / BUU-LSPINE / CSXA); level once every person is used; 3 seeds at N up to 25, 1 seed above (`ABL`) | no power calculation. 7 of 9 pre-stated cells separated outside the intervals (`ABL`) | no file. A student needs: the ratio grid, the real-frame N per arm, the between-seed SD per cell (in `ABL`), test persons per corpus, and the intraclass correlation of frames within a person | no file |
| 6 | **Transitional against ordinary levels** (does naming accuracy drop on transitional spines?) | none assumed. Observed (none quotable; marks added 2026-10-08 from `RESULTS_CATALOG.md`): film interior windows 91.8 % [89.4, 94.1] ordinary (455 films) against 66.0 % [39.6, 87.2] anomalous (12 films) (as recorded in `mem:feasibility-claims-measured.md`; RECORD ONLY [LEAK], C1.14); real C-ArmLSpine laterals: whole frame 98.2 %, L6 by the classifier 44.9 % (as recorded in `mem:two-mechanisms-thesis.md`; SUPERSEDED, C1.18 and A3.11; the current whole frame is 97.4 %, A3.1); render L6 recall 56.1 to 72.4 % on 10 held-out L6 spines ([SEL-SPLIT], `EVAL_LEAKS.md` item 6) (`LCM` §8 item 3; `sn:results/ALPHABET_LOSS.md`) | 10 L6 evidence persons on renders, 0 T13 (`sn:results/ALPHABET_LOSS.md`); 3 real L6 patients, excluded from the primary analysis (`LCM` §4) | no file computes it | no file. **calc** (two-sided alpha 0.05, Cohen's h, `stats_compare.n_two_proportions`): 91.8 against 66.0 % needs 36 per arm at design effect 1, 143 at design effect 4. Design effects of 3.84 to 4.47 were measured for lateral naming (`NUM:419`, `NUM:463`) | **calc**: 48 per arm at design effect 1, 191 at 4 |
| 7 | **Count against count plus morphology on transitional persons** (paper 2, M1) | none assumed. Development: coupled better than count on 3 cases, worse on 0, ties 127, sign P 0.25 (`SR2` S6; `RS2` N3) | none scored (paper 2 not unblinded; `sn:paper2_levelcheck/open_gate_40438004/README.md`) | not computed. The test runs only if at least 6 persons are discordant (`LCM` §12); **calc**: 6 discordant, all one way, is the fewest that can give one-sided P at or below 0.025 | no file; inputs: expected discordance rate among transitional persons | no file |
| 8 | **L6 detection** (variant sensitivity, Wilson lower bound at least 85 %) | true sensitivity 95 to 99 % in the planning tables (`SR1` R4), with no measurement behind it; development L6 recall 56.1 to 72.4 % on renders (`LCM` §8) | 43 CT test persons (`T2`), but 49 of 54 L6 validation and test persons sit in the current encoder's training lineage (`T2` note d); real frames: 3 C-ArmLSpine L6 excluded (`LCM` §4), 3 COBRA2026 two-labeller L6 with an exported frame (`NUM:435`) | at 43 carriers, one miss allowed: 0.36 / 0.63 / 0.79 / 0.93 at a true 95 / 97 / 98 / 99 % (**calc**). At the render recall of 72.4 %, P(22 of 22 found) = 0.0008 (**calc**); the bound cannot reach 85 % at any n | 22 carriers with no miss is the floor (`PJ`). **calc** first n: 74 (true 95 %), 45 (97 %), 34 (98 %), 22 (99 %); 347 at a true 90 %; never at 72.4 % | **calc**: 92 / 55 / 45 / 34; 461 at 90 % |
| 9 | **T13 detection** (same 85 % target) | as row 8; no T13 recall can be measured: "no validation film carries one" (`sn:results/ALPHABET_LOSS.md`) | 3 CT test persons, 0 real (`T2`); 7 T13 persons in all sources (`T2`), 14 in the registry (`REG` table A) | 0: below the 22-carrier floor (`PJ`); "the T13 row (6 persons) ... cannot [reach it], whatever the result" (`RS1` F17) | at least 22 carriers with no miss (`PJ`) | **calc**: as row 8 |
| 10 | **Paper 1 exact level** (Wilson lower bound at least 90 % on transitional test persons; `FP` G6 item 4) | true 95 to 99 % planning values (`SR1` R4); not supported by any transitional measurement (`RS2` N1) | 51 at-risk CT test persons, 36 rendered, most in the current encoder's training data (`NUM:436`; `T2`); 7 real at-risk persons by a two-labeller count with an exported frame (`NUM:435`); 0 verified real (`sn:sections/results.tex`, "Transitional sample size") | at 51 (no error allowed): 0.07 / 0.21 / 0.36 / 0.60 at a true 95 / 97 / 98 / 99 % (**calc**). At 7: 0, the best-case bound is 64.6 % (`NUM:435`) | 99 at a true 97 % and 69 at 98 % (`SR1` R4); **calc**: 217 at 95 %, 53 at 99 % | **calc**: 291 / 127 / 84 / 53 at 95 / 97 / 98 / 99 % |
| 11 | **LevelCheck H1** (paper 2: at-risk pooled, superiority over 82.2 %, Peh 1999 coronal localiser) | true 90 / 95 / 97 % (`LCM` §7), planning values | real frames are primary (`LCM` §4): 7 two-labeller at-risk persons (`NUM:435`), below n_min 19; 57 COBRA2026 screen calls supported by their field (`T2` note e), not verified; CT renders of 51 at-risk test persons are a secondary analysis (`LCM` §4; `NUM:436`) | at 7: 0 (ineligible; **calc**). P(at least 19 of the 57 calls confirmed) = 0.00007 at the labeller's CTSpinoPelvic1K PPV, 0.30 at its upper Wilson limits (`SR2` S4). At 51 CT persons: 0.24 / 0.75 / 0.93 / 0.998 at 90 / 95 / 97 / 99 % (**calc**). Expected endpoint accuracy with the frozen detectors about 0.14, so power 0 (`SR2` S12) | 162 (always from 175) at 90 %; 55 at 95 % (`SR2` S1); 71 at 95 % under the Holm alpha/3 step (`SR2` S1); **calc**: 38 at 97 % | **calc**: 208 (always from 228) at 90 %; 63 (always from 70) at 95 %; 47 at 97 % |
| 12 | **LevelCheck H2** (superiority over 97.6 %, Manbachi 2018 median of five surgeons) | true 95 / 99 % (`SR2` S1) | as row 11 | 0 below n = 152 at any true accuracy (`LCM` §13); maximum over n up to 2,000 is 0.00041 at a true 95 % (`SR2` S1) | 708 (always from 763) at a true 99 % (`SR2` S1); never at 98 % within 1,300 (**calc**) | 922 (always from 974) at a true 99 % (**calc**; the same figure `LCM` §13 gives for accepted persons at 0.990) |
| 13 | **LevelCheck H3 to H5** (per subtype against 82.2 %) | as row 11 | L6 43 CT test persons, sacralised L5 5, T13 3 (`T2`); real: L6 3, four-lumbar 4, T13 0 (`NUM:435`) | H4 and H5 are ineligible on every count (n below 19, `LCM` §5); H3 is ineligible on real frames | n_min 19 (23, 25, 28 at the Holm steps) (`LCM` §5) | as row 11 |
| 14 | **LevelCheck H6** (ordinary spines, non-inferiority, p0 92.6 % = 97.6 % minus a 5-point margin chosen knowing the development results) | true 95 / 97 / 98 / 99 % (`SR2` S3) | at most 51 ordinary real-frame test persons (COBRA2026 41, C-ArmLSpine 10) (`SR2` S3); of these only 13 reference-ordinary COBRA persons are in the open gate, and the 10 C-ArmLSpine persons have no reference (`RES22` lines 679-688); 103 COBRA test persons have no automated reference (`sn:paper2_levelcheck/open_gate_40438004/README.md`) | at 51: 0.07 / 0.21 / 0.36 / 0.60 (`SR2` S3). At 13: 0, below n_min 48 (**calc**) | **calc**: 210 (always from 245) at 97 %; 136 at 98 %; 73 (always from 95) at 99 % | **calc**: 262 (296) / 155 (173) / 95 (116) |
| 15 | **LevelCheck S1** (accepted-person accuracy against 97.6 %, selective) | true accuracy of accepted persons 99.9 / 99.5 / 99.0 % (`LCM` §13) | none scored | 0 below 152 accepted persons (`LCM` §13) | 152 (always from 230) / 299 (363) / 708 (763); against p0 0.97: 122, 239, 386 (`LCM` §13) | 230 / 424 / 922 (always from 974) (`LCM` §13) |

### What the endpoint does to every row from 10 to 15

The frozen endpoint scores a person wrong for a missed body, an unanchored frame or an abstention, not only for a
wrong name (`LCM` §4). On ordinary C-ArmLSpine development frames that endpoint held on 162 of 284 frames (57.0 %),
and naming failed on 1 (`SR2` S11). The COBRA2026 sacrum detector fixed for the primary analysis found the sacrum on
21 of 609 frames (3.4 %), with no anchored frame for 19 of 27 patients (`SR2` S12). `LCM` §15 replaced those
detectors with one trained on the G3 training side of every device before unblinding. No file recomputes the power
under the replacement detector.

---

## 3. Size against the studies each comparison leans on

| comparison | published study | its n, as recorded | this programme's n today |
|---|---|---|---|
| LevelCheck comparator | Manbachi 2018, Study 1 | 5 surgeons, 62 radiographs, 16 with deliberately shifted labels; no denominator or interval for 97.6 % (as recorded in `LCM` §2) | at-risk real-frame persons: 7 unverified (`NUM:435`) |
| LevelCheck comparator | Manbachi 2018, Study 2 | 20 operating-room patients, 20 of 20 correct (as recorded in `LCM` §2) | ordinary real-frame persons: at most 51, 13 with a reference (row 14) |
| LevelCheck registration | De Silva 2016; Lo 2015; Otake 2012 | 398 radiographs of 178 patients; 20 patients with 10,000 trials; 10 CTs with 50,000 simulated images (as recorded in `LCM` §2) | not applicable (SchwingNet does not register) |
| planning-read miscount | Nakagawa 2017; Peh 1999; Yun 2018; Albano 2024 | 71 LSTV of 550 operations; 129 patients with 17 LSTV; 100 variant patients of 1,446 CTs; 885 LSTV surgical patients over 39 studies (as recorded in `LCM` §2) | transitional persons in all sources: 194 (`T2`) |
| CT transitional labelling | VERIDAH | 1,171 training CTs with 60 thoracic- and 83 lumbar-enumeration anomalies; test 25 and 29 (as recorded in `RATIO`) | L6 persons 110, T13 7 (`T2`); registry L6 146, T13 14 (`REG` table A) |
| when L6 becomes learnable | VerSe'20 | L6 in 85 scans, T13 in 6; T13 "never stabilised" (as recorded in `RATIO`; `mem:lstv-data-landscape.md`) | L6 18 distinct CTSpinoPelvic1K cases gave L6 Dice 0.000 under 12-fold duplication (as recorded in `mem:l6-sample-count-and-counting-decoder.md`) |
| 2-D LSTV on film | Kwak 2025 | 3,116 lateral films, 313 test films, one surgeon reader (as recorded in `mem:lstv-data-landscape.md`) | no human-read transitional label on any released film (`ABL`, last line) |
| C-arm detection and naming | Rao 2024; VDVM (Zhang 2023); Huang 2022 | 578 C-arm images from 3 C-arms, recall 0.964, names nothing; 31 C-arm images, naming 73.3 %; 13 cadavers, 88.3 %, O-arm tomosynthesis (as recorded in `mem:registration-free-prior-art.md`) | C-ArmLSpine 617 lateral vertebrae in 141 cases, zero-shot and five-fold (`NUM:419`, `NUM:463`); device-held-out test 28 cases, 56 frames, 287 vertebrae (`NUM:123`); COBRA2026 held-out 27 patients, 609 frames (`SR2` S12) |
| synthetic and real mixing | Barr 2026; Gherardini 2020; SyntheX; DeepDRR | 100 to 700 real radiographs, 374 test; 240 real frames; 366 real images from 6 cadavers and 20 CTs; 20 CTs, 78 real cadaver images (as recorded in `RATIO` §1 to §2) | film N curves to 264 (NHANES II), 2,967 (BUU-LSPINE) and 4,114 (CSXA) persons (`PJ` panel_b_film); C-arm naming to 87 persons per view (`PJ` panel_b_carm) |
| prevalence priors | Hanhivaara 2020; Nardo 2012; Nagata 2025; Sun 2025; VertebralBodiesCT-Labels | 3,855 abdominal CTs; 4,636 films; 551 whole-spine CTs; 500 UK Biobank controls; 7 T13 of 1,088 TotalSegmentator scans (as recorded in `AP` §2 and `ssn:tools/acquisition_census.py:17-26`) | CTs in the ruleclass census: 21,622 (21,603 persons) (`TIERS` §1) |

---

## 4. What the prevalence literature implies for the CT holding, against the calls so far

The priors, as recorded in `ssn:tools/acquisition_census.py:17-26` and `AP` §2: numbering-relevant LSTV (Castellvi
II to IV) 9 % (Hanhivaara 2020) to 18 % (Nardo 2012; Nagata 2025 at 16.3 % falls inside); what a mask count can see
without a reader, 4.8 % = L6 3.2 % + four-lumbar 1.6 % (Sun 2025); T13 0.64 % (VertebralBodiesCT-Labels) to 2.0 %
(Sun 2025, L1 ribs). Each prior multiplies the people whose field holds the count: both lumbosacral references for
L6, four-lumbar and Castellvi, and the rib cage from T1 for T13 (`AP` §2).

| block of the holding | countable people (source) | expected L6 | expected four-lumbar | expected Castellvi II-IV | expected T13 | called so far (source) |
|---|---|---:|---:|---:|---:|---|
| CTSpinoPelvic1K, 802 | 789 = 802 x 0.984 (`FOV` ctsp_all) | 25.3 (**calc**) | 12.6 (**calc**) | 71 to 142 (**calc**) | 0, no cage in the colonography field (`FOV` p_t13_ref 0.0) | read: L6 18, four lumbar identifiers 9, 33 Castellvi-graded (`ART:622`, `ART:773-779`); registry: L6 29 (17 read, 11 two-labeller, 1 single), sacralised L5 fused 12, Castellvi I/II 4, lumbar rib 14, unassigned 5 (`REG` tables B, C) |
| TotalSegmentator v2, 1,228 | 483.0 lumbosacral, 471.0 cage (**calc**, summed over `FOV` ts_by_class) | 15.5 (**calc**) | 7.7 (**calc**) | 43 to 87 (**calc**) | 3.0 to 9.4 (**calc**) | registry over 1,935 TotalSegmentator keys: L6 22, T13 4, unassigned 26, unresolved 74 (`REG` table B) |
| COBRA2026, 692 planning CTs | 435 readable by the one-labeller screen (`COBS`) | 13.9 (**calc**) | 7.0 (**calc**) | 39 to 78 (**calc**) | not computable: cage coverage of these CTs is not recorded | one-labeller screen: L6 38, T13 45, four-lumbar 8 (`COBS`); registry: L6 3, unassigned 6, unresolved 11 (`REG` table B) |
| 18 screened acquisition collections | 12,123 passing the field-of-view gate, 16,898 on disk (`CEN` §1) | 322 (`CEN` §1) | 161 (`CEN` §1) | 907 to 1,813 (`CEN` §1) | 38 to 119 (`CEN` §1) | 2026-09-25: L6 two-labeller 21, single 18; T13 single 16; review 84; most large collections not yet called (`CEN` §1). 2026-09-27 flags on tier-1 CTs from the acquisition screens: L6 303, T13 82, L6 and T13 1, unassigned 368, review 1,168 (`TIERS` §1) |
| RibFrac, 660 | 459.4 cage, 0 lumbosacral (`RANK` zenodo:ribfrac) | 0 | 0 | 0 | 2.9 to 9.2 (`RANK`) | registry: T13 4 single-labeller, L6 1 morphology-only, unresolved 29 (`REG` tables B, C) |
| VerSe, 355 persons | not applicable: the cases were found by report search and are enriched, not a prevalence sample (as recorded in `mem:lstv-data-landscape.md`) | — | — | — | — | registry: L6 85, T13 6, sacralised L5 13, Castellvi I/II 27, lumbar rib 12, unassigned 23 (`REG` table B) |
| C-ArmLSpine, 149 CBCTs | 0: lumbar-only CBCT, "neither could count" (`LCM` §4) | — | — | — | — | registry: L6 3 morphology-only, unassigned 1 (`REG` table C) |
| **total, excluding VerSe, C-ArmLSpine and the 10 phantoms** | about 20,280 of the 21,622 census CTs (**calc** from the rows above and `TIERS` §1) | **377** (**calc**) | **188** (**calc**) | **1,061 to 2,120** (**calc**) | **44 to 138** (**calc**) | registry on 2026-09-24 over every stream but the acquisitions: L6 146, T13 14, sacralised L5 fused 27, Castellvi I/II 31, lumbar rib 26, unassigned 62, unresolved 129 (`REG` table A) |

The total double-counts the 71 TotalSegmentator validation CTs, which sit both in the `CEN` block and inside the
1,228 (`TIERS` §0 folds them onto their TotalSegmentator scans); that is about 2 expected L6 (`CEN` §1). Other
cross-collection duplicates are not removed (`TIERS` §8).

What the comparison says, in plain sentences:

- **CTSpinoPelvic1K agrees with the priors where it was read.** L6 18 of 789 is 2.3 % (Wilson 1.4 to 3.6 %, **calc**), around the 3.2 % prior; four-lumbar 9 of 789 is 1.1 % (0.6 to 2.2 %, **calc**) against 1.6 %. Only 33 records carry a Castellvi grade (`ART:239`) against 71 to 142 expected, and the article names a Castellvi read of the whole cohort as work still to do (`ART:919-921`). The gap reads as an unread cohort, not a measured shortfall; how many a full read would add is not recorded.
- **The COBRA2026 one-labeller screen is far above the prior.** Its L6 rate, 38 of 435, is 8.7 % (6.4 to 11.8 %, **calc**) against 3.2 %, and it made 45 T13 calls on abdominopelvic planning CTs. The same labeller's calls matched reader truth on CTSpinoPelvic1K in 10 of 24 L6 and 0 of 52 T13 (`SR2` S4). The registry keeps 3 COBRA L6 (2 two-labeller, 1 single-labeller; `REG` table C), 0.7 % of 435 (0.2 to 2.0 %, **calc**), below the prior. Neither number is verified, and the 435 denominator is the one-labeller screen's, not the registry's.
- **The acquisition screens match the expected total at face value, which is not evidence.** 303 L6 flags (`TIERS` §1) sit near 322 expected (`CEN` §1), or 270 once PANORAMA, which had no flags yet (`TIERS` §1), is removed (**calc**: 322 − 52). The 303 include the TotalSegmentator validation set, which was chosen for its outside L6 and T13 labels (`CEN` §1, 12 L6 calls there). The screen's measured sensitivity on those 70 outside-labelled CTs was 12 of 28 L6 for labeller A, 17 of 28 for B and 9 of 28 for both (`CEN` caveats). If the expected L6 are present, a screen that finds a third to two-thirds of them and still flags about as many as expected is carrying false positives; the agreement of the totals does not say the flags are right. The plan already recorded one plausible but wrong rate: the NLST pilot's 9.3 % T13 fell to 1.5 % once a rib on the named body was required (`AP` §11).
- **T13 is the scarce class in every block.** Between 44 and 138 T13 people are expected in the whole holding, almost all from chest-containing fields (`CEN` §1; **calc**), against the 22 carriers the 85 % sensitivity bound needs on the test side alone (`PJ`). Under the 50 / 10 / 40 split (`FP` G3), 22 test carriers need about 55 T13 people in total (**calc**: 22 / 0.40). The low end of the expectation (44) falls short of that even before any call fails verification.
- **L6 is not the bottleneck in number.** 377 L6 and 188 four-lumbar people are expected (**calc**), against 85 distinct scans that made L6 learnable in VerSe (as recorded in `RATIO`). The bottleneck is verification: no acquired CT has a radiologist read (`AP` §9).

---

## 5. The CTSpinoPelvic1K article: n per analysis

| analysis | n | comparator n | power statement | source |
|---|---|---|---|---|
| geometric invariants | 802 of 802 pass | — | none | `ART:230` |
| rib to vertebra incidence | 5,753 evaluable ribs, 0.035 % offset; 0 assigned to a lumbar vertebra | — | none | `ART:230`, `ART:685` |
| spinopelvic measures | 756 of 802 (44 rejected by the plate gate) | Veilleux n = 200; Hasegawa n = 24 | none | `ART:713-723` |
| T12 against L1 on shape | AUC 0.990, 97.3 % over 1,485 vertebrae, case-grouped folds | — | none | `ART:336-340` |
| Castellvi consensus grades | 33 records, two readers | — | none | `ART:239`, `ART:435` |
| L6; four lumbar; source subtype | 18; 9 (all Castellvi IIIb); lumbarization 14, sacralization 17, semi-sacralization 2 | — | none | `ART:622`, `ART:773-779`, `ART:902-905` |
| rare strata in the folds | two strata of 15 (three per fold); two strata of 2 cannot appear in every fold | — | "a fold-level metric on the rare classes carries an error bar far wider than its own decimal places"; no lumbosacral classifier attempted | `ART:779-786`, `ART:905-907` |
| stump twelfth rib; lumbar rib | 98 of 789 (12.4 %); 16 (2.0 %) | Nagata 2025: 12.6 % and 1.5 % (whole-spine CT) | none; stump ribs with sacralisation 4 of 14 against 94 of 775, no test | `ART:807-812` |
| rib and lumbosacral co-occurrence | not tested in the article | VerSe 280 graded: odds ratio 3.61 [2.08, 6.27] (as recorded in `mem:feasibility-claims-measured.md`) | a whole-cohort Castellvi read "would test the co-occurrence ... at full power" | `ART:919-921`; `ssn:tools/anomaly_cooccurrence_from_labels.py:3-6` |
| per-level morphometry | 802 records, population intervals | cadaveric series of 10 to 30 specimens | the interval argument at n = 12 | `ART:860-868` |
| within-patient posture | 351 patients | — | none | `ART:872` |
| demographics | 393 female, 345 male, 11 other, 53 missing; age on 709 | — | none | `ART:801-803` |

---

## 6. Where the programme stands, in four sentences

- Every powered statement the programme has made rests on planning accuracies of 95 to 99 % that no transitional measurement supports; the transitional figures on disk (render L6 recall 56.1 to 72.4 % [SEL-SPLIT], `sn:results/eval_gate/EVAL_LEAKS.md` item 6; real C-arm L6 classifier 44.9 %, SUPERSEDED, `RESULTS_CATALOG.md` C1.18; film interior anomalous 66.0 %, RECORD ONLY [LEAK], C1.14) would put every transitional test at or near zero power (`RS2` N1; `SR2` S2; rows 6, 8, 10). **No held-out transitional measurement exists**: read this as a planning statement, not a measured result (marks added 2026-10-08).
- Of the comparisons in section 2, the one already decided at its n is LODO against pooled detection on one device (28 cases, 8 to 0) (`NUM:131`); device-level claims cannot be tested with 4 devices (row 1).
- Paper 1's 90 % target needs 35 error-free at-risk persons and paper 2's primary H1 needs 19; today 7 unverified real at-risk persons exist, and the 51 CT test persons are mostly in the encoder's training lineage (`PJ`; `LCM` §5; `NUM:435-436`; `T2`).
- The 97.6 % LevelCheck figure cannot be exceeded at any reachable n (152 error-free persons give 0.22 power at a true 99 %) (`LCM` §7).

---

## 7. Checks made while reading, and discrepancies found

| # | what was checked | finding | source |
|---|---|---|---|
| 1 | `LCM` §7 H1 power tables, unadjusted and at Holm alpha/3, all 14 rows; H2 at 152 and 300 | reproduced to two decimals | **calc** against `LCM` §7 |
| 2 | `PT` inventory_today (89 persons: VerSe 56, CTSpinoPelvic1K 18, TotalSegmentator 12, real 3; 37 test persons) | superseded: the 12 TotalSegmentator spines were read from raw mask ids, and 4 are transitional on an independent rib count | `ssn:tools/anomalous_inventory.py` docstring; `sn:results/anomalous_inventory.json` summary (totalsegmentator total 4) |
| 3 | `LCM` §7: "H6 ... At 145 persons, power is 0.44 at a true 98 % and 0.82 at 99 % (unadjusted)" | does not reproduce unadjusted: the frozen code gives 0.83 and 0.98 at alpha 0.025. The stated values reproduce at alpha 0.025/6 (the six-hypothesis Holm step), or at p0 0.95. `RS2` N8 already notes the 145 row "no longer describes the design" | **calc** |
| 4 | Wilson-target n for 80 % power (99 at 97 %, 69 at 98 %), H1 first n (55, 71, 162), H2 (708, 763), H6 at 51 | reproduced | **calc** against `SR1` R4, `SR2` S1, S3 |
| 5 | `SR2` S12 and `LCM` §15 | the power-0 reading of `SR2` S12 applies to the detectors `LCM` §15 replaced; no file recomputes power for the replacement | `LCM` §15; `SR2` S12 |

---

## 8. Unknowns

| # | unknown | where it was looked for | what would settle it |
|---|---|---|---|
| 1 | the true person-level transitional naming accuracy of any arm on real frames, which every power row needs as its effect size | `PJ`, `SR2` S2, `LCM` §8, `T2` | the paper-2 blinded gate on verified at-risk persons |
| 2 | how many of the 57 field-supported COBRA2026 calls are transitional | `T2` note e; `SR2` S4; `RS2` N7 | a human read of each call (`LCM` §4, §14) |
| 3 | whether the 13 reference-ordinary COBRA persons and 10 C-ArmLSpine persons can carry H6: the reference-standard score of the open gate was not written | `sn:paper2_levelcheck/open_gate_40438004/README.md`; `RES22` lines 679-688 | fixing the gate path in `sn:tools/fig6_score.py` and re-scoring |
| 4 | the person-level intraclass correlation for transitional endpoints (needed by `stats_compare` power) | `NUM` (design effects 3.84 to 4.47 are for vertebrae within cases, ordinary spines) | not recorded |
| 5 | any power calculation for device-level differences, for LODO against pooled across devices, or for the synthetic-to-real ratio | grep of all repositories (section 1) | not recorded; inputs listed in section 2 rows 1, 4, 5 |
| 6 | power under the `LCM` §15 replacement detector | `LCM` §15; `SR2` | not recorded |
| 7 | why `LCM` §7's H6 sentence says "unadjusted" when its numbers match alpha 0.025/6 | `LCM` §7; `SR2` S1 | not recorded |
| 8 | cage-from-T1 coverage of the COBRA2026 planning CTs, so the expected T13 there | `COBS`; `FOV`; `CEN` | not recorded |
| 9 | P(both references) for the TotalSegmentator v300 keys beyond the 1,228 calibrated v2 scans | `FOV` (n_ts 1,228) | not recorded |
| 10 | how many CTSpinoPelvic1K LSTVs a whole-cohort Castellvi read would add (33 graded against 71 to 142 expected) | `ART:919-921` | not recorded |
| 11 | person counts across acquisition collections after deduplication (near-duplicates listed, not merged) | `TIERS` §8; `AP` §9 | `alias_pairs_all.csv` on the grid; not on this laptop |
| 12 | the ruleclass flag counts after the Möller rib and Dataset803 pelvis arms ran (after 2026-09-27) | `TIERS`; `mem:ruleclass-super-detector-run.md` (CORPUS.md is on the grid) | not on this laptop |
| 13 | whether the 148 C-ArmLSpine cases are 148 people (every intraoperative interval assumes they are) | `sn:sections/discussion_limits.tex` | not recorded |
| 14 | the sampling error of the frozen comparators: 97.6 % has no published denominator, and Peh 1999's numerator is assumed (106 of 129) | `LCM` §2; `SR2` S9; `RS2` N10 | the source papers' full text |
| 15 | Barr 2026's de novo value at n = 700, flagged for checking in the report | `RATIO` §2 | the paper's table |
| 16 | whether Li 2016, Li 2017 and ABLSpineLevelCheck (IEEE, unread) report a C-arm naming n that changes section 3 | `mem:registration-free-prior-art.md` | library access |
