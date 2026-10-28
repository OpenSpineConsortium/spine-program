# synthetic_spine: the published per-level vertebral morphometry series, with their papers

The published reference values that ostk's per-level morphometry was compared against in CTSpinoPelvic1K: Panjabi's,
and every other series that was collected. For each source this folder gives:
- the values themselves;
- the paper, with the citation as the tables give it and as the paper prints it;
- its DOI, PubMed and PMC links, and how each was found;
- what a check of each value against the paper itself found;
- the code that redoes each step.

Asked for by Greg on 2026-10-27 (spine-program #235). It is a collection, not a systematic review (below).
`HANDOFF.md` says what was attempted, what failed and why, and what is left for a person.

## Where these come from

The collection was built in CTSpinoPelvic1K on 2026-09-10 for Figure 6 of the dataset article, which overlays
CT-measured end-plate width, canal width and depth, and pedicle width on published values.
- c355e0a ("Thirteen published series, not one, and they disagree by 65%") added the pedicle-width table.
- a08c821 ("Every panel now carries its published range, and the ranges disagree") added the level table and its
  generator.
- 17e4434 and 770d463 cut the figure back to Panjabi alone. The figure code keeps the switch (`DRAW_SERIES` in
  `paper/mpda/make_levelatlas_fig.py`), and CTSpinoPelvic1K's `docs/NEXT_PAPER_REFERENCES.md` holds the multi-series
  comparison back for a paper of its own.

**There is no record of a systematic search.** The series were gathered by targeted reading, and no Scopus or PubMed
query, search date or inclusion rule was written down. To make this a review, the search has to be designed and run,
and its hits screened against these 42 papers.

## The numbers

| | rows | series | papers |
|---|---|---|---|
| `data/level_references.csv`: body heights, end-plate width, canal width and depth, disc height; T11 to L5 | 365 | 27 | 28 |
| `data/pedicle_width_references.csv`: transverse pedicle width, L1 to L5 | 65 | 13 | 13 |
| `data/panjabi_full_spine.csv`: Panjabi's three papers, C2 to L5 (06's bordercall reference) | 108 | 1 | 3 |

There are 42 papers in all (`sources.csv`). Panjabi 1992 supplies both of the first two tables, and two papers supply
no row of either: Ahn 2001, whose table Hinck 1966's values were read from, and Panjabi's cervical paper, which
supplies only the whole-spine table. Of the 42:
- 36 have a DOI;
- 39 have a PubMed id;
- 23 have a PMC copy; 13 of those are in PMC's open-access text subset, and 12 of those serve their
  tables as text (Pierro 2017's are images).

Three (Alonge 2021, Ahmed 2019, Chaudhary 2015) are found in neither Crossref nor PubMed.

| measure in the tables | what it is | source abbreviation |
|---|---|---|
| `h_ant` | anterior vertebral body height | VBHa |
| `h_post` | posterior vertebral body height | VBHp |
| `endplate` | upper end-plate transverse width | EPWu |
| `canal_w` | spinal canal width, interpedicular | SCW |
| `canal_ap` | spinal canal depth, midsagittal anteroposterior | SCD |
| `pedicle`, `PDW` | transverse pedicle width at the isthmus (Panjabi: mean of right and left) | PDW |
| `disc` | intervertebral disc height, by interspace (T12L1 ... L5S1) | - |

All values are in millimetres.

## Files

| path | what it is |
|---|---|
| `data/level_references.csv`, `data/make_reference_table.py` | The level table and its generator, which holds every value as a literal per series. |
| `data/pedicle_width_references.csv` | The pedicle table. It has no generator; its header explains the series. |
| `data/panjabi_reference.csv` | Panjabi 1992's lumbar Tables 2-4, as the article's figure draws them. |
| `data/panjabi_full_spine.csv`, `data/build_panjabi.py` | Panjabi's cervical, thoracic and lumbar tables, C2 to L5, and their builder, from 06. |
| `data/COPIED_FROM.csv`, `data/SHA256SUMS` | For every copied file: the repository, commit and path it came from, its git blob id and its SHA-256. |
| `data/series_papers.csv` | Which paper each series name in the tables belongs to, which paper its values were read from, and notes. |
| `sources.json`, `sources_raw/` | The identifiers resolved per paper, how each was found, whether year, issue and first page agree with the citation, and every raw answer from Crossref and NCBI (Crossref's copies of abstracts removed). |
| `sources.csv`, `SOURCES.md` | One row per paper, generated: what it supplies, its links, its full-text status, the check, and every disagreement between the tables' citation and the paper. |
| `verification/values.csv` | Every value against its paper: the result, and the table cell or the sentence that confirms it. |
| `verification/series.csv` | The same per series. |
| `verification/panjabi_page_reading.csv`, `verification/panjabi_page_reading_check.csv` | A blind reading of Panjabi's printed tables, and every Panjabi row here against it. |
| `verification/closed_page_reading.csv`, `verification/closed_page_reading_check.csv` | A blind reading of the tables of ten closed-access papers, and every value here from those papers against it. |
| `verification/spread.csv` | How far the series disagree, per measure and level. |
| `figures/series_by_level.png`, `.pdf` | Every series by level, one panel per measure. |
| `code/` | The scripts below. All but the plot are standard library only. |

The four files from CTSpinoPelvic1K are copied byte for byte from `morphometrics/` at commit e887274 (2026-10-27),
which corrected Panjabi 1992's posterior body height SEM at L1 to 1.03 (Table 2, p. 301), where every earlier commit had
0.92. The two from 06 are byte-identical to 06's own copies, which this pull request also corrects (the same SEM, a header
that said the cervical levels were absent, and a docstring that said no second reading checks them). `03_ctspinopelvic1k_dataset/mdpa/morphometrics/` keeps the
figure data as the article was built, with 0.92.

## How to redo each step (from `synthetic_spine/`)

| step | command | needs |
|---|---|---|
| The copies are the recorded bytes, and both generators still write their tables | `python3 code/check_copies.py [--against <CTSpinoPelvic1K clone>]` | nothing; the clone to prove the blobs |
| Resolve every paper to DOI, PubMed and PMC, keeping the raw answers | `python3 code/resolve_sources.py [paper ...]` | network (Crossref, NCBI) |
| Check every value against its paper, in context | `python3 code/verify_tables.py` | network on the first run (full texts and abstracts cached in `.cache/`, not committed) |
| Check Panjabi's values against the blind page reading | `python3 code/check_page_reading.py` | nothing |
| Check the closed-access papers' values against their blind page reading | `python3 code/check_closed_reading.py` | nothing |
| How far the series disagree | `python3 code/spread.py` | nothing |
| Write `sources.csv` and `SOURCES.md` | `python3 code/render_sources.py` | nothing |
| Draw every series | `python3 code/plot_series.py` | matplotlib |

On Windows the interpreter is `python`. `bash scripts/check.sh` at the repository root runs every step that needs no
network: the copies, the two page readings, the spread, and whether the generated pages are current (`--check` on
each).
Do not run a generator inside `data/`: Python's csv writer ends rows with CRLF and would rewrite a committed table;
`check_copies.py` runs both in a temporary folder.

To read a paper, use `SOURCES.md`.
- **A PMC link** opens the full text free to read.
- **A paper with no PMC link** is behind the publisher's paywall, at its DOI: through the library or interlibrary loan.
  Panjabi 1991 (thoracic) came that way on 2026-09-13; the scan Ovid serves skips its page 892.
- **The PDFs are not committed**, as they are the publishers' copyright. The laptop holds the Panjabi copies the page
  reading used: in `CTSpinoPelvic1K-1/`, `PANJABI_1991_FULL.pdf` and `PANJABI_1991_FULL_fixed.pdf` (thoracic, complete)
  and `cervical-human-vertebrae-quantitative-three-dimensional.pdf` (cervical); in `CTSpinoPelvic1K-1/MANUAL_REFS/`,
  `panjabi1991.pdf` (thoracic, without p. 892) and `panjabi1992.pdf` (lumbar).
  The ten closed-access papers read on 2026-10-28 came from Greg the same way, and are not committed either.

## Read before using a value

- **Dispersion is not interchangeable.** Each row names its type in `dispersion`; never draw an SEM as a spread.
  - Panjabi reports the SEM over twelve specimens; the SD is `sem * sqrt(12)`.
  - Bonczar reports a pooled meta-analytic SE.
  - Tan states SEM but defines it as SD/n, not SD/sqrt(n).
  - Bach prints a plus-or-minus it never defines (`unlabelled`).
  - Van der Houwen gives medians and no dispersion; Eisenstein and six secondary pedicle series give none.
- **Not every series is independent.**
  - Panjabi's 1991 thoracic and 1992 lumbar papers are one set of twelve spines.
  - Bonczar's meta-analysis pools 18 studies, among them Panjabi 1992, Tan (its Table 1 says 2003, n = 10) and
    Robertson 2000. Its Table 1 also gives Panjabi 1992 as "Asia, India, radiograph"; Panjabi measured at Yale with a
    three-dimensional digitiser.
  - The Zindrick and Makino rows agree with Arockiaraj 2025's Table 3, itself a compilation (below).
  - Kunkel's 2010 "prediction equations", widely cited, are a regression fitted to Panjabi's same spines. They are not
    in these tables. Kunkel 2011, which is, is a separate radiographic series.
- **Definitions differ under one name.**
  - End-plate depth as the maximum contour extent runs about 4 mm above the midsagittal chord.
  - Disc height from a recumbent radiograph runs about 6 mm above the same disc on CT.
  - Pedicle width endosteal (Makino) against outer cortical differs by about 5 mm at L5.
  - An axial pedicle reading overestimates one taken perpendicular to the axis by about 12%.
- **Primary and secondary are marked.** A secondary row was read from a later paper's comparison table and is
  provisional; for six of the thirteen pedicle series that later paper is not named.
- **The series disagree by 17 to 71% of their own median** (`verification/spread.csv`: largest minus smallest, over
  the median, at each level where three or more series report). By measure, with the most series at any level in
  brackets:

  | measure | spread |
  |---|---|
  | anterior body height (6) | 21-33% |
  | posterior body height (7) | 23-31% |
  | upper end-plate width (7) | 17-30% |
  | canal width (13) | 27-40% |
  | canal depth (12) | 35-54% |
  | disc height (5) | 28-71% |
  | pedicle width (13) | 61-69% |

## What the checks found (2026-10-27)

### How a value counts as confirmed

`code/verify_tables.py` reads each paper's full text from PMC where PMC serves it as text, and its PubMed abstract. A
value is confirmed only where the paper prints it **in context**:
- in a table cell whose row, column or section names the value's level, does not name the other sex, another species
  or another measure, and holds the number in the right role (the mean of a "mean +/- SD" cell, or its SD);
- or in a sentence of the text or the abstract that gives the number to the value's level, sex and role.

A cell that prints a mean together with its SD is preferred to one that prints the number alone, and exact matches
are looked for before rounded ones. `verification/values.csv` quotes the cell or the clause behind every confirmation,
so each one can be read by a person. One convention is declared per paper, with its evidence: Busscher lists each
disc under the vertebra above it (its C3 row has a disc height though the spines were dissected from C3, and it has
no S1 row).

### The counts

Of the 815 values (means and dispersions):
- **316 are confirmed in context**: 280 in a table (210 of them in the same cell as their partner), 31
  in a PubMed abstract and 5 in the running text. Every one is an exact match.
- **5 are not printed in the paper**: Cizmic's five canal-depth SDs (below).
- **None is found only out of context.**
- **494 cannot be checked by machine**: 389 because only the abstract is open and it does not print the
  value, 85 because neither the full text nor the abstract is open, and 20 because the paper's tables are
  images (Pierro 2017).

Fifteen series have values confirmed. Twelve are confirmed in full: Abbas, Arockiaraj, Bach (from its abstract),
Bonczar, Busscher, Duman, Li ("Front Physiol 2026"), Abu-Leil ("Masharawi"), Moncada-Habib, Irie ("Otsuki"), Shin
and van der Houwen. Cizmic and Makino (from its abstract) are confirmed in all their means, Mitra in two of its five.

**Panjabi, read from the page.** Panjabi's papers are scans with no text layer, so no machine reads them. A reader who
was not shown any table here transcribed his printed tables from the page images
(`verification/panjabi_page_reading.csv`: 138 cells of the cervical, thoracic and lumbar papers, each as printed, with
its table, page, PDF and page index). `code/check_page_reading.py` compares every Panjabi row in the four tables with
that reading, deriving pedicle width as the mean of right and left: all 173 agree, among them every row of 06's
whole-spine table, whose cervical and upper thoracic values had been read only once. The reading also records what the
papers print oddly: the thoracic text gives T1's posterior height as 14.3 mm where Tables 3 and 8 print 14.1; the
cervical PDWl SEM at C2 is printed 0.07, against 0.32 to 0.64 elsewhere; C2 prints a dash for the upper end plate and
posterior height.

**The closed-access papers, read from the page (2026-10-28).** Greg sent the PDFs of ten papers that have no open full
text (spine-program #238): the own papers of the seven secondary pedicle series, Hinck 1966, Tang 2016 and Bach 2019.
Readers who were not shown any table here transcribed, from the page images, every table these values could come
from (`verification/closed_page_reading.csv`: 4,943 rows, one per printed cell and statistic, each as printed, with
its table and pages). Each reader was told to read every table twice, from fresh crops, and to mark a cell whose two
reads differed as unclear. Five of the papers are typeset (Mitra, Robertson, Yu, Tang, Bach), and every number read
from their tables and text was also found on the publisher's own text layer; Bach's figures are pictures, so the
108 data labels read from them have none. `code/check_closed_reading.py` sets the 78 values these
papers carry beside the cells. Where a value differs, the script also holds the calculation, or the other paper's
table, that reproduces it, and fails if it stops doing so. Of the 78:
- **65 agree** with their own paper's cells. Tang's four agree once its centimetres are read as millimetres, and
  Bach's 24 are printed in its Results and abstract, not in a table.
- **13 do not, and each is reproduced by a calculation or by another paper's table:**
  - Mitra's L2 to L4 (3) are its CT means over all 20 cadavers, where its L1 and L5 are the men's direct means.
  - Krag's five are printed only in Yu 2015's comparison table, not in Krag's paper.
  - Yu's five are the midpoints of two of its age groups' means, not its overall means.

| series | what the paper measured | where the series' values are in it |
|---|---|---|
| Zindrick 1987 | post-mortem specimens, on radiographs of the disarticulated vertebrae and on CT; its counts are of studies (547 in Table 1), and it gives no count of specimens or people | Table 1, the transverse isthmus width (p. 161): all ten agree |
| Hou 1993 | 40 dry columns, T9 to L5, 25 male and 15 female, Chinese; Vernier caliper | Table 1, both sexes (p. 1852): all five agree |
| Olsewski 1990 | 21 embalmed cadaver spines, 12 men and 9 women, 41 or 42 pedicles per level; the paper's other parts are 49 cadavers and 51 patients | Table II, measured directly, sexes pooled (p. 544): all five agree |
| Mitra 2002 | 20 cadavers, 18 male and 2 female, Indian; measured directly and on CT | L1 and L5 are the men's direct means, as the abstract gives them; L2 to L4 are the CT means of all 20 (Table 1, p. 455) |
| Robertson 2000 | 10 dry-bone lumbosacral spines, 100 lumbar pedicles, wire-marked and radiographed coaxially, corrected for magnification | Table 1's left "Width" (p. 711): all five agree, but it is not the isthmus (below) |
| Krag 1988 | CT of 91 vertebrae of 41 living patients, 14 women and 27 men; 8 cadaver vertebrae sectioned to validate it | none: Krag prints no mean width; Yu 2015's Table 5 (p. 1645) prints the five under Krag's name |
| Yu 2015 | 503 dry skeletons of the Hamann-Todd collection, Cleveland, 404 male and 99 female; digital caliper, the two sides averaged | none as Yu's own, whose overall means are 8.52, 8.66, 10.46, 13.19 and 18.33 (Table 5, p. 1645); the five are midpoints of Table 3's age groups (p. 1642) |
| Hinck 1966 | 474 AP spine radiographs of white patients of the University of Oregon, taken for other reasons, 121 of them of adults; calipers on 40-inch films, no correction for magnification | Tables IA and II, adults over 18, sexes combined (pp. 142, 145): all ten agree, so Ahn 2001's copy is exact |
| Tang 2016 | T2-weighted 1.5 T MRI of 109 adults aged 20 to 40, 55 women and 54 men, from the University Hospital of the University of Utah, Salt Lake City; discs of Pfirrmann grade V left out with their end plates | Table 4's frontal diameter of the caudal end plate, all subjects, of the disc above each level (p. 4120): all four agree once its centimetres are read as millimetres |
| Bach 2019 | CT of 240 people scanned for complaints other than the spine at the University of South Florida, Tampa, 109 men and 131 women from their teens to their eighties (its age ranges disagree between abstract, methods and results); one neuroradiologist placed the points on 3D reconstructions | the Results' average disc height by sex (p. e108), which the abstract repeats: all 24 agree; Table 6 prints another average (below) |

What follows from the reading:
- **Part of the pedicle table's spread is definitional, not population.** Robertson's width is "the dimension from
  the most medial to lateral extent of the pedicle" on the coaxial view (p. 710); the narrowest diameter, the isthmus,
  is a separate row of the same table. At L5 the width is 21.6 mm and the isthmus 13.2 mm, so the pedicle table's
  header, which calls the New Zealand series high, compares a different measure. The table carries the left side
  only; whether that is the specimen's left or the reader's is not said.
- **One series mixes two methods.** Mitra's L1 and L5 are the men's direct means, 7.05 and 16.19, which the abstract
  quotes. L2 to L4 are CT means over all 20 cadavers: (18 x 7.59 + 2 x 6.15) / 20 = 7.446 at L2, and likewise 8.51
  and 9.709. The table's modality column says "direct".
- **Two secondary series hold values their own papers do not print.** Krag's five are in Yu 2015's Table 5, which
  says Krag measured on CT; the series was evidently read there, and how Yu came by them is not said. Yu's five (8.55,
  8.65, 10.43, 13.06, 18.03) are, at every level, the midpoint of Table 3's means for its youngest age group (30 years
  or less) and for 50 to 69 years: (8.41 + 8.68) / 2 = 8.545 at L1. From L1 to L4 those two are the lowest and highest
  of its four age groups, which fits the table's citation, "midpoint of published range". At L5 the oldest group's
  19.15 is higher still, so the same two groups were taken there too. The midpoint of two group means is not a mean
  of the 503 specimens.
- **Yu 2015's Table 5 holds Zindrick's, Olsewski's and Hou's values exactly as the pedicle table has them**, beside
  Krag's. That makes it the likeliest paper the table read those four from, though the three agree with their own
  papers too. Mitra's values in it (6.94, 7.72, 8.86, 11.37, 15.85) are not the table's, and Robertson is not in it.
- **The cohort columns are wrong in four pedicle rows.** Olsewski's "cadaveric + patients, 100" adds the paper's 49
  cadavers and 51 patients, but the values are 21 cadaver spines. Robertson's "patients New Zealand, 100, CT" is 10
  dry-bone spines on radiographs. Zindrick's "caliper" was radiographs and CT. Krag's "CT vs cut cadaver" was CT of
  living patients, with a sectioned-cadaver check of 8 vertebrae.
- **Three series print an SD the table leaves out:** Hou (1.2, 1.3, 1.6, 1.8, 2.7), Olsewski (2.3, 2.1, 2.5, 2.5, 3.7)
  and Robertson's left width (2.5, 3.0, 2.6, 3.7, 3.9), each at L1 to L5 (`sd_printed` in the check). Yu prints SDs
  only by group, not overall.
- **Hinck's canal widths are film distances.** They were measured on 40-inch anteroposterior films with no correction
  for magnification, as Chaudhary's row says of its own values ("uncorrected") and Hinck's does not.
- **Tang names an end plate by its disc, in centimetres.** The data's L4 upper end-plate width, 50.5 mm, is Tang's
  frontal diameter of the caudal end plate of the L3/L4 disc, 5.05 cm (Table 4, p. 4120). Its 109 subjects were 20
  to 40 years old, and its cells count 107 and 105 people, since discs of Pfirrmann grade V were left out with their
  end plates.
- **Bach's own Table 6 prints another average disc height.** The 24 values are the Results' and the abstract's
  average, the mean of the anterior, middle and posterior heights over all ages: Tables 2 and 3's decade rows of that
  mean, weighted by Table 1's counts, give them to their rounding (5.57 for men at T12/L1, printed 5.6; `note` in the
  check). Table 6, the paper's table of all ages by sex, prints an "Average disc height" 0.2 to 0.9 mm lower (5.02
  for men at T12/L1), which is the mean of its anterior and posterior rows alone. Figure 8, which the Results cite for
  the values, prints a third set (5.656725 for men at T12/L1). The Results do not say what their +/- is; pooled from
  the decade rows it is the size of an SD over all the people of one sex (1.10 for men at T12/L1, printed 1.1), not
  of an SE. The table's n of 240 counts both sexes in each sex's row: the men are 109 and the women 131. And 16 of
  the 240, 8 of each sex, are in the decade Table 1 labels 10, whose ages start at 14 by the abstract; the cohort
  column calls them all adults.

### Discrepancies

They are recorded here; the copied tables are left as their sources have them.

1. **Cizmic 2023's five canal-depth SDs** (1.66, 1.93, 1.95, 2.2, 2.71 at L1-L5) are printed nowhere in the paper,
   and a08c821, which added them, does not say where they came from. Its Tables 3 and 4 give a mean and a range for
   both sexes; its Table 5 gives SDs by sex; its text gives SDs for canal width only. Those canal-width SDs are the
   SD of the combined sample: computed from Table 5's per-sex means and SDs, it gives 2.298, 2.247, 2.373, 3.062 and
   4.006 against the printed 2.29, 2.24, 2.37, 3.06 and 4.00. The same calculation for canal depth gives 1.64, 1.98,
   2.00, 2.21 and 2.69, and the average of the two sexes' SDs gives 1.62, 1.92, 1.93, 2.19 and 2.70. Neither is the
   table's five.
2. **Olsewski 1990's pedicle widths** (8.20, 8.40, 10.20, 13.20, 20.10) disagree at L2 to L5 with Arockiaraj 2025's
   transcription of the same paper (8.2, 8.3, 10.1, 12.9, 18.2). Answered from the page (2026-10-28): the table's
   five are Olsewski's Table II, measured directly on 21 disarticulated cadaver spines, sexes pooled (p. 544).
   Arockiaraj's 8.3 at L2 is the same table's radiograph column, and its 10.1, 12.9 and 18.2 are in none of the
   paper's three tables.
3. **Zindrick 1987's SD at L3** is 2.60 in the table, where Arockiaraj 2025's Table 3, whose Zindrick row holds all
   five of the series' means and the other four SDs, prints 2.61. Answered from the page: Zindrick's Table 1 prints
   2.6 (p. 161), so the table agrees with the paper to its printed precision, and 2.61 is not what Zindrick prints.
4. **Citations that do not match their papers** (`SOURCES.md` notes, generated from the resolver):
   - "Masharawi Y et al." is Abu-Leil S et al. (Masharawi a co-author), and article 1026, not 1023.
   - "Otsuki B et al." is Irie TY et al., and issue 7, not 6. The DOI built from the citation's article number
     resolves to Irie's paper, which fits the series (cadaveric micro-CT perpendicular to the pedicle axis); no Otsuki
     is among its authors.
   - "van der Houwen 2009" is printed 2010 (Ann Biomed Eng 38(1)); "Shin 2024" is printed 2025 (Brain Spine
     5:104162).

   - Both Amonoo-Kuofi papers and Eisenstein 1977 have one author, as PubMed's records in `sources_raw/` show, but
     `SOURCES.md` writes "et al." after them: `code/render_sources.py` writes it after every first author.

   The figure's labels use the resolved first authors.
5. **Robertson 2000's cohort columns are wrong.** The pedicle table says 100 CT patients from New Zealand; the paper's
   abstract describes cadaveric vertebrae marked with radiopaque material and imaged in the coaxial projection, and
   Bonczar's Table 1 lists it as radiographs of 10. Answered from the page: 10 dry-bone lumbosacral spines, 100
   lumbar pedicles, each wrapped in wire, radiographed coaxially and corrected for magnification (pp. 709-710). The
   series is Table 1's left "Width", the pedicle's full medial-to-lateral extent, not its isthmus (above).
6. **Moncada-Habib 2025 is the left pedicle only.** Its Table 2 prints the left (LPW) and right (RPW) widths apart; the
   table carries LPW. The right differs by up to 0.6 mm.
7. **Yadav 2020, women, L3-L4 disc SD 6.87** is four to five times its neighbours (1.41, 1.65). The full text is not
   open here, so whether the paper prints it is not known.
8. **Stale text in the copied files.** The pedicle table's header says it has twelve series; it has thirteen.
   `panjabi_reference.csv` says the T11 and T12 end-plate widths exist only as a curve; Table 3 p. 892 prints them, and
   the generator has those values. The article's figure code labels "Otsuki 2020" and "Moncada-Habib 2023" carry the
   wrong years (Irie 2021; 2025).
9. **Not indexed**: Alonge 2021, Ahmed 2019 and Chaudhary 2015 are in neither Crossref nor PubMed, but each is open
   on its journal's own site (2026-10-28):
   - Alonge OJ, Adeolu AA, Omololu AB, Atalabi OM, "Lumbar spinal canal dimensions in Nigerians using computed
     tomography scan", Afr J Med Med Sci 50(2), June 2021, pp. 69-76:
     https://www.ojshostng.com/index.php/ajmms/en/article/view/1782
   - Ahmed MA, Aditya M, Anitha T, Sailaja TK, "Radiological anatomy of the lumbar canal: a MRI study", J Chalmeda
     Anand Rao Inst Med Sci 17(1), 2019, pp. 21-26 as its pages print them, not 21-27:
     https://caims.in/assets/journal/2019_1/CAIMS%20JOURNAL___05.pdf
   - Chaudhary S, Sarvesh, Batra APS, Gupta R, Swami S, "A radiographic study of interpedicular distance of the
     lumbar vertebrae measured in plain antero-posterior radiographs", Int J Adv Res 3(8), 2015, pp. 33-36:
     https://www.journalijar.com/uploads/2015/08/684_IJAR-4961.pdf

   None was read here, since the proxy of the session that wrote this refuses those sites to scripts. Eisenstein
   1977's values were read through Chaudhary.
10. **Not checkable here**: every paper with neither open full text nor an abstract that prints the values: Tan
    2004, Griffith 2016, Yadav 2020, Gilad 1985, Twomey 1985, Kunkel 2011, Chen 2011 and both Amonoo-Kuofi papers.
    Twomey 1985 is free in Acta Orthopaedica's archive (https://actaorthop.org/actao/article/view/23300, which
    gives Twomey L, Taylor J, 56(6):496-499), behind the same refusal. Hinck 1966, Tang 2016, Bach 2019 and the
    seven secondary pedicle series were checked against their own papers from the page instead (above).

### What the resolver does, and what it found

Every DOI the tables lack is either found by a Crossref query whose candidate agrees with the citation on author,
year, journal and first page, or pinned in `code/resolve_sources.py` with where it came from: the header of a copied
file (Panjabi), the citation's article number in the journal's DOI pattern (Frontiers, PLoS One), or a stated reason
(Bonczar, Abbas: the query returned another paper; Masharawi: the citation's article number is wrong, so the page
test refuses the right record). Europe PMC answered 503 to every request on 2026-10-27 while this was written, so NCBI
is used; each run asks Europe PMC once and keeps its answer in `sources_raw/_europepmc_probe.json`.

## Not in this folder

- CT-measured values: ostk's per-level morphometry stays in CTSpinoPelvic1K's `morphometrics/`. Its
  `paper/mpda/make_levelatlas_fig.py` with `DRAW_SERIES = None` overlays every series on the dataset's own
  distributions again.
- The papers' PDFs and full texts (copyright). `.cache/` holds what the checker downloads and is not committed.
