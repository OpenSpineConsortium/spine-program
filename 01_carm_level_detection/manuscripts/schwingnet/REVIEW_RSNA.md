# REVIEW_RSNA.md — Radiology: Artificial Intelligence reviewer pass

Reviewed: `main.pdf` (27 pages, compiled 2026-09-23, job 40419641 build) read page by page with pymupdf
(text + 150-dpi page renders); `supplement.pdf` (5 pages); every rule in `RSNA_AI_REQUIREMENTS.md`; claims
checked against `NUMBERS.md`, `CLAIMS_LEDGER.md` and the files under `results/` (spot-verified:
`a1.json`, `a3.json`, `a4.json`, `a6.json`, `a7.json`, `a9.json`, `counting.json`, `coupling.json`,
`contribution_matrix.json`). The manuscript was not edited.

---

## VERDICT

**Not submittable today, and that is mostly by design: 83 open `\PENDING` placeholders (G0–G6) sit in the
abstract, Results, Discussion, Table 4, Figure 4d and Figures 6a–c.** The structure, word economy and
number discipline are the strongest I have reviewed against this journal's rules — every quoted quantity I
spot-checked traces to a result file and matches it exactly, negative results are reported, the selective-quoting
disclosure (5 of 1,440 / 6 of 120 cells) is in Methods, and the box-convention caveat survives everywhere a
detector number appears.

Three things beyond the gates require action before submission, ranked below: (1) the anonymization
failures (the network is named after the author in a double-anonymized submission, plus sole-author guarantor
and a commercial-interest statement in the anonymized file); (2) the title's two claims that no number on disk
yet supports; (3) one selective-reporting soft spot on the modality-boundary claim. Everything else is
reference formatting, abbreviation hygiene and figure production mechanics.

---

## RULE-BY-RULE (RSNA_AI_REQUIREMENTS.md)

### Limits
| Rule | Verdict | Where |
|---|---|---|
| Body word count ≤3,000 | **PASS** (2,999; `tools/check_limits.py`) | p4–11 |
| Abstract structured, ≤250 words, four sections | **PASS** (250; Purpose/M&M/Results/Conclusion) | p3 |
| References ≤35 | **PASS** (33, all with DOI) | p12–15 |
| Figures ≤6, ≤4 components each | **PASS** (6 × a–d exactly) | p22–27 |
| Tables ≤4 | **PASS** | p18–21 |
| Key Points ≤3, with summary data, no vague language, no abbreviations beyond CT/MRI | **PASS** (3; each carries k/n and an interval; "C-arm" and "cone-beam CT" are within the allowance) | p1 |
| Summary statement 1–2 sentences, ≤255 chars, boldface, no abbreviations | **PASS** (220 chars, bold on the title page) | p1 |
| Abbreviations ≤10, defined at first use | **PARTIAL FAIL** — list holds 7, but "CI" (p3, abstract Results) and "R2" (p3) are used in the abstract without expansion; R² is not in the abbreviation list yet appears in Figure 4 and Tables 1–2 (defined only in table footnotes, not the Fig 4 legend); the list ends with a stray semicolon and BCa is out of alphabetical order | p1–3, p25 |
| CLAIM checklist at first submission | **PASS structurally** (`CLAIM_CHECKLIST.md`, `claim_checklist.json`, the docx in the packet) — verify it rides in the packet |
| Supplement ≤12 pages, one document | **PASS** (5 pages; Figure S1 flow, Figure S2 matrix, Table S1 all present as vector content) |
| Text file .docx, double-spaced, no page numbers | **FAIL today, packet item** — the compiled artifact is a single-spaced LaTeX PDF with page numbers; the ScholarOne upload must be the .docx conversion. Not a manuscript defect, a packet defect. |

### Abstract content
| Rule | Verdict |
|---|---|
| Purpose 1–2 sentences | **PASS** |
| M&M: retro/prospective, dates, subjects, groups, procedures, evaluation in Results order, statistics sentence | **PARTIAL** — all present except **age and sex** (owed by `\PENDING{G0}{age and sex by source}`; when G0 closes, the abstract M&M must gain the age/sex clause or an explicit "not released by the sources", not only the Results) |
| Results: parallel to Methods, significance indicators, actual numbers and percentages | **PASS** (every share carries k/n and a 95 % CI; one sentence is a PENDING placeholder) |
| Conclusion derived from results, no elaboration | **PASS**, with one softening flagged below |

### Main body
| Rule | Verdict |
|---|---|
| Intro: brief, final paragraph = hypothesis + purpose | **PASS** (330 words; hypothesis names the pre-stated 97 % grade) | 
| Methods first paragraph: design, dates, IRB determination, HIPAA, registry, subject-overlap citation | **PASS** (determination 2026-269; overlap = ref 20) |
| Exclusions with cause, per source | **PASS** (Table 1 footnotes b–i are exemplary) |
| Sample-size derivation | **PASS** (Wilson arithmetic for the transitional bound; "no sample size was set for naming" is stated plainly) |
| Readers: number, training, expertise | **PASS with note** — "No person read an image" is stated first in Reference standard; the two automatic labellers and the 814/910 agreement filter substitute. A reviewer may still ask why no human read even a sample; the three-L6-cases row already concedes the cost. |
| Pre-specified primary/secondary outcomes | **PASS** |
| Statistics last paragraph: methods, software+versions, P, power | **PASS** |
| Results first paragraph = demographics | **PASS** ("Study population") |
| n/N for every percentage | **PASS** (checker warns on one sentence — the film-vs-fluoroscopy −0.7 is a difference, n = 7,311 stated; acceptable) |
| Same order/subheadings as Methods | **PASS** (detection → formation → naming/counting/coupling → transitional) |
| "significant" only with a test | **PASS** |
| Discussion: no table/figure citations | **PASS** (grep: 0) |
| Discussion first paragraph = problem + primary results | **PASS** |
| Limitations = second-to-last paragraph | **PASS** (paragraph 5 of 6 opens "This study has limitations.") |
| Summary = last paragraph | **PASS** |
| No claim of priority | **FAIL as written — see Fix 6.** "to our knowledge, the first" (device terms), "to our knowledge no released model performs this task", and "The corpus is largest on assembly" are priority claims. The ledger adjudicates the first two as DEFENSIBLE with the hedge and the third as DEFENSIBLE **only after G4**; the transcribed rule says none at all. |
| No self-evaluation words, no institution/funder, SI units | **PASS** (grep clean; the one "unique" is inside a cited article title, which is allowed) |
| Anonymization | **FAIL — see Fix 2.** |

### Statistics (journal top-10)
**PASS**: denominators everywhere; clustered bootstraps with the cluster named per row; BCa beside
percentile; Holm over four pre-listed comparisons; sign tests; multiplicity disclosed; power arithmetic given;
the design-effect Wilson intervals are a nice touch.

---

## CLAIMS AUDIT — abstract, key points, discussion

Every number below was re-read from its file. "VERIFIED" = matches the file to the digit.

| Claim | Evidence | Status |
|---|---|---|
| 594/617 = 96.3 % [93.1, 98.7] zero-shot lateral | `results/a7.json#cells/zeroshot2~1det~1LAT~1kfull` | **VERIFIED** |
| 606/617 = 98.2 % [95.7, 100.0] case-grouped | `results/a4.json#cells/det~1LAT~1kfull` | **VERIFIED** |
| 239/631 = 37.9 % AP zero-shot | `results/a7.json` | **VERIFIED** |
| 231/287 = 80.5 % [74.1, 86.8]; 43/56 = 76.8 % [64.3, 89.3] at 0.74 | `results/a1.json#operating_points/cross_device_0.74` | **VERIFIED** |
| 260/287 = 90.6 %; 47/56 = 83.9 % at 0.25 | `results/a1.json#operating_points/conf_0.25_as_quoted` | **VERIFIED** |
| +71.8 pp [63.4, 79.6] wide-arc marginal | `results/contribution_matrix.json#marginal_contributions` | **VERIFIED but seed 0 of two** — seed 1 gives +67.6 [57.6, 76.8]. The Results discloses "seed repeats moved it 1.1–5.6 points", but the abstract and Key Point 2 quote only the larger seed. Soften (Fix 4). |
| +0.038 [0.021, 0.057], 4/24 negative, sign-flip P = .0002 | `results/a3.json#comparisons/card_vs_uncalibrated_physics` | **VERIFIED** |
| Cios Fusion fails the BCa interval (−0.0005 lower bound) | `results/a6.json#verdict` (`C3_holds_bca: false`) | **VERIFIED** — and honestly reported |
| 188/197 = 95.4 % ordinal; 306/378 pooled; 46/56 anchored | `results/counting.json` | **VERIFIED** |
| 1,129/1,149; 1,104; 1,120; 18/266 stop signal | `results/coupling.json` | **VERIFIED** |
| 92.5 % (571/617) day-grouped | `results/a9.json#cv/cvday...` | **VERIFIED** |
| +57.7 pp lateral−AP; +27.5 pp film−render; +14.3 pp control−held-out sacrum; Holm P = .002 each | `results/a3.json#primary_with_holm` | **VERIFIED** |
| Film validation 97.3–99.8 % per release | `results/a5.json` per NUMBERS.md | traced (not re-opened) |
| −0.7 pp [−10.1, 8.6] modality-boundary excess | `results/a2.json#corpus_manifold` per NUMBERS.md | **VERIFIED against NUMBERS.md, but see Fix 3**: the same block records knn15 +9.2 (BCa [+1.4, +23.4]) and pca12/knn15 BCa [+0.6, +21.6] — two of six cells exclude zero on BCa. Quoting only the logistic cell under-sells the counter-signal to "must be held out by device, not modality". |
| Intro literature rates (50 % surveyed; 0.12 % of 34,544; 4.3–15 %; 8.8 % of 3,147; 38/71) | `CLAIMS_LEDGER.md` comparator table | **VERIFIED against the ledger** |
| "first per-vertebra recall on a held-out C-arm with interval and pre-stated operating point" framed as a test-design claim, "80.5 % sits below the in-domain 0.964" | ledger row: DEFENSIBLE NOW | **VERIFIED** — the self-deprecating comparison is exactly right |
| "largest on assembly, not raw image count" | ledger: DEFENSIBLE **AFTER G4** | **UNSUPPORTED TODAY** — written against `\PENDING{G4}`; must not survive if the census disappoints |
| Transitional sensitivity/specificity/parity | all `\PENDING{G3/G5/G6}` | placeholders, correctly not asserted |

No claim in the abstract or key points is invented; the two flagged items are emphasis, not fabrication.

---

## FIGURES (each: four components? legend complete? legible? convention stated?)

**Figure 1 (p22), method.** Four panels a–d. Legend defines GRU, NCC. Diagrams legible at print size.
**PASS.**

**Figure 2 (p23), transitional gallery.** Four panels; five columns per panel with per-cell source
sub-captions; hatched cells name what is absent (good). Arrow and 20-mm bar defined. **Two gaps**: (i) the
journal wants **age, sex and clinical history** for human images "where relevant" — none is given and none
is released by the sources; add one legend sentence saying so; (ii) the C-arm exposure in (a) is "level by
automatic read, unverified" — stated, good. Tonal convention (bone white on dark) holds in columns 1–2 and
4–5; the device-card renders (column 3) are fluoroscopy-toned; acceptable but be ready to defend.
**PASS with the age/sex sentence owed.**

**Figure 3 (p24), detection.** Four panels. Convention stated in the caption and on the panel
("whole-vertebra boxes throughout; the body-box recompute is pending") — the box-convention rule is
satisfied. **Defects**: (b) the red pending annotation collides with plotted markers around N = 200–400;
(d) the per-box confidence labels (0.61, 0.39, …) will be near-illegible at 3-inch column width — enlarge
or drop to the two the caption needs; the pre-stated-vs-default legend is clear. **PASS after cosmetics.**

**Figure 4 (p25), formation.** Panels a–c real; **(d) is a labelled PENDING G4 placeholder** — blocks
submission until filled. R² appears in panel (a) sub-captions and is **not defined in this legend** (rule:
every abbreviation defined in the legend of that figure). Panel (b) nine-term grid is dense but each mark
type is defined below the panel. **FAIL until 4d fills and R² is defined in the legend.**

**Figure 5 (p26), naming and safety net.** Four panels. (a) intervals and per-point n's given; (b) states
convention and threshold on the panel ("whole-vertebra boxes, confidence 0.74") — the annotation "off by
more 0" should read "off by more than one: 0"; (c) the worked L6 example is the best figure in the paper;
its small grey source footer text ("truth, VERIDAH read … TotalSegmentator read: L1–L5") is
essential and must stay legible at print size; (d) matrix legible. **PASS with the two wording/size fixes.**

**Figure 6 (p27), transitional claim.** (a)–(c) are PENDING G6 placeholder panels; (d) is real and good.
**FAIL until G6 fills** — by design.

Production mechanics for the packet (not the PDF): photographic panels as TIF/PSD/EPS at 300 dpi (PNG
refused), graphs at 1,200 dpi with layers, labels in bold sans-serif ≥12 pt, one combined figures document
with legends after each figure for a new submission.

---

## TABLES (title? footnotes? n/N? merged cells?)

**Table 1 (p18).** Titled; group rows are sub-headings, not merged cells (checker confirms); every
abbreviation footnoted; the eleven-footnote exclusion accounting (b–i) is the most rigorous data table I
have seen at this journal. Extremely dense at ~7 pt rotated — the .docx conversion must keep it one page
without dropping below legibility; consider moving footnotes g/h detail to the supplement if it breaks.
**PASS.**

**Table 2 (p19).** Titled; convention stated in the title AND footnotes; every cell k/n [CI]; "–" defined;
the footnote conceding the 5.2 % convention-mismatch reading and the body-box control numbers is exactly
the right honesty. PENDING G5 rows structural. **PASS.**

**Table 3 (p20).** Titled; every row k/n, clusters, percentile and BCa; abstention rule and the three-L6
agreement row properly quarantined in footnotes. **PASS.**

**Table 4 (p21).** Titled; inventory column real, claim columns PENDING G3/G6 as designed; footnotes
define every abbreviation and the mask-vs-subtype distinction. **PASS as structure.**

---

## SENTENCES TO CUT OR SOFTEN (verbatim, with the ask)

1. **Title:** "…robust to transitional anatomy, versus registration-assisted neurosurgeons" — CUT or
   defer both clauses. No transitional accuracy exists on disk (all G6-pending), so "robust to transitional
   anatomy" is today unsupported; the neurosurgeon comparison is a **simulated** surgeon+LevelCheck
   reconciliation, also pending. If G6 lands and passes the pre-stated bounds, "robust to" is still stronger
   than a bound-passing result warrants; "tested on transitional anatomy against a registration-assisted
   reference" is what the evidence would then support. (`TITLE.md` records the title as fixed by the PI —
   this is the reviewer's finding for that decision, not an edit.)
2. **Abstract conclusion / summary statement:** "Naming needed only the C-arm on lateral exposures" —
   soften to bind it to the one device tested (the limitation paragraph already concedes "only one
   intraoperative device is held"). E.g. "on lateral exposures of the one intraoperative device tested".
3. **p8:** "so a detector must be held out by device, not modality" — soften or complete: the quoted
   logistic cell is −0.7 [−10.1, 8.6], but two of the six pre-listed cells (knn15, pca12/knn15) exclude zero
   on the BCa interval (`results/a2.json`). Either quote the range across the six cells or say "the linear
   readout found no boundary; two nearest-neighbour readouts found a weak one" — the conclusion still
   holds, and then it is bullet-proof.
4. **Key Point 2 and abstract:** "(+71.8 percentage points; 63.4, 79.6)" — state the seed or the pair:
   seed 1 of the same arm gives +67.6 [57.6, 76.8]. "+67.6 to +71.8 across two seeds" costs four words and
   removes the only favorable-selection example a hostile reviewer can find in the front matter.
5. **Key Point 3:** "fitted per device on 40 real exposures" — one device (PIXIUM 4600) was fitted on 14
   of 18. "on up to 40 real exposures per device" or "(14–40 per device)".
6. **p10 Discussion:** "the nine terms here are, to our knowledge, the first"; "The corpus is largest on
   assembly, not raw image count"; "to our knowledge no released model performs this task" — the journal
   rule as transcribed is *no claim of priority*. Minimum action: keep at most the one ledger-adjudicated
   "to our knowledge, the first" for the device terms (DEFENSIBLE NOW), and cut "largest on assembly" until
   G4 delivers the census (ledger: DEFENSIBLE AFTER G4). "No released model performs this task" can be
   restated as a fact about the literature search ("the survey found none") rather than a priority claim.
7. **p11:** "The clinical role is decision support abstaining visibly beside the surgeon's own count, never
   replacing the check film" — keep; but "the next test is a phantom, then a cadaver, then a human series"
   borders on announcing ongoing work; recast as recommendation ("the next test should be…") to stay inside
   the no-incomplete-investigations rule. (Two words.)

---

## FIXES REQUIRED BEFORE SUBMISSION, RANKED

1. **[Blocking, by design] Close gates G0–G6 and fill the 83 PENDING placeholders**, including the abstract
   Results sentence, Figure 4d, Figures 6a–c and Table 4's claim columns. `tools/check_limits.py` must exit
   0. After every fill, re-run it — the body sits at 2,999/3,000 words and the abstract at 250/250 with
   zero headroom.
2. **[Blocking, editorial risk] Anonymization.** Three identity signals sit in the anonymized file:
   (i) "SchwingNet" — the author's surname — in the title and throughout (`TITLE.md` records
   ANONYMISED-VARIANT = no as the PI's decision; the rule as transcribed fails it, and desk return is the
   realistic risk); (ii) "The sole author is the guarantor" (p11) reveals single authorship, which with
   ref 20 (Schwing G, first author of the dataset this work builds on) makes identification trivial;
   (iii) the conflicts statement (p12, commercial interest in a level-confirmation product) belongs on the
   full title page, not the anonymized manuscript. Minimum without overriding the PI: move (ii) and (iii)
   to the full title page and put the ANONYMISED-VARIANT decision in the cover letter.
3. **[Required] Selective-reporting repair on the modality-boundary sentence** (item 3 above) — this is
   the same class of defect `results/RIGOR_FIXES.md` was created to purge; fix it the same way.
4. **[Required] Seed disclosure on +71.8** (item 4) and the PIXIUM frame count in Key Point 3 (item 5).
5. **[Required] Title claims** (item 1) — at minimum after G6: if the bounds are missed, the title's two
   clauses are falsified by the paper's own Table 4 and must change; decide the fallback title now.
6. **[Required] Priority-claim trim** (item 6).
7. **[Required] Reference cleanup:** ref 14 has mangled authors ("P YR, S G, R D") — restore real
   surnames; refs 19, 28 and 30 embed editorial annotations inside the bibliography entry ("Generic
   image-formation model: …", "867 patients, six European centres… public split 692 / 52 / 123",
   "preprint posted 10 December 2015") — annotations belong in the text, not the reference; journal names
   inconsistently abbreviated (refs 1, 2, 4, 5, 13 full names vs NLM style elsewhere) — NLM-abbreviate all;
   ref 28 "Kamp F et al." should list authors per NLM before et al.
8. **[Required] Abbreviation hygiene:** spell out "confidence interval (CI)" at first abstract use; either
   spell out R² at first use and add it to the list or keep it footnote-defined everywhere it appears
   **including the Figure 4 legend**; delete the trailing semicolon after "NCC, normalised cross-correlation;";
   alphabetize BCa.
9. **[Required] Figure cosmetics:** Fig 3b annotation collision; Fig 3d label size; Fig 5b "off by more 0"
   → "off by more than one: 0"; Fig 2 legend sentence "age, sex and clinical history are not released by
   any source"; define R² in Fig 4's legend.
10. **[Packet] .docx conversion** double-spaced, no page numbers, 11-pt Arial/Calibri/TNR; tables one per
    page at the end; separate combined figures document with legends after each figure; production files
    TIF/EPS (no PNG) at 300/1,200 dpi; CLAIM checklist, cover letter with subject-overlap statement
    (ref 20 named), full title page with word count, data-sharing statement, ORCID, CRediT.
11. **[Advisory] Abstract age/sex clause** when G0 closes (or an explicit unavailability statement) — the
    abstract M&M element list requires it "where appropriate".
12. **[Advisory] Table 1 legibility** through the Word conversion; pre-plan the footnote spill to the
    supplement.

## What is genuinely strong (keep)

The test-design framing of the detection claim ("a test-design claim, not a larger number: 80.5 % sits
below the in-domain 0.964"); the pre-stated operating point and its honest miss of the 97 % grade; both
fold groupings reported with the gap unexplained; the three-L6-cases quarantine ("agreement, not
correctness"); the Cios Fusion BCa failure reported in the abstract-adjacent Results; the day-grouped
92.5 % beside the case-grouped 98.2 %; Table 1's exclusion accounting; the stop-signal quantification
(9 of 10 error frames flagged, 1,040 of 1,041 unflagged bodies exact). Do not let condensation passes
remove any of these.
