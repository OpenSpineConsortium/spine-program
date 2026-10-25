# mdpa: the dataset article and the data its figures are made from

The *Medical Physics* Dataset and Software article for CT Spinopelvic One-thousand, with every
table its figures read, so a figure can be rebuilt or replotted for a talk without the private
`CTSpinoPelvic1K` working repository. Brought in under issue #226.

This is a real folder. `../figures/`, `../manuscripts/` and `../results/` beside it are symlinks
to `/rs/rs_grp_oschome/shared/spine-program/archive/` and resolve only on the grid (#87); nothing
here depends on them.

```
paper/mpda/            the LaTeX of the submitted article, the build scripts, the figure scripts
paper/mpda/figures/    the built figure PDFs and PNGs
scripts/               the extraction scripts, the separability test, the violin script
morphometrics/         every table the figures read, copied as it stands
dist/submission/       the journal packet as uploaded, with the abstract as plain text
talk_figures/          output of the violin script; not article figures
```

**The layout mirrors the source repository on purpose.** Each script anchors its data path on its
own location (`Path(__file__).resolve().parents[2] / "morphometrics"` in `make_levelatlas_fig.py`,
`parents[1]` in `select_anchor_cases.py`). `mdpa/` therefore stands in for the repository root, so
every script runs unchanged and a later re-sync from `CTSpinoPelvic1K` is a plain copy rather than
a re-patch. Run each script from its own directory.

## Which file makes which figure

| Figure | Script | Reads |
|---|---|---|
| 1 pipeline | drawn in TikZ inside `paper/mpda/main.tex` | — |
| 2 anchors | `scripts/make_fig_anchors.py` | `morphometrics/transition_morphometrics.csv`, `anchor_cases.json` |
| 3 hardware | `scripts/render_hardware_gallery.py` | `morphometrics/metal.csv` + the label volumes |
| 4 validation | `paper/mpda/make_figures.py` | `morphometrics/surgical_morphometrics.csv` |
| 5 level atlas | `paper/mpda/make_levelatlas_fig.py` | `morphometrics/level_atlas.csv`, `panjabi_reference.csv` |
| 6 field of view | `paper/mpda/make_fov_fig.py` | `morphometrics/label_census_v7.csv` |

Figures 2 and 3 need the CT and label volumes and only rebuild on the grid. Figures 4, 5 and 6
rebuild from `morphometrics/` alone; 5 and 6 were run here to check that.

## The thoracolumbar transition as violins

```
cd scripts
python plot_thoracolumbar_violins.py                    # end-plate width
python plot_thoracolumbar_violins.py --measure canal_w
python plot_thoracolumbar_violins.py --measure h_post
```

Left panel, one violin per ground-truth level with Panjabi's cadaveric interval over it; right
panel, the same vertebrae scored by the article's classifier, so the transition is visible as the
model places it. `--measure` takes `endplate`, `canal_w`, `h_post`, `h_ant` or `tp_span`; Panjabi
covers the first three. Images land in `talk_figures/`.

**`level_atlas.csv` cannot draw a violin.** It holds summary statistics per level (median,
quartiles, 5th and 95th percentile) and is what published Figure 5 draws. The distributions are in
**`level_gradients.csv`**: one row per case, 802 of them, with per-level columns for T11, T12 and
L1–L5 (`endplate_width_L1_mm`, `canal_width_L1_mm`, `body_height_L1_mm`,
`body_height_post_L1_mm`, `tp_span_L1_mm`, `wedge_ratio_L1`). Canal depth and pedicle width are
per level in `surgical_morphometrics.csv` instead (`canal_ap_mm_L1`, `pedicle_mm_L1`).

`panjabi_reference.csv` holds the cadaveric means with their standard error, each row naming the
table and page it was read from. The **standard error, not the SD**: the population SD is
`sem * sqrt(12)`, and drawing the SEM band instead gives an interval 3.5x too narrow that makes
this cohort look aberrant for a reason that is arithmetic rather than anatomy. T11 and T12
end-plate width are not in his table at all; `paper/mpda/tools/digitize_panjabi_fig4a.py` recovers
them from his Figure 4A and records why that curve is not attributable to him alone.

**L5 is withheld for end-plate and pedicle width.** Both are measured on a body isolated by cutting
at the anterior wall of the canal, and at L5 the transverse processes arise in front of that wall,
so the cut keeps them: the L5 median runs about 2 mm wide with an SD 1.58x the levels above. Three
separation rules were built and run over all 802 records and none beat the one that ships. The
violin script drops the level and says so on the panel.

## The separation the article reports

```
cd scripts
python test_morphometric_separability.py --levels ../morphometrics/level_gradients.csv
```

Features are each measure divided by that patient's own median across their levels, plus ratios
between measures, so patient size is removed and only shape is left. Folds are grouped by case.
Two numbers come out and they answer different questions:

- **T12 versus L1, AUC 0.990 over 1,486 vertebrae.** The adjacent pair, and the one the article
  quotes, because that is the boundary a reader actually has to call. Reproduced here on
  2026-10-25.
- **T11/T12 versus all of L1–L5, AUC 0.998.** What the violin script prints, since it scores every
  level. Easier, because it includes levels far from the boundary; not a reproduction of the 0.990
  and not quotable as one.

## Handoff: how the violin plots came about, and how the transition performs

### How they came about

Asked for on 2026-10-25, for a talk: the thoracolumbar transition as violins with ground-truth
vertebral class on the y axis and Panjabi's reference over the morphometry. Two claims were
made while building them and both were false; they are written down because each would have
put a wrong number on a slide.

1. *"`level_atlas.csv` has the data."* It does not. It is summary statistics per level and
   draws published Figure 5. Violins need `level_gradients.csv`, one row per case.
2. *"The violin script reproduces the article's AUC."* It does not. It prints **0.998**, which
   is T11/T12 against all of L1–L5. The article's **0.990** is the adjacent T12-versus-L1 pair
   over 1,486 vertebrae. Quoting 0.998 as the paper's number would overstate it.

### Where the classifier puts the junction

`scripts/junction_vs_labels.py`, out of fold, folds grouped by case. Of 798 cases scored, 713
have both T12 and L1 in the field of view, and 712 of those give a clean top-down run of
thoracic calls.

| predicted junction | cases | share |
|---|---|---|
| at the labelled T12/L1 interspace | 677 | **95.1%** |
| one level caudal (L1 called thoracic) | 28 | 3.9% |
| one level cranial (T12 called lumbar) | 7 | 1.0% |

Per vertebra: T11 called thoracic 99.9%, T12 98.7%, L1 4.3%, L2 0.1%. The two vertebrae either
side of the predicted point are T12 and L1 in 677 cases, L1 and L2 in 27, T11 and T12 in 7.

### How it performs at predicting anomalies

Two tests, both independent of the name the reader gave the border vertebra.

**By the count down to the sacrum.** Five is the usual count. The labels' own count calls 28 of
712 anomalous; the predicted junction calls 61. They agree on 27. So the predicted count adds 34
records the labels' count does not call, and most of those are not recorded anomalies — as a
standalone detector by count it is noisy.

**By the ribs**, which the classifier never sees: its features are body and canal measures, no
rib among them. The lowest rib-bearing vertebra is T12 in the usual column.

| offset | lowest rib-bearing | cases | reading |
|---|---|---|---|
| −1 | T11 | 5 | T12 bears no rib, so it looks lumbar |
| −1 | T12 | 2 | |
| 0 | T12 | 668 | |
| 0 | T11 or L1 | 9 | anomaly the shape did not show |
| +1 | L1 | 10 | L1 bears a rib, so it looks thoracic |
| +1 | T12 | 18 | |

Against that criterion: **sensitivity 62.5%** (15 of 24 rib-anomalous cases disagree),
**specificity 97.0%** (21 of 689 rib-normal cases disagree), **precision 41.7%** (15 of 36
disagreements are rib-anomalous).

**The direction is the part worth trusting.** Every disagreement runs the way the rib does: a
vertebra carrying a rib is called thoracic, one without is called lumbar. Of the 14 cases whose
lowest rib-bearing vertebra is L1, ten are called one level caudal and in every one the vertebra
called thoracic is the L1 carrying the rib (`P(thoracic)` 0.54 to 0.99). None run the other way.
A rate alone could not tell that from noise.

**What this is not.** The classifier is trained on these labels, so it cannot find an anomaly the
labels do not already encode; a disagreement says only that the vertebra's shape is atypical for
the name it carries. The lumbosacral flags behave as they should for a thoracolumbar classifier
and barely move: L6 11.1%, LSTV 12.5%, Castellvi 12.5%, against 3.6% for records with no flag.
Whether the 21 rib-normal disagreements are false positives or unrecorded thoracolumbar variants
is **not known**: no record in this release carries a T13, and thoracic ground truth is
field-of-view limited.

### Accuracy by anomaly class

`scripts/anomaly_classes.py` assigns each case ONE class, most specific first, so the groups are
disjoint and the thoracolumbar phenotypes are tested before the lumbosacral ones. A case can
carry both, and the order is stated rather than left to the reader.

| Class | Corpus | In field | Junction correct | |
|---|---|---|---|---|
| Rib on a lumbar body (L1) | 19 | 14 | 4 | **28.6%** |
| No rib on T12 | 13 | 10 | 5 | **50.0%** |
| Six lumbar vertebrae (L6) | 18 | 18 | 16 | 88.9% |
| Four lumbar identifiers | 10 | 10 | 10 | 100% |
| Castellvi grade, usual count | 5 | 5 | 4 | 80% |
| Typical column | 737 | 656 | 638 | 97.3% |
| **All** | 802 | 713 | 677 | **95.0%** |

The two thoracolumbar classes are the only ones that break it, and they break it badly. The
lumbosacral classes sit at or near the typical column, which is what a thoracolumbar classifier
should do: an L6 or a Castellvi grade changes the bottom of the column, not the T12/L1 border.
`four_lumbar` scoring 100% is on ten cases and should be read as "no failures seen", not as a
better result than `typical`.

`talk_figures/anomaly_benzel_<measure>.png` plots this the way the textbook plates read:
vertebral body class on the y axis, the measurement on the x axis, one panel per class. The
typical column is the same grey distribution behind every panel so a class is read against it
rather than against its neighbour, and each anomalous case is a point, because a violin over
n=14 would imply a density the data cannot support.

`talk_figures/anomaly_renders.png` is the same six classes as real 3-D renders of the released
label volumes (`scripts/render_anchors.py`), one exemplar each, chosen as the most ordinary
member of its class. Red is the lowest rib-bearing vertebra with its rib, yellow the lumbar
bodies, blue the sacrum. Colour is by ROLE, not by identifier: in a lumbar-rib case the red
vertebra sits a level lower than usual, and colouring T12 specifically would assert the count
the figure is supposed to be deriving.

### Are the failures simply mislabelled?

`scripts/test_relabel_hypothesis.py`. No scan here contains C2, so the border vertebra's name
is a reader's call. If the reader is wrong where the shape disagrees, the failures are theirs
and relabelling should fit better. Three arms, each retrained from scratch and scored out of
fold:

| Labels | Whole span AUC | T12/L1 pair AUC | Vertebrae moved |
|---|---|---|---|
| reader, as released | 0.9981 | 0.9880 | — |
| **rib-defined border** | **0.9986** | **0.9916** | 26 of 5,233 |
| model's own call | 1.0000 | 0.9998 | 44 |

**The third arm is circular and is in there as a control.** Relabel every disagreement to the
model's own prediction and the score must rise: the target has been moved to where the model
already points. Run alone it would look like a result. It is the scale against which the
honest arm is read.

The honest arm moves the border using the **ribs**, which are not among the features. It moves
26 vertebrae — 16 where L1 bears a rib, 10 where T12 bears none — and recovers roughly a third
of the circular arm's gain at the adjacent pair (+0.0036 against +0.0118).

So the answer is partly yes: the shape fits the rib-defined border better than the reader's
name, and that is evidence rather than a restatement because the rib is independent of every
feature. But most of the remaining disagreement is **not** explained by mislabelling.

What this still cannot settle: a rib on L1 may be a thirteenth thoracic vertebra above five
lumbar ones, or a rudimentary rib on a true L1. Different columns, same rib, and only a count
from C2 separates them.

### The T12/L1 disc space

`scripts/measure_t12l1_disc.py`. The release ships disc heights for L1L2 down to L5S1 and nothing
at T12/L1, so the junction had no measured ground truth and the labelled name was standing in for
one. The disc is the gap between the inferior surface of T12 (19) and the superior surface of L1
(20), and both are in the label volumes, so it is measured rather than assumed. It is independent
of the classifier, whose features contain no disc height.

The method is `extract_degenerative.py`'s, not a new one: per column through the overlap of the
two bodies, then the median. End-plates are concave, so a rim-to-rim gap reads 4 to 6 mm against a
published lumbar 8 to 12. The same run recomputes L1L2 as a control, and **reproduced
`degenerative.csv` exactly** on the records checked (100% identical, largest difference 0.0 mm),
which is what licenses the T12L1 column beside it.

## Rebuilding the article

`paper/mpda/build.sh` compiles it; `build.sh --reprint` is the only thing that measures the
published page count, which the journal caps at ten. `paper/mpda/REPRODUCE.md` is the pipeline end
to end and the traps in it. The abstract is deliberately **not** in the main document: a Dataset
and Software article carries it in the submission form instead, from
`dist/submission/Abstract.txt`, and the submission was returned once for carrying one.

## Not here

The co-author `.docx` drafts, the `_schehr` / `_upd` / `_others` revision working copies and the
duplicate preview PDFs stay in the `CTSpinoPelvic1K` repository; they are 48 of that directory's
53 MB and nothing here reads them. The CT and label volumes are on the grid and on Zenodo; the release this article describes
is v11.
