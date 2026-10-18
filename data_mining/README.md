# data_mining

The Fluoroscopy Data Atlas of 17 October 2026: every fluoroscopy, spine radiograph, paired CT and X-ray, CBCT
projection and DRR dataset found for intraoperative vertebral level identification and for CT-to-C-arm parity, sorted
by what is drawn on the images, how the images were saved and how to get them, with what is already on the grid and the
16 request letters that are ready to send. It serves folders 01, 02, 05, 07 and 08 and draws on folder 10's manifest.

## Open it

- **On GitHub, from any account:** read [`CATALOG.md`](CATALOG.md). It holds every record as tables by kind, the ten
  most valuable gaps, the request list with Radiopaedia's steps, and, under each table, how to get each dataset.
- **With search and filters:** open [`fluoroscopy_data_atlas.html`](fluoroscopy_data_atlas.html) in a browser. GitHub
  shows HTML as source, so download it first (the "Download raw file" button on the file's page), or open it from a
  clone: `start data_mining\fluoroscopy_data_atlas.html` on Windows, `open` on a Mac. It needs no server; its fonts come
  from Google Fonts and fall back to system fonts offline. Filters remember themselves in that browser only.
- The same page was published on 2026-10-17 as a private claude.ai artifact on one of Greg's accounts
  (https://claude.ai/artifact/8YNXyLYbthsLjqEbFxQph2). This folder is the copy every account can reach, and the one to update.

## What is here

| Path | What it holds |
|---|---|
| `CATALOG.md` | The catalog as Markdown, written by the build |
| `fluoroscopy_data_atlas.html` | The page: search, filters, the request letters with copy buttons; data embedded |
| `data/datasets.json` | The 217 merged records the page and the catalog show |
| `data/requests.json` | The 16 request records (route, effort, status, what to expect, subject, letter text) |
| `data/sources/inhouse.json` | 189 records extracted from Greg's own files (below) |
| `data/sources/web_fluoro.json` | 44 fluoroscopy and spine radiograph datasets from a web search on 2026-10-17 |
| `data/sources/web_paired.json` | 30 paired CT and X-ray, CBCT projection and DRR datasets from a web search on 2026-10-17 |
| `data/sources/idc_ct_plus_radiograph_patients_v25.csv` | Per TCIA collection (Imaging Data Commons v25): patients with CT, with CR/DX, and with both |
| `scripts/` | `merge_atlas.py`, `parse_requests.py`, `make_catalog_md.py` and the page template |
| `video_issues.json` | The 21 fluoroscopy video datasets as tasks, one issue each under epic #185 (#186 to #206), opened by `scripts/make_video_issues.py` |

## How it was built

- **Greg's records** (`inhouse.json`): spinesurg-ct-nnunet `data_platform/DATA_MANIFEST.md` and `sources.json` (the
  212-source manifest), `HANDOFF/literature_state/dataset_landscape_by_task.md` and `LITERATURE_STATE.md`; this
  repository's `01_carm_level_detection/docs/data_requests/`, `FLUORO_VIDEO_SOURCES_2026-09-26.md` and
  `docs/external_reports/` (the two dataset reports); and the project memory notes.
- **Web search** (`web_*.json`): official dataset pages, repositories and papers, opened one by one. A record with
  `verified: false` came from search results only; the page marks it "link not opened". Radiopaedia's site was not
  fetched, because its terms bar automated access.
- **Merge** (`scripts/merge_atlas.py`): Greg's records are the base and are never merged with one another, since the
  manifest lists separate banks on purpose. Each web record joins the record it names (same name, or the same dataset
  family and a compatible kind), filling only empty fields; Greg's records win for status, grid path and notes. Web
  records with no match are added. Three TCIA collections whose CT Greg holds but whose radiographs he does not
  (COVID-19-NY-SBU, COVID-19-AR, CMB-MML) are marked not held, with a note saying so.
- **Status**: *held* means present under `/rs/rs_grp_oschome/go2432/data/` on the Wayne State grid, where approved
  students can read it; *request ready* means a letter is drafted (none was recorded as sent on 2026-10-17); *not held*
  means it is not on the grid.

## Rebuild

From the repository root, with Python 3.10 or later and nothing else installed:

```
python data_mining/scripts/merge_atlas.py
```

It parses the letters in `01_carm_level_detection/docs/data_requests/` into `data/requests.json`, merges the three
source catalogs, and rewrites `data/datasets.json`, the page and `CATALOG.md`. To add or correct a dataset, edit the
source record in `data/sources/` and rebuild; the ten "worth getting next" items are listed twice, in
`scripts/atlas_template.html` and `scripts/make_catalog_md.py`, and should be changed together.

Each record has these keys: `name`, `aka`, `category` (`fluoro_video`, `fluoro_frames`, `radiograph`,
`paired_ct_xray_real`, `paired_ct_drr_synthetic`, `cbct_projections`, `private_request`), `anatomy`, `size`,
`image_quality`, `annotation_level`, `annotation_detail`, `level_labels`, `pose_geometry`, `access`, `how_to_get`,
`license`, `link`, `paper`, `greg_status` (`held`, `requested (letter drafted)`, `not held`), `grid_path`, `notes`, and
for web records `verified`.

## Read before relying on it

- Everything here is as of 17 October 2026. Dataset pages, licences and fees change; open the page before a download
  or a request.
- Radiopaedia's fee (USD 250 in the draft) could not be confirmed from public sources; its licensing contact is the one
  published studies cite.
- A letter promising non-commercial use binds the data to that use: data meant to validate the level-confirmation
  product needs a commercial licence instead.
