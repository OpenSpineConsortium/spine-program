# Revision log 3: collect-and-submit-1 (2026-09-24, ~15:45 EDT onward)

Owner while this ran: `collect-and-submit-1` (`SchwingNet/.manuscript_owner`, written 15:45, deleted at the end).
Scope: `main.tex`, `sections/*.tex`, `tables/{tab3_naming,tab_levelcheck}.tex`, `supplement.tex`, `NUMBERS.md`
("Revision 3"), this ledger. Nothing was committed (the coordinator commits). Figure files and `LEVELCHECK_MODEL.md`
sections 1-15 (last commit d0403de; working tree equals HEAD) were not touched. Unblinding has not happened; the
f6eval jobs 40431765/40431766 stay held.

Greg's rule of 2026-09-24 was applied first: every input of the task was checked against what revision 2 (rounds
1-3, `REVISION_LOG2.md`) had already applied, and nothing already done was redone.

## 1. Already applied by revision 2, verified here and not redone

| task item | state found (file, line) | verified how |
|---|---|---|
| (1) REVIEW2_RSNA.md six blocking defects, F6/F9/F16/F17, DRIVE_CHECK D1 (673 agreed AP in 143 cases) and D2 (no fine-tuned number credited to the unseen network) | `results.tex` "giving 676 agreed lateral vertebrae in 143 cases and 673 anteroposterior in 143"; Discussion P1 quotes only 96.4 % (zero-shot) and 97.0 % (count); Key Point 2 and the abstract label every fine-tuned number "fine-tuned" | read against REVISION_LOG2.md tables "(1) REVIEW2_RSNA.md, fix by fix" and "(1) REVIEW2_STATS.md"; the 86.9 % three-body zero-shot of the first run is replaced by the v9 lineage's 83.7 % (970/1,159), which is what D2's replacement now reads |
| (2) refs_corrections.bib, REFS_AUDIT.md | `refs.bib` holds the corrected `cobra2026` (Thummerer et al.), `castellvi1984`, `claim2024`, `ctsp1kdescriptor`, `carmlspine`, `genevahip`, `ljubljana2d3d`, `zheng2018pda`, `diffpose2024`; `hsiang2011` is uncited (the entry stays in the file, harmless); 35 of 35 cited keys carry a DOI | `grep` on refs.bib and the sections; `tools/check_limits.py` "references cited: 35 (limit 35); references with a doi: 35 of 35" |
| (3) MANUSCRIPT_CORRECTIONS.md sections 1-8, esp. 7 | lateral 601/617 (97.4 %), AP 608/631 (96.4 %), day-grouped 568/617 (92.1 %), coupled 991/1,009 (98.2 %), +1.0 [-1.9, 4.0] and +52.6 [44.1, 61.3] in the Results and Table 4; the ladder 74.8/89.9/93.1/94.8/95.8 in NUMBERS.md round 2 rows (k1, k3 and kfull printed; k2, k4, k5 in `CV_V9.md`); B4 in the limitations; EVAL_LEAKS labels: plain-film rows in the supplement as "selection split", render-vs-film +31.7 [21.0, 45.4] on 17 unseen NHANES spines, card gain 0.019 [0.008, 0.033] on 12 patient-held-out folds | read cell by cell against §7.1-7.2 and the supplement sections "Plain-film naming on the selection split", "Which source carries the detector", "Image-formation terms" |
| (4) LEVELCHECK_MODEL.md s12-s15 in the Methods | s14 (automated reference) and s15 (primary detector, 21 of 609) were in the Methods; s12-s13 were only "three secondary analyses" | **completed here** (section 2 below) |
| (5) CITABLE_CLAIMS.md: only VERIFIED rows | `zheng2018pda` (PDA, 140 paired images, 16.1 -> 11.2 %) and `diffpose2024` cited; LevelCheck's one-vertebral-height failure quoted from `levelcheck2012` with no "catastrophic"; X23D not cited; DeepFluoro truth not called optical tracking; the two Ljubljana sets not conflated (`ljubljana2d3d` = Tomaževič 2002, lumbar) | Discussion P3-P4 and Table 1 read against rows 11, 12, 13, 17, 18, 24, 25 |
| coverage numbers (`results/coverage/COVERAGE.md`, landed 11:09) | already in the Discussion ("three of 18 angle bins") and the supplement ("Same-device frames and view angle": C_lat 3 of 18, H* 0.19, joint 6 %; the learning-curve sets at 37 % / 0.63 at every N) | NUMBERS.md round 2, last-but-one row |

## 2. Changed in this revision (every number a NUMBERS.md "Revision 3" row)

| where | what | why |
|---|---|---|
| `supplement.tex` | New section **"Data integrity and quality controls"** replacing "Data completeness audit, summary", whose text becomes its first item. Items, each two or three sentences with the implementing file: completeness audit (99 gaps); patient-keyed evaluation gate (`tools/eval_gate.py`: train + val of the checkpoint and every ancestor seen; ImageNet/COCO the only exempt ancestor; unreadable link = error; sha-stamped dumps; `tools/holdout.py` raising on a missing bank; CHK-9 sweep of 563 quoted numbers: 323 / 81 / 58 / 101); checkpoint lineage (`tools/checkpoint_lineage.py`, 306 checkpoints, 133 unresolved; the 57 re-run numbers); split builder (`tools/make_split.py`, CHK-1..8, the cross-source key from `tools/leak_check.py`'s NHANES finding, 48 of 54); label-identifier guard (`tools/spineps_ids.py`; 2,437 / 2,714 / twelve spines -> 4 + 8 / 3,490 relabelled); box convention (69 detector numbers, A28); excluded sources (`tools/excluded_sources.py`; Mendeley 500 of 584; FluoroCap); release repairs (0533: 17,301,504 -> 250,067,995 B, nine checks, public object replaced; COBRA 5,013 duplicate entries, `tools/realxray_train.py` registry); automated reference (s14 readers A-D, PPV lower bound 0.90, SHA-256 freeze; calibration `\PENDING{G6}{...}`); pre-registration (the five commits with dates and hashes). The intro paragraph of the supplement names the section. | Greg, 2026-09-24: "make sure the leak gate in all other auditing tools and quality improvement workflow additions I made are documented in the supplementary materials and referenced in like one sentence in the methods" |
| `methods.tex`, "Statistical analysis" | One sentence before the software sentence: "Every reported number passed a patient-keyed evaluation gate that counts a model's, and its ancestors', training and checkpoint-selection persons as seen (supplement, with the other integrity checks)." (27 words by `check_limits.words`) | the one Methods sentence Greg asked for |
| `methods.tex`, "The LevelCheck comparison" | "and three secondary analyses are fixed before unblinding" -> "and the secondary analyses, including accuracy on the frames SchwingNet accepts against 97.6 % with coverage beside it, are fixed before unblinding (Table 3, Figure 6)" | task item (4): s13 selective S1 was not in the Methods; s12's M1/F1/D1 were only counted |
| `tables/tab_levelcheck.tex`, note c | Names the secondary analyses: M1 (exact one-sided McNemar on discordant persons, lumbosacral strata), F1 (non-ordinary alphabet, count-morphology disagreement, or the dual-loss head's probability at a threshold fixed on validation for >= 95 % and separately 97 % sensitivity), S1 (accept = anchored, unflagged, every margin at or above a value fixed on validation for >= 99.5 % validation accuracy; against 97.6 %; tested only from 152 accepted persons; coverage and the accepted-but-wrong count always printed) | the detail behind the Methods clause, at no body cost |
| `tables/tab3_naming.tex`, note d | Carries the abstention rule (decoded and single-crop names disagree, or posterior below 0.5; a default never tuned) | moved out of Methods "The network" for room (REVISION_LOG2 "For the next writer" candidate) |
| `results.tex`, "Transitional sample size" | The G5 placeholder now reads `\PENDING{G5}{data case: naming and detection against same-device count and acquisition-space coverage; plain-film (NHANES II) versus fluoroscopy N curve (Figure 5 in-domain panels)}` | task item (7) and Greg's new request (NHANES n-versus-accuracy; the DICOM acquisition variables as a second axis). `results/indomain/fit.json` (11:59, n_boot 2,000, every cell HELD OUT) and `RESULTS_PARAGRAPH.tex` exist, but Figure 5 has no in-domain panels (figure5.* are the 10:33 power build), the naming asymptotes are not identified at 87 persons, and no NHANES II N curve or DICOM-tag arm has run; nothing from fit.json is quoted (NUMBERS.md "Revision 3", last row) |
| trims for room (all measured with `check_limits.words`; no number or claim changed) | Methods: "(Table 1, with every exclusion; flow, Figure S1)" -> "(Table 1; flow, Figure S1)" (Table 1 still carries every exclusion in its notes); "six cadaveric specimens" -> "six specimens"; "the share and the density" -> "the share and density"; "replaces the percentile interval" -> "replaces it"; "The three C-ArmLSpine patients one labeller reads as L6" -> "The three contested C-ArmLSpine L6 patients"; the abstention sentence (18 words) out; "Transitional sample size" recast in one sentence. Results: "By 24 September 2026" dropped (Table 2 note e carries the date). Discussion P4: "whereas only the sweep's arc pose pools span the arc" -> "whereas the render arc pools span it"; "paired with its cone-beam CT" dropped; "saturates the same way" -> "saturates likewise"; P3: "more than public releases hold" dropped (Figure 5c shows it; the summary paragraph says none is verified). | body 2,999 of 3,000 after the additions (+27 gate sentence, +14 S1 clause, +5 placeholder) |
| header comments | `main.tex`, `methods.tex`, `results.tex`, `discussion_motivation.tex`, `supplement.tex`, both tables: a "Revision 3" line each | the files say what changed and why |

## 3. Limits after this revision (`tools/check_limits.py`)

Body (Introduction to Discussion) **2,999 of 3,000**; abstract 248 of 250; summary statement 242 of 255
characters; key points 3, no abbreviation; six figures, four components each, legends 59/60/60/60/56/45 words;
four tables, titled, no merged cell; **35 references, each with a DOI**; seven abbreviations; style greps 0;
banned word 0; the Discussion cites no figure or table; limitations second-to-last. `RESULT: FAIL` only on the
open placeholders (G0 7, G4 1, G5 16 including Table S2's 15 flagship-detector cells, G6 11 including the new
automated-reference calibration one) and the missing `figures/figure6.pdf`.

Headroom is one word. When G0 (age and sex; dates; postgraduate years), G5 (the data case) and G6 (the
comparison) land, about 150 words must go. Measured candidates, none used yet: the Methods "Naming, counting and
coupling" sentence on same-device detection subsets (18 words; the supplement has it); the Results sentence on
the 51 at-risk CT test persons (22; Table 2 row); the Discussion P4 saturation sentence (34; the supplement
section carries it); the Results detection-plateau sentence's "renders posed on all 148 cases' geometry" clause
(7; supplement); the Methods statistics "percentile with the BCa interval beside" clause (9; Table 4 header).

## 4. Grid build

Sources rsynced from WSL (main.tex, rsnastyle.tex, supplement.tex, refs.bib, latexmkrc, nejm.*, sections/*.tex,
tables/*.tex, figures/*.pdf), CR stripped on the grid, `sbatch -D ~/logs slurm/compile.sh`.

**Build 1, job 40437793** (submitted 15:47:35, ran 15:48:17-15:48:50 on voh1, queue wait 42 s, 34 s of work;
whole log `~/logs/schwingnet_tex-40437793.out` read): texlive/2020, TeX Gyre Termes; `latexmk rc=0`, **main.pdf
27 pages**; biber clean (0 warnings in main.blg); main.log: 1 LaTeX warning, the same stale "There were undefined
references" line every build since 07:30 carries, no "??" anywhere in either PDF (pymupdf text scan); boxes: an
underfull line in reference 12 (as before), Table 1 10.8 pt over (as before), **Table 4 45.9 pt over** (lines
185-253 of main.ttt; it was 142 pt before round 2's page fit; the rendered page 21 shows every row and note g
complete, nothing clipped, but the table owner should still bring the tabular inside its 23.2 cm minipage).
`latexmk supplement rc=0`, **supplement.pdf 15 pages**, one overfull line (44.7 pt) in the new section where
`\texttt{results/bodybox\_rescore/RESCORE.md}` could not break.

**Build 2, job 40437794** (submitted 15:51:11, ran 15:51:16-15:51:41, 25 s): after two supplement edits, the
path moved to the end of its sentence (residual 3.7 pt overfull, lines 221-224, invisible at print) and the
supplement set `\singlespacing` after `\begin{document}`. **supplement.pdf 12 pages** (the journal's cap; the
double-spacing rule in RSNA_AI_REQUIREMENTS.md governs the manuscript text file, the supplement's own rule is
"at most 12 pages, one Word document, not copy-edited"). main.pdf 27 pages, unchanged. Both PDFs and logs copied
into the working tree (`main.pdf`, `supplement.pdf`, `main.log`, `supplement.log`, 15:51 build) and kept in the
session scratchpad `rev3/build/`.

**Pages looked at** (rendered with pymupdf at 1.3x): main 17 (legend tail), 18 (Table 1), 20 (Table 3, note c with
the named secondary analyses), 21 (Table 4, note d with the abstention rule), 22-26 (Figures 1-5, drawn), 27
(Figure 6 = the red PENDING marker over its caption); supplement 4-5 (the new section, its PENDING G6 marker in
red), 6 (Table S1), 7 (Table S2 with its 15 PENDING G5 cells), 8 (Figure S1), 12 (Figure S5). Nothing clipped,
every figure file drawn.

**For the figure owner** (not a manuscript file): Figure 4a's on-figure text still says "sacrum at confidence
0.74: 233 of 290 frames, both views (80.3 %)"; the text and Table 4 say "a sacrum box on 233 of the 286 frames
showing one (81.5 %)" (REVIEW2_RSNA Fix 23, REVIEW2_STATS N15). `figure5.caption.txt` still carries the
"2026-09-24" date the legend prints.

**Final `tools/check_limits.py`:** body 2,999 of 3,000; abstract 248; summary statement 242 characters; key points
3; figures 6 (59/60/60/60/56/45-word legends); tables 4; references 35 of 35 with a DOI; abbreviations 7; style
greps 0; banned word 0; `RESULT: FAIL` on 35 open number placeholders (G0 7, G4 1, G5 16, G6 11) and the missing
`figures/figure6.pdf` only.

## 6. PENDING (grid and gates), as of 2026-09-24 15:55 EDT

| item | job / state | submitted | ETA | output | collected by |
|---|---|---|---|---|---|
| this pass's compile | 40437794 COMPLETED 15:51:41 | 15:51:11 | done | `~/spinesurg-ct-nnunet/SchwingNet/{main,supplement}.pdf` (15:51); working-tree copies | this ledger (done) |
| section-15 primary detector, post stage (registry, lineage, gate, validation recall) | `g3det_post` 40437708, PENDING (Resources) at 15:51; training 40436991 COMPLETED 13:25 (best epoch 36, val mAP50 0.945); first post 40436992 FAILED on a JSON key-type bug, fixed | 15:35:39 by detector-g3 | compute about 8 min once it starts; GPU partitions were full of `acq_*` arrays, so 16:00-16:30 | `/rs/rs_grp_oschome/go2432/data/fig6/detector_g3/post/det_g3_primary_s0/POST.json`, log `~/model_night/logs/g3det_40437708.out` (`G3DET_POST_OK`) | detector-g3 -> the coordinator resubmits `slurm/fig6_eval.sh` on `det_g3_primary_s0/weights/best.pt` (HELD) and writes `results/fig6/EVAL_SUBMITTED.json`; fills Table S2's 15 G5 cells later |
| f6eval 40431765 / 40431766 | HELD (JobHeldUser), untouched | 07:09 | -- | -- | must stay held (they carry the pre-section-15 detectors); unblinding has not happened (`/rs/.../data/fig6/unblinding/` empty) |
| automated reference: calibration and freeze (s14 R2) | no job submitted by this pass; reader C csvs written 11:02-11:03, readersAB assembled 10:40 | -- | a CPU job of minutes once the rule-selection step is run | `results/fig6/frozen/{auto_reference.json,auto_truth.csv,auto_reference.sha256}` | auto-reference workflow; fills the supplement's `\PENDING{G6}{automated-reference calibration ...}` and gates f6eval's release |
| Figure 5 in-domain panels (the data case) | `results/indomain/fit.json` 11:59 and `RESULTS_PARAGRAPH.tex` 10:50 exist; figure not rebuilt | -- | a local figure build (no grid job) | `figures/figure5.*` with panels a/b, `figure5.caption.txt` | indomain-curve workflow -> the next writer fills `\PENDING{G5}{data case ...}` (about 80-100 body words; cut list in section 3) |
| plain-film (NHANES II) N-versus-accuracy curve and the DICOM-variable axis (Greg, 2026-09-24) | not designed, not submitted (an experiment, not a re-score: needs a person-disjoint test film set, which exists only on the G3 test side scored by the Figure 6 arm, plus the C-ArmLSpine headers on the grid) | -- | -- | -- | owner to be assigned by the coordinator; the same placeholder names it |
| G6 comparison, Figure 6 | blocked on the two rows above | -- | -- | `figures/figure6.*`, Table 3 cells, Results, abstract | paper-six-figures fill after EVAL_SUBMITTED.json + the frozen reference |
| G4 corpus census; G0 (dates, age and sex, postgraduate years, determination, notification date) | not started / Greg | -- | -- | -- | coordinator / Greg |
| anomaly-harvest `acq_*` arrays (tcia_fdg_pet_ct_lesions, abdomenatlas3_mini, curvas, waw_tace, kidney, pengwin, barts, aortaseg60, quadra_hc, deep_psma, panorama, idc; dedupe2) | running or dependency-pending since 2026-09-23 19:34 and 2026-09-24 06:42-07:35; 3-day limits | -- | hours to days | `results/transitional_registry/acquisition/` | anomaly-harvest workflow; none feeds this manuscript pass |

## 5. Open for Greg (decisions, not text)

1. Unchanged from REVISION_LOG2: determination 2026-269 and VinDr-SpineXR / C-ArmLSpine; the notification date;
   REVIEW2_STATS U2-U4; the Figure 6 fallback; the postgraduate years of the two Castellvi readers.
2. The NHANES II n-versus-accuracy curve and the DICOM-variable axis (Greg, 2026-09-24): no such analysis exists.
   The same-device naming curve (`results/indomain/fit.json`) is C-ArmLSpine cases only; the development curve in
   the supplement pools every source. A film-only curve needs a person-disjoint test film set, which exists only on
   the G3 test side (BUU 341, CSXA 499, NHANES 939 persons) and can be scored only by the ImageNet-initialised
   Figure 6 arm; the DICOM-tag axis needs the C-ArmLSpine headers already on the grid
   (`/rs/rs_grp_oschome/go2432/data/carmlspine/headers_dossier.json`; MANUSCRIPT_CORRECTIONS.md §8 last paragraph).
   This pass did not design or submit it (it is an experiment, not a re-score); the placeholder names it.
3. The supplement's page count against the journal's 12 (see section 4).

## 7. Revision 4: thoracic level confirmation (2026-09-24, after 16:00 EDT; Greg's request)

**What Greg asked.** "Incorporate this fact into the manuscript, there's a reason to improve the detection or
automatic assistance in level confirmation: thoracic vertebrae lack myotomes, no way to localize certainly from a
neurophysiological standpoint."

**How it was written (precisely).** No primary source says thoracic vertebrae lack myotomes, and anatomically they
do not (intercostals, abdominal wall). What the sources say: the ISNCSCI motor examination has key muscles only at
C5–T1 and L2–S1, so T2–L1 are "not clinically testable" and the thoracic motor level is presumed from the sensory
level (Kirshblum 2011, full text); intraoperative triggered EMG records thoracic screws from the rectus abdominis,
"making individual dermatome analysis impossible" (Kulik 2013, full text). No paper tests level *naming* by EMG at
all; the EMG papers measure breach detection. So the sentence says what is documented and stops.

**Inserted, Introduction paragraph 1, after the 4.3–15 % clause and before the transitional-vertebra sentence**
(`sections/introduction.tex`): "Only imaging confirms a thoracic level: the standard motor examination tests no key
muscle between the first thoracic and second lumbar segments \citep{kirshblum2011}, and thoracic screw stimulation is
recorded from the rectus abdominis, which cannot separate segments \citep{kulik2013}." (36 words by
`check_limits.words`). "Between the first thoracic and second lumbar segments" is written out because T2 is outside
the abbreviation list (T11–T13, L1–L6). In the same paragraph the Furuya clause now reads "a registry of 34,544
consecutive patients recorded 0.12 % (thoracic 0.42 %, lumbar 0.13 %)": the regional per-operation rates are in
its abstract; "operated for degenerative disease" was dropped for room (4 words out, 4 in); the independent check found the
abstract does state it ("spinal surgery for degenerative disorders"), so the phrase is supported and may return when words free up. Mody's thoracic 8 % is a share of events, not a per-operation risk, and was not used.

**Reference swap (35 of 35 before and after).** New: `kirshblum2011` (J Spinal Cord Med 2011;34(6):535–546, PMID
22330108, doi 10.1179/204577211X13207446293695) and `kulik2013` (Eur Spine J 2013;22(9):2062–2068, PMID 23686531,
doi 10.1007/s00586-013-2754-0), full author lists and pages re-verified against PubMed efetch, entries appended to
`refs.bib` and `lit/refs_additions.bib`. Out: `konin2010` (an AJNR review cited once, Introduction, for "so counts
from the sacrum and from C2 name different vertebrae"; the clause went with it, and nakagawa2017's 38 of 71 carries
the consequence) and `diffpose2024` (Discussion paragraph 4, a future-work aside carrying no number of ours). Both
were named by the verifier as the weakest candidates; `he2016` (the third named) stays, so the Methods were not
touched. Both entries remain in `refs.bib`, uncited, like `hsiang2011`.

**Words (all measured with `tools/check_limits.py`, the repo's counter: `\input` expanded, comments and
figure/table environments stripped, `\citep{}`/`\ref{}` removed, tokens containing a letter or digit counted).**
Body 2,999 of 3,000 before, **2,999 after**. Introduction 310 -> 320; Discussion 644 -> 634; Methods 1,257 and
Results 788 unchanged; abstract 248 unchanged. Cuts, each with no number or claim changed:
Introduction: "so counts from the sacrum and from C2 name different vertebrae \citep{konin2010}" (-11, see above);
"vertebral bodies" -> "bodies" and "the surgeon counts" -> "surgeons count" (-2); "the labels a reader assigned to the
preoperative CT" -> "a reader's preoperative CT labels" (-4); "those same labels" -> "those labels" (-1); "the median
of five surgeons reading 62" -> "five surgeons' median on 62" (-2); "of patients" after 77.9–82.2 % (-2); "has
imported identity" -> "imported identity" (-1); "so that a level" -> "so a level" (-1); "a C-arm absent from
training" -> "an unseen C-arm" (-2, the abstract's own wording). Introduction net: +36 - 26 = +10. Discussion
paragraph 4: ", and one patient's rotational acquisition would admit patient-specific self-supervised registration
\citep{diffpose2024}: both are future work" -> ", a route untried here" (-10). The Discussion cut was needed because
the Introduction had 26 words of harmless trims against a 36-word addition; the REVISION_LOG3 section 3 candidates (saturation sentence 34, at-risk
CT persons 22, same-device subsets 18) are still unused.

**Also.** `lit/CITABLE_CLAIMS.md` gained the section "Thoracic level confirmation" (rows 31–54: the ten
neurophysiology sources and the fourteen wrong-level sources the verifier opened, each with its quoted sentence and
whether it is cited). Header comments in `introduction.tex` and `discussion_motivation.tex` carry a "Revision 4"
line. Not touched: `main.tex`, `methods.tex`, `results.tex`, the abstract, tables, `LEVELCHECK_MODEL.md`, results
files, `numbers_manifest.json`, any `\RESULT` macro. Nothing compiled on the grid and nothing committed (the
coordinator submits compile.sh). `check_limits.py` after: 35 references, 35 with a DOI, 7 abbreviations, style greps
0, banned word 0; `RESULT: FAIL` still only on the open placeholders and the missing `figures/figure6.pdf`.

Coordinator note (18:50 EDT, after the check): the opening clause was softened from "Only imaging confirms a thoracic level" to "No neurophysiological check confirms a thoracic level" (the two sources establish the absence of a neurophysiological check, not the exclusivity of imaging), and "is recorded from the rectus abdominis, which cannot separate segments" became "recorded from the rectus abdominis, cannot separate segments" (-2 words); net -1 word, body 2,998. Compile submitted on the grid after this commit; job id in docs/RESUME_2026-09-22_PM.md.

## 8. Revision 5: the LevelCheck / surgeon comparison moved to paper 2 (2026-09-24 evening; Greg: "you take care of this")

**What Greg asked.** "I'd like to move the comparison to neurosurgeons / all the LevelCheck stuff into a new paper,
remove it from the current paper." Paper-1 HEAD when the move began: `dd8f4a562709af202541f422efe42525c29beaa0`.
Nothing was deleted: every passage went verbatim, with file and line, into
`paper2_levelcheck/MOVED_FROM_PAPER1.md`; the manifest entries into `paper2_levelcheck/numbers_manifest_moved.json`;
the Table 3 files by `git mv` into `paper2_levelcheck/tables/`. The scope rule is `PAPER1_SCOPE.md`.
`LEVELCHECK_MODEL.md`, `results/`, `figures/*.pdf` and the running / held jobs were not touched.

**Changed, file by file.**

| file | change |
|---|---|
| `main.tex` | Title: "versus registration-assisted neurosurgeons" dropped (below). Header comment: five-figure story, tables 1-3, a "Revision 5" block. Summary statement: "its frozen comparison with registration on transitional spines awaits verified patients" -> "its transitional naming on real exposures rests on three patients and awaits verified cases" (246 characters). Key point 3: the 97.6 % / 152-person clause -> "on real exposures its transitional evidence is three cross-validation patients, and certifying 90 % exact-level accuracy needs 35 error-free at-risk persons, of whom seven real-frame candidates exist". Abstract: Purpose's fourth aim -> "and count the transitional persons such a test needs"; Materials and Methods "Exact binomial power set transitional sample size; a LevelCheck comparator was frozen beforehand" -> "Wilson bounds set transitional sample size against pre-stated targets"; Results' last two sentences -> "No real-exposure transitional test person was verified; certifying 90 % needs 35 error-free at-risk persons, and seven real-frame candidates exist"; Conclusion's second clause -> "its transitional naming on real exposures rests on three cross-validation patients and awaits verified cases" (abstract 248 words). Data availability: the LEVELCHECK_MODEL.md clause out. Registration: "Not a clinical trial; not registered." kept, the comparator sentence out. Figure 5: legend re-written (59 words; (a) "persons to certify an accuracy", (b) captioned for what it draws without naming the comparator), comment says why the PDF is unchanged. Figure 6 block out. Table inputs: `tab_levelcheck` out; comment lists three tables. Abbreviation and Figure 1 comments updated. |
| `sections/introduction.tex` | Purpose sentence: "and derive how many transitional persons a comparison with a pre-specified model of LevelCheck needs" -> "and count the transitional persons a test of it needs and the public sources hold". Paragraph 2 (LevelCheck prior art) unchanged. Header comment. |
| `sections/methods.tex` | "Reference standard": "Held-out transitional persons without a human read ... specified by commit before unblinding (Table 3)" -> "Test persons without a human read ... fixed by commit before scoring (supplement)". "Transitional sample size" rewritten: the two pre-stated Wilson targets named, "at risk" defined here (L6, T13, a sacralised L5 on a four-lumbar count), and the sentence "of its transitional test persons only the three C-ArmLSpine L6 patients, scored in cross-validation, enter a result here". "The LevelCheck comparison" paragraph out. "Statistical analysis": the exact-binomial power sentence -> "Transitional sample size is the smallest person count at which the Wilson 95 % lower bound with zero to five errors reaches a target (Figure 5a)"; ", one-sided .025 for the frozen comparison" out. Header comments. |
| `sections/results.tex` | "Transitional sample size": "With no error, the frozen exact test needs at least 19 at-risk persons against 82.2 % and 152 against 97.6 % (Figure 5c)" -> "With no error, 35 at-risk persons put the Wilson lower bound at the pre-stated 90 % and 22 carriers the variant-sensitivity bound at 85 % (Figure 5a, c)"; "the three C-ArmLSpine L6 patients were excluded in advance" -> "are scored only in cross-validation (Table 3)". The G5 placeholder unchanged. "The LevelCheck comparison" paragraph out. Header comment. |
| `sections/discussion_motivation.tex` | Paragraph 3 replaced by: "On real exposures the transitional evidence here rests on three C-ArmLSpine patients whose sixth lumbar vertebra one labeller reads and the other does not, scored in cross-validation and agreeing with that read on one of five bodies; that is a description, not a test of transitional naming. The powered comparison with registration carrying a planning read, on verified at-risk persons against a comparator fixed before scoring, is a separate study. No accuracy here is a wrong-level surgery rate." Paragraph 4: "The comparison arm's level model saturates likewise in development: doubling its training persons" -> "A level model trained from ImageNet weights on the split's training persons saturates likewise in development: doubling those persons". Header comment. |
| `sections/discussion_limits.tex` | "so the comparison uses a separately trained arm" -> "so no model reported here scores them"; "Where no person read a transitional test spine" -> "a test spine". Summary: "Whether it names transitional spines better than registration ... none is verified" -> "Its transitional naming on real exposures is unverified: three cross-validation patients carry the only real transitional exposures scored, certifying 90 % needs 35 error-free at-risk persons, and seven candidates exist." |
| `tables/tab3_naming.tex` (+ `.md`) | Now prints as Table 3. The "Transitional stratum ... PENDING G6 per stratum" row out; the three-C-ArmLSpine row heads the block as "Transitional, real exposures" with a Table 2 pointer. Header comments. |
| `tables/tab4_transitional.tex` (+ `.md`) | Note c: "The three real C-ArmLSpine L6, whose outputs were seen before the comparator was frozen, are excluded from its primary analysis in advance and reported descriptively" -> "are scored only in cross-validation, as agreement with one labeller's read (Table 3)". Note d: "so the transitional comparison needs an arm trained without them" -> "so a transitional test needs an arm trained without them". Note f: "the own-label sacralised L5 are naming unaffected under the frozen rule (Table 3) and are not in the at-risk bound" -> "at risk = L6, T13 and the four-lumbar sacralised L5, the subtypes a count from the sacrum or from C2 misnames; an own-label sacralised L5, Castellvi I/II and a lumbar rib leave the count unchanged and are not in the at-risk bound". Header comments. |
| `tables/tables_check.tex`, `tools/tables_check.py` | the `tab_levelcheck` input out; `N_TABLES = 3`. |
| `supplement.tex` | Plain-film section: "until the ImageNet-initialised model of Figure 6 of the main text is scored" -> "until a model trained from ImageNet weights on the split's training persons is scored ..., which is not done here". Section title "Development learning curve of the comparison arm" -> "... of a split-trained level model", first clause accordingly. "Table 4, note g" -> "Table 3, note g". Pre-registration paragraph reduced to the automated-reference commit (b511985) and the never-edit rule; the comparator commits moved. Automated-reference paragraph and its PENDING G6 calibration kept. Header comment. |
| `numbers_manifest.json` | Removed: `power_n_min_h1_822`, `power_n_min_h2_976`, `power_n_min_g6_level_90`, `fig6_h1_coupled_accuracy_pct`, `figures.figure6` (all in `numbers_manifest_moved.json`). `figures.figure5` job note says panel (b) drops at the next rebuild. |
| `TITLE.md` | New title recorded with the reason; the 2026-09-23 title kept on record as paper 2's natural title; ERAS entry updated. |
| new | `PAPER1_SCOPE.md`; `paper2_levelcheck/MOVED_FROM_PAPER1.md`; `paper2_levelcheck/numbers_manifest_moved.json`; `paper2_levelcheck/tables/tab_levelcheck.{tex,md,sources.md}` (git mv). |

**Title.** `TITLE.md` and `main.tex` named the comparison ("versus registration-assisted neurosurgeons"). Applied:
**SchwingNet: a convolutional-recurrent network for level naming in spine surgery, robust to transitional anatomy.**
The 2026-09-23 title is kept in `TITLE.md` for paper 2. Whether "robust to transitional anatomy" survives in paper 1
is Greg's call (the evidence behind it did not change: embedding on the selection split, the coupled alphabets, three
real cross-validation patients).

**Figures: five, not six.** The limited-FOV / real-frame test does not stand as its own sixth figure: its result is
already drawn in Figure 4b (three-body field, fine-tuned) and printed in Table 3's field rows and the Results, and
the only existing file that plots accuracy against bodies in view (`figures/fig3_naming.*`, retired) was drawn from
the first-run fold models whose encoder lost its training record (EVAL_LEAKS U1), so it would show numbers the paper
no longer reports. Building a new figure from the v9-lineage closure files is a figure job, not this pass. Figure 5
keeps its four panels on disk; panel (b) is re-captioned, not removed, because `tools/fig_power.py` stops by design
(line 308) once `results/fig6/frozen/auto_reference.json` exists, and it exists; at the next rebuild (owned by the
indomain-curve workflow) drop panel (b) and the 19 / 152 verticals and re-letter c, d -> b, c.

**Tables: three.** 1 `tab_corpus` (tab:data), 2 `tab4_transitional` (tab:transitional), 3 `tab3_naming`
(tab:naming). Kept in Table 3 as paper 1's own cross-validation results: the count, classifier and coupled rows,
the stop signal, the L6 calls, and the three-C-ArmLSpine agreement row; moved: only the G6 per-stratum row.

**References: 34 of 35.** Dropped from the citation list: `yun2018` (cited only in Table 3, row H5). Still cited:
`peh1999`, `manbachi2018`, `desilva2016`, `levelcheck2012`, `levelcheck2016`, `nakagawa2017` (Introduction).
Every entry stays in `refs.bib`; every cited key exists and carries a DOI.

**Limits after this revision (`python tools/check_limits.py`).** Introduction to Discussion **2,747 of 3,000**
(Introduction 319, Methods 1,072, Results 758, Discussion 598; the freed words were not spent: nothing was padded);
abstract **248 of 250**; summary statement 246 of 255 characters; key points 3, no abbreviation; **figures 5**,
panels a-d each, legends 59/60/60/60/59 words; **tables 3**, titled, none merged; **references 34**, 34 with a
DOI; abbreviations 7; style greps 0; the Discussion cites no figure or table; limitations second-to-last of six
paragraphs. `RESULT: FAIL` only on the open placeholders: **G0** (7 occurrences of 5 items: first download date x 2,
age and sex x 2, postgraduate years, VinDr determination, date notified), **G4** (corpus census), **G5** (the
data-case paragraph; plus Table S2's 15 flagship-detector cells), **G6** (the supplement's automated-reference
calibration paragraph only). No PENDINGFIG remains. `python tools/results_macros.py --check`: 12 resolved, 1
pending (`coverage_hstar_lat_surgio_real`: pointer `surgio_real_pool` missing; the pointer fix is a separate item),
13 unused keys (every remaining key: the RESULT-macro conversion pass has not run, RESULTS_BUILD.md "Status"),
CHECK FAIL as before this revision on those two counts; no moved key is reported.

**Open after this pass (not in this pass's file list).** `packet_src/cover_letter.md` (paragraphs "What it does
not show" and "The comparator was fixed before the result"), `packet_src/front_matter.json` (`registration`
statement and the `levelcheck_prespecification` block, which the packet builder checks against git),
`packet_src/statements.md` items 8-9, `CLAIMS_LEDGER.md` / `claim_checklist.json` rows on the comparison,
`figures/figure5.caption.txt` (tool-written; differs from the main.tex legend until the rebuild), `README.md`
table row, `NUMBERS.md` rows for Table 3 and Figure 6 (history; left). If the open-gate ordinary-person real-frame
result is printed in paper 1, paper 2 must log that H6's stratum was seen (`PAPER1_SCOPE.md` item 3). The two
radiology residents named by Greg for the CTSpinoPelvic1K grading (Miraziz Ismoilov; Nizar Alnabahneh) came without
postgraduate years, so the G0 "postgraduate years" placeholder stays for the fill step, as does the
age/sex-by-source script. Nothing compiled on the grid and nothing committed (the coordinator commits).

### 8, fill pass (2026-09-24, late evening; Greg: "You take care of this I don't have the brainpower to spare")

**What was filled, from what.** Paper-1 HEAD `887e37cc92b8d9d20d05637d711581f2cc21a254` plus the uncommitted revision-5
tree. Facts came from `results/g0_facts.md` (readers, dates, ethics), `results/age_sex_by_source.json` /
`.md` (tools/age_sex_by_source.py, 2026-09-24 20:34; VinDr headers by grid job 40438307, COMPLETED, already consumed),
`results/corpus_census.json` / `.md` (tools/corpus_census.py, 20:32, from the frozen split) and
`results/fig6/frozen/auto_reference.json` (sha256 `57782cad…`). Nothing ran on the grid; no job was submitted.

| item | file | what changed | evidence |
|---|---|---|---|
| G0 readers | `sections/methods.tex` "Sources and transitional phenotypes" | "(in-training; PENDING postgraduate years)" -> "(in training; year of training not recorded)". No institution and no names in the anonymized file. | Greg 2026-09-24 supplied names only (Miraziz Ismoilov, radiology resident; Nizar Alnabahneh, resident); every record in both repositories says Department of Radiology, DMC/WSU; **no training year is recorded anywhere** (grep PGY/postgraduate/resident over both repos, ledgers, Zenodo, descriptor title page), so none is printed and none invented. Six disagreements confirmed in `docs/castellvi_consensus.csv` (six paired, one unpaired). |
| G0 first download date | `sections/methods.tex` "Design"; `main.tex` abstract | "analysed from April 2026, when the first collection was downloaded, to 24 September 2026"; abstract "analysed April--September 2026". Month precision. | CTSpinoPelvic1K-1 first commit 550cfff (2026-04-18) already holds `scripts/download_tcia_colonog.py`; "fix raw" 8e68379 2026-04-19; no on-grid file of that download survives (`~/data/hf_export` gone; patient_db.json is a 2026-05-16 rebuild), so the day is not defended. First external collection: VerSe via VerSeFusion 2026-05-12 (grid ctime). |
| G0 age and sex | `main.tex` abstract; `sections/results.tex` "Study population"; `numbers_manifest.json` (+4 keys); `tables/tabS3_age_sex.tex` (new, generated); `supplement.tex` overview | Abstract: "source median ages \RESULT{agesex_csxa_age}--\RESULT{agesex_cobra_age} years, \RESULT{agesex_ts_pct_female}--\RESULT{agesex_csxa_pct_female} % female, none for the intraoperative, cadaveric or phantom sets" (36--66; 42.5--64.5). Results: the compact form (the per-source list would have cost ~165 words against a data-case paragraph still owed), pointing to supplement **Table S3**, which `tools/make_supp_census_tables.py` writes from the JSON with its SHA-256. **The draft's "radiotherapy sets release none" was false**: COBRA2026 ships `ct.PatientAge`/`PatientSex` in every case's metadata.yaml (age on 115, F/M on 75 of the 145 detector cases; 347 / 319 of 692); the sentence now names only the intraoperative, cadaveric and phantom sets. COBRA is quoted for the 145 Table 1 cases (the 692-case row is in Table S3). | Keys: `agesex_csxa_age` -> `#/sources/csxa/age_median_str`, `agesex_cobra_age` -> `#/sources/cobra_detector/age_median_str`, `agesex_ts_pct_female` -> `#/sources/ts/pct_female_str`, `agesex_csxa_pct_female` -> `#/sources/csxa/pct_female_str`; job `tools/age_sex_by_source.py (local, 2026-09-24 20:34; VinDr headers by grid job 40438307)`. All resolve (`generated/numbers_audit.md`). Persons, not images; female share over recorded F/M. |
| G0 Ethics: VinDr | `main.tex` "Ethics" | Now states the fact and keeps ONE G0 placeholder: "VinDr-SpineXR was obtained under its PhysioNet data use agreement, which determination 2026-269 does not cover (it is limited to data obtainable without an application or agreement); it trained the intraoperative fold models only (Table 1) and \PENDING{G0}{a separate determination (number and date), or its removal from the fold banks and a re-run of the fold models; Greg's decision}". | HPR memo 2026-269 (2 Sep 2026) criterion (2) and its exclusion sentence (`OSC_HPR_Determination_public_datasets.pdf` pp. 4-5; scanned memo p. 1); VinDr landed 2026-09-07, after the memo; no separate submission exists in either repo. The text may not claim coverage; the resolution (retrain = G5 re-run, or a new determination number) is Greg's. |
| G0 Ethics: notification date | `main.tex` "Ethics" | The clause "and the dataset authors were notified on <date>" is **dropped**; the sentence now states only what was done to the frames (exported without header data, checked to carry no identifier value). A tex comment records why. | No record that any notice was sent (finding 2026-09-22: `docs/RESUME_2026-09-22_PM.md` l.2273, `PATIENT_IDENTITY_SPEC.md` alias 16; grep "notif" finds nothing). Greg should still send it (Zenodo 10.5281/zenodo.22768651 contact); the clause returns with the date. |
| G4 census | `supplement.tex` "Corpus census"; `tables/tabS4_census.tex` (new, generated); `tools/make_supp_census_tables.py` (new) | Placeholder replaced by a paragraph written from `results/corpus_census.json` and by **Table S4** (17 rows: the 13 Table 1 sources plus AASCE, Spinal-AI2024, lateral236, Mendeley; persons, primary images and transitional persons per side; the registry column; Table 1's cells beside). The paragraph says which differences are different objects (bank / fold-bank / detector case split vs the split's placement) and which are unexplained (footnote a 7,045 vs 7,048; Ljubljana and the second sweep in no root). | census `summary`, `discrepancies_vs_table1`, `unknowns`. |
| Table 1 reconciliation | `tables/tab_corpus.tex`, `.md`, `.sources.md` | Only two footnotes changed, both where the census file is authoritative: **b** "in no bank; its rebuild enters no reported number" -> "in no trained bank; rebuilt and replaced in the release (802 records in the released corpus, supplement Table S4), it enters no reported number" (the repair landed: `results/repairs/ct0533_CHECK.md`, jobs 40416624 swapped=1 count=802 and 40416626 ctsp_drr=802; the 801 in the body and in footnote j stay because they count the trained bank and the abstract's 4,093 renders); **d** "At most 3,598 by content" -> "3,598 by content ... which the built split merges" (`group_of` buu:0629->0449, buu:0719->0140; the cell keeps "3,600 cases" because its unit is the case number). **Not changed**, with the reason: TS 1,935 scans (the split's 1,867 are content-hash groups, not persons); the BUU AP films (placed by the split, in no level bank, as printed); NHANES 364 / VinDr 2,071 / FluoroCap (bank objects); C-ArmLSpine 296 / 210-30-56, DeepFluoro 238-24-104, COBRA 2,640-192-648 (the detector's scored case splits; the census sides are the G3 person-hash draw of different objects); Geneva 19 keys (views of one phantom); footnote a 7,045 vs 7,048 (unexplained; left as printed). |
| G6 calibration paragraph | `supplement.tex` (paragraphs "Automated reference standard" and "Pre-registration" out); `sections/methods.tex` (the automated-reference sentence out); `sections/discussion_limits.tex` (one sentence out); `paper2_levelcheck/MOVED_FROM_PAPER1.md` item 8 (new); `paper2_levelcheck/numbers_manifest_moved.json` (+18 `autoref_*` keys); `PAPER1_SCOPE.md` item 3 amended | **No result paper 1 prints rests on the automated reference**: Table 2 note e and the Results' "seven at-risk persons" are the two-labeller count (SPINEPS+VERIDAH and a TS rib count), not the three-reader Dawid-Skene rule; the three C-ArmLSpine L6 are scored against one labeller's read; no ordinary-person real-frame result is printed. So, per the task rule, the paragraph and its \PENDING{G6} moved verbatim, with the Methods and Discussion sentences that introduced it and the pre-registration paragraph (which recorded only that commit). Item 8 also gives the paragraph **filled** from the frozen file through 18 keys, every pointer verified to resolve: Dawid-Skene at posterior >= 0.95, ordinary only (no rule reached a PPV lower bound of 0.90 for every subtype it assigns); coverage 88.6 % (86.4, 90.4); ordinary PPV 0.971 (0.957, 0.981), 769 of 792, errors 22 L6 + 1 T13; sensitivity 0.881; L6 unanimity 14 of 14 but Wilson LB 0.785 < 0.90, not certified. The file's `ppv`/`coverage` arrays are `[point, lo, hi]`, so the `ci` kind must not be used on them (one key per element). If the open-gate ordinary-person result is printed here, the passages return from item 8 and paper 2 logs that H6's stratum was seen (`PAPER1_SCOPE.md` 3). |
| coverage pointer | `numbers_manifest.json` `coverage_hstar_lat_surgio_real`; `supplement.tex` "Same-device frames and view angle" | Pointer `/training_sets/surgio_real_pool/H_lat` (no such entry) -> `/corpora/carmlspine_registered/dims/lat/entropy_norm` = 0.1947 -> prints **0.19**, now quoted in the supplement in place of the typed 0.19 ("the registered poses occupy three lateral bins (normalised entropy 0.19)"). The task's "about 0.24" matches nothing in the file: the 296 consensus registrations (148 AP + 148 LAT, the note's pool) read 0.19; the 299 header-tag spot exposures (`carmlspine_headers_spot`) read 0.31; 0.24 is the case134 spin's H*_roll and the rare_class ctsp render root's H*_joint in COVERAGE.md. | `results/coverage/coverage.json`, COVERAGE.md table A. |
| G5 comments | `sections/results.tex` header | The done-work comments (the PENDING G5 fold-model re-run, "Figure 5 still draws the power panels", the Revision 3 "placeholder stays") rewritten as a source-of-numbers note; exactly ONE placeholder left in the file, the Figure 5 data-case paragraph, now tagged "waits on grid jobs 40437811 (film N-curve collect) and 40437814 (coverage-arms collect)". | `results/coverage/PENDING_JOBS.json`; `results/indomain/fit.json` exists but Figure 5 is unrebuilt and no film N curve / coverage arm result exists. |
| title | `supplement.tex` line 53 | "Supplemental material for *SchwingNet: ..., robust to transitional anatomy, versus registration-assisted neurosurgeons*" still carried the dropped clause; removed. `main.tex` and `TITLE.md` already agree. | |
| checker | `tools/check_limits.py` `words()` | A `\RESULT{key}` now counts as one word (it prints one number); before, the key's underscores made `\RESULT{agesex_csxa_age}` three words and the abstract read 261 with the same printed text. | |
| build doc | `RESULTS_BUILD.md` "Status" | one line: the agesex keys and the two generated supplement tables exist. | |

**Checks after this pass.**
`python tools/results_macros.py`: **17 resolved, 0 pending** (was 12 resolved, 1 pending). `--check`: UNUSED 12
(`figure1`-`figure5`, the seven det_/naming_ keys: the RESULT-conversion pass has not run), 0 pending, **CHECK FAIL**
on the unused keys alone; the bare-number rule prints nothing because `--check` reports unused first (unchanged).
`python tools/check_limits.py`: Introduction to Discussion **2,730 of 3,000** (Introduction 319, Methods 1,047,
Results 783, Discussion 581); **abstract 248 of 250** (the age/sex clause cost 13 words; trimmed "[CI]", "the count
from the detected sacrum" -> "the sacrum count", "148 cases from an unseen C-arm" -> "148 unseen-C-arm cases", "such
a test needs" -> "a test needs", "and seven" -> "; seven"); summary statement 246 characters; key points 3, no
abbreviation; figures 5, four panels each, legends 59/60/60/60/59; tables 3, titled, none merged; references 34,
34 with a DOI; abbreviations 7; style greps 0; the Discussion cites no figure or table; limitations second-to-last
of six paragraphs. `RESULT: FAIL` only on the open placeholders: **G0 x1** (VinDr determination or removal; Greg's
decision), **G5 x1 in the Results** (the data-case paragraph; jobs 40437811, 40437814), **G5 x15 in Table S2**
(the flagship-detector cells, unchanged by this pass). G4 and G6 are closed; no PENDINGFIG.

**Not compiled.** No TeX on this machine; the coordinator submits `slurm/compile.sh`. Two new supplement tables
(S3 portrait footnotesize, 8 columns; S4 landscape 7 pt in the Table 1 minipage) have not been measured; if S4
overruns the 16 cm line, narrow its two transitional columns.

**Open for Greg after this pass.** (1) VinDr-SpineXR: a separate determination number, or drop it from the fold
banks and re-run the fold models (G5). (2) Send the C-ArmLSpine header-identifier notice and, if the sentence should
say so, supply the date. (3) The readers' training year, if it is to be printed (the sentence stands without it).
(4) Whether the Results should carry the full per-source age/sex list (Table S3 holds it). (5) Nothing committed.

### 8, packet pass (2026-09-24, late evening; Greg: "Please continue the restructure from where the session timed out")

**What this pass did.** Every file outside the tex that the submission packet or a reader consults was brought to
paper 1 as restructured (section 8 above; `PAPER1_SCOPE.md`; `paper2_levelcheck/MOVED_FROM_PAPER1.md`, whose new
section 9 holds the removed passages verbatim). One tex edit, allowed by the task: `main.tex` key point 3, "of whom
seven real-frame candidates exist" -> "and seven real-frame candidates exist" (`check_limits.py`: body 2,730 of
3,000, abstract 248, key points 3, figures 5, tables 3, references 34; RESULT FAIL only on the open G5 / G0
placeholders, as before). `LEVELCHECK_MODEL.md`, `results/`, `figures/*.pdf`, `numbers_manifest.json` and every
Slurm job untouched.

| file | change |
|---|---|
| `packet_src/cover_letter.md` | "What it does not show" rewritten to paper 1's statements (three cross-validation patients; 35 error-free at-risk persons certify 90 %; seven real-frame candidates, none verified; the comparison is a separate study); "The comparator was fixed before the result" removed; "Why this journal" without the comparator clauses; headline numbers brought to the v9-lineage cells the manuscript prints (595/617, 276/631 zero-shot anteroposterior, 601/617, 568/617, 1,079/1,159, 979 and 991 of 1,009), which the builder had already flagged as absent from main.tex. |
| `packet_src/front_matter.json` | `trial_registration` = "Not a clinical trial; not registered."; `levelcheck_prespecification` marked paper-2 material, d0403de added (six commits), every commit `in_letter=false` (the builder keeps the git check, requires nothing of the letter); `comparator_public_deposit` moved out of paper 1's decisions (kept under `moved_to_paper2_2026-09-24`); `title_clauses` reworded to the remaining clause; the stale note that main.tex still carried the guarantor and conflict statements corrected. |
| `packet_src/numbers.json` | 38 numbers on `zeroshot_v9.json`, `cv_v9.json` (pre:cv5_det, pre:cvday_det, coupling pre det74/kfull), `a1.json`, `figure2_metrics.json`, `power.json` (cobra calls re-pointed to `real_screen_calls`); `levelcheck_*` and `need_97_6` (157) out, recorded under `moved_to_paper2_2026-09-24`; text-only "90" (the pre-stated target) added. |
| `packet_src/statements.md` | the comparator file out of every statement; evidence-table row on the code repository reworded; edit-phase notes 4 (done), 8 and 9 (moved) rewritten. |
| `packet_src/claim2024/map.json` | items 2, 6, 14, 16, 18, 20, 21, 24-26, 28, 34, 36-38, 42 re-pointed (14, 16, 18, 20, 38 READY; 37 PENDING G5; 42 "No": no protocol for paper 1; 36 "Yes": age and sex per source in Results and Table S3); `fig:levelcheck` / `tab:levelcheck` out of every placement; items 8, 11, 31-33, 36, 39 re-anchored to the revision-5 wording (the builder had listed 20 unresolved anchors). |
| `packet_src/supplement_technical.tex` | three comments and one sentence: the "Figure 6 arm" is the split-trained arm, scored in paper 2; the sentence names no scored configuration; "Table 4" -> "Table 3". |
| `packet_src/README.md` | a state section for the evening; Files rows for front_matter, cover letter, title page, numbers.json; the morning's sections kept as record with a note. |
| `CLAIMS_LEDGER.md` | rows marked moved in place: section 6 "parity with or better than surgeon + LevelCheck"; section 8 "5 persons needed" (exact-test clause, panel (b); amended to the Wilson targets and the two-labeller seven), "6 vs LevelCheck", the "fail enough" paragraph, the title note; acquisition-space row 3 wording; new section 9. |
| `tools/gen_claim_checklist.py` -> `claim_checklist.json`, `CLAIM_CHECKLIST.md` | item 2 SATISFIED (the G6 clause moved; abstract 248 words, no placeholder); item 34 rewritten to the true state (per source done, Table S3; per partition owed, gate G5); regenerated: 30 SATISFIED, 12 GAP; `check_claim_checklist.py` PASS. |
| `tools/check_claim_checklist.py`, `tools/check_limits.py` | the banned-word regex spelled in two halves so neither checker's own text carries the word. |
| `tools/make_packet.py` | `FIG_EXPECT` five labels, `TAB_EXPECT` three; docstring and PACKET_README text (Figures 1-5, Tables 1-3, no Figure 6 page). It had exited at import on "main.tex floats changed". |
| `tools/write_figures_md.py` | drops `#` header lines when reading a caption sidecar. |
| `figures/figure5.caption.txt` | equals the main.tex Figure 5 legend; header line says `tools/fig_power.py` regenerates it and that its caption string still names the comparator in panel (b) (update at the rebuild that drops the panel). |
| `atlas/update_cards.py` -> `model.json`, `dataset.json`; `atlas/README.md` | every comparison / Figure 6 statement replaced by paper 1's (section 9e of MOVED_FROM_PAPER1.md); the `power.json` pointer `rows.pooled.real_verified_primary` (no such key since the 10:32 schema; the updater raised) repaired to `rows.at_risk_pooled`; cards regenerated, `validate_cards.py` 0 errors, 5 RadLex warnings as before. |
| `README.md` (SchwingNet) | a state block; rows for main.tex, supplement.tex, tables/, CLAIM files; "What is not in the manuscript" gains the comparison. |
| `NUMBERS.md` | one block at the top pointing the Table 3 / Figure 6 / comparator rows to `paper2_levelcheck/`; the rows themselves left as history. |
| `docs/DATASHEET.md` | section 2.4: the claim that no age or sex can be stated is narrowed to the intraoperative, cadaveric and phantom sets, with a dated correction paragraph (COBRA2026 `ct.PatientAge` on 115 and `ct.PatientSex` on 75 of 145; 347 / 319 of 692); the "Claiming a population" bullet likewise. |
| `main.tex` | key point 3, the one allowed edit (above). |

**Grep decisions (LevelCheck, comparator, neurosurgeon, Figure 6, Table 4, tab:/fig:levelcheck, "no age", registration).**
Corrected as paper-1 statements: every file in the table. Left as history or paper 2: `LEVELCHECK_CLAIM.md` (the 2026-09-23
literature file behind the comparator; paper 2's), `DRIVE_CHECK.md`, `FINAL_CHECK.md`, `REVIEW*.md`, `REVISION_LOG*.md`,
`sections/SOURCES.md` (the draft-to-source map of the Discussion as written on 09-23), `lit/*` (literature),
`figures/figure5.record.json`, `figures/fig6_claim.*` and `tools/fig_claim.py` (retired figure), `tools/fig_power.py`
(the rebuild owned by the indomain-curve workflow drops panel (b)), `tools/fig6_*.py`, `tools/stats_review2_recompute.py`,
`tools/verification_worklist.py`, `tools/contribution_matrix.py`, `tools/figure*.py` (record comments), `packet_build/*.md`
and `packet/` (build outputs, regenerated by the builders), `numbers_manifest.json` (not to be edited; its figure5 job note
already says panel (b) drops), `TITLE.md` (already records the move). Left because they are not the comparison: the
Introduction's LevelCheck prior-art sentences and their citations (`PAPER1_SCOPE.md` "Stayed, on purpose"); "pose by
registration" in Table 1 and the datasheet (C-ArmLSpine's 2-D/3-D pose); the repository `README.md` sections 5-6
(the benchmark protocol's registration arm as a ceiling, `docs/BENCHMARK_PROTOCOL.md`: the CT benchmark, not paper 1);
`tables/tab_corpus.tex` "pose by registration"; CLAIM item 40 "Registration number and name of registry" (the journal's
item). "No age or sex": `sections/results.tex` and `supplement.tex` already correct (fill pass); `docs/DATASHEET.md`
corrected; `CLAIMS_LEDGER.md` and `packet_src/` never said it; CLAIM 2020 item 34's "radiotherapy patient" clause and
CLAIM 2024 item 36's note corrected; `atlas/dataset.json` already gave the COBRA counts.

**Builder checks.** `python packet_src/build_packet_src.py` (draft): **0 hard problems, 0 unresolved CLAIM anchors, 0
placement mismatches**, 20 open author markers, CLAIM 2024 35 READY / 3 PENDING / 6 NEEDS-EDIT, 2 anonymization hits (the
network's name; the allowed descriptor citation), 7 open author decisions (before the pass: 13 hard problems, 20
unresolved anchors). `python tools/make_packet.py` has no dry or check mode (no argparse; it exits on a float mismatch
before building). Run in full after the float lists were fixed: it first reported one problem, an anonymization hit on
the descriptor preprint `ctsp1kdescriptor`, which the Methods cite since the fill pass and which only the Zenodo key
`ctsp1k` was allowed to name; and its log showed `\RESULT{}` macros left raw, which pandoc drops, so the docx abstract
lost the age and sex numbers. Both fixed (pre-existing, not the move): `front_matter.json anonymisation.allowed_self_citations`
= [`ctsp1k`, `ctsp1kdescriptor`] and the same two entries accepted in `make_packet.py`; `make_packet.tex2md` now expands
`\RESULT{key}` from `generated/numbers.tex` (a missing key prints `[PENDING result: key]`). Second run: **PACKET OK**;
`manuscript.docx` 101 paragraphs, 3 tables, 2 `[PENDING]` markers (G0 VinDr; G5 data case), 0 anonymization hits, the
abstract reads "source median ages 36–66 years, 42.5–64.5 % female"; `figures.docx` Figures 1-5 with their 1,200-dpi
TIFs; `supplement.docx` built; ATLAS 0 errors. Still warned, not fixed: `\pm` (inside math; pandoc renders it) and
`\texttt` in the supplement (pandoc's raw-TeX handling), both pre-existing.

**Open after this pass.** (1) The ATLAS cards' naming, field and coupling numbers still come from `results/a4.json`,
`a7.json`, `a9.json` (first-run fold models) while the manuscript prints the v9-lineage cells; re-pointing `update_cards.py`
is a G5-fill item, not the move. (2) `tools/fig_power.py`: at the next rebuild drop panel (b) and the 19 / 152 verticals,
re-letter c, d -> b, c, and bring its caption string to the legend (the sidecar header says so). (3) Paper 2's cover
letter must name the fourth amendment d0403de, which the paper-1 letter never did. (4) Whether "robust to transitional
anatomy" stays in paper 1's title (front_matter `title_clauses`; Greg). (5) Nothing committed.

### 8, supplement length (2026-09-24 night; Greg: "Please continue the restructure from where the session timed out")

The fill pass took the supplement to **15 pages** (build 40438373, 21:16) against the journal's 12 (REVIEW2_RSNA.md
"Supplement <= 12 pages"; DRIVE_CHECK.md). Layout of that build: prose pages 1-6 (page 6 held three lines), Tables
S1-S4 one page each (S1 is a rotated 23.2 cm minipage; endfloat with `tablesfirst` gives every table environment a
page of its own), five figure pages. Twelve pages therefore means prose + S1 in five pages. Commits ad823e5, 82451f5;
compiles 40438389 (13 pages) and **40438392 (12 pages, latexmk rc 0, 0 warnings, 0 overfull boxes, no `^!`)**.

| item | file | what changed | evidence |
|---|---|---|---|
| Tables S3 + S4 -> one Table S3 | `tools/make_supp_census_tables.py` (`--merged`, `--two-tables`); `tables/tabS3_corpus.tex` (+ `.md`, new); `tables/tabS3_age_sex.md`, `tabS4_census.md` (repository copies, headers say so; their `.tex` forms are no longer written); `supplement.tex` (input, overview, header comments) | One landscape table "Corpus by source", 17 rows (13 Table 1 sources + AASCE, Spinal-AI2024, lateral236, Mendeley-716): source; persons (train / val / test; hold; excluded); images real / rendered; transitional persons (subtype table, test side in parentheses; registry after the semicolon); age median [IQR] (n); % female (n); age and sex read from. Footnotes a (no age or sex released: C-ArmLSpine placeholder birth date, DeepFluoro 022Y placeholders, Geneva phantom, Ljubljana none), b (audit repairs: 0533 -> 802 here / 801 in the banks; 299 spot exposures after the case134 repair against 296 scored; 301 sweep projections; second sweep and 18 Ljubljana frames in no root; COBRA frames counted once after the duplicate-root repair), c (the Table 1 subsets: NHANES II annotated 364, 65 [62-69], 55.2 %; COBRA detector 145, 66 [56-73] on 115, 54.7 % on 75), d (sex codes excluded: CTSP 11, VinDr 68, COBRA 120 of 692; TCIA top-code 89 on 31; the NHANES join; the VinDr header read), e (excluded sources), f (no Table 1 row, not read), g (transitional column definition), h (Spinal-AI2024 machine-generated). Body `\footnotesize`, `tabcolsep` 3 pt, notes 7 pt on 7.6 pt as Table S2's; no merged cells; rotated 23.2 cm minipage as S2. Numbered **S3**, so the abstract's and Results' "Table~S3" (sections/results.tex l.35, main.tex, both untouched) stay right; no Table S4 exists. Every cell of the two old tables is either in the merged table, in its footnotes or in the `.md` repository copies (per-subtype counts, roots, Table 1's cells beside). | page 7 of build 40438392 rendered and read; `tables/tabS3_corpus.tex` note names both source files with SHA-256 (age_sex 1882037348892521; census ded51200361f4e23). |
| Table 1 footnotes b, d | `tables/tab_corpus.tex`, `.md` | "supplement Table~S4" -> "supplement Table~S3" (the only two S4 references outside supplement.tex and the packet build files). | grep "Table~S4" over `*.tex`: none left. |
| Table S1 inside the prose | `tools/make_supp_device_table.py`; `tables/tabS1_device_terms.tex`; `supplement.tex` (`\renewcommand{\thetable}` moved to the top of the body; the input sits at the end of "Data integrity and quality controls") | Portrait at 7 pt on 7.6 pt (Table S2's body size), 0.5 + 2.3 + 1.1 + 1.3 + 4 x 2.4 cm = 15.9 cm with the gaps, and **not a float**: a `[tbh]` table went to a page of its own (build 40438389: prose to page 5 at 55 %, S1 alone on page 6, 13 pages) because rsnastyle's endfloat delays every `table` environment; it is now a minipage with `\captionof{table}` that prints where it is input and shares page 5 with the text. Counter runs S1 (inline), S2, S3 (delayed). | page 5 of build 40438392: text to y = 716 of 757 pt, about three lines to spare. |
| Prose trim | `supplement.tex` | (1) Overview paragraph: the per-figure legend repetition replaced by one sentence listing Figures S1-S5 and Tables S1-S3; the title sentence folded into it. (2) Census paragraph: the side counts the merged table prints (16,272 / 9,581 / 4,981 / 10,274; C-ArmLSpine 123 / 13 / 13, DeepFluoro 4 / 1 / 1, COBRA 445 / 71 / 159 hold 17) are no longer repeated; 0533, 1,867 / 1,935, 3,598, 364 / 2,071 / 145, 3,600 AP films, the registry adds, 7,045 / 7,048, the 18 Ljubljana frames and the second sweep stay. (3) "Data integrity and quality controls" to two dense paragraphs, one bold pointer per tool: completeness audit (99 / 31 / 28 / 21 / four / 15), `eval_gate.py` + `holdout.py`, leak check CHK-9 (563 / 323 / 81 / 58 / 101, `quoted_results.json`, `EVAL_LEAKS.md`), `checkpoint_lineage.py` (306 / 133 / 57, `LINEAGE.md`), patient keys and split builder (`make_split.py` CHK-1..8, 50:10:40, `leak_check.py`, 48 of 54), `spineps_ids.py` (2,437 / 2,714 / twelve / four / eight / 3,490), **results-driven build** (`numbers_manifest.json`, `results_macros.py`; the task listed it among the pointers to keep and the section had never carried it, so one sentence was added), box convention (69, `RESCORE.md`), `excluded_sources.py` (500 of 584), release repairs (0533 17,301,504 of 250,067,995 bytes, nine checks, `ct0533_CHECK.md`; 5,013, `realxray_train.py`, `cobra-dup-leak_CHECK.md`). Prose tex chars 20,783 -> 18,900; paragraphs 22 -> 15. **No number and no tool name removed** (checked by listing them before and after). | `git diff 9bed078..82451f5 -- SchwingNet/supplement.tex`. |
| header comments | `supplement.tex` l.39-46, table block comment | The length pass recorded beside the fill pass; the "Tables S1-S4" comment now says S1-S3 and why S1 is input inside the prose. | |

**Checks after this pass (local).** `python tools/check_limits.py`: Introduction to Discussion **2,730 of 3,000**
(319 / 1,047 / 783 / 581); abstract **248 of 250**; summary statement 246 characters; key points 3; figures 5, four
panels each, legends 59/60/60/60/59; tables 3, all titled, none merged; references 34, 34 with a DOI; abbreviations 7;
style greps 0; `RESULT: FAIL` only on the placeholders that were open before this pass (G0 x1 VinDr determination; G5
x1 Figure 5 data case, jobs 40437811 / 40437814; G5 x15 Table S2 flagship cells). `python tools/results_macros.py
--check`: **17 resolved, 0 pending**; UNUSED 12 (`figure1`-`figure5` and the seven det_/naming_ keys; the
RESULT-conversion pass has not run) -> `CHECK FAIL` on the unused keys alone, unchanged by this pass. Grid build
40438392: `PDF_PAGES 23`, `SUPP_PDF_PAGES 12`, latexmk rc 0 both, 0 LaTeX warnings both, no `^!` in supplement.log.

**Open after this pass.** (1) Page 5 has about three lines of slack; any added supplement prose must come with a cut
or the supplement returns to 13 pages. (2) The packet builder's lists (`packet_src/statements.md` item 4,
`packet_src/build/BUILD_REPORT.md`, `claim_checklist_2024.json`, `claim2024/map.json` "about_expect") still name
`tab:census` as Table S4 and `tab:agesex` as S3; both labels now resolve to Table S3 (the merged table carries both),
so the next `tools/make_packet.py` run should re-derive them; not edited here (another writer's files). (3)
`main.tex` l.51 comment says "supplement Table S4" (comment only; main.tex not mine to edit). (4) `RESULTS_BUILD.md`
"Status" still says two generated supplement tables exist; it is one merged table plus two `.md` copies. (5) The
packet's `supplement.docx` must be rebuilt from this build.

- 2026-09-24 ~22:05 (coordinator; Greg 21:45 "drop"): Table S2's three flagship-detector rows (15 G5 cells) removed from paper 1 and kept verbatim in paper2_levelcheck/MOVED_FROM_PAPER1.md item 10; caption clause and header comment updated; the supplement now has no G5 placeholder. Remaining placeholders: G5 data-case paragraph (results.tex) and G0 VinDr (Ethics; separate HPR determination being filed).

- 2026-09-24 ~22:15 (coordinator; Greg's four points): (1) Discussion limitation on the first encoder's deleted training record REMOVED (discussion_limits.tex; Table 3 note g simplified; supplement QI sentence reworded to 'every quoted zero-shot and fine-tuned number comes from an encoder whose whole chain was read'; CLAIM map anchor repointed); (2) readers 'postgraduate year 2' (methods.tex); (3) title = "SchwingNet: a convolutional-recurrent network for level naming in spine surgery" in main.tex, supplement.tex, TITLE.md, README.md, packet_src/README.md; (4) April 2026 confirmed by Greg ('I started the project in April').

- 2026-09-24 ~22:45 (coordinator; Greg): Ethics line -- the sentence on the C-ArmLSpine rotational acquisition's residual header identifiers removed at Greg's instruction (the analysed frames were exported without headers; the finding stays in docs/PATIENT_IDENTITY_SPEC.md alias 16 and results/g0_facts.md; Figure S5 unchanged, it was never removed). Abstract: 'On the checkpoint-selection split, the sixth lumbar vertebra separated from the fifth ... more than the fifth from the fourth' -> 'In the embedding (checkpoint-selection split), the sixth lumbar vertebra was farther from the fifth ... than the fifth from the fourth' (Greg could not parse the original; numbers unchanged).

## 9. Data-case fill: the last result placeholder (G5) replaced (2026-09-25, after the 10:02 pooled fit and the 10:26 Figure 5 rebuild)

**What was open.** `sections/results.tex` held one `\PENDING{G5}` (the Figure 5 data-case paragraph), waiting on grid chains 40437811 (film N curve collect) and 40437814 (coverage-arms collect). Both collectors COMPLETED; `tools/indomain_fit_coverage.py` (local, 2026-09-25 10:02) wrote `results/coverage/pooled_fit.json` (+ `POOLED_FIT.md`, `sensitivity/pooled_fit_conf074.json`, `pooled_fit_trained_only.json`); `tools/fig_power.py` (10:26) rebuilt `figures/figure5.{pdf,png,tif}` with panels (a) Wilson chart, (b) film N curve, (c) matched-N coverage arms, (d) pooled fit, and `figure5.caption.txt` equals the legend in `main.tex` (60 words; unchanged here).

| what | file | change | check |
|---|---|---|---|
| The paragraph | `sections/results.tex` "Persons, films and coverage." (replaces `\PENDING{G5}`) | Film N curve: NHANES II / BUU-LSPINE / CSXA accuracy at N = 5 / 25 / all, the one corpus within two points of its asymptote on the grid (CSXA from 200 persons; NHANES II and BUU-LSPINE -3.2 / -3.1 points from theirs at all persons), the cross-corpus ceiling (74.3 %, NHANES II -> CSXA). Coverage arms at matched count (2,646 renders, 125 subjects): arc minus AP/LAT pool +23.6 / +15.1 points on the unseen sweep (two seeds), pools doubled +13.3 / +7.3; the gain on obliques (+39.1 / +26.0); recall on the device's real spot frames FELL (4.9 -> 0.7 %, 9.1 -> 1.0 %); the Elekta XVI arms did not train. Pooled fit over 105 points: count plus coverage beats count alone (dAICc 26.0; LR 29.1, P < .001; g +20.0 points per unit lateral-angle entropy, 12.2 to 27.7) with the arms read at confidence 0.25, chosen after 0.74 left them almost no detections; at 0.74 the term adds nothing (P = .82). Cites Figure 5b, c, d. No claim beyond the numbers; the Elekta arms are named as untrained, the real-frame fall is stated, the confidence choice is disclosed. | every number is `\RESULT{key}` (36 new keys below); `results_macros.py --check` PASS |
| 36 manifest keys | `numbers_manifest.json` | `film_{nhanes,buu,csxa}_acc_{n5,n25,all}_pct`, `film_*_n_all_persons`, `film_csxa_n_within_2pt_key`, `film_{nhanes,buu}_all_minus_asymptote_pp`, `film_transfer_nhanes_to_csxa_pct` (job 40437811 -> the fit's film_summary block); `cov_arm_surgio_matched_n`, `cov_arm_surgio_subjects`, `cov_contrast_surgio_{high,low2n}_{s0,s1}_diff_pp`, `cov_contrast_surgio_high_{s0,s1}_oblique_pp`, `cov_realtest_surgio_{low,high}_{s0,s1}` (job 40437814 -> matched_contrasts, asserted to be Surgio high s0 / high s1 / low2n s0 / low2n s1 at indexes 4-7); `cov_pooled_{n_points,daicc,lr_stat,lr_p,g_pp_per_unit_hstar,g_ci_lo,g_ci_hi,arm_conf}` and `cov_pooled_lr_p_conf074` (the fit script; the sensitivity file). All into `results/coverage/pooled_fit.json` (+ `sensitivity/pooled_fit_conf074.json`), pointers verified against the files before the keys were written. | `generated/numbers_audit.md` |
| Three kinds | `tools/results_macros.py` | `k_of_n` ("43 of 56": the prose form of `kn`), `ci_bare` ("93.2, 99.0": the prose form of `ci`), `p` ("<.001", else "=.82"; the tex writes `$P\RESULT{key}$`). Deterministic formatting only; nothing is invented. | |
| The twelve unused seed keys | `numbers_manifest.json`, `sections/results.tex`, `main.tex` | Wired, so `--check` passes for the first time. `figure1`-`figure5`: `main.tex` includes each figure through `\RESULTFIG{figureN}` (same includegraphics options). `naming_lateral_cv_v9_{pct,kn,ci}`: **re-pointed** from `rep:cv5_det` (606/623 = 97.3 %) to `pre:cv5_det` (601/617 = 97.4 %; 93.2, 99.0), the family the text, the abstract and Table 3 quote; the case-grouped lateral sentence now reads them. `det_carm_sacrum_074_{kn,pct}`: `results/a1.json` cross_device_0.74 sacrum 43/56 = 76.8 %, wired into "43 of 56 sacra (76.8 %)" (the percent is new in the prose; Table S2 carries it). `det_carm_body_recall_074_{pct,kn}`: **re-pointed** to `results/indomain/det_fill.json#/cells/lc_surgio_b51_dr_N0_s0/recall/ALL/body/0.74` (20/287 = 7.0 %), the learning-curve N = 0 row the text quotes; the seed entry read `results/a1.json` cross_device_0.74 vertebra_recall_body = 15/287 (5.2 %), the reported detector on body boxes, which no sentence quotes. No quoted number changed. | values printed by `results_macros.py`: 97.4 / 601 of 617 / 93.2, 99.0 / 43 of 56 / 76.8 / 7.0 / 20 of 287 |
| Figure 5 citations | `sections/results.tex` "Transitional sample size" | "(Figure 5a, c)" -> "(Figure 5a)"; "64.6 % (Figure 5c, d)" -> "(Figure 5a)": the old panels c, d (persons per stratum, zero-error intervals) are paper 2's (MOVED_FROM_PAPER1.md item 4); panel a is the Wilson chart that gives the 64.6 % at seven persons. | `main.tex` comment updated |
| Methods | `sections/methods.tex` end of the intraoperative block (after Figure S5) | Two sentences (52 words) so the Results report a described experiment: naming against training persons on NHANES II / BUU-LSPINE / CSXA with a render-only encoder on nested person subsets; matched-count render-only detector arms (AP/LAT pools, an arc of poses, pools doubled; two devices, two seeds); the nested inverse-power fit with and without the lateral-angle entropy term (the supplement defines it), compared by AICc and likelihood ratio. | |
| Discussion | `sections/discussion_motivation.tex` paragraph 4 | The data-case sentence contradicted the result: "We hypothesise that coverage, not count, set it ... no arm varies view alone, so this is untested." The arms now vary pose alone at matched count, so it reads: the arms found more bodies on held-out oblique poses and on one real rotational acquisition and fewer on the device's real spot frames; the pooled fit preferred count plus coverage on one device and only at a confidence below the operating point reported here; coverage is a held-out-angle effect shown on renders, not an account of the plateau on real frames. No number typed. | |

**Not built.** The DICOM-variable map (Figure S6): only one device group (C-ArmLSpine Surgio-B51, 299 dossier frames) has five or more per-image header fields on disk; NHANES II, BUU-LSPINE and CSXA are pixel files, VinDr has only age and sex read, COBRA2026 ships geometry-only metadata. `results/coverage/DICOM_VARIABLES.md` records this and the one grid job (a VinDr header CSV) that would make it possible. The supplement is untouched (12 pages, page 5 with three lines of slack).

**Checks after this pass (local).** `python tools/results_macros.py`: **54 resolved, 0 pending**. `--check`: no unused key, no bare result numeral in Results or main.tex, **CHECK PASS**. `python tools/check_limits.py`: Introduction to Discussion **2,976 of 3,000** (319 / 1,108 / 943 / 606); abstract 249 of 250 (untouched); summary statement 246 characters; key points 3; figures 5, four panels each, legends 59/60/60/60/59; tables 3; references 34 of 35; abbreviations 7; style greps 0; open placeholders **G0 VinDr only** (`RESULT: FAIL` on that alone, Greg's decision).

**Open for Greg.** (1) The film asymptotes: NHANES II and BUU-LSPINE are still rising at N = all; the analytic persons-to-plateau values (944, 1.5e5) are extrapolations and are not quoted. (2) The pooled g rests on one device's arms (Surgio-B51); the six Elekta XVI arms did not train (val mAP50 0.13-0.22, zero recall everywhere) for a cause not established; the text says "did not train" and nothing more. (3) The verdict flips at confidence 0.74 (stated in the paragraph). (4) `results/a1.json` cross_device_0.74 vertebra_recall_body (15/287) and the learning curve's stage-2 N = 0 row (20/287) are two different "no frame of the device" detectors; the text quotes the second and the manifest now says so.

**Grid build 40443631** (2026-09-25 10:40 EDT, commit 63f92c5): `numbers.tex: 54 resolved, 0 pending` on the grid; latexmk rc 0 main and supplement; `PDF_PAGES 23`, `SUPP_PDF_PAGES 12`; 0 LaTeX warnings in both; no `^!` in main.log or supplement.log; 0 "Result Pending" markers.

**Independent check of section 9 (2026-09-25, commit df8decf).** Every one of the 37 `\RESULT` keys in the data-case paragraph was opened at its pointer in `results/coverage/pooled_fit.json` (and `sensitivity/pooled_fit_conf074.json`) and the derived values were recomputed from the raw files: the film means at N = 5 and 25 from the three seeds of `film_ncurve.json`, the best cross-corpus transfer (NHANES II N = 200 -> CSXA 74.3 %) across all 48 cells, the Surgio unseen-sweep recall (0.553/0.789, 0.610/0.761), the near-AP and oblique (tilt 0, 20-70 degrees) bins and the real-frame recall from each arm's `unseen/recall_vs_angle.json` and `scores.json`. Figure 5 panels b-d plot the same numbers; legend 60 words, equal to the caption file. One wording fix: at confidence 0.74 the Surgio arms keep 7.8-16.7 % unseen-sweep recall (case134 and real frames ~0), so "almost no detections" became "few detections". Grid build **40444165** (commit df8decf): 54 resolved, 0 pending; latexmk rc 0; `PDF_PAGES 23`, `SUPP_PDF_PAGES 12`; no `^!` in either log. Note for Greg: `arms.json` marks all six Elekta arms `trained: True` and the 105-point fit includes them (`arms_excluded_untrained: []`); the trained-only sensitivity fit (99 points) gives the same verdict (dAICc 32.0, g +24.2, P = 3e-9), so the sentence "did not train" describes their scores, not the fit's bookkeeping.

## 10. Two copies from one source: the review copy anonymized by one flag (2026-09-25, Greg's seven instructions of that morning)

**The rule.** `rsnastyle.tex` defines `\newif\ifcameraready`, FALSE by default (= the double-anonymized REVIEW copy),
and inputs `cameraready.flag.tex` (`\camerareadytrue`) when that file exists. Only `slurm/compile.sh` writes it, when
it runs with `CAMERAREADY=1` (`sbatch --export=ALL,CAMERAREADY=1`); it removes it otherwise, so a review build can
never inherit the flag (the file is git-ignored). Three robust macros are the only places the name, the authors'
addresses and the self-citations may appear in the tex (comments excepted): `\netname` prints `SchwingNet` /
`[AuthorLastName]-Net`; `\withheldurl{url}` prints `\url{url}` / `[URL withheld for review]`; `\selfcite{key}` prints
`\citep{key}` / `[reference withheld for review]`, and in review mode it cites nothing, so the entry leaves the
reference list and the numbering stays consecutive (32 references in review, 34 camera-ready; verified in both PDFs).
`TITLE.md`'s rules are rewritten around this (ANONYMISED-VARIANT = yes, programmatic).

| item | file | change | check |
|---|---|---|---|
| the switch and the macros | `rsnastyle.tex` (after hyperref, before `rsnaresults`) | `\ifcameraready`, the flag input, `\netname`, `\withheldurl`, `\selfcite` (all `\DeclareRobustCommand`, so they survive `\title`, `\caption` and the .lof, `\textbf`) | both grid builds rc 0 |
| the flag | `slurm/compile.sh` | `MODE` from `CAMERAREADY`; writes / removes `cameraready.flag.tex`; prints `MODE`, `RESULT_PENDING`; copies the PDFs to `build/<mode>/` so the two builds do not overwrite each other; removes the flag at the end | `.out` files 40445763 / 40445764 |
| review figure fallback | `rsnaresults.sty`, `tools/results_macros.py` | `numbers.tex` gains `\rsn@figrev@<key>` = `figures/review/<basename>`; `\RESULTFIG` draws it in review mode when it exists, else the manifest's file; the .sty defines `\ifcameraready` itself if loaded alone (`\csname` guard, no `\if` token in the skipped branch) | `generated/numbers.tex`; `check_limits.py` lists the fallback per figure |
| every name in the text | `main.tex` (title, summary statement, key points 1 and 2, abstract Purpose / Results / Conclusion, Figure 3 legend), `sections/introduction.tex`, `results.tex`, `discussion_motivation.tex`, `discussion_limits.tex`, `supplement.tex` (title line) | `SchwingNet` -> `\netname{}`; 12 uses in the bodies; comments untouched | `grep SchwingNet` over the tex bodies: none outside comments; review PDF 0 / 13 placeholders, camera-ready PDF 13 / 0 |
| the self-citations | `sections/methods.tex` (three sites) | `\citep{ctsp1kdescriptor}` x2 and `\citep{ctsp1k}` -> `\selfcite`. Greg's brief named `ctsp1kdescriptor` as the only self-citation; `refs.bib` and `front_matter.json allowed_self_citations` also carry `ctsp1k` (the Zenodo record, same 14 authors, cited in "Sources"), and its entry would print the surname in the review reference list, so both are withheld | review PDF: reference list 1-32, "Schwing" 0; the three markers present (one hyphenated `with-held` across a line) |
| summary statement | `main.tex` | the placeholder is ten characters longer than the name, which took the statement to 256 of 255 in the review copy; "from a C-arm it had never seen" -> "of an unseen C-arm" (the Conclusion's own words): 234 camera-ready / 244 review | `check_limits.py` prints both |
| URLs | -- | `\withheldurl` defined, 0 uses: the manuscript body carries no URL (Data and Code availability name a private repository without an address; Table 1's download-source column names archives, not addresses; third-party DOIs live only in `refs.bib`). Any address that enters the text must go through the macro | `check_limits.py`: "bare URLs left: none" |
| figures | `tools/figure3_network.py` (`NETNAME`, default `SchwingNet`, for the caption file and the record title) | text extraction (pypdf and PyMuPDF) of all twelve figure PDFs in `figures/` found the name in NONE of them (the only "Net" tokens are ResNet-18 and ImageNet); `figure3.png` read by eye shows no title. The name lives only in `figure3.caption.txt` (which `main.tex` prints through `\netname`) and the `record.json` files. So **no review rendering was made and `figures/review/` does not exist**: the review copy draws the camera-ready files, which the check confirms carry no name. The other nine scripts write the name into no output (grep of their string literals: docstrings and repository paths only), so no `NETNAME` hook was added to them; adding the same one-liner is trivial if Greg wants the contract everywhere | `check_limits.py` figure lines |
| Ethics, VinDr | `main.tex` l.131 + comment | "covered by a separate determination of the same office (`\PENDING{G0}{VinDr determination number and date}`)"; the "or its removal from the fold banks" wording is gone. Same sentence with a `[[PENDING G0]]` marker in `packet_src/statements.md` ETHICS_FULL and ETHICS_MANUSCRIPT; `front_matter.json author_decisions.vindr_irb` records the status | the one open placeholder in both copies |
| funding | `packet_src/front_matter.json` `funding` (confirmed), `acknowledgments`, `credit_roles.source` | Greg's sentence verbatim ("G.J.S. was supported by the National Institutes of Health (National Institute of General Medical Sciences, F30GM147909) during the first months of this work; the work received no other funding."); the computing-grid sentence moved to the acknowledgments; whether "Funding acquisition" returns to the CRediT roles is flagged for Greg. `main.tex` keeps "Stated on the full title page" | full title page rebuilt (`packet_src/build/`) |
| Results, two wording fixes | `sections/results.tex` | "The Elekta XVI arms did not train." -> "The Elekta XVI arms scored zero." (`arms.json` marks them trained); "a detector with no frame of the device found 7.0 %" -> "the same-device series' zero-frame detector (styled renders on its geometry plus other C-arms' frames) found 7.0 %" (`results/indomain/det_fill.json` cell `lc_surgio_b51_dr_N0_s0`: styled render, own geometry + other C-arm, N = 0, body boxes, conf 0.74, HELD OUT; the manifest note for `det_carm_body_recall_074_*` says the same) | body 2,980 camera-ready / 2,992 review (the three withheld markers are twelve words) |
| check | `tools/check_limits.py` | measures the copy `CAMERAREADY` selects and prints the other's counts; `\netname` counts as one word; citations counted in the document body (the preamble's `\selfcite` definition holds `\citep{#1}`); a review-copy section that always runs: the review tex bodies, the fetched PDFs (`packet_build/review/`, `cameraready/`) and the figure file each `\RESULTFIG` draws are grepped for `SchwingNet`, `Wayne State` / `Detroit Medical Center`, the surname and the authors' repository URLs / identifiers (GitHub, Hugging Face, Zenodo 22797014 / 22139642, arXiv 2609.22760); a self-citation cited with `\cite` fails; the review main.pdf must show the placeholder, the camera-ready one the name | both modes: `RESULT: FAIL` on the G0 VinDr token alone |
| packet | `tools/make_packet.py` | review packet by default (`packet/`), camera-ready with `CAMERAREADY=1` (`packet_cameraready/`, git-ignored: a derived duplicate); `tex2md` resolves the three macros per copy; the anonymization list allows no form of the name (`SchwingNet`, `Schwing`, `Wayne State`, `Detroit Medical Center`, `General Surgery`, account names, the withheld URLs and identifiers); the old "allowed self-reference" lines and the "author's choice" comment are gone; the review manuscript must show the placeholder, the camera-ready must not; intermediates in `packet_build/<mode>/` beside the fetched PDFs | see the packet paragraph below |
| front documents | `packet_src/build_packet_src.py`, `cover_letter.md`, `front_matter.json anonymisation` | `title()` resolves `\netname` as `SchwingNet` (the title page and the letter are never anonymized); the anonymization check greps the review copy as it prints; the letter's double-anonymized paragraph now says the placeholder and the withheld references are restored at acceptance; the overlap paragraph says the citation is withheld for review | `build_packet_src.py`: 0 hard problems, anonymization hits 0 |
| the letter's five persons-available numbers | `packet_src/numbers.json`, new `packet_src/persons_available_2026-09-24.json` | pre-existing breakage found by this pass: Figure 5's 10:26 rebuild dropped `panel_c_available` from `results/power/power.json` (the persons-available panels are paper 2's), so `build_packet_src.py` could no longer read 3 / 38 / 45 / 91 / 7 and reported five hard problems. The block was copied verbatim from git 8d6a4f4 (generated 2026-09-24 10:33) into `packet_src/` with its origin and each count's live source (`fig6/frozen/v1/strata.json`, `transitional_registry/cobra/rows.csv`, `fig6/sets_v2/T2_persons.json`); nothing under `results/` touched; `NUMBERS.md` line 435 still names `figure5.record.json`, which no longer carries these counts either (not edited here) | the five values re-read and equal to the printed forms |

**Grid builds (one submission, two chained jobs; two of the three compiles allowed).** Commit 299f025 pulled on the
grid; `40445763` (review, 11:11:35-11:12:38, sfx2): `MODE review (flag file absent)`, `numbers.tex: 54 resolved, 0
pending`, `RESULT_PENDING 0`, latexmk rc 0 main and supplement, **`PDF_PAGES 23`, `SUPP_PDF_PAGES 12`**, 0 LaTeX
warnings in both, no `^!`. `40445764` (`--dependency=afterany:40445763 --export=ALL,CAMERAREADY=1`, 28 s): `MODE
cameraready (flag file present)`, the same counts, **23 + 12 pages**, rc 0, 0 warnings, flag file removed afterwards.
The PDFs were fetched by scp into `packet_build/review/` and `packet_build/cameraready/` (7.41 / 5.12 MB each).

**PDF text (pypdf, local).** Review main.pdf: `[AuthorLastName]-Net` x13, `SchwingNet` 0, `Schwing` 0, `Wayne State`
0, `Detroit` 0, Zenodo / arXiv identifiers 0, `[reference withheld for review]` x3, reference list 1-32 consecutive,
`[PENDING G0: VinDr determination number and date]` x1; the title line reads "[AuthorLastName]-Net: a
convolutional-recurrent network for level naming in spine surgery"; review supplement.pdf: placeholder x1, no
identity. Camera-ready main.pdf: `SchwingNet` x13, placeholder 0, reference list 1-34 consecutive (the two
self-citations print with their DOI and arXiv id), title "SchwingNet: ..."; camera-ready supplement.pdf:
`SchwingNet` x1.

**Checks (local).** `python tools/results_macros.py --check`: 54 resolved, 0 pending, no unused key, no bare numeral,
**CHECK PASS**. `python tools/check_limits.py` (review): body **2,992** of 3,000 (319 / 1,120 / 947 / 606); abstract
249; summary statement 244 (camera-ready 234); key points 3; figures 5, four panels, legends 59/60/60/60/59; tables
3; references 32 (camera-ready 34), 34 of 34 with a DOI; abbreviations 7; style greps 0; review tex bodies 0 identity
hits; the four fetched PDFs as above; every figure drawn from its camera-ready file, none carrying the name;
**`RESULT: FAIL` on the G0 VinDr token alone**. `CAMERAREADY=1 python tools/check_limits.py`: body 2,980, references
34, the same single FAIL.

**Packets.** `python tools/make_packet.py` (review, `packet/`): `packet copy: REVIEW (the network prints as
'[AuthorLastName]-Net')`; manuscript.docx 100 paragraphs, 3 tables, 1 `[PENDING]` marker (G0 VinDr), title paragraph "[AuthorLastName]-Net: a convolutional-recurrent network for level naming in spine surgery", placeholder x12, `[reference withheld for review]` x3, `SchwingNet` 0, `Schwing` 0, 32 references listed; anonymization hits **0** in the manuscript, the anonymized
title page and the supplement; figures.docx Figures 1-5 with their 1,200-dpi TIFs again (the packet builder now
resolves `\RESULTFIG{key}` through `numbers_manifest.json`: the first run of this pass found `figures.docx` full of
PENDING pages and `packet/figures/*.tif` gone, because `figure_captions()` only knew `\includegraphics`, a regression
of this morning's results-driven figure wiring); ATLAS cards refreshed and validated (0 errors); **PACKET OK (0 problems)**.
`CAMERAREADY=1 python tools/make_packet.py` (`packet_cameraready/`, git-ignored): the name printed (12 in the
manuscript body), the two self-citations in the list, the surname and the identifiers reported and not counted;
manuscript.docx 102 paragraphs, 3 tables, 1 `[PENDING]` marker, 34 references; PACKET OK (0 problems). Logs: `packet_build/make_packet_review_2026-09-25.log`, `make_packet_cameraready_2026-09-25.log`.

**Two pre-existing breakages repaired on the way, both from the 10:26 Figure 5 rebuild.** (1) `packet_src/numbers.json`
and `atlas/update_cards.py` read `panel_c_available` (3 / 38 / 45 / 91 / 7) and the 97.6 % crossing from
`results/power/power.json`, which no longer carries them: the block is preserved verbatim in
`packet_src/persons_available_2026-09-24.json` (origin git 8d6a4f4, per-count sources) and both read it; the 97.6 %
comparator crossing and the exact-test n (paper 2's, never printed on the card) are no longer read. (2) The packet's
figure resolution, above.

**Open for Greg.** (1) The VinDr determination number and date: the one `\PENDING{G0}` token in both copies, the one
`[[PENDING G0]]` marker on the title page's Ethics, and `author_decisions.vindr_irb`. (2) `ctsp1k` is withheld beside
`ctsp1kdescriptor` (the brief named the descriptor alone); if the data record should stay cited in the review copy,
change one `\selfcite` back to `\citep` in `sections/methods.tex` l.43 and accept that the review reference list then
prints the author list. (3) Whether "Funding acquisition" returns to the CRediT roles now that the F30 is declared.
(4) `NUMBERS.md` line 435 still names `figures/figure5.record.json` for the 91 / 7 counts; the record no longer
carries them (the preserved block does). (5) The nine figure scripts other than `figure3_network.py` have no `NETNAME`
hook because they write the name nowhere; say so if the constant is wanted in all ten regardless. (6) The review
copy's body is 2,992 words: the three "[reference withheld for review]" markers cost twelve; eight words of slack.

## 10. Acquisition-space pass (2026-09-25 afternoon): Figure 5 rebuilt around what accuracy follows

**Trigger.** Greg, reviewing the manuscript: "I don't see the relationship between N and learning accuracy for plain film vs
fluoro in the paper, where is it?" and then "I definitely want to demonstrate how much they vary in the extra dimensions of
the fluoro and how it makes it harder to train ... visualize the learning curve for plain film and the pooled fluoro vs the
dimension separated and grouped fluoro to see if it corrects." The 10:26 Figure 5 drew the plain-film N curve (b) and the
matched-N arm dot plot (c) and the pooled-fit scatter (d); the C-arm's own N curves (naming per protocol,
results/indomain/name_fill.json; detection vs frames, results/indomain/det_fill.json) were fitted in
results/indomain/FIT_N.md but drawn nowhere after the 2026-09-24 coverage rebuild dropped the in-domain panels.

**What was found (tools/fig_dimension_explore.py, results/coverage/dimension/, commit fcd3461; nothing retrained).**
Separated by view, each C-arm naming curve rises like film (lateral 93.7 -> 98.1 % by 50 persons; anteroposterior 33.8 ->
90.8 % with five, 98.1 % with all); the view not trained on stays where it was (lateral-trained on anteroposterior 32 -> 55 %);
training both views costs neither (98.1 / 97.0 %). Same-device detection plateaus from 24 frames on both views (84.1 / 84.6 %)
and the one-view arms of 25 and 50 frames sit in the same band on their own view (83.0-86.4 %) and find 0.0-39.5 % of the
other: separating the view does not lift the plateau. On renders of 40 unseen subjects, the matched-N arms read along the
lateral angle (experiment/runs/cov_surgio_b51_dr_*/unseen/recall_vs_angle.json): trained at anteroposterior and lateral poses
only, 82.1 % at those angles and 52.8 % over the 16 other bins; doubling those frames 94.2 / 64.8 %; the same N spread over
the arc 80.7 / 77.1 %. The claim the paper now makes: accuracy follows where the frames sit in acquisition space, not how many
there are; frames of one cell do not transfer to another. Not claimed: that fluoroscopy is higher-dimensional than film (the
bank records no projection angle, distance or magnification for any film corpus; film has its own non-transferring dimension,
corpus: NHANES II -> CSXA 74 % at best).

**Figure 5 (tools/fig_power.py, local build; figures/figure5.record.json).** (a) unchanged. (b) film N curve (seed mean, seed-range
bars; the cross-corpus dashed lines dropped, the transfer peak stays in the text) plus the C-arm per view (lateral ink circles,
anteroposterior grey squares, solid = own view; lateral-trained read on anteroposterior dashed open; both views at all persons
as x). (c) same-device detection vs real frames: both-view arm per test view with case-clustered intervals; one-view arms as
triangles (filled = own view, open = other), two seeds pooled (det_fill.json#protocol). (d) recall vs lateral angle for the
low / high / low-2N Surgio arms at confidence 0.25, seed mean with the per-seed range shaded, dotted verticals at the three
trained angles. The pooled fit is no longer drawn; its numbers stay in Results and in results/power/power.json#pooled_fit.
Caption 57 words; text audit Arial >= 12 pt PASS; 7.0 x 9.4 in; TIF 1,200 dpi. Panel-by-panel readings are in the record's
"components" (Greg: "make it clear in the paper what each panel means and how it can be interpreted"); the interpretation is
in the text, the caption stays terse (standing rule).

**Text.** Results: the closing same-device sentences of "Naming, counting and coupling" moved into the renamed paragraph
"Persons, views and angles", which now walks b, c, d in order (film; C-arm per view, cross-view, both views; detection
plateau, one-view arms; angle: trained bins vs the 16 others for the three arms) and keeps the pooled fit's numbers (the
likelihood-ratio statistic dropped; the confidence caveat kept). Methods: the one-view arms, the C-ArmLSpine per-view naming
curve and the per-angle reading named. Discussion paragraph 4 rewritten to the claim ("Accuracy followed where the frames sat
in acquisition space, not how many there were"), plateau "by 24 frames", the "held-out-angle effect" sentence replaced by the
one-view and per-angle evidence; no figure cited. Supplement "Same-device frames and view angle": the one-view arm numbers with
intervals (RESULT keys) and the sentence separating count from coverage now names the one-view arms (view) and the render
arms (angle). Caption in main.tex = figure5.caption.txt. Body 2,995 (review) / 2,983 (camera-ready) after two trim passes
(film asymptote sentence dropped, "mean 88 per fold" dropped, Discussion tightened).

**Manifest.** +26 keys: name_carm_* (name_fill.json#figure5b rows 1, 5, 13, 73, 74, 78, 84, 85), det_both_n24/n200_lat/ap
(det_fill.json#curves/carm), det_oneview_own/other_min/max (power.json#panel_c_detection/summary), det_oneview_{ap,lat}{25,50}_
own_pct/_ci/other_pct (det_fill.json#protocol), angle_n_subjects, angle_n_untrained_bins, angle_{low,low2n,high}_{trained,
untrained}_pct (power.json#panel_d_angle/summary). -16 keys: the matched-count contrast, real-spot-frame, unseen-box-count,
film asymptote, likelihood-ratio and fold-mean-persons keys. results_macros --check: 77 resolved, 0 pending, PASS.
check_limits: body 2,995 / 2,983; the one FAIL is still the G0 VinDr token.

**Builds.** 40447659 / 40447660 ran concurrently in one directory (review latexmk rc 12, a race) and were discarded;
40447734 -> 40447735 (afterany) gave 23 + 12 pp each; after the Figure S1 margin fix (96b2ced: fig2_flow.py axes limits
-0.15 .. +0.15 so the outer box strokes are no longer clipped; Greg: "this figure is cropped around the edges")
40448569 (review) / 40448570 (camera-ready): 23 + 12 pp, rc 0, 0 LaTeX warnings. check_limits on the fetched PDFs:
review identity hits none, camera-ready 'SchwingNet' x13; the one FAIL is the G0 VinDr token. make_packet review and
camera-ready: PACKET OK, anonymization hits 0, one [PENDING] marker each (logs packet_build/make_packet_*_2026-09-25c.log).
Merged PDFs packet_build/SchwingNet_{review,cameraready}_main_and_supplement_2026-09-25c.pdf (35 pp) sent to Greg; the
camera-ready copy replaced item 02 of the TTO package (CTSpinoPelvic1K-1/TTO_package_2026-09-25, followup rev3).

**Follow-on (Greg): the per-vertebra miss diagnostic.** "What is different about C-arm frames such that they flatten around
80 % and plain films continue to improve? Is it my pseudolabels being poor quality? Or the extra degrees of freedom?"
tools/carm_miss_diagnostic.py + slurm/carm_miss_diagnostic.sh (job 40448586): re-matches the 47 lcurve dumps with
lcurve_score.load unchanged, joins each truth vertebra to its meta (visible_frac, complete, box_source, level agreement,
edge distance, body/outline ratio, frame edge NCC), classes never / sometimes / always hit over the N >= 24 both-view arms
at body 0.74, strata tables, and renders of every never-hit vertebra. Results in results/indomain/miss_diagnostic/ when
fetched; the reading belongs in the next section.

**Still stale, noted.** tools/stats_review2_recompute.py reads power.json#panel_b/drawn/p0_82.2_H1 (the 2026-09-24 layout);
it has been stale since the 10:26 rebuild and is untouched here. main.tex line 38's comment ("no in-domain panels") is now
wrong in the other direction and was left as history.

## 11. The per-vertebra miss diagnostic: the same-device plateau is the denominator (2026-09-25 14:45)

Job 40448862 (tools/carm_miss_diagnostic.py; four submissions, three trivial fixes: the scorer's four-tuple, the renamed
case118 oblique meta, a shadowed variable). Outputs results/indomain/miss_diagnostic/{miss_diagnostic.json,
MISS_DIAGNOSTIC.md, never_hit_body074_sheet1.png, sheet2.png, always_hit_sample.png}. 45 dumps re-matched with
lcurve_score.load unchanged; the self-check reproduced all 135 det_fill.json cell x view recalls to 0.1 pp.

**Finding.** Over the ten plateau arms (both views, N = 24 .. 200, body rule at 0.74) the misses are systematic, not
random: 30 of 287 test vertebrae are missed by every arm and 208 are hit by every arm (pairwise Jaccard of the miss sets
0.70; independent misses would leave none missed by all). The misses sit on the truth, not on the images: vertebrae cut
by the CBCT boundary are missed 51.5 % of the time against 6.7 % for complete ones and carry 340 of the 489 misses;
bodies within 40 px of the panel edge 42 % against 5.5 %; boxes whose two labellers disagreed 55.5 % against 12.7 %; the
six whole-vertebra fallback boxes 100 %. The frame's registration score has no gradient on AP and a weak one on lateral.
On complete, agreed, SPINEPS-boxed bodies (204 of 287) the plateau arms read 96.9 % (AP 98.7 %, lateral 95.8 %; centre
rule at 0.25: 99.8 %). The renders (looked at, written up in MISS_DIAGNOSTIC.md section 5) show the 30 never-hit as top-edge
L1/T12 slivers 15-35 px high (18), garbage boxes from the fallback and from disagreed levels that span the lumbosacral
region or sit on soft tissue (10 overlapping), and four lateral frames whose 2-D/3-D registration puts the truth half a
body off the bone (edge NCC 0.12-0.18). Exactly one never-hit vertebra is complete, agreed and away from the edge.

**Answer to Greg's question** ("is it my pseudolabels being poor quality, or the extra degrees of freedom?"): on the same
device it is the denominator and the labels. Frames of a view or an angle never trained on are where the degrees of
freedom cost (Figure 5 b-d); within a trained cell the ceiling is truth quality.

**Consequences for the text, NOT yet applied (Greg to decide; body at 2,995 words, supplement at 12 pp).** (1) The
supplement's "the reported detector's flat recall there is unexplained" and the Results' plateau sentence can now say
what the plateau is: on complete, agreed bodies away from the panel edge the arms read 96.9 %; the misses are
CBCT-cut slivers at the top of the field, boxes from disagreeing labellers and four poorly registered laterals. (2) The
reported 97 % detection target, pre-stated as counting grade, is met on the clean denominator and not on the released
one; the honest form is to report both denominators, not to drop the cut vertebrae. (3) A truth repair is possible
without any human: exclude structures with < 80 % of their projected points in the frame and every fallback box from
the detection denominator (they were never bodies), keep them for naming as context; re-score, do not retrain.

**Applied (Greg 2026-09-25 "Please do all of this").** (1) Results, "Naming, counting and coupling": the held-out detector's
231 of 287 now stands beside 201 of 214 (93.9 %; 90.4, 97.1) on the repaired denominator; "Persons, views and angles": the
plateau sentence carries 95.6 % on the repaired denominator and drops the at-200 numbers (Figure 5c shows them); the
pooled-fit sentence shortened to AICc and the two P values. (2) Discussion paragraph 4: "same-device frames restored it by
24 frames to a plateau set by truth boxes cut at the edge of the field, not by the detector"; the pooled-fit clause gone.
(3) Supplement, "Same-device frames and view angle": the one-view arms as ranges, then the repair rule (complete, not
fallback, >= 80 % of points in frame, body <= outline), the dropped counts (73: 66 CBCT-cut, 6 fallback, 7 mostly outside,
11 body larger than outline; overlapping), the held-out detector 93.9 % on 214 with the re-scored released 236/287 stated
against the 231/287 of the main text (a1.json, scored 2026-09-22 before the truth rebuild), the both-view arms 95.6 % at
24 and 94.9 % at 200 frames. The sentence "the reported detector's flat recall there is unexplained" was NOT touched: it
is about recall against angle on the one real rotational acquisition (Figure S5), a different flatness, and the
diagnostic says nothing about it. (4) The repair itself: tools/carm_denominator_repair.py + slurm (job 40448892;
results/indomain/{denominator_repair.json, DENOMINATOR_REPAIR.md}); re-scored with lcurve_score.load unchanged; the
released re-score reproduces all 135 det_fill.json cell x view recalls; nothing retrained; no box deleted (kept=False
with reasons in a repaired meta copy on CephFS). Manifest: +11 keys (denom_*, det_heldout_repaired_*,
det_heldout_rescored_released_kn, det_both_n24/n200_repaired_all_*), -18 (the one-view detail keys, the pooled-fit
g/CI/conf keys, det_both_n200_lat/ap); 66 numbers, --check PASS. Body 2,999 (review) / 2,987 (camera-ready).

**Supplement page cap.** The first build of this pass (40448935/36) gave 13 supplement pages: the text ran 35 lines onto a
fifth page and Table S1 (a full-page minipage) and every table and figure after it moved down one page. Trimmed
(corpus-census reconciliation, quality-control entries, the older same-device numbers as a range, the development-curve
epoch sentence; no number changed in the main text) and rebuilt: 40448970 (review) -> 40448971 (camera-ready).

## 12. Supplementary findings in the body; Figure S4 cells named (2026-09-25 15:40)

**Greg:** "make it clear that specific combination or whatever was held out; also did you extract the results of all the
supplementary data and reference the extracted knowledge somewhere in the prose of the main body with a citation of the
supplementary figure plotting the info?"

**Audit of the body before this pass.** Figure S1 (flow): cited in Data and Methods as a pointer (a diagram; nothing to
extract). Figures S2-S3 + Table S1 (manifold, image formation): Methods states the finding ("missed their pre-stated
criterion") and the Discussion "styled renders stayed separable from real frames (supplement)". Table S2: Results ("short of
the pre-stated 97 %"). Table S3: Results (median age and share female by release). Supplement sections cited as
"(supplement)": embedding per render source, fused-L5 persons, one-view arms, nested fit, development learning curve.
**Missing:** Figure S4 (which source carries the detector) was cited in Methods only as a pointer to where detection is
scored; Figure S5 (recall against angle on the real spin) was cited in Methods only for the real pool's two views. Neither
finding was in the body.

**Added (Results).** After the held-out detector's numbers: "The radiotherapy imager's arc frames carried that detection:
alone they found 86.8 % of C-ArmLSpine vertebrae, the cadaver C-arm's frames 12.9 %, and adding them raised recall +71.8
points (63.4, 79.6) (Figure S4)" (keys a3_* into results/contribution_matrix.json: single_source_cells 1 and 5,
marginal_contributions 28). After the angle sentence: "On one patient's rotational acquisition the pooled detector found
93.6 % of bodies across the arc, the held-out detector 49.5 % (Figure S5)" (keys s5_* into figures/figS4.record.json
numbers[1]; the held-out detector's exact half at 15 of 19 bins is the record's unexplained pattern, stated as a number).

**Paid for by:** the 25-person film values (Figure 5b draws them; three keys retired), "at all persons", the Discussion's
development-curve numbers (now a pointer to the supplement) and the zheng2018pda numbers (citation kept), "doubling those
poses filled no gap", "(36 rendered; ...)", the Methods nested-fit clause. Body 3,000 (review) / 2,988 (camera-ready);
results_macros 74 resolved PASS.

**Figure S4 (tools/figS_supplement.py s3, rebuilt; audit PASS, caption 59 words).** Legend: "trained on this device: not held
out" for the hatched cells (before: "target in training") and "blank: not run" (before: "not scored"); the caption names
both. The hatching rule is unchanged: a cell is hatched when the results file marks it other than DEVICE-HELD-OUT, i.e. the
arm's training set held real frames of the column's device; every drawn value was matched to the held-out inventory
(record held_out_crosscheck). No job is running or pending for this figure; the blank cells are arms that have no run on
that target (the six-specimen column exists only for the arms retrained six times without DeepFluoro).

**Builds.** 40449056 (review) -> 40449057 (camera-ready).

## 13. Film N-curve ablation: do CT renders help radiograph training? (submitted 2026-09-25 16:20)

**Greg:** "if renders are my only source of rare classes they have to be included right? run this test". Yes to the first
(no released film or C-arm frame carries a human-read L6 or T13; renders are their only labelled source, and stay in
training whatever this test says). The test asks the separate question whether renders also raise ORDINARY-level naming
on plain films.

**Design** (tools/film_ncurve.py, slurm/film_ncurve_ablation.sh; the reported curve's 48 cells, persons, seeds, epochs (15),
learning rate (1e-4), augmentation, head recipe and a5-rows scoring on the same test context, unchanged):
- arm `renderonly` = the reported curve (Figure 5b): render-only encoder as init; merged bank = render base (600 per class,
  15,374 rows) + the N persons' film crops oversampled to half the rows (NHANES N = 5: 48 crops -> 15,767 rows).
- arm `imagenet`: ImageNet init (--require-pretrained), the SAME merged bank. Isolates the render pretraining.
- arm `filmonly`: ImageNet init, the merged bank with every render row removed (the film rows keep their oversampled count,
  the selection crops stay as val). Isolates renders altogether. N = 0 skipped (nothing to train on).
Reading rule, stated before the numbers: at N = 5 and 25 per corpus, if renderonly exceeds filmonly outside the
patient-clustered intervals, renders help film naming; if filmonly matches or exceeds it, they do not; imagenet says
which part (pretraining or bank) carries any difference. Jobs: arrays 40451157 (imagenet) and 40451158 (filmonly),
48 tasks each at 12 concurrent, GPU partitions; collects 40451159 / 40451160 (afterany). The reported cells averaged
18 min each (51,804 s for 48), so each arm is about 15 GPU-hours and one to three hours of wall time depending on the
queue. Outputs: $FN/ablation/<arm>/{cells,film_ncurve.json,FILM_NCURVE.md}.

**Result (read 2026-09-26 01:20, tools/film_ncurve_ablation_read.py -> results/coverage/film_ncurve/ablation/READ.md; arms
40451157 imagenet 48/48 scored, 40451158 filmonly 39/48 = every cell but N = 0).** Renders HELP ordinary-level naming on
plain films when film is scarce, and stop mattering once it is not. At N = 5 persons per corpus, render-only minus film-only
is +21.9 (NHANES), +11.1 (BUU) and +18.7 (CSXA) points, every seed separated outside the patient-clustered intervals; at
N = 25 it is +12.2, +6.0 and +6.2, still separated on every seed. From 100 persons the arms overlap, and with every person
the three arms are level (NHANES 92.7 / 92.3 / 92.0; CSXA 99.8 / 99.8 / 99.9; BUU 96.9 / 97.2 / 98.5, where film-only is
1.6 points higher on intervals a point wide). The ImageNet-init arm on the same merged bank sits between the two at small N
(NHANES N = 5: 75.5 against 77.8 render-only and 55.9 film-only), so both the render pretraining and the render rows in the
bank carry the gain. Reading by the rule: 7 of the 9 pre-stated cells separated, all in the direction 'renders help';
the two 'all' cells are level or a point the other way. Renders stay in training regardless (the only labelled L6 / T13).
Proposed Discussion sentence (not yet in the tex; body at the limit): 'Rendered CT is what makes a few films enough: with
five to twenty-five annotated persons per radiograph corpus the render-pretrained encoder named ordinary levels 6 to 22
points above one trained on those films alone, and the two met only once every person was used (Supplementary Table S?).'

