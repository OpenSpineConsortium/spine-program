<!--
Cover letter, source. build_packet_src.py renders it to build/cover_letter.docx (Arial 11, double spaced, no page
numbers). Tokens: {{TITLE}} from main.tex; {{fm.<path>}} from front_matter.json (an unconfirmed field prints with a
red [CONFIRM] marker); [[PENDING Gx: what]] prints red until the gate lands. Every number below is in numbers.json
with its result file and must also appear in the expanded main.tex, or the build fails. Paragraph order follows the
journal's list (RSNA_AI_REQUIREMENTS.md, "What is submitted", item 1): title and authors; what the work shows and
what it does not; why this journal; anonymization; subject overlap; conflicts and support; sole submission.
2026-09-24 (evening): the LevelCheck / surgeon comparison is paper 2 (PAPER1_SCOPE.md; paper2_levelcheck/
MOVED_FROM_PAPER1.md). The paragraph "The comparator was fixed before the result", the G6 result sentence and the
Figure 6 pointer left this letter (their text is kept in MOVED_FROM_PAPER1.md section 9); the letter names no
comparator commit, so front_matter.json levelcheck_prespecification marks every commit in_letter=false. The
headline numbers are the v9-lineage cells the manuscript prints (results/eval_gate/leaks/zeroshot_v9.json,
results/eval_gate/closure/cv_v9/cv_v9.json), not the first-run a4/a7/a9 cells of the 2026-09-24 morning.
Rules: no priority claim, no "novel", no product or regulatory pathway, no wrong-level surgery rate; a zero-shot
result and a fine-tuned result are never put in one clause (2026-09-24: the three-body and coupled figures are from
the fine-tuned case-grouped folds, not from the zero-shot model); no per-stratum transitional accuracy, no modelled
LevelCheck value and no hypothesis H1-H6 (PAPER1_SCOPE.md, standing rules).
-->
{{DATE}}

To the Editor, *Radiology: Artificial Intelligence*

Dear Editor,

Please consider the enclosed Original Research manuscript, "{{TITLE}}", for publication in *Radiology: Artificial Intelligence*. The sole author is {{fm.corresponding_author.name}} ({{fm.affiliations.0.name}}).

**What the study asks and shows.** A vertebral level in spine surgery is counted, not seen, and a transitional vertebra changes the count. Registration-assisted labelling carries the labels of the preoperative CT into the operating room, so on a transitional spine it is only as right as the planning read. The manuscript asks whether a network can name the level from the local shape of the vertebrae on one intraoperative C-arm exposure, with no preoperative scan. It was tested on 148 lumbar cases from a C-arm absent from its training, against cone-beam CT. Trained on public rendered CT and radiographs, it named 595 of 617 detected lateral vertebrae exactly (96.4%); the anteroposterior view did not transfer (276 of 631). Fine-tuned on that C-arm, it named 601 of 617 (97.4%) with folds grouped by case and 568 (92.1%) with folds grouped by acquisition day, both reported because whether the 148 cases are 148 people cannot be established. In the case-grouped folds it named 1,079 of 1,159 (93.1%) with three vertebrae in view, where no count from the sacrum is possible; on anchored frames the count from the detected sacrum named 979 of 1,009 bodies (97.0%) and coupling shape with that count named 991 (98.2%). Detection on the unseen device, not naming, was the binding constraint: 231 of 287 vertebrae were found (80.5%). The encoder's embedding set the sixth lumbar vertebra apart from the fifth (silhouette 0.35, against 0.23 for the fifth against the fourth), on 10 validation persons of a split that chose the checkpoint, which the manuscript states as a limit.

**What it does not show.** No transitional test person of the built person-disjoint split is scored. On real exposures the transitional evidence is three C-ArmLSpine patients whose sixth lumbar vertebra one automatic labeller reads and the other does not, scored in cross-validation as agreement with that read; the manuscript calls this a description, not a test of transitional naming. Certifying 90% exact-level accuracy by a Wilson lower bound needs 35 error-free at-risk persons, and the public releases hold seven real-frame candidates, none verified; the manuscript counts them and claims nothing from them. The powered comparison with registration-assisted labelling and with surgeons using it, on verified at-risk persons against a comparator fixed before scoring, is a separate study and is not reported here. No naming accuracy is converted into a wrong-level surgery rate, and nothing has been evaluated prospectively.

**Why this journal.** The question is how much a single projection radiograph shows, asked of a deep learning model and answered against a volumetric reference standard: case-clustered intervals throughout, a device held out entirely, both fold groupings reported where the identity of the intraoperative subjects cannot be established, and the transitional sample size stated against pre-specified targets rather than claimed. The study is reported to CLAIM 2024 and uses TotalSegmentator, both published in this journal.

**Double-anonymized review.** The network is named after the author. In the anonymized manuscript file it appears as "[AuthorLastName]-Net" in the title and throughout, and the two references whose author list identifies the author (the CTSpinoPelvic1K data record and its descriptor, which the subject overlap requires) print as "[reference withheld for review]"; the name and the references are restored in the camera-ready copy, which is built from the same source. Author, affiliation, funding, acknowledgments, the guarantor statement and the conflict of interest are on the full title page and not in the anonymized manuscript.

**Subject overlap.** The CTSpinoPelvic1K CT records (801 of 802 rendered for training; 18 of its persons are among the transitional persons with a sixth lumbar vertebra) were reported in that dataset's descriptor ({{fm.subject_overlap.0.status}}). The descriptor reports the dataset; it trains no C-arm model, names no level on a radiograph and reports none of these results. The overlap is stated in the Methods (its citation is withheld for review and restored at acceptance), and the preprint is enclosed. {{OVERLAP_OTHERS}} Every other image source is a public release by another group, cited in the manuscript.

**Conflicts of interest and support.** {{fm.conflicts_of_interest}} {{fm.industry_support}}

**Sole submission.** {{fm.sole_submission}} {{fm.prior_presentation_of_this_work}} {{fm.preprint_of_this_manuscript}}

Sincerely,

{{fm.corresponding_author.name}}
{{fm.affiliations.0.name}}
{{fm.institution_street_address}}
{{fm.corresponding_author.email}}
