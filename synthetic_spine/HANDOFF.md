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
- **The sixteen closed papers read from the page (2026-10-28, spine-program #238).** They are sixteen of the 29 papers
  whose full text no script here may read (`sources.csv`). The other 13 are Panjabi's three, read from the page
  before; Ahn 2001, which supplies no value of its own; and the nine PMC-held papers still unread (README, discrepancy
  10; item 1 below). Greg sent eleven as PDFs: the seven secondary pedicle series' own papers, Hinck 1966, Tang 2016,
  Bach 2019 and, last, Eisenstein 1977. Another thread of this project fetched the other five the same day from their
  publishers' free copies: Griffith 2016, Twomey 1985, Alonge 2021, Ahmed 2019 and Chaudhary 2015. None is committed.
  Readers not shown our values transcribed the tables these values could come from, whole or at the values' levels,
  from the page images (`verification/closed_page_reading.csv`); the nine typeset papers were also matched against
  their text layer, and Eisenstein's Table I and counts, which two readers read apart and agree on, against his scan's
  text layer, made by optical character recognition. What the reading leaves out holds no mean or SD of the data that
  the reading does not; of the counts the papers print only in their text, the reading holds Ahmed's, Chaudhary's,
  Tang's and Eisenstein's, and Hou's, Olsewski's and Robertson's are named in the README ("What the reading leaves
  out"). Of the 203 values these papers carry, 190 agree with their own papers, Eisenstein's five among them, which
  Chaudhary's copy, where the level table read them, prints too; each of the other 13 is reproduced by a calculation
  or by another paper's table (`code/check_closed_reading.py`, run by `scripts/check.sh`). It answers the Olsewski and
  Robertson questions below and how Eisenstein measured (item 3), and it found that each sex-split series' n is its
  whole sample, in every sex's row (item 4 below). The pull request that added the check, spine-program #239, records
  its three adversarial reviews, and what was checked of the Eisenstein commit that came after them.
- **#239's open decisions taken (2026-10-28, spine-program #240).** Asked for his word on them, Greg answered "i want
  you to figure out those decisions". Each is decided in the README ("Decided"), with its reason and page: the four
  wrong pedicle rows corrected, n as the count of the people a row is of, Yu's own means and Mitra's one method, the
  women's rows and the SDs the papers print, Eisenstein from his own Table I, and the two open data questions. The
  same pull request read the per-sex counts of the eight sex-split series #239 had not read, and Pierro 2017's Table 2,
  beside their page images (`verification/open_questions_reading.csv`, not blind), so each of the eight carries its own
  sex's n, the Italian MRI series is Pierro's own table, whose values the copy did not hold, and four citations name
  their papers as the papers' own records do. The copies stay as they are; `code/apply_decisions.py` writes
  `data/corrected/` and `verification/decisions.csv`, every number from a page reading, and `scripts/check.sh` fails
  once a copy changes under a decision or a written file goes stale. A model reads `data/corrected/`.

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
| Not indexed in Crossref or PubMed | 3 | 65 | all | Alonge 2021, Ahmed 2019 and Chaudhary 2015, with Eisenstein 1977's five, which the level table took from Chaudhary's copy and which were also read from Eisenstein's own Table I. Each is open on its journal's own site (README, discrepancy 9), which this session's proxy refuses to scripts; another thread fetched them. |
| Secondary series, transcribing paper not named | 7 | 38 | all | The pedicle table took these from a later paper's comparison table and did not record which. |
| Paywalled, no PMC copy | 3 | 34 | all | Ahn 2001 (Hinck 1966's values, read here from Hinck's own paper; Ahn's copy was not read), Tang 2016, and Twomey 1985, which is free in Acta Orthopaedica's archive. |
| Tables are images | 1 | 20 | all, for #240 | Pierro 2017 is open access, but PMC holds its tables as pictures. Read from the page for #240: none of the 20 is Pierro's (README, "Decided", 8). |

Panjabi's 70 values also fall outside the machine check, but the page reading covers them. The reading of the closed
papers covers 177 more: the 38 secondary pedicle values, Hinck's 10, Tang's 4, Twomey's 20, the 65 read from the three
unindexed papers (Eisenstein's five from his own Table I and Chaudhary's copy of it) and Griffith's 40. It also checks
from the page the 26 values of those papers that only an abstract had confirmed (Bach's 24 and two of Mitra's). That
leaves 227 values that no reading has checked, those of the nine PMC-held papers still unread (README, discrepancy
10). Pierro's 20 were read for #240 and are none of his; `data/corrected/` holds his Table 2 in their place.

**Of four data questions, two were answered from the page by #239 and two by #240.** The copied tables are left as
their sources have them; `data/corrected/` holds each answer (README, "Decided"):
- **Cizmic 2023's five canal-depth SDs** (1.66, 1.93, 1.95, 2.2, 2.71) are printed nowhere in the paper, and a08c821
  does not say where they came from. Two derivations were tried and neither reproduces them:
  - the combined-sample SD from the paper's per-sex Table 5 gives 1.64, 1.98, 2.00, 2.21, 2.69 (the same formula
    reproduces the paper's printed canal-width SDs within 0.01);
  - the average of the two sexes' SDs gives 1.62, 1.92, 1.93, 2.19, 2.70.

  Decided for #240: `data/corrected/` holds the first (README, "Decided", 6).
- **Olsewski 1990's pedicle widths**, answered: they are the paper's Table II (p. 544), 21 cadaver spines (p. 543)
  measured directly, the sexes combined (p. 545), and Arockiaraj 2025's transcription is the one that differs. Its
  five values need no change; its cohort row does (item 4 below).
- **Robertson 2000's cohort columns**, answered: 10 dry-bone lumbosacral spines, wire-marked and radiographed
  coaxially, not 100 CT patients; the paper gives no origin, sex or age for them, and New Zealand is only where its
  authors worked. The series is Table 1's transverse width at the isthmus, the measure the table's
  header names; the paper's "isthmus diameter" row is the short axis of the pedicle's ellipse, which tilts 31 deg
  from the vertical at L4 and 55 deg at L5, so it is not a transverse width. `data/corrected/` corrects the cohort
  columns (README, "Decided", 1).
- **Yadav 2020, women, L3-L4 disc SD of 6.87** is four to five times its neighbours. Read from the page for #240: its
  Table 3 prints it (p. 178), and it stays (README, "Decided", 7).

**Not fixed upstream, because each would change a copied file:**
- The pedicle table's header still says twelve series; it has thirteen, as `data/corrected/`'s header says.
- `panjabi_reference.csv` still says the T11 and T12 end-plate widths exist only as a curve.
- The article's figure code labels "Otsuki 2020" and "Moncada-Habib 2023" have the wrong years (Irie 2021; 2025).

**No systematic search was ever run.** This is the collection gathered for one figure, not a review.

## What needs a person

1. **Read the 9 PMC-held papers still unread on PMC's site** and compare their values with `verification/values.csv`
   (filter `paper`). Yadav and Tan carry the most values (72 and 60). The links are in `SOURCES.md`. Griffith 2016,
   the tenth, was read from the page on 2026-10-28. Copies of all nine reached the project's files on 2026-10-28,
   outside git, after the reading; none was read for it.
2. **Done on 2026-10-28:** the values of the paywalled, secondary and unindexed papers were read from their own
   papers' pages, Twomey 1985, Alonge 2021, Ahmed 2019 and Chaudhary 2015 among them; Hinck's from Hinck 1966 itself,
   since Ahn 2001, which the level table cites for them, was not read; and Eisenstein 1977's five from his own Table
   I, the last paper Greg sent, as well as from Chaudhary's copy of them (item 3).
3. **Done on 2026-10-28: Eisenstein 1977 read from his own page.** Greg sent the paper (J Bone Joint Surg Br
   59-B(2):173-180, one author), and two readers not shown our values read its Table I (p. 174) and the counts of its
   first two pages apart from each other. The five values are his Table I's mean interpedicular widths (I.P.) of the
   Caucasoid men at L1 to L5, and Chaudhary's Table II copies them exactly, with his Caucasoid women's and his Zulu
   men's and women's rows, 20 means in all, and leaves out his Sotho rows. He measured 443 dry skeletons of the
   Raymond Dart Collection with a vernier caliper, the canal's width taken as the greatest interpedicular distance (p.
   173), so the modality column's dry bone, typed in `data/make_reference_table.py` (line 82) with no source given, is
   right, and Chaudhary's naming him among the workers who used plain radiography (p. 34) does not describe these
   values. The three decisions this left, his own Table I and primary, the Caucasoid men as the cohort, and n, were
   taken on 2026-10-28 (#240; README, "Decided", 5): n is 78, the Caucasoid men's skeletons (p. 173).
4. **Decided on 2026-10-28 (#240; README, "Decided", 1 to 4).** The four wrong cohort rows of the pedicle table are
   corrected; n is the count of the people a row's values are of, where the copy's sex-split series carry their whole
   sample in every sex's row (README, "What follows from the reading"); Yu holds Yu's own means and Mitra one method;
   and the women's rows that Ahmed, Chaudhary and Alonge print, and Hou's, Olsewski's and Robertson's SDs, are added.
   The eight sex-split series #239 did not read take their own counts, read for #240: Abbas 90 and 90, Amonoo-Kuofi
   1982 150 and 140, Amonoo-Kuofi 1985 79 and 43, Chen 43 and 40 (Table 3's 430 and 400 endplates, ten to a
   patient), Duman 277 and 240, Pierro 302 and 302, Masharawi 25 and 25, and van der Houwen a dash, since it measured
   25 patients of both sexes at each endplate; Eisenstein's Caucasoid women are added, 35 skeletons.
5. **Done for #240: Pierro 2017's Table 2 read from the page.** Its sagittal canal diameters (p. 4) hold none of
   the copy's twenty values at its level, sex and statistic, nor do its dural sac diameters (Table 4), and where the
   copy's came from is not recorded; `data/corrected/` holds Table 2 (README, "Decided", 8). Its Tables 3 and 5, vertebral body diameters
   and the dural sac ratio, are measures the tables do not carry, and were not taken.
6. **The two open data questions were decided on 2026-10-28** (#240; README, "Decided", 6 and 7): Cizmic's five
   canal-depth SDs, printed nowhere, become the SD over both sexes of its Table 5, and Yadav's 6.87 is what its Table
   3 prints and stays. What is left of this item is Greg's word: to make these corrections and those of items 3 to 5
   and of the four citations (README, "Decided", 9) in the public CTSpinoPelvic1K `morphometrics/`, as e887274 did
   for Panjabi, and re-copy here with
   `code/check_copies.py`. `code/apply_decisions.py` then stops, as it should, until each decision the new copy
   carries is taken out of it.

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
