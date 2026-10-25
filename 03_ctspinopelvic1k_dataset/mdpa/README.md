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
