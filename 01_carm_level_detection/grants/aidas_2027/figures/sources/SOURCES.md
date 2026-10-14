# Where each figure source came from

`make_figures.py` beside the packet draws Figures 1, 2, 3b and 4 from these files; `latex/main.tex` places
`network_architecture.pdf` as Figure 3a. No image here was retouched by hand. Paths are relative to each repository's
root.

| file | origin | how it was made |
|---|---|---|
| `beethoven_popup_top.png` (Figure 2b) | OpenSpineConsortium/beethoven-extension at e900bae, `extension/store-assets/raw-20/04-home-panel.png`, the extension's popup as release 20's store kit captured it | cropped with Pillow at (20, 12, 700, 476): the popup's top half, from its name to the session buttons, which shows no grid login |
| `l6_labeled_ct.png`, `l6_render.png`, `l6_film.png` (Figure 1c) | spine-program at 5597197, `01_carm_level_detection/figures/schwingnet/figure1.png` (the paper's Figure 1, a sixth lumbar vertebra in a labeled CT, its physics render, and another person's film; its white bars are 20 mm, `figure1.record.json` "bar, 20 mm") | cropped with Pillow at (89, 149, 551, 842), (89, 858, 551, 1551) and (89, 1567, 551, 2260) |
| `network_architecture.pdf` (Figure 3a) | spine-program at 5597197, `01_carm_level_detection/figures/schwingnet/fig1c_arch.pdf` | copied unchanged (sha256 804e18f0...) |

Figures 1a, 1b and 2a are drawn as vector boxes in `make_figures.py` itself. Figure 2a follows the extension's own
store diagram (`extension/store-assets/src/diagram.js` at e900bae: claude.ai, "a chat" to Claude servers, "a Code
session" to "your Claude Code worker" on the Wayne State grid, "the model", "the heavy lifting" to an H200 GPU), and
names the grid's H200 partition as `11_students_grid_access/docs/handoff/EXTRACTS_11.md` records it (gmsap, 4 nodes
of 4).

Every number drawn is typed once in `make_figures.py`, beside the file it comes from:

| constant | figure | file |
|---|---|---|
| `NAMING` | 4a | `01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md` rows A2.1, A2.2, A9.2 and A5.1; A9.2's intervals from `01_carm_level_detection/results/schwingnet/indomain/name_fill.json` at 5597197, the file the catalog's A9 header names |
| `DETECTION` | 4b | the same catalog, rows A6.1, A6.2, A6.11, A7.8 and A6.12 |
| `TARGET` | 4b | row A6.13 (the 97 % set in advance, `ssn:docs/RSNAI_PLAN.md` C7) |
| `COHORT` | 2c | the 2026 cohort's Table 1, Cureus 2026;18(7):e112661 |
| `GEOMETRY` | 3b | `01_carm_level_detection/docs/MODEL_CARD.md` section 6.1 (source to detector 1,140 mm, to object 745 mm) |
