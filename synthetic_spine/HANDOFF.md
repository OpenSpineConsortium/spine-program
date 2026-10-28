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
- **The fifteen closed papers read from the page (2026-10-28, spine-program #238).** They are fifteen of the 29
  papers whose full text no script here may read (`sources.csv`). The other 14 are Panjabi's three, read from the
  page before; Ahn 2001, which supplies no value of its own; Eisenstein 1977, read through Chaudhary 2015; and the
  nine PMC-held papers still unread (README, discrepancy 10; item 1 below). Greg sent ten as PDFs: the seven
  secondary pedicle series' own papers, Hinck 1966, Tang 2016 and Bach 2019. Another thread of this project fetched
  the other five the same day from their publishers' free copies: Griffith 2016, Twomey 1985, Alonge 2021, Ahmed
  2019 and Chaudhary 2015. None is committed. Readers not shown our values transcribed the tables these values could
  come from, whole or at the values' levels, from the page images (`verification/closed_page_reading.csv`), and the
  nine typeset papers were also matched against their text layer. What the reading leaves out holds no value of the
  data that the reading does not (README, "What the reading leaves out"). Of the 203 values these papers carry, 185
  agree with their own papers and Eisenstein's five with Chaudhary's copy of them, and each of the other 13 is
  reproduced by a calculation or by another paper's table (`code/check_closed_reading.py`, run by
  `scripts/check.sh`). It answers the Olsewski and Robertson questions below, and it found that the level table's n
  is each study's whole sample in every sex's row (item 4 below).

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

**494 of the 815 values cannot be checked by machine here.** By cause, and how many a page reading has checked
since:

| cause | papers | values | read from the page | why the machine stops |
|---|---|---|---|---|
| PMC holds the paper, outside its open-access subset | 10 | 267 | 40, Griffith 2016's | NCBI serves full text for text mining only from the open-access subset. A person can read these on PMC's site; a script may not fetch them in bulk. |
| Not indexed in Crossref or PubMed | 3 | 65 | all | Alonge 2021, Ahmed 2019 and Chaudhary 2015, with Eisenstein 1977's five read through Chaudhary. Each is open on its journal's own site (README, discrepancy 9), which this session's proxy refuses to scripts; another thread fetched them. |
| Secondary series, transcribing paper not named | 7 | 38 | all | The pedicle table took these from a later paper's comparison table and did not record which. |
| Paywalled, no PMC copy | 3 | 34 | all | Ahn 2001 (Hinck 1966's values, read here from Hinck's own paper; Ahn's copy was not read), Tang 2016, and Twomey 1985, which is free in Acta Orthopaedica's archive. |
| Tables are images | 1 | 20 | none | Pierro 2017 is open access, but PMC holds its tables as pictures. Not attempted; it needs the same page reading Panjabi had. |

Panjabi's 70 values also fall outside the machine check, but the page reading covers them. The reading of the closed
papers covers 177 more: the 38 secondary pedicle values, Hinck's 10, Tang's 4, Twomey's 20, the 65 read from the
three unindexed papers (Eisenstein's five through Chaudhary's copy) and Griffith's 40. It also checks from the page
the 26 values of those papers that only an abstract had confirmed (Bach's 24 and two of Mitra's). That leaves 247
values that no reading has checked: the 227 of the nine PMC-held papers still unread (README, discrepancy 10) and
Pierro's 20.

**Of four data questions, two are answered from the page and two are open.** The copied tables are left as their
sources have them, because each needs the paper or your decision:
- **Cizmic 2023's five canal-depth SDs** (1.66, 1.93, 1.95, 2.2, 2.71) are printed nowhere in the paper, and a08c821
  does not say where they came from. Two derivations were tried and neither reproduces them:
  - the combined-sample SD from the paper's per-sex Table 5 gives 1.64, 1.98, 2.00, 2.21, 2.69 (the same formula
    reproduces the paper's printed canal-width SDs within 0.01);
  - the average of the two sexes' SDs gives 1.62, 1.92, 1.93, 2.19, 2.70.
- **Olsewski 1990's pedicle widths**, answered: they are the paper's Table II (p. 544), 21 cadaver spines (p. 543)
  measured directly, the sexes combined (p. 545), and Arockiaraj 2025's transcription is the one that differs. Its
  five values need no change; its cohort row does (item 4 below).
- **Robertson 2000's cohort columns**, answered: 10 dry-bone lumbosacral spines, wire-marked and radiographed
  coaxially, not 100 CT patients; the paper gives no origin, sex or age for them, and New Zealand is only where its
  authors worked. The series is Table 1's transverse width at the isthmus, the measure the table's
  header names; the paper's "isthmus diameter" row is the short axis of the pedicle's ellipse, which tilts 31 deg
  from the vertical at L4 and 55 deg at L5, so it is not a transverse width. Correcting the cohort columns is yours.
- **Yadav 2020, women, L3-L4 disc SD of 6.87** is four to five times its neighbours. The paper is in PMC but outside
  the open-access subset.

**Not fixed upstream, because each would change a copied file:**
- The pedicle table's header still says twelve series; it has thirteen.
- `panjabi_reference.csv` still says the T11 and T12 end-plate widths exist only as a curve.
- The article's figure code labels "Otsuki 2020" and "Moncada-Habib 2023" have the wrong years (Irie 2021; 2025).

**No systematic search was ever run.** This is the collection gathered for one figure, not a review.

## What needs a person

1. **Read the 9 PMC-held papers still unread on PMC's site** and compare their values with `verification/values.csv`
   (filter `paper`). Yadav and Tan carry the most values (72 and 60). The links are in `SOURCES.md`. Griffith 2016,
   the tenth, was read from the page on 2026-10-28.
2. **Done on 2026-10-28:** the values of the paywalled, secondary and unindexed papers were read from their own
   papers' pages, Twomey 1985, Alonge 2021, Ahmed 2019 and Chaudhary 2015 among them; Hinck's from Hinck 1966
   itself, since Ahn 2001, which the level table cites for them, was not read; and Eisenstein 1977's five from
   Chaudhary's copy of them (item 3).
3. **Read Eisenstein 1977 (J Bone Joint Surg Br) itself**, if its five values matter: they agree with Chaudhary's
   copy of them, and Eisenstein's own paper has not been read here. It would also say how Eisenstein measured, which
   is not known here: Chaudhary names Eisenstein 1977 among the workers who used plain radiography (p. 34), Alonge
   2021 calls it a study of Caucasian and Negroid bone specimens (p. 75), and the level table's modality, dry bone,
   is typed in `data/make_reference_table.py` (line 82) with no source given.
4. **Correct the four cohort rows of the pedicle table** the page reading found wrong (Olsewski, Robertson,
   Zindrick, Krag; README, "What follows from the reading"). Decide what the level table's n should hold: each
   study's whole sample in every sex's row, as now, or the count of the people the row is of, which the check sets
   beside n for six series (`n_printed`: Bach's 109 men and 131 women of 240, Griffith's 540 of each of 1,080,
   Alonge's 54 and 66 of 120, Ahmed's 36 men of 80, Chaudhary's 150 men of 300, and Tang's 107 and 105 of 109). Five
   more series carry an n that is not the count of the people a value is of, and `n_printed` leaves them out:
   Twomey's 20 carry 204, every cadaver of every age, where its Table 2 prints no n and Table 1's young adults are
   24 men and 24 women; Mitra's L1 and L5 are of 18 men, where n is 20; Olsewski's are of 41 or 42 pedicles of 21
   spines, and Robertson's of 10 specimens, where n is 100; and Hinck prints 59 to 50 per level, whose range is its
   n (README, "What follows from the reading"). Decide whether Yu's row should hold Yu's own means and Mitra's one
   method, and whether the women's columns that Ahmed, Chaudhary and Alonge print should be added.
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
