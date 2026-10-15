# Round 6: panel review and line edit of the AIDaS 2026-2027 seed packet

This review reads the packet the way an AIDaS faculty panel of computer scientists and clinicians would, using the call's five criteria. It was a read-only review, and no repository was edited.

- **Base text.** main.tex as of 23:24 UTC on 2026-10-14 (sha256 09bc67a0396a2d01...), which is the `latex/main.tex`
  of commit daeeb53; every line number below refers to that file. The packet PDF was rebuilt from it in daeeb53.
- **How the edits were checked.** Each edit was applied by search to a scratch copy; every current text was found exactly once. Each copy was built twice with pdflatex and measured page by page. Every combination in section 3 builds to 8 pages, and only the hidden-check fix applied alone overflows.
- **No number, citation or [DATA NEEDED] mark changes.** All 21 marks stay. The only numeric differences are:
  - two aim labels, "Aim 2" in N5f and "Aim 3" in A2;
  - the room number, which N6f takes out of Aim 3 and budget line B3 keeps.
- **The edits, saved beside this report as patches** (`git apply` each from the repository's root, in this order):
  - `r6_line_edits.patch`: the 70 line edits of section 2, to `latex/main.tex`.
  - `r6_hidden_check.patch`: the hidden-check fix W1-W3, on top of the line edits.
  - `r6_figure_edits.patch`: the figure changes of section 4, to `make_figures.py`; run `python3 make_figures.py` after it.
  - A8 is in no patch; its text is in section 2.2. The reviewer's scratch copies and preview PDF were not kept.

## 1. Panel scores and the fixes that matter most

### 1.1 Scores

Scores run from 1 to 5, with 5 best. Round 3 used 1 to 9, with 1 best: roughly, 5 here is 1-2 there, 4 is 3, and 3 is 4-5.

| Criterion | Now (1-5) | Round 3 (1-9) |
|---|---|---|
| Intellectual merit and innovation | 4 | 3 |
| Strategic and national alignment | 4 | 2 |
| Pathway to external funding | 4 | 2 |
| Team and leadership | 3 | 3 |
| Feasibility | 3 | 5 |
| Overall | 4 | 3 |

- **Merit (4).**
  - For it: the held-out results are honest, with the miss up front (80.5% against the 97% set in advance), and gates fixed before any run are a real methodological stance.
  - Against it: H1's win over the repair loop is partly true by construction, and the agent can read the gate, so it could game it (section 1.3).
  - Against it: paragraph 3 states the contribution inside a 93-word sentence, so a reader has to dig for it.
- **Alignment (4).**
  - For it: the national hooks are specific and were checked in round 5: the AI Action Plan, EO 14363 and the Genesis Mission, NSF DCL 26-023, EO 14303, NIH's data policy and FDA's Q-Submission program.
  - Against it: Foundational AI as the primary area holds only if the panel accepts the "reliability of agentic systems" claim. The hidden-check fix makes that claim defensible.
- **Pathway (4).**
  - For it: three solicitations with dates; program-officer contact in months 1-3; a Pre-Submission that feeds the R21; a cadaver set opened in September for the R21.
  - Against it: CAREER eligibility is still a red mark.
  - Against it: a CAREER on agents reads as a step away from the PI's 3-D vision record unless one sentence ties the two together (A8).
- **Team (3).**
  - The facts this criterion turns on are still red marks: tenure-track status, the PI's role in the consortium and since when, and effort. The call gives priority to tenure-track Assistant Professors.
  - Aim 3 names no spine-imaging or radiology input. The clinical collaborator's specialty is General Surgery.
- **Feasibility (3).**
  - For it: the scope is honest, and each risk has a fallback.
  - Against it: $8,291 of the $18,568 (45%; lines B, D and F) waits on the AIDaS office's allowability answer.
  - Against it: nobody has confirmed that the C-arm room takes human specimens.
  - Against it: it is untested whether two Premium seats carry 360 benchmark runs.
  - Against it: one 10-hour-a-week researcher carries all three aims.

### 1.2 The three changes that would most raise the score

1. **Close the gaming hole in Aim 1 (W1-W3, section 1.3).** This turns the repair-loop comparison into a real test and protects the Foundational AI claim. It fits only together with the paragraph 2 cuts (N2a-N2e); this was checked by building it.
2. **Fill the eligibility and team red marks, and add one sentence (A8) to the CAREER item.**
   - The red marks: tenure-track status, the PI's role and since when, and effort.
   - A8: "Aim 1's tasks come from the 3-D-to-2-D experiments the PI leads in Aim 3, so the agent serves the PI's own vision program."
   - Checked: A8 costs one line, and page 5 keeps 22.5 pt.
3. **Make page 2 readable for both halves of the panel.**
   - Split the 93-word contribution sentence (N3a).
   - Define the terms each half lacks (N1c, N3a, N4a, N4c, N6a).
   - Remove two overclaims: N4a calls Claude Code a large language model, and A5 counts the cadaver set as reusable data before it exists.

### 1.3 The biggest weakness, and an answer that fits

**The objection.** A skeptical panelist will say H1 is won by construction:

- The gated loop stops only when its gate passes, so of course it passes more gates than a loop that stops at a clean exit.
- The agent can read the gate, so it can pass by gaming it. Reward hacking has been reported on RE-Bench-style tasks.
- So the "reliability of agentic systems" claim, the reason Foundational AI is the primary area, rests on a measure the agent can game.

**The answer.** Three edits, all in r6_main_with_all_edits.tex and checked by building:

- **W1** (Aim 1, +72 characters). Add after the benchmark sentence, which ends "to fail on a planted error." with N4b, or "30 sealed until the final run." without it: "A hidden check on each sealed task, seen by no arm, catches gamed gates."
- **W2** (H1, l.165-166, +24). Change "with no intervention and no rule violation," to "with no intervention, no rule violation and no failed hidden check,".
- **W3** (table, l.251, +13). Change "GPU-hours per pass; false successes" to "GPU-hours per pass; false successes; gamed gates".

**Cost.**

- Aim 1 grows from 11 lines to 12. Paragraph 2's cuts (N2a-N2e) pay for that line.
- Without those cuts, the fix pushes page 4 6.3 pt into the margin and leaves one overfull box. With them it fits, and page 4 keeps 5.6 pt.
- The PI must write 30 hidden checks, one for each sealed task, in quarter 1.

**Optional, if room appears.**

- Soften "model-agnostic", since only one model is run.
- Or say why there is no open-weight model arm; leaving it out was a design decision.

### 1.4 Round 3's concerns

- **Met:**
  - the Aim 2 crossover;
  - Aim 3 now answers Figure 4b's gap;
  - the three arms;
  - H3 respecified;
  - the cadaver timing;
  - separate aims for the CAREER and the R21;
  - MLE-bench and RE-Bench cited;
  - contradictions and filler removed;
  - line D;
  - the scope sentence.
- **Partly met:**
  - density, in paragraph 3 and Aim 3;
  - jargon for each half of the panel;
  - Figure 1.
- **Not yet met:**
  - the PI's role, effort and tenure-track status;
  - no spine or radiology advisor.
- **Kept by design (RECORD.md, section 4):**
  - Foundational AI as the primary area;
  - Figure 2 kept;
  - no open-weight model arm.

## 2. Line edits

All 70 line edits are in both .tex files. Each entry below gives the edit's ID, its main.tex line or lines, and the change in characters, followed by what it changes and why.

### 2.1 The edits that matter most

- **N3a** l.140-144 (-2).
  - Change: splits paragraph 3's 93-word sentence into four: "...its own jobs on the WSU grid. Its methodological contribution is a gate-conditioned repair loop that treats the scheduler as part of the runtime. Cluster refusals (a wrong quality-of-service, or QoS, setting; a job killed for memory) and code errors enter one loop that edits and resubmits the job. The loop stops not at a clean run but when the job's gate passes; a gate is a pass/fail test, sealed by hash before the first job, that the agent can read but not change."
  - Why: the project's one claim was buried mid-sentence, and QoS and gate were undefined.
- **N4a** l.156-158 (-3).
  - Change: "The agent is Claude Code, an AI coding agent, at a pinned model version, run by a model-agnostic test harness with no intervention (no human edit or resubmission)."
  - Why: Claude Code is an agent built on a model, not a large language model, and a computer-science panelist will mark the error. "Test harness" also tells a clinician what the harness is.
- **A5** l.336-337 (+16).
  - Change: "...ask for data others can reuse, as CTSpinoPelvic1K is and the cadaver set will be where its terms allow. FDA's Q-Submission program gives Aim 3 written feedback on its validation plan within the award."
  - Why: the cadaver set does not exist yet, and its release waits on a red mark; the old sentence claimed it as reusable data. The edit also removes the second "FDA's".
- **N6c** l.217 (+13).
  - Change: "cross-validated models, checked against the count, name 98.2% of 1,009 bodies,".
  - Why: as written, the 98.2% reads as the zero-shot level model's result. It comes from the cross-validated C-ArmLSpine fold models.
- **N2a** l.128 (+6).
  - Change: "a check that needs no CT, only the C-arm image" replaces "a check that reads the C-arm image alone".
  - Why: it names the clinical advantage over LevelCheck, which needs the preoperative CT.
- **N2b** l.129 (-10).
  - Change: drops "the hips" from the dataset's labels.
  - Why: the hips do not matter for counting levels, and the cut pays for N2a.
- **N2c** l.130-131 (-2).
  - Change: splits at "(Figure 3a). With no C-arm image in training, it names the level".
  - Why: this was the paragraph's 79-word sentence.
- **N2d** l.132-133 (-13).
  - Change: "on one held out of its training, our C-arm detector finds".
  - Why: "the stack's" is not defined yet at this point, and the new text is shorter.
- **N2e** l.135-136 (-2).
  - Change: "fine-tunes). The consortium's 2026 trainee program hit the same wall: it relied on mentors expert in Python, imaging and cluster computing [9]."
  - Why: it splits the sentence, and "Slurm" means nothing to a clinician here.
  - N2a-N2e together take paragraph 2 from 9 lines to 8. That freed line pays for W1.
- **N1a** l.119-120 (-4).
  - Change: ends the first sentence at "mobile fluoroscope." and starts the next with "The count fails often enough to matter:".
  - Why: the opening sentence ran 66 words.
- **N1b** l.120-121 (0).
  - Change: "a 27-hospital Japanese registry recorded wrong-level surgery in 0.12% of 34,544 patients having degenerative spine surgery (0.42%".
  - Why: it puts the rate beside its denominator.
- **N1c** l.122-123 (+5).
  - Change: "It fails most on a transitional vertebra, part lumbar and part sacral: 12.9% of 550 surgical patients had one,".
  - Why: it defines the term for a computer-science reader; "unusual anatomy" was vague.
- **N1d** l.125-126 (-5).
  - Change: drops "that" from "the 20 s to one minute that surgeons said they would wait".
  - Why: it pays for N1c, so paragraph 1 stays at 7 lines.
- **N6d** l.220 (+20).
  - Change: "at 0.74, a cross-device threshold chosen on other devices" replaces "at the cross-device threshold of 0.74".
  - Why: a reviewer's first question is whether 0.74 was tuned on the test device. The edit answers it and keeps the required name "cross-device".
- **N6b** l.211-213 (-12).
  - Change: "the C-arm detector" replaces "the cross-device detector", and "the CT's corners" replaces "the CT body's corners".
  - Why: one detector should have one name; paragraph 2 and Figure 3 call it the "C-arm detector".
- **N6e** l.227-228 (+5).
  - Change: "sensor response until that classifier is at chance" replaces "detector response until that classifier fails".
  - Why: "detector" already names the vertebra detector, and "fails" could be read as the renderer failing.
- **N3b** l.147-149 (-3).
  - Change: "(Figure 2). Aim 3 turns it on the detection gap, with a paired CT and C-arm cadaver set imaged at WSU and a differentiable 3-D Gaussian X-ray renderer, like those of [13,14], built on the PI's Gaussian-splatting work."
  - Why: it splits the sentence, and it drops "throughput" and "the transfer problem", two more names for the gap paragraph 2 already named.
  - Why: "like those of" stops a reader from taking [13,14] as the PI's own papers, which they are not.
- **N5f** l.179 (+17).
  - Change: adds "Aim 2 adds both." after "a control group and objective measures."
  - Why: it ties the 2026 report's limits to this aim's design in four words.
- **N5e** l.182 (+7) and **T3** l.264-265 (+12).
  - Change: "sizes the NSF CyberTraining proposal" and "size the CAREER and CyberTraining studies".
  - Why: "the Pilot" appears before the alignment page names it.
- **C3** l.91-93 (-19).
  - Change: splits the abstract's 66-word first sentence after "mobile fluoroscope." and drops "intraoperative".
  - Why: the abstract is what the panel reads first.
- **C4** l.95 (-17).
  - Change: "and a level model. Never trained on a C-arm image, it names the level of".
  - Why: it splits the next long sentence and is shorter.
- **N4c** l.163-165 (+25).
  - Change: "The consortium's agents already run through Beethoven as jobs under Slurm, the grid's scheduler, and our prototype runs the loop against a simulated scheduler with the grid's partitions and refusals, a design check, not a result."
  - Why: it defines Slurm and replaces "workers" and "skeleton", which are internal words.
- **N6n** l.220-221 (+2). This edit is conditional.
  - Change: "on corrected truth it finds" replaces "on rebuilt truth it finds".
  - Why: "rebuilt truth" is never defined. Use this edit only if the rebuild corrected labels; otherwise define "rebuilt" in a clause.
- **S4b** l.276 (+9).
  - Change: "If the agent is not ready by month 4, wave 1 starts on the 2026 setup and the crossover moves to wave 2;".
  - Why: in the old sentence the agent that is not ready is the subject that starts wave 1.

### 2.2 The rest, by page

Cover:

- **C1** l.71-73 (+25).
  - Change: lists the areas in aim order (area 1 with Aim 1, area 3 with Aim 2, area 4 with Aim 3); adds "studied in an agent" and "the cluster's safety rules".
  - Why: the reader meets the areas in the same order as the aims, and "safety rules" alone did not say whose rules.
- **C2** l.86 (-5).
  - Change: "Aim 3 uses WSU's own C-arm".
  - Why: plainer.
- **C6** l.105 (+17).
  - Change: "what it adds over a coding assistant, the 2026 program's setup".
  - Why: it names the comparison arm.
- **C7** l.105-106 (-11).
  - Change: "Aim 3 turns the agent on the detection gap".
  - Why: the gap gets one name, the one the abstract has just given it.
- **C8** l.107 (+11).
  - Change: "an invention-disclosure review".
  - Why: "a disclosure review" is unclear.
- **C9** l.102-103 (0).
  - Change: splits at "passes. We expect it".
  - Why: the sentence ran 52 words.

Paragraph 3:

- **N3c** l.145 (0).
  - Change: splits at "(MLE-bench [11], RE-Bench [12]). None we know of scores".
  - Why: the novelty claim gets its own sentence.

Figure captions:

- **F1** l.151-153 (+8).
  - Change: drops "on the grid" from (a); (c) now begins "Why counting fails:".
  - Why: the caption says what panel c is for.
- **F2** l.186-187 (-2).
  - Change: "sends GPU jobs to H200s"; "before (recalled) and after".
  - Why: "the heavy lifting" is store-kit language, and the "before" ratings were recalled afterward.
- **F3** l.200 (+10).
  - Change: "boxes the vertebral bodies and the sacrum".
  - Why: "bodies" alone is unclear to a computer-science reader.
- **F4** l.239 (-1).
  - Change: "on a C-arm never trained on".
  - Why: it matches the word the text uses.

Aim 1:

- **N4b** l.158-160 (-2).
  - Change: moves "(10 for development, 30 sealed until the final run)" next to "40 tasks".
  - Why: the split belongs with the count, and the sentence then ends where W1 attaches.
- **N4d** l.162-163 (-5).
  - Change: "Each arm runs each task three times (360 runs), with pass rates by task type."
  - Why: it fixes the dangling "pass rates reported".
- **N4e** l.166-167 (-3).
  - Change: "whose clean exits may fail their gate (false successes)".
  - Why: it defines the false successes the table counts.

Aim 2:

- **N5a** l.171-172 (-8).
  - Change: splits the sentence and rewrites the end as "the trainee owns the question and the result, and a mentor reviews the code".
  - Why: "pull request" is jargon to a clinician.
- **N5b** l.172-173 (+4).
  - Change: "two matched starter tasks drawn from the 10 development tasks (never a sealed one): one with the agent, one with the 2026 setup".
  - Why: the commas ran three clauses together.
- **N5c** l.174 (-4).
  - Change: "comfort survey" replaces "comfort instrument".
  - Why: plainer.
- **N5g** l.177 (0).
  - Change: splits at "mentors expert in Slurm. All six domains improved".
  - Why: the sentence ran 54 words.

Aim 3:

- **N6a** l.208 (+16).
  - Change: "AP (front-to-back) and lateral frames".
  - Why: it defines AP for a computer-science reader.
- **N6j** l.215-216 (+1).
  - Change: splits at "the 631 AP bodies. Fine-tuned on the AP frames of five cases, it names".
  - Why: the sentence ran 64 words.
- **N6l** l.226-227 (+7).
  - Change: makes three sentences: "(SyntheX [16]). We randomize devices' geometry and spectra likewise and hold out each device in turn. We also fit the Gaussian renderer".
  - Why: the sentence ran 61 words.
- **N6f** l.230-231 (-34).
  - Change: drops the parenthesis with the room and its booking office, leaving "on WSU's C-arm. A frame grabber records".
  - Why: logistics belong in the budget, where line B3 keeps them, and the cut pays for N6a and N6d.
- **N6g** l.233 (0).
  - Change: splits at "confirms. End-to-end latency is unmeasured,".
  - Why: the sentence made two claims. Better still, move the intended-use sentence to the start of Aim 3, where it frames H3.
- **H3x** l.233 (-1). This one is the owner's call.
  - Change: "on each held-out C-arm" replaces "on each held-out device".
  - Why: as written, H3 promises 97% on every held-out device, but the results catalog has COBRA at 6.2% and DeepFluoro at 74.7% at 0.74 (rows A6.9 and A6.10).
  - Better still: name the devices H3 is judged on.

Table:

- **T1** l.248 (+8).
  - Change: "40 tasks from the consortium's lists and Aim 3".
  - Why: "the repository" is never defined, and the new wording matches Aim 1.
- **T2** l.250-251 (+18).
  - Change: "a job run on the shared login node".
  - Why: "a login-node run" is jargon to a clinician. The cell grows to 4 lines, which still fits inside the row's 4.

Section 4:

- **S4a** l.271 (+8).
  - Change: "the agents' subscriptions" replaces "the agents' seats".
  - Why: "seats" is billing jargon.
- **S4c** l.272-273 (+16).
  - Change: "the Gaussian renderer is fitted only as a feasibility test".
  - Why: "a feasibility fit" is unclear.
- **S4d** l.271-272 (-4).
  - Change: splits at "regulatory review. The trainee program, grid, pipelines and faculty time come in kind;".
  - Why: the sentence ran 46 words.

Alignment page:

- **A1** l.311-313 (-22).
  - Change: "carrying the agent and its trainees: Aim 1's gate-conditioned agent as the research plan, Aim 2's trainees as the education plan" becomes "built on Aims 1 and 2: the gate-conditioned agent as the research plan, the trainees as the education plan".
  - Why: "carrying" is figurative, and the new text is shorter.
- **A2** l.316 (-5).
  - Change: "NIH R21 at NIBIB, built on Aim 3:".
  - Why: it parallels A1.
- **A3** l.318-319 (-20).
  - Change: "Submitted October 18, 2027 (October 16 is a Saturday), while the PI is still an Early Stage Investigator."
  - Why: shorter. With A2 and A4, the R21 item drops from 6 lines to 5.
- **A4** l.321 (+18).
  - Change: "80% power to show a Wilson lower bound of 90% if the true accuracy is 97%".
  - Why: it says what the power is for.
- **A6** l.340-342 (+3).
  - Change: "The PI builds the agent and the 3-D-to-2-D model, including the Gaussian X-ray renderer; a computer vision researcher, the PI leads the Machine Perception Lab and publishes on ... The PI's part".
  - Why: the role comes first and the record second, and a 61-word sentence is split.
- **A7** l.331 (-4).
  - Change: splits at "that support it. NIH's Bio Genesis Mission carries it into biomedicine."
  - Why: the sentence strung three "and" clauses together.
- **A8** (new; not in the saved .tex files, but checked in a build).
  - Change: add to the CAREER item, after the education-plan clause: "Aim 1's tasks come from the 3-D-to-2-D experiments the PI leads in Aim 3, so the agent serves the PI's own vision program."
  - Why: it answers the question "why is a vision researcher's CAREER about agents?". It costs one line, and page 5 keeps 22.5 pt.

Budget page:

- **B1** l.399-400 (-3).
  - Change: "An hourly graduate student assistant (the call's graduate student support), or else a post-baccalaureate researcher:".
  - Why: shorter, and the call's heading now reads as a gloss.
- **B2** l.402-403 (-19).
  - Change: "...not an enrolled student; hiring a student, at WSU's composite rate of 1.7% (fiscal year 2025), would buy about 30 more hours."
  - Why: it says which way the difference runs.
- **B3** l.404 (+2).
  - Change: "Aim 2's go to the cohort's accounts and measures".
  - Why: "run" clashed with the runs counted just before.
- **B4** l.409-410 (-51).
  - Change: "The cadaver set adds WSU's own C-arm."
  - Why: the video-output point belongs to B6, and the cut pays for B5.
- **B5** l.411-412 (+47).
  - Change: "Each C-arm user enrolls in WSU's dosimetry program and files the training form of OEHS, WSU's safety office, both with the director of DLAR, which books the room, 15 business days before the session."
  - Why: OEHS and DLAR were undefined.
- **B6** l.412-413 (+15).
  - Change: "records what the C-arm shows, the input a deployed tool would read".
  - Why: "the deployment input" is jargon.
- **B7** l.426 (+20).
  - Change: "Anthropic's AI for Science program takes applications".
  - Why: it names the sponsor in the text, not only in the table.
- **B8** l.434-435 (-10).
  - Change: "Without B the request is $13,349: Aim 3 tests on the held-out devices' frames, and its 100 cadaver hours go to benchmark repeats;".
  - Why: the old phrasing read like notes.
- **B9** l.422-425 (-7).
  - Change: "The filing asks FDA whether..." and "A consultant at a mid-level rate reviews the PI's package in months 1 to 3."
  - Why: "It" had no clear referent, and "regulatory" repeated line D.
- **B10** l.416-417 (+12).
  - Change: "...two for the benchmark and development. All six are bought in January 2027, since the price holds".
  - Why: as written, only the last two seats read as bought in January.

### 2.3 Already done upstream by 23:24 (no action needed)

- The abstract's two-detector sentence.
- "patients" in paragraph 1.
- Paragraph 2's detector names.
- Aim 2's "submitted as abstracts to a national meeting".
- "hours to each task's first passing GPU job" in H2 and the table.
- Figure 2b's caption.
- The DeepDRR and SyntheX attribution.
- "leaving the crossover to wave 2".
- References [8] and [12].
- Future CoRe (NSF 25-543).
- The Bio Genesis wording.
- $50,000 per project.
- Figure fixes: Figure 1b's overlap, Figure 4b's key and Figure 4a's intervals.

### 2.4 Terms left to the owner

- "film-trained": optionally "radiograph-trained", at +5 characters each time.
- "Gaussian splatting" and "sacrum" stay undefined; there is no room.
- NIBIB is not spelled out.

## 3. Page slack measured

### 3.1 Room left on each page

Each figure is the room, in pt, between the lowest point of the last text line and the bottom of the text block.

| Build | p2 | p3 | p4 | p5 | p6 | Pages | Overfull boxes |
|---|---|---|---|---|---|---|---|
| Committed PDF, 22:38 (older text) | 1.5 | 1.0 | 29.5 | 34.5 | 29.6 | 8 | - |
| Current text, 23:24 | 1.5 | full | 5.6 | 34.5 | 29.6 | 8 | 0 |
| Plus the line edits (r6_main_with_line_edits.tex) | 1.5 | 0.9 | 17.6 | 34.5 | 29.4 | 8 | 0 |
| Plus the line edits and W1-W3 (r6_main_with_all_edits.tex; the preview PDF) | 1.5 | full | 5.6 | 34.5 | 29.4 | 8 | 0 |
| W1-W3 alone on the current text | 1.5 | full | -6.3 | 34.5 | 29.6 | 8 | 1 |
| W1-W3 with N2a-N2e only | 1.5 | full | 5.6 | 34.5 | 29.6 | 8 | 0 |
| All edits, W1-W3 and A8 | 1.5 | full | 5.6 | 22.5 | 29.4 | 8 | 0 |

- "Full" means TeX set text down to the page's last line. The measure reads about -1.6 pt, from a descender below the baseline, and there is no overfull box.
- The 23:24 changes used up page 4's slack: about 2.5 lines in the committed PDF, now 5.6 pt (about half a line).
- The line edits win back about one line (17.6 pt), and W1 then spends it.
- Pages 5 and 6 keep their 2.5 to 3 lines.

### 3.2 Lines per paragraph, as built

"Room" is the space left on the paragraph's last line, in characters. "Net" is the total change in characters from that block's edits.

| Block | Room | Net | Printed lines |
|---|---|---|---|
| Paragraph 1 | ~2 | -4 | 7 -> 7 |
| Paragraph 2 | ~105 | -21 | 9 -> 8 |
| Paragraph 3 | ~2 | -5 | 12 -> 12 |
| Figure 1 caption | ~16 | +8 | 2 -> 2 |
| Aim 1 | ~16 | +12 | 11 -> 11 (12 with W1) |
| Aim 2 | ~74 | +16 | 12 -> 12 |
| Figure 2 caption | ~3 | -2 | 2 -> 2 |
| Figure 3 caption | ~23 | +10 | 2 -> 2 |
| Aim 3 | ~46 | +17 | 30 -> 30 |
| Figure 4 caption | ~7 | -1 | 2 -> 2 |
| Note under the table | ~22 | +12 | 2 -> 2 |
| Section 4 | ~76 | +29 | 10 -> 10 |
| R21 item | - | -7 | 6 -> 5 |
| B1-B5 bullet | - | +11 | 8 -> 8 |

In the table, T1 keeps the Data cell at 4 lines; T2 takes the Metrics cell from 3 lines to 4, which still fits inside the row's 4.

### 3.3 Sentence length, current -> edited

| Block | Mean words per sentence | Longest | Sentences over 40 words |
|---|---|---|---|
| Abstract | 40.1 -> 28.8 | 66 -> 38 | 3 -> 0 |
| Paragraph 1 | 45.3 -> 34.2 | 66 -> 43 | 2 -> 2 |
| Paragraph 2 | 54.0 -> 31.8 | 79 -> 52 | 2 -> 1 |
| Paragraph 3 | 47.0 -> 23.7 | 93 -> 42 | 4 -> 1 |
| Aim 1 | 34.5 -> 32.4 | 48 -> 47 | 3 -> 3 |
| Aim 2 | 37.7 -> 25.6 | 54 -> 43 | 4 -> 2 |
| Aim 3 | 42.3 -> 30.7 | 64 -> 61 | 7 -> 4 |
| Section 4 | 24.6 -> 22.1 | 46 -> 48 | 2 -> 1 |
| Alignment: targets | 27.0 -> 26.9 | 40 -> 41 | 0 -> 1 |
| Alignment: relevance | 35.8 -> 26.0 | 44 -> 44 | 2 -> 1 |
| Alignment: team | 30.8 -> 25.8 | 61 -> 45 | 1 -> 1 |
| Budget justification | 29.1 -> 28.0 | 59 -> 44 | 5 -> 2 |

## 4. Figures

All four figures keep their sizes: 7.10 x 1.97, 7.10 x 1.70, 2.62 x 1.62 and 7.10 x 1.48 in. At print size:

- the drawn labels are 6.8 pt or larger;
- the Figure 2b screenshot's text is about 6 pt;
- Figure 3a's text is about 7.5 pt.

The make_figures.py line numbers below are those of the current file.

- **Figure 1 earns its space.** It is the only picture of the whole loop and of why counting fails. Changes:
  - l.178: "Task and its pass/fail gate,\nwritten by people, sealed" ("hashed" is jargon).
  - l.182: "It passes: the result goes\nto the trainee for review" ("pull request" is jargon to a clinician).
  - l.204: panel c's title becomes "Aim 3: from labeled CT to X-ray"; the old title was abstract.
  - Caption: F1.
- **Figure 2 earns about half its space.** Panel 2a repeats 1a, 2b shows one button, and 2c holds the only cohort data. Changes:
  - l.222: the legend becomes "gray: before (recalled); green: after". The old legend used the British spelling of gray and did not say the ratings were recalled.
  - l.234: "H200 GPUs,\n4 nodes of 4", which drops the internal partition name.
  - l.242: "GPU jobs" replaces "the heavy lifting".
  - Caption: F2.
  - If room is needed later: drop 2a and set the figure about 1.45 in tall, which saves about 1.5 lines.
- **Figure 3.** Panel 3a is an archived drawing and stays as it is. Its "2 x 320^2" input label is unexplained, and the caption has no room to explain it. Changes to 3b:
  - l.303: "X-ray panel" replaces "detector", a word that collides with the vertebra detector.
  - l.305-306: the distances are labeled "745 mm to the spine" and "1,140 mm to the panel: 1.53 times larger". The old left label was clipped at the edge.
  - Caption: F3.
- **Figure 4 is the strongest figure.** It shows the success and the gap side by side, with intervals. Changes:
  - l.62: "Checked\nby the count\n991 / 1,009"; the old "Checked against the count" collided with the next label.
  - Caption: F4.
- **Nothing is unclear without the text** once the captions are edited, except 3a's input label.

## 5. Notes for the owner

- **Before Friday:**
  - CAREER eligibility turns on the tenure-track date (appointed January 2021). Fill the red mark before the panel reads "untenured Assistant Professor".
  - Lines B, D and F ($8,291, 45% of the request) need the AIDaS office's allowability answer.
  - Rebuild the packet after the edits; the PDF in daeeb53 is built from the 23:24 text.
  - Confirm that the Figure 2b crop shows no person's name or username at print size. SOURCES.md says the crop shows no grid login.
- **Wording to settle:**
  - Either define "rebuilt truth" in a clause or use N6n.
  - H3's "each held-out device": see H3x and the COBRA and DeepFluoro results.
  - The 0.74 threshold keeps the name "cross-device". It was adopted after the 0.25 result was seen. N6d says only where it was chosen, which is true, and the packet reports both thresholds.
- **Risks to check:**
  - It is untested whether the two Team Premium seats carry 360 benchmark runs, each with up to six repairs and two GPU-hours.
  - Expect an exempt IRB determination, and say so if the 2026 determination was exempt.
  - From round 5: PA-25-304 does not allow clinical trials, so keep the R21's 99-patient validation aim outside NIH's clinical-trial definition.
  - From round 5: the Trailblazer discourages preliminary data.
  - From round 5: [13,14] are not the PI's papers; N3b now says "like those of".
- **Team:** a letter from a spine-imaging or radiology advisor would answer the team gap, since the clinical collaborator's specialty is General Surgery.
- **Room number:** N6f takes room 0312 out of Aim 3, and budget line B3 keeps it.
