# Handoff: what was done, where it falls short, and what needs a person (2026-10-27, updated 2026-10-28)

Written for Greg, who takes this on from here. README.md describes the folder and its findings; this file says what
was attempted, what failed and why, and what is left, so nothing is redone blind.

## Done

- **The collection, copied exactly.** The level and pedicle tables and their generator, copied byte for byte from
  CTSpinoPelvic1K `morphometrics/` at e887274, and 06's whole-spine Panjabi table. `data/COPIED_FROM.csv` records each
  file's repository, commit, path, git blob and SHA-256. `code/check_copies.py --against <clone>` proves the blobs.
- **Every paper resolved.** 42 papers through Crossref and NCBI: 36 DOIs, 39 PubMed ids, 23 PMC copies. Every raw
  answer is kept in `sources_raw/`, and every disagreement between the tables' citation and the paper is printed in
  `SOURCES.md`.
- **Every value checked in context where a machine can read the paper.** 316 of 815 values are confirmed at the right
  level, sex, measure and role, each with the table cell or sentence quoted in `verification/values.csv`. None is
  found only out of context.
- **Panjabi read from the page.** His three papers are scans with no text layer. A reader not shown our values
  transcribed his tables from the page images. All 173 Panjabi rows across the four tables agree with that reading.
- **One wrong value corrected at its source.** Panjabi 1992's posterior body height SEM at L1 is 1.03 (Table 2,
  p. 301), not 0.92. Fixed in CTSpinoPelvic1K (e887274, pushed to origin and osc) and in 06; 03's article data keeps
  0.92 as published.
- **Two adversarial reviews.** The first found the checker was blind to level and sex, so planted wrong values
  passed; everything since was rebuilt against its findings. The pull request records the second.
- **The ten closed-access papers read from the page (2026-10-28, spine-program #238).** Greg sent their PDFs, which
  are not committed: the seven secondary pedicle series' own papers, Hinck 1966, Tang 2016 and Bach 2019. Readers
  not shown our values transcribed their tables from the page images (`verification/closed_page_reading.csv`), and
  the five typeset papers were also matched against their text layer. Of the 78 values these papers carry,
  65 agree, and each of the other 13 is reproduced by a calculation or by another paper's table
  (`code/check_closed_reading.py`, run by `scripts/check.sh`). It answers the Olsewski and Robertson questions
  below.

## How it was done, and what failed on the way

Each of these was tried, failed, and was replaced. They are listed so the same mistakes are not made again.

1. **Matching a number anywhere in a paper's tables.** The first checker did this, and it was wrong. A value of 2.4
   turned up in some cell of most tables, so planted errors passed. It was replaced by a context test on the cell's
   row, column and section: level, sex, measure, species, and the mean-or-SD role. A cell holding both the mean and
   its SD is preferred to one holding the number alone. The measure test is what caught Busscher's posterior-height SD
   being matched in the anterior-height column.
2. **A fixed 160-character window for text and abstracts.** Bach's abstract names the level after the values
   ("5.6 +/- 1.1 mm for men ... at T12/L1"), so the window credited each level's numbers to the level before it. In
   Pierro, a single patient's L5 reading matched an L4 value. The window was replaced by clauses: a sentence is split
   at commas and semicolons, the level comes from the number's own clause, and the sex from the words next to it.
3. **Crossref's first plausible candidate.** It returned the wrong paper four times:
   - Gilad: a J Biomech paper.
   - Abbas: a J Biomed Res paper.
   - Bonczar: another paper by the same author.
   - Amonoo-Kuofi 1982: his muscle-spindle paper.

   A candidate now has to agree with the citation on author, year, journal and first page. Where that is not enough,
   the DOI is pinned in `code/resolve_sources.py` with the reason written beside it.
4. **The first-page test refused a right paper.** The tables cite Masharawi as article 1023; it is 1026. That DOI is
   pinned, with the evidence: every value of the series is in that paper's Table 4.
5. **Europe PMC**, the first choice for full text, answered 503 to every request on 2026-10-27. NCBI's E-utilities
   were used instead. Europe PMC answered again later that day; each run now records its answer.
6. **Smaller traps**, each found by a second run or a check:
   - Sorted output changed between runs: "T12" and "T12L1" sort equal, and set order follows Python's per-process
     string hashing.
   - The test for image-only tables counted `<table-wrap-foot>` as a table.
   - The Write tool turned typed `\u2013` escapes into the characters themselves.
   - Windows checkouts with core.autocrlf rewrote line endings. Hence `.gitattributes`, and `scripts/check.sh` must
     run from an LF checkout: on this laptop its vendored-copy step fails only for that reason, and it passes in a
     clean LF clone.

## Where it falls short, and why

**494 of the 815 values cannot be checked by machine here.** By cause:

| cause | papers | values | why the machine stops |
|---|---|---|---|
| PMC holds the paper, outside its open-access subset | 10 | 267 | NCBI serves full text for text mining only from the open-access subset. A person can read these on PMC's site; a script may not fetch them in bulk. |
| Not indexed in Crossref or PubMed | 3 | 65 | Alonge 2021, Ahmed 2019 and Chaudhary 2015. Each is open on its journal's own site (README, discrepancy 9), but this session's proxy refuses those sites to scripts. |
| Secondary series, transcribing paper not named | 7 | 38 | The pedicle table took these from a later paper's comparison table and did not record which. Read from their own papers' pages since. |
| Paywalled, no PMC copy | 3 | 34 | Ahn 2001 (Hinck 1966's values) and Tang 2016, both read from the page since; Twomey 1985, free in Acta Orthopaedica's archive, behind the same proxy refusal. |
| Tables are images | 1 | 20 | Pierro 2017 is open access, but PMC holds its tables as pictures. Not attempted; it needs the same page reading Panjabi had. |

Panjabi's 70 values also fall outside the machine check, but the page reading covers them. The reading of the
closed-access papers covers 52 more: the 38 secondary pedicle values, Hinck's 10 and Tang's 4. It also checks from
the page the 26 values of those papers that only an abstract had confirmed (Bach's 24 and two of Mitra's).

**Of four data questions, two are answered from the page and two are open.** The copied tables are left as their
sources have them, because each needs the paper or your decision:
- **Cizmic 2023's five canal-depth SDs** (1.66, 1.93, 1.95, 2.2, 2.71) are printed nowhere in the paper, and a08c821
  does not say where they came from. Two derivations were tried and neither reproduces them:
  - the combined-sample SD from the paper's per-sex Table 5 gives 1.64, 1.98, 2.00, 2.21, 2.69 (the same formula
    reproduces the paper's printed canal-width SDs within 0.01);
  - the average of the two sexes' SDs gives 1.62, 1.92, 1.93, 2.19, 2.70.
- **Olsewski 1990's pedicle widths**, answered: they are the paper's Table II, 21 cadaver spines measured directly,
  sexes pooled (p. 544), and Arockiaraj 2025's transcription is the one that differs. The table needs no change.
- **Robertson 2000's cohort columns**, answered: 10 dry-bone lumbosacral spines, wire-marked and radiographed
  coaxially, not 100 CT patients. The series is also the pedicle's full width, not its isthmus, which is a separate
  row of the same table (left 9.9, 10.0, 12.3, 13.4, 13.2 at L1 to L5). Correcting the cohort columns, and choosing
  between the width and the isthmus, is yours.
- **Yadav 2020, women, L3-L4 disc SD of 6.87** is four to five times its neighbours. The paper is in PMC but outside
  the open-access subset.

**Not fixed upstream, because each would change a copied file:**
- The pedicle table's header still says twelve series; it has thirteen.
- `panjabi_reference.csv` still says the T11 and T12 end-plate widths exist only as a curve.
- The article's figure code labels "Otsuki 2020" and "Moncada-Habib 2023" have the wrong years (Irie 2021; 2025).

**No systematic search was ever run.** This is the collection gathered for one figure, not a review.

## What needs a person

1. **Read the 10 PMC-held papers on PMC's site** and compare their values with `verification/values.csv` (filter
   `paper`). Yadav and Tan carry the most values (72 and 60). The links are in `SOURCES.md`.
2. **Done on 2026-10-28 but for Twomey 1985:** the paywalled and secondary papers were read from the page. Twomey
   1985 is free in Acta Orthopaedica's archive (https://actaorthop.org/actao/article/view/23300); download it and
   read it from the page the same way.
3. **Read Alonge 2021, Ahmed 2019 and Chaudhary 2015**, found open on their journals' own sites (README, discrepancy
   9), from the page. Eisenstein 1977 (JBJS Br) can be read directly instead of through Chaudhary.
4. **Correct the four cohort rows of the pedicle table** the page reading found wrong (Olsewski, Robertson, Zindrick,
   Krag; README, "What follows from the reading"), and Bach 2019's n in the level table, 240 in each sex's row where
   the men are 109 and the women 131. Decide whether Yu's row should hold Yu's own means, Mitra's one method, and
   Robertson's the isthmus.
5. **Read Pierro 2017's table images** (open access).
6. **Decide the two open data questions**, and the corrections of item 4. Then correct them in CTSpinoPelvic1K
   `morphometrics/`, as e887274 did for Panjabi, and re-copy here with `code/check_copies.py`.

## Not started: every measurement, not seven

The collection carries seven measures, those Figure 6 compared. The 12 open-access papers print about 5,800 numbers
in their tables and this folder uses 280. Some are ages and p-values, but most are measurements that were never
taken: end-plate depths, the lower end plate, central body height, pedicle height, length and angle, process lengths,
facets, foramina, canal areas, laminar angles, the patient arms, and the per-sex tables. Panjabi alone reports several
dozen parameters per level. The plan, for a hierarchical Bayesian model in which a study contributes whatever it
reports:

1. **One long table.** A row per study, group, sex, level, measure and statistic. Each row carries n, the dispersion
   type, modality, the paper's own definition (plane, landmarks, cortex), and the table, page and cell it came from.
2. **Re-extract everything from the 42 papers already resolved.** `code/verify_tables.py` already reads every cell
   with its row, column and section, so the open-access papers can be extracted by program and Panjabi's by a full
   blind page reading.
3. **A real search, as code.** Queries, dates and hit lists saved, and screening with recorded reasons. PubMed,
   Europe PMC, OpenAlex and Crossref are open; Scopus needs an institutional API key, and none was available here.
   Expect hundreds of papers.
4. **What the model needs that summaries cannot give.**
   - Published summaries give each measure's mean and spread, never how two measures vary together. That joint
     structure has to come from individual-level data, which here means ostk's measurements on the 802 CTs.
   - The definition is part of the measure, so incompatible definitions stay separate.
   - Panjabi's two papers are the same twelve spines, and meta-analyses such as Bonczar pool primaries already
     present, so those must not be counted twice.
   - Which measures a paper reports is not random.
