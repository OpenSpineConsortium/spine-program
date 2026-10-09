# Revision plan: "Not All Spines Are Created Equal" (neurips_2026.tex), September 2026

What changed since the May draft, and where each change lands in the manuscript. Items
marked PENDING wait on the one-shot folds (Dataset810, launched 2026-09-07, expected ~12
September) or on detect_v2 (radiograph corner detector, training now).

## 1. The dataset is v10, not the May v3 tree

| May draft says | v10 fact | where |
|---|---|---|
| 1,153 records / 802 patients, fused 342, separate 352, spine-only 90, pelvic-only 20 | 802 records, one per patient, on the patient's bone-richest acquisition; separate-mode pairs held out by design (351 patients) | §Dataset, Table scan_stats |
| merged 9-class scheme (last_lumbar) | 68-identifier scheme: VerSe vertebrae 1–25 (L6 = 25), sacrum 26, T13 28, S1 29, hips 30/31, femora 32/33, thirteen ribs per side 34–46 / 47–59, lumbar ribs 60/61, hardware 62–68 | §Dataset |
| no ribs, no femora, no hardware, no S1 | per-level ribs (5,749 evaluable, 0.035% offset), femora, a carved S1, 11 instrumented records with hardware as its own class | §Dataset |
| Castellvi: two residents jointly | two-reader consensus on 33; null means ungraded, not normal | §Castellvi |
| 6-way count taxonomy from filename qualifiers | keep, but add the thoracolumbar axis: 98 stump twelfth ribs (ratio < 0.33), 16 lumbar ribs, 18 six-lumbar records, 9 four-lumbar records whose fused segment sits inside S1 | §Dataset, new paragraph |
| validation: not stated | three layers: geometric invariants 802/802, rib–vertebra incidence, spinopelvic measures vs published values | §Dataset, new paragraph |
| Zenodo/HF pointers | Zenodo 10.5281/zenodo.22139642 (v10 = 22642578), build archive 22647933, HF OpenSpineConsortium/CTSpinoPelvic1K, code OpenSpineConsortium/CTSpinoPelvic1K tagged v10-build-archive | §Data availability |

## 2. The method: from a merged-label baseline to one-shot identity plus a decoder

- Keep §Spinopelvic Baseline (Dataset803, merged last_lumbar) as the baseline it is.
- New §"One-shot level identity": Dataset810, 24 classes (T10–T13, L1–L6, sacrum, ribs 1–11 pooled, rib 12, rib 13, lumbar rib per side, hips, femur, ignore), ResEnc-L at the 100 GB target (patch 256×320×320, batch 2), nnUNetTrainerWandB_500ep_LSTVOversample with the oversampling pool extended to lumbar-rib and T13 carriers (half of every queue), patient-grouped LSTV-stratified five folds, trained from NFS with the dataset unpacked once.
- New §"Sequence decoder": instances per name class, per-instance thoracic/lumbar/sacral probability from the softmax, rib contact, monotone decode → posterior over the rib-free count, and the A/B/C readings for six rib-free bodies with the double shift reported (tools/decode_sequence.py). Self-test on one-hot ground truth: 4/4 exact.
- Why the merged baseline could not answer the question (it erases L5/L6 and has no thoracic or rib classes) and why the one-shot target is the right test of "identity is local".

## 3. Results to add

- Shape separability (already computed): thoracic vs lumbar AUC 0.998; T12 vs L1 AUC 0.990, 97.3% over 1,485 vertebrae, features normalised by the patient's own median; transverse-process span dominates.
- Six-lumbar readings from the labels (scripts/six_lumbar_readings.py + shift_hypothesis_test.py): 11 true L6, 4 lumbarized S1, 1 aplastic-rib T12, 2 both-ends; controls 37/40 favour their labels; figure results/six_lumbar_readings/six_lumbar_readings.png; the reading sheets.
- Co-occurrence: stump ribs 98/788 (12.4%), lumbar ribs 16 (2.0%); stump with sacralization 4/14 vs 94/758, OR 2.8, p 0.09; no lumbar rib among 14 lumbarizations.
- PENDING one-shot folds: per-class Dice typical vs transitional; rib-free count accuracy by status; rib confusion by class; lumbar-rib and T13 emission; decoder posterior on the 18 six-lumbar records vs the label-based readings (tools/eval_oneshot.py, tools/decode_sequence.py).
- PENDING radiograph extension (spine-detector): 33,943 instances on 5,401 films (BUU 19,991; AASCE 8,069; NHANES 3,217; Mendeley 2,666); detect_v1 AP50 0.957 / PCK@0.1 0.77 on 558 instances; detect_v2 (120 ep, done 2026-09-08, runs/detect_v2/eval on the grid): AP50 0.970 / PCK@0.1 0.812 / PCK@0.2 0.942 on the same 558; film (NHANES) 0.960 / 0.852 / 0.946, standing DR (Mendeley) 0.970 / 0.767 / 0.937. Validation during training (535 films, 3,408 instances): box mAP50 0.991, pose mAP50 0.977.

## 4. Discussion

- Replace "downstream Castellvi-aware reasoning (VERIDAH-style global count constraints or a Type III head)" with what was built: the local-identity network plus the sequence decoder, and what it can and cannot decide (L5 vs L6 is a count; the bottom body's type is not).
- Development: the six-lumbar readings put the extra segment at the lumbosacral end (A or C), not the thoracolumbar end; a single homeotic shift predicts the rib/LSTV pairings; VerSe transfer tests it at scale.
- Surgery: origin of the border vertebra decides the mobile junction, pedicle size and trajectory, the exiting root, and the endplate the pelvic parameters were measured on.
- Limitations: no C2 in any scan, so readings are morphological consistency; 33 grades; supine screening cohort; ribs are triaged-review pseudolabels.

## 5. Related work to add

Du Plessis 2018 (J Anat 232:850), Poolman 2023 (J Anat 243:311), Nagata 2025 (Skeletal Radiol 54:2169), VERIDAH (Möller 2026) as the labelling comparator, SPINEPS.

## Order of work

1. Dataset section and tables to v10 (no results needed) — now.
2. Method sections (one-shot + decoder) — now.
3. Label-based results (separability, six-lumbar readings, co-occurrence) — now, with figures copied into figs/.
4. Fold results and detect_v2 — when they land.
5. Abstract, introduction and discussion rewritten last, once the numbers are in.
