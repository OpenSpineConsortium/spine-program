# STATUS.md — what is in hand on 2026-10-08

Every number names its file. Rigor marks follow `docs/handoff/RESULTS_CATALOG.md` ("How to read a row"): CURRENT, DATED,
RECORD ONLY, SUPERSEDED. This project scores nothing: its numbers are latencies, counts and dates, not accuracies, and
none of them goes through the evaluation gate because none is a model claim.

## Results in hand

| id | claim | file | mark |
|---|---|---|---|
| CAT-G.8 | PACS X-ray demo latency 40,018 ms to 1,360 ms on 2026-09-12: the http redirect on the custom domain disabled WebGPU and service workers (single-threaded WASM, 40 s); forcing https fixed that; COEP then refused the jsdelivr CDN, so onnxruntime-web was vendored under `pacs/ort/`; the 1024 to 640 export cut anchors 21,504 to 8,400 (3,257 to 1,360 ms on Intel Gen-9) | `docs/handoff/RESULTS_CATALOG.md` G.8; `memory/pacs-website-latency-root-cause.md` (its site commits 4955e46, 1446389, e1d2fde, 45ae8f1 are pre-rewrite ids from the memory note: not resolvable after the 2026-09-14 git-filter-repo rewrite, by `git cat-file -t` on c1800f8 and origin/master a17ea39, 2026-10-08; the surviving anchor is ea0086c, 2026-09-14; the 5559d87 named in `memory/level-service-serving.md` is likewise gone) | DATED: since 2026-09-14 the X-ray model runs behind the level service, not in the page; the root causes still bind |
| site-1 | the site is generated: 25 body fragments under `tools/pages/`, 6 templates, 41 sitemap entries, 420 tracked files at c1800f8; origin at a17ea39 with 221 commits since 2026-05-18 | `MANIFEST_CODE.md` section 1 (counted on the clone and `git rev-list`, 2026-10-08) | CURRENT (the clone was ten commits behind; `TODO.md` step 1) |
| site-2 | no model weight in the tree: zero `.pt` or `.onnx`; the 12 `.bin` files are gallery meshes under `assets/gallery/` (874,636 to 1,327,480 B); `gallery/data/` holds only `distributions.json` (1,368,004 B); the four demo volumes are 292,542 to 1,682,039 B | `git ls-files '*.pt' '*.onnx'`, `git ls-files '*.bin'` and `git ls-files '*.nii.gz'` on the clone at c1800f8, 2026-10-08 (an earlier inventory said 13 meshes under `gallery/data/` and five volumes; those counts were wrong and are withdrawn); `MANIFEST_CODE.md` section 1 | CURRENT |
| site-3 | the X-ray tab calls the service: `SERVICE_DEFAULT = https://level-id.openspineconsortium.org`, chosen after `?service=` and `localStorage.levelIdService`; `GET /health`, `POST /infer` (multipart image, conf, imgsz); the answer carries boxes, four corners per instance and the level names (`level_run`, `level`, `top3`) | `pacs/remote.js` at c1800f8 (read 2026-10-08); `memory/level-service-serving.md` | CURRENT as code; the endpoint was not live on 2026-09-14 and has not been re-checked |
| site-4 | the CT tab on case 0003 (v3-scheme export; full PI, SS, PT, LL) reads `metrics.json` with keys `case_id, summary, geometry, files, label, postop`; the post-op tab shows the toolkit's synthesis | `pacs/data/0003/metrics.json`, `pacs/data/manifest.json` (read 2026-10-08); `memory/pacs-demo-and-ostk-params.md` | CURRENT (legacy scheme; re-export pending `TODO.md` step 6) |
| CAT-G.5 | the post-operative synthesis the demo shows: case 0003, ALIF L1-S1, age 50, LL 45.7 to 55.0, PI-LL 9.8 to 0.5, five cages; re-measuring the synthesised image collapses LL to about 24 (voxel roughness), so post-op numbers are carried analytically and the image is display only | `docs/handoff/RESULTS_CATALOG.md` G.5 | prototype (the toolkit's, `04_openspinetoolkit`) |
| atlas-1 | `atlas/level_atlas.csv`: 47 data rows, 8 measures (`canal_ap, canal_w, disc, endplate, h_ant, h_post, hu, pedicle`) at T11, T12, L1-L5 and the discs L1L2-L5S1, each with n, median, quartiles, p5, p95, mean, SD and unit; rendered by `build_table.py` so the page carries no typed number | the CSV at c1800f8, counted with `csv.DictReader` on 2026-10-08 | CURRENT as a file; its values are `05_ct_morphometry_parity`'s and the catalog's F rows say which per-level measures are trusted (the canal-closing regression G.2 inflates posterior height and end-plate depth after toolkit commit 1b7005c; the committed morphometry CSV predates it) |
| site-5 | the people page renders 20 entries from `contributions/manifest.json`; the education page renders `meded/survey-summary.json` | the two files at c1800f8 (counted 2026-10-08) | CURRENT |
| MAN-12 | the medical-education study is published: Schehr A, Kim J, Schwing G. "OpenSpineConsortium: An Open-Source Framework for Medical Student Engagement in Computational Spine Imaging Research." Cureus 2026;18(7):e112661, doi 10.7759/cureus.112661, 14 Jul 2026 (16 respondents, six domains); a CNS 2026 printed poster (CNS 66639) and a JEEHP version that would publish the same data twice | `docs/handoff/EXTRACT_MANUSCRIPTS_12.md` | CURRENT (published); OQ A21 open |
| svc-1 | service latency as measured on the grid login node (8 old CPUs): 1.6-2.3 s per 2048-px film end to end, about 0.9 s fixed overhead; on a V100 the detector 23 ms plus 2.3 ms per crop | `memory/level-service-serving.md` (2026-09-14) | RECORD ONLY: measured on the login node, against the standing rule; a CPU host is not faster than the former in-browser WebGPU path, a GPU host is |

## Superseded, and by what

| what | superseded by | record |
|---|---|---|
| in-browser inference: `pacs/models/v11n_640.onnx` and `v11n_1024.onnx` (11 MB each) with vendored onnxruntime-web; the per-backend medians 133 ms (WebGPU, discrete NVIDIA), 445 ms (WebGPU, Intel Gen-9), 1,093 ms (WASM); the live-site parity on 40 BUU test radiographs (SS MAE 2.86 vs 2.79 degrees offline, LL 3.86 vs 3.81, within 0.07 degrees; median 264 ms) | the level service (2026-09-14): the model files were removed from the site, the history rewritten (head ea0086c), and the page sends pixels to `SERVICE_DEFAULT` | `pacs/README.md` at c1800f8 still prints these numbers; they are RECORD ONLY: a weight the browser loads is a weight given away (`memory/level-service-serving.md`), and the BUU numbers never went through the evaluation gate |
| the one-page site (`index.html` with anchors `#datasets`, `#people`, ...) | the generated multi-page site (`tools/build_site.py`, 2026-09-30, commit a1cf7ee) | `git show 28d2cee:index.html` in the site repository |
| `tools/stamp_assets.py` | the stamping inside `build_site.py` | site `README.md`, "Caching" |
| the `/ashley/` address and the Ashley Bridge name | `/beethoven/` (public name since 2026-09-29); `/ashley/` holds only redirects and SHA-pinned kept files | site `README.md`, "Publishing" item 3 |
| direct downloads of Beethoven 7.0.0 from the site | the private Chrome Web Store listing by invitation (8.0.0 and later, site commit 3f805f4, 2026-09-30); the site `README.md` says the packages remain in history at 816e9c4, but 816e9c4 is not an object in the clone on 2026-10-08 (`git cat-file -t`), so which commit holds them is unverified | site `README.md`, "Beethoven" (lines 185-186) |
| the demo's "SVA/TPA out of scope (needs C7/T1)" sentence and the supine-CT-versus-standing framing | removed by Greg; never reintroduced | `memory/pacs-demo-and-ostk-params.md` |
| the demo bundle's legacy label scheme (case 0003, v3: femurs 11/12) | a v11 re-export with `labels_for` once catalog G.2 and G.3 are fixed | `TODO.md` step 6 |

## What is not known

- Whether `https://level-id.openspineconsortium.org` or any host answers today (no network on 2026-10-08).
- Whether "Enforce HTTPS" is ticked on the Pages settings today.
- Whether the Beethoven 14.0.0 texts (repository 2f90319, 2026-10-03) are on the live site: the clone at c1800f8 rendered
  12.0.0; origin's 1b4b337 (2026-10-07) says "the products' current texts"; not re-checked.
- Which build produced the 12 gallery meshes under `assets/gallery/` and the demo's DRR reference pane (`pacs/data/xr/0003/`): not recorded.
- Which commit holds the Beethoven 7.0.0 packages: the site `README.md` names 816e9c4, which is not an object in the
  clone on 2026-10-08 (`TODO.md` step 13).
- Whether the GitHub Support purge of the cached ONNX blob was ever requested: not recorded.
