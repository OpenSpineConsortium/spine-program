# Groundwork adversarial check — 2026-09-23

Independent verification of the three groundwork deliverables (CLAIM map, LEVELCHECK_CLAIM.md,
COBRA LSTV screen), performed by a separate agent with independent tooling: the docx was parsed
directly from `word/document.xml` (zipfile + ElementTree, not python-docx and not
`tools/gen_claim_checklist.py`), Wilson bounds were recomputed from the closed formula, PMIDs were
fetched from NCBI eutils, and the grid queue was read live.

| # | Check | Verdict |
|---|---|---|
| a | Every docx item verbatim in CLAIM_CHECKLIST.md | **PASS** |
| b | Five PMIDs/DOIs in LEVELCHECK_CLAIM.md fetched and compared | **PASS** |
| c | Three (twelve) Wilson power-table cells recomputed | **PASS** |
| d | COBRA screen jobs live; no reorient on write; missing ct_def.mha skipped | **PASS** |

## (a) Docx items vs CLAIM_CHECKLIST.md — PASS

The docx (`CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx`) was parsed independently of the
repo's generator: cell text assembled from `w:t` runs, paragraphs joined with newline, stripped —
the same normalisation python-docx applies, arrived at separately.

- Numbered items in the docx table: **42**, numbered exactly 1–42 (assert passed).
- Item texts found verbatim (exact substring) in `SchwingNet/CLAIM_CHECKLIST.md`: **42/42**.
- Item texts byte-equal to `claim_checklist.json` `rows[].text`: **42/42**.
- Tally cross-check: json `counts` = {items 42, SATISFIED 29, GAP 13}; independent recount over
  `rows[].verdict` = 29/13. The 13 GAP gates recount to G0×3 (8, 17, 34), G1×2 (16, 18),
  G3×2 (20, 21), G5×3 (25, 31, 35), G6×1 (2), G7×2 (41, 42) — matching the reported headline.

## (b) PMID/DOI spot-checks in LEVELCHECK_CLAIM.md — PASS

Five records fetched from NCBI eutils (PubMed HTML blocks cookie-less fetches; eutils does not).
All five match the doc's citation and its quoted numbers:

| doc row | fetched record | numbers check |
|---|---|---|
| Manbachi 2018, PMID 30051244 / 10.1007/s10439-018-2099-2 | Manbachi A, Ann Biomed Eng 2018 Oct;46(10):1548-1557, "Clinical Translation of the LevelCheck Decision Support Algorithm..." | 5 surgeons × 62 cases; median error 30.4 % → 2.4 % (p < 0.01); confidence up in 91 %; 20 patients; runtime 17–72 s — all as quoted. Confirms the doc's correction that the 2018 clinical series is first-author Manbachi, not Ketcha. |
| Nakagawa 2017, PMID 28717058 / 10.1620/tjem.242.223 | Nakagawa T, Tohoku J Exp Med 2017;242(3):223-228 | LSTV 71/550 (12.9 %); 37 sacralised L5 + 34 lumbarised S1; miscounted in 38 (54 %); level altered in 11 (15 %) — all as quoted. |
| Liebrand 2026, PMID 42009915 / 10.1007/s00586-026-09925-x | Liebrand B, Eur Spine J 2026 (ahead of print), ASReview systematic review | Abstract verbatim: "In the studies involving transitional vertebrae no 100% was achieved." The doc's load-bearing sentence is exact. Note the abstract ALSO says conventional methods reached up to 100 % in nine studies overall — the doc's phrasing correctly scopes the claim to transitional studies; the manuscript must keep that scope. |
| Otake 2012, PMID 22864366 / 10.1088/0031-9155/57/17/5485 | Otake Y, Phys Med Biol 2012;57(17):5485-508 | 10 CTs, 50,000 simulated images, 99.998 % (1 failure in 50,000), 4.7 s GPU — all as quoted. |
| Hanhivaara 2020, PMID 32072261 / 10.1007/s00330-020-06691-2 | Hanhivaara J, Eur Radiol 2020;30(6):3409-3416 | 1,101/3,855 (29 %); Castellvi I 68 %, II 16 %, III 13 %, IV 3 % — the doc's type breakdown (and its ~9 % numbering-relevant derivation) checks out. |

## (c) Wilson power table recompute — PASS

Wilson two-sided 95 % lower bound, z = 1.96, p̂ = (n−k)/n, closed formula, independent script.
Well beyond three cells — twelve cells plus both min-n rows:

- n=30 k=0: 88.65 (doc 88.6) · n=45 k=2: 85.17 (85.2) · n=60 k=0: 93.98 (94.0) ·
  n=60 k=2: 88.64 (88.6) · n=80 k=3: 89.55 (89.5) · n=100 k=3: 91.55 (91.5) ·
  n=130 k=5: 91.31 (91.3) · n=36 k=0: 90.36 (90.4) · n=36 k=1: 85.83 (85.8) ·
  n=45 k=0: 92.13 (92.1) · n=45 k=1: 88.43 (88.4) · n=3 k=0: 43.85 (43.9).
  Every cell agrees to ≤0.05 pp; differences are last-digit rounding only.
- Min n for lower bound ≥90 %: 35/53/69/84/113 at k=0/1/2/3/5 — matches the doc exactly.
- Min n for lower bound ≥85 %: 22/34/45/55/74 at k=0/1/2/3/5 — matches the doc exactly.

## (d) COBRA screen: jobs, orientation, missing files — PASS

- **Jobs live** (squeue, 2026-09-23, this check): array `40419018_*` `cobralstv` **RUNNING**, 8
  tasks on gvohp nodes voh4–voh7; `40419065` `cobralstv_sum` **PENDING (Dependency)** — exactly
  the reported afterany chain. The untouched COBRA fetch/verify chain was not disturbed.
- **Never reorients on write** (`tools/cobra_lstv_screen.py`, full read): `convert_mha` is
  `sitk.ReadImage` → `sitk.WriteImage` with a round-trip assert on origin/spacing/direction/size
  and no orientation filter; `analyse` reads the mask in its own orientation and derives the
  craniocaudal axis from the affine via `nib.aff2axcodes`. A grep for
  `canonical|reorient|DICOMOrient|OrientImageFilter` finds only the docstrings stating the rule —
  no reorientation API is called anywhere.
- **Skips missing ct_def.mha**: `main` (lines 202–205) checks `mha.exists()`, prints
  "no ct_def.mha yet (skipped; a re-run picks it up)", increments `n_nomha`, and `continue`s
  **without writing a json**, so the resumable skip-if-json-exists logic re-attempts the case on
  the next run once the fetch lands it.

One observation, not a failure: `call_subtype` trusts `has_sacrum` without a caudal-face check, so
a sacrum clipped to a sliver above `--min-vox` (150) at the caudal edge would still count as "the
junction is in field". The per-id `touches_caudal_face` flag is already in every json, so the
summary or the human read of test-set entrants can screen for it without a rerun.
