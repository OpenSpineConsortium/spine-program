# Transitional gallery -- what was looked at, what was chosen, what is still owed

Figure file: `SchwingNet/figures/fig_transitional_gallery.{pdf,tif,png}` (183 x 223.8 mm; TIF 2,161 x 2,643 px, RGB, LZW,
300 dpi in the header; PDF with the 15 cells as rasters and every label as live text). Legend sidecar
`fig_transitional_gallery.caption.txt`, 59 words, four components (a)-(d), the same text `main.tex` carries at
`\label{fig:gallery}`. Sources of every cell: `GALLERY_SOURCES.md` (same folder). Spec: `gallery_spec.json`; facts:
`panel_facts.json`; the fourteen rendered panel sets stayed on the grid under `/rs/rs_grp_oschome/go2432/data/gallery/v2/`
(grid job 40416670, `slurm/gallery_panels.sh`, 4.5 min); the picked cells are mirrored in `panels/`.

## Every panel was looked at

Contact sheets of all 128 rendered PNGs (15 per CT case: labelled surface, CT slice with outlines, plain render, four
device cards x three seeds; one per real frame or film), each with its marker box drawn, and the composed figure at
full resolution, twice (before and after the layout fixes). What the looking decided:

| cell | choice | why |
|---|---|---|
| (a) labelled CT | sagittal slice of CTSpinoPelvic1K 0244 with the label outlines, L6 in the accent colour | six bodies and their discs count on a slice; the lateral surface hides the sacrum behind the ala |
| (b) labelled CT | AP bone surface of VerSe verse547, T13 in the accent colour | the rib-bearing body is a three-dimensional feature; the coronal slice through the centroid showed neither rib head |
| (c) labelled CT | AP bone surface of CTSpinoPelvic1K 0008, L5 in the accent colour | the transverse processes fused to the ala (Castellvi IV) are seen from the front |
| (d) labelled CT | sagittal slice of CTSpinoPelvic1K 0760 with the outlines | the fused body has no label of its own (it is inside the sacrum label, `inside_sacrum`), so a slice shows the body and the obliterated disc under L4 |
| plain render, all rows | the corpus's own definition (bone above 150 HU, `make_drr_dataset.HU_FLOOR`) | the image the level model trains on; the soft-tissue projection of the first attempt showed the spine poorly |
| device-card render, all rows | Cios Fusion card, seed 11 | of the four released cards x three seeds, the Cios Fusion draws showed the column and the discs most often; seed 11 was the most legible of its three in every row |
| (a) radiograph | BUU-LSPINE 2580-F-031Y1 | adult, no burned-in text in the crop; 3496-F-061Y1 carries "RT", 4200-M-025Y1 a letter at the bottom; the seven films of subjects under 15 y were not considered |
| (d) radiograph | BUU-LSPINE 0233-F-064Y1 | adult, clean; 0006-F-031Y1 has a bright block beside the spine |
| (a) real C-arm | C-ArmLSpine case136, lateral, release test split | clean lateral; case121's frame carries a bright plate at the top; case42 is the validation split |

Alternates rendered and kept on the grid: 0565 (L6), verse588 (T13), 0021 (sacralised L5), 0151 (four lumbar),
case42, 3483-F-062Y1, 0271-F-062Y1.

## The marker

One arrow in every cell, from panel_facts.json boxes, never placed by hand: on a lateral view the tip touches the
anterior edge of the transitional vertebra's projected label box; on an AP view the label box spans both transverse
processes, so the tip goes 0.3 of the box width in, at the lateral edge of the body. Four rules for where the box
comes from:

- CT rows: the projected box of the label (25 = L6, 28 = T13, 24 = L5); for the four-lumbar case the fused body has
  no label, so the box is the upper 30 mm of the sacrum label (26).
- C-ArmLSpine: the box of the body TotalSegmentator names L5 and SPINEPS+VERIDAH names L6 (`carmlspine/levels.json`:
  the two labellers segment the same six bodies at Dice 0.93-0.95 and disagree on every name by one; no reader has
  looked; "L6" here is a naming convention of a lumbar-only cone-beam CT with no rib to count from, and the cell says
  "automatic read, no reader").
- BUU-LSPINE: the body between the shipped L5a and L5b corner rows. Established by looking at the films, not assumed:
  on every six-lumbar film the sacrum follows the S1a row directly (L5b-to-S1a gap 4.6-11.4 mm on the six read,
  a normal disc), so the shipped rows label the five lowest bodies and the body under the L5 rows is the sixth
  lumbar body, the one above the sacrum; on the four-lumbar films the L5b-to-S1a gap is 1.7-2.9 mm (five read), a
  fused disc, so the body under the L5 rows is the sacralised one. The gap of each used film is in GALLERY_SOURCES.md.

## Scale bars

20 mm in every image cell. CT cells: 0.25 mm/px after resampling from the native voxel pitch recorded per case
(0.78 x 0.80 mm CTSpinoPelvic1K, 0.92 x 0.90 mm VerSe), an upsample for display that adds nothing. C-ArmLSpine:
0.1915 mm/px, the detector pitch scaled to the isocentre (0.293 x 745 / 1140, from the frame meta). BUU-LSPINE:
0.175 mm (2580) and 0.140 mm (0233) from the dataset report's "Pixel Spacing" sheet.

## Truth, and where it is weaker than a reader

- CTSpinoPelvic1K: v11 release labels (identifier 29 asserted absent) plus the adjudicated Castellvi read in
  `results/rare_class/transitional_subtypes.csv`; the label file of each case is named in GALLERY_SOURCES.md.
- VerSe: raw mask identifier 28 in `~/VerSeFusion/data/unified`, and the published table agrees.
- BUU-LSPINE: the dataset report's L4L6 sheet, a count anomaly only ("L6" 15 films, "L4" 129); no Castellvi grade
  exists in any released radiograph set, which is why the (c) radiograph cell is hatched.
- C-ArmLSpine: pseudo-truth, said so on the figure and in the legend ("level by automatic read, unverified").
- TotalSegmentator's 12 SPINEPS+VERIDAH L6 calls were not used: CTSpinoPelvic1K and VerSe carry reader truth for
  every CT cell.

## Splits

CTSpinoPelvic1K 0244: v9 level bank validation (v8 train); 0008 train; 0760 validation; verse547 train (all from
`transitional_subtypes.csv`). C-ArmLSpine case136: release test split, absent from every level bank. BUU-LSPINE
2580-F-031Y and 0233-F-064Y: no entry in `allspine_v9_fov96_ctx/meta.json` or `allspine_v8_fov96_ctx/meta.json`
(0 matches of the patient id; 0271-F-062Y, an alternate, has 1), so neither film is in the level bank.

## Journal rules checked

- Components: four, (a)-(d); each is one strip of five cells (the journal counts components, not images).
- 300 dpi at the production width; TIF RGB LZW; labels are Arial Bold (letters 12 pt, column headers 8.5 pt,
  row titles 8.5 pt, cell tags 7 pt) at 183 mm. The journal's collage rule asks 12 pt or larger for labels and
  3 in per image; five cells across 183 mm cannot give either, and the manuscript prints the figure at
  `\linewidth` (160 mm, a further 0.87 scale). The letters meet the rule; the tags do not, and a reviewer may ask
  for the figure split or the tags moved into the legend. Recorded here rather than silently accepted.
- No identifier is printed: case ids live in GALLERY_SOURCES.md only. Patient's right on the observer's left on the
  AP cells; bone white on dark on every radiographic cell.
- Legend: 59 words, defines the arrow, the bar and the hatching, names the plane by column; the ages and sexes the
  journal asks for "where relevant" are in GALLERY_SOURCES.md, because the 60-word cap leaves no room.
- The figure is cited from `sections/results.tex` (the transitional paragraph); `\PENDINGFIG` replaced by the
  real float in `main.tex`, `check_limits.py` reports `fig:gallery: panels ['a','b','c','d'], caption 59 words`.

## Still owed (not by this figure)

1. **The device-card cells are the weakest cells.** They are what `docs/devices/cios_fusion.json` produces from the
   same line integrals the corpus uses (`make_drr_dataset.water_bone_paths_cm`, styled by `device_style.style_paths`),
   and the spine is faint in them. The corpus's own styled frames under `devcorpus/styled/` were looked at for
   comparison and are worse (the Surgio lateral shows no spine at all), which is the open physics item of the G4
   rebuild (`docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`, A28). When the cards or the path definitions change, re-run
   `slurm/gallery_panels.sh` and `tools/gallery_figure.py`; the picks are the constants at the top of the composer.
2. **BUU-LSPINE reproduction.** The dataset states no licence; its site asks for acknowledgement and forbids
   re-identification. Reproducing two films in a journal figure is a permission question for the PI; if it is not
   cleared, set `film=dict(empty=...)` for rows (a) and (d) in `tools/gallery_figure.py` and the cells hatch with the
   reason. Nothing else changes.
3. **Figure order.** The float sits fifth in `main.tex` at the time of writing; the coordinator owns the order.
