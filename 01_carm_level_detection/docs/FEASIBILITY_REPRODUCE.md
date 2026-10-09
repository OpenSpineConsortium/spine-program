# Reproducing every number in the feasibility manuscript

One job, `slurm/reproduce_feasibility.sh`, recomputes every figure and table from raw inputs and writes a
ledger. A reviewer runs it, diffs `LEDGER.tsv` against the shipped one, and any stage whose input hashes match
while its output hash differs is the stage to look at. Nothing is cached between stages.

    sbatch -D ~ ~/slurm/reproduce_feasibility.sh
    cat ~/model_night/repro_feasibility/LEDGER.tsv

## What the claims rest on, and where each input came from

| input | what it is | how it was obtained | used by |
|---|---|---|---|
| `~/lstv_flag/lstv_flag_labels_v2.csv` | 1,113 CT spines (802 CTSpinoPelvic1K + 311 VerSe) with a lumbosacral and a thoracolumbar flag each, read from the label voxels; adjudicated Castellvi grade where two radiologists read it | `lstv_flag/derive_*.py` over the v11 release labels and VerSe masks; Castellvi consensus in `CTSpinoPelvic1K/docs/castellvi_consensus.csv` | anomaly manifest, co-occurrence, four-class labels |
| `KIOM2022_dataset_report.xlsx` | BUU-LSPINE authors' own sheets: `L4L6` (129 four-lumbar, 15 six-lumbar), `Pos_AP`/`Pos_LA` (four corner keypoints per lumbar body on 3,600 AP + 3,600 lateral films, S1 superior end-plate on lateral), `Pixel Spacing` (0.175 mm) | shipped inside the public BUU-LSPINEv1 download | geometric indices, real-film anomaly ground truth |
| `~/allspine_v2_fov96_ctx/` | 8-source context-crop bank (real films: CSXA, BUU, NHANES; renders: CTSP, VerSe, physics) | `tools/make_context_crops.py` | 98.32% anchor-free measurement, claims run A |
| `~/allspine_v5_fov96_ctx/` | 14-source bank, 253,763 crops, incl. VinDr and the pseudolabelled films | `tools/build_allspine_v3.py` lineage; label origin per source in `source_quality.json` | claims run B, source quality |
| `model_r18_ce.pt`, `model_r18_ce_v5.pt` | ResNet-18 encoders, 27-class cross-entropy, trained on v2 and v5 | `tools/night_train.py`; registered in `~/model_registry` | all model-based stages |
| `head_allspine_v2_…_seed0.pt`, `head_r18_ce_v5_v5.pt` | BiGRU run-level heads, mixed-length training | `tools/head_mixed_length.py`; each head's sidecar JSON names its encoder | anchor-free, claims |
| `~/ctsp_drr ~/verse_drr ~/physics_drr ~/physics_rare` | DRR renders with per-render level boxes carried from CT | `tools/aasce_to_drr.py` lineage / physics renderer | global signature, FOV separability |
| `~/vindr_pseudo ~/nhanes_pseudo ~/lateral236_pseudo` | decoder outputs on real films, one JSON per film with `spine_config`, `config_posterior`, `levels` | `tools/pseudolabel_real_films.py` | manifest tier B, decoder-fires-blind finding |
| `~/FluoroCap/captions_matched_lstv.jsonl` | literature figures whose caption names transitional anatomy | FluoroCap harvest, TRANS_RE gate | manifest tier C only; no number in the paper depends on it |

## The stages, in order, and the number each one owns

| # | stage | tool | output | owns |
|---|---|---|---|---|
| 1 | anomaly manifest | `tools/anomaly_manifest.py` | `anomaly_manifest/spine_classes.json`, `anomaly_manifest.csv` | 749 anomalous spines in three tiers; 902/98/47/66 four-class counts; the 0-of-65 junction-in-frame finding on VinDr pseudolabels |
| 2 | geometric indices | `tools/geometric_indices_buu.py` | `geometric_indices/geometric_indices_buu.json` | Wigh-band coverage 5.1%; sacral slope AUC 0.73 for six-lumbar; L5–S1 gap AUC 0.99 for four-lumbar |
| 3 | source quality | `tools/source_quality_report.py` | `source_quality/source_quality.json` | per-source label origin and crop quality; 45.8% from CT, 30.0% pseudo, 14.1% human, 10.2% counting |
| 4 | global signature | `tools/eval_global_anomaly_signature.py` | `global_signature/global_signature.json` | within-source AUC of a distant vertebra for spine class |
| 5 | FOV separability | `tools/eval_fov_separability.py` | `fov_separability/fov_separability.json` | four-class balanced accuracy against window length, junction-free and junction-seen |
| 6 | feasibility claims | `tools/eval_feasibility_claims.py` (×2 pairings) | `feasibility_claims/{v2_ce,v5_ce}/feasibility_claims.json` | C1 unanchored accuracy by anomalous/ordinary; C2 per-level L1–L5 in State C; C3 signed-offset error structure |
| 7 | anchor-free | `tools/eval_anchor_free.py` | `anchor_free/anchor_free_head.json` | 98.32% [98.17, 98.46] on 28,547 unanchored vertebrae |

Co-occurrence is computed directly from stage 1's input; the quotable figures are the 280-subject exact OR
3.61 [2.08, 6.27], morphology-only 3.2 [1.8, 5.8], and both-junctions-in-field 2.1 [0.9, 5.0]. The all-rows
4.30 is inflated by count-coupling and by 31 unknowns scored negative; the pooled cross-cohort OR is Simpson's
paradox and is not reported.

## Stages added after the adversarial audit (2026-09-17)

| # | stage | tool / job | output | owns |
|---|---|---|---|---|
| 8 | interior windows | `tools/eval_interior_windows.py` / `slurm/interior_windows.sh` | `interior_windows/{v2_ce,v5_ce,v6_ce}/interior_windows.json`, `failures/` | pixel-defined anchor-free naming with film-cluster CIs and structural baselines; failure contact sheets. **Supersedes** the label-defined 98.32% / 87.2%. |
| 9 | BUU schema correction | `tools/correct_buu_schema.py` | `~/films_drr_buucorr/{ann,CORRECTION_SUMMARY.json,review/}` | S1a→L6 on 15 six-lumbar studies (per-study resize fit, residual ≤1 px), L5 sacralised on 129; reader review package |
| 10 | data fixes | `slurm/data_fixes2.sh` | `film_match/{film_match_measure,film_match_params}.json`, `~/pseudo_filtered/`, `~/allspine_v2fm_fov96_ctx` | fitted film-noise model; anchored-only pseudolabels with human agreement by region; film-matched render bank |
| 11 | v6 | `tools/build_v6_bank.py` / `slurm/v6_chain.sh` | `feasibility_claims/v6_*` | no anomalous BUU film in training; anomalous CT renders ×4; CE and CORN encoders |
| 12 | scaling sweep | `tools/subset_bank.py` / `slurm/scaling_sweep.sh` | `scaling/SCALING_CURVE.json` | accuracy vs synthetic fraction (0/0.25/0.5/1) and real fraction (0.25/0.5) |
| 13 | film-look LoRA | `tools/film_style_dataset.py` / `slurm/train_film_lora.sh` | `~/fluorogen/lora_film_v1/` | SDXL LoRA on public X-ray datasets only, equal weight per (dataset, region); FluoroCap excluded by assertion |
| 14 | film-look renders | `tools/label_preservation_gate.py` / `slurm/film_lora_apply.sh` | `~/*_drr_film`, `film_apply/gate.json`, `~/allspine_v2sd_fov96_ctx` | DRRs passed through the LoRA under Canny control; encoder-agreement gate; bank with renders replaced |
| 15 | explainability | `tools/explain_level_model.py` / `slurm/explain.sh` | `explain/explain.json`, `prototypes_*.png` | region-occlusion ablation per level, Grad-CAM, embedding silhouettes, prototypes, probes |

## Environment

Two conda environments, exported without build strings to `env/spineps.yml` and `env/fluorogen.yml`; how
to recreate and verify them, and what the YAML cannot carry (GPU driver, SDXL weights, TeX, credentialed
data), is in `env/README.md`. `tools/audit.sh` verifies the environments, line endings, that every job's
tools exist, static analysis, and the smoke tests in `tests/test_feasibility_tools.py`; it is the first
stage of `slurm/reproduce_all.sh`.

## Discarded on the way, and why (so nobody re-runs them)

- `feasibility_claims` with `head_r18_corn_v5_v5.pt` + `model_r18_ce.pt`: head/encoder mismatch, 0–1% with a +2 shift.
- `fov_sep` / `global_sig` jobs 40321204/40321205: started before `spine_classes.json` had `per_case`; fell back to 802 cases.
- `anomaly_cooccurrence_labels.json`: the voxel recount processed one case.
- `data_fixes` job 40321763: the first film-noise knobs gave 10× the real noise; cancelled before the bank finished, bank removed.
- The label-defined "decoder fires blind" finding (65/65 vs 0/1,127): a tautology of the pseudolabel script's demotion; retracted.

## Things a reviewer should know before trusting a number

- **A head decodes only the encoder it was trained on.** Pairing the newest head in a directory with a
  different encoder produced 0–1% accuracy with a systematic +2 offset. The ledger records the sha256 of both
  files for every model stage; the sidecar JSON beside each head names its encoder.
- **Two runs of the separability and signature stages were discarded** because they started before
  `spine_classes.json` carried `per_case` and silently fell back to the 802-case manifest. Their logs are kept
  under `~/model_night/logs/` (jobs 40321204, 40321205); the reported numbers are from 40321225 and 40321226.
- **Unresolved films are dropped, not assumed ordinary.** In the claims stage, 5,102 held-out films had no
  anomaly ground truth from either the CT flag table or the BUU sheet and are excluded from the
  anomalous/ordinary split. Reading absence of evidence as absence of anomaly manufactures specificity.
- **BUU negatives are contaminated.** The L4L6 sheet records a count anomaly only; a Castellvi I–IV on a
  five-lumbar spine is in the negatives. Every AUC against BUU is a floor.
- **The pooled global-signature AUC is not the result.** Rare-case renders are built from anomalous spines,
  so a pooled probe can score by recognising the collection. Only within-source rows are reported.
- **VerSe is enriched.** 130 of 311 spines carry a lumbosacral flag. Prevalence must never be quoted from it;
  co-occurrence odds ratios are within-cohort and reported beside CTSP's.
- **NHANES contributes zero anomalies structurally.** Its films are cervical (C3–C7); `p_variant` sits at
  the prior 0.0288 on all 16,234. This is not a detector failure.
