# Where each figure source came from

`make_figures.py` beside the packet draws the packet's one figure, the panel `fig1_panel.pdf` with panels a to f,
from these files. No image here was retouched by hand. Paths are relative to each repository's root.

| file | origin | how it was made |
|---|---|---|
| `l6_labeled_ct.png`, `l6_render.png`, `l6_film.png` (Figure 1d) | spine-program at 5597197, `01_carm_level_detection/figures/schwingnet/figure1.png` (the paper's Figure 1, a sixth lumbar vertebra in a labeled CT, its physics render, and another person's film; its white bars are 20 mm, `figure1.record.json` "bar, 20 mm") | cropped with Pillow at (89, 149, 551, 842), (89, 858, 551, 1551) and (89, 1567, 551, 2260) |

Panels a, b and e are drawn as vector boxes in `make_figures.py` itself. Panel b follows the extension's own store
diagram (`extension/store-assets/src/diagram.js` of OpenSpineConsortium/beethoven-extension at e900bae: claude.ai,
"a chat" to Claude servers, "a Code session" to "your Claude Code worker" on the Wayne State grid, "the model", "the
heavy lifting" to an H200 GPU), and names the grid's H200 partition as
`11_students_grid_access/docs/handoff/EXTRACTS_11.md` records it (gmsap, 4 nodes of 4). Panel e draws the RAG-LLM
as Aim 3's "The RAG-LLM" in `latex/main.tex` describes it, and carries no number.

Every number drawn is typed once in `make_figures.py`, beside the file it comes from:

| constant | panel | file |
|---|---|---|
| `NAMING` | 1f | `01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md` rows A2.1, A2.2, A9.2 and A5.1; A9.2's intervals from `01_carm_level_detection/results/schwingnet/indomain/name_fill.json` at 5597197, the file the catalog's A9 header names |
| `DETECTION` | 1f | the same catalog, rows A6.1, A6.2, A6.11, A7.8 and A6.12 |
| `TARGET` | 1f | row A6.13 (the 97 % set in advance, `ssn:docs/RSNAI_PLAN.md` C7) |
| `COHORT` | 1c | the 2026 cohort's Table 1, Cureus 2026;18(7):e112661 |

Until issue #110 the packet had four figures, and this folder also held the crop of the Beethoven popup (Figure 2b)
and the archived network drawing (Figure 3a); both are in git history at e664bd2, the commit that pull request
started from.
