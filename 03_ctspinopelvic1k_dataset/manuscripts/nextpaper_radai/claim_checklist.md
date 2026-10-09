# CLAIM 2024 checklist (Checklist for Artificial Intelligence in Medical Imaging), to fill

Reference: Tejani AS et al., Radiology: Artificial Intelligence 2024 (CLAIM 2024 update);
original: Mongan J, Moy L, Kahn CE. Radiology: AI 2020;2(2):e200029. The journal requires the
completed checklist as a supplement. Item numbering follows CLAIM 2024; answer with the
manuscript page/section, or "N/A" with a reason.

| # | item | where |
|---|---|---|
| 1 | Title: identifies the study as AI/ML | title |
| 2 | Abstract: structured, purpose, methods, results, conclusion | abstract |
| 3 | Introduction: scientific and clinical background, role of AI | intro |
| 4 | Study objectives and hypotheses | intro, last paragraph |
| 5 | Study design: retrospective; prospective components | M&M design |
| 6 | Data source: institutions, dates, public collection (TCIA CT Colonography) | M&M data |
| 7 | Eligibility criteria: inclusion of one acquisition per patient, bone-richest | M&M data |
| 8 | Data pre-processing steps: resampling, remap of labels, derived disc space | M&M network |
| 9 | Selection of data subsets: five patient-level folds, LSTV stratification | M&M network |
| 10 | Definitions of data elements: label scheme (68 ids), transitional subtypes | Table 1, M&M |
| 11 | De-identification methods | public de-identified data |
| 12 | How missing data were handled: ignore label for unannotated regions | M&M network |
| 13 | Reference standard definition: labels; Castellvi two-reader consensus | M&M data |
| 14 | Rationale for choosing the reference standard | M&M data |
| 15 | Source of ground-truth annotations; annotator qualifications (13 trained annotators, 2 radiologists) | M&M data |
| 16 | Annotation tools | M&M data (ITK-SNAP, review tool) |
| 17 | Measurement of inter- and intrarater variability; adjudication | M&M data (Castellvi consensus) |
| 18 | Intended sample size and how it was determined | M&M stats (public cohort; power for count rate) |
| 19 | Data partitions: training/validation/test with numbers | M&M network |
| 20 | Level at which partitions are disjoint: patient | M&M network |
| 21 | Model description: nnU-Net v2 ResEnc-L, inputs, outputs, layers | M&M network, Fig 1 |
| 22 | Software libraries, frameworks, packages, versions | M&M stats |
| 23 | Initialization of model parameters: random | M&M network |
| 24 | Training details: augmentation, hyperparameters, oversampling, epochs, loss | M&M network |
| 25 | Method of selecting the final model: fixed 500 epochs, checkpoint best | M&M network |
| 26 | Ensembling: none / per fold | M&M network |
| 27 | Metrics of model performance and rationale | M&M stats |
| 28 | Statistical measures of significance and uncertainty: bootstrap CIs, McNemar | M&M stats |
| 29 | Robustness or sensitivity analysis: transitional vs typical, hardware | Results |
| 30 | Methods for explainability or interpretability: the decoder's posterior; instance masks | M&M decoder |
| 31 | Validation on external data: none; competitors on the same internal data | Discussion limitation |
| 32 | Flow of participants/scans with numbers at each stage | Results, Fig/diagram |
| 33 | Demographic and clinical characteristics | Results, Table 1 |
| 34 | Performance metrics on the optimal model, with CIs | Results, Table 2 |
| 35 | Estimates of diagnostic accuracy and precision | Results |
| 36 | Failure analysis of incorrectly classified cases | Results, where competitors fail |
| 37 | Study limitations | Discussion |
| 38 | Implications for practice, including intended use | Discussion |
| 39 | Registration number and registry | N/A (not a trial) |
| 40 | Where the full study protocol can be accessed | GitHub repo |
| 41 | Sources of funding and other support; role of funders | title page |
| 42 | Data, code and model availability statements | end of main text |
