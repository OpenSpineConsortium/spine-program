"""sdr: code for the scoping review of human spine CT and projection-radiography datasets.

One module per stage (PIPELINE.md maps them to the names PROTOCOL.md uses): search_literature
(L1-L7), search_repositories (R1-R14, F1, F4-F8), dedup_prescreen (7.1-7.2), chart (validate,
8-9), availability (the probe, 10), quality (11), stats (the SAP), figures, manuscript, recipe;
and one shared layer, `sdr.common` (+ creds, ids), which every other module imports. Nothing in this package downloads a dataset, writes outside
`spine_data_review/`, or prints a credential value. The protocol version the code
implements is recorded here so that `run_meta.json` can name it.
"""
PROTOCOL_VERSION = "1.0"
__version__ = "1.0"
