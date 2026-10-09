# FluoroCap

Published spine fluoroscopy / C-arm figures whose captions name a vertebral level, collected
from the PubMed Central Open Access subset under the protocol in `PROTOCOL.md`. Every panel
is documented in `manifest.csv` (origin, rights, de-identification, modality, region,
projection, population, acquisition, inclusion / exclusion codes, label status,
preprocessing, hashes). This directory is regenerated end to end by the scripts below; a
frozen version lives under `releases/` and is never rewritten.

## Regenerate

```
python tools/fluorocap.py search   --root ~/FluoroCap            # Europe PMC -> articles.jsonl
python tools/fluorocap.py captions --root ~/FluoroCap --threads 14 --rate 4   # BioC / JATS -> captions_*.jsonl
python tools/fluorocap.py captions --root ~/FluoroCap --retry-errors
python tools/fluorocap_openi.py    --root ~/FluoroCap            # Open-i -> openi_matched.jsonl (+ openi/)
python tools/fluorocap_multicare.py --csv captions_and_labels.csv --out ~/FluoroCap/extra_targets.jsonl
python tools/fluorocap_pmc18m.py   --root ~/FluoroCap --workers 4   # Open-PMC-18M -> pmc18m_matched.jsonl, pmc18m_negatives.jsonl
python tools/fluorocap.py fetch    --root ~/FluoroCap --threads 4 --rate 3   # PMC CDN -> raw/, fetched.jsonl
python tools/fluorocap_context.py  --root ~/FluoroCap            # -> articles_context.jsonl
python tools/fluorocap_panels.py   --root ~/FluoroCap --workers 16   # verify, split, hash -> panels/, panels.jsonl
python tools/fluorocap_classify.py --root ~/FluoroCap --manifest <films manifest.parquet> --images <films>   # -> panel_preds.jsonl, classifier_report.json
python tools/fluorocap_manifest.py --root ~/FluoroCap --version 0.1   # -> manifest.csv, figures.csv, articles.csv, stats.json, reader_sheet_template.csv
python tools/fluorocap_infer.py    --root ~/FluoroCap --weights <detector.pt> --model <level model.pt> --ctx <crop bank>   # -> infer_results.jsonl, panel_subgroups.jsonl
python tools/fluorocap_manifest.py --root ~/FluoroCap --version 0.1   # again, now with subgroup columns
python tools/fluorocap_freeze.py   --root ~/FluoroCap --version 1.0   # -> releases/FluoroCap_v1.0/ (SHA256SUMS, LOCK.json)
```

`slurm/fluorocap_run_rest.sh` and `slurm/fluorocap_run_infer.sh` chain the stages on the
grid (network stages on the login node, panels / classifier / inference as batch jobs).
Network stages are resumable and polite (a few requests per second).

## Files

| File | One row per | Content |
|---|---|---|
| `articles.jsonl` | article | Europe PMC search result: PMCID, title, journal, year, licence |
| `captions_all.jsonl` | article | every figure caption with its graphic file name |
| `captions_matched.jsonl` | figure | captions meeting I2–I4, with levels, view, species / phantom / other-modality flags |
| `openi_matched.jsonl`, `extra_targets.jsonl`, `pmc18m_matched.jsonl` | figure | the same from Open-i, MultiCaRe, Open-PMC-18M |
| `pmc18m_negatives.jsonl` | sub-figure | random Open-PMC-18M sub-figures with modality labels (classifier training) |
| `fetched.jsonl` | figure | URL fetched, UTC time, bytes, sha256, local path |
| `articles_context.jsonl` | article | licence, abstract, MeSH, equipment / exposure / positioning / population / ethics sentences, caption identifier scan |
| `panels.jsonl` | figure | decode check, dimensions, colourfulness, sha256, panel boxes |
| `panel_preds.jsonl` | panel | p(not x-ray), p(x-ray other), p(x-ray spine), p(lateral) |
| `manifest.csv` | panel | the full record (columns listed in `tools/fluorocap_manifest.py`) |
| `figures.csv`, `articles.csv` | figure, article | roll-ups |
| `stats.json` | — | counts by route, licence class, region, level, projection, exclusion code; manifest hash |
| `classifier_report.json` | — | held-out confusion matrices of the modality and view heads |
| `infer_results.jsonl`, `infer_summary.json` | panel | detector run, single-vertebra and recurrent level predictions, caption consistency |
| `reader_sheet_template.csv` | included panel | blinded reading sheet (no caption, no source) |
| `ids.json` | panel | stable `image_id` assignment |
| `releases/FluoroCap_v*/` | — | frozen versions: panels by `image_id`, manifest, `SHA256SUMS`, `LOCK.json` |
