# manuscripts/superseded/: the earlier C-arm drafts, sources only

Lineage (`../../docs/handoff/MANUSCRIPTS.md` section 2.1): `rsnai/main.tex` "Naming Vertebrae Without an Anchor"
(2026-09-17 to 09-19; leaky banks) was superseded by `focused/main.tex` "Making the Intraoperative Count Exact" (09-19 to
09-22; every number transcribed from the evidence briefs), superseded by `rsnai/main_v2.tex` "Navigation from the C-arm
alone" (09-22; numbers from `claims.tex` through `tools/claims_fill.py` from `docs/RSNAI_CLAIMS.json`), superseded by
`../schwingnet/main.tex` from the evening of 2026-09-22, built only from rigor-passing numbers. Nothing here is quotable;
each is kept for a paragraph the current paper does not carry.

- `rsnai/`: `main.tex`, `main.pdf`, `main.tex.pre-restructure`, `graveyard.tex` and `graveyard.pdf` (cut text), `main_v2.tex`,
  `main_v2.pdf`, `claims.tex`, `main_kdevices_skeleton.tex`, `build.sh`, `refs.bib` (shared with the QI paper in project
  09), `figures/` (93 files: the Figure 1 story rows, fig10 to fig15, `dataset_profile.json`; `fig5_confirm_fluoro` of
  paper 1 was copied from here). **`main_v2.tex`'s title page says Neurosurgery; the affiliation is General Surgery.**
- `focused/`: `main.tex`, `main.pdf`, `build.sh`, `wordcount.py`, `figures/`, `_drafts/` (clinical, deployment and methods
  drafts with their PDFs). Holds the deployment paragraph and the only "latency unmeasured" sentences (lines 382 and 632 of
  `main.tex`); its TikZ Figure 6 (lines 876 to 941) is the model for the numbered panorama. **Its affiliation line and
  those of `_drafts/clinical.tex` and `_drafts/methods.tex` say Neurosurgery; the affiliation is General Surgery.**
- Not copied: `rsnai/web/index.html` (project 99 by path); the LaTeX build products (`.aux`, `.bbl`, `.fdb_latexmk`,
  `.fls`, `.log`, `.out`, `.toc`), regenerable with `build.sh`.
