# FluoroCap: the dormant literature harvest (record only)

FluoroCap was a collection of published spine fluoroscopy and C-arm figures whose captions name a vertebral level,
harvested from the PubMed Central Open Access subset and other open sources under a written protocol, to evaluate a
locked level-identification algorithm with no patient contact. It is dormant: 72.8 % of its panels have zero pixel
residual against the printed figure, so they are reproductions of published figures, not fluoroscopy
(`../../memory/fluoro-panel-gap-diagnosed.md`; the reproduction note is owned by 01); no model distinguished a fluoroscopy
panel from a radiograph; Greg's directive D1 of 2026-09-23 took it out of every training set
(`../../memory/data-directives-2026-09-23.md`); a human-read test set of about 200 panels was proposed and does not exist
(`../../TODO.md` step 8). Nothing here is run; the harvester tools, slurm chains and grid tree are named by path in
`../../MANIFEST_CODE.md` and `../../MANIFEST_GRID.md`.

| file | last commit (spinesurg-ct-nnunet) | what it is |
|---|---|---|
| `FLUOROCAP_README.md` (4,242 B) | 116b6ef, 2026-09-13 | how the directory was regenerated end to end; the manifest columns (origin, rights, de-identification, modality, region, projection, population, acquisition, inclusion and exclusion codes, label status, preprocessing, hashes); the frozen release under `releases/` |
| `FLUOROCAP_PROTOCOL.md` (13,347 B) | a6e36b3, 2026-09-13 | protocol version 1, written 2026-09-13 before the collection was frozen: the search and inclusion rules, traceability from a result back to a panel, figure, article and licence |
| `FLUOROCAP_QC_2026-09-14.md` (12,646 B) | 351808c, 2026-09-14 | the corpus QC counted off disk: 11,349 panel images; no number in it is a human-verified accuracy because no human-verified set existed (its section 8, line 166, says so: "No panel has been read by a human") |
| `PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` (454,660 B) | b1469ae, 2026-09-14 | 366 sources and 534 literal queries from a parallel sweep across eleven search angles for pathology, variant and wrong-site images, plus a clinical knowledge base for 7 pathology families; the clinical entries are machine-authored and the skeptic pass that was to check them never ran (it says so in its first paragraph); it also records why the RSNA 2022 cervical archive was fetched (line 397); on the fix pass of 2026-10-08 the two named contact addresses (a vendor and a society contact, lines 1254 and 1257) were replaced by the domain and "(named contact address withheld)", the same way as in the JSON twin (`../../MANIFEST_LOCAL.md` section 3) |
| `pathology_source_sweep_2026-09-14.json` (1,345,233 B at the source) | b1469ae, 2026-09-14 | the machine form of the sweep; two named vendor and society contact addresses were replaced by the domain (in this file and, since the fix pass, in the Markdown twin) and the banned word was rewritten as origin on copy (`../../MANIFEST_LOCAL.md` section 3) |

The overnight report of 2026-09-14 (`FLUOROCAP_MORNING_2026-09-14.md`) is with the dated checkpoints in `../checkpoints/`.
The descriptive numbers of the frozen release (4,979 figures, 2,205 articles, 10,281 panels; A 2,531 included, B 991
licence-clean) are in `../../STATUS.md` section 4 with their files. The 2,100 FluoroCap crops that still sit inside the
C-ArmLSpine fold banks are 01's item (`../handoff/DATASET_USAGE.md` sections 0.4 and 3.2; `../../TODO.md` step 9).
