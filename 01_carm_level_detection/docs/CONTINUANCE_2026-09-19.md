# Continuance point, 2026-09-19 ~17:00 EDT

Written so the next session can pick up every in-flight item without re-deriving it. Read this, then
`docs/PIPELINE_RESUME.md` and `tools/pipeline_state.py`.

## Done and pushed (branch L6_Class, up to 4aa0e2d)

- Every CT-render sweep number re-measured on respaced renders (`~/model_night/sweep_v3/`; mirror
  `laptop:model_night\sweep_v3`). Manuscript `paper/rsnai/main.tex` (23 pp, builds clean),
  tables via `tools/make_results_table.py`, `docs/SWEEP_PROTOCOL.md` all on sweep_v3.
- Findings recorded in the manuscript: end-of-sweep rule ("last move is a full move or none":
  120/120 on CTSP, 98.5% on TS); detector on films 21/25 with unlabelled-body exemption; one open
  decoder error (film 00378); rib oracle adds nothing; stitching improvements help only at o3/o4;
  TotalSegmentator bench (522 sacrum-anchored, 203 C2-anchored unseen CTs).
- Tools: `sweep_map.py` gained `--end-rule`, `--last-link`, `--hybrid local`, `--node-merge/--node-order`
  (opt-in), `--rib oracle`, unlabelled-node scoring, `node_P` records; `make_drr_dataset.py` got
  `pir_spacing` + `--respace`; `ts_to_drr.py`, `rib_bearing_ann.py` new.

## Running on the grid (check with squeue / the log paths)

| what | job / path | check | then |
|---|---|---|---|
| SPINEPS+VERIDAH over TS+VerSe (1602 CTs, 12 shards) | array 40384988; out `~/bench_ts/spineps/native/`; logs `~/model_night/logs/spineps_tv_*.out` | `ls ~/bench_ts/spineps/native/*_seg-vert_msk.nii.gz \| wc -l` (1126 at 16:51) | score VERIDAH L6/T13 calls on VerSe truth (VerSe ids 25=L6, 28=T13 in `_seg-vert_msk`), then census on TS; compare with the sweep decoder's calls (`sweep_v3/ts/*` `variant_call`) |
| RSNA 2022 cervical CT bundle | `~/data/rsna_cspine/` via `slurm/rsna_cspine_fetch.sh` (nohup, log `fetch.log`) | `du -sh`, `RSNA_FETCH_DONE` in log | unzip; DICOM→NIfTI; SPINEPS; render for C2 sweeps. **Rotate the Kaggle token** afterwards (it is in the chat transcript). |
| RibFrac + RibSeg v1 + Möller manual rib masks | `~/data/ribs/` (`dl.sh`, log `dl.log`, `RIBS_DL_DONE`); RibSeg v2 at `~/data/ribs/ribseg_v2.zip` (661 numbered rib masks + centrelines) | log | unzip; SPINEPS for vertebrae; render; rib-count anchor (first rib → T1) as a new anchor type; rib-count variant census |
| TotalSegmentator v3 unzip | `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300/` (`unzip.log`, `UNZIP_DONE`) | `ls \| wc -l` (610/1939 at 16:51) | `sbatch --export=SRC=~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300,DST=~/ts_drr_v3 slurm/ts_drr.sh`; diff v2 vs v3 labels on common ids; separate paediatric by `meta.csv` age; rerun `sweep_v3` TS arms on `ts_drr_v3` |
| disk census | `~/du_home_top.txt` (done) | — | candidates NOT deleted, user's call: `spine-detector` 382G, `spinesurg-ct-nnunet` checkout 363G (nnunet data inside), `FluoroCap` 316G, `ablate` 235G, `u251-xenograft…` 194G (other project), `implant_verse` 187G, `scaling` 130G, `.cache` 104G, `nhanes_pseudo` 74G, `allspine_v5*` 120G. Quota 3.78 of 4.29 TB soft. |

## The scoping review build (workflow wf_04a13df2-fe8)

Directory `spine_data_review/` (self-contained; venv `~/sdr_venv` in WSL; credentials
`~/.fluorocap/credentials.env`, never printed — NCBI/S2/Springer keys live, Kaggle token added,
PhysioNet username/password to be added by Greg). Protocol final after two adversarial passes:
`PROTOCOL.md`, `PRISMA-ScR_checklist.md`, `charting_schema.json`, `quality_rubric.md`,
`statistical_analysis_plan.md`, `information_sources.md` (verbatim per-source query strings).
Code under `sdr/` (common, creds, ids, search_literature, search_repositories, dedup_prescreen, chart,
availability, quality, stats, figures, manuscript, recipe), `queries/*.yaml`, `manuscript/`, `recipe/`,
`tests/`. The workflow reached Verify round 1: reviews of all modules are in the journal (issues per module), but the fix agents, re-reviews and the smoke run FAILED on the account's session limit (resets 17:10). Resume it (command below) — cached stages replay, the fixes re-run. Journal: `laptop:.claude\projects\<laptop project slug>\
f1bdbd78-151f-470b-b703-dd9af9b3fecc\subagents\workflows\wf_04a13df2-fe8\journal.jsonl`. To resume a
killed run: Workflow({scriptPath: ".../workflows/scripts/spine-data-review-build-wf_04a13df2-fe8.js",
resumeFromRunId: "wf_04a13df2-fe8"}). **Nothing under spine_data_review/ is committed yet** — commit it
once the smoke run passes (no data, no `runs/*/raw/`).

### Amendments to apply BEFORE the first real search (pre-registration amendments, logged in
PROTOCOL.md §19 as Amendment 1–4, then regenerate query strings via `sdr/terms.py` so
`tests/test_terms.py` passes)

1. **Ribs in scope.** Rib datasets (per-rib labels, rib fractures, rib segmentation) eligible as their
   own category; `rib*` enters BLOCK_S; charting gains `rib_labels` (per-rib instance yes/no) and
   `rib_to_vertebra_assignment`; RibFrac/RibSeg move from `I1-test` to `recall` in
   `screen/known_items.csv`.
2. **Field-of-view tier, both modalities.** Population = public CT and projection-radiography datasets
   whose field of view includes at least one vertebral body. Tier 1 = spine-claimed/annotated (full
   charting). Tier 2 = neck/chest/abdomen/pelvis/trunk/whole-body CT (trauma pan-scans, PET/CT,
   low-dose screening, cardiac) and any radiograph including the thoracic or lumbar spine (chest films
   incl. laterals, abdominal, pelvic/hip, whole-body DXA, scoliosis, fluoroscopy), annotated or not,
   charted on the same form with `spine_labels=none` and a `key_slices_only` flag. BLOCK_S gains body-region
   terms (chest, thorax, thoracic CT, abdomen, abdominal, pelvis, pelvic, whole-body, trauma, polytrauma,
   low-dose, lung screening, neck). Statistics reported per tier; the variant meta-analysis stays on
   datasets with per-subject labels. Recipe gets `pseudolabel_ready`.
3. **Projection as a stratification.** Per dataset: counts lateral / AP-PA / paired / oblique /
   unknown (derivable from MIMIC `ViewPosition`, CheXpert Frontal/Lateral, PadChest projection);
   tables, storage plan and recipe split by projection; `--projection lateral` preset; per-file
   lateral-only fetch where the repository serves files (PhysioNet does).
4. **Storage planning fields.** `size_gb_download`, `size_gb_unpacked`, `n_volumes`/`n_images`,
   `bit_depth`/format (DICOM vs JPEG both recorded — whether 8-bit JPEG suffices for the thoracic
   spine behind the mediastinum is UNTESTED; test on ~500 MIMIC studies before committing TB),
   `recipe/storage_plan.py` summing by tier/route/projection with a preprocessing multiplier; an
   **"actions for Greg" checklist** (PhysioNet agreements: MIMIC-CXR, MIMIC-CXR-JPG, VinDr-CXR,
   VinDr-PCXR; registrations: PadChest, MIDRC, Stanford AIMI/CheXpert, grand-challenge; applications:
   NLST/CDAS, UK Biobank, MrOS/SOF; author requests: SX-Stitch draft at
   `docs/data_requests/SX-Stitch_request.md`).

### Then, in order
1. `make search` from WSL (network there) with `--run-date`, commit `runs/<date>/records/` + counts.
2. Dedup + prescreen → `screening_sheet.csv`; reviewer decisions recorded; LLM-assisted pass named.
3. Charting (agents, adversarially verified) → `data/charting/*.json`; availability probes; quality;
   stats; figures; manuscript build; recipe + storage plan; commit; push.
4. Run the recipe on the grid (quota!) → all Tier 1 + lateral Tier 2 first.


## Added later on 2026-09-19 (evening)

- **Introduction** carries the verified cost/burden evidence (`docs/WRONG_LEVEL_COST_EVIDENCE.md`,
  `docs/WRONG_SITE_BURDEN_EVIDENCE.md`, `docs/SWEEP_TIME_EVIDENCE.md`; each claim has 3 refutation votes).
- **QI paper** `paper/qi_universal_protocol/` (8 pp, builds): the Universal Protocol performed WITH the level
  map (verification = target entered; site mark = sweep + digital fiducial; time-out = fiducial vs count).
  Two bib placeholders: mongardi2021 (PMID 33358493), keil2024 (PMC11476588).
- **Caterpillar / digital fiducial** `tools/fiducial_walk.py`, `slurm/fiducial_walk.sh` → `~/model_night/fiducial/`:
  hybrid decoder, true boxes: CTSP 950 walks 94.5% correct (96.3% of reached, 2.0 exposures); TS 7,405
  walks 92.2% (lumbar 96.2, thoracic 91.6, cervical-from-sacrum 80.4). Errors one body off; three CTSP
  spines have FOUR lumbar bodies (no alphabet) → `--alphabets ext` (four-lumbar + T13 variant,
  `slurm/sweep_l4.sh` → `sweep_v3/l4/`): CTSP o2 chain naming 96.7→98.0, K2/3/4 95.2/94.7/94.8 →
  96.9/96.4/96.6; TS −1 pt (labels cannot express it). Opt-in. **CTSP v11 COLONOG_299 has a misplaced L5
  label between T12 and L1 — report to the dataset.**
- **Pure counting** (`--naming count --anchor cranial`, no model; `slurm/count_walk.sh` →
  `~/model_night/count_walk/`): VerSe from C2, o2: 832/834 walks (99.76%) on 76 spines; the two misses are
  one cervical scan (12 px pitch at 1.25 mm slices) where a link paired nothing. TS C2 / o3 / sacrum arms
  pending at the time of writing — read `count_walk/*/fiducial.json`.
- **Time budget** (verified): C-arm move 36–49 s, exposure <1 s, our compute <1 s per walk; lumbar walk
  ~1–2 min, mid-thoracic ~2–3 min vs ~15 min for fluoroscopic counting and 14 min CT-suite for a fiducial.
- Review build resumed after the 22:10 limit reset (run wf_04a13df2-fe8); still uncommitted.

## Other open items
- SX-Stitch data request drafted (docs/data_requests/); Greg to send.
- `paper/rsnai/main.tex` is 23 pages; check the venue's limit.
- The v2-era detector arms' `box_repair=None` explains why film 00468's duplicates vanished under the
  current tool (box repair on, conf 0.25); noted in the manuscript's detector paragraph implicitly.
