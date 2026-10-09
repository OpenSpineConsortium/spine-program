# DRIVE_CHECK: adversarial check of the draft and the packet

2026-09-24, against `main.tex` 07:17, `main.pdf` and `supplement.pdf` compiled on the grid at 07:22 (job 40435724), and
the packet built at 07:47. Nothing in the manuscript, packet or results was edited, and nothing was committed.

**Verdict: FAIL.** The G5/G6 placeholders are expected. The failures are defects that exist independently of those gates:
- open G0 and G4 placeholders;
- two wrong statements, one in the Results and one in the Discussion;
- non-held-out numbers quoted in the abstract without a qualifier;
- a Figure 5 that is not the planned data-case figure;
- none of the REFS_AUDIT fixes applied, and a dead DOI in print;
- identity leaks in the anonymized docx metadata;
- three statements in the cover letter or Ethics section that the manuscript contradicts.

| # | Item | Verdict |
|---|---|---|
| 1 | Grid compile, whole log read | PASS (with a warning) |
| 2 | `check_limits.py` output | FAIL (placeholders only; every limit passes) |
| 3 | Six figures × four components | FAIL (Figures 2 and 5; 6 pending) |
| 4 | Numbers in the abstract, Key Points and Results traced to files | FAIL (3 defects; the rest trace) |
| 5 | Every `\PENDING` is G5 or G6 | FAIL (G0 ×3, G4 ×1) |
| 6 | No priority wording | PASS |
| 7 | Abbreviations ≤10 and defined | PASS (with a warning) |
| 8 | References ≤35; every DOI and PMID in REFS_AUDIT resolved | FAIL |
| 9 | `LEVELCHECK_MODEL.md` unchanged since ecae75f | PASS |
| 10 | Packet files open and match the PDF | FAIL (anonymization leaks, cover-letter contradictions) |
| 11 | Fixed title, network name, affiliation | FAIL (network name); title dash warning; affiliation PASS |
| 12 | Banned word | PASS |

---

## 1. Grid compile — PASS, with a warning

- **Sources match the grid build.** md5 over `main.tex`, `supplement.tex`, `rsnastyle.tex`, `refs.bib`, the 5 section
  files, the 6 table files, the 10 figure PDFs and both output PDFs: the local copies (CR stripped) equal the grid copies.
  `main.pdf` therefore reflects the current sources, and no recompile was needed.
- **Job 40435724.**
  - latexmk: rc 0 for both documents.
  - `PDF_PAGES 26`; `SUPP_PDF_PAGES 10`, within the supplement's 12-page cap.
  - Supplement: 0 LaTeX warnings.
- **Warning.** The final main pass still logs "There were undefined references" and "Please (re)run Biber", but it names
  no individual key. What the PDF shows:
  - 0 occurrences of `??` and no bold key names;
  - citations numbered 1–30 in order of first use;
  - one underfull hbox, in reference 12.
- **Tables.** Pages 17–20 were rendered and inspected. All four landscape tables are intact, with nothing clipped.

## 2. check_limits — FAIL (placeholders only)

Every journal limit passes:

| Limit | Value |
|---|---|
| Body words | 2,985 / 3,000 |
| Abstract words | 248 / 250, four headings in order |
| Summary statement | 231 / 255 characters |
| Key Points | 3, no abbreviations |
| Figures | 6 |
| Caption words | 59, 56, 59, 60, 56, 45 |
| Tables | 4, all titled, no merged cells |
| References | 30 / 35, all with a doi field |
| Abbreviations | 6 |
| Discussion | cites no figure or table; limitations is the second-to-last paragraph |
| Style greps (self-evaluation, institution, self-reference) | 0 hits |
| Banned word or retired rule | 0 hits |

`RESULT: FAIL` comes from 29 open numeric placeholders and one missing figure (`figures/figure6.pdf`). See item 5.

## 3. Six figures × four components — FAIL

Each figure was rendered and inspected against its caption and `figureN.record.json`.

- **Figure 1** (L6 | T13 | sacralised L5 | four-lumbar): **PASS**.
- **Figure 2** (spec: t-SNE with transitional marked | close-ups | where the name is read | published gradients): **FAIL, partial.**
  - (a) t-SNE with transitional crops marked, (b) lumbosacral close-up and (d) occlusion ("where the name is read") are present.
  - (c) is a silhouette ladder. No panel shows published gradients.
- **Figure 3** (detector | level model | count | coupling): **PASS**.
- **Figure 4** (detection | three-body field | count | real L6 frame): **PASS**.
- **Figure 5** (spec: detection vs same-device frames | naming vs same-device cases, lateral and AP | power | people available vs needed): **FAIL.**
  - The built figure is (a) the Wilson bound against n, (b) exact-test power, (c) persons available against needed, and (d) best-case intervals.
  - The data-case panels a and b are absent. No `\PENDING{G5}` marks them in the caption or the text.
  - The in-domain inventory (`results/indomain/INVENTORY.md`) is not drawn and not quoted.
- **Figure 6**: **PENDING G6**, as expected. `\PENDINGFIG` is wired, but the placeholder caption names no (a)–(d) components.

## 4. Numbers traced to files — FAIL (three defects; every other number traces)

Each file below was opened and each number recomputed from it.

**Traced correctly:**
- **Zero-shot naming.** `results/a7.json` `zeroshot2/det/{LAT,AP}/kfull`:
  - lateral 594/617, Wilson on n_eff [92.0, 98.3], 6 of 141 cases with an error;
  - 594/676 = 87.9 %;
  - AP 239/631.
- **Fine-tuned naming.** `results/a4.json`:
  - `det/LAT/kfull` 606/617 [94.6, 99.4];
  - `det/LAT/k3` 1,079/1,162 [89.6, 95.6];
  - `det/LAT/k1` 440/604.
- **Day-grouped.** `results/a9.json` cvday: 0.92545 × 617 = 571 [87.7, 96.4].
- **Paired difference.** `results/a3.json` `zeroshot_lateral_vs_ap`: 57.7 [48.9, 66.4], 593 vertebrae in 140 cases, Holm exact 1.0e-22.
- **Coupling.** `results/coupling.json` `det74/kfull`:
  - count 979/1,009 [94.2, 99.2]; classifier 993; coupled 995; coupled minus count 1.6 [0.0, 3.8];
  - 12/233 disagreement frames; 4/5 and 17/225 flag counts; 921/922 unflagged;
  - 130 cases; 233/290 anchored;
  - L6 calls: 4 anchored frames, all flagged; `l6_patients` det74: 1 of 4 anchored frames.
- **Detection.** `docs/carmlspine_cv5_mixed_2026-09-21.json`: 617 of 676 lateral.
- **Held-out detector.** `results/a1.json` `cross_device_0.74`: 231/287 [74.1, 86.8].
- **Embedding.** `results/figure2/figure2_metrics.json`:
  - 13,009 crops, 1,612 persons; 2,889 crops and 164 persons dropped;
  - nearest-neighbour 74.9 [72.2, 77.6];
  - silhouettes 0.349 [0.310, 0.386] (98 crops, 10 persons) and 0.227 [0.205, 0.249]; lumbar range 0.159–0.227;
  - within-source 0.140 vs 0.208 (5 persons); 75 of 98 crops called correctly;
  - never-seen L6: 0.104, 0.124 and 0.165 against 0.338; L3–L5 from −0.087 to −0.014; 84 of 180; body box −0.067 and 13 of 180.
- **Fused L5.** `figure2_transitional.json`: −0.13, −0.18; 0.238; 6.6 % of 1,066; L3 0.007 and −0.259; 0.161.
- **Occlusion.** `zones_lateral_clean.json`: sacrum 4.51 [3.42, 5.79]; L4 1.29 [1.13, 1.44]; L5 1.26 [1.09, 1.45].
- **Transitional persons.** `results/rare_class/transitional_subtypes.csv`, recounted by distinct `patient_key`:
  - 194 in total: L6 110 (18 / 86 / 3 / 3), T13 7, sacralised 28 (12 four-lumbar), Castellvi I/II 31, lumbar rib 14, unassigned 4.
- **Figure 5 numbers.** `figures/figure5.record.json` and `results/power/power.json`: 35, 157, 19, 152, 55, 71 and 708; 91 and 57 (L6 11, T13 38, four-lumbar 8); 93.7; 57 CT test persons (43 / 3 / 11), 48 of them in the lineage.
- **Wilson bounds** recomputed: 91.8, 43.9, 56.6, 61.0, 75.8, 74.1, 90.8, 67.6 and 93.7.
- **Other sources.** VERIDAH 10 of 24 (`spineps_ids/IMPACT.md` §5); 814/910 (`docs/DATASHEET.md`); study dates (`carmlspine_day_groups.json`); ages 24–89 (`figure1.record.json`).

**Defects:**
- **D1. Results, Study population: "631 anteroposterior in 142" is called agreed truth.**
  - The agreed AP count is 673 vertebrae in 143 cases (`oracle/AP/kfull`).
  - 631 in 142 is the number of detected AP vertebrae (`det/AP/kfull`).
- **D2. Discussion, first paragraph: "Never shown the intraoperative C-arm, it named 96.3 % … and 92.9 % with three bodies in view … coupling … 98.6 %".**
  - 92.9 % is the fine-tuned, case-grouped result (`a4.json` `det/LAT/k3`). The zero-shot figure with three bodies in view is 86.9 % (1,010/1,162, `a7.json` `zeroshot2/det/LAT/k3`).
  - 98.6 % also comes from the CV fold models.
  - Key Point 2 follows Key Point 1's "Never trained on the intraoperative C-arm" without saying "fine-tuned".
- **D3. Abstract Results, first sentence, and Key Point 3 quote non-held-out silhouettes without a qualifier.**
  - The values are 0.35 [0.31, 0.39] and 0.23, with "10 persons" in Key Point 3.
  - `results/eval_gate/quoted_results.json` (NUMBERS:L40) marks them NOT HELD OUT: they are on the v9 checkpoint-selection split.
  - The Methods, Results and Figure 2 caption carry the qualifier; the abstract and Key Point 3 do not.

## 5. Every \PENDING is G5 or G6 — FAIL

- **G0, 3 placeholders:**
  - abstract Materials and Methods: "age and sex";
  - `sections/methods.tex:18`: "first download date";
  - `sections/results.tex:19`: "age and sex by source".
- **G4, 1 placeholder:** `supplement.tex:69`, the corpus census.
- **G5, 15 placeholders:** all in Table S2 (`tables/tab2_detection.tex`). None marks the pending Figure 5 a/b content.
- **G6, 10 placeholders:** the abstract, the Results, Table 3 (H1–H6 and naming unaffected) and Table 4. Figure 6 is missing.

## 6. Priority wording — PASS

- **Grep.** Searched for first, novel, unique, only, to our knowledge, state of the art, outperform, surpass, best, pioneer, no prior/previous/other and breakthrough.
- **Files searched:** main, sections, tables, captions and the supplement (comments stripped), plus the cover letter, both title pages, `supplement.docx` and `figures.docx`.
- **Result.** No priority claim; every hit is a non-priority use.
- **Flag only; the title is fixed by Greg.** Two phrases in the title claim more than the present results show:
  - "robust to transitional anatomy": there is no transitional result yet;
  - "versus registration-assisted neurosurgeons": the comparator is a model, not surgeons. The cover letter says so.

## 7. Abbreviations — PASS, with a warning

- **Count.** 6 list entries, covering 7 terms because "L5, L6" is one entry. The limit is 10.
- **Definitions.** Each listed term is defined at first use in both the abstract and the body.
- **Warning: abbreviations used without definition:**
  - F1 (Methods, "the best pooled F1");
  - JSON (Data availability);
  - L1–L4, S1, T11, T12 and C2, while L5, L6 and T13 are listed.

## 8. References and REFS_AUDIT — FAIL

- **Count.** 30 cited, within the 35 limit: PASS.
- **DOIs.** Resolved via the doi.org handle API from WSL: 29 of 30 are registered.
  - `hsiang2011` `10.4103/2152-7806.79769` returns code 100 (not registered). It is still printed as reference 1 in the PDF and the docx.
- **REFS_AUDIT corrections not applied.** `refs_corrections.bib` was never merged. In print today:
  - COBRA2026 prints "Kamp F et al.", the wrong title, and a note ("867 patients … arXiv 2607.20037").
  - Rao 2024 prints "P YR, S G, R D" and "PMID: 40039607".
  - He 2016 prints its arXiv note.
  - VinDr prints "MICCAI 2021" as if it were a journal.
  - `ctsp1k`, the Zenodo dataset, is cited where the descriptor (arXiv:2609.22760) is meant.
  - `castellvi1984` (marked required) is absent, although Castellvi is named 10 times.
  - 12 journal names are not NLM abbreviations.
  - `levelcheck2012` is missing issue 17.
- **Tex fixes still open in REFS_AUDIT:**
  - Methods: "no other subject overlaps a prior publication" is literally false.
  - Introduction and Discussion: Huang 2022 "tomosynthesis" and "about 17 vertebrae" are not supported by the source abstract.
  - Minor: Furuya counts patients, but the text says "operations"; Mody's surgeons were "responding", but the text says "surveyed".

## 9. LEVELCHECK_MODEL.md frozen since ecae75f — PASS

- **Diff.** `git diff ecae75f HEAD` gives 176 insertions and 0 deletions, in one hunk starting after line 602. The working tree equals HEAD.
- **Frozen part identical.** Lines 1–602 have the same md5 as ecae75f (`012689ba…`), so §1–§11 are unchanged.
- **Appended sections:**
  - §12: 1897772, with a time correction in efab8dd;
  - §13: 2993f40;
  - §14: b511985.
- **Table 3 matches the §11 JSON:** 82.2/19, 97.6/152, 92.6/48, and the anchors.
- **Note.** The held-out split was applied at 20:18:48, 28 minutes after the freeze. What had been seen before the freeze is disclosed only in the Table 3 note, not in the Methods or Registration sentence.

## 10. Packet opens and matches the PDF — FAIL

**Matches:**
- **Files open.** All seven .docx files and all five TIFs open.
- **TIFs.** 1,200 dpi and 8,400 px wide; pixel-identical to `figures/figureN.tif`.
- **figures.docx.** Its images are identical to `figureN.png`, and the captions are verbatim apart from typographic quotes.
- **manuscript.docx body.** A word-level diff against `main.pdf` finds only extraction artefacts and an added Acknowledgments stub. Inline math is carried as 26 OMML objects.
- **Tables 1–4.** Every number equals the tex.
- **supplement.docx.** Its text equals `supplement.pdf`.
- **Checklist.** `claim_checklist.docx` is the CLAIM 2024 form with 44 items.

**Defects:**
- **Identity leaks in the anonymized files.**
  - `manuscript.docx` `docProps/custom.xml` holds the paths `laptop:…\spinesurg-ct-nnunet\SchwingNet\refs.bib` and `…\nlm.csl`.
  - The image alt text (`descr`) in `supplement.docx` and `figures.docx` holds `spinesurg-ct-nnunet:…`. The repository is named on the full title page.
- **References do not match the PDF.**
  - The docx lists 6 authors before "et al." and drops issue numbers; the PDF lists 3 and keeps them.
  - The docx suppresses the notes the PDF prints.
  - The docx prints the citation "[14,9]" unsorted; the PDF has [9,14].
- **Cover letter contradicts the manuscript.**
  - It says "The Methods cite the CTSpinoPelvic1K data descriptor". They cite the dataset (see item 8).
  - It says SchwingNet is used "in the title and throughout". The manuscript says "the network" everywhere except the title, the Figure 6 caption and Table 3 (see item 11).
  - It says "Public releases hold three persons with a real transitional C-arm exposure". The manuscript calls these one labeller's contested read, excluded in advance.
- **Ethics statements conflict.**
  - The main-text Ethics and Data availability sections say every source is public and covered by determination 2026-269.
  - The full title page itself flags VinDr-SpineXR, which is under the PhysioNet restricted DUA, as outside that determination (a `[[CONFIRM]]` marker).
- **Open author items:**
  - 22 `[[CONFIRM]]` markers and 8 open author decisions;
  - CLAIM 2024: 3 items answered No (18, 24, 36) and 17 PENDING markers.

## 11. Fixed title, name, affiliation — FAIL (network name)

- **Affiliation: PASS.** "Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center" appears on the full title page and in the cover letter.
- **Title: warning.** The wording is exact, but the tex, both title pages and the cover letter print "convolutional–recurrent" with an en dash. `TITLE.md` has a hyphen.
- **Network name: FAIL.**
  - `TITLE.md` and `packet_src/front_matter.json` require SchwingNet in the abstract, the Key Points and the figures (ANONYMISED-VARIANT = no).
  - The abstract, Key Points and Figures 1–5 say "the network".

## 12. Banned word — PASS

`check_limits` walks the whole tree and finds 0 hits. A grep of the packet .docx files also finds 0.

---

## Also found

These are outside the items above; each is a warning.

- **Supplement, in-sample count.** The supplement says the film-trained detector was "in-sample for 196" of 233 bodies. The eval gate (`detector_v5z_final` on nhanes25) finds 225 of 233 bodies, from 24 of 25 spines, in its train or val lists.
- **Supplement, box convention.** 86.8 % and 12.9 % are whole-vertebra outline numbers; under the body convention they are 11.1 % and 3.8 % (`results/indomain/INVENTORY.md`). The text does not state the convention; the Figure S4 caption does.
- **Methods, COBRA2026.** "152 of 467 Elekta cases, cut by download volume" conflicts with the standing directive against download-budget subsets. The G0 fetch is pending.
