# Where each figure source came from

`make_figures.py` beside the packet draws Figures 1, 2, 3b and 4 from these files; `latex/main.tex` places
`network_architecture.pdf` as Figure 3a. Nothing here was redrawn by hand. Paths are relative to each repository's root.

| file | origin | how it was made |
|---|---|---|
| `beethoven_route.png` | OpenSpineConsortium/beethoven-extension at e900bae, `extension/store-assets/src/` (`store.css`, `diagram.css`, `diagram.js`, `common.js`): the Chrome Web Store diagram behind `release/20.0.0/store-kit/07-screenshot-1-your-grid.png` | rendered in Chromium (Playwright) at device scale 3 on a 1236 x 532 px canvas, with the diagram's own label sizes scaled for print by CSS overrides (class `t-node` x1.1, `t-arrow` x1.65, `t-me` x1.3), the `t-lift` label ("the heavy lifting") wrapped at 5.2 em and the `t-pm` label moved 30 px left; then cropped to its content with a 30 px margin (40 px on the right) |
| `beethoven_popup.png` | the same folder, `shot-04.html` (store screenshot 4, "click once") | Chromium at device scale 3, viewport 1280 x 800, clip x 640 to 1160, y 95 to 720 |
| `beethoven_worker_settings.png` | the same folder, `shot-05.html` (store screenshot 5, "your worker, your rules") | Chromium at device scale 3, viewport 1280 x 800, clip x 635 to 1255, y 65 to 635 |
| `l6_labeled_ct.png`, `l6_render.png`, `l6_film.png` | spine-program at 5597197, `01_carm_level_detection/figures/schwingnet/figure1.png` (the paper's Figure 1, a sixth lumbar vertebra in a labeled CT, its physics render, and another person's film) | cropped with Pillow at (89, 149, 551, 842), (89, 858, 551, 1551) and (89, 1567, 551, 2260) |
| `network_architecture.pdf` | spine-program at 5597197, `01_carm_level_detection/figures/schwingnet/fig1c_arch.pdf` | copied unchanged |

The popup's grid login `st1234` is the mock portal's demo user that the extension's own store listing and contract
vectors use (`docs/STORE_LISTING.md`), not a person. The store screenshots carry no student name.

The numbers in Figures 2c and 4 are typed once in `make_figures.py` (`COHORT`, `NAMING`, `DETECTION`) beside the file
each comes from: the 2026 cohort's Table 1 (Cureus 2026;18(7):e112661) and `01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md`
rows A2.1, A2.2, A3.2, A5.1, A6.1, A6.11, A6.12, A6.13 and A13.3.
