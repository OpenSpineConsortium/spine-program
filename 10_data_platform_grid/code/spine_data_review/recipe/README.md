# recipe/ — downloading what the review found downloadable

Secondary objective SO3 of `PROTOCOL.md`: a download recipe for every included dataset whose
verified access route is `open-download` or `registration`, a manifest of every dataset with
its route, and a stub for a patient-grouped split. Everything in this directory except
`prepare_splits.py` and this file is **generated** by `python -m sdr.recipe` from the charting
records; edit the records, not the scripts. The review code itself downloads nothing; these
scripts are what a reader runs afterwards, on their own machine, under their own accounts.

## Regenerate

```
python -m sdr.recipe --run-dir runs/<run-date> --run-date <run-date>          # writes recipe/
python -m sdr.recipe --run-dir runs/<run-date> --run-date <run-date> --dry-run # plan only
python -m sdr.recipe --run-dir runs/x --run-date 2026-09-19 --demo            # three built-in records -> runs/x/recipe_demo/
```

Inputs: `charting/datasets/<id>.json` (or `--datasets some.jsonl`), `analysis/quality.json`
when it exists (for `fit_level_id` and the quality total, SAP A7 order), and
`charting/enrichment/<id>.json` when it exists (a `files` list supplementing the record's
`checksums[]`). Output is byte-identical on rerun; the only date in it is `--run-date`.

## Run

```
DATA_ROOT=~/data bash recipe/download_all.sh                 # everything, in manifest order
DATA_ROOT=~/data bash recipe/download_all.sh --skip-manual   # only the routes a script can fetch
DATA_ROOT=~/data bash recipe/download_all.sh --only verse,ctspine1k
DRY_RUN=1 bash recipe/datasets/<id>.sh                       # print what would be listed and fetched; no network, no writes
```

`DRY_RUN=1` (and `download_all.sh --dry-run`) makes no network call: a script whose files come
from a baked-in list prints one `would fetch` line per file, and a script that lists files through
the host's API at run time prints the endpoint it would query instead of querying it.

Each dataset lands in `$DATA_ROOT/<id>/` (default `~/data`) with a `.recipe_status` file
(`downloaded`, `manual`, `failed`). Order is SAP A7: reachable `fit_level_id` datasets not on
the authors' grid first, by quality total descending; then the other reachable sets; then the
manual routes; ties by id. Exit codes of a dataset script: 0 downloaded, 10 manual step printed
(a person must act; the driver counts it as `manual`, not a failure), 3 missing tool, 4
verification failed, 5 the host answered an HTTP error for the record, or listed no files for it.

Exit 5 is written by the methods that talk to a host directly: `zenodo-api`, `figshare-api`,
`mendeley-api` and `nbia-rest` on a listing the host refuses or answers with an error body,
`physionet-wget` on a slug whose version cannot be resolved, and `files`, `dryad-zip` and
`osf-zip` on a fetch curl reports as an HTTP error (curl exit 22); each of these logs the
failure and leaves `.recipe_status=failed`. Any other curl status (a transport fault) is
propagated as the script's own exit status, also after writing `failed`. The three client
methods are the exception: `hf-cli`, `kaggle-cli` and `git-clone` propagate their client's exit
status, and write `.recipe_status=failed` only where the script checks a result itself (a failed
`git lfs pull` exits 4).

## What each route becomes

| access_route (verified, charting record) | recipe_action | download_method |
|---|---|---|
| open-download, file URLs known from `checksums[]` or enrichment | download | `files`: curl each URL, verify sha256 > md5 > size > non-empty |
| open-download on Zenodo / Figshare | download | `zenodo-api` / `figshare-api`: list files through the records API at run time, verify md5 from the API; a missing record exits 5 |
| open-download on Mendeley Data | download | `mendeley-api`: list `public-api/datasets/<id>/files?folder_id=root&version=<v>` at run time (the version the record's DOI or URL carries, else the highest available one from `public-api/datasets/<id>/versions`, resolved by the script), verify `content_details.sha256_hash` from the API; an `{"error":...}` body exits 5. The version is not optional: without it the API answers HTTP 200 with `{"error":400}` |
| open-download on PhysioNet (Open Access) | download | `physionet-wget`: mirror `files/<slug>/<version>/`, then `sha256sum -c SHA256SUMS.txt` |
| open-download on TCIA (public collection) | download | `nbia-rest`: `getSeries` for CT/CR/DX/RF/XA/OT, one `getImage` zip per series |
| open-download on Dryad / OSF | download | `dryad-zip` / `osf-zip`: the repository's whole-dataset zip endpoint |
| open-download on Hugging Face | download | `hf-cli`: `hf download --repo-type dataset` (`huggingface-cli` accepted as the older name) |
| open-download on GitHub | download | `git-clone` (`--depth 1`, then `git lfs pull` when git-lfs is installed; a failed pull exits 4) |
| open-download elsewhere, `file_url_probed` or a data-extension URL | download | `files` with that one URL |
| open-download elsewhere, no file URL recorded | download | `browser`: prints the landing page (the probe saw a download link the record did not keep) |
| registration on Kaggle | registration | `kaggle-cli` when `~/.kaggle/kaggle.json` exists, else the registration step |
| registration on Hugging Face (gated) | registration | `hf-cli` when `HF_TOKEN` or the cached token exists, else the step |
| registration elsewhere (grand-challenge, institutional) | registration | `browser`: register and download through the site |
| data-use-agreement | manual-dua | prints the DUA step; the review signed none (protocol section 8) |
| request-to-authors | manual-request | prints the request step; the review sent none (section 16) |
| unavailable | unavailable | prints the last probe status and rule; nothing to download |
| commercial | commercial | prints the terms; nothing purchased |

Verification is the strongest published check the record carries (`sha256`, `md5`, `size`), else
the host API's checksum read at run time (`md5 (API, run time)`, `sha256 (API, run time)`,
`sha256 (SHA256SUMS.txt)`); when none is published the script checks only that a file exists and
is non-empty and the manifest says `non-empty`. Three methods verify nothing the review recorded:
`hf-cli` and `git-clone` rely on the client's own integrity check and the manifest says
`client (not a published checksum)`; `kaggle-cli` and the `browser` steps perform no check and
the manifest says `none`. Nothing is ever re-downloaded when it exists and verifies; partial
downloads resume.
Credentials are never stored here: the Kaggle and Hugging Face clients read their own
configuration, and `RECIPE_AUTH_HEADER` can carry a header for a `files` fetch behind a token.

## manifest.csv

One row per included dataset (all routes), in run order: `recipe_order, dataset_id, name,
modality, region, n_subjects, access_route, access_route_rule, host_type, host_key,
access_url, recipe_action, download_method, verification, n_files_known, size_gb,
licence_text, licence_tier, on_grid, fit_level_id, quality_total, script, manual_step`.
`licence_tier` is the charted tier; a `non-commercial` or `restricted` licence downloads the
same way and binds the reader the same way, so read it before training on anything.

## prepare_splits.py

A patient-grouped train/validation/test split over the downloaded sets, seed 20260919,
stratified per dataset, with the discovery of subjects left as a registry
(`DISCOVERY_RULES`, `@register`) that is empty on purpose: a dataset is never split by a guessed
grouping. `python recipe/prepare_splits.py --self-test` checks the split rule on synthetic
subjects; `--dry-run` reports which downloaded datasets have a discoverer; `--limit N` caps the
subjects taken per dataset; `--run-dir`/`--run-date` are optional here (the script runs on a
reader's machine after the download) and record the invocation in `run_meta.json` when given; a
full run writes `$DATA_ROOT/splits.json`. A missing `manifest.csv` exits 2 and names the
regenerate command. Partitions are filled by cumulative subject count with groups kept whole, so
a partition whose slice is smaller than one group can come out empty (five two-image patients
split 8/0/2); the script warns per dataset when that happens.

## Limits

TCIA series arrive as one zip per series and can be tens of gigabytes; PhysioNet mirrors are
version-pinned to the current version at run time; GitHub releases larger than the repository
are reached through `checksums[]` URLs when enrichment recorded them. A landing page that
answered `open-download` by rule P20 (a download anchor on an HTML page) without a recorded
file URL becomes a `browser` step, because the recipe fetches only URLs a record names.
