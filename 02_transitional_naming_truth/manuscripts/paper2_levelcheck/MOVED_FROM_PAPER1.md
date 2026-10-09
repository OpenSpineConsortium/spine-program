# Moved from paper 1 (SchwingNet manuscript) into paper 2 (the LevelCheck / surgeon comparison)

Greg, 2026-09-24: "I'd like to move the comparison to neurosurgeons / all the LevelCheck stuff into a new paper,
remove it from the current paper." Every passage below is copied **verbatim** from the paper-1 source at
`SchwingNet/` commit **dd8f4a562709af202541f422efe42525c29beaa0** (HEAD when the move began), with the file and
the line numbers it occupied in that commit. Nothing was deleted without being copied here first. The manifest
entries moved with it are in `numbers_manifest_moved.json` beside this file; the Table 3 files were moved whole with
`git mv` into `paper2_levelcheck/tables/` (their text is also reproduced below). `LEVELCHECK_MODEL.md` (frozen,
d0403de) was not touched and stays where it is; paper 2 reads it from there.

Seven things moved (the list `PAPER1_SCOPE.md` names), plus an eighth in the fill pass (item 8):

1. The Results paragraph "The LevelCheck comparison" with its `\PENDING{G6}` placeholder.
2. Figure 6 (`\PENDINGFIG{figures/figure6.pdf}` and its caption) and its manifest keys.
3. Table 3 = `tables/tab_levelcheck.tex` (+ `.md`, `.sources.md`) and its `\input`, plus the Table 4 row that owed
   the per-stratum G6 result.
4. Figure 5 panel (b) (exact-test power against the modelled LevelCheck accuracies) and the manifest keys
   `power_n_min_h1_822`, `power_n_min_h2_976`, `power_n_min_g6_level_90`. The PDF was **not** rebuilt (see the note
   at item 4 below); panel (a) stays, re-captioned as persons needed to certify an accuracy.
5. The Methods paragraph "The LevelCheck comparison" (the comparator, the strata, the unit, the primary detector of
   s15, the secondary analyses of s12-s13: M1, F1, D1, S1) and the power sentences of "Statistical analysis".
6. The Discussion paragraph on LevelCheck (seven mentions) and the two comparison clauses of the limitations and
   summary paragraphs.
7. The "Registration" sentence on the frozen comparator, the fourth aim of the Introduction's purpose sentence, the
   abstract's Purpose / Materials and Methods / Results / Conclusion clauses on the comparison, the summary-statement
   and key-point clauses, and the title clause "versus registration-assisted neurosurgeons".

What stayed in paper 1 because it is paper 1's own cross-validation result (not moved): the coupled call, the count
from the detected sacrum and the stop signal on C-ArmLSpine (Results "Naming, counting and coupling", Table 4 now
Table 3, "Coupled: classifier and count" block); the three C-ArmLSpine L6 patients' cross-validation row (agreement
with one labeller's read); the Introduction's prior-art sentences on LevelCheck (`levelcheck2012`, `levelcheck2016`,
`desilva2016`, `manbachi2018`, `peh1999`). The supplement's automated-reference paragraph stayed at first (for an
ordinary-person real-frame result, if one landed) and moved on the evening of 2026-09-24 as item 8 below, because no
result paper 1 prints rests on it.

---

## 1. Results paragraph — `sections/results.tex` lines 88-91

```latex
\paragraph{The LevelCheck comparison.}
The comparator was committed before any held-out transitional person was scored (Table~\ref{tab:levelcheck}).
The comparison is \PENDING{G6}{SchwingNet against the frozen LevelCheck comparator per stratum: k of n persons,
Wilson interval, Holm-adjusted exact P} (Figure~\ref{fig:levelcheck}).
```

Also from the Results "Transitional sample size" paragraph, `sections/results.tex` lines 78-79, the first sentence
(the exact-test n against the frozen values; the rest of that paragraph stays in paper 1, rewritten around the
pre-stated Wilson targets):

```latex
With no error, the frozen exact test needs at least 19 at-risk persons against 82.2\,\% and 152 against 97.6\,\%
(Figure~\ref{fig:power}c).
```

and the clause "the three C-ArmLSpine L6 patients were excluded in advance" (line 79-80), which described the
comparator's exclusion rule (LEVELCHECK_MODEL.md s4).

Header comment of `sections/results.tex`, lines 4-5: "... transitional sample size (Figure 5), and the LevelCheck
comparison (Table 3, Figure 6; gate G6)."

## 2. Figure 6 — `main.tex` lines 182-190

```latex
% Figure 6 (gate G6; the Figure 6 path of workflow paper-six-figures: tools/fig6_sets.py, fig6_freeze.py,
% fig6_manifest.py, fig6_score.py). Drawn from figures/figure6.pdf as soon as that file exists; until then the
% PENDING marker prints and tools/check_limits.py fails. The caption is written from LEVELCHECK_MODEL.md s7 (what
% the figure draws); replace it with figures/figure6.caption.txt when that lands.
\begin{figure}[tbh!]
\centering
\PENDINGFIG{figures/figure6.pdf}{G6}{Figure 6, SchwingNet against the frozen LevelCheck comparator}
\caption{SchwingNet against the frozen LevelCheck comparator on held-out persons, by stratum: accuracy per person with Wilson 95\,\% interval, and the one-sided exact $P$ against modelled LevelCheck accuracy swept from 10\,\% to 100\,\%; frozen values (82.2\,\%, 97.6\,\%, 92.6\,\%) and published anchors marked. Modelled, not measured, LevelCheck.\label{fig:levelcheck}}
\end{figure}
```

Manifest keys (`numbers_manifest.json`): `figures.figure6`, `numbers.fig6_h1_coupled_accuracy_pct` — in
`numbers_manifest_moved.json`.

`main.tex` header comment, lines 9-19 (the six-figure story), the relevant clauses: "6 SchwingNet against the frozen
LevelCheck comparator (fig:levelcheck, gate G6)" and "3 the frozen LevelCheck comparator (tab:levelcheck)".
`sections/introduction.tex` header line 4: "(1 phenotypes, 2 embedding, 3 network, 4 one exposure, 5 persons needed,
6 LevelCheck)".

## 3. Table 3 — `tables/tab_levelcheck.tex` (whole file; now `paper2_levelcheck/tables/tab_levelcheck.tex`) and its `\input`

`main.tex` lines 192-200 (the table block; the `\input{tables/tab_levelcheck}` line is 199):

```latex
% ---- Tables 1-4, in citation order (the journal: tables after the legends, one per page, numbered in order of
% first citation). 1 = image sources (tab:data), 2 = transitional persons by subtype (tab:transitional),
% 3 = the frozen LevelCheck comparator (tab:levelcheck), 4 = naming, counting and coupling (tab:naming). Each .tex
% has a .md twin and a .sources.md naming the file behind every cell; fit check slurm/tables_check.sh +
% tools/tables_check.py (tables/tables_check.tex inputs the same four).
\input{tables/tab_corpus}
\input{tables/tab4_transitional}
\input{tables/tab_levelcheck}
\input{tables/tab3_naming}
```

`tables/tables_check.tex` line 35: `\input{tab_levelcheck}` (and its `\clearpage`).

`tables/tab_levelcheck.tex`, whole file (66 lines):

```latex
% Table 3 -- the LevelCheck comparator, pre-specified and frozen (SchwingNet/LEVELCHECK_MODEL.md sections 3-5 and the
% JSON block of section 11; frozen by the commit that added that file, ecae75f, 2026-09-23 19:50 EDT). Every frozen
% cell is transcribed from that file; the columns a gate owes are \PENDING{G6}{...}. No merged cells. Sources, one
% line per cell, in tab_levelcheck.sources.md; the same rows in tab_levelcheck.md.
% Revision 2 (2026-09-24, REVISION_LOG2.md): footnote a says the render L6 recall seen before the freeze is on the
% encoder's selection split (EVAL_LEAKS L5); footnote c adds the primary detector of LEVELCHECK_MODEL.md s15 (commit
% d0403de) and that the frozen values are constants (REVIEW2_STATS N10); footnote d adds H6 feasibility (N8a;
% results/stats_review2/recompute.json#S3_H6_feasibility: at most 51 ordinary real-frame test persons).
% Revision 3 (2026-09-24, collect-and-submit-1; REVISION_LOG3.md): footnote c names the secondary analyses of
% LEVELCHECK_MODEL.md s12 (M1 McNemar, F1 flag at 95 % validation sensitivity, D1 dual-loss head) and s13 (S1
% accepted-person accuracy vs 0.976 with tau_s fixed on validation for >= 99.5 %, n_min 152, coverage and the
% confidently-wrong count beside it; F1b at 97 %), which the Methods now name in one clause.
% Layout: landscape (rotated 23.2 cm minipage, see tab_corpus.tex); 7 pt on 7.6 pt.
\begin{table}[p]
\centering
\begingroup
\singlespacing
\fontsize{7}{7.6}\selectfont
\newcommand{\fnm}[1]{\textsuperscript{\fontsize{7}{7}\selectfont #1}}
\renewcommand{\arraystretch}{1.0}
\rotatebox[origin=c]{90}{\begin{minipage}{23.2cm}
\captionsetup{font=footnotesize,skip=4pt}
\centering
\caption{The LevelCheck comparator, frozen before any held-out transitional person was scored: per hypothesis the stratum, the test, the modelled LevelCheck accuracy and its source, the published range, the smallest test count at which an error-free result passes, and the result owed.}
\label{tab:levelcheck}
% widths sum to 22.00 cm; 14 gaps of 1.9 pt (0.94 cm) -> 22.94 cm
\setlength{\tabcolsep}{1.9pt}
\begin{tabular}{%
>{\raggedright\arraybackslash}p{1.30cm}%
>{\raggedright\arraybackslash}p{3.90cm}%
>{\raggedright\arraybackslash}p{2.20cm}%
>{\raggedright\arraybackslash}p{1.60cm}%
>{\raggedright\arraybackslash}p{4.30cm}%
>{\raggedright\arraybackslash}p{3.70cm}%
>{\raggedright\arraybackslash}p{1.60cm}%
>{\raggedright\arraybackslash}p{3.40cm}}
\toprule
Hypothesis\fnm{a} & Stratum\fnm{b} & Test\fnm{c} & Modelled LevelCheck accuracy, \% & Source of the frozen value & Published range of the modelled accuracy, \% & Smallest passing test count\fnm{d} & Test persons; SchwingNet $k/n$ [Wilson]; Holm-adjusted $P$ \\
\midrule
H1 (primary) & at risk, pooled & superiority & 82.2 & a lumbar planning read without a count from C2, coronal localiser \citep{peh1999}: the most favourable published value, measured on all patients & 20.8 (count-changing transitional spines counted correctly, 10 of 48 \citep{nakagawa2017}) to 100 (the read counted correctly) & 19 & \PENDING{G6}{H1} \\
\addlinespace[2pt]
H2 (key secondary) & at risk, pooled & superiority & 97.6 & surgeons with the LevelCheck overlay, median of five over 62 difficult films \citep{manbachi2018}; assumes the planning read counted correctly; no interval published & as H1 & 152 & \PENDING{G6}{H2} \\
\addlinespace[2pt]
H3 & at risk, L6 & superiority & 82.2 & as H1 (no subtype given) & 17.6 (lumbarised S1 counted correctly, 6 of 34 \citep{nakagawa2017}) to 100 & 19 & \PENDING{G6}{H3} \\
\addlinespace[2pt]
H4 & at risk, sacralised L5 & superiority & 82.2 & as H1 & 28.6 (sacralisation, Castellvi III, 4 of 14 \citep{nakagawa2017}) to 100 & 19 & \PENDING{G6}{H4} \\
\addlinespace[2pt]
H5 & at risk, T13 & superiority & 82.2 & borrowed from H1: no planning-read series on thoracolumbar variants & 31 (a twelve-thoracic count agreeing with morphology on L1, 31 of 100 \citep{yun2018}) to 100 & 19 & \PENDING{G6}{H5} \\
\addlinespace[2pt]
H6 & ordinary spines & non-inferiority, margin 5 points & 92.6 & 97.6 \citep{manbachi2018} minus the margin, chosen knowing the development accuracy on ordinary spines & 97.6 to 100 (operating-room series, 20 of 20 \citep{manbachi2018}) & 48 & \PENDING{G6}{H6} \\
\addlinespace[2pt]
-- & transitional, naming unaffected & descriptive & none & 97.6 and 100 printed beside & 97.6 to 100 (sacralisation, Castellvi II, 23 of 23 counted correctly \citep{nakagawa2017}) & -- & \PENDING{G6}{naming unaffected} \\
\bottomrule
\end{tabular}
\par\vspace{1pt}
\begingroup\fontsize{7}{7.6}\selectfont\raggedright
L5, L6 = fifth, sixth lumbar vertebra; S1 = first sacral segment; T13 = thirteenth thoracic vertebra; LevelCheck = labelling by registration of the preoperative CT to the intraoperative radiograph \citep{levelcheck2012}.
\fnm{a}Model: LevelCheck carries the labels a reader assigned to the preoperative CT, so its accuracy on a stratum is $r(1-e)$, with $r$ the registration success, frozen at 1.0 (published 0.993--1.000 \citep{levelcheck2016}), and $e$ the probability that the planning read names a scored vertebra otherwise than the reference; no residual surgeon error is multiplied in, both simplifications favouring LevelCheck. Frozen by commit on 23 September 2026 before any held-out transitional person was scored; seen before the freeze were the ordinary-spine development results, the three C-ArmLSpine L6 patients and render L6 recall of 56.1--72.4\,\% on the encoder's checkpoint-selection split, all below 82.2\,\% where transitional.
\fnm{b}Membership from the reference standard alone, fixed before unblinding. At risk: a transitional person with a frame on which a reference-named body is misnamed by counting up from the sacrum over five lumbar vertebrae or down from C2 over seven cervical, twelve thoracic and five lumbar. Naming unaffected: Castellvi I/II, lumbar rib, a fused L6 left unlabelled, a sacralised L5 keeping its label, or no flagged frame. The three C-ArmLSpine L6 patients are excluded from the primary analysis in advance and reported descriptively.
\fnm{c}Unit: the person. One frame with at least four reference-named bodies drawn per person by a fixed seed from the truth alone; correct when every reference-named body receives its reference name (missed, unnamed, abstained or unanchored = wrong). SchwingNet configuration fixed before unblinding: an arm never trained on a test person (encoder from ImageNet weights on the split's training persons), the coupled call, detector confidence 0.74, whole frame, seed 0; the detector is trained on the split's training persons of every device (patient-held-out, device seen; added by commit on 24 September 2026), the device-held-out detectors a secondary analysis. Reference: the source's reader truth; otherwise a human verification or, failing that, an automated reference whose rule and calibrated positive predictive value were frozen before unblinding (added by commit on 24 September 2026). Secondary analyses added by commit on 23 September, outside the H1--H6 family: the count from the detected sacrum against the coupled call on the same frames (exact one-sided McNemar on discordant persons, lumbosacral strata); a transitional flag (non-ordinary alphabet, count--morphology disagreement, or a dual-loss head's spine-level probability at a threshold fixed on validation for at least 95\,\% and, separately, 97\,\% sensitivity); and accuracy on the persons whose frame SchwingNet accepts (anchored, unflagged, every margin at or above a value fixed on validation for at least 99.5\,\% validation accuracy) against 97.6\,\%, tested only from 152 accepted persons and always printed with its coverage and the count of accepted-but-wrong persons. One-sided exact binomial $P$, the probability of at least $k$ correct of $n$ at the frozen value; Holm over the eligible hypotheses at a familywise one-sided 0.025; Wilson 95\,\% interval for description. The frozen values are fixed constants; their own sampling error is not modelled.
\fnm{d}The smallest $n$ at which $n$ of $n$ correct gives $P \le 0.025$; a hypothesis whose stratum is smaller is reported descriptively and not claimed. The built split holds at most 51 ordinary real-frame test persons (COBRA2026 41, C-ArmLSpine 10), so H6 passes only without error.
\par\endgroup
\end{minipage}}
\endgroup
\end{table}
```

The Table 4 row that owed the G6 result — `tables/tab3_naming.tex` line 94 (the row after it, the three C-ArmLSpine
cases, stays in paper 1 under a new block heading):

```latex
Transitional stratum & held-out transitional persons of the built split & one frame per person; conf 0.74 & all bodies named right (Tables~\ref{tab:transitional}, \ref{tab:levelcheck}) & \PENDING{G6}{per stratum} & -- & -- & -- \\
```

and its twin, `tables/tab3_naming.md` line 71:

```
| Transitional stratum | held-out transitional persons of the built split | one frame per person; conf 0.74 | all bodies named right (Tables 2, 3) | PENDING G6 (per stratum) | — | — | — |
```

`tables/tab3_naming.tex` header lines 15-16: "% Transitional stratum: PENDING G6 (the G3 split is built; the G6 arm
scores it under tab_levelcheck.tex); the three C-ArmLSpine cases one labeller reads as L6 are shown as agreement with
that read, not correctness (CLAIMS_LEDGER 6)."

Table 2 (`tables/tab4_transitional.tex`) clauses that named the comparator:
- line 77, note c, last sentence: "The three real C-ArmLSpine L6, whose outputs were seen before the comparator was
  frozen, are excluded from its primary analysis in advance and reported descriptively."
- line 78, note d, last clause: "so the transitional comparison needs an arm trained without them."
- line 80, note f: "the own-label sacralised L5 are naming unaffected under the frozen rule (Table~\ref{tab:levelcheck})
  and are not in the at-risk bound;"
- header comments lines 5-6 ("the comparison is Table 3 (tab_levelcheck.tex) and Figure 6") and 16-17 ("footnote c
  says the three real C-ArmLSpine L6 are excluded from the primary analysis in advance (LEVELCHECK_MODEL.md s4), so
  their 43.9 % bound is no longer printed as an available real-frame bound").
The same sentences in `tables/tab4_transitional.md` notes (c), (d), (f) (lines 26-28 and the (f) line).

## 4. Figure 5 panel (b) — `main.tex` lines 172-180 and `tools/fig_power.py`

The Figure 5 block as it stood (caption = `figures/figure5.caption.txt` verbatim):

```latex
% Figure 5 (SchwingNet/tools/fig_power.py -> results/power/power.json; record figures/figure5.record.json, rebuilt
% 2026-09-24 08:26 with the COBRA2026 anomaly-harvest count; legend = figures/figure5.caption.txt verbatim). The
% indomain-curve workflow may rebuild Figure 5 around the data case (no results/indomain/fit.json yet: the data case
% is PENDING G5 in the Results); its caption and RESULTS_PARAGRAPH.tex are then integrated, not here.
\begin{figure}[tbh!]
\centering
\includegraphics[width=\linewidth,height=0.88\textheight,keepaspectratio]{figures/figure5.pdf}
\caption{Transitional persons needed and available. (a) Wilson 95\,\% lower bound, by errors. (b) Exact-test power at a true 95\,\% against modelled LevelCheck accuracies (curve labels, \%); dashed, Holm $\alpha/3$; dotted, true 99\,\%. (c) Persons, not frames, per pre-specified stratum, 2026-09-24; dashed, n each claim needs. (d) Zero-error intervals at open-marker n. L6, sixth lumbar; T13, thirteenth thoracic.\label{fig:power}}
\end{figure}
```

Moved to paper 2: the panel (b) clause "(b) Exact-test power at a true 95\,\% against modelled LevelCheck accuracies
(curve labels, \%); dashed, Holm $\alpha/3$; dotted, true 99\,\%." and, in `tools/fig_power.py`, `panel_b()` (lines
640-721 at dd8f4a5: the one-sided exact binomial power of the frozen H1/H2 tests at p0 = 20.8, 46.5, 82.2 (also at
Holm α/3) and 97.6 % at a true 95 % and 99 %), its call at line 869, its letter at line 882, and the record's
`components.b`, `numbers_on_figure.comparators_pct / true_accuracies_pct / power_80_pct / panel_b_first_n_power_80`.
The dashed verticals of panel (c) at 19 and 152 (`need["H1_exact_82.2"]`, `need["H2_exact_97.6"]`, lines 767-772,
844-850) are the frozen exact test's n and belong to paper 2 as well.

**The PDF was not rebuilt and the script was not edited.** `tools/fig_power.py` is local, but its `load_available()`
stops by design as soon as `results/fig6/frozen/auto_reference.json` exists (line 308), and that file exists now
(the automated reference was frozen 2026-09-24), so the script cannot run until the automated reference is wired
into panel (c); the workflow that rebuilds Figure 5 around the data case owns that rebuild (main.tex comment). Paper
1 therefore keeps `figures/figure5.pdf` as drawn and captions panel (b) for what it shows, without naming the
comparator; at the next rebuild panel (b) and the 19 / 152 verticals are to be dropped (and the letters c, d become
b, c), which is recorded in `REVISION_LOG3.md` section 8 and `PAPER1_SCOPE.md`.

Manifest keys moved: `power_n_min_h1_822`, `power_n_min_h2_976`, `power_n_min_g6_level_90` (in
`numbers_manifest_moved.json`). Note on the third: it is the Wilson-90 % n (35 persons), the pre-stated G6 target
that paper 1 still prints in Table 2 note f and the Results from `results/stats_review/recompute.json#R4_wilson` and
`results/power/power.json#n_needed_zero_errors/G6_level_wilson_90`; it was moved with the other two as the task
listed it, and paper 1 can re-key it under a name without "g6" when the `\RESULT{}` conversion pass runs.

## 5. Methods — `sections/methods.tex`

Lines 97-113, the whole paragraph:

```latex
\paragraph{The LevelCheck comparison.}
LevelCheck was modelled and frozen by commit before any held-out transitional person was scored
(Table~\ref{tab:levelcheck}): carrying the planning read's labels, its accuracy is registration success (1.0
\citep{levelcheck2016}) times the probability that the read names each vertebra as the reference does. For
persons at risk, those a count from the sacrum or from C2 misnames (Table~\ref{tab:levelcheck}), the frozen value
is 82.2\,\%, the most favourable published accuracy of a read without a count from C2 \citep{peh1999}; the
published 97.6\,\% \citep{manbachi2018} is the key secondary comparator; ordinary persons are tested for
non-inferiority at 92.6\,\%. The unit is the person,
one real frame with at least four reference-named bodies, correct only if every body gets its reference name, so a
missed body, an unanchored frame or an abstention is wrong; one-sided exact binomial tests, Holm-adjusted, run
only where a stratum can pass. CT renders are secondary. Because the device-held-out sacrum
detector anchored 21 of 609 COBRA2026 development frames (3.4\,\%), the primary detector was changed by commit
before unblinding to one trained on every device's training persons (Table~\ref{tab:levelcheck}). The scored
configuration, with an encoder trained from ImageNet weights on the
split's training persons, and the secondary analyses, including accuracy on the frames SchwingNet accepts
against 97.6\,\% with coverage beside it, are fixed before unblinding (Table~\ref{tab:levelcheck},
Figure~\ref{fig:levelcheck}).
```

Lines 52-54, "Reference standard", last sentence (the clause "(Table~\ref{tab:levelcheck})" moved; the sentence
itself stays in paper 1 pointing to the supplement, because an ordinary-person real-frame result would rest on the
automated reference):

```latex
Held-out transitional persons
without a human read take an automated reference, three readers combined under a rule specified by commit before
unblinding (Table~\ref{tab:levelcheck}), its measured error carried into every result resting on it.
```

Lines 92-95, "Transitional sample size" (the clause "sit outside the frozen tests' multiplicity control" moved; the
paragraph is rewritten in paper 1 around the pre-stated Wilson targets):

```latex
\paragraph{Transitional sample size.}
Pre-stated Wilson targets on pooled at-risk test persons sit outside the frozen tests' multiplicity control
(Table~\ref{tab:transitional}, Figure~\ref{fig:power}); the person-disjoint split (50:10:40 per subtype) puts every
real transitional subject on the test side.
```

Lines 116-119, "Statistical analysis", the power sentence:

```latex
Transitional power is exact binomial enumeration against the frozen values at an
assumed accuracy of 95\,\%, which no transitional measurement supports: against 82.2\,\%, 80\,\% power needs 55
at-risk persons (71 at the Holm step); against 97.6\,\% it reaches 80\,\% only at a true 99\,\%,
at 708 persons (Figure~\ref{fig:power}b).
```

Lines 123-124, the clause ", one-sided .025 for the frozen comparison" in "significance was two-sided $P<.05$,
one-sided .025 for the frozen comparison."

Header comment lines 4-8 and 13-21 (the parts naming the LevelCheck comparison, s12-s15, "Fixed before unblinding",
the G5 manifest / slurm/fig6_*.sh / RELEASE_v2.json condition, and the Revision 3 s12-s13 clause).

## 6. Discussion — `sections/discussion_motivation.tex` and `sections/discussion_limits.tex`

`discussion_motivation.tex` lines 28-35, the whole paragraph:

```latex
LevelCheck's published accuracies measure convergence onto a reader's labels \citep{desilva2016,manbachi2018}, a
ceiling this network can at best match where the read counted correctly. In simulation every
registration failure was a one-vertebra shift from the spine's periodicity \citep{levelcheck2012}, later removed
clinically by multistart \citep{levelcheck2016}; a count from
the sacrum is off by one level on a transitional spine, and a label carried from a planning read fails with that
read \citep{peh1999,nakagawa2017}. The comparator was therefore frozen at the most favourable
published accuracy of such a read, and local morphology is tested as a different mechanism, not a better optimiser. Exceeding the published 97.6\,\% needs at least 152 error-free at-risk persons; it is reported beside an
interval, not beaten. Neither accuracy is a wrong-level surgery rate.
```

Lines 40-41, the phrase "The comparison arm's level model saturates likewise in development" (the sentence stays in
paper 1 with the arm named for what it is: a level model trained from ImageNet weights on the split's training
persons).

Header comment lines 1-6 (the LevelCheck parts).

`discussion_limits.tex` lines 11-12: "most transitional test persons were in the current encoder's lineage, so the
comparison uses a separately trained arm." (the first clause stays; "so the comparison uses a separately trained
arm" moved).

`discussion_limits.tex` lines 17-19 (summary paragraph): "Whether it names transitional spines better than
registration carrying a planning read is untested: the frozen comparison needs at least 19 verified at-risk persons
with real exposures, and none is verified."

## 7. Front matter, purpose, registration, title

`main.tex` line 42, the title clause: ", versus registration-assisted neurosurgeons" in
`\title{SchwingNet: a convolutional-recurrent network for level naming in spine surgery, robust to transitional anatomy, versus registration-assisted neurosurgeons}`
(and the same in `TITLE.md`, whose 2026-09-23 fixing note is kept there with the change recorded).

`main.tex` line 75, summary statement clause: "; its frozen comparison with registration on transitional spines
awaits verified patients."

`main.tex` line 81, key point 3 clause: ", and exceeding the published 97.6\,\% accuracy of surgeons using
registration needs at least 152 error-free at-risk transitional persons."

`main.tex` line 89, abstract Purpose clause: ", and pre-specify a comparison with registration on transitional
spines."

`main.tex` line 91, abstract Materials and Methods sentence: "Exact binomial power set transitional sample size; a
LevelCheck comparator was frozen beforehand."

`main.tex` line 93, abstract Results: "No real-exposure transitional test person was verified; exceeding 97.6\,\%
needs 152 error-free at-risk persons. The LevelCheck comparison is \PENDING{G6}{result}."

`main.tex` line 95, abstract Conclusion clause: "; its comparison with registration on transitional spines awaits
verified exposures."

`main.tex` line 114, Data availability clause: "; the frozen LevelCheck comparator is the file LEVELCHECK\_MODEL.md"

`main.tex` line 120, Registration:

```latex
\textbf{Registration.} Not a clinical trial; not registered. The LevelCheck comparator was frozen by a dated repository commit before any held-out transitional person was scored.
```

(the first sentence stays; the second moved.)

`sections/introduction.tex` lines 40-41, the fourth aim: "and derive how many transitional persons a comparison
with a pre-specified model of LevelCheck needs." in "The purpose was to build that network (SchwingNet), examine what
it learns, test it on an unseen C-arm, and derive how many transitional persons a comparison with a pre-specified
model of LevelCheck needs."

`main.tex` lines 48-49 comment: "(S1 appears only in Table 3, whose footnote defines it; ...)"; lines 137-140
comment: "(the at-risk distinction of Table 3)".

## Supplement — `supplement.tex`

Line 101, clause: "until the ImageNet-initialised model of Figure~6 of the main text is scored on the test films of
the person-disjoint split." (paper 1 now says such a model is not scored here).

Lines 130-131, section title and first clause: `\section*{Development learning curve of the comparison arm}` /
"The recurrent head of the frozen comparison's level model (encoder from ImageNet weights on the split's training
persons)". The section's numbers (a development learning curve, no test person) stay in paper 1 under a neutral
title.

Lines 246-250, the pre-registration paragraph (the comparator commits moved; paper 1 keeps the automated-reference
commit b511985 and the never-edit rule):

```latex
\textbf{Pre-registration.} The comparator and its analysis plan were fixed by dated repository commits before any
held-out transitional person was scored: the comparator (23 September 2026, 19:50; ecae75f), the mechanism test,
transitional flag and dual-loss arm (20:50; 1897772), the accepted-frame analysis (20:58; 2993f40), the automated
reference (24 September, 05:29; b511985) and the primary detector (08:09; d0403de). A committed section is never
edited; a change is a new commit before unblinding that records the old value, the new one and the reason.
```

Header comment line 28: "the automated reference (LEVELCHECK_MODEL.md s14; calibration PENDING G6)" (kept as a
comment; the paragraph it describes stays).

## References that were cited only in moved text

`yun2018` (Table 3, H5 row). Its entry stays in `refs.bib`; paper 1 now cites 34 keys. `peh1999`, `manbachi2018`,
`desilva2016`, `levelcheck2012`, `levelcheck2016`, `nakagawa2017` remain cited in the Introduction's prior-art
sentences and stay.

## Not moved, flagged for paper 2's own ledger

- `packet_src/cover_letter.md`, `packet_src/front_matter.json` (the `levelcheck_prespecification` block and the
  Registration statement), `packet_src/statements.md` items 8-9 and `CLAIMS_LEDGER.md` / `claim_checklist.json`
  rows on the comparison still describe the comparison as part of paper 1; they are outside this pass's file list
  and are listed in `REVISION_LOG3.md` section 8 as open.
- `figures/figure5.caption.txt` (written by `tools/fig_power.py`) still carries the panel (b) LevelCheck clause; the
  main.tex legend no longer equals it (recorded in the main.tex comment).

---

## 8. The automated reference standard — moved in the fill pass of 2026-09-24 (evening; paper-1 HEAD 887e37cc92b8d9d20d05637d711581f2cc21a254, working tree of revision 5)

**Why it moved.** The fill-pass task asked whether any result paper 1 still prints rests on the automated reference
(LEVELCHECK_MODEL.md section 14: three readers combined under a rule fixed by commit b511985, calibrated on
CTSpinoPelvic1K and VerSe reader truth). None does. The COBRA2026 screen counts of Table 2 note e and the Results
("seven at-risk persons with an exported frame") are the *two-labeller* count (SPINEPS+VERIDAH and a TotalSegmentator
rib count, both junctions in the field), not the three-reader rule; the three C-ArmLSpine L6 are scored against one
labeller's read; no ordinary-person real-frame result is printed. So the supplement paragraph, its `\PENDING{G6}`
calibration, the pre-registration paragraph that recorded its commit, the Methods sentence that introduced it and
the Discussion sentence that qualified it moved here verbatim. `PAPER1_SCOPE.md` item 3 kept them "for the open-gate
ordinary-person result, if it lands"; that item now says the paragraphs return from here if such a result is printed
(and that paper 2 must then log that H6's stratum was seen). The frozen files were not touched:
`results/fig6/frozen/auto_reference.json` (sha256 `57782cad4ec3b2b05ef6986ccc0048f3c99bdae7675b713ae3217ac6a3d04229`),
`auto_truth.csv` (`aa306deb…`), `results/auto_reference/CALIBRATION.md`.

### 8a. Supplement paragraph — `supplement.tex` lines 242-249 (revision 5)

```latex
\textbf{Automated reference standard.} For a transitional test person without a human read, three readers (the
segmentation tool's ordered names behind the guard above; TotalSegmentator bodies and ribs counted geometrically;
a direct rib-to-vertebra count on the CT, and for COBRA2026 the same on the planning CT and the cone-beam CT of one
patient) are combined under a rule chosen on CTSpinoPelvic1K and VerSe reader truth with test persons excluded:
the rule with the highest coverage whose positive predictive value per subtype keeps a Wilson lower bound of
0.90. The rule and its calibration are written with their SHA-256 before any test person is scored; the
calibration is \PENDING{G6}{automated-reference calibration: positive predictive value, sensitivity and coverage
per subtype, and the frozen rule}.
```

### 8b. Supplement pre-registration paragraph — `supplement.tex` lines 251-253 (revision 5)

```latex
\textbf{Pre-registration.} The automated reference and its selection rule were fixed by a dated repository commit
before any test person was scored (24 September 2026, 05:29; b511985). A committed section is never edited; a
change is a new commit before scoring that records the old value, the new one and the reason.
```

### 8c. Methods sentence — `sections/methods.tex` "Reference standard", lines 56-58 (revision 5)

```latex
Test persons without a human
read take an automated reference, three readers combined under a rule fixed by commit before scoring (supplement),
its measured error carried into every result resting on it.
```

Also the header comment of `sections/methods.tex` line 5, "(with the automated reference of LEVELCHECK_MODEL.md s14,
detailed in the supplement)", and of `supplement.tex` line 28, "the automated reference (LEVELCHECK_MODEL.md s14;
calibration PENDING G6) and the five pre-registration commits".

### 8d. Discussion sentence — `sections/discussion_limits.tex` line 16 (revision 5)

```latex
Where no person read a test spine, its reference is automated, with its error measured, not removed.
```

At the committed HEAD (887e37c, `sections/discussion_limits.tex` line 13) the same sentence read, one word longer:

```latex
Where no person read a transitional test spine, its reference is automated, with its error measured, not removed.
```

(the restructure pass of revision 5 dropped "transitional" before the fill pass moved the sentence; both wordings
are recorded so that the diff against HEAD matches this file).

### 8e. The paragraph filled from the frozen file (ready for paper 2, or to return to paper 1)

Every number below is a pointer into `results/fig6/frozen/auto_reference.json` (the keys are in
`numbers_manifest_moved.json`, section "automated reference"); nothing is typed. The frozen rule is *per subtype*:
no rule reached a PPV Wilson lower bound of 0.90 for every subtype it assigns, so the reference certifies **ordinary
persons only**, under Dawid–Skene at posterior ≥ 0.95, and assigns no transitional subtype (an L6, T13 or four-lumbar
call is excluded with the reason written in `auto_truth.csv`).

```latex
\textbf{Automated reference standard.} For a test person without a human read, three readers (the segmentation
tool's ordered names behind the guard above; TotalSegmentator bodies and ribs counted geometrically; a direct
rib-to-vertebra count on the CT, and for COBRA2026 the same on the planning CT and the cone-beam CT of one patient)
are combined under a rule chosen on \RESULT{autoref_n_calibration} CTSpinoPelvic1K and VerSe persons with a human
read on the train and validation sides (\RESULT{autoref_n_test_in_calibration} test persons): the rule with the
highest coverage whose positive predictive value per subtype keeps a Wilson lower bound of
\RESULT{autoref_ppv_lb_min}. No rule met that bound for every subtype it assigns, so the frozen reference assigns
ordinary persons only, by Dawid--Skene at posterior \RESULT{autoref_ds_threshold} or above: coverage
\RESULT{autoref_ds_coverage_pct}\,\% (95\,\% CI: \RESULT{autoref_ds_coverage_lo_pct}, \RESULT{autoref_ds_coverage_hi_pct}),
ordinary positive predictive value \RESULT{autoref_ds_ord_ppv} (\RESULT{autoref_ds_ord_ppv_lo},
\RESULT{autoref_ds_ord_ppv_hi}; \RESULT{autoref_ds_ord_correct} of \RESULT{autoref_ds_ord_assigned} assigned,
the errors \RESULT{autoref_ds_ord_wrong_l6} L6 and \RESULT{autoref_ds_ord_wrong_t13} T13), sensitivity
\RESULT{autoref_ds_ord_sens}. Unanimity of the three readers named L6 in \RESULT{autoref_unan_l6_correct} of
\RESULT{autoref_unan_l6_assigned} persons, but that count bounds its positive predictive value only at
\RESULT{autoref_unan_l6_ppv_lb} and L6 is not certified; T13 and the four-lumbar sacralised L5 were assigned
correctly in too few persons to qualify. The rule, its parameters and every person's assignment were written with
their SHA-256 before any test person was scored (commit b511985; frozen file 57782cad).
```

Pointers (file `results/fig6/frozen/auto_reference.json`; `fmt` in the moved manifest):

| key | pointer | value at freeze |
|---|---|---|
| `autoref_n_calibration` | `/calibration_table/dawid_skene/n_calibration` | 945 |
| `autoref_n_test_in_calibration` | `/calibration_set/test_persons_in_calibration` | 0 |
| `autoref_ppv_lb_min` | `/parameters/ppv_wilson_lower_bound_min` | 0.90 |
| `autoref_ds_threshold` | `/parameters/ds_posterior_threshold` | 0.95 |
| `autoref_ds_coverage_pct` (+ `_lo_pct`, `_hi_pct`) | `/calibration_table/dawid_skene/coverage/0` (1, 2), `pct_of` | 88.6 (86.4, 90.4) |
| `autoref_ds_ord_ppv` (+ `_lo`, `_hi`) | `/calibration_table/dawid_skene/per_class/ordinary/ppv/0` (1, 2) | 0.971 (0.957, 0.981) |
| `autoref_ds_ord_correct` / `_assigned` | `/calibration_table/dawid_skene/per_class/ordinary/n_correct`, `/n_assigned` | 769 / 792 |
| `autoref_ds_ord_wrong_l6` / `_wrong_t13` | `/calibration_table/dawid_skene/per_class/ordinary/wrong_truths/L6`, `/T13` | 22 / 1 |
| `autoref_ds_ord_sens` | `/calibration_table/dawid_skene/per_class/ordinary/sensitivity/0` | 0.881 |
| `autoref_unan_l6_correct` / `_assigned` | `/calibration_table/unanimity/per_class/L6/n_correct`, `/n_assigned` | 14 / 14 |
| `autoref_unan_l6_ppv_lb` | `/calibration_table/unanimity/per_class/L6/ppv/1` | 0.785 |

The `ppv`, `sensitivity` and `coverage` arrays in that file are `[point, lo, hi]`, so `results_macros.py`'s `ci`
kind (which reads `[lo, hi]`) must not be used on them; each element is its own key.

---

## 9. Packet, ledger and card passages brought into line (2026-09-24, late evening; the packet pass)

The files this section lists are outside the tex and were named "open" in section 8's "Not moved, flagged for paper
2's own ledger" and in `REVISION_LOG3.md` section 8. Each was brought to paper 1 as restructured; the passages that
described the comparison are reproduced here verbatim before their replacement, as the rule of this file requires.

### 9a. `packet_src/cover_letter.md` (state at commit 5fc6a31)

The paragraph "What it does not show", replaced:

```
**What it does not show.** Public releases hold three persons with a real transitional C-arm exposure, and a 95% lower bound above LevelCheck's published 97.6% needs 157 error-free transitional persons. The manuscript therefore reports what the transitional comparison can decide at the size available: [[PENDING G6: one sentence with the frozen comparison per stratum, k of n persons and Holm-adjusted P, worded as LEVELCHECK_MODEL.md section 6 allows, and the reference behind those persons (human-verified or the pre-specified automated reference with its calibrated PPV)]]. The title names the comparison the study was built to make; the comparator is a model of registration-assisted labelling built from its published literature, not a reader study with surgeons, and the manuscript reports the comparison in Figure 6 whichever way it falls. No naming accuracy is converted into a wrong-level surgery rate, and nothing has been evaluated prospectively.
```

The paragraph "The comparator was fixed before the result", removed whole (paper 2's cover letter can take it as it
stands; the commit list it rests on is `front_matter.json levelcheck_prespecification`, now six commits):

```
**The comparator was fixed before the result.** Because a comparison with an established method is the easiest to tune, LevelCheck was modelled from its published literature and frozen in a file committed to the study repository on 23 September 2026 at 19:50 EDT (commit ecae75f), before any held-out transitional person was scored: the comparator value for each stratum (82.2% for persons at risk of a naming error, the most favourable published accuracy of a planning read made without a count from C2), the person-level endpoint, the frame drawn per person, one-sided exact tests with Holm adjustment, and the rule that a hypothesis is tested only when its stratum reaches the size at which an error-free result can pass (19 persons at risk). The file was then amended three times, each before unblinding and by a new commit under its own amendment rule, and no amendment changed a comparator value, stratum, endpoint, test or primary hypothesis: secondary analyses of the count against the count plus morphology, a transitional flag and a dual-loss model (commit 1897772 at 20:50 EDT, with its stated time corrected in efab8dd); accuracy when the network accepts a frame, always printed beside the share of frames it accepts (commit 2993f40 at 20:58 EDT); and, on 24 September at 05:29 EDT (commit b511985), an automated reference standard for test persons whom no person has read, its consensus rule chosen on human-read CT and frozen before testing, with human-verified truth kept primary wherever it exists. The file lists every transitional development result that had been seen when it was written. The evaluation recorded its unblinding at [[PENDING G6: UTC time and git HEAD from the G6 evaluator's record, with ecae75f and every amendment among its ancestors and earlier than that time]]. The file and its commit history are available to reviewers.
```

(A fourth amendment, d0403de of 24 September 08:09 EDT, section 15, the primary detector, was not yet named in that
paragraph; paper 2's letter must add it.)

From "Why this journal", the clauses "and a clinical comparator" and ", and a comparator frozen before unblinding".
The letter's headline numbers were also brought from the first-run cells (594 / 606 / 571 / 1,162 / 995) to the
v9-lineage cells the manuscript prints; that is the G5 fill, not the move, and is recorded in `packet_src/README.md`.

### 9b. `packet_src/front_matter.json`

`trial_registration.value`, replaced by "Not a clinical trial; not registered.":

```
Not a clinical trial; not registered. The LevelCheck comparator was frozen by a dated repository commit (ecae75f, 23 September 2026) before any held-out transitional person was scored, and amended three times by dated commits before unblinding (1897772 with efab8dd, 2993f40, b511985); no amendment changed a comparator value, stratum, endpoint, test or primary hypothesis.
```

`author_decisions` item `comparator_public_deposit` (kept in the file under `moved_to_paper2_2026-09-24`; it is
paper 2's decision):

```
Whether to deposit LEVELCHECK_MODEL.md publicly now, with a timestamp outside git, before G6 unblinds. It would answer CLAIM 42 and let a reader check 'pre-specified'; it identifies the author, so an embargoed deposit or 'available to reviewers' are the options. The letter currently says the file and its commit history are available to reviewers.
```

The `levelcheck_prespecification` block stays in paper 1's front matter, marked paper-2 material, every commit
`in_letter=false`, with d0403de added: the builder keeps checking the frozen file's git history so a new commit to
it is noticed, which is the guard `PAPER1_SCOPE.md` asks for.

### 9c. `packet_src/statements.md`

From `DATA_SHARING_FULL`: "the file that froze the LevelCheck comparator before unblinding (LEVELCHECK_MODEL.md;
commit ecae75f and its three pre-unblinding amendments),". From `DATA_AVAILABILITY_MANUSCRIPT`: ", and the file that
froze the LevelCheck comparator before unblinding, with its dated amendments,". From `WEIGHTS_OPTION_DEPOSIT`,
`WEIGHTS_OPTION_AGREEMENT` and `CODE_AVAILABILITY_MANUSCRIPT_AGREEMENT`: "the comparator file". Edit-phase notes 8
(the automated reference in the Methods when Figure 6 lands) and 9 (the amendment history wherever "frozen" appears)
are marked moved in place.

### 9d. `CLAIMS_LEDGER.md`, `claim_checklist.json` / `CLAIM_CHECKLIST.md`, `packet_src/claim2024/map.json`

Ledger rows marked moved in place (section 9 of that file lists them). CLAIM 2020 item 2's gap ("the LevelCheck
result (G6)") closed as moved; CLAIM 2024 items 2, 6, 14, 16, 18, 20, 21, 24-26, 28, 34, 36-38 and 42 re-pointed,
`fig:levelcheck` and `tab:levelcheck` removed from every placement. Item 42 (reference to the full study protocol)
is answered "No" for paper 1; the protocol `LEVELCHECK_MODEL.md` is paper 2's item 42.

### 9e. ATLAS cards (`atlas/update_cards.py`, regenerated `model.json`, `dataset.json`)

Removed from the model card: "the comparison with a LevelCheck model frozen before unblinding is pending
(SchwingNet/LEVELCHECK_MODEL.md, gate G6)"; keyword "LevelCheck comparison"; Limitations (5)-(6) on the 157 / 152
persons against 97.6 % and the comparator "a model, not a measurement"; the Recommendation clause "quote only the
frozen comparison (LEVELCHECK_MODEL.md) once gate G6 has run"; Model performance "TRANSITIONAL: the comparison per
stratum against [the frozen model] is pending gate G6". From the dataset card: the Test partition's comment on the
automated reference and "Scored in Figure 6 against the frozen LevelCheck model (gate G6, pending)". The constant
`LC_FROZEN` (the amendment history) stays in the updater for paper 2's card and is no longer printed.

### 9f. `figures/figure5.caption.txt`

The tool-written sidecar carried the panel (b) clause "(b) Exact-test power at a true 95 % against modelled LevelCheck
accuracies (curve labels, %); dashed, Holm α/3; dotted, true 99 %." It now equals the main.tex legend and opens with a
header line saying `tools/fig_power.py` regenerates it (that script's caption string still carries the clause; item 4).

## 10. Table S2, the flagship-detector rows (dropped from paper 1 on 2026-09-24 21:45; Greg: report in paper 2)

From `tables/tab2_detection.tex` (three blocks: C-ArmLSpine, COBRA2026, DeepFluoro), removed at commit after 1dba814. Why: the row is
`det_g3_primary_s0` (LEVELCHECK_MODEL.md s15, trained on the G3 train side of every device) and can be scored only on G3 TEST frames,
which include the transitional persons paper 1 does not score (PAPER1_SCOPE.md); paper 2 scores it on the unblinded test set. The
caption clause "the vertebral-body convention of the human truth is pending gate G5" became "the all-device detector trained on
vertebral-body boxes is reported in the separate held-out study". Rows verbatim:

```latex
 & Flagship on vertebral-body boxes, patient-disjoint split & \PENDING{G5}{C-ArmLSpine body recall 0.74} & \PENDING{G5}{C-ArmLSpine sacrum 0.74} & \PENDING{G5}{C-ArmLSpine body recall 0.25} & \PENDING{G5}{C-ArmLSpine sacrum 0.25} & \PENDING{G5}{C-ArmLSpine PR-AUC} \\
 & Flagship on vertebral-body boxes, patient-disjoint split & \PENDING{G5}{COBRA body recall 0.74} & \PENDING{G5}{COBRA sacrum 0.74} & \PENDING{G5}{COBRA body recall 0.25} & \PENDING{G5}{COBRA sacrum 0.25} & \PENDING{G5}{COBRA PR-AUC} \\
 & Flagship on vertebral-body boxes, patient-disjoint split & \PENDING{G5}{DeepFluoro body recall 0.74} & \PENDING{G5}{DeepFluoro sacrum 0.74} & \PENDING{G5}{DeepFluoro body recall 0.25} & \PENDING{G5}{DeepFluoro sacrum 0.25} & \PENDING{G5}{DeepFluoro PR-AUC} \\
```
