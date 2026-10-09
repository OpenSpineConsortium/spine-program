# The scoping review, run for run date 2026-09-23

`spine_data_review/` ran end to end on its full search for the first time. Every stage ran. It stops where the
protocol says a person must act: screening (PROTOCOL.md 7.3) and charting (8). It also fails its own search
validation. Known-item recall is 0.43, and PROTOCOL.md 6.4 requires a documented revision of the query strings below
0.80 (section 4). That revision is Greg's decision and was not made here.

## Where it ran and what it wrote

- **Where.** In WSL, in a copy of the review directory outside the synced folder (`~/sdr_work/spine_data_review`), as the
  README advises for a full search. The code there and in the repository are identical, checked with
  `diff -rq --exclude=runs`.
- **Small run files, copied into the repository** at `spine_data_review/runs/2026-09-23/`: `run_meta.json`,
  `queries.json`, `counts.json`, `prisma_counts.json`, `requests.log.jsonl` (8 MB) and `probes/summary.json`.
- **Large run files, left in WSL** under `~/sdr_work/spine_data_review/runs/2026-09-23/`:
  - `records/` (1.2 GB) and `merged.jsonl` (488 MB)
  - `screening_sheet.csv` (484 MB)
  - `raw/` (4.1 GB)

  The README lists the first three as committed files, but at this size they need Git LFS or an archive. That
  decision is the coordinator's.
- **Downstream outputs, left in the WSL copy only.** The later stages wrote `charting/`, `analysis/`, `tables/`,
  `figures/` and `manuscript/` there. They hold pending markers, so they were not copied over the repository's files.

## Stage by stage

| stage | result | what happened |
|---|---|---|
| protocol-check | pass | 346 query entries; every self-test passes; the credential names are present and every keyed probe answered 200 |
| search | ran 2026-09-23 18:31–21:23 EDT, repaired 2026-09-24 | every adapter ran. The requests that did not answer are listed in section 2, with what was re-observed |
| check-run | failed, fixed, passes | Two defects, both fixed (section 2). `paging` is printed, not fatal, for three queries whose index moved by one record or whose PubMed history returned 22 fewer than it counted |
| dedup | pass | 254,935 identified, 26,382 duplicates, 228,553 after merge. All four flow identities hold |
| chart-check | pass, 0 records | no one has charted a dataset yet (PROTOCOL.md 8) |
| availability | pass, 0 probed | nothing is charted to probe. The second pass must come at least 48 h after the first |
| quality | pass, 0 scored | as above |
| stats | failed, fixed, then stops at `--check-flow` | a CSV field over 128 kB crashed it (fixed). It now writes every analysis and stops on `screened = pass + uncertain + non-English + audit_included`, because no record has been screened. That is the human gate, not a defect |
| figures | pass | drawn from the pending analyses |
| manuscript | builds (67 pages); `--strict` fails | 26 pending macros, 3 pending tables and 1 pending figure, all waiting for screening and charting |
| recipe | stops | no charting records (by design) |

## 1. The search

| source | queries | hits (records) | retrieved | notes |
|---|---:|---:|---:|---|
| PubMed | 2 | 6,933 | 6,911 | keyed |
| Europe PMC | 2 | 158,681 | 158,681 | `resultType=core` (deviation of 2026-09-19) |
| OpenAlex | 2 | 16,060 | 16,061 | re-observed; the index moved by one during paging |
| Semantic Scholar | 1 | 11,648 | 11,647 | re-observed |
| arXiv | 1 | 186 | 186 | re-observed from a grid compute node |
| bioRxiv / medRxiv | 2 | not answered | 0 | the API was down on both days (section 2) |
| Crossref | 29 | 2,260,848 | 90,367 | pass (a) local filter; 5,000 cap on 18 strings |
| Springer (S1) | 1 | 432 | 432 | `p=25` |
| Zenodo / Figshare / Dryad / OSF / DataCite | 67 | 14,568 | 11,019 | DataCite `datacite_01` partial (1,000 of 2,042) |
| TCIA / PhysioNet / grand-challenge | 3 | harvest | 23 | |
| Hugging Face / Kaggle / GitHub | 83 | | 5,938 | GitHub and Kaggle code or competition search need credentials that are absent |
| Open-i / Wikimedia Commons | 61 | figures / files | 15,915 | 11 Open-i queries partial: the service answered with an HTML error page |
| J-STAGE / SciELO / KoreaMed / Redalyc / OpenDataLab | 55 | 6,509 | 6,509 | KoreaMed, Redalyc and OpenDataLab have no public API (as foreseen) |
| Mendeley Data | 8 | | 0 | the front end reports nothing; its records come through DataCite (`datacite_04`) |
| Papers with Code | 7 | | 0 | retired (as foreseen) |
| MultiCaRe, Open-PMC-18M | 14 | | 0 | no adapter in this version (`not-run`) |

**Prescreen** (PROTOCOL.md 7.2):

| outcome | records |
|---|---:|
| pass | 18,309 |
| uncertain | 4,094 (2,771 of them because no source gave an abstract) |
| non-English route | 3,773 |
| fail: no spine term (S) | 41,934 |
| fail: no modality term (M) | 140,060 |
| fail: no dataset term (D) | 20,383 |

**26,176 records go to a person for screening.**

## 2. What failed, and what was done about it

Every item below is a row dated 2026-09-24 in PROTOCOL.md section 19, entered by the agent for Greg's review.

1. **The chain was cut at `check-run`.** The session running `run_all.sh` ended (SIGHUP) after the three-hour search
   had finished. The remaining stages were run one at a time in the same run directory. The search was not
   repeated, because repeating it would have re-drawn every source's answer.
2. **Requests that did not answer.** About twenty queries ended in transport errors, timeouts or 429s: OpenAlex,
   Semantic Scholar, one DataCite page, a Dryad grid query and Open-i.
   - **The rule being changed.** A fresh observation needed a fresh run directory (deviation of 2026-09-19).
   - **The new mechanism.** `sdr.common.reobserve` (`SDR_REOBSERVE=second-pass`, `SDR_REOBSERVE_SOURCES=...`)
     re-sends only the cached non-answers, under a salted cache key. The failed envelopes and their log lines stay.
     A replay with the same label reproduces the second observation; a replay without it reproduces the first.
   - **Recovered:**

     | query | before | after |
     |---|---:|---:|
     | `openalex_01` | 200 | 15,059 |
     | `openalex_02` | 0 | 1,002 |
     | `s2_01` | 0 | 11,647 |
     | `datacite_03` | 4,000 | 5,042 |
     | `openi_04` | 2,370 | 3,808 |
     | `openi_05` | 0 | 1,110 |

     `dryad_g31` also answered this time.
   - **Still partial:** `datacite_01` (page 2 timed out again) and eleven Open-i queries.
3. **Springer `p=100` returns 403 "premium feature"** on this key's plan. The adapter now pages at 25, and 432 of 432
   records were retrieved.
4. **arXiv refuses the WSL address.** `export.arxiv.org` answers HTTP 406 to every non-browser client from that
   address, and 200 to a grid compute node (probe job 40429437).
   - `arxiv_01` was re-observed on a compute node (job 40429469) and merged back with the new
     `tests/merge_reobservation.py`, which records the host on the invocation.
   - A browser TLS fingerprint was also answered from WSL. It was not used, because it would defeat a refusal the
     service placed on that address.
5. **bioRxiv/medRxiv did not answer.**
   - On 2026-09-23, `api.biorxiv.org` returned HTTP 200 with empty bodies for all 243 monthly intervals.
   - On 2026-09-24 it completed no TCP connection, from WSL or from the grid.
   - Both queries now record `hit_count_api` null with a "no answer" note, instead of the zero the old code wrote.
   - The L6 cross-check against Europe PMC `SRC:PPR` cannot be computed for this run.
6. **Two audit defects.**
   - **Wallclock.** `check-run` flagged 39 dates inside DOIs, titles and repository names that records copy from their
     sources. The rule now reads only fields the pipeline writes.
   - **Open-i.** Its HTML error page (HTTP 200) ended the paging loop silently, so eleven truncated queries read as
     complete. It is now counted as a failed request.
7. **`stats` crashed on the screening sheet.** A field was over the csv module's 128 kB limit. The limit is now raised
   once in `sdr/common.py`.

## 3. Known-item recall: the search fails its own threshold

Recall = retrieved / items with `role = recall` in `screen/known_items.csv`, computed on the merged records.

**9 of 21 = 0.43** (Wilson 95 % 0.25–0.63) against the protocol's 0.80.

- **Retrieved (9):** VerSe, CTSpine1K, CTSpinoPelvic1K, CT-ORG, the Glocker SpineWeb set, RSNA 2022 C-spine,
  BUU-LSPINE, VinDr-SpineXR, Mendeley 5jdfdgp762.
- **Missed (12):**
  - CT: TotalSegmentator, CTPelvic1K, CSI 2014, xVertSeg, CADS
  - radiographs: NHANES II films, CSXA, AASCE 2019, the IEEE lateral full-spine set, SpinalAI 2024
  - two figure sources with no adapter: MultiCaRe, Open-PMC-18M

  Without the two unrun sources, recall is 9 of 19 = 0.47.
- **I1-test items retrieved (outside the denominator):** LIDC-IDRI, SAROS.

PROTOCOL.md 6.4 says recall below 0.80 triggers a documented revision of the query strings, logged with the items
that drove it, and a rerun. The strings are frozen protocol content, so the revision was not made here. The misses
look structural rather than random:

- **Body-CT datasets.** TotalSegmentator, CTPelvic1K and CADS do not say "spine" in the text the searches read.
- **Radiograph datasets.** CSXA, AASCE, SpinalAI and the IEEE set live on GitHub, grand-challenge and IEEE DataPort,
  which the literature indexes do not cover and whose repository adapters matched nothing.

## 4. What the review gives the acquisition plan, and what it cannot

- **The review's scope is spine datasets, by design.** A widening to "any CT whose field of view includes a vertebral
  body" was considered and declined before the search (PROTOCOL.md 19, 2026-09-20 row). The review therefore cannot
  enumerate body CT, which is where most anomalous people are. The census (IDC exhaustively, the aggregators, a Zenodo
  sweep; ACQUISITION_PLAN.md sections 1 and 4b) does that job.
- **How much of the review is about CT.** 10,227 of the 26,176 records to screen name CT, and 4,261 of those are
  repository-class records.
- **A keyword pass for acquisition.** It found human CT datasets with a spine or body term and a dataset cue, read by
  the agent for acquisition only. It is not the review's screening, which is a person's.
  - **New to the plan:** ENHANCE.PET 1.6k (1,683 whole- or total-body PET/CT, CC BY 4.0, Science Data Bank) and LUMOS
    (280 lumbar CT). Both are in `ranking.csv` as deferred (section 4b of the plan).
  - **Already on disk, fetched or ranked:** VerSe (and the stump-rib labels), CTSpine1K, CSI 2014,
    TotalSegmentator v3, Spinal-Multiple-Myeloma-SEG, SAROS, PENGWIN 2024 and LumVBCanSeg.
  - **Not volumes:** the "1000 CT Images of Thoracic Vertebrae" set is 8-bit slices, and LumASe is cropped vertebrae.

## 5. Human steps the run now waits for

- **Screening.** Screen the 26,176 records (7.3). A second reviewer screens the stratified dual sample, and the
  prescreen audit draws 300 failed records.
- **Charting.** Chart every included dataset (8).
- **Availability.** Run the second availability pass at least 48 h after the first (`AVAIL_FLAGS=--apply`).
- **Query revision.** Decide the revision that section 3 requires.

## Reproduce

In WSL:

```
cd ~/sdr_work/spine_data_review
make check-run dedup chart-check availability quality stats figures manuscript recipe RUN_DATE=2026-09-23
```

That command runs every stage after the search. To replay the search offline, with the second observations, into a
fresh directory and compare it with the run:

```
mkdir -p runs/2026-09-23-replay && cp -r runs/2026-09-23/raw runs/2026-09-23-replay/
SDR_REOBSERVE=second-pass SDR_REOBSERVE_SOURCES=openalex,s2,springer,arxiv,datacite,dryad,openi \
  make search RUN_DATE=2026-09-23 RUN_DIR=runs/2026-09-23-replay REPLAY=1
~/sdr_venv/bin/python tests/diff_runs.py runs/2026-09-23 runs/2026-09-23-replay
```

The arXiv answer is in the run's `raw/arxiv/`, merged from the grid, so the replay serves it too.

**This replay was run on 2026-09-24, and it passes.** All 25 record files come back byte-identical to the run. The
only difference is the `arxiv_01` note in `queries.json` and `counts.json`, which records the grid host and was added
after the merge.

The first attempt at it failed, and that exposed a defect in the re-observation rule. `openi_05` page 871 was first
sent, and failed, during the labelled pass itself, so no salted answer exists. The replay then asked for one and
raised `ReplayMiss`. A replay now serves that failure, which is what the run observed (`sdr/common.py`;
`tests/test_reobserve.py` case 8).
