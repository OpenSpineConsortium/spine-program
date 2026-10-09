# The flagship: one corpus, one super model, one claim

Greg, 2026-09-23 02:00 (verbatim spirit): *wait until all the data is audited and verified against literature
sources; a good synthetic-to-real ratio; splits that prevent leakage and are stratified to train L6 and T13
detection; use all the physics noise parameterisation work; ONE giant database for training and testing; maximise
generalisability of a super model — no held-out device on the flagship unless holding out would improve it; extract
every bit of utility from the whole corpus including the plain films, even if only to plot them in a higher
dimensional space and show the fluoroscopy / plain-film separation; the finished manuscript, the dataset as an
ATLAS card, the model, the whole CLAIM checklist; and experiments showing that while LevelCheck is the ceiling I
cannot match with imperfect registration, I reach parity with or beat surgeon + LevelCheck because I classify
L6 / T13 / sacralised L5 — which, with simple miscounting, is the entire set of reasons for wrong-level surgery.
Design the splits so I can say this.*

This document is the program. Every gate is a file on disk; nothing downstream starts before its gate is closed.

## What the paper claims (Greg, 2026-09-23 03:00) — the frame every gate now serves

The manuscript ships a network, not a feasibility study. Five contributions, and the clinical payload:

1. **Detection on real C-arm fluoroscopy** at the best per-vertebra recall anyone has reported on real
   intraoperative frames — verified against the published comparators in `SchwingNet/CLAIMS_LEDGER.md`, or the
   sentence is rewritten into what is true.
2. **Synthetic-to-real transfer solved for this task**: the model is trained on physics-styled renders and works
   on real frames; the published gap is Pelphix 99.2 % simulated to 71.7 % cadaver, and our own renders-only
   detector sat at 71.67 % on real film.
3. **The per-device C-arm image-formation parameters are released** — nine terms per device, fitted on real
   frames of that device (the Elekta card must be REFITTED on the full COBRA release first: the audit found it was
   fitted on 40 frames from three cases).
4. **The corpus is released**: rendered CT, plain film and real fluoroscopic frames with three-dimensional truth,
   synthetically augmented; the "largest" axis is established against the published corpora before it is claimed.
5. **The weights are released** for inference in the operating room and for retrospective analysis.

Payload: naming the level on a transitional spine (L6, T13, sacralised L5, four-lumbar) at parity with or better
than surgeon + LevelCheck, because transitional anatomy and miscounting are the failure set (gate G6).

**The figure that ties it up (G7):** every transitional phenotype across every modality we hold — CT / three-
dimensional surface, plain DRR, physics-styled DRR, released radiograph, real C-arm frame. Empty cells are named,
not filled with lookalikes. Workflow `transitional-gallery`; sources table
`SchwingNet/results/gallery/GALLERY_SOURCES.md`.

**Morphology synthesis (G4 augmentation, and the future-work paragraph) — LITERATURE FIRST.** The goal is to fill
the thin parts of the cohort's lordosis / kyphosis distribution and to manufacture diversity among the transitional
cases. The method is NOT ours to invent: `docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` (workflow
`spine-synthesis-prior-art`) surveys the published, validated options — statistical shape and shape-intensity
models, anatomically-conditioned diffusion CT synthesis, learned-registration and atlas interpolation, patient-
specific finite-element and articulated models — with what each was validated against, whether code exists, and
whether anyone measured a downstream gain, verifies the top candidates against the papers, and recommends one.
Greg decides from that document; only then is anything built. Whatever is adopted must produce a CT whose digitally
reconstructed radiograph still looks like a radiograph and whose labels stay aligned, and every synthetic variant
keeps its SOURCE PATIENT KEY so a generated copy of a person cannot leak across the split. If the literature has
nothing that meets the requirement, the fallback is pose and projection augmentation only, and the paper says so.

## Gates

| gate | closes when | evidence file |
|---|---|---|
| **G0 data complete** | every D1–D9 directive in `RESUME_2026-09-22_PM.md` repaired or justified in writing; every release count verified against the dataset's paper or release page | `docs/DATA_COMPLETENESS_AUDIT.md` with no open budget/bug/unfinished row; `cobra2026/COBRA_COMPLETE.md` = 692/692 |
| **G1 transitional inventory** | every transitional subject in every source found by its own truth (VerSe raw masks, CTSP release labels, SPINEPS+VERIDAH on TotalSegmentator AND on all 692 COBRA planning CTs, C-ArmLSpine CBCTs), typed by subtype (L6, T13, sacralised L5 / Castellvi where readable, four-lumbar, both) | `SchwingNet/results/transitional_inventory_final.{json,md}` |
| **G2 identity keys** | one person key per case across ALL sources (DICOM/manifest fields first, filename last); anchor-crop renders mapped to their CTSP patients; NHANES to sample person; VinDr to study; COBRA case = patient; phantoms one object each | `~/patient_keys_final.json` + `tools/test_patient_keys.py` PASS |
| **G3 the split** | patient-disjoint, subtype-stratified, device-aware split of the whole corpus (below); leak audit PASS | `~/split_final.json` + `SchwingNet/results/split_audit.md` |
| **G4 the corpus** | EVERY rendered box is a VERTEBRAL BODY box (SPINEPS bodies, `--body-mask-dir`), matching the human annotation; every CT rendered with every device card under the arc pose pools; every real frame exported (all COBRA projections, the case134 spin, case39's third frame, NHANES full, VinDr full); ratio and oversampling per the recipe | `~/corpus_final/` + `SchwingNet/results/corpus_census.md` |
| **G5 models** | evaluation arms (held-out device, held-out transitional) and the flagship (all devices) trained from the same recipe; heads λ=0 and alphabet loss | `SchwingNet/results/final/*.json` |
| **G6 the claim** | the LevelCheck-ceiling / surgeon+LevelCheck comparison computed on the held-out transitional test set with intervals | `SchwingNet/results/levelcheck_claim.{json,md}` |
| **G7 manuscript + cards** | CLAIM checklist every item ticked against a file; ATLAS dataset + model cards regenerated from disk; PDF compiled | `SchwingNet/FINAL_CHECK.md` PASS |

## The corpus (G4) — what goes in and in what role

| source | role in the flagship | how much |
|---|---|---|
| CTSpinoPelvic1K 802, TotalSegmentator v2 1,228 + v3, VerSe 19/20 | rendered CTs: level bank (classifier) + detector renders, every device card, arc poses | ALL; 200–500 renders per CT, transitional CTs first |
| COBRA2026 692 cases (Elekta A–D, Varian F–G) | real frames for the detector; two device cards; the largest REAL transitional test pool (planning CT screened for LSTV) | ALL cases, ALL projections (per-epoch uniform sampler, never a fixed subset) |
| C-ArmLSpine 149 | the intraoperative device: 297 spot frames + case134's 302-frame spin | ALL |
| DeepFluoro 366, Geneva 116, Ljubljana 18 | device cards + real frames | ALL |
| SpineSAC (six C-arms, sawbone phantom) | six more device cards fitted from real frames; bone truth built from the phantom CT + shipped poses; detector frames | ALL |
| NHANES II ~17,000 films (543 annotated) | annotated: level bank + validation; unannotated: detector self-training and the manifold plot | ALL |
| CSXA 4,963, BUU 3,600×2, VinDr 10,466 | level bank + validation; manifold plot | ALL |
| AASCE 457, SpinalAI 8,358, anchor-crop 7,842 | level bank / detector renders where their truth allows (each with a one-line role and its key) | ALL |
| FluoroCap | **dropped from training** (PI decision; reproductions, not fluoroscopy); real-film test only if annotated | 0 in training |
| Mendeley-716 | **excluded**: redistribution of BUU-LSPINE (duplicate subjects) | 0 |

Ratio and oversampling (from `reports/Synthetic real ratio X-ray detectors.md` §6): two stages — synthetic-only
pretraining on the whole render bank under strong randomisation, then full-depth fine-tuning with real frames at
10–20 % of the sampled mix (never beyond 10:1); real transitional frames repeated 4× per epoch; variants in
25–35 % of rendered CTs by CT choice; no parity rebalancing, no weighted BCE; rare recall reported with PR-AUC.

## The split (G3) — designed so the LSTV claim can be made

- **Unit:** the person key (G2). A person is on one side only, across every source and every naming scheme.
- **Strata:** ordinary; L6; T13; sacralised L5; four-lumbar; both. Within each stratum, split by person.
- **Ordinary:** 80 / 10 / 10 train / val / test.
- **Transitional:** **50 / 10 / 40** train / val / test by person, so the test side holds ≥ 60 transitional
  persons (target from G1; if the inventory is smaller than 150 transitional persons, test takes 50 %). The claim
  needs the lower interval bound, and that is set by test n, not train n; the classifier learns the variant from
  the training half under 4× oversampling and the rendered-variant share.
- **Real transitional subjects (C-ArmLSpine L6 patients; COBRA transitional cases; any SpineSAC-like real
  frame of a variant) go to TEST entirely** — never trained on — because the claim is made on real frames.
- **Devices:** the flagship trains on every device. The paper's generalisation numbers come from the evaluation
  arms trained by the same recipe with one device held out (LODO) and from the pooled cross-device holdout; the
  flagship reports its own patient-disjoint test split per device and per stratum. Holding a device out of the
  flagship is done only if the LODO arms show it improves the held-in devices (it will not; that is measured,
  not assumed).
- **Leak audit** before anything trains: `tools/patient_keys.py` + a fresh check that no person key, no CTSP id
  under any of its three naming schemes, no VerSe subject, no NHANES sample person, no VinDr study, no COBRA
  case sits on two sides. Fail = stop.

## The claim (G6) — LevelCheck is the ceiling; surgeon + LevelCheck is the comparator

What LevelCheck is: 3-D/2-D registration of the preoperative CT to the intraoperative radiograph; the level
label on the radiograph is the label the preoperative CT carries. Its published accuracy is registration accuracy;
it imports the name. Its failure set on a correctly labelled CT is registration failure; on a transitional spine
the name it imports is whatever convention the radiologist used, and that is where wrong-level surgery comes
from in the presence of LSTV (the surgeon counts one way, the report another).

Experiments (all on the G3 test split; every number with a person-clustered interval):
1. **Registration ceiling (oracle boxes):** truth boxes with CT-derived names = LevelCheck with perfect
   registration. Naming accuracy 100 % on ordinary spines by construction; on transitional spines, the
   convention disagreement rate: the fraction of transitional test cases where two accepted labelling conventions
   (count from C2 / count from the sacrum / morphology) give different names to the operated level.
2. **Ours, detected boxes:** classifier alone; count alone; coupled (alphabets) — naming accuracy per stratum,
   variant-call sensitivity / specificity per subtype, and the stop-signal rate.
3. **Surgeon + LevelCheck simulated:** the surgeon's count from a landmark on the intraoperative frame
   (our count-from-sacrum) reconciled with the CT-imported label; disagreement on transitional spines is the
   error the combination cannot resolve without a variant call. Compare with ours (2) that names the variant.
4. **Power:** with n transitional test persons and k errors, the Wilson lower bound; pre-stated target: exact
   level correct on transitional real frames with lower bound ≥ 90 %, and the variant detected with sensitivity
   lower bound ≥ 85 %. If the bound is not met, the manuscript says so.
5. **Literature anchors** (each with PMID/DOI): LevelCheck registration accuracy and its clinical series; wrong-
   level rates (Mody 2008, Ammerman 2006, Furuya 2026); LSTV prevalence and its share of wrong-level events.

## Everything else the corpus can give (G5/G6)

- **Manifold plot:** embeddings of every real frame and film (fluoroscopy, kV imager, plain film, DRR, styled
  DRR) in one space (UMAP/t-SNE of the detector or encoder features), coloured by modality and by device; the
  pairwise device separation and the modality boundary quantified (the existing `corpus_manifold` result: devices
  separate pairwise, the film/fluoro boundary does not).
- **Recall vs angle** (renders, and the case134 spin real curve); **real-frame learning curve** per device;
  **per-subtype behaviour** (fused L5 → one box or two; box-size distributions; classifier and coupler calls).
- **Self-training on unannotated NHANES / VinDr films** for the detector, reported as an ablation.

## The deliverables (G7)

`SchwingNet/main.pdf` + supplement; `SchwingNet/atlas/{dataset,model}.json` regenerated from disk;
`SchwingNet/CLAIM_CHECKLIST.md` with every item of `CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx` mapped to
a file; the released model weights in the private registry with the card; `docs/DATASHEET.md` re-derived.
