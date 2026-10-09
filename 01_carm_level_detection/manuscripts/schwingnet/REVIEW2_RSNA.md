# REVIEW2_RSNA.md: second Radiology: Artificial Intelligence reviewer pass (the six-figure wrap)

**What was reviewed.**
- `main.pdf`: 26 pages, compiled 24 Sep 2026 at 06:33 (grid job 40430741). Each page was read as text with pymupdf and as a 110-dpi render.
- `supplement.pdf`: 10 pages.
- `main.log`: the whole file.
- Every rule in `RSNA_AI_REQUIREMENTS.md`, and the output of `tools/check_limits.py` from today.

**How the numbers were checked.** Numbers were re-read from `results/a7.json`, `a9.json`, `coupling.json`,
`figure2/figure2_metrics.json`, `figure2/figure2_transitional.json`, `figure2/zones_lateral_clean.json`,
`figures/figure1.record.json`, `figures/figure5.record.json`, `bodybox_rescore/RESCORE.md` and `indomain/INVENTORY.md`.
Identity facts came from `docs/PATIENT_IDENTITY_SPEC.md` and `results/arc/ARC_CHECK.md`.

**Word counts.** Every replacement's effect on the word count was computed with `check_limits.py`'s own `words()` function; the script and the pairs are in the scratchpad.

**Nothing was edited or committed.** This file is the only new file.

Where a fix below reads as prose, it is exact replacement text in LaTeX form. **Paste it as written, then re-run
`check_limits.py`.** New numbers are marked **[trace]**: each needs a NUMBERS.md row before it is used, and the row's file and JSON path are given.

---

## VERDICT

**The draft cannot be submitted yet, and not only because of the open gates.**
- 29 `\PENDING` numbers and one pending figure (G0, G4, G5, G6) are open. That is by design.
- Beyond the gates there are six blocking defects:
  - two ethics or compliance statements that the project's own files contradict;
  - a Discussion that credits fine-tuned results to the network that never saw the device;
  - a title that the paper's own Results now say cannot yet be tested;
  - the anonymization defects left over from the last review;
  - a primary test set (C-ArmLSpine) that is never cited.

**Number discipline has improved.** Every number the wrap put in the text traces to a results file and matches it.

**The failure is selection and attribution.** The number shown is often the fine-tuned or the favourable member of a pair, and the text does not say so. Four examples:
- The three-body figure is 92.9 % fine-tuned but 86.9 % zero-shot.
- Coupling is compared with the count, where it gains 1.6 points, but not with shape alone, where it gains 0.2 points (interval −1.7 to 2.1).
- Occlusion is reported as enrichment per unit area, but by share most of the attribution for L4 to L6 falls on the body below.
- The fused-L5 result is described as "a pull toward the level below". In fact, the classifier named the last free vertebra L5 in both persons where it moved: that is the counting error the paper sets out to avoid.

None of these is fabricated. Each is the kind of thing a hostile reviewer finds by reading Table 4 against the Discussion.

**The story (last section).**
- Figures 1, 3 and 4 each carry one claim.
- Figure 2 carries its claim only on the selection split.
- Figure 5 no longer matches the six-figure specification: the data-case panels a and b are absent.
- Figure 6 is pending, and no fallback drawing has been decided for the case where no stratum is eligible.
- What the paper currently demonstrates is naming on lateral exposures of an unseen C-arm without a preoperative scan, plus a comparison with registration on transitional spines that is frozen in advance and whose data needs are stated. The title claims the result of that comparison, which has not been run.

---

## RULE-BY-RULE (RSNA_AI_REQUIREMENTS.md)

| Rule | Verdict | Note |
|---|---|---|
| Body ≤ 3,000 words | **PASS today, no headroom**: 2,985 | The fixes below add +141 words; the measured cuts in §4 remove 102, which gives 3,024. The G0, G6 and Figure 5 data-case text needs about 150 more words, so about 175 must still be cut (§4). |
| Abstract ≤ 250, four headings | **PASS**: 248 | The abstract fixes (ABS1–ABS3) take it to 246. The G0 age and sex clause will need a cut of about 6 more words. |
| Summary statement ≤ 255 characters, no abbreviations | **PASS**: 231 | Fix 15 takes it to 239. |
| 3 Key Points, with data, no abbreviations | **PASS on form, FAIL on content** | Key Point 2 does not say its three-body number is after fine-tuning (Fix 3). Key Point 3 does not say its silhouette comes from the selection split (Fix 10). |
| ≤ 10 abbreviations, defined at first use | **PARTIAL** | "F1" is undefined (Methods, network). The gate labels G0, G3 and G7 are laboratory slang in Table 1 and in the Figure 5 legend (Fix 26). |
| ≤ 35 references, NLM style, DOI | **PASS on count (30), FAIL on content** | See Fix 6. Four required citations are missing, and `refs_corrections.bib` is not loaded. |
| ≤ 6 figures, ≤ 4 parts each | **PASS** | Figure 6 is still a placeholder. |
| ≤ 4 tables, titled, no merged cells, n/N | **PASS on form** | Table 4 omits the zero-shot and day-grouped rows for three bodies and one body in view (Fix 8). |
| Methods first paragraph: IRB, HIPAA, prior reports of the subjects | **FAIL** | Three problems: the ethics wording is contradicted (Fixes 1 and 2); the overlap sentence cites the dataset, not the descriptor (Fix 6); and "no other subject overlaps a prior publication" is literally false, because every public-release subject was reported by that release (Fix 21). |
| Readers: number, training, years | **FAIL** | The CTSpinoPelvic1K two-reader Castellvi consensus gives no training or experience. Neither does the planned human verification (Fix 11). |
| Exclusions per cause; sample-size derivation | **PASS** | Table 1 footnotes; Statistical analysis paragraph. |
| Pre-specified primary outcome | **PASS, honestly caveated** | "designated after the zero-shot run was first scored" |
| Statistics last paragraph, software and versions | **PASS** | Remove the internal script names (cut CUT2). |
| Results first paragraph = demographics | **PASS in structure, open (G0)** | |
| Results in Methods order with the same subheadings | **PARTIAL** | Three headings differ (Fix 25). |
| n/N for every percentage | **PARTIAL** | The checker warns four times. One is fixable now: 9,740 of 13,009 (Fix 24). |
| Discussion: no table or figure citations; limitations second-to-last; summary last | **PASS** | |
| No ongoing or incomplete investigations in the Discussion | **BORDERLINE** | The summary paragraph describes the pending comparison as deciding the question (Fix 22). |
| No priority claims, no self-evaluation | **PASS**, except the title | "robust" in the title is an unsupported self-evaluation (Fix 4). |
| No laboratory slang | **FAIL** | Table 1 footnotes and the Figure 5 legend carry gate labels and pipeline jargon (Fix 26). |
| Legends: age and sex for human images; planes; what to observe | **FAIL (Figure 1)** | The ages sit in a Results parenthesis instead of the legend (Fix 18). |
| Anonymization | **FAIL** | Fix 5. Carried over from REVIEW_RSNA.md Fix 2, items ii and iii. |
| Supplement ≤ 12 pages | **PASS** (10) | |
| CLAIM 2024 checklist | **FAIL for the packet** | `packet/claim_checklist.docx` is the 2020 form, and the packet dates from 23 Sep 14:37, before the wrap (REFS_AUDIT.md). |

---

## 1. BLOCKING DEFECTS, RANKED

### Fix 1: The ethics statement says the directory holding a residual identifier was excluded, but Figure S5 is built from it

- **The manuscript (p. 11, Ethics):** "One C-ArmLSpine directory carrying a residual patient identifier was excluded and reported to the dataset authors."
- **The project's own files say otherwise:**
  - `docs/PATIENT_IDENTITY_SPEC.md` (alias 16) locates the identifier in `case134/ori/`: 302 XA frames with a real PatientID and a real patient name. The values are not reproduced here.
  - `results/arc/ARC_CHECK.md` §5 records that the grid job "read 302 headers under `case134/ori`".
  - The case134 rotational acquisition is the source of **Figure S5** (`figures/figS4.record.json`: "the real case134 CBCT spin", 301 frames).
  - The export was checked and carries no identifier value (`summary.json#identifier_hits_in_export` = 0). That is good, but the directory was read and used, not excluded.
  - Table 1 footnote h gives a different reason for leaving out case134's spot frames ("missed by a folder walker"). A reader will take the Ethics sentence as the reason 148 of 149 cases are scored.
- **Also unverified:** "reported to the dataset authors". No record of the report was found in the repository. If it has not been sent, send it and date it.
- **Question for the HRPP office:** determination 2026-269 covers sources "de-identified before release". A release with a named patient in one directory is outside that description. Ask the office whether the determination still covers C-ArmLSpine, or whether it needs a note.

**Replacement (main.tex, Ethics; the same in `packet_src/statements.md` ETHICS_MANUSCRIPT):**
> One C-ArmLSpine directory, one patient's rotational acquisition used only for Figure~S5, carries a residual
> name and identifier in its image headers; its frames were exported without header data and checked to carry
> no identifier value, and the dataset authors were notified on \PENDING{G0}{date notified}.

### Fix 2: VinDr-SpineXR is outside the determination, and "every image source is a public release" is inaccurate

**The problem.**
- VinDr-SpineXR is released under the PhysioNet Restricted Health Data Use Agreement.
- `packet_src/statements.md` already marks the item [[CONFIRM: VinDr-SpineXR … is outside determination 2026-269]].
- The manuscript says nothing about it, and three places contradict the facts:
  - Methods, first paragraph: "public, de-identified releases".
  - Data availability: "Every image source is a public release".
  - Table 1 title: "one row per public release".
- FluoroCap is not a release at all. Its 950 panels are figures from published articles, harvested for training.
- Both VinDr and FluoroCap trained the **fold models** (Table 1, footnote f). Those models produced every fine-tuned number: 98.2 %, 92.5 %, 92.9 %, 72.8 % and the coupled 98.6 %.
- The Methods never say which bank the **zero-shot** network trained on, or whether VinDr or FluoroCap were in it. Establish this and state it.

**Options.** Obtain a determination that covers VinDr-SpineXR, or retrain the fold models without VinDr and FluoroCap.
The draft must say which was done. Until then:

**Replacement (main.tex, Ethics, append):**
> VinDr-SpineXR was obtained under its PhysioNet data use agreement (\PENDING{G0}{determination covering it, or
> removal from the fold models}); the literature fluoroscopy panels are figures of published articles, used for
> training only and not redistributed.

**Replacement (main.tex, Data availability, first sentence):**
> Every image source is listed in Table~\ref{tab:data} with its licence and download source; VinDr-SpineXR requires
> a PhysioNet data use agreement, and the literature panels are not redistributed.

**Replacement (Table 1 title):** "Image sources: one row per public release, …" becomes "Image sources: one row per collection, …".

**Replacement (Discussion, paragraph 1):** delete "From public releases alone," (this is folded into A1a in Fix 3).

### Fix 3: Fine-tuned results are credited to the network that never saw the C-arm (Discussion, Key Point 2, abstract, Figure 4b)

**What the files say.**
- `results/a7.json`:
  - Zero-shot, three lateral bodies in view: **86.9 % (1,010/1,162; 83.1, 90.3; BCa 82.9, 90.1; 45 of 142 cases erring)**.
  - Zero-shot, one body in view: **63.1 % (381/604; 58.5, 67.6)**.
  - The 92.9 % (1,079) and 72.8 % (440) are the **case-grouped fine-tuned** cells (`cv5/det/LAT/k3`, `k1`).
- `results/a9.json`: day-grouped, three bodies in view, 87.6 % (1,018/1,162).
- `coupling.json`: the coupled numbers (1,009 bodies, 98.6 %) also come from the fold models.

**Why it matters.**
- Discussion paragraph 1 says, under "Never shown the intraoperative C-arm", "92.9 % with three bodies in view … coupling … 98.6 %". That is false as written.
- Key Point 2 and the abstract place 92.9 % right after the zero-shot sentence and never say it is fine-tuned.
- The Results heading "on an unseen C-arm" covers a paragraph whose numbers are mostly fine-tuned.

**Replacements (every new number marked [trace]; the files are named above):**
- **A1a (discussion_motivation.tex, +12 words):**
  > This study trained a network that names a level from one C-arm exposure by the shapes of the bodies in view.
  > Never shown the intraoperative C-arm, it named 96.3\,\% of detected lateral vertebrae exactly, and 86.9\,\% with
  > three bodies in view and no sacrum to count from; fine-tuned on other cases from that C-arm, it named 92.9\,\% of
  > three-body fields, and coupling shape to a count from the detected sacrum was exact on 98.6\,\% of anchored bodies.

  (It replaces "From public releases alone, this study trained … 98.6\,\% of anchored bodies.")
- **A1b (results.tex, +12):** replace "With three lateral bodies in view, where no count is possible, it named 92.9\,\% (1,079 of 1,162; 89.6, 95.6); with one, 72.8\,\% (440 of 604)" with
  > With three lateral bodies in view, where no count is possible, it named 86.9\,\% (1,010 of 1,162; 83.1, 90.3)
  > zero-shot and 92.9\,\% (1,079; 89.6, 95.6) fine-tuned (day-grouped, 87.6\,\%); with one, 63.1\,\% (381 of 604) and
  > 72.8\,\% (440)
- **A1c (results.tex, +13; also Fix 9):** replace "At confidence 0.74, on 1,009 bodies of 130 cases the count was exact on … 1.6 points above the count (0.0, 3.8)" with
  > At confidence 0.74, on 1,009 bodies of 130 cases read by the case-grouped fold models, the count was exact on
  > 97.0\,\% (979; 94.2, 99.2), the classifier on 98.4\,\% (993) and the coupled call on 98.6\,\% (995), 1.6 points above
  > the count (0.0, 3.8) and 0.2 above the classifier ($-1.7$, 2.1)

  [trace: `coupling.json#cells/det74~1kfull/coupled_minus_classifier_anchored`]
- **A1d (discussion_motivation.tex, +14; also removes the jargon "class-agnostic and in-pool"):**
  > Where registration-free naming on real C-arm images needed a preoperative radiograph or about 17 vertebrae in
  > view \citep{zhang2023vdvm,huang2022}, three sufficed here for 86.9\,\% of ordinary vertebrae untrained on the
  > device and 92.9\,\% fine-tuned. Detection lost more than naming to the unseen device (80.5\,\%); published C-arm
  > recalls (0.964, 0.982) do not name the vertebra and were scored within the training pool \citep{rao2024}.
- **A1e (results.tex, heading; also Fix 25):** "Naming, counting and coupling on an unseen C-arm." becomes "Naming, counting and coupling on the intraoperative C-arm."
- **Key Point 2 (+8):**
  > With three vertebrae in view and no sacrum to count from, it named 1,010 of 1,162 exactly (86.9\,\%) before and
  > 1,079 (92.9\,\%) after fine-tuning; of 1,009 bodies, counting from the detected sacrum named 979 (97.0\,\%),
  > fine-tuned shape 993 (98.4\,\%) and the two coupled 995 (98.6\,\%).
- **Abstract Results (ABS1, +7):**
  > With three bodies in view it named 1,010 of 1,162 (86.9\,\%) zero-shot and 1,079 (92.9\,\%) fine-tuned; on 1,009
  > bodies the count named 979 (97.0\,\%), shape 993 (98.4\,\%), both coupled 995 (98.6\,\%).
- **Figure 4, panel b sub-caption on the figure** (for the figure owner). "Three in view: 1,079 of 1,162 bodies exact (92.9 %)." becomes "Three in view, fine-tuned: 1,079 of 1,162 exact (92.9 %); never trained on this C-arm: 1,010 (86.9 %)."
- **Figure 4 caption (60 words; drops "real" and "Lateral frame:"):**
  > Reading C-arm exposures. (a) Bodies (blue) and sacrum (dashed) boxed by detectors never trained on this C-arm.
  > (b) Field b named by shape alone, fine-tuned on other cases (``none'': no name). (c) Ranks from the sacrum. (d) A
  > frame one CT reading calls six-lumbar: count and shape agree only as L6 (red); stop signalled. L1--L6, first to
  > sixth lumbar vertebrae.

### Fix 4: The title claims what the paper now says cannot yet be tested

"…robust to transitional anatomy, versus registration-assisted neurosurgeons".

**What the paper says itself.**
- No real-exposure transitional test person is verified (abstract, Results, summary).
- 97.6 % "is reported beside an interval, not beaten" (Discussion).
- The comparator is a *model* of registration carrying a planning read. No neurosurgeon was studied.
- On disk, the only transitional evidence runs the other way:
  - in two of four fused-L5 persons, the classifier gave the counting name (Fix 12);
  - in the three never-seen L6 patients, the separation vanished under body boxes;
  - on this device the L6 call fired on 4 frames read as five-lumbar, against 1 of 4 frames in the patients one labeller reads as six-lumbar.

**This is a reviewer finding for a decision `TITLE.md` records as Greg's.** It is not an edit.

**Two titles that the evidence supports** (the name kept, per TITLE.md):
- If G6 does not produce an eligible stratum:
  > SchwingNet: naming lumbar levels from one C-arm exposure without a preoperative scan, and the pre-specified
  > test on transitional spines
- If G6 passes H1:
  > SchwingNet: a convolutional–recurrent network that names vertebral levels on an unseen C-arm, tested against a
  > pre-specified model of registration on transitional spines

**If the title stays.** The Introduction's purpose sentence ("derive how many transitional persons a comparison … needs") does not state the title's comparison as a purpose. When G6 lands, add to it: "and make that comparison".

### Fix 5: The anonymized file still identifies the author (carried over from REVIEW_RSNA.md Fix 2, items ii and iii, not done)

- **p. 12, "Guarantor.":** "The sole author is the guarantor of the integrity of the entire study." This reveals single authorship. Ref 17 (Schwing G, first author) and the network's name then identify the author trivially.
- **p. 12, "Conflicts of interest.":** "The author has a commercial interest in a level-confirmation product under development…". This belongs on the Full Title Page and in the ICMJE forms.
- **Replacement:** delete both paragraphs from main.tex and move them verbatim to `full_title_page` in the packet. In the anonymized file, if a placeholder is wanted: "**Guarantor and conflicts of interest.** Stated on the full title page."
- **The network's name** is Greg's recorded decision (ANONYMISED-VARIANT = no). The risk is unchanged. State the decision in the cover letter.

### Fix 6: The primary test set is never cited; required citations are missing; the reference corrections are not loaded

**Uncited sources.**
- **C-ArmLSpine** (every intraoperative number; CC BY 4.0, which requires attribution) has no reference anywhere. The Zenodo record is 10.5281/zenodo.22768651. Take the authors and title from its DataCite record.
- **Geneva hip phantom** (Yareta, 10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu; CC BY-SA 4.0) is uncited, and its licence is missing from Ethics.
- **Ljubljana 2D-3D-GS** (docs cite Tomaževič 2002; the lab's page at lit.fe.uni-lj.si names the paper to cite) is uncited.
- **Castellvi** is named about ten times (Methods, Results, Tables 2 and 3, Figure 1) with no citation. `castellvi1984` is ready in `refs_corrections.bib`.

**The overlap sentence.** It cites the Zenodo dataset (`ctsp1k`) as "that release's descriptor". Cite `ctsp1kdescriptor` there, as REFS_AUDIT.md item 5 says.

**The corrections are not loaded.**
- `rsnastyle.tex` runs `\addbibresource{refs.bib}` only, so none of REFS_AUDIT.md's corrections reach print.
- Printed refs 25 (COBRA2026: wrong first author, and a note printed inside the entry), 27 (He 2016: "preprint posted 10 December 2015") and 29 (Rao 2024: mangled authors "P YR, S G, R D") still carry REVIEW_RSNA.md Fix 7's defects.
- Twelve journal names are still not in NLM form.
- **Action:** replace each same-key entry in `refs.bib` with its `refs_corrections.bib` version, and add `castellvi1984` and `ctsp1kdescriptor`.

**Budget.**
- Today: 30 references.
- Adding C-ArmLSpine, Geneva, Ljubljana, Castellvi and the descriptor gives **35, the limit**.
- Citing Liebrand 2026 as well (REFS_AUDIT recommends it) needs one citation to go. Rao 2024 is the weakest.
- The statistical methods (Wilson, Holm, BCa, silhouette, t-SNE) stay uncited. The journal's "references for established methods" is satisfied by the stated software.

**Replacement (methods.tex, Sources).** "Real exposures with three-dimensional truth came from C-ArmLSpine (296 exposures, …" becomes "Real exposures with three-dimensional truth came from C-ArmLSpine \citep{carmlspine} (296 exposures, …". Likewise "a phantom \citep{genevahip} and a cadaveric specimen \citep{ljubljana2dd3d}".

---

## 2. REQUIRED BEFORE SUBMISSION (rigor, selective reporting, incorrect statements), RANKED

### Fix 7: "more than any lumbar level from the one above" is false: L1 separates from T12 about as far as L6 from L5

`figure2_metrics.json#silhouette/pairs/L1|T12`: 0.324 (0.294, 0.352). That interval overlaps L6|L5 (0.349; 0.310, 0.386).

The same file also holds the answer to the reviewer who notices that L6 has 9.8 crops per person against 1.4 for L5: the leave-person-out value is 0.338 (0.299, 0.376) (`#heldout_l6/ladder_against_level_above/L6|L5/validation_leave_person_out`).

**B1 (results.tex, +16):**
> L6 separated from L5 (silhouette 0.35; 0.31, 0.39; 98 crops, 10 persons; 0.34 with each person's own crops left
> out) more than L2--L5 from the level above (0.16--0.23; L5 from L4, 0.23; 0.21, 0.25) and as far as L1 from T12
> (0.32; 0.29, 0.35), and the classifier named 75 of 98 L6 crops L6;

This helps the thesis: L6 separates as far as the rib boundary does. The Discussion sentence is in Fix 12, S1.

### Fix 8: Table 4 leaves out the zero-shot and day-grouped rows for small fields, and day-grouped fine-tuning falls below zero-shot

**Rows to add (each is on disk):**

| Test set; grouping | View; field | Measure | % (k/n) | Clusters (with an error) | 95 % percentile | BCa |
|---|---|---|---|---|---|---|
| no C-ArmLSpine frame in training | lateral; three in field | exact level | 86.9 (1,010/1,162) | 142 (45) | [83.1, 90.3] | [82.9, 90.1] |
| no C-ArmLSpine frame in training | lateral; one in field | exact level | 63.1 (381/604) | 142 (113) | [58.5, 67.6] | [58.5, 67.5] |
| day-grouped folds | lateral; three in field | exact level | 87.6 (1,018/1,162) | 142 | [83.3, 91.6] | [82.3, 91.2] |
| day-grouped folds | lateral; one in field | exact level | 66.6 (402/604) | 142 | [62.6, 70.6] | [62.4, 70.4] |

Sources: `a7.json#cells/zeroshot2~1det~1LAT~1k3`, `…k1`; `a9.json#cv/cvday_acquisition_day_folds/cells/det~1LAT~1k3`, `…k1`.

**The finding no text sentence states.**
- Grouped by acquisition day, fine-tuning on this C-arm gave **92.5 %**, below the untuned network's **96.3 %**.
- Case-grouped, it gave 98.2 %.
- The unpaired intervals overlap. Still, the ordering suggests that case-grouped folds share people or sessions across days, so the case-grouped figures may be optimistic. Those figures include the three-body, the one-body and the coupled results.

**B4 (discussion_limits.tex, +20):** after "…is too narrow if they are not." add
> Grouped by acquisition day, fine-tuning scored below the untuned network (92.5\,\% against 96.3\,\%), so the
> case-grouped results may be optimistic.

**Verify before adding the day-grouped AP row.** Two cells coincide exactly, and neither pairing has been checked:
- Day-grouped AP is **610/631**, the same as case-grouped AP.
- The zero-shot answered share is **513/617**, the same as the case-grouped answered share.

Compare the per-vertebra prediction files on the grid for both pairs. If a cell was copied, the day-grouped AP entry in NUMBERS.md is wrong.

### Fix 9: Coupling is credited with an accuracy gain it does not have over shape alone

- **What the paper says.** Key Point 2 and the abstract compare the coupled call (995) with the count (979) only.
- **What the file says.** Shape alone gives 993. Coupled minus classifier is +0.2 points (−1.7, 2.1): 13 bodies corrected, 11 introduced (`coupling.json#…/transitions`).
- **What coupling actually contributes:**
  - the **stop signal**: 921 of 922 unflagged bodies exact; 4 of 5 error frames flagged;
  - the **L6 alphabet**.

  It adds no accuracy.
- **The fix.** The replacements in Fix 3 (A1c, Key Point 2, ABS1) put the classifier beside the count. The Discussion should not describe coupling as improving naming. It does not do so now; keep it that way.

### Fix 10: Key Point 3 presents a selection-split result as a key point with no qualifier

**Key Point 3 (+7):**
> On the validation split that selected it, its embedding separated the sixth lumbar vertebra from the fifth
> (silhouette 0.35; 10 persons) more than the fifth from the fourth (0.23); no real-exposure transitional test
> person is yet verified, and exceeding the published 97.6\,\% registration-assisted accuracy needs at least 152
> error-free at-risk transitional persons.

("at-risk" added: the 152 is for at-risk persons, not for all transitional persons.)

### Fix 11: Reader training and experience are not given

**The rule.** The journal requires the number, training and years of experience of everyone who executed or read the reference standard. It also asks how disagreements were handled.

**What is missing.**
- The CTSpinoPelvic1K Castellvi reads are "a two-reader consensus", with no training given.
- The planned human verification of COBRA2026 and C-ArmLSpine truth (Table 3, footnote c) gives neither the number of readers nor their training.
- If a reader is an author, give the author's initials. If a reader is in training, mark them "in-training".

**B9 (methods.tex, +8; fill the bracketed words):**
> CTSpinoPelvic1K from a two-reader Castellvi \citep{castellvi1984} consensus (READER TRAINING AND YEARS;
> disagreements resolved by RULE),

Add one sentence on the verification readers when G6 defines them.

### Fix 12: The occlusion and fused-L5 results are stated more favourably than the files support

**Occlusion** (`zones_lateral_clean.json`, ten crops per level, six levels: T12, L3, L4, L5, L6, sacrum).
- The target zone has the highest *enrichment* at every level. Enrichment is attribution per unit area.
- By *share* of attribution, L4, L5 and L6 put more on the body below than on the target:

  | Level | Below | Target |
  |---|---|---|
  | L4 | 43 % | 32 % |
  | L5 | 42 % | 24 % |
  | L6 | 36 % | 24 % |

- So the Discussion's "drew mostly on the target body" is not what the file shows.
- "At every level" should read "at each of six levels tested". Figure 2d draws four of them.

**B2 (results.tex, +8):**
> Per unit area, occlusion attribution was densest on the target body at each of six levels tested (enrichment
> 1.39--4.51; sacrum 4.51; 3.42, 5.79), but for L4--L6 more fell on the body below (36--43\,\%) than on the target
> (24--32\,\%) (Figure~\ref{fig:embedding}d).

[trace: `zones_lateral_clean.json#sets/v9_val/<level>/maps/occlusion/share_mean`, `enrichment_mean`]

**Fused L5** (`figure2_transitional.json#fused_L5`).
- The two negative silhouettes rest on **one crop each**.
- The classifier called both crops **L5**. That is the name a count from the sacrum gives, and it is wrong for a fused L5.
- In one of the two persons, L3 was also called L4: the whole run was shifted.
- The current text ("a pull toward the level below reached beyond the junction") hides the one direct piece of transitional evidence the paper has. That evidence goes against the thesis, and it should be stated plainly.

**B3 (results.tex, +11):**
> In four validation persons with a fused L5 (seven crops), the last free vertebra sat nearer L5 than L4 in two (one
> crop each; $-0.13$, $-0.18$; ordinary L4, 0.24, 70 of 1,066 crops below zero), and the classifier named both L5,
> the name a count from the sacrum gives; one of the two also had its L3 named L4.

[trace: `#fused_L5/last_free/per_person[].called`, `#control_level_above/per_person[2].called`; 70 = 0.0657 × 1,066]

**S1 (discussion_motivation.tex, paragraph 2, −11):**
> The encoder set a sixth lumbar vertebra apart from the fifth as far as the rib boundary sets L1 apart from T12,
> and per unit area drew most on the target body, as local identity predicts. The evidence is thin: ten persons on
> a selection split, an order reversed in one render source, a contested L6 in three never-seen patients, and, in
> two of four persons with a fused L5, the name a count gives.

### Fix 13: The COBRA2026 best-case bound rests on calls this labeller mostly gets wrong

**The problem.**
- The abstract quotes "57 unread screen calls, if confirmed, allow a best-case bound of 93.7 %". Of the 57, **38 are T13 calls**.
- By the project's own measures, the labeller's L6 call matched readers in 10 of 24.
- An independent rib count confirmed one of three of its T13 calls on TotalSegmentator (`figures/figure5.record.json#discrepancies_stated[2]`).
- It calls T13 in 45 COBRA2026 patients, while the CTSpinoPelvic1K labels hold no T13 in 801 patients (Table 2).
- An outside comparison therefore predicts that most T13 calls will not verify. The 93.7 % is a bound on a scenario the data make unlikely.

**ABS2 (abstract, −12):**
> No real-exposure transitional test person was verified; exceeding 97.6\,\% needs 152 error-free persons.

**B6 (results.tex, +25):** replace "…the lower bound would be 93.7\,\% (Figure~\ref{fig:power}c, d)." with
> …the lower bound would be 93.7\,\% (Figure~\ref{fig:power}c, d), an upper bound: the labeller's L6 call matched
> readers in 10 of 24, and its 45 T13 calls compare with none in 801 CTSpinoPelvic1K patients.

**B6b (−12):** delete "; on CTSpinoPelvic1K its L6 call matched the readers in 10 of 24" from "Transitional phenotypes". It moves to B6.

### Fix 14: The stop signal is defined incompletely

- In `coupling.json#flags/reasons`, 10 of the 22 anchored frames that were flagged were stopped for a **low margin**: the alphabet's margin was below τ, the 5th percentile of correct frames in the other folds.
- Methods mention only the classifier disagreement.

**B7 (methods.tex, +9):**
> a classifier name differing from the call, or a low margin over the next-best alphabet (Table~\ref{tab:naming}),
> stops the read.

Add the τ rule to Table 4, footnote d: "stop also when the winning alphabet's margin over the runner-up is below the fifth percentile of correct frames in the other four folds".

### Fix 15: The summary statement claims lumbar levels generally; the AP view failed (37.9 %)

**SS1 (239 characters):**
> **A network trained on rendered CT and radiographs named lumbar levels on lateral exposures from a C-arm it had
> never seen, without a preoperative scan; its frozen comparison with registration on transitional spines awaits
> verified patients.**

### Fix 16: The Reference standard sentence on truth boxes is true for detection only (verify, then fix)

- `coupling.json#definitions/truth` states the rule the naming numbers use: "carmlspine_eval.py's match (centre inside the truth body box, IoU >= 0.3, one to one)".
- `bodybox_rescore/RESCORE.md` says C-ArmLSpine's meta `box` "is already the body".
- The Methods sentence "Truth boxes are whole-vertebra label projections" is therefore true only of the detection scoring (a1).

Confirm this against `carmlspine_eval.py`, then:

**B8 (methods.tex, +13):**
> Naming matches detections to vertebral-body truth boxes (centre inside, overlap at least 0.3); detection is scored
> against whole-vertebra projections.

**A trap for Figure 5a.**
- `indomain/INVENTORY.md` records that "detectors that never saw this C-arm find about 5 %" is a box-convention artefact. Under the centre rule the same arm finds 87.7 %.
- The film keypoint detector, which never saw the device either, boxed 617 of 676 (91.3 %) under the naming match.
- If Figure 5a draws body-IoU recall with a zero-frame point near 5 %, the paper will print three incompatible figures for one question: 5 %, 80.5 % and 91.3 %.
- Draw Figure 5a under the centre rule, or under the naming match, and say which in the legend.

### Fix 17: Figure 4d is the one frame in four that fits, and its panel title reads as a success

**What the frame shows.**
- On this device, the L6 alphabet fired on 1 of the 4 anchored frames of the patients one labeller reads as six-lumbar.
- It fired on 4 of the 233 frames both labellers read as five-lumbar.
- The sub-caption on the figure gives both counts, which is good.
- The panel title "six lumbar: both must agree" and the caption's "count and shape agree only as L6" present the chosen frame as a verdict.

**Fix (on-figure title for the figure owner):** "d six lumbar: a stop, not a verdict". The caption's (d) clause can stay. The Results already says "agreement with one reading, not correctness".

### Fix 18: Figure 1 legend lacks ages and sex, and does not say how (c) differs from (d)

**Ages and sex** (`figure1.record.json`):
- (a) man, 54 years;
- (b) woman, 24;
- (c) 89 years, with sex recorded as "other";
- (d) man, 60;
- the films are of women aged 31 and 64.

**Panels (c) and (d)** are both sacralised L5. The difference that matters to the paper is whether the fused body keeps a lumbar label or is counted with the sacrum. That is the at-risk distinction in Table 3.

**The fix.** Put the planes on the figure's row labels ("Labelled CT: sagittal; b, coronal slab; c, surface"), so the caption can carry the demographics.

**Caption (60 words by `check_limits.py`'s count):**
> Transitional phenotypes. (a) Sixth lumbar (man, 54 years); (b) thirteenth thoracic, rib-bearing
> (woman, 24); (c) sacralised L5 labelled lumbar, Castellvi IV (89, sex recorded as other); (d) L5 fused into the
> sacrum, four lumbar, Castellvi IIIb (man, 60). Rows: labelled CT; its render; released film of another patient
> (women, 31, 64). Arrow, transitional vertebra; bar, 20 mm; hatched, none human-read.

Then apply **C4 (results.tex, −4):** "(Figure~\ref{fig:phenotypes}; persons aged 24--89 years)" becomes "(Figure~\ref{fig:phenotypes})".

### Fix 19: Methods say 152 COBRA2026 cases; Table 1 says 145

- Methods: "COBRA2026 (152 of 467 Elekta cases, cut by download volume)".
- Table 1: 145 kept (152 fetched, 7 excluded, per footnote i).

**Replacement:**
> COBRA2026 (145 of 467 Elekta cases; 152 were downloaded before analysis and seven failed a pre-export check \citep{cobra2026})

"Cut by download volume" is the unexplained subset Greg's rule forbids ("fix, don't disclose"). G0 must finish the download and rerun. Until then the phrase is at least honest.

### Fix 20: The study dates in the Methods and the abstract are inaccurate

- "public, de-identified releases published 2020–2026": the Ljubljana gold-standard set dates from about 2002 (docs cite Tomaževič 2002). The NHANES II films date from 1976–80, although the label release is from 2023.
- The journal asks for the date range *of the study*. That range is the analysis window (G0) and the intraoperative acquisition dates.

**B10 (methods.tex, −1):**
> This retrospective study used public, de-identified releases (Table~\ref{tab:data}), assembled and analysed

**Abstract.** Replace "(2020--2026; intraoperative, November--December 2023)" with "(analysed \PENDING{G0}{first download date}–September 2026; intraoperative exposures November–December 2023)".

### Fix 21: The prior-report sentence

"no other subject overlaps a prior publication" is literally false: every public-release subject was reported by the release cited for it. The journal's rule asks whether *any* of the population was previously reported.

**Replacement (methods.tex, Design, last sentence):**
> Every subject was reported by the release cited for its source (Table~\ref{tab:data}); the CTSpinoPelvic1K
> subjects were also reported in a data descriptor \citep{ctsp1kdescriptor}.

The cover letter's subject-overlap statement names the descriptor and attaches it.

### Fix 22: The summary paragraph describes an incomplete investigation as deciding the question

**C10 (discussion_limits.tex, −2):**
> Whether it names transitional spines better than registration carrying a planning read is untested: the
> comparison frozen before unblinding needs 19 verified at-risk persons with real exposures, and none is verified.

### Fix 23: Two different sacrum numbers without a distinction

The Results give "the sacrum on 233 of 290 frames (80.3 %)" and then "43 of 56 sacra" (76.8 %).
- The first counts frames that carry any sacrum box at confidence 0.74.
- The second counts sacra matched to truth.

**B14 (+1):** "the held-out detector the sacrum on 233 of 290 frames" becomes "the held-out detector a sacrum box on 233 of 290 frames".

In Figure 4a's sub-caption, "sacrum at confidence 0.74: 233 of 290 frames" becomes "a sacrum box at 0.74 on 233 of 290 frames".

### Fix 24: A numerator is missing

**C13 (+1):** "the same level for 74.9 %" becomes "the same level for 9,740 (74.9\,\%; …". [trace: 0.748712 × 13,009 = 9,740, exact]

### Fix 25: The Methods and Results subheadings differ (the journal asks for the same ones)

- **C3a:** methods "Evaluation on an unseen C-arm." becomes "Naming, counting and coupling on the intraoperative C-arm." (+3)
- **C3b:** results "What the encoder learned." becomes "The level encoder and what it learns." (+3)
- **Transitional sample size.** Methods "Transitional sample size and the LevelCheck comparator." against Results "Transitional persons needed and available." plus "Comparison with LevelCheck." Use "Transitional sample size." and "The LevelCheck comparison." in both places.

### Fix 26: Laboratory slang in the tables and legends

| Where | Now | Replace with |
|---|---|---|
| Methods, network | "the best pooled F1 of its sweeps on three other devices" | "the best pooled F1 score (harmonic mean of precision and recall) on three other devices" (+4) |
| Methods, statistics | "intervals and tests by the repository's rigor\_fixes.py and stats\_review\_recompute.py;" | delete (CUT2, −12) |
| Table 1 note b | "its rebuild is a gate G0 repair" | "its rebuild enters no reported number" |
| Table 1 note h | "(case134's two were missed by a folder walker) … rebuilt at gate G0" | "(case134's two, filed in its cone-beam directory, were missed by the export script)"; delete "rebuilt at gate G0" |
| Table 1 note i | "the full release is fetching (gate G0)" | "the remaining cases enter no reported number" |
| Table 1 note k | "corpus and weights ship at gate G7. Absent above, used by no trained component: the SpinalAI, AASCE and anchor-crop render banks, the SpineSAC phantom frames, Mendeley-716." | "corpus and weights are released at publication. Downloaded but used by no trained component: SpinalAI, AASCE, SpineSAC phantom frames, Mendeley-716 and one internal render set." |
| Table 1, released column, COBRA row | "corpus (692 cases, fetching)" | "corpus (all 692 public cases)" |
| Table 2 note d | "(v8 or v9)" | "(the two most recent training sets)" |
| Figure 5 legend (on figure) | "CT renders, G3 test" | "CT renders, test side of the split" |
| Figure 3a (on figure) | "YOLO11m box detector, trained on real frames of other devices" | "YOLO11m box detector, render-trained, fine-tuned on real frames of two other devices" (it was fine-tuned from the render detector: Methods, `LINEAGE.md`) |

### Fix 27: Figure 5, panel b is mislabelled

- **The axis label.** It reads "power, % (true 95 %)", but the dotted curve is at a true 99 %. Change it to "power, %".
- **The annotation.** "97.6 %: 0" becomes "97.6 %, true 95 %: power 0".
- **The 20.8 % curve** is not explained in the caption.

**Caption (b):**
> (b) Exact-test power against modelled LevelCheck accuracies (82.2\,\% frozen; 20.8\,\%, lowest published): solid,
> true 95\,\%; dotted, true 99\,\%.

This adds about 6 words. Cut "2026-09-23;" from (c) and "Transitional persons needed and available." down to "Persons needed and available." to stay at 60.

### Fix 28: Figure 6 has no fallback drawing

**The problem.**
- The Methods say one-sided tests "run only where a stratum reaches the count at which an error-free result passes".
- On 23 Sep no real-frame transitional test person was verified. Unless verification yields at least 19 at-risk persons, Figure 6 has no eligible stratum.
- The caption promises a P curve per stratum.

**The fix.** Decide the fallback now and commit it next to the frozen `LEVELCHECK_MODEL.md`, before any scoring. The fallback is the CT-render secondary analysis: 57 persons, scored by the ImageNet-trained arm.

**Caption for that case:**
> SchwingNet against the frozen LevelCheck comparator, CT renders of held-out persons (secondary analysis; no
> real-exposure stratum reached 19 verified persons): accuracy per person with Wilson 95\,\% interval, and the
> one-sided exact $P$ against modelled LevelCheck accuracy from 10\,\% to 100\,\%; frozen values marked. Modelled,
> not measured, LevelCheck.

### Fix 29: Minor accuracy fixes in the Introduction (from REFS_AUDIT.md)

**R-intro (+4):**
> Half of responding spine surgeons report a wrong-level operation \citep{mody2008}, a registry of 34,544
> consecutive patients operated for degenerative disease recorded 0.12\,\% \citep{furuya2026},

---

## 3. PACKET AND BUILD (not manuscript text)

- **The packet predates the wrap.** `packet/` was built 23 Sep 14:37. Rebuild it after these fixes.
  - The CLAIM checklist must be the 2024 form: `packet_src/build/claim_checklist_2024.docx` (REFS_AUDIT.md).
  - `CLAIM_CHECKLIST.md`'s line references date from 23 Sep 13:35 and are stale.
- **The log warnings are still unexplained.** `main.log` ends with "There were undefined references" and "Please (re)run Biber", and names no label or key. The PDF has no "??", and all 30 cited keys print.
  - Diagnose on the grid with `grep -n "undefined\|Citation\|Reference" ~/spinesurg-ct-nnunet/SchwingNet/latexmk.log`. latexmk.log holds every pass.
  - This matters once Fix 6 adds keys: an un-rerun biber would drop them silently.
- **Stale files.**
  - `figures/figS4.caption.txt` still says "Figure S3". The print is right, because supplement.tex overrides it.
  - `figures/FIGURES.md` is stale.
- **Figure production.** Figures must be TIF/EPS at 300 or 1,200 dpi (PNG is refused), with bold sans-serif labels of 12 pt or more. Figures 2 and 5 carry small annotation text ("people", "n", the tick labels) that will fall below 12 pt at 3 inches. Check them at column width.
- **The supplement's "Which source carries the detector" section** gives only whole-vertebra numbers:
  - 86.8 % against 12.9 %;
  - +71.8 points;
  - −47.7 points.

  The same arms read 11.1 % and 3.8 % against body truth, and −8.0 points for the equal-count cut (`indomain/INVENTORY.md`, "Corrections"). The section's first sentence should name the convention:
  > Transfer to the held-out C-arm, scored against whole-vertebra boxes (the convention of the training sources),
  > tracked the source whose frames span the gantry arc
  
  Add the body-convention values after the claim, in brackets.

---

## 4. WORD BUDGET

| | Words |
|---|---|
| Body today | 2,985 |
| Replacements above (A1a–A1e, B1–B4, B6–B10, B14, C2–C4, C10, C13, S1, R-intro) | +141 |
| Cuts measured below (CUT1, CUT2, CUT3, CUT5–CUT9) | −102 |
| **Result after the fixes and the measured cuts** | **3,024: 24 over the limit** |
| Still to fit: G0 age and sex sentence, G6 result sentence, Figure 5 data-case paragraph (panels a and b) | about +150 |
| **Total still to cut** | **about 175** |

**Cut bank (exact text; each measured):**
- **CUT1 (discussion_motivation.tex, −11):** "LevelCheck's published accuracies measure convergence onto labels a reader assigned \citep{…}; they cannot register an error in the planning read, and where that read counted correctly LevelCheck is a ceiling this network can at best match." becomes
  > LevelCheck's published accuracies measure convergence onto a reader's labels \citep{desilva2016,manbachi2018};
  > where that read counted correctly, LevelCheck is a ceiling this network can at best match.
- **CUT2 (methods.tex, −12):** delete "intervals and tests by the repository's rigor\_fixes.py and stats\_review\_recompute.py" (also slang).
- **CUT3 (results.tex, −6):** "110 with L6 (CTSpinoPelvic1K 18, VerSe 86, TotalSegmentator three, intraoperative three)" becomes "110 with L6 (three intraoperative)". The per-source counts are in Table 2.
- **CUT5 (methods.tex, −14):**
  > The scored configuration, with an encoder trained from ImageNet weights on the split's training persons, and
  > three secondary analyses were fixed before unblinding (Table~\ref{tab:levelcheck}, Figure~\ref{fig:levelcheck}).
- **CUT6 (methods.tex, −7):** "against 97.6\,\% power stays below 0.1\,\% at any size, and at a true 99\,\% it first reaches 80\,\% at 708" becomes "against 97.6\,\% it reaches 80\,\% only at a true 99\,\%, at 708 persons".
- **CUT7 (results.tex, −10):**
  > The built split holds 57 CT test persons for the render analysis, 48 of them in the current encoder's training
  > data (Table~\ref{tab:transitional}).
  
  Also fix the table: Table 2 prints validation plus test (67 of 72 for these rows), not the 48 of 57 test-only. Add a test-only column or cite `figure5.record.json#discrepancies_stated[4]`.
- **CUT8 (methods.tex, −13):**
  > For validation persons with an unlabelled fused L5, the last free vertebra was placed between the L4 and L5
  > clusters, their L3 as control.

- **CUT9 (methods.tex, Reference standard, −29).** The rule is already in Table 3, footnote c. "For held-out transitional persons without a human read, an automated reference (three readers, combined by the rule whose per-subtype positive predictive value keeps a Wilson lower bound of 90\,\% on CTSpinoPelvic1K and VerSe reader truth) was fixed before unblinding; results resting on it carry its measured error." becomes
  > An automated reference for unread transitional test persons, with its measured error, was fixed before
  > unblinding (Table~\ref{tab:levelcheck}).

**For the remaining ~175 words (estimates, not yet measured):**
- **Retire the parallel Wilson criteria from the text** (Methods: "The pre-stated transitional criteria are Wilson 95 % lower bounds of 90 % … and 85 % …"; Results: "With no error, a Wilson lower bound of 90 % needs 35 test persons;"), about −40 words. Keep them in Table 2, footnote f. The frozen exact test is the one test the paper runs, and two criterion systems for one question confuse the reader.
- **Move the network paragraph's detector-lineage clause to the supplement** ("fine-tuned from a render-trained detector on the real frames of COBRA2026 and DeepFluoro, … a rule reading no C-ArmLSpine frame"), about −25 words. Figure 3a carries it once corrected (Fix 26).
- **Shorten the Discussion's LevelCheck paragraph to two sentences,** about −30 words. The Introduction already makes the argument.
- **Move the never-seen L6 body-box detail to Table 4, footnote e** ("with vertebral-body boxes this vanished (−0.07; 13 of 180)"), about −12 words. Keep the fact in the Discussion's list of weaknesses.
- **Together these give about −107, which leaves about 70 words still to cut.** The paper cannot hold the Figure 5 data case, G0 and G6 without moving one block of detail to the supplement.
  - The natural candidate is the never-seen-patient and fused-L5 detail in "The level encoder and what it learns" (about 90 words).
  - Leave one sentence in the text: "In three never-seen patients one labeller reads as six-lumbar, and in four persons with a fused L5, the embedding did not show local identity robustly (supplement)."
  - The Discussion keeps both in its list of weaknesses.
- **The alternative is to drop Figure 5's power panels to the supplement** and keep only people needed against people available. The Discussion carries the 152 either way.

---

## 5. THE STORY: one claim per figure, in order, and whether the text says what each proves

| Fig | Specification (task) | What it shows now | One claim? | Text says what it proves? | Verdict |
|---|---|---|---|---|---|
| **1** | L6, T13, sacralised L5, four-lumbar | The four phenotypes in CT, render and released film; two film cells are empty because no human-read film exists | Yes: *the count-changing variants look like this, and two have no human-read real image* | The Results cite it for the absence of human-read films. No sentence says why (c) and (d) differ (Fix 18). | **Carries it** once the caption says (c) keeps its label and (d) is counted with the sacrum: the at-risk distinction the comparison turns on |
| **2** | t-SNE with transitional marked, close-ups, where the name is read, **published gradients** | a t-SNE; b lumbosacral window; c silhouette per level; d occlusion | Intended claim: *local identity is learnable: L6 has its own cluster*. Panel (c) mixes three sub-claims: validation L6, the never-seen patients, fused L5. | Yes, with caveats. Before Fixes 7 and 12 the text stated two results more favourably than the files support. | **Carries a narrower claim than intended**: L6 separates from L5 as far as L1 from T12, **on the split that chose the checkpoint**. The **published-gradients component of the specification is missing**. Nothing ties the embedding to an outside anatomical measure, and that is the check that separates "morphology" from "render source". A panel plotting a per-level published morphometric gradient against the embedding's level-to-level distances would supply it. Panel (c) could absorb the silhouette. |
| **3** | detector, level model, count, coupling | Schematic, four panels | Yes: *two mechanisms, shape and count, and a rule that couples them* | Methods only, which is right for a schematic | **Carries it.** Fix the 3a wording (Fix 26). The text must not imply that coupling improves accuracy: its value is the stop signal and the L6 alphabet (Fix 9). |
| **4** | detection, three-body field, count, the real L6 frame | Detection by unseen detectors (a); **fine-tuned** shape naming (b); count (c); the chosen L6 frame (d) | Nominally *one exposure on an unseen C-arm*, but (b)–(d) show fine-tuned models | The Results heading and the Discussion attribute fine-tuned results to the unseen device (Fix 3) | **Carries it after Fix 3.** The strongest defensible claim in the paper (zero-shot lateral naming at 96.3 %) is in the text but not on the figure. Either print the zero-shot number in (b) (Fix 3), or make (b) the zero-shot model's reading of the same field. Retitle (d) (Fix 17). |
| **5** | **detection vs same-device frames, naming vs same-device cases (lateral/AP)**, power, people available vs needed | a Wilson bound; b power; c persons per subtype; d best-case intervals | Yes: *the transitional test cannot yet be run, and 97.6 % cannot be beaten with public data* | Yes (Results; Discussion paragraph 3) | **Does not match the specification.** The *data case* is absent from the figure and from the text: an unseen device fails on AP, and 50 frames from 25 patients restore it. Methods, Results and Discussion have no sentence on it. When the learning curves land, (a) and (d) of the current figure are dropped, and about 80–100 words of text are owed (§4). Draw detection under the centre rule, not body IoU (Fix 16). |
| **6** | SchwingNet vs the frozen LevelCheck model | Placeholder | n/a | Methods and Table 3 define it well | **At risk.** With no verified real-exposure person, the figure may have no eligible stratum. Decide the render-only fallback now (Fix 28), because the title (Fix 4) rests on this figure. |

**Order.** The figures are cited in order: Introduction 1; Methods 1–6; Results 1, 2, 4, 5, 6. The tables are cited in order. Figure 3 is cited only in Methods, which is fine for a schematic.

**Overall.** The arc runs phenotype, embedding, network, exposure, power, comparison. That arc is right for the question the Introduction asks. What the draft can support today is narrower than its title.

What is demonstrated:
- Naming on lateral exposures of a C-arm absent from training, with no preoperative scan: 96.3 %, and 86.9 % with three bodies in view.
- The AP view failed, and fine-tuning recovers it.
- The comparison with registration on transitional spines is frozen in advance, and its data needs are stated.

What is not demonstrated: any transitional result. The only direct transitional evidence (Figure 2's fused L5; Figure 4d's L6 calls) is small, and it leans against the thesis.

The paper is honest about all of this in its Results and Discussion. Its front matter and title are not. After Fixes 3, 4, 10, 13 and 15, the Key Points, abstract and summary statement will say what Figures 4 and 5 prove. Figure 6 either lands or becomes the stated next test.

---

## What is strong (keep through every cut)

- The frozen LevelCheck model: its r(1 − e) derivation, the simplifications that favour the comparator, and the commit-backed dates in Table 3's footnotes.
- The exact-test arithmetic that shows 97.6 % cannot be beaten at any reachable sample size, stated plainly in the Discussion.
- The "agreement, not correctness" quarantine of the three C-ArmLSpine L6 patients, applied in the Methods, the Results, Table 4 and Figure 4d alike.
- The day-grouped folds reported beside the case-grouped ones. Now also say what the difference implies (Fix 8).
- "The primary outcome, designated after the zero-shot run was first scored": a rare and correct disclosure.
- The accounting of exclusions per source in Table 1, and the leak audit behind Table 2.
