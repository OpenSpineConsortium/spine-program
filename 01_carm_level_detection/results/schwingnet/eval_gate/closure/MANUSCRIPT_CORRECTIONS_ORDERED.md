# The closure's manuscript corrections as one ordered list (2026-09-24 15:50 EDT)

Consolidated from `MANUSCRIPT_CORRECTIONS.md` sections 1-8 and `cv_v9/MANUSCRIPT_CORRECTIONS_cv_v9.md`. Status
was read from the working tree at 15:45 (`grep` of `main.tex`, `sections/`, `tables/`, `NUMBERS.md`,
`figures/`), not from any log. **No manuscript file was edited here.** Order: what still changes a printed number
or sentence first, then bookkeeping, then items outside the manuscript. The full replacement text of every item is
in the section named in brackets.

## A. Open: printed text or cells still to change

1. **NUMBERS.md, thirteen rows unmarked** [§2.4, §3a, §3b, §4; status §6.3]. The drive's convention is to add a
   row and mark the old one SUPERSEDED, never to rewrite. Still unmarked at 15:45: `:308` (Numbers deliberately
   absent: widen from "VerSe from v8" to "any CT-render naming accuracy from v8 or v9", implant alias 187 / 164
   persons + 5 VerSe); `:112` (append: the a5 leak check never ran on the four render sources); `:113`, `:244`,
   `:296` (render vs film: 233 bodies / 25 spines -> superseded by `:434`, 161 bodies / 17 held-out spines,
   +31.7 pp [21.0, 45.4]); `:134`, `:141`, `:292` (card gain: 24 folds -> superseded by `:435`, 12 patient-held-out
   folds +0.019 [0.008, 0.033]; "within-subject" before the Pulsera and PIXIUM medians); `:140`, `:245` (retire
   the device-level $P=.13$: two of four device means are within-subject); `:125`, `:128`, `:243` (Holm: 0.0078 ->
   0.0088, printed $P=.009$; superseded by `:436`). Owner: manuscript drive / paper-six-figures.
2. **`figures/figS2.caption.txt`** [§3b; status §6.3] still reads "(a) … of the same projection … (c) Held-out R²
   gain over uncalibrated physics per fold"; the printed legend at `supplement.tex:130` already carries the 58-word
   replacement ("(c) Per-fold R² gain … (Pulsera, PIXIUM within one object)"). Bring the caption file to the print,
   and mark panel (c)'s two within-subject devices (hollow markers). Owner: figure owner.
3. **`figures/figS4.record.json#not_shown_and_why`** (line 1386) [§1.3, §6.2]: the render-curve reason should
   name `closure/case134_sweep_eg2/` (the unseen 40-subject curve, eval_gate/2, set beside the real spin), or the
   curve can be drawn. Owner: figure owner.
4. **`quoted_results.json`** [VERIFY.md §1]: adopt `closure/chk9_cv_v9/quoted_results_cv_v9.json` as
   `results/eval_gate/quoted_results.json` (the C-ArmLSpine rows on the v9 lineage: UNRESOLVED 58 -> 1, HELD OUT
   323 -> 380, SEEN unchanged at 81, 0 disagreements with the hand inventory), and point `figure4.record.json`'s
   `leak_gate` rows at the cv_v9 files so their "HELD OUT" labels are true under CHK-9. Owner: eval-gate workflow.
5. **`FIGREC:figS2/07`, the device-card refit gate** [VERIFY.md §1]: the one row CHK-9 cannot decide, because
   `card_refit` records `n_train` / `n_held` and not the frames. Either `tools/device_fit.py` writes the fitted /
   held frame keys per fold (then a CPU re-fit), or the supplement keeps the row labelled "not established".
   Owner: device-card owner.
6. **Section 8, the accuracy-saturation reading** [§8]: one Results sentence after the fine-tuned numbers and one
   Discussion paragraph in place of a second same-device-data claim (lateral plateau unmoved by same-device data,
   +1.0 pp [-1.9, +4.0]; AP filled, +52.6 pp [+44.1, +61.3]; a held-out day worse than never seeing the device,
   -4.4 pp [-9.1, +0.2]). The paper workflow owns the text; the overview is cited nowhere, its primary sources are.
   The DICOM-tag coverage follow-up §8 asked for now exists as `results/coverage/coverage.json` / `COVERAGE.md`
   (11:08, `tools/acq_coverage.py`, C_d and H*_d per corpus and training set); the matched-N low- against
   high-coverage arms it wanted for Figure 5's coverage axis do not.
7. **Plain-film naming** [§3c]: no held-out plain-film number exists until the Figure 6 model is scored on the G3
   test films (f6eval 40431765 / 40431766 HELD; unblinding has not happened). Table 3 note f already says so.
   Nothing to do until the freeze lifts.

## B. Applied in the working tree (verified verbatim at 15:45; listed so nobody applies them twice)

8. **U1, C-ArmLSpine naming on the v9 lineage** [§7.2 items 1-9, 11]: every `\PENDING{G5}{C-ArmLSpine CV …}` is
   gone from `main.tex`, `sections/results.tex` and `tables/tab3_naming.tex`; "601 of 617" is printed in all three
   (Key Point 2, Abstract, Results 55-59, Table 4 rows 58-60 / 73 / 75 / 78 and note h); `discussion_limits.tex`
   carries "fell four points below the model that had never seen the device". The 98.2 % headline became 97.4 %
   (601/617), day-grouped 92.1 % (568/617), coupled 98.2 % (991/1,009); fine-tuning +1.0 pp lateral (not
   significant), +52.6 pp AP. Remaining `\PENDING{G5}` macros (28) are the Flagship cells of `tab2_detection.tex`
   54-66 and Figure 5's data-case panel at `results.tex:85`, which are other workflows' (FLAGSHIP_PLAN G5;
   indomain / coverage).
9. **NUMBERS.md, the 40 U1 rows** [§7.2 item 10] and **CLAIMS_LEDGER.md:211** [item 11]: the new rows `:413-436`
   region carries the v9 numbers; the old rows `:84-103`, `:205-207`, `:211-215`, `:237-241`, `:251`, `:298-301`
   are the ones item 1 above says to mark SUPERSEDED where not yet marked (`:402-403`'s "UNRESOLVED" note is
   resolved by §7; `:417` gains "first fold-model runs, not used: 606/617, 571/617").
10. **Table 1 note c** (`tab_corpus.tex:69`), **Geneva / Ljubljana cells and note k** (`:60-61`, `:77`), **role
    cells** (`:51-53` "level bank; checkpoint selection") [§2.4, §3b, §3c].
11. **Table S2 rows and notes a, f** (`tab2_detection.tex:68-69`, `:75`, `:80`): 161 bodies / 17 held-out NHANES II
    spines, film-trained 99.4 % vs render-trained 67.7 % at 0.05, +31.7 pp [21.0, 45.4], 16 : 0 [§3a].
12. **Supplement "Which source carries the detector"** (`supplement.tex:74-77`) [§3a]; **"Image-formation terms"**
    (`:50-55`, with the within-subject sentence deleted) [§3b]; **Holm $P=.009$** (`:71`) [§4]; **Figure S3 legend**
    (`:130`) [§3b].
13. **Table S1 row and note** (`tabS1_device_terms.tex:24`, `:27`; generator `make_supp_device_table.py`) [§3b].
14. **Table 3 (printed Table 4) note f** (`tab3_naming.tex:89`): no held-out plain-film accuracy until the Figure 6
    model is scored [§3c].
15. **Methods optional clause** (`methods.tex:52`, implant alias) [§2.4]: declined by the drive for length; no
    action.

## C. Closed with no manuscript change (the evidence, for the record)

16. **case134 real spin** [§1, §6.2]: the pooled detector never saw case134 (0 lines in `P_pooled/train.txt` and
    `val.txt`; weights written before the frames existed). Re-scored under eval_gate/2 (job 40436881): every
    number identical to the 07:18 run; pooled 93.6 / 78.1 %, lodoA 37.2 / 29.1, lodoB 29.6 / 23.5, real_lodo
    49.5 / 49.4 at 0.25 / 0.74; the render column now the unseen 40-subject curve. Figure S5 draws only the real
    spin.
17. **allspine_v8, 192 persons on both sides** [§2]: the implant alias (187 CTSpinoPelvic1K) and VerSe series
    keyed as subjects (5); v9: 164, all implant alias. No film patient among them; no quoted number moves; the
    49 / 4 / 14 / 15 / 7 / 3 per-subtype exposure re-derived identically.
18. **The gate closed (VERIFY 1b, 1c)** [§5]: `--matches` binding, `carry()` audit, key canonicalisation, 29
    evaluators gated; the unseen curve re-aggregated under the binding reproduces 1,824 of 1,824 cells; the
    headline detector dump re-scored with today's weight file is identical on 55 of 56 frames (one 1e-4 score
    difference, floating point). `eval_sets.json` rebuilt: 0 keys changed in 17 sets.
19. **Holm family after the replacements** [§4]: raw 1.3e-22 (v9 zero-shot), 3.1e-5, 0.0078, 0.0044; adjusted
    5.4e-22, 9.2e-5, 0.0088, 0.0088; printed $P<.001$, $P<.001$, $P=.009$, $P=.009$.
20. **The three cv_v9 cells re-derived from raw fold dumps** [VERIFY.md §2-4]: 601/617, 608/631, 568/617 (and
    598/631, 991/1,009) reproduce exactly; every gate block is bound to its weights by sha256; no test case in any
    fold model's train / val keys or in the `allspine_v9` ancestor's keys.

## D. Outside the manuscript, for their owners

21. `results/a5.json#v2_statement` ("v8's known leak is VerSe") -> VerSe series (5) and CTSpinoPelvic1K implant
    renders (187), both CT-derived; `results/RIGOR_FIXES.md` A5; `docs/MODEL_CARD.md:168` and
    `docs/DATASHEET.md:267` ("the clean rebuild"); `results/rare_class/split_plan.md` "Model exposure" totals
    (9,893 / 9,878 over-count TotalSegmentator and NHANES persons neither bank read; the banks hold 9,609 / 9,589);
    `EVAL_LEAKS.md` L4 (names the 192, not the cause) [§2.3-2.4].
22. Stale: `results/arc/case134_sweep.{json,md}` and its figure (void curve, false contamination sentence);
    `EVALUATORS.md` §1.4 can point at `closure/case134_sweep_eg2/` [§1.4].
23. eval_gate/2 re-runs so scorers can carry them without a declaration: `leaks/render_vs_film_unseen_rerun.json`
    (`rigor_fixes.py a3a-rows`, CPU), `results/arc/recall_vs_angle_unseen/` (eval_gate/2 twin already at
    `closure/bypass/out/R1d_i/`), `docs/devices/eval_gate/*.json` (`tools/device_fit.py gate`, CPU); the cv_v9
    dumps themselves (eval_gate/1 blocks, no dump-level `weights_sha256`) [§5.4, §6.4, §7.0]. Numbers not in
    question.
24. `tools/head_mixed_length.py` and `tools/head_dual.py` write no `weights_sha256`; left alone for the held
    Figure 6 chain; a scorer refuses their output until each calls `EG.stamp` [§5.4].
