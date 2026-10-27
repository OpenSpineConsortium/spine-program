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
| How far the series disagree | `python3 code/spread.py` | nothing |
| Write `sources.csv` and `SOURCES.md` | `python3 code/render_sources.py` | nothing |
| Draw every series | `python3 code/plot_series.py` | matplotlib |

On Windows the interpreter is `python`. `bash scripts/check.sh` at the repository root runs every step that needs no
network: the copies, the page reading, the spread, and whether the generated pages are current (`--check` on each).
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
   transcription of the same paper (8.2, 8.3, 10.1, 12.9, 18.2). The paper (JBJS Am, paywalled) decides; the table
   does not record where its values were read.
3. **Zindrick 1987's SD at L3** is 2.60 in the table, where Arockiaraj 2025's Table 3, whose Zindrick row holds all
   five of the series' means and the other four SDs, prints 2.61.
4. **Citations that do not match their papers** (`SOURCES.md` notes, generated from the resolver):
   - "Masharawi Y et al." is Abu-Leil S et al. (Masharawi a co-author), and article 1026, not 1023.
   - "Otsuki B et al." is Irie TY et al., and issue 7, not 6. The DOI built from the citation's article number
     resolves to Irie's paper, which fits the series (cadaveric micro-CT perpendicular to the pedicle axis); no Otsuki
     is among its authors.
   - "van der Houwen 2009" is printed 2010 (Ann Biomed Eng 38(1)); "Shin 2024" is printed 2025 (Brain Spine
     5:104162).

   The figure's labels use the resolved first authors.
5. **Robertson 2000's cohort columns are wrong.** The pedicle table says 100 CT patients from New Zealand; the paper's
   abstract describes cadaveric vertebrae marked with radiopaque material and imaged in the coaxial projection, and
   Bonczar's Table 1 lists it as radiographs of 10.
6. **Moncada-Habib 2025 is the left pedicle only.** Its Table 2 prints the left (LPW) and right (RPW) widths apart; the
   table carries LPW. The right differs by up to 0.6 mm.
7. **Yadav 2020, women, L3-L4 disc SD 6.87** is four to five times its neighbours (1.41, 1.65). The full text is not
   open here, so whether the paper prints it is not known.
8. **Stale text in the copied files.** The pedicle table's header says it has twelve series; it has thirteen.
   `panjabi_reference.csv` says the T11 and T12 end-plate widths exist only as a curve; Table 3 p. 892 prints them, and
   the generator has those values. The article's figure code labels "Otsuki 2020" and "Moncada-Habib 2023" carry the
   wrong years (Irie 2021; 2025).
9. **Not found anywhere**: Alonge 2021 (Afr J Med Med Sci), Ahmed 2019 (J Chalmeda Anand Rao Inst Med Sci) and
   Chaudhary 2015 (Int J Adv Res), in neither Crossref nor PubMed. Their citations are all there is, and Eisenstein
   1977's values were read through Chaudhary.
10. **Not checkable here**: every paper with neither open full text nor an abstract that prints the values, among them
    Tan 2004, Griffith 2016, Yadav 2020, Gilad 1985, Twomey 1985, Kunkel 2011, Tang 2016, Chen 2011 and both
    Amonoo-Kuofi papers; Hinck 1966, read through Ahn 2001; and the six secondary pedicle series whose transcribing
    paper is not named (Yu, Olsewski, Hou, Krag, Mitra, Robertson).

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
