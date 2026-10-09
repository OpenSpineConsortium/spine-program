# Revision log 2: the manuscript drive of 2026-09-24

Owner while this ran: `manuscript-drive` (`SchwingNet/.manuscript_owner`, written 08:07, deleted at the end).
Scope: `main.tex`, `sections/*.tex`, `tables/*.tex` (Tables 1-4, S1, S2), `supplement.tex`, `refs.bib`,
`NUMBERS.md` (new section "Revision 2"), `tools/make_supp_device_table.py` (Table S1 generator). Nothing was committed.
Figure files (`figures/figure*.*`, `figS*.*`) belong to the figure workflows and were not written; where the printed
legend differs from a `figureN.caption.txt`, `main.tex` says so beside the figure. Every number that entered or left
the text is a row of NUMBERS.md "Revision 2 (2026-09-24, manuscript-drive)".

Inputs applied, in the order the task gave them: (0) `results/eval_gate/EVAL_LEAKS.md` (and its closure,
`results/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md`), `LEVELCHECK_MODEL.md` s14-s15, `DRIVE_CHECK.md`;
(1) `REVIEW2_RSNA.md`, `REVIEW2_STATS.md`; (2) `refs_corrections.bib` per `REFS_AUDIT.md`; (3) supplement figures;
(4) the in-domain Figure 5 (not present: kept PENDING); (5) limits, then key points, summary statement and abstract.

## Final state

`python tools/check_limits.py` after the last edit (see the end of this file for the full count block):

- Body (Introduction to Discussion) **2,963 of 3,000**, counting the text of the open placeholders. Abstract
  **238 of 250**. Summary statement **242 of 255** characters. Key points 3, no abbreviation. Six figures, each
  with four components and a legend of at most 60 words (59, 60, 59, 59, 52; Figure 6 45). Four tables, titled,
  no merged cell. **34 references cited, each with a DOI** (limit 35). Seven abbreviations.
- Style greps 0; banned word 0; Discussion cites no figure or table; limitations second-to-last.
- `RESULT: FAIL` on the open placeholders only: G0 7, G4 1, G5 22, G6 10 numbers and the Figure 6 file.
- Headroom. What the gates still owe the body (G5 fine-tuned and coupling sentences, the Figure 5 data case, G6,
  G0 age and sex) is about 250 words against about 90 words of placeholder text now counted, so **about 125 more
  words must be cut when they land** (candidates at the end).

## (0) Held-out rule: EVAL_LEAKS.md and its closure

| item | what changed | where |
|---|---|---|
| U1, zero-shot (UNRESOLVED: `allspine_v2_r1` training bank deleted) | Replaced by the certified re-score `zeroshot_v9` (v9 encoder + recurrent head; eval_gate HELD OUT, overlap 0, all 148 cases): lateral 595/617 = 96.4 % (Wilson on n_eff 92.3, 98.4), AP 276/631 = 43.7 %, paired +54.3 (45.6, 62.9), 79 vs 1 cases; 88.0 % of all 676. It is the network the Methods describe (encoder + GRU head); the first run had no head. The first run's 594/617 and 239/631 are disclosed in Table 4 note h, not used. Why not PENDING: EVAL_LEAKS names this file as the U1 replacement and it passes the strict gate; the task's `cv_v9` condition concerns the fold models, which have no replacement yet. | Key Point 1, abstract, Results, Discussion, Table 4 rows 1-2 and notes b, h; Methods "Naming, counting and coupling" |
| U1, fold models (case- and day-grouped, field sizes, classifier, coupled call, stop signal, L6 calls; 57 rows) | `\PENDING{G5}{C-ArmLSpine CV on the v9 lineage}`: `results/eval_gate/closure/cv_v9/` holds only its scripts (grid jobs `carmcv9i` 40431706 still running at 08:13). Also the zero-shot three- and one-body fields (86.9 %, 63.1 %: same unresolved encoder). | Key Point 2, abstract, Results (two placeholders), Table 4 (five rows), Figure 4 legend comment |
| count from the sacrum alone | Kept: uses no level encoder, CLEAN (`FIGREC:figure4/07-12`): 979/1,009 at 0.74; 1,104/1,149 at 0.25. | Key Point 2, abstract, Results, Discussion, Table 4 |
| detection counts | Kept, CLEAN: 617/676 (`figure4/00`), 233 sacrum boxes (`figure4/01`), a1 231/287 and 43/56. | Results |
| L4 plain-film naming (v8 selection split) | Already labelled "selection split" in Table 4 and not quoted in the text; Table 1 role column now "checkpoint selection"; Table 4 note f adds that no held-out plain-film accuracy exists until the Figure 6 model is scored (closure 3c). | Tables 1, 4 |
| L5 embedding (v9 selection split) | Labelled wherever quoted: Results paragraph opens "On the checkpoint-selection split"; abstract "On the checkpoint-selection split"; Key Point 3 "On the split that chose its checkpoint"; summary paragraph "on its selection split"; Table 3 note a (render L6 recall 56.1-72.4 %). DRIVE_CHECK D3. | abstract, Key Point 3, Results, Discussion, Table 3 |
| L2 render vs film | Replaced by the 17 NHANES II spines neither detector saw: 99.4 % vs 67.7 %, +31.7 (21.0, 45.4), 16 vs 0 (closure 3a); "in-sample for 196" removed. | Supplement, Table S2 rows, notes a, f |
| L6 device-card gain | Replaced by the 12 patient-held-out folds, +0.0193 (0.0076, 0.0326), P=.004 (Holm .009); within-subject folds named (closure 3b); the device-level P=.13 retired. Table S1 generator writes "held-out" or "within-subject" per device; Table 1 Geneva and Ljubljana cells and note k; Figure S3 legend. | Supplement, Tables S1 and 1 |
| Holm family | Recomputed with the replaced members (closure 4): sacrum P=.009 (was .008), card P=.009; lateral vs AP from the v9 run (Holm 5.4e-22, printed P<.001). | Supplement, Methods |
| closure 2.4 (implant-render key alias; 192 and 164 persons) | Table 1 note c replaced as written. The optional Methods clause (+14 words) not taken for length. | Table 1 |

## (0) LEVELCHECK_MODEL.md s14 and s15, in the Methods

- s14: "Held-out transitional persons without a human read take an automated reference specified by commit before
  unblinding: three readers combined by the rule keeping a per-subtype positive predictive value above 90 % (Wilson
  lower bound) on reader truth (Table 3), its measured error carried into every result resting on it." "Specified
  by commit" is exact (b511985 commits the selection rule); the rule itself is frozen later (s14 R2).
- s15: "Because the device-held-out sacrum detector anchored 21 of 609 COBRA2026 development frames (3.4 %), the
  primary detector was changed by commit before unblinding to one trained on the split's training persons of every
  device (patient-held-out, device seen); the device-held-out detectors are a secondary analysis." Table 3 note c
  says the same. The Methods now also state the s4 failure modes (missed body, unanchored frame, abstention) that
  REVIEW2_STATS N1 found missing.

## (0) DRIVE_CHECK.md

| item | status |
|---|---|
| D1 "631 anteroposterior in 142" called agreed truth | Fixed: 673 agreed AP vertebrae in 143 cases (`docs/carmlspine_cv5_mixed_2026-09-21.json#/oracle/AP/kfull`); 631 appears only as the detected count. |
| D2 fine-tuned numbers credited to the unseen network | Fixed by construction: the Discussion quotes only the held-out 96.4 % and 97.0 %; every fine-tuned number is PENDING and labelled fine-tuned where its placeholder stands (Results, Key Point 2, Figure 4 legend "(b) ... fine-tuned on other cases"). |
| D3 silhouettes unqualified in the abstract and Key Point 3 | Fixed (see L5 above). |
| 5 G0/G4 placeholders | Not fixable by text: G0 first download date, age and sex (twice), and G4 corpus census stay; three G0 added (reader postgraduate years; VinDr determination; date the C-ArmLSpine authors were notified). |
| 3 Figure 5 data-case panels | No `results/indomain/fit.json`, so `\PENDING{G5}{the data case ...}` in the Results; the Figure 5 legend is the rebuilt figure's own caption. |
| 7 undefined abbreviations | F1 and JSON left the text; C2 spelled out at first use (Introduction); the list now reads BCa, C2, CI, GRU, L1-L6, T11-T13, t-SNE (7). |
| 8 references | refs_corrections.bib merged; hsiang2011 (dead DOI) no longer cited; Furuya "consecutive patients", Mody "responding"; Huang 2022 worded from its abstract ("long-length (Long-Film) images of cadavers"; "tomosynthesis" and "about 17 vertebrae" removed from Introduction and Discussion); overlap sentence fixed (see Fix 21). |
| 10 packet | Not in scope (packet files are built by `tools/make_packet.py`); rebuild after this revision. The docx metadata paths, the cover-letter sentences ("the Methods cite the descriptor" is now true; "SchwingNet throughout" is now true of the abstract, Key Points and text; the "three persons with a real transitional exposure" sentence still contradicts the manuscript) are for the packet owner. |
| 11 network name | SchwingNet now in the abstract (Purpose, Results, Conclusion), all three Key Points, the summary statement, the Introduction's purpose, Results, Discussion and summary. Figures 1-5 still print "the network" on the figure (figure owners). |
| 11 title dash | "convolutional-recurrent" with a hyphen, as in TITLE.md (main.tex and supplement.tex). |
| Also found: COBRA 152 vs 145 | Methods: "145 of 467 Elekta cases; seven of 152 downloaded failed a pre-export check". |

## (1) REVIEW2_RSNA.md, fix by fix

| fix | status |
|---|---|
| 1 Ethics: case134 directory "excluded" | Replaced as written; the notification date is `\PENDING{G0}{date notified}` (no record of the report was found). The question to the HRPP office stays with Greg. |
| 2 VinDr-SpineXR under a DUA; FluoroCap not a release | Ethics sentence with `\PENDING{G0}{determination covering it, or its removal from the fold models}`; Data availability sentence replaced; Table 1 title "one row per collection"; Methods first paragraph drops "public". |
| 3 fine-tuned numbers | See D2; the replacement numbers A1a-A1c are fold-model numbers and are PENDING. A1d applied without its numbers. Figure 4 legend per the fix, with "a stop, not a verdict" (Fix 17). The on-figure panel (b) text is the figure owner's. |
| 4 title | Not applied: the title is fixed by TITLE.md (Greg). Recorded here and in the main.tex header. |
| 5 anonymization | Guarantor and COI were already out; "the author is responsible" (singular) replaced by "responsibility for the content rests with the authorship stated on the full title page". |
| 6 citations | C-ArmLSpine (`carmlspine`, DataCite read 2026-09-24: Feng Q, Zenodo 2026), Geneva (`genevahip`, Yareta dataset, CC BY-SA 4.0 also added to Ethics), Ljubljana (`ljubljana2d3d`, Tomaževič 2002 LNCS 2489:461-468, the paper the laboratory names), Castellvi (`castellvi1984`, at first mention), the descriptor (`ctsp1kdescriptor`) added; refs_corrections.bib merged into refs.bib (rsnastyle.tex loads refs.bib only). Liebrand 2026 not cited: the cap (35) leaves one slot, kept for Figueroa 2012 when the Figure 5 extrapolation paragraph lands. |
| 7 silhouette "more than any lumbar level" | Replaced: "more than L2-L5 from the level above ... and as far as L1 from T12 (0.32; 0.29, 0.35)", with the leave-person-out 0.34. |
| 8 Table 4 missing rows; day-grouped below zero-shot | The rows are fold-model numbers and are PENDING; the table comment tells the filler to add the zero-shot and day-grouped field rows. B4 (limitations) waits for the re-run: the discussion_limits.tex header says to add it if the v9 day-grouped result again falls below the zero-shot 96.4 %. The two suspect coincidences (610/631, 513/617) are in the PENDING block. |
| 9 coupling vs shape alone | The Results placeholder asks for "against the count and the classifier"; the Discussion no longer mentions coupling. |
| 10 Key Point 3 | Applied, with "at-risk". |
| 11 reader training | Methods: two radiology residents (in-training; `\PENDING{G0}{postgraduate years}`), independent grades, six disagreements by consensus, cited to the descriptor. The years are not in the descriptor. |
| 12 occlusion and fused L5 | Occlusion by share and density (B2); fused L5 stated plainly in the Results and in full in the supplement; Discussion S1 applied. |
| 13 COBRA best case | Superseded: the rebuilt Figure 5 (08:26) replaced the 57 "supported" calls with the two-labeller harvest (7 at-risk persons with a frame; 64.6 %). The abstract drops the best case (ABS2); the Results give the harvest count with the labeller's 10 of 24 and 0 of 52. |
| 14 stop signal | Methods: "or a margin over the next-best alphabet below the fifth percentile of correct frames in the other folds"; Table 4 note d. |
| 15 summary statement | Applied, with SchwingNet (242 characters). |
| 16 truth boxes | Verified against `tools/carmlspine_eval.py` lines 10-11 and 95-102 and `coupling.json#definitions/truth`; Methods sentence and Table 4 note b. |
| 17 Figure 4d | Legend "a stop, not a verdict"; the on-figure title is the owner's. |
| 18 Figure 1 ages and sex | Legend carries them (60 words); it now differs from `figure1.caption.txt` (08:24), noted in main.tex. |
| 19 COBRA 152/145 | Applied. |
| 20 dates | Methods first sentence without "2020-2026"; abstract "analysed \PENDING{G0}{first download date}-September 2026; intraoperative exposures November-December 2023". |
| 21 prior report | "Every subject was reported by the release or article it comes from; the CTSpinoPelvic1K subjects were also reported in a data descriptor \citep{ctsp1kdescriptor}." |
| 22 summary paragraph | "is untested: ... needs at least 19 verified at-risk persons ..., and none is verified." |
| 23 two sacrum numbers | "a sacrum box on 233 of the 286 frames showing one (81.5 %)" (with REVIEW2_STATS N15). |
| 24 numerator | 9,740 of 13,009. |
| 25 subheadings | Methods and Results share "Sources and transitional phenotypes", "The level encoder and what it learns", "Naming, counting and coupling on the intraoperative C-arm", "Transitional sample size", "The LevelCheck comparison". |
| 26 slang | Methods F1 and script names gone; Table 1 notes b, c, h, i, k and the COBRA released cell; Table 2 note d. On-figure items (Figure 3a, Figure 5 legend) are the figure owners'. |
| 27 Figure 5 panel b | The figure was rebuilt at 08:26; its own caption (dashed Holm alpha/3, dotted true 99 %) is printed verbatim. The 20.8 % curve is still not named in the legend: for the figure owner. |
| 28 Figure 6 fallback | Not decided here (a commit beside the frozen file, Greg's decision). |
| 29 Introduction wording | Applied. |
| cuts | CUT1 (Discussion), CUT2 (script names), CUT3 (per-source L6 counts), CUT5, CUT6, CUT8 applied; CUT9 applied in a shorter form that keeps s14 in the Methods; C8 applied (the Wilson 35/157 left the text; they remain in Figure 5a and Table 2 note f); the never-seen and fused-L5 detail moved to a new supplement section with every number. |

## (1) REVIEW2_STATS.md

| item | status |
|---|---|
| N1 endpoint decided by detection | Methods: the failure modes of s4 stated; "an assumed accuracy of 95 %, which no transitional measurement supports"; the COBRA anchoring figure (21 of 609) given as the reason for s15. The development endpoint rates (162 of 284; 54 of 284) are not quoted: they rest on the fold models (UNRESOLVED). U1-U4 are the author's (see "Open for Greg"). |
| N2 | See D2. |
| N3 coupling | Numbers PENDING; the placeholder asks for the comparison with the classifier. |
| N4 stop signal | Methods and Table 4 note d; the 22/233 and 79/290 are fold-model numbers, PENDING. |
| N5 L6 false positives | "111 of 1,012 L5 crops L6". |
| N6 | (a) L1 from T12 added; (b) ten persons stated; (c) "one crop each"; (d) occlusion by share. |
| N7 | 0 of 52 T13 added in Results and Table 2 note e; the best case replaced by the harvest (Fix 13). |
| N8 | (a) Table 3 note d; (b) abstract and Key Point 3 qualified. |
| N9 | Superseded by the closure's Holm family (card member = 12 patient-held-out folds, P=.009). |
| N10 | Table 3 note c. |
| N11 | "at least 19" (Results, summary paragraph); "152 error-free at-risk persons" (abstract, Key Point 3). |
| N12 | "Pre-stated targets on pooled at-risk test persons ... sit outside the frozen tests' multiplicity control". |
| N13 | "one-sided .025 for the frozen comparison". |
| N14 | 9,740; the 70 of 1,066 moved to the supplement with the fused-L5 detail. |
| N15 | 233 of 286. |
| N16 | Wording "are fixed before unblinding" (configuration) and "specified by commit" (s14). True only if the G5 manifest and `slurm/fig6_*.sh` are committed before `RELEASE_v2.json`: see "Open for Greg". |
| N17 | Python 3.11 and 3.12; SciPy 1.15.3 and 1.18.1. The rigor tool revision is not named (the code is private; the Code availability paragraph covers deposit at publication). |
| N18 | Table S2 [0.1, 1.9] and [1.8, 14.6], note g. |
| N19, N20 | Abstract "Intervals were cluster-adjusted"; "detected lateral vertebrae". |
| N21 | Supplement: "the crops are three patients, not 180 observations"; the L3-L5 negatives do not discriminate. |
| F22 "148 cases" in the abstract | Kept (the scored set); Key Point 1 gives 141 cases for the primary endpoint. |

## (2) References (REFS_AUDIT.md)

- `refs_corrections.bib` merged into `refs.bib` by key (every corrected entry replaces its old entry; the audit's
  comments carried); castellvi1984, ctsp1kdescriptor, figueroa2012, liu2021ctpelvic1k added (the last two uncited);
  schwing2026mixed, dea2016 and kanmounye2021 removed (uncited; the first carried the author's GitHub path). The merge
  script is in the session scratchpad (`rev2/merge_refs.py`); do not re-run it on the merged file.
- New: `carmlspine`, `genevahip`, `ljubljana2d3d` (records read from DataCite and Crossref on 2026-09-24).
- Cited now: 34 (30 - hsiang2011 + castellvi1984, ctsp1kdescriptor, carmlspine, genevahip, ljubljana2d3d).
- `tools/make_refs.py` regenerates refs.bib from `paper/rsnai/refs.bib` and would undo this; apply the same
  corrections upstream before it is run again (REFS_AUDIT style item 6).

## (3) Supplement figures S1-S4

Already wired before this drive (figS1-figS4 print as Figures S2-S5, fig2_flow as S1; fig_manifold and
fig5_contribution retired). This drive: the Figure S3 legend per closure 3b; header comment CLAIM 2024 item 35 (was
the 2020 item 33); new section "Transitional crops in the embedding"; the detector section names its box convention
and gives the body-convention values in brackets (REVIEW2_RSNA section 3); film-vs-render and card gain replaced;
Holm .009. Main-text citations: Figure S1 (Methods, Data availability), S2 and S3 (Methods), S4 (Methods), S5
(Ethics). `figS4.caption.txt` still says "Figure S3" (the print is right; the file is the figure owner's).

## (4) In-domain Figure 5

`results/indomain/fit.json` does not exist, so `RESULTS_PARAGRAPH.tex` was not integrated. The Results carry
`\PENDING{G5}{the data case: detection against same-device training frames and naming against same-device training
cases, lateral and anteroposterior (in-domain panels of Figure 5)}`. Figure 5 was rebuilt at 08:26 by its owner
(power panels with the COBRA2026 anomaly-harvest count); the Results and Table 2 now match that build.

## Tables

- Table 1: see (0) and Fix 26.
- Table 2: COBRA2026 column and the "real" Wilson bounds follow the rebuilt Figure 5 (L6 3, T13 0, four lumbar 4,
  pooled 7; 43.9, none, 51.0, 64.6); the Any row gives the at-risk bound 93.0 (51 CT); notes d, e, f.
- Table 3: notes a, c, d.
- Table 4: zero-shot rows from `zeroshot_v9`; fold-model rows PENDING (five rows; to be split one measurement per
  row when filled); count rows kept; notes b, d, f, h.
- Table S1: regenerated by the updated generator (within-subject / held-out).
- Table S2: plain-radiograph rows, zero-floor cells, notes a, f, g.
- The `.md` twins and `.sources.md` files of Tables 1-4 and S2 were NOT updated and lag the `.tex` for the cells
  listed above; the packet builds its tables from the `.tex`, and NUMBERS.md "Revision 2" traces every changed cell.

## Open for Greg (decisions, not text)

1. The ethics questions: does determination 2026-269 cover VinDr-SpineXR (PhysioNet DUA) and C-ArmLSpine (a release
   with a named patient in one directory)? Was the dataset authors' notification sent, and when?
2. REVIEW2_STATS U1-U4 before unblinding: s15 has now addressed the COBRA anchor (U1); U2 ("abstention" in s4), U3
   (commit the G5 manifest and `slurm/fig6_*.sh` before anyone reads `fig6_score_open.json`) and U4 (freeze
   `auto_reference.json` with its SHA-256) are open.
3. Figure 6 fallback (REVIEW2_RSNA Fix 28): commit it beside the frozen file before scoring.
4. The title (REVIEW2_RSNA Fix 4) stays as TITLE.md fixes it.
5. The postgraduate years of the two Castellvi readers.

## For the next writer (when G5/G6 land)

- Fill the five Table 4 PENDING rows from `closure/cv_v9/` (split per view and field; add zero-shot and day-grouped
  field rows); fill the two Results placeholders, Key Point 2 and the abstract; if day-grouped falls below the
  zero-shot 96.4 %, add REVIEW2_RSNA B4 to the limitations; redraw Figure 4 b and d from the v9-lineage folds.
- Word cuts available (about 125 needed): the Discussion's detection-versus-recall sentence (about 30); the Methods
  "Transitional sample size" paragraph into Table 2 note f (about 35); the Methods abstention sentence into Table 4
  (about 20); the Study population film/render subject counts into Table 1 (about 20); the Results within-source
  silhouette clause into the supplement (about 20).
- Rebuild the packet (`tools/make_packet.py`) and re-read the cover letter against this text.

## check_limits.py, final run

(pasted below after the last edit)

---

# Round 2 (2026-09-24, 10:24 onward; owner `manuscript-drive`, `.manuscript_owner` re-used)

Task: (00) integrate the uploaded acquisition-space review (`lit/acquisition_space_review_2026-09-24.txt`, an
AI-generated synthesis: nothing cited from it directly) once `lit/CITABLE_CLAIMS.md`, `lit/refs_additions.bib` and
`results/coverage/COVERAGE.md` arrive from workflow review-integration; (0)-(5) as in round 1, re-checked. The
round-1 `check_limits.py` block was never pasted (the session ended); the count block at the end of this round
stands for both.

## State found at 10:24

- Body 2,963 / abstract 238 / summary 242 characters / 34 references / 7 abbreviations; `RESULT: FAIL` on the
  44 open placeholders (G0 7, G4 1, G5 22, G6 14) and the missing `figures/figure6.pdf` only.
- `results/eval_gate/closure/cv_v9/` (local) holds scripts only. On the grid the collector `cv9icollect`
  (40436581) ran 09:03-09:10: `coupling_pre/`, `coupling_rep/`, `rigor_pre/`, `rigor_rep/` and the two
  intermediates `carmlspine_cv5_v9init_pre.json`, `carmlspine_cvday_v9init_pre.json` were written, but the gated
  closure `closure_cv_v9.py` **crashed** before writing `cv_v9.json`:
  `closure_cv_v9.py:176 min_det_conf: for v in r.get("vertebrae") -> AttributeError: 'list' object has no
  attribute 'get'` (log `~/logs/cv9icollect_40436581.out`, line 185). The pre-repair job `cv9iprerep` (40436575)
  FAILED at 08:20 as well. **Every G5 fold-model placeholder therefore stays PENDING**: the intermediates are
  not gate-certified (the gate runs inside the crashed step) and the task allows their use only from
  `closure/cv_v9/` replacements. For the coordinator: fix `min_det_conf` (the fold score files' `vertebrae`
  entries are lists) and requeue `collect_cv_v9.sh`; nothing else in that chain needs re-running. For the record,
  the intermediate (pre-repair truth, v9-initialised, case-grouped) reads lateral whole-frame exact 0.974 on
  617 vertebrae of 141 cases and anteroposterior 0.964 on 631 of 142; these are NOT quoted anywhere.
- `results/indomain/fit.json` and a rebuilt Figure 5 with in-domain panels: still absent (namefill/detfill
  intermediates only). The data-case placeholder stays.
- `results/fig6/` on the grid: absent; `f6eval` 40431765/66 held (JobHeldUser) as the coordinator said.
- `lit/CITABLE_CLAIMS.md`, `lit/refs_additions.bib`, `results/coverage/COVERAGE.md`: absent at 10:24; a watch
  was armed (30-minute arms, re-armed) and the integration below was written when they landed.

## Cuts made before the review text (room for it and for the G5/G6 fills)

| cut | words | where the number still lives |
|---|---|---|
| A: Methods "Transitional sample size": the Wilson 90 %/85 % targets named only as "pre-stated Wilson targets" with a pointer to Table 2 | -10 | Table 2 note f (90 %: 35 persons; 85 %: 22 carriers) |
| B: Results "Study population": the bracketed subject counts (801 patients, 1,935 scans, 355 subjects; 4,963 individuals, 3,600 cases, 364 persons) | -12 | Table 1 rows (each count present) |
| C: Results, encoder: the within-source silhouette clause (0.14 against 0.21; five persons) | -15 | supplement "Transitional crops in the embedding", first paragraph, now with all three sources and intervals (`results/figure2/figure2_metrics.json#silhouette_within_source`) |
| G: Methods "Reference standard": "The three C-ArmLSpine cases VERIDAH reads as L6 are read L1-L5 by TotalSegmentator; they measure agreement, not correctness." | -18 | Table 4 note e; supplement "Transitional crops" (the two labellers named); Methods still says the three patients are "one labeller reads as L6" and Results/Discussion call the L6 contested |

Body after the cuts: 2,908 (`check_limits.py`, 10:50).

## (00) The acquisition-space review, once `lit/CITABLE_CLAIMS.md` (10:39) and `lit/refs_additions.bib` (10:40) landed

Rule followed: nothing cited from the review itself; every sentence below rests on a CITABLE_CLAIMS row marked
VERIFIED, or on our own result files (NUMBERS.md "Revision 2, round 2").

| item | what the text now says | source |
|---|---|---|
| (i) plateau | Results (intraoperative paragraph): a vertebra detector fine-tuned on 50 C-ArmLSpine frames of 25 cases found 82.9 % (238/287; 7.0 % with none) at 0.74; from 50 to 210 frames every arm 81.5-86.8 % (234-249/287) with overlapping intervals; renders posed on all 148 cases' geometry. Methods: the nested whole-case design, two seeds, body boxes. Supplement, new section "Same-device frames and view angle": every row with its interval, the 0.25 range, the nesting, the pose-donor caveat. Discussion: "Detection, not naming, lost most to the unseen device, and same-device frames restored it only to a plateau reached by 50 frames" + the coverage framing (below, from COVERAGE.md). CITABLE_CLAIMS row 1: the "90 % plateau vs 99 % parity" is OUR result; stated uncited. Row 2: the saturation explanation is an assertion with no source; used only as far as COVERAGE.md supports it. | `results/indomain/INVENTORY.md` (GENERATED:detection_carm, HELD OUT rows; "Pose donors") |
| (ii) coverage-driven sampling | Methods: "Detection against view angle used +/-90 deg render pose pools per device and one patient's 301-frame rotational acquisition, the real pool holding only anteroposterior and lateral views (Figure S5)". Supplement: the real pool (148 within 10 deg of AP, 148 lateral, none between), the arc pools (592, 1,100, 4,216 poses; tilt about +/-13 deg), and the held-out render sweep on 40 unseen TS v3 subjects with the anchor floor (0.64-0.68) and the photon-starved Surgio lateral stated. CITABLE_CLAIMS row 3: coverage/entropy is our method, no attribution; the DICOM-tag rows (4-8) are not used (no DICOM tag is named in the text). | `results/arc/audit/pose_pools.json`; `results/arc/ARC_CHECK.md` s1; `results/arc/recall_vs_angle_unseen/` |
| (iii) periodicity / level jumping | Discussion, LevelCheck paragraph: "In simulation every registration failure was a one-vertebra shift from the spine's periodicity \citep{levelcheck2012}, later removed clinically by multistart \citep{levelcheck2016}; a count from the sacrum is off by one level on a transitional spine, and a label carried from a planning read fails with that read \citep{peh1999,nakagawa2017}. The comparator was therefore frozen ..., and local morphology is tested as a different mechanism, not a better optimiser." Rows 12 (VERIFIED: "translational shift in the superior-inferior direction by one vertebral height", all 47 failures "from the periodically symmetric structure of the spine") and 13 (the clinical series removed it: Lo 2015 100 % at 200 multistarts; the review's "catastrophic misalignment" is CONTRADICTED and is not used). No new reference: both keys were already cited. | CITABLE_CLAIMS rows 12, 13 |
| (iv) paired domain adaptation | Discussion, one sentence: "paired domain adaptation with 140 paired images cut a synthetic-trained pose regressor's real-radiograph failure rate from 16.1 % to 11.2 % \citep{zheng2018pda}" (row 11 VERIFIED: 420 real X-rays of 42 C-arm CT volumes, 1,000,000 synthetic pretraining images, failure = TRE > 10 mm, 16.07 % -> 11.20 %; pose regression, not naming, which the sentence says). Our residual gap: "Styled renders stayed separable from real frames (supplement)", the supplement's Corpus manifold section now giving the per-device styled-vs-real accuracies 100 %, 99.8 %, 99.0 % (736, 666, 771 frames; majority 50.3-64.7 %). | `refs_additions.bib` -> `refs.bib` (`zheng2018pda`, DOI 10.1117/1.JMI.5.2.021204); `figures/figS1.record.json#numbers/.../styled_vs_real` (source `results/manifold/probes.json`) |
| (v) patient-specific N = 1 | Discussion, one clause: "one patient's rotational acquisition paired with its cone-beam CT would admit patient-specific self-supervised registration \citep{diffpose2024}: both are future work" (row 18 VERIFIED; the review's "circumvents periodicity" inference has no source and is not used; XVR, row 19, is a preprint and not cited). | `refs_additions.bib` -> `refs.bib` (`diffpose2024`, DOI 10.1109/CVPR52733.2024.01108) |

**References: 35 of 35.** `zheng2018pda` and `diffpose2024` entered; `rao2024` left with the Discussion sentence
"Detection lost more than naming to the unseen device (80.5 %); published C-arm recalls (0.964, 0.982) ..." (its
place is taken by the plateau sentence, which makes the same point about detection from our own held-out data; the
CLAIMS_LEDGER row on Rao 2024 stands as a record, not a citation). `konin2010` and `he2016` stay. `figueroa2012`
(planned for a fitted curve) is not needed: no curve is fitted. `refs_additions.bib` is left in `lit/` untouched;
only the two cited entries were appended to `refs.bib` (rsnastyle loads refs.bib alone). `tools/make_refs.py` would
undo this (REFS_AUDIT style item 6): the same two entries must go upstream before it is run.

**Other Discussion edits for room:** P1's first two sentences merged; "No thoracic variant lay outside training"
dropped from P2 (the Results keep "No T13 crop was outside training"); P4's first sentence shortened to "Unlike
published registration-free naming ..., one lateral exposure sufficed here on ordinary spines"; the summary paragraph
drops "trained on rendered CT and radiographs" and "from the shape of the bodies in view" (both stand in the
summary statement, Key Points and P1); the limitations say "Held-out detector numbers use whole-vertebra boxes",
because the learning curve is reported in body boxes and says so.

**Methods trims for room:** "(checked for every scored case)" (Table 4 note h keeps it); the automated-reference
sentence shortened to "three readers combined under a rule specified by commit before unblinding (Table 3)" (the
rule is Table 3 note c); the stop-signal margin clause shortened (Table 4 note d has it in full). **Results trims:**
"The automatic labeller's COBRA2026 screen calls are unread" (said again two paragraphs later); "The intraoperative
set was 148 cases and 296 exposures" (Methods has both); the labeller-agreement parenthesis (Table 2 note e has
10 of 24 and 0 of 52); the never-seen/fused-L5 sentence compressed (every number in the supplement).

## Grid build 1 (job 40436989, 10:46; before the coverage sentence)

rsync of main.tex, rsnastyle.tex, supplement.tex, refs.bib, nejm.*, latexmkrc, sections/*.tex, tables/*.tex and the
ten figure PDFs the two documents include; `strip_cr.sh` stripped CR from refs.bib only; `sbatch -D ~/logs
slurm/compile.sh`. Whole log read (`~/logs/schwingnet_tex-40436989.out`): texlive/2020, TeX Gyre Termes;
`latexmk rc=0`, **main.pdf 28 pages**, `latexmk supplement rc=0`, **supplement.pdf 12 pages**; biber clean (no
warning in main.blg). main.log: 1 LaTeX warning ("There were undefined references"), which the 07:30 log carried
identically and which no "??" in either PDF's text bears out (stale summary line); **two Overfull \hbox in
`main.ttt`, new since 07:30**: 10.8 pt at lines 9-61 (Table 1) and 82.3 pt at lines 185-243 (Table 4), both from the
round-1 table edits of 08:33 (the tables are rotated minipages; each still fits its page, pages 19 and 22 rendered
and looked at, no clipped column or note). For the table owner: Table 4's tabular exceeds its 23.2 cm minipage by
about 2.9 cm; shorten a cell or widen the minipage. Both PDFs' text carries every new sentence and the two new
references (numbered 33 and 34 by first citation). The PDFs were not copied back over `main.pdf`/`supplement.pdf`
in the working tree (those stay the 07:30 packet builds until the packet is rebuilt).

## G5 fill: the C-ArmLSpine fold models on the v9 lineage (closure landed 10:35, extras 10:39, Figure 4 rebuilt 10:41)

The gated closure `results/eval_gate/closure/cv_v9/cv_v9.json` was written on the grid at 10:35 by `cv9iclosure`
40436862 after the `min_det_conf` bug was fixed (script updated 10:45 on the grid; local copy of the directory in the
session scratchpad, rsynced from the grid, not yet mirrored to the working tree by the closure workflow).
`cv_v9_extras_pre.json` (10:39) carries the paired comparisons. Every `pre:*` family reads `held_out: true, overlap 0,
unresolved 0`; the old families are refused by the strict gate and reproduced only for the record. Figure 4 was
rebuilt from the same files (`figure4.record.json`: models `v9init_pre`, every drawn input HELD OUT), and its record
says the manuscript must switch to the drawn values, which is this edit. PRE truth (the export every quoted
C-ArmLSpine number was scored on) is used throughout; the REP re-run is in the same file and not quoted.

| where | filled with |
|---|---|
| Results, intraoperative paragraph | case-grouped lateral 601/617 (97.4 %; Wilson 93.2, 99.0) and AP 608/631 (96.4 %; 92.5, 98.3); paired gains over zero-shot +1.0 (-1.9, 4.0) and +52.6 (44.1, 61.3); day-grouped lateral 568/617 (92.1 %; 87.5, 96.0), -4.4 (-9.1, 0.2) against zero-shot; three-body lateral 1,079/1,159 (93.1 %; 89.2, 96.2), one-body 451/603 (74.8 %); classifier 986/1,009 (97.7 %), coupled 991/1,009 (98.2 %; 96.5, 99.5), +1.2 over the count (0.0, 3.2), +0.5 over the classifier (-1.5, 2.4); stop on 23/233 anchored frames, 5 of 6 erring frames caught; four L6 calls all stopped (3 on five-lumbar frames, 1 of the 4 anchored frames of the three contested patients). A small `\PENDING{G5}{zero-shot three- and one-body fields on the v9 lineage}` remains: the `zs_v9_kfield` job (grid, 10:43) had not finished. |
| Table 4 | rows 58-70 one measurement per row: zero-shot fields PENDING; case-grouped lateral/AP at whole frame, three and one in field (Wilson where the file flags the ceiling regime); day-grouped the same six; coupling at 0.74: classifier, coupled, the two differences, disagreement/stop/erring-caught, L6 calls on five-lumbar frames (3/233, 2 cases); at 0.25: classifier and coupled, disagreement frames; the three-L6-cases row 1/5; 0/5; 1 of 4. Note h rewritten (fold models fine-tuned from the latest encoder, re-run of 24 September). |
| Key Point 2 | 1,079 of 1,159 (93.1 %), 608 of 631 (96.4 %), coupled 991 of 1,009 (98.2 %), all labelled fine-tuned on other cases of that C-arm |
| Abstract | "fine-tuned by case-grouped folds, 601 of 617 (97.4 %) and 608 of 631 (96.4 %)"; "the coupled call 991 (98.2 %)" (248 of 250 words) |
| Discussion P1 | "the anteroposterior view did not survive the unseen device until fine-tuned on it (96.4 %); the lateral did not change" |
| Limitations (REVIEW2_RSNA B4, now triggered) | "day-grouped fine-tuning scored below zero-shot laterally" |
| Figure 4 legend | the owner's rebuilt caption file adopted verbatim (60 words); the main.tex comment records the build |
| Figure 5 legend | the owner's caption file of 10:33 adopted verbatim ("(curve labels, %)"; "Persons, not frames"; 56 words). Figures 1-3 legends already equal their rebuilt files. |

Every number is a NUMBERS.md "Revision 2, round 2" row with its JSON path. REVIEW2_STATS N3 ("coupling adds
nothing measurable") is now answered by the re-run's own interval (+1.2, lower bound 0.0, against the count; +0.5,
interval spanning zero, against the classifier), stated in the Results without a claim.

Room for the fill was made by: the at-risk definition in Methods reduced to a pointer to Table 3 note b; the s15
sentence shortened (Table 3 note c has it); "drawn by fixed seed" (note c); "(149 cases, five dates)" -> "(five
dates)"; the prior-report sentence tightened; "at intersection over union 0.5" (Table 4 note c); the detector
lineage clause in "The network" (Figure 3a and the supplement carry it); "(open source)"; in the Results the
subtype breakdowns of the seven COBRA2026 and 51 CT persons (Table 2 rows), the labeller-agreement parenthesis
(Table 2 note e), the never-seen sentence, "(130 cases, ...)" and the classifier interval (Table 4); in the
Discussion two clause-level trims. Body after the fill: **2,991 of 3,000** with the "[COVERAGE FRAMING]" slot
still to be written.

## Grid build 2 (job 40437080, 11:03) and the Table 4 page fit

`latexmk rc=0`, main.pdf **27 pages**, supplement.pdf **12 pages**, biber clean, no "??" in either PDF. But Table 4
with its 15 new rows put the rotated table **142 pt (5 cm) over the text width** (main.log line 1110; 82 pt before
this session, from the round-1 table edits), and page 21 rendered shows the notes clipped at the page edge. Fixed
without dropping a quoted number: the three plain-film selection-split rows (CSXA, BUU-LSPINE, NHANES II) and their
note f moved to a new supplement section "Plain-film naming on the selection split" (every k/n, interval, the
three-body values and the no-held-out-film caveat kept); the day-grouped one-in-field rows (never quoted) live in
NUMBERS.md only; two Measure cells cut to one line; note h shortened; notes re-lettered g->f, h->g throughout the
table. Rebuild checked below (build 3).

## Zero-shot fields (the last G5 naming placeholder)

The `zs9kfield` array (40436982, five folds, fail=0, done 10:49-10:54) scored the v9 encoder + head on the k-in-field
crops; the closure was re-run (`closure_only.sh`, 40437081, done 11:07; the closure workflow had also re-run it at
10:57) and `cv_v9.json#families/pre:zs_v9head` now carries k1-k5 with the same gate verdict (HELD OUT). Results and
Table 4 filled: lateral three in field 970/1,159 (83.7 %), one in field 385/603 (63.8 %); AP fields (33.2 %, 19.0 %)
in NUMBERS.md only. No G5 naming placeholder remains; the G5 placeholders left are Table S2's flagship-detector
cells and the Figure 5 in-domain naming panels (`results/indomain/fit.json` still absent).


---

# Round 3 (2026-09-24, 10:45 onward): the requeued manuscript-drive session, beside the round-2 session

**Two writers.** Greg's 10:30 request (integrate the uploaded acquisition-space review, "especially the learning rate
accuracy saturation part", resume what is unaffected, requeue what changes) relaunched the manuscript-drive edit
step. The round-2 session was not stopped by the relaunch and kept writing: between 10:56 and 11:09 it filled every
G5 placeholder from `results/eval_gate/closure/cv_v9/cv_v9.json` (case- and day-grouped folds, fields, coupling,
the L6 patients, then the zero-shot fields at 11:08), adopted the Figure 4 and 5 legends, added REVIEW2_RSNA B4,
moved the plain-film rows to the supplement for Table 4's page fit, and compiled (job 40437080, 27 + 12 pages).
This session watched the files (mtime polling), did not write while they moved, and **checked the round-2 fill
cell by cell** against its own copies of `cv_v9.json` (10:35 and 11:07 versions, scp from the grid) and
`cv_v9_extras_pre.json`: every quoted k, n, cluster count, interval choice (Wilson on n_eff where the file flags
`ceiling_regime`, else percentile), BCa and paired difference agrees, PRE truth throughout; the count row is
unchanged; the four L6 calls (case139 AP and lateral, case44 lateral, case42 lateral) are all flagged. Nothing of
that fill was rewritten.

**Written by this session (11:12-11:14), in one burst while the files were quiet:**

| where | what | source |
|---|---|---|
| Discussion P4 | the `[COVERAGE FRAMING]` slot: "We hypothesise that coverage, not count, set it: every real frame of that device is anteroposterior or lateral, so frames after the fiftieth added no view, whereas the render pools span the arc; no arm varies view alone, so this is untested." Labelled a hypothesis (journal rule); consistent with CLAIMS_LEDGER section 1 (F13: no arm isolates angle). | `results/arc/audit/pose_pools.json`, `results/arc/ARC_CHECK.md` s1; NUMBERS.md "round 3" |
| Discussion P4 | the saturation evidence Greg asked for, from our own development curve: "The comparison arm's level model saturates the same way in development: doubling its training persons from 4,477 to 8,950 moved validation accuracy on real films by 0.1 points and on rendered L6 bodies by 1.7 (supplement)." | `results/dual_loss/saturation.json` (validation side, no test person) |
| Discussion P4 | dropped "Unlike published registration-free naming [zhang2023vdvm, huang2022], one lateral exposure sufficed here on ordinary spines" (both are cited with their numbers in the Introduction; -16 words). | -- |
| supplement | new section "Development learning curve of the comparison arm" (fractions 563-8,950 persons, three seeds; random-window 68.9 -> 74.0 %, films 98.2 -> 98.7 %, renders 59.6 -> 66.2 %, L6 51.8 -> 64.2 %, T13 never at full size; epochs to within 0.5 points 8-12 of 30; the bank's coverage census and its five validation-only lateral cells). Placed before "Transitional crops in the embedding". | `saturation.json#data/metrics`, `#epochs`, `#coverage` |
| Methods, room (-46 words) | the H6 margin parenthesis (Table 3 row H6 has it); the L6-patients exclusion clause (Table 3 note b, Results); "Holm-adjusted at 0.025, run only where a stratum reaches the count at which an error-free result passes" -> "Holm-adjusted, run only where a stratum can pass" (Table 3 notes c-d; the .025 is in the statistics paragraph); the rib-convention parenthesis (Table 2 note a); the matching-rule parenthesis (Table 4 note b); "source contributions,"; "The model abstains" -> "It abstains". | -- |
| CLAIMS_LEDGER.md | new section 8: the review's claims the Discussion answers, each with its verdict (hypothesis, development evidence, not written). | `lit/CITABLE_CLAIMS.md` |
| NUMBERS.md | new section "Revision 2, round 3" with every number above and its JSON path. | -- |

**Not written, deliberately.** `results/coverage/` (acquisition-space coverage / entropy per corpus; grid job
`acqcov` 40436995 running at 11:10) and `results/indomain/fit.json` (the Figueroa fit: every interval "no interval"
at n_boot 10, its coverage block "pending") are not quoted; the Discussion hypothesis sentence is written so it
takes their numbers when they land without changing its claim. The round-2 session's watch for
`results/coverage/COVERAGE.md` will find the `[COVERAGE FRAMING]` string gone: **re-read
`sections/discussion_motivation.tex` before editing paragraph 4**; add the coverage numbers to the hypothesis
sentence rather than replacing it. Table S2's PENDING G5 rows are the flagship detector on vertebral-body boxes
(workflow detector-g3, jobs `g3det` 40436991/40436992), not the cv_v9 closure, and stay.

**Limits after this round** (`tools/check_limits.py`, pasted below): body 2,998 of 3,000; abstract 248; every
other limit as in round 2; FAIL on the open G0, G4, G6 placeholders and the missing Figure 6 file only.
