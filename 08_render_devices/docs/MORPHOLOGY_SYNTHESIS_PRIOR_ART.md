# Morphology synthesis for spine CT — what the literature actually validates

A27. Compiled 2026-09-23 from six search angles (`research_notes/spine synthesis prior art/`:
`ssm.md`, `diffusion.md`, `registration.md`, `biomech.md`, `rare-variant.md`, `downstream.md`, plus five
adversarial verification files). Literature only. **Nothing is implemented, nothing was run on the grid,
the manuscript is untouched.** Every number below was read off the cited source; where a source would not
open, that is said rather than filled in.

Requirement being judged against: labelled CT in (~2,900 held: CTSpinoPelvic1K 802, TotalSegmentator
1,228, VerSe ~374; 86 carry a transitional variant) → NEW anatomically plausible volumes WITH aligned
labels, realistic enough that a DRR cast from them looks like a radiograph, steerable to a target
lordosis/kyphosis/PI or a transitional phenotype, population-plausible.

---

## 1. Recommendation

**No published method meets the requirement, and one part of it — manufacturing a transitional vertebra —
has never been done by anyone, in any modality, on any anatomy that is named by its position in a chain.**
What the field actually does instead, and what we should do, in this order:

1. **Keep the control condition.** Every spine challenge winner, TotalSegmentator, SPINEPS and VERIDAH
   train on affine + intensity augmentation; nnU-Net deliberately removed elastic deformation and its
   successor never reinstated it. This is the published state of the art, not a fallback.
2. **For the transitional scarcity, the only measured lever is real rare cases, oversampled.** VERIDAH
   (arXiv 2601.14066): delete the labelled anomalous cases and thoracic-anomaly recall collapses
   **87.80% → 32.93% (T2w) and 96.30% → 25.93% (CT)**. No synthesis method has recovered that.
3. **If we want anatomical variation at all, adopt one published mechanism: PolyPose** — Gopalakrishnan V,
   Dey N, Golland P, *PolyPose: Deformable 2D/3D Registration via Polyrigid Transformations*, NeurIPS 2025,
   arXiv:2505.19256, PMID 40492249, PMC12148084, code `github.com/eigenvivek/polypose` (**MIT**, verified
   today) — validated on **DeepFluoro, 6 cadavers, pelvis Dice 0.99, femurs 0.98, HD95 1.48/1.56 mm,
   0.00% topological folds**, on the exact cohort we already hold, bounded by Panjabi's segmental ROM, and
   reported as a **measured, possibly negative** augmentation experiment, because nobody has ever run one.

**It cannot make an L6, and neither can anything else in the literature.** Say that in the paper.

---

## 2. The ranked table

Ordered by strength of evidence against our requirement, not by novelty. "Validated" is the single number
that carries the claim; where a paper has none, that is the entry.

| # | Method (citation) | What it generates | How validated (number) | Code / licence | Spine? | Verdict | Effort |
|---|---|---|---|---|---|---|---|
| 1 | **Real rare cases + anomaly-aware labelling** — VERIDAH, arXiv 2601.14066 | nothing; it trains on real anomalies | ablation: remove labelled anomalies → thoracic recall **87.80→32.93% (T2w), 96.30→25.93% (CT)**; 99.18% of CT subjects fully correct vs 77.26% | ships with SPINEPS | yes | **ADOPT** (this is the control we must beat) | none; already held |
| 2 | **Projection + appearance domain randomisation from real labelled CT** — SyntheX (Nat Mach Intell 2023); AnyCXR arXiv:2512.17263 | labelled radiographs from real CT; **no anatomy synthesis** | SyntheX: 20 CTs, beat a real-data-trained model on real X-ray. AnyCXR: 2,982 CTs → 126,410 renders, zero-shot real CXR DSC **94.53 (PA) / 91.35 (LA)** vs 91.62 / 85.98 baseline | SyntheX/DeepDRR public | our modality | **ADOPT** — already our pipeline | none |
| 3 | **PolyPose polyrigid warp** — NeurIPS 2025, arXiv:2505.19256 | warped 3-D CT + fold-free displacement field; labels ride along | DeepFluoro 6 cadavers: pelvis **0.99**, femurs **0.98**, HD95 **1.48/1.56 mm**, **0.00% folds**; Head&Neck 31 patients rigid Dice >0.90 | `github.com/eigenvivek/polypose` **MIT** | validated on pelvis/femur; DeepFluoro is ours | **ADOPT as the mechanism** — but it has **zero downstream numbers**, ever | 2–3 wk to first render |
| 4 | **Log-Euclidean poly-rigid framework** — Arsigny 2003 / 2006 / JMIV 2009; POLAFFINI, IPMI 2023, arXiv:2407.03922 | same transform class, CPU, regions defined by a label map | invertibility is a **theorem**, not a Jacobian check; POLAFFINI beats affine init on brain MRI registration | `github.com/CIG-UCL/polaffini` **Apache-2.0** (LICENSE.md read today: Copyright 2025 A. Legouhy) | no (spine instantiations: Drobny 2020, Bukas 2021) | **ADOPT as the name and the citation**; ADAPT as CPU fallback | days |
| 5 | **Anatomy-informed augmentation** — Kovacs, MICCAI 2023, arXiv:2309.03652 | deformed image + label, organ-driven | 774 biopsy-confirmed exams, **+4 of 76 lesions (5.3% rel.) at 0.32 FP/scan**, bootstrap- and t-test-significant | `github.com/MIC-DKFZ/anatomy_informed_DA` **Apache-2.0**, nnU-Net v2 fork | no (prostate) | **ADAPT** — copy the validation design, not the deformation | 1 wk |
| 6 | **Statistical Shape and Intensity Model augmentation** — Schmid, Eur Radiol Exp 2023;7:39 | real host CT, TPS-warped, synthetic bone painted in; label from the tet mesh | intensity encoding error **<10%**; basic+SSIM **0.95 / 6.16 mm** vs basic **0.93 / 7.35 mm**; **SSIM alone was not significant** | none released (TetGen AGPL if reimplemented) | **hip** | **ADAPT** if ported; not a fix for the tails | 3–6 wk |
| 7 | **Type-conditioned shape generation across a topology change** — SDF4CHD, Med Image Anal 2024, PMC11372630; SV-Cine arXiv:2609.12997 | shape (SDF) carrying a discrete phenotype, then a painted image | **type correctness 47/50 vs 2/50** for conditional DeepSDF; downstream whole-heart 84.7→86.3; SV-Cine **RV Dice 0.36→0.72**, and **0.14** with the conditioning removed | generator promised; URL not located | heart | **ADAPT** — the only published design that crosses a topology change; porting it is **new method work** | months |
| 8 | **Synthesise the label map, then paint it** — brainSPADE, SASHIMI@MICCAI 2022, arXiv:2209.08256 | synthetic anatomy maps + images, rare class conditioned | real+synthetic tumour Dice **0.813→0.876**, recall 0.773→0.852; synthetic-only **lost** in-distribution on every tissue class | `github.com/virginiafdez/brainSPADE_MICCAI` | brain, 2-D | **ADAPT** (design only) | months |
| 9 | **Vertebra-level inpainting** — Bukas, MICCAI 2021, arXiv:2103.07279 | deletes a vertebra from CT **and** mask and regrows both from one head | virtual vertebra volume error **3.88 ± 7.63%**, **n=10**, one scalar | none found | **yes, spine CT** | **REJECT as adoption** — no conditioning input exists to ask for a different vertebra type | new method work |
| 10 | **Synthetic radiographs, expert-validated** — Barr, arXiv:2510.22166; BMC MIDM 2026, PMC13185266 | 2-D cervical radiographs, **no labels** | 8 experts picked the real image in **29.0%** of trials (chance 25%), κ 0.061; landmark MSE **31.78 vs 84.33** at 100 real training images | 20,063 images released | yes (cervical) | **ADAPT** — the adjacent route the evidence keeps pointing at | — |
| 11 | **MAISI / NV-Generate-CT** — WACV 2025, arXiv:2409.11169 | full 3-D CT + mask to 512³, our exact label dictionary | authors publish **no mask-adherence number**; third party (Foundation VAE, arXiv:2605.30893) measures **rib 15.20**, vessel 13.50 Dice; downstream +2.5–6.5% on **lesions** | MONAI Apache-2.0; weights under NVIDIA Open Model Licence (**commercial terms unread**) | no | **REJECT** — run it once as a **disproof**, not a pilot | 1 day |
| 12 | **seg2med** — Phys Med Biol 2025;70(24) | 2-D CT painted on a mask | only per-vertebra numbers in the field: **L4 0.72 ± 0.02**, L1 0.74 ± 0.31; **composite artificial mask FSIM 0.45 vs 0.82** for real masks | none | no | **REJECT as a tool; cite as the decisive evidence** | — |
| 13 | **Computational phantoms / virtual imaging trials** — VICTRE, JAMA Netw Open 2018;1(7):e185474; XCAT 3.0, Med Image Anal 2025 | explicit anatomy → simulated **projections**; labels are the model | VICTRE replicated a regulatory trial: 2,986 synthetic subjects, **ΔAUC 0.0587 (SE 0.0062)**, consistent with the human trial | VICTRE FDA open source; XCAT by request | breast (VICTRE); XCAT per-vertebra labelling and bone texture **unconfirmed** | **REJECT for now** — the only family whose native output is a projection; the one to revisit | unknown |
| 14 | **Registration / atlas augmentation** — Zhao CVPR 2019; Shen MICCAI 2020 | image + aligned label | brain **0.759→0.804** from **one** labelled scan; knee +1.5–3 Dice at n=1–60; **≈0 vs B-spline on brain** | `brainstorm` **MIT**, dead since 2020 | no | **REJECT** — a small-data technique; we hold ~2,900 | — |
| 15 | **Thoracolumbar SSM + 16,807 released models** — Sci Data 2024;11:549 | meshes only, no intensity | generalisation **0.36 ± 0.24 mm**, specificity 0.45 ± 0.21 mm; FE ROM up to **30.76%** off in-vitro | Zenodo **CC BY 4.0**, 694 GB | yes | **REJECT** — a 7⁵ design lattice, not a cohort: **85.3% of models lie outside their own 95% ellipsoid**, 5.8% have TPA > 90° | salvage the 42 real STLs |
| 16 | **Morphable lumbar model** — J Biomech 2023;146:111421 | L2–L5 surfaces, 20 named knobs | round-trip control error **<0.8°, <0.3 cm², <0.7 mm**; permutation nulls p<0.04 / <0.001 / <0.01 | `github.com/aclouthier/morphable-lumbar-model` **MIT** | yes | **REJECT** — no intensity, no sampler, no fitting code; one knob moved the block 15% craniocaudally | — |
| 17 | **Full-spine SSM from partial observations** — Meng, ShapeMI@MICCAI 2020 | 24 vertebra surfaces, C1–L5 | completion of unseen vertebrae, mean error **<3 mm** | `gitlab.inria.fr/spine/spine_model` **non-commercial only** | yes | **REJECT** — surfaces, stops at L5, and the licence blocks the commercial track | — |
| 18 | **GPMM / Scalismo; ShapeWorks, Deformetrica** — TPAMI 2018;40(8):1860 | correspondence and deformation priors | formalism + a tool benchmark (Med Image Anal 2022;76:102271); **no spine, no generator validation** | Apache-2.0 / MIT | no | **REJECT as a generator** | — |
| 19 | **Patient-specific FE spine models** (Aubin/Clin/Kadoury lineage) | geometry, no image | best case ~**5° Cobb / 2.5 mm** per vertebra; material choice alone moves Cobb **6.2°** | varies | yes | **REJECT** — hours to days per patient, no image, one paper ever wrote a CT and validated it with a smoke test | — |

---

## 3. Why the runners-up lose, one sentence each

- **MAISI** — the only released generator whose label dictionary is ours, and the only measurement of its
  bone faithfulness is a third party's rib Dice of **15.20**, beside Konz's head-to-head where a ControlNet
  on CT scored **0.1132** against segmentation-guided diffusion's 0.8980: two independent measurements say
  this class of conditioning ignores bone.
- **seg2med** — it ran our experiment (condition on anatomy no patient has) and the answer was that the
  image stops being anatomy (FSIM 0.45 vs 0.82), which is evidence we should cite and a tool we cannot use.
- **Generated CT → DRR in general** — the one group that ran the whole chain (Rapuri, arXiv:2606.21414) on
  **DeepFluoro, which we hold**, found the generated-CT route was the **worst of four** on the held-out
  specimen (8.00 ± 10.80 mm landmark error vs 4.38 real film), and the 2-D route matched real films.
- **Schmid's SSIM** — its output is a real host CT warped with a synthetic bone painted into the hole, so
  every sample is a local perturbation of an existing case: it optimises realism, not reach, and our thin
  tails are exactly where there is no near host to warp.
- **Rasouligandomani's 16,807** — the marginals were built to look right (PI 59.30 ± 15.89 against the real
  59.26 ± 15.73) over a joint distribution that is a uniform grid; this is the project's own recurring
  failure mode, shipped in a data descriptor, and the parameter table cannot be used as a selection key
  without filtering.
- **Clouthier's morphable model** — the best control validation in the family and still only 20 separate
  one-dimensional lines through shape space, with no sampler, no fitting code, no sacrum and no grey values.
- **Meng 2020** — the only public whole-spine shape space, fitted to VerSe, and it stops at L5, which is
  precisely the junction this project is about; the non-commercial licence settles it.
- **Zhao 2019 / Shen 2020** — +4.5 Dice from **one** labelled scan is the headline, the gains shrink as n
  grows, no paper in the family has shown a gain at n in the thousands, and a diffeomorphism provably
  cannot change the number of vertebrae.
- **Finite element models** — they cost hours to days per patient, produce no image, and their own fidelity
  to a real spine (≈5° Cobb) is larger than the effects we would be trying to place.
- **XCAT / VICTRE** — the strongest external validation in this whole search (a replicated regulatory
  trial) and the only pipeline whose native output is a projection, but it is breast; for the spine I could
  not confirm whether XCAT labels per vertebra or whether phantom bone carries trabecular texture, and that
  answer decides whether the route exists at all.
- **SDF4CHD** — structurally the right design (discrete phenotype in, plausible anatomy out, across a
  topology change) with the right validation (47/50 type correctness), on hearts, with n=67, and porting it
  to 3-D bone would be new method work rather than adoption.
- **Barr's synthetic radiographs** — the strongest human validation in the spine generative literature
  (experts at 29.0%, below chance) and it produces **no labels**, so it cannot train a level detector.

---

## 4. Implementation plan for the winner

**What is being adopted:** the PolyPose / log-Euclidean poly-rigid transform, used **forward** as a
generator. The transform, its invertibility proof and its spine and pelvis validation are published. Using
it forward, as an augmenter, is **the one bespoke step**, and it is bespoke because no paper in any of the
six angles has ever done it — PolyPose has zero downstream numbers, and the only spine deformation-augmentation
result in existence (the Nijmegen scoliosis simulation, 61.5 → 93.6% Dice) measured itself on its own
synthetic output. Everything else below is taken from published designs.

**Repository and version.** `github.com/eigenvivek/polypose`, **MIT**, NeurIPS 2025 paper
(arXiv:2505.19256v5, PMC12148084). No tagged release — **pin a commit SHA**. Dependencies: torch, `diffdrr`
(same author, our DRR machinery already sits in this lineage), `xvr`, MONAI, cupy, jaxtyping. The README
documents only the DeepFluoro experiment scripts and **does not document a label-map input**; whether
per-bone anchors are a first-class CLI argument has to be read out of the code. CPU fallback with a
documented label-map interface: **POLAFFINI**, `github.com/CIG-UCL/polaffini`, **Apache-2.0** (LICENSE.md
read today), which takes a fine-grained segmentation as the region definition — which is exactly what our
v11 labels are.

**Step 0 — reproduce before trusting (2 days).** Run their DeepFluoro scripts on the DeepFluoro we already
hold and reproduce pelvis Dice 0.99, femurs 0.98, HD95 1.48/1.56 mm, **0.00% folds**. Their validation
cohort is our cohort; this is a rare chance to check a published number against an independent run before
depending on it. **If it does not reproduce, stop here.**

**Step 1 — inputs.** All 802 CTSpinoPelvic1K CTs with **v11** labels, TotalSegmentator 1,228 and VerSe
~374, resolved through `ostk.labels.labels_for(volume)` and never a fixed map; and specifically all 86
transitional subjects, where the warp broadens the sagittal distribution around cases we actually have.
Note 0533 is a truncated download (801/802 usable). Anchors = the labelled vertebral bodies, one rigid
transform per level, plus sacrum/hips/femora as further rigid regions.

**Step 2 — the bound (this is the contribution, not the warp).** Clip each level's rotation and translation
to **Panjabi 1991 Table 3** segmental range of motion (already on hand,
`PANJABI_1991_FULL_fixed.pdf`) and cross-check against **Boisvert 2008** (IEEE TMI 27(4):557–568), a
per-level, per-axis, anisotropic covariance of inter-vertebral pose over 295 spines. Both are external to
our computation, which is the whole point. **No published work has used ROM as a generative bound** — that
is the small, honest, defensible novelty, and it should be stated as the bound and the validation, not as
the warp.

**Step 3 — outputs.** Warped CT on its own grid, warped v11 labels by the same field (nearest neighbour),
the field itself, and a recomputed spinopelvic row per sample. **Never reoriented when written** —
canonicalise to RAS for analysis only. Storage: ~200 MB per abdominopelvic volume, so 5,000 samples ≈ 1 TB,
which goes on `/rs/rs_grp_oschome/go2432/`, not home.

**Step 4 — validation on our data, against the same metrics the sources used.**

| Gate | Metric, and whose it is | Pass condition |
|---|---|---|
| a | **Fold fraction** (PolyPose's own) | exactly 0.00%, as they report |
| b | **Per-level mask adherence** (Konz's protocol): re-segment the warped CT with SPINEPS/TotalSegmentator and Dice it against the warped label, **per level, never lumped** | quote it beside seg2med's L4 0.72 and Foundation VAE's rib 15.20; below ~0.95 per level and the sample is not usable |
| c | **Control fidelity, round trip** (Clouthier's design): command a lordosis/PI, re-measure it on the warped volume with `ostk` | their published errors were <0.8°, <0.3 cm², <0.7 mm; ours has to be stated whatever it is |
| d | **Population plausibility** (La Mattina's design, Ann Biomed Eng 2022): push the generated cohort through our own estimator and compare **distributions including spread and shape** against the real cohort and against published normative series, KS test | this is the gate the project's own history says matters — the medians were never the problem |
| e | **Render it.** Cast a Siddon DRR and look: end-plate sharpness, disc-space integrity, ghosting | no published spine warp has ever been projected; twice in this project a render has settled what numbers could not |
| f | **Downstream** (Kovacs' design): paired, one working point, bootstrap CI, **real held-out C-arm frames only**, in the **body-box convention** (A28) | report the number even if it is negative; a synthetic test set is the Nijmegen flaw and is disqualifying |

Rohlfing (IEEE TMI 2012;31(2):153–163) is the reason gate (b) is not enough on its own: he built a
deliberately wrong registration that scored extremely well on overlap and similarity. Dice on a warped
label tells you the warp moved the label to where the label is. Gates (c), (d) and (e) are the external
checks.

**Compute.** Forward warping is seconds per volume; there is no training in the generator. The only GPU
cost is the detector A/B at gate (f) and the re-segmentation at gate (b) (SPINEPS is already submitted over
CTSpinoPelvic1K as job 40416509 for the box-convention work, so gate (b) largely rides on that). Renders
reuse `sweep_v3`. Everything via `sbatch`, nothing on the login node.

**Where we abandon it.** (i) Step 0 does not reproduce → stop, and say so. (ii) Gate (b) below ~0.95
per level, or gate (e) shows broken end plates or disc interpenetration → stop; the warp is not preserving
the thing our morphometry measures. (iii) Gate (f) does not move outside the bootstrap CI → report the
negative result and stop. Each gate is cheaper than the next, in that order.

**And the part this plan does not solve.** None of it makes an L6, a T13 or a sacralised L5. A
diffeomorphism preserves the label set; that is a fact about the method class, not a gap to close. If the
transitional scarcity is the target, the only published design that crosses a topology change is the
SDF4CHD two-stage pattern (type-conditioned shape generator, then a mask-conditioned image generator), it
has never been done on bone or in 3-D CT, and adopting it is a separate decision that buys months of new
method work. The measured alternative is item 1 of the recommendation: more real transitional cases,
oversampled, with an anomaly-aware head.

---

## 5. What the paper could say, and what it could not

**Could say, with citations already in hand:**

- That the augmentation is *articulated (poly-rigid) morphological augmentation bounded by published
  segmental range of motion* — Arsigny's framework, PolyPose's instantiation, Panjabi's and Boisvert's
  bounds. The literature supports that phrase exactly and supports nothing stronger.
- That the spine field's control condition is affine + intensity, that nnU-Net removed elastic deformation
  on purpose, and that **nobody in the spine literature has used anatomically constrained deformation or
  generated anatomy at all** — a real, narrow, citable gap.
- The first per-level mask-adherence number for a warped or generated spine CT in 3-D (nobody has one; the
  only per-vertebra numbers in existence are seg2med's 2-D ones).
- The first DRR-fidelity number for a spine warp (gate e). Nobody has projected one.
- A with/without number on real C-arm frames, positive or negative, which no spine paper has published.

**Could not say:**

- That we synthesised a transitional vertebra. Nobody has, anywhere, and a warp provably cannot.
- That the synthetic spines are population-plausible — unless gate (d) passes and is reported with spread,
  not medians.
- That generated CT helps C-arm work: the one published end-to-end test of that chain, on DeepFluoro, found
  it **lost** to real CT and to 2-D generation.
- "State-of-the-art generative augmentation": the one challenge won with it (BraTS 2023) has a sequel from
  the same group measuring the effect as **negative on five of six regions**, by the recall-up/precision-down
  mechanism that is exactly the risk of manufacturing L6s — and our metric penalises false positives.
- That the DRRs looking right means anything. Skandarani: top GANs pass an expert visual Turing test and
  still fail to train a segmenter.

---

## 6. Open questions the literature does not answer

1. **Whether a warped or generated spine CT still casts a radiograph-like DRR.** Unmeasured by anyone, in
   any family. It is the single largest unknown for this requirement and the cheapest to settle.
2. **Whether any generator's per-vertebra mask adherence clears 0.9 in 3-D.** The only per-vertebra numbers
   that exist are 2-D and the worst lumbar level is 0.72.
3. **Whether registration or shape augmentation helps at all at n ≈ 2,900.** All the evidence is n ≤ 101.
4. **Whether interpolating between two spine CTs yields a spine a person has.** No specificity measurement
   exists for any of these generators, on any anatomy.
5. **Whether XCAT 3.0 labels the spine per vertebra, and whether phantom bone carries trabecular texture.**
   Both decide whether the phantom route exists for us; neither could be confirmed.
6. **What the right target even is for an LSTV edit.** Minimality is wrong: LSTV columns have longer
   transverse processes at *every* lumbar level and altered acetabular orientation and pelvic tilt, so the
   right question is "did the whole column move the way LSTV columns move". No published work states that
   target, let alone measures it.
7. **The Castellvi 19 mm threshold is reported on two different axes** (AJNR: craniocaudal; several
   secondary sources: width). Any generator claiming to place a case at type I must name the axis. Treat
   the AJNR craniocaudal reading as primary.
8. **Licences that decide the commercial track and were not resolved:** the NVIDIA Open Model License's
   commercial terms (unread, and not my decision); Meng's non-commercial spine model (a hard blocker);
   TetGen's AGPL if Schmid were ever reimplemented. Resolved today: POLAFFINI is Apache-2.0 and PolyPose is
   MIT.
9. **Whether PolyPose accepts a label map as a first-class input.** Not documented in the README; read the
   code before planning around it.

---

## 7. Closed today (so nobody re-derives them)

- **POLAFFINI licence** — Apache-2.0, "Copyright 2025 Antoine Legouhy". Previously flagged unread.
- **PolyPose code** — `github.com/eigenvivek/polypose`, **MIT**, NeurIPS 2025 (the notes had only the
  arXiv preprint and an unchecked repository licence). 18 commits, no tagged release: pin a SHA.
- **Castro-Mateos SIMs DOI ambiguity** — `10.1109/TMI.2015.2443912` is the paper (PMID 26080379);
  `10.1109/TMI.2015.2456376` is that issue's guest editorial.
- **Schmid's mechanism** — it does not synthesise a whole CT; it warps the nearest real training image and
  paints a sampled bone into it, which removes the "no soft tissue, cannot render" objection and replaces
  it with a worse one (every sample is local to an existing case).
