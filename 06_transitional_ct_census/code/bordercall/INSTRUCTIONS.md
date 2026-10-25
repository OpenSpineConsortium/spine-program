# bordercall — how to run this on your corpus

Naming a vertebral border from the shape of the bone, with no count from C2. Self-contained:
label volumes in, numbers and conference figures out. Nothing here reads a CTSpinoPelvic1K
table.

## What you need

- Python 3.9+, with `numpy`, `scipy`, `nibabel`, `matplotlib`. Nothing else; the model is a
  logistic regression written out rather than a library call.
- A directory of segmented label volumes, `*.nii.gz`, one per case, each carrying vertebrae
  as integer identifiers. Ribs as well if you want the phenotype classes.
- No CT. Everything is measured off the labels.

## Run it

```bash
cd 06_transitional_ct_census/code/bordercall

# 1. Is the identifier map right for this corpus?  NOT OPTIONAL.
python run.py scheme --labels /path/to/labels

# 2. Does this copy of the code still reproduce the published answer?  NOT OPTIONAL.
python run.py selftest --levels ../../../03_ctspinopelvic1k_dataset/mdpa/morphometrics/level_gradients.csv

# 3. Everything else
python run.py all --labels /path/to/labels --outdir out/
```

`all` runs measure → phenotype → border → breakout → figures. The pieces, if you want them
one at a time:

```bash
python run.py measure   --labels LABELS --out levels.csv      # geometry, the slow step
python run.py phenotype --labels LABELS --out phenotype.csv   # ribs and counts
python run.py border    --levels levels.csv --above T12 --below L1
python run.py breakout  --levels levels.csv --phenotype phenotype.csv
python run.py plot      --levels levels.csv --phenotype phenotype.csv --measure endplate
```

Any adjacent pair works: `--above C7 --below T1`, `--above L5 --below L6`. Narrow what gets
measured with `BORDERCALL_LEVELS=T11,T12,L1,L2,L3,L4,L5` in front of `measure`.

## The two commands you must not skip, and why

**`scheme`** prints the identifiers actually in your volumes against the map in `scheme.py`
and stops if they disagree. A wrong map does not raise. It returns a finite, plausible,
wrong number: this programme once shipped a release whose pelvic incidence was computed
against a legacy map, and the only symptom was a quality flag reporting too few voxels in a
structure that was plainly there. On its first real run this check found that the local
CTSpinoPelvic1K deposit still carries identifier 29, the carved S1 that v11 retired, meaning
those volumes are v10. If `scheme` complains, edit `scheme.py` and nothing else.

**`selftest`** re-derives three published CTSpinoPelvic1K numbers from the released table —
adjacent-pair AUC 0.988, whole-span 0.998, junction placement 95.1% — and fails if any has
moved by more than 0.004. It takes seconds and it is the only thing standing between you and
a silently changed model.

## Reading the output

`border` gives one number for the corpus. **It will mislead you on its own.** On
CTSpinoPelvic1K the corpus figure is 95%, and broken out by phenotype:

| Class | In field | Correct | |
|---|---|---|---|
| Rib on a lumbar body | 14 | 4 | **28.6%** |
| No rib on the last thoracic | 10 | 5 | **50.0%** |
| Six lumbar vertebrae | 18 | 16 | 88.9% |
| Four lumbar identifiers | 10 | 10 | 100% |
| Typical column | 656 | 638 | 97.3% |

Two populations averaged together. Always run `breakout`, and read a class of fewer than
about twenty cases as "no failures seen" rather than as an accuracy.

Expect the same shape of answer at any border: the classes that break it are the ones whose
anomaly sits *at that border*. The lumbosacral classes barely move a thoracolumbar
classifier, and they should not.

## The figures

`plot` writes a PDF and a PNG side by side. **Use the PDF in a slide or a poster**: it is
vector, its text stays text (`pdf.fonttype 42`), and it will not blur on a projector.

Two figures per measure:

- `levels_<measure>` — every case, one violin per level, with the published reference
  interval over it. What the corpus looks like.
- `classes_<measure>` — one panel per phenotype over the typical column in grey. Where the
  method succeeds and where it fails, with the per-class accuracy printed in each title.

Conventions, all deliberate:

- **Vertebral body class on the y axis, cranial at the top; the measurement on the x axis.**
  This is the axis order of the morphometry plates a spine audience has read for thirty
  years. Keep it and a surgeon reads the figure without being taught the plot first.
- Anomalous classes are drawn as **points, not violins**, below `--violin-min` (40). A violin
  over fourteen cases draws a density through almost nothing.
- The reference band is a **population interval**, mean ± 1.96 SD, with the SD recovered from
  the published standard error as `sem*sqrt(n)`. The SEM band would be √n times too narrow
  and would make any cohort look aberrant for a reason that is arithmetic, not anatomical.
- `--scale 1.3` for a poster. `--measure` takes `endplate`, `h_ant`, `h_post`, `canal_w`,
  `tp_span`.

## The reference table

`reference/panjabi_full_spine.csv`, used by default. Built by `reference/build_panjabi.py`
from the printed tables of

- Panjabi et al., *Thoracic human vertebrae*, Spine 1991;16(8):888–901 — T1–T12
- Panjabi et al., *Human lumbar vertebrae*, Spine 1992;17(3):299–306 — L1–L5

for `endplate`, `h_post`, `canal_w`, `canal_ap` and `pedicle`. Pages 892 and 894 are image
only in the publisher's scan, so those tables were read from the page images; the build
script re-checks its T11/T12 values against an earlier independent transcription and fails
if any disagrees.

**There is no cervical reference yet.** The companion paper —

> Panjabi MM, Duranceau J, Goel V, Oxland T, Takata K. Cervical human vertebrae. Quantitative
> three-dimensional anatomy of the middle and lower regions. *Spine* 1991;16(8):861–869.
> PMID 1948369, doi:10.1097/00007632-199108000-00001

— is in the **same journal issue as the thoracic paper**, 27 pages earlier, and is closed
access. Get it the same way the thoracic one was got, read Tables 3–5 off the page images,
and add the rows to `build_panjabi.py`. Until then a cervical border simply has no interval
drawn, which is the right failure: no line rather than a wrong one.

Supply your own table with `--reference FILE`, columns `measure, level, mean, sem, n`
(or `sd` instead of `sem`). `--no-reference` draws none.

## Traps

1. **The identifier map is assumed, not detected.** Above, and first for a reason.
2. **Only the lumbar measurements are validated.** End-plate width, canal width and
   transverse-process span were checked against published lumbar norms. The original
   measurement code says in as many words that those comparisons *do not transfer to
   thoracic levels*; only the height and wedge columns are meant to be used above L1.
   Widening the identifier range makes the code run over a whole spine. It does not make the
   numbers validated there. Check each measure at your levels against a published series
   before quoting anything; until then a cervical or upper-thoracic result is a pipeline
   test, not a finding.
3. **The last lumbar level is withheld for end-plate and pedicle width.** The body is
   isolated by cutting at the anterior wall of the canal, and at the last lumbar level the
   transverse processes arise in front of that cut, so the cut keeps them. This is a property
   of the measurement and travels with the code to any corpus. `--no-withhold` overrides it.
4. **The per-case normalisation is the whole method.** Every measure is divided by that
   case's own median across its levels, plus ratios that carry no size at all. Lumbar
   vertebrae are simply bigger than thoracic ones; a classifier given raw millimetres learns
   size and reports a high AUC that says nothing about the border, where the two neighbours
   are nearly the same size.
5. **Folds are grouped by case.** Two vertebrae from one patient are not independent. Keep
   any new split grouped or everything inflates.

## If your corpus has C2

Then it can answer what CTSpinoPelvic1K could not. A rib on L1 may be a thirteenth thoracic
vertebra above five lumbar ones, or a rudimentary rib on a true L1 — different columns, the
same rib, and only a count from C2 separates them. Add the true count as a column and ask: of
the cases where shape and name disagree, how many are *counted* anomalies? That is the single
most valuable thing a whole-spine corpus can do here.

A warning about how to test it. Relabelling the disagreements to the model's own prediction
and re-scoring is circular — the AUC must rise, because the target has moved to where the
model already points. On CTSpinoPelvic1K that circular arm reached 0.9998 against a baseline
of 0.9880, while relabelling by an *independent* criterion (the ribs, which are not among the
features) reached 0.9916, about a third of the way. Always put the circular arm beside the
honest one, or the honest one reads as larger than it is.

## Files

| File | What it is |
|---|---|
| `run.py` | the CLI: `scheme`, `selftest`, `measure`, `phenotype`, `border`, `breakout`, `plot`, `all` |
| `scheme.py` | the identifier map, in one place, with the check |
| `measure_levels.py` | label volumes → wide per-level table |
| `phenotype.py` | label volumes → per-case phenotype, from the labels alone |
| `border.py` | features, grouped-CV logistic regression, border evaluation |
| `plots.py` | the two conference figures |
| `reference/` | the Panjabi tables and the script that builds them |
| `render_anchors.py`, `render_turntable.py`, `label_scheme.py` | the 3-D phenotype gallery |
| `HANDOFF.md` | the shorter version of this, with what the method already found |
