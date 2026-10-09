# Claims ledger

Every claim the manuscript makes about what this work *is* — each superlative, each "first", each comparison
with prior work — with the published comparator that decides it, the file in this repository that carries our
side of it, and a verdict. The Discussion is built from this file and nothing else.

Rule: **no number is invented.** A quantity is either read from a file named in the row, or it is a
`\PENDING{gate}{what}` macro that prints visibly in the PDF and that `tools/check_limits.py` fails on.

Written 2026-09-23 against the flagship frame in `docs/FLAGSHIP_PLAN.md`. Comparators searched
2026-09-23; searches recorded at the bottom.

Verdict vocabulary:

- **DEFENSIBLE NOW** — the sentence is true against a result file on disk today.
- **DEFENSIBLE AFTER Gx** — the sentence becomes true when gate *x* closes; until then the number is
  `\PENDING` and the sentence is written so it survives the gate.
- **REWRITE** — the superlative as Greg phrased it is not supportable; the row gives the sentence that is.

---

## 1. Detection on real C-arm fluoroscopy

### What is published

| study | task | test set | number | why it is not our number |
|---|---|---|---|---|
| Rao 2024, *Spine Vision* (EMBC; DOI 10.1109/EMBC53108.2024.10781813; arXiv 2407.08349) | **class-agnostic** vertebra detection/segmentation on C-arm images | 578 C-arm images split 500 / 58 / **20**; test images from the same pool of patients, cadavers and phantoms | recall 0.964 and 0.982 | **20 test images**, one image pool, no device held out, no class, no interval. The number is in-domain. |
| Zhang 2023 (VDVM; DOI 10.3233/XST-230025) | vertebra detection **and naming** on C-arm images | 31 real intraoperative images | naming 73.3 % | identity is imported by matching to the same patient's preoperative full-length radiograph |
| Huang 2022 (DOI 10.1016/j.cmpb.2022.107222) | registration-free vertebra labelling | 13 cadavers, **long-length tomosynthesis** (~17 vertebrae in field) | 88.3 % | a field no mobile C-arm produces |
| Killeen 2025 (DOI 10.1007/s11548-025-03351-y) | per-level vertebra segmentation on real cadaver C-arm frames | cadaver frames | Dice 0.04 per individual level | the closest real-frame per-level number published, and it is a floor |
| FluoroSAM 2025 (MICCAI; arXiv 2403.08059) | language-promptable X-ray segmentation, 3M synthetic X-rays, 128 organ types | real X-rays | reports Dice by structure, not per-vertebra recall on intraoperative C-arm frames | not a per-vertebra detection recall; not device-held-out |
| DeSilva 2016 (DOI 10.1097/BRS.0000000000001589), LevelCheck | vertebra localisation by 3-D/2-D registration | 398 clinical radiographs | 100 % of labels within the correct level | registration accuracy conditioned on a CT a human already named; excluded 13 of 504 radiographs showing three or fewer levels |

### The sentence we can defend

> No published per-vertebra detection recall on real intraoperative C-arm frames is measured on a C-arm absent
> from training. The closest comparator, a class-agnostic detector, reports 0.964 and 0.982 on a 20-image test
> split drawn from its own acquisition pool (Rao 2024); the only per-level number on real cadaver C-arm frames
> is a Dice of 0.04 (Killeen 2025). We report per-vertebra recall on a C-arm never seen in training, at an
> operating point set on other devices without reading a test frame, with a case-clustered interval.

**"Obliterates the state of the art" is not defensible and must not be written.** There is no state of the art
on this metric and this test design, and our own held-out recall today (80.5 % at the cross-device threshold,
90.6 % at the software default; `results/a1.json`) sits *below* Rao's in-domain 0.964. What is new is the
**test design** (device held out, interval, an operating point set without the test device), not a higher number against a like
comparator.

| claim | evidence | verdict |
|---|---|---|
| "first per-vertebra detection recall on a C-arm absent from training, with a case-clustered interval and an operating point fixed beforehand" | `results/a1.json#operating_points/cross_device_0.74` (`how_chosen`); `results/a2.json` (multiplicity); REVIEW_STATS F16 | **REWRITE** (2026-09-23, statistical review F16): the 0.74 rule reads no C-ArmLSpine frame, but it pools the detector's sweeps on COBRA2026, DeepFluoro and the Geneva phantom (not "the two training devices"), was computed in the same run as the test curve, and was adopted as the headline after the 0.25 result had been reported. Write "an operating point set without the test device" / "cross-device", never "fixed beforehand" or "pre-stated" |
| "best per-vertebra recall reported on real intraoperative C-arm frames" | — | **REWRITE**: not true against Rao 2024's in-domain 0.964/0.982 |
| the flagship's own per-device recall on its patient-disjoint test split | `\PENDING{G5}{flagship per-device recall}` → `results/final/*.json` | **DEFENSIBLE AFTER G5** |
| "detection is the binding constraint, and its cause is the angular coverage of the training frames" | `results/contribution_matrix.json` (85 held-out cells; +71.8 pp [63.4, 79.6] for the wide-arc source, +67.6 [57.6, 76.8] with the second seed; equal-count arm +26.1 [18.2, 33.6] over the cadaver source) | **REWRITE** (2026-09-23, statistical review F13): "detection is the binding constraint" stands; the cause does not. Adding the radiotherapy source changes device, anatomy (110 patients against 4 specimens), frame count and angle together, and no arm isolates angle. Write "transfer tracked the source whose frames span the arc" / "carried most of the transfer", quote both seeds, and do not attribute it to angular coverage |

---

## 2. Synthetic-to-real transfer from DRR to real fluoroscopy

### What is published

| study | the gap it reports | exact reading |
|---|---|---|
| Pelphix 2023 (MICCAI; arXiv 2304.09285; PMC11016332) | 99.2 % on simulated sequences → 71.7 % on cadaver | **surgical phase recognition accuracy**, averaged over four granularity levels — *not* a detection number. Anyone quoting it as a detection gap is misreading it. |
| SyntheX 2023 (Nat Mach Intell; DOI 10.1038/s42256-023-00629-1) | realistic simulation + strong domain randomisation, with no real image, matched CycleGAN, ADDA and real-image training on cadaveric hip fluoroscopy | the one controlled comparison of the routes; it supports parameterising the device rather than translating images |
| DeepDRR 2018 (DOI 10.1007/978-3-030-00937-3_12) | the image-formation model everything here builds on: learned material decomposition and scatter, analytic projection, attenuation and noise | ships a generic model, not per-device fitted terms |
| **Zheng 2018**, pairwise domain adaptation (J Med Imaging 5(2):021204; DOI 10.1117/1.JMI.5.2.021204; PMID 29376104) — added 2026-09-24 from `lit/CITABLE_CLAIMS.md` row 11 (VERIFIED) | 1,000,000 synthetic images for pretraining, **140 paired real images** for adaptation; failure rate (TRE > 10 mm) on 420 real X-rays of 42 C-arm CT volumes **16.07 % → 11.20 %** (fine-tuning alone 15.71 %); mean TRE 7.45 → 5.65 mm | vertebra **pose regression**, not level naming; an 11 % failure rate remained. Cited in the Discussion as the published measure of how much paired real data closes a synthetic-to-real gap on spine X-ray; future work here, since our styled renders remain separable from every device's real frames (99.0–100 %, Figure S2c). |
| **Gopalakrishnan 2024**, DiffPose (CVPR 2024, pp. 11662–11672; DOI 10.1109/CVPR52733.2024.01108) — added 2026-09-24 from `lit/CITABLE_CLAIMS.md` row 18 (VERIFIED) | a CNN trained to regress the pose of synthetic X-rays rendered from the patient's own preoperative CT; DeepFluoro median mTRE ≈ 0.9 mm (87 % sub-millimetre), Ljubljana cerebral set 0.2 mm; ≈ 12 h pretraining per patient | pelvis and cerebral vessels, no spine, no level claim. Cited in the Discussion only as what a paired rotational acquisition + cone-beam CT (one patient here) would allow: patient-specific self-supervised registration, future work. The review's inference that it "circumvents" level jumping has no source and is not used. |

Our own measured gap on this task: a renders-only detector reached **71.67 %** against a film-trained
**99.14 %** on the same 233 vertebral bodies of 25 real films, a paired **+27.5 pp [20.5, 35.2]** for real
training (`results/a3.json#comparisons/render_vs_film_detector`; the film side is an in-sample bound).

**What the renders are worth on the naming side, measured both ways** (added 2026-09-26; the Discussion sentence it
licenses is the one beginning "Rendered CT made a few films enough"). Three arms differing only in the rendered data —
the reported render-pretrained encoder, the same merged bank from ImageNet weights, and that bank with every rendered
row removed — with persons, seeds, epochs, learning rate, augmentation, head and scoring held identical. Where film is
scarce the renders carry ordinary-level naming: at five to twenty-five annotated persons per corpus, render-pretrained
minus film-only is **+6.0 to +21.9 points**, separated on every seed in **7 of 9** pre-stated cells. Where it is not,
they stop mattering: with every person the arms meet, and in the one cell that separates the other way, BUU-LSPINE with
every person, **film alone ends 1.6 points higher** on intervals about a point wide. The ImageNet arm sits between the
two at small N, so both the pretraining and the rendered rows in the bank carry the gain.
*Verdict:* **DEFENSIBLE, and it must be stated in both directions** — the reversal is a measured cell, not noise to be
dropped. Say "renders make a few films enough", never "renders replace film". Independently of this test the rendered
rows stay in training, because no released radiograph carries a human-read sixth lumbar or thirteenth thoracic
vertebra, so they are the only labelled source of the rare classes; this test concerns ordinary levels only.
Files: `results/coverage/film_ncurve/ablation/ablation_read.json` (read by
`tools/film_ncurve_ablation_read.py` against the rule pre-stated in `REVISION_LOG3.md` section 13), the three arms'
own `film_ncurve.json`, grid jobs 40451157 and 40451158 with collects 40451159 and 40451160; Table S4, generated by
`tools/make_supp_ablation_table.py`. Every number the Discussion quotes is a `\RESULT{}` key into that read file.

### The sentence we can defend

> Trained on physics-styled renders of other devices and no frame of the target C-arm, the detector reaches
> `\PENDING{G5}{styled-render-only recall on the held-out C-arm}` of the vertebrae the same detector finds
> when real frames of that C-arm are in training — the sim-to-real gap for this task, measured on one metric
> with one test set on both sides.

| claim | evidence | verdict |
|---|---|---|
| "we solve synthetic-to-real transfer" | renders-only arm is at 31.7 % [27.1, 36.1] on held-out C-ArmLSpine and 71.67 % on real film today | **REWRITE**: the gap is measured and partly closed, not solved. Say by how much, both sides on one metric. |
| "the published gap is Pelphix 99.2 → 71.7" | Pelphix reports surgical **phase** accuracy | **REWRITE**: cite it as the phase-recognition gap, or do not cite it here |
| "parameterising the device beats translating images" | SyntheX's controlled comparison + our own card-vs-uncalibrated gain, `results/a6.json` | **DEFENSIBLE NOW** |
| the closed gap after the G4 corpus and G5 flagship | `\PENDING{G5}{styled-render-only vs real-trained recall, same metric, same test set}` | **DEFENSIBLE AFTER G5** |

---

## 3. Released per-device image-formation parameters

### What is published

Searched for any release of C-arm image-formation parameters fitted to real frames of a named device. Found
none. DeepDRR releases a **generic** physics model (material decomposition, scatter, quantum and readout
noise) with no per-device fit; SyntheX randomises over a parameter range rather than fitting one; device
calibration in the literature is geometric (distortion, pose), not photometric. Vendors do not publish
image-formation parameters.

### The sentence we can defend

> We release nine image-formation terms fitted per device against real frames of that device — for
> `\PENDING{G4}{number of devices with a fitted card}` devices — which to our knowledge is the first such
> release; DeepDRR's model is generic and SyntheX randomises rather than fits.

Today's fits, and their honesty caveats (`results/a6.json`, `docs/devices/*.json`):

| device | held-out $R^2$ gain over uncalibrated physics | frames fitted | caveat |
|---|---|---|---|
| BV Pulsera | +0.0417 [0.0348, 0.0528] | 40 of 116 | 0 of 6 folds negative |
| Cios Fusion | +0.0153 [0.0029, 0.0274] | 40 of 366 | **fails the pre-stated criterion on the BCa interval** ([−0.0005, 0.0269]) and on the six-fold t interval ([−0.003, 0.034]; `results/stats_review/recompute.json#R2_card`) |
| Elekta XVI | +0.0232 [0.0054, 0.0453] | 40 of 335 | the audit found these 40 frames came from **three cases**; refit is gate G4 |
| PIXIUM 4600 | +0.0703 [0.0063, 0.1312] | 14 of 18 | two folds hold one frame |

The exposure draws were clipped to the central 60 % of each marginal — a disclosed defect, not a repair
(`docs/RESUME_2026-09-22_PM.md`, memory `device-sampling-audit`).

| claim | evidence | verdict |
|---|---|---|
| "first release of C-arm image-formation parameters fitted per device on real frames" | no comparator found; `docs/devices/*.json` | **DEFENSIBLE NOW**, with "to our knowledge" and the fitted-frame count stated |
| "fitted on the full release of each device" | Elekta card fitted on 40 frames from three cases | **DEFENSIBLE AFTER G4** (refit); until then the sentence names the frame count |
| "the fitted terms beat uncalibrated physics on every device" | Cios Fusion fails on BCa; on six-fold t intervals only BV Pulsera excludes zero; over the four device means the exact sign-flip P = .125 and the t interval is (−0.001, 0.077); frame-weighted gain 0.025 (`results/stats_review/recompute.json#R2_card`) | **REWRITE** (2026-09-23, statistical review F6): the pre-stated every-device criterion (C3) **was not met**; it held only on six-fold percentile bootstraps, which undercover. Say "the pre-stated every-device criterion not met", quote the fold-level P < .001 beside the device-level P = .13, and never "held on percentile intervals" as if that satisfied the criterion |

---

## 4. The corpus

### What is published, by axis

| corpus | images | subjects | what it is |
|---|---|---|---|
| VinDr-SpineXR (DOI 10.1007/978-3-030-87240-3_28; PhysioNet) | 10,466 | 5,000 studies | spine radiographs with lesion boxes; states it is the largest with radiologist bounding boxes |
| CSXA (DOI 10.1038/s41597-024-03383-0) | 4,963 | 4,963 individuals | cervical lateral radiographs **with per-vertebra levels** |
| BUU-LSPINE (DOI 10.3390/app13158646) | 7,203 (3,603 lateral + 3,600 AP) | 3,600 cases | lumbar radiographs with end-plate lines |
| NHANES II (DOI 10.5281/zenodo.10223910) | 17,075 entries in the release; 543 with landmarks | 364 persons among the annotated | digitised national survey films |
| COBRA2026 (DOI 10.5281/zenodo.21322350; arXiv 2607.20037) | ~950 GB of raw projections; **867 patients** across six European centres, split 692 / 52 / 123 | 867 | radiotherapy kV projections with planning CT and geometry |
| DeepFluoro (DOI 10.1007/s11548-020-02162-7) | 366 real fluoroscopic frames | 6 cadaveric specimens | the standard 2-D/3-D registration benchmark; CT and pose per frame |
| Ljubljana 2D-3D-GS | 18 | 1 cadaveric specimen | turntable flat panel, gold-standard pose |
| Geneva hip | 116 | 1 phantom | BV Pulsera, gold-standard pose |
| C-ArmLSpine | 296 spot frames (+ one 302-frame spin) | 149 cases | the only public **intraoperative** C-arm set with a per-case CBCT |
| Pelphix / SyntheX / FluoroSAM | 1.5M–3M **simulated** X-rays | — | synthetic; not a corpus of real frames |

### Where ours sits

Nothing here out-sizes VinDr on radiographs or COBRA on projections — those are their releases, and we use
them. The axis on which this work is largest is the **assembly**: every one of the rows above brought into one
split-disjoint corpus with one truth convention. Today's assembled totals, from `tables/tab_corpus.md` and
`tables/tab_corpus.sources.md`: 4,093 primary renders, 9,108 level-bank films (2,071 VinDr films and 950 FluoroCap
panels sit in the intraoperative fold banks alone), 4,276 real frames with three-dimensional truth, of which 778 are
C-arm frames. After G4 those become
`\PENDING{G4}{final corpus census: renders, films, real frames, C-arm frames, devices, labelled vertebrae}`.

| candidate sentence | verdict |
|---|---|
| "the largest corpus of fluoroscopic and plain-film spine images" | **REWRITE** — VinDr alone is 10,466 radiographs and COBRA alone is 867 patients of projections; a bare "largest" is false |
| "the largest **assembled** corpus of real radiographic and fluoroscopic spine images with a common vertebra-level truth convention and a person-disjoint split across every source" | **DEFENSIBLE AFTER G4**, with the census printed; the axis is *assembly with common truth*, not raw image count |
| "the largest set of real C-arm frames with three-dimensional truth used for vertebra-level work" | **DEFENSIBLE AFTER G4** — today 778 C-arm frames (C-ArmLSpine 296 + DeepFluoro 366 + Geneva 116); after the case134 spin and case39's third frame are exported it is `\PENDING{G4}{C-arm frames with three-dimensional truth}`. No published set exceeds DeepFluoro's 366 on this axis. |
| "the largest number of devices for which real frames and a fitted image-formation card exist" | **DEFENSIBLE AFTER G4** — `\PENDING{G4}{devices with real frames and a fitted card}` (four today; SpineSAC adds six if its bone truth is solved) |

---

## 5. Released weights

### What is published

SpineNetV2 releases code and pretrained weights (MRI, disc pathology grading). DeepDRR, SyntheX, Pelphix and
FluoroSAM release code and weights for their own tasks — none of them names a vertebral level on an
intraoperative C-arm frame. LevelCheck is not released as weights; it is a registration algorithm requiring
the patient's own preoperative CT.

### The sentence we can defend

> We release the detector and the level model as weights that run on a single C-arm exposure with no
> preoperative scan, no registration and no tracked instrument, together with the device cards that generated
> their training frames. No released model performs this task.

| claim | evidence | verdict |
|---|---|---|
| "we release weights for a model that names a vertebral level from a single C-arm exposure" | `atlas/model.json`; registry entry per memory `model-registry` | **DEFENSIBLE AFTER G7** (the card and the registered hash are the evidence; today the weights are private) |
| "no comparable released model exists" | the table above | **DEFENSIBLE NOW** with "to our knowledge" |
| "ready for inference in the operating room" | **REWRITE** — nothing here has been tested prospectively. The supportable phrasing is: released for retrospective analysis and for bench, phantom and cadaver evaluation; the clinical role is decision support beside the surgeon's own count, never a replacement for the check film. |

---

## 6. The clinical payload — the transitional spine

### What is published

| source | number |
|---|---|
| Mody 2008 (DOI 10.1097/BRS.0b013e31816043d1) | half of responding spine surgeons report at least one wrong-level operation |
| Furuya 2026 (DOI 10.1302/0301-620X.108B5.BJJ-2025-1129.R2) | 0.12 % of 34,544 consecutive degenerative operations |
| Ammerman 2006 (DOI 10.1016/j.surneu.2006.05.069), Dablouk 2019 (DOI 10.1080/02688697.2018.1562030) | the level first exposed is wrong in 4.3–15 % of lumbar operations before a check film corrects it |
| **Nakagawa 2017** (Tohoku J Exp Med 242:223–228; DOI 10.1620/tjem.242.223) | of 550 consecutive lumbar operations, 71 (12.9 %) had a lumbosacral transitional vertebra; the count was wrong in **38 of those 71 (54 %)** and the planned level changed in 11 (15 %) once the level was properly identified |
| Sabri 2025 (DOI 10.3171/2025.3.FOCUS2555) | 8.8 % of 3,147 adult full-length radiographs lack 24 presacral segments |
| Konin 2010 (DOI 10.3174/ajnr.A2036) | with a transitional vertebra, counting from the sacrum and counting from C2 name different vertebrae |
| **Otake 2012** (Phys Med Biol 57(17):5485–5508; `levelcheck2012`) and **Lo 2015** (Spine 40(8):E476–E483; `levelcheck2016`) — rows added 2026-09-24 from `lit/CITABLE_CLAIMS.md` rows 12–13 | in simulation, all 47 LevelCheck registration failures across λ = 30–150 (one in 50,000 trials at λ = 120) arose "from the periodically symmetric structure of the spine" and show "a translational shift in the superior-inferior direction by one vertebral height"; clinically, multistart optimisation gave 100 % at 200 multistarts (99.3 % at 50), and the later series report no wrong-level localisation. The Discussion states the mechanism (a one-vertebra shift, shared with a count from the sacrum on a transitional spine) and that it was engineered away clinically; the review's "catastrophic misalignment in real-world applications" is CONTRADICTED by those series and is not used. |
| DeSilva 2016 / Manbachi 2018 (DOI 10.1007/s10439-018-2099-2) | LevelCheck's 97.6 % is five surgeons reading 62 difficult films **with** the overlay — a surgeon-plus-machine figure, so the comparator for this work is surgeon + LevelCheck, not LevelCheck alone |

### The sentence we can defend

> Transitional anatomy is where registration cannot help: LevelCheck imports the name its preoperative CT
> carries, and on a transitional spine that name depends on the convention the reporting radiologist used.
> Nakagawa 2017 measured the consequence — 54 % of transitional patients miscounted, 15 % with the surgical
> plan changed once the level was established. This work names the variant from the intraoperative frame
> itself.

| claim | evidence | verdict |
|---|---|---|
| "transitional anatomy and miscounting are the entire failure set for wrong-level surgery" | no source establishes *entire*; Nakagawa gives 54 % miscounted **among transitional patients**, not the share of wrong-level events attributable to transitional anatomy | **REWRITE**: "the two mechanisms that the published series identify" — and state plainly that the share of wrong-level events attributable to transitional anatomy is **not established in the literature we found** |
| "parity with or better than surgeon + LevelCheck on transitional spines" | `\PENDING{G6}{exact-level accuracy on transitional test persons vs the simulated surgeon + LevelCheck comparator, with Wilson lower bounds}` → `results/levelcheck_claim.json` | **moved to paper 2 (paper2_levelcheck/)** on 2026-09-24 (evening); paper 1 makes no such claim (`PAPER1_SCOPE.md`). The row is kept as paper 2's ledger entry, where the verdict stood at **DEFENSIBLE AFTER G6** — and only if the pre-stated bound (exact level lower bound ≥ 90 %, variant sensitivity lower bound ≥ 85 %) is met on the pooled count-changing test persons; if it is not, the manuscript says so. Per subtype the 85 % bound needs at least 22 carriers without a miss (`results/stats_review/recompute.json#R4_wilson/min_n_zero_errors`), which the rarer subtypes cannot reach under the 50/10/40 rule on the inventory as it stands (that inventory is under the running transitional-registry audit), so per-subtype rates are descriptive (statistical review F17, stated before G6 runs). At 60 test persons the 90 % bound is met with probability 46 % at a true accuracy of 97 %; the design is not powered, and the Methods say so |
| "the classifier names L6 / T13 / sacralised L5" | `results/anomalous_inventory.md`: 89 transitional subjects with truth across four sources (VerSe 56, CTSP 18, TotalSegmentator 12, C-ArmLSpine 3); the classifier's L6 accuracy was 44.9 % in the FOV study | **DEFENSIBLE AFTER G1/G5** — today the evidence base is too small and partly in training |
| "three real L6 patients confirm the coupler" | the three C-ArmLSpine "L6 patients" are a **VERIDAH morphology read** of a lumbar-only CBCT, not a count; TotalSegmentator read L1–L5 there and VERIDAH L2–L6 | **REWRITE**: scoring on them measures agreement with VERIDAH, not correctness. Say so wherever it appears. |
| the coupling result (classifier + count) | `results/COUPLING.md`, `results/coupling.json` — classifier unchanged in 20 of 20 cells; coupled 90.3 % [79.8, 98.4] vs classifier 86.0 % [75.1, 95.4] on anchored bodies | **DEFENSIBLE AFTER a verifier re-runs** — the adversarial verifier died; marked unverified |

---

## 7. Priority statements in the manuscript (journal rule; RSNA review Fix 6, 2026-09-23)

The journal forbids a claim of priority in the Discussion. A verdict above that reads "DEFENSIBLE NOW with
'to our knowledge'" or "DEFENSIBLE AFTER G4" says whether the sentence is **true**; it does not license it in
this manuscript. Every such sentence was removed from `SchwingNet/` or rewritten as a plain statement about
the cited work, which the rows above support. The verdicts stand for other venues (cover letter, talks).

| ledger row | manuscript before | manuscript now |
|---|---|---|
| §1 held-out detection | Discussion: "no published per-vertebra recall on real C-arm images carries a held-out device, an interval and an operating point set without the test device --- a test-design claim"; Introduction: "No vertebra detector on real intraoperative C-arm images has been published with the device held out" | Discussion: Rao 2024's recalls are "class-agnostic, on 20 in-pool images without an interval"; "With the device held out, the 80.5 % here sits below the in-domain 0.964". Introduction: "Published vertebra detectors on real C-arm images were scored within their own acquisition pool, the strongest class-agnostic" |
| §3 per-device image formation | "the nine terms here are, to our knowledge, the first released image-formation parameters fitted to a named device" | "Unlike the generic released formation model (DeepDRR), the nine terms here are fitted per named device" |
| §4 corpus | "The corpus is largest on assembly, not raw image count, its census \PENDING{G4}" | removed; the census stays `\PENDING{G4}` in Methods (Sources) and the supplement. A G4 census does not bring the superlative back into this manuscript |
| §5 released weights | "to our knowledge no released model performs this task"; Introduction: "Naming from the C-arm alone is unpublished" | both removed; the Introduction keeps the facts that followed the colon (Zhang 2023 imports identity from a preoperative radiograph; Huang 2022 names only on cadaver long-length tomosynthesis) |

The "What the title may say" list below still words contributions 1, 3, 4 and 5 as priority claims; it is a
record of the adjudication, not text for the manuscript.

---

## 8. The six-figure manuscript (2026-09-23): the claims each figure carries

Greg, ~20:00: six figures, the manuscript wrapped around them. Each figure's claim, its comparator, and the sentence
the rewritten text uses. Figure 6 (the LevelCheck comparison) is built on `LEVELCHECK_MODEL.md`, frozen by commit
ecae75f before any held-out transitional person was scored; its §6 governs what may be said.

**2026-09-24 (evening): Figure 6, the former Table 3 (`tab_levelcheck`) and every comparison clause moved to paper 2**
(`paper2_levelcheck/MOVED_FROM_PAPER1.md`; scope rule `PAPER1_SCOPE.md`; log `REVISION_LOG3.md` section 8). Paper 1 has
five figures and three tables. The rows below are kept as the record; the ones that moved are marked in their verdict.

| figure | claim in the text | evidence | verdict |
|---|---|---|---|
| 1 phenotypes | four transitional phenotypes shown on labelled CT, render and released radiograph; "no released radiograph or C-arm frame carries a human-read T13 or Castellvi grade" | `figures/figure1.record.json#not_shown_and_why`; `results/rare_class/transitional_subtypes.md` | **DEFENSIBLE NOW** (a statement about the sources on disk; the C-ArmLSpine L6 frame is not shown because its L6 is one automatic labeller against another) |
| 2 embedding | "L6 separated from L5 more than any lumbar level from the one above"; "as local identity predicts" (Discussion); (2026-09-24) "in two of four validation persons with a fused L5, the last free vertebra ... sat nearer L5 than L4, but their L3 was also low" | `results/figure2/figure2_metrics.json#silhouette` (0.35 vs 0.16-0.23); `results/figure2/figure2_transitional.json#fused_L5` | **DEFENSIBLE NOW, with the four caveats the text carries**: the validation split chose the checkpoint (not held out, gate rule); within one render source the order reverses (0.14 vs 0.21, five persons); the never-seen "L6" is one labeller's reading, the second reads the same body as L5 (`results/spineps_ids/VERIFY.md` 1a), and it vanishes under the body box (−0.07); the fused-L5 pull toward the level below is not confined to the junction (the same two persons' L3 is low), so four persons cannot separate a junction effect from a whole-spine shift, and the text claims neither. The Discussion says "the evidence is thin" |
| 3 network | architecture only; no result | `figures/figure3.record.json#results_numbers` = none | n/a. The mismatch recorded on 2026-09-23 (panel a drew YOLO11m alone feeding the level model) is fixed in the 2026-09-24 build: (a) draws the film-trained YOLO11m-pose keypoint detector boxing the bodies and the YOLO11m detector boxing the sacrum (`figure3.record.json#routing`); the Methods name both (REVIEW_STATS F9), and the sacrum detector's lineage (fine-tuned from the render-trained detector, `results/eval_gate/LINEAGE.md`) |
| 4 one exposure | naming, counting and coupling on the unseen C-arm; the six-lumbar frame; (2026-09-24) "the coupled call was L6 on one of four anchored frames of the three patients one labeller reads as L6 and on four of 233 anchored frames both labellers read as five-lumbar, each with a stop" | `figures/figure4.record.json#leak_gate` (every number HELD OUT); `#panels/d/denominators` | **DEFENSIBLE NOW**; (d) is agreement with one labeller, never correctness (§6 row "three real L6 patients"), and the Results say so. The four false L6 calls on five-lumbar frames are reported beside the one agreeing call, so the frame is not read as a detection result |
| 5 persons needed | (2026-09-24, Figure 5 rebuilt on the frozen exact test) "the frozen exact test needs 19 at-risk persons against 82.2 % and 152 against 97.6 %"; "no real-frame transitional test person was verified"; "of 91 unread COBRA2026 test-side calls, 57 were not contradicted by their own field"; "if all 57 were confirmed and named correctly, the lower bound would be 93.7 %"; power 55 / 71 / below 0.1 % / 708 (Methods) | `results/power/power.json`; `figures/figure5.record.json#reading`, `#counts_and_intervals` | **Amended 2026-09-24 (evening):** the exact-test clause (19 / 152 against 82.2 / 97.6 %), the power sentence (55 / 71 / 708) and Figure 5 panel (b) **moved to paper 2 (paper2_levelcheck/)** on 2026-09-24 (evening). Paper 1 prints the pre-stated Wilson targets (35 at-risk persons at 90 %, 22 carriers at 85 %), seven real-frame candidates from a two-labeller count with both junctions in the field (error-free lower bound 64.6 %) and 51 at-risk CT test persons (93.0 %) (`results/power/power.json#n_needed_zero_errors`, `figures/figure5.record.json#numbers_on_figure/counts_and_intervals`); the 57 / 93.7 % of the morning are superseded by that count. Earlier verdict: **DEFENSIBLE NOW** (arithmetic plus a dated count). The count is dated 2026-09-23; the 57 are an upper bound (VERIDAH's L6 PPV near 42 % on CTSP), stated as "if confirmed". **Withdrawn**: "three persons have a real transitional exposure (best-case 43.9 %)" — the three are excluded from the primary analysis in advance (`LEVELCHECK_MODEL.md` §4); "exceeding 97.6 % with 80 % power first at 4,276" — that was power at 98.2 % with a Wilson-bound test, not the frozen test |
| 6 vs LevelCheck | "SchwingNet named every vertebra correctly in k of n at-risk persons … exceeding the 82.2 % modelled for surgeon + LevelCheck when the preoperative labels come from a planning read without a count from C2" | `LEVELCHECK_MODEL.md` §6; `\PENDING{G6}` | **moved to paper 2 (paper2_levelcheck/)** on 2026-09-24 (evening); paper 1 prints no such sentence and scores no held-out transitional person. Paper 2's ledger: **DEFENSIBLE AFTER G6, and only if H1 is eligible (n ≥ 19 at-risk real-frame test persons) and rejected.** The words "modelled" and the condition clause are part of the claim. "Exceeds the published 97.6 %" is allowed only if H2 is eligible (n ≥ 152) and rejected, which no inventory in reach allows (Figure 5b; `LEVELCHECK_MODEL.md` §7) |

*The paragraph below is paper 2's since 2026-09-24 (evening); kept as the record of the adjudication.* **Greg asked for LevelCheck to "fail enough" for the network to outperform it or the 97 % surgeon + registration
figure.** Not done by tuning, and the manuscript does not do it. What the frozen comparator does instead is the
honest version of the same argument: LevelCheck carries the planning read's labels, so on a transitional spine it is
as right as that read, and the frozen value is the most favourable published accuracy of a read made without a count
from C2 (Peh 1999, 82.2 %), not a value chosen to be beaten. Where the planning read counted correctly LevelCheck is
the ceiling, and the text says so. The 97.6 % cannot be exceeded at any inventory in reach, and the text says that
too (Results, "Transitional persons needed and available"; Discussion, third paragraph). Since 2026-09-24 the
summary statement and Conclusion say the comparison "awaits verified" transitional patients rather than that public
data hold too few: 57 field-supported COBRA2026 calls exceed H1's n_min of 19 if enough of them are confirmed at
risk, so "too few" is true only of H2 (152). Since the evening of 2026-09-24 the summary statement and Conclusion say
instead that transitional naming on real exposures rests on three cross-validation patients and awaits verified cases.

**The title** ("… robust to transitional anatomy, versus registration-assisted neurosurgeons") is fixed by Greg
(`TITLE.md`). Both clauses remain **unsupported until G6** (REVIEW_RSNA.md, sentences to cut, item 1): no transitional
accuracy on held-out persons exists on disk, and the comparator is a model, not neurosurgeons. If G6 misses H1, the
title's clauses are contradicted by the paper's own Table 3 and Figure 6. **2026-09-24 (evening):** the clause "versus
registration-assisted neurosurgeons" left the title with the comparison (`TITLE.md`; paper 2 keeps it); "robust to
transitional anatomy" remains, still unsupported by any held-out transitional accuracy, and whether it stays in paper 1
is Greg's call (`REVISION_LOG3.md` section 8; `front_matter.json` author decision `title_clauses`).

Corrections from `LEVELCHECK_MODEL.md` §10 applied in the rewritten text: the LevelCheck literature does address
transitional anatomy, judged against the neuroradiologist's own labels (the Discussion says the published accuracies
"measure convergence onto labels a reader assigned"); the 97.6 % carries its definition wherever it appears (median of
five surgeons, 62 difficult films, with the overlay); Nakagawa's "planned level changed in 11" is no longer quoted
(every one of the 11 was an added level, not a substituted one), and the `nakagawa2017` bibliography note that said
so was removed from `refs.bib`.

---

## What the title may say

Greg's instruction is a network that ships. The five contributions survive the ledger in this form:

1. detection **evaluated with the device held out** — a test design nobody has reported, not a higher number;
2. the sim-to-real gap **measured on one metric with one test set on both sides**, and narrowed;
3. **per-device image-formation parameters released** — first, to our knowledge;
4. **one assembled corpus** with a common level truth and a person-disjoint split — largest on assembly, not
   on raw image count;
5. **weights released** for a task no released model performs.

Payload: naming the level on a transitional spine.

A title that survives every row:

> **A released C-arm network that names the vertebral level, including the transitional one, from a single
> intraoperative exposure: per-device image formation, an assembled corpus, and evaluation with the device
> held out**

Nothing in it claims a number, so nothing in it can be falsified by a gate.

---

## Searches behind this ledger (2026-09-23)

per-vertebra detection recall on C-arm fluoroscopy · Pelphix simulated-to-cadaver gap · per-device C-arm
image-formation parameters / DeepDRR calibration · largest public spine radiograph datasets · FluoroSAM ·
public real-fluoroscopy datasets with three-dimensional truth · COBRA2026 release size · registration-free
intraoperative vertebra labelling · wrong-level surgery and transitional anatomy.

Sources consulted, with the URL each row's number came from:

- Rao 2024 — https://pubmed.ncbi.nlm.nih.gov/40039607/ , https://arxiv.org/pdf/2407.08349
- Pelphix — https://arxiv.org/abs/2304.09285 , https://pmc.ncbi.nlm.nih.gov/articles/PMC11016332/
- FluoroSAM — https://arxiv.org/abs/2403.08059
- DeepDRR — https://link.springer.com/chapter/10.1007/978-3-030-00937-3_12
- VinDr-SpineXR — https://physionet.org/content/vindr-spinexr/1.0.0/ , https://vindr.ai/spinexr
- COBRA2026 — https://zenodo.org/records/21322350 , https://arxiv.org/abs/2607.20037
- DeepFluoro — https://github.com/eigenvivek/DiffDRR-Datasets
- Nakagawa 2017 — https://www.jstage.jst.go.jp/article/tjem/242/3/242_223/_article
- Sabri 2025 — https://thejns.org/focus/view/journals/neurosurg-focus/58/6/article-pE13.xml
- SpineNetV2 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11617751/


---

## 8. The acquisition-space review (2026-09-24): what of it the Discussion says, and on what

The review Greg uploaded (`lit/acquisition_space_review_2026-09-24.{pdf,txt}`; an AI-generated synthesis, 12 pages,
47 URL citations, no peer review) was checked claim by claim at the primary sources in `lit/CITABLE_CLAIMS.md`.
Nothing is cited from the review itself. The rows below are the sentences the Discussion now carries because of
it, each against the file that carries our side, in the vocabulary of this ledger.

| sentence in the manuscript | the review's claim it answers | our file | verdict |
|---|---|---|---|
| "same-device frames restored it only to a plateau reached by 50 frames" (Discussion P4) | "convolutional models plateau at about 90 % in the fluoroscopic domain while reaching 99 % on standardised radiographs" (review sections 1, 2, 9; CITABLE_CLAIMS row 1: NOT FOUND in any published series) | `results/indomain/INVENTORY.md` item 1; `results/indomain/det_fill.json` (50 frames 82.9 % = 238/287; 50-210 frames 81.5-86.8 %, intervals overlapping; every cell held out) | **DEFENSIBLE NOW** as our own held-out result, stated uncited. The "99 % on films" half is the selection-split film accuracy of Table 4's twin / supplement, not held out, and is not set beside it. |
| "We hypothesise that coverage, not count, set it: every real frame of that device is anteroposterior or lateral ... whereas the render pools span the arc; no arm varies view alone, so this is untested" (Discussion P4) | "sampling-density saturation within a redundant region of the acquisition space; coverage-driven sampling" (review 2.1-2.2; CITABLE_CLAIMS rows 2-3: an assertion with no source; coverage / entropy are a proposal, not a finding) | `results/arc/audit/pose_pools.json` (real pool 148 AP within 10 deg, 148 lateral, 0 between 10 and 60 deg; arc pools 592 / 1,100 / 4,216 poses over -90..+90 deg); `results/arc/ARC_CHECK.md` s1; section 1 row "detection is the binding constraint, and its cause is the angular coverage of the training frames" (REWRITE: no arm isolates angle) | **DEFENSIBLE NOW as a labelled hypothesis only.** The journal requires new hypotheses to be labelled; the sentence says "hypothesise" and "untested". It must never be promoted to a finding on the present arms (statistical review F13). The matched-N low- versus high-coverage render experiment of workflow review-integration (`results/coverage/experiment/`, not yet written) is the test. |
| "The comparison arm's level model saturates the same way in development: doubling its training persons from 4,477 to 8,950 moved validation accuracy on real films by 0.1 points and on rendered L6 bodies by 1.7 (supplement)" (Discussion P4); supplement "Development learning curve of the comparison arm" (wording since 2026-09-24 evening: "A level model trained from ImageNet weights on the split's training persons saturates likewise in development"; supplement section "Development learning curve of a split-trained level model"; the arm is named for what it is, not as a comparison arm) | "injecting more randomly sampled images yields diminishing returns" (review 2.1, 9; CITABLE_CLAIMS row 30: the general law is VERIFIED in Hestness 2017, Sun 2017 and Figueroa 2012; none separates coverage from count) | `results/dual_loss/saturation.json` (validation side of the G3 bank, three seeds per fraction; `status`: development numbers, no test person) | **DEFENSIBLE NOW as development evidence, labelled.** It is not a test result and is not in the Results; it is quoted as "in development" and the supplement says "no test person is among them". No reference is spent on the power-law form (35 of 35 used; `figueroa2012` stays in refs.bib for the in-domain fit if Figure 5 gains its data panels). |
| the DICOM-tag coverage vector (positioner angles 0018,1510/1511; SID 0018,1110; patient position 0018,5100) | review 2.2 table (CITABLE_CLAIMS rows 4-8 VERIFIED against DICOM PS3.3) | `slurm/acq_coverage.sh` -> `results/coverage/` (grid job 40436995 `acqcov`, running at 11:10: 901 C-ArmLSpine XA headers read, COBRA 692 cases' geometry, 4,167 render stems) | **DEFENSIBLE AFTER the coverage census lands.** No DICOM tag is named in the text today; the supplement says the level bank records no angle, distance or magnification, which is true of that bank (`saturation.json#coverage/what`). |
| not used: "catastrophic misalignment in real-world clinical applications" of LevelCheck; "X23D heavily reduced dose"; "patient-specific networks circumvent periodicity"; "90 % plateau" as a literature fact | review sections 4, 5.1, 8 | `lit/CITABLE_CLAIMS.md` rows 13 (CONTRADICTED by Lo 2015, De Silva 2016, Manbachi 2018), 17 (the grade-C breach and the dose difference are misattributed), 18 (no source), 1 | **REWRITE / not written.** |

---

## 9. Paper 1 restructured: the comparison is paper 2 (2026-09-24, evening)

Greg: "I'd like to move the comparison to neurosurgeons / all the LevelCheck stuff into a new paper, remove it from the
current paper." What paper 1 now claims is `PAPER1_SCOPE.md`; every moved passage is verbatim in
`paper2_levelcheck/MOVED_FROM_PAPER1.md`; the log is `REVISION_LOG3.md` section 8. In this ledger the rows that moved
are marked in place rather than deleted: §6 "parity with or better than surgeon + LevelCheck", §8 rows "5 persons
needed" (the exact-test clause and panel (b)) and "6 vs LevelCheck", the "fail enough" paragraph and the title note.
Nothing else changed its verdict. Standing rule while paper 2 is pending: paper 1 adds no per-stratum transitional
accuracy, no modelled LevelCheck value (82.2, 97.6, 92.6 %) and no H1-H6 language; the Introduction's prior-art
sentences on LevelCheck (`levelcheck2012`, `levelcheck2016`, `desilva2016`, `manbachi2018`, `peh1999`) stay, and the
rows above that cite them as literature (§1 De Silva 2016, §5 "LevelCheck is not released as weights", §6 Otake / Lo /
De Silva / Manbachi) are unchanged. The radiotherapy set is not without demographics: COBRA2026 metadata.yaml gives
PatientAge on 115 and PatientSex on 75 of the 145 detector cases (`results/age_sex_by_source.json`; Table S3), so no
sentence here or in the packet may say it releases none.

- 2026-09-24 ~22:15 (Greg): title is now "SchwingNet: a convolutional-recurrent network for level naming in spine surgery" -- "robust to transitional anatomy" removed ("if it's not robust to transitional anatomy, then it should be removed from the title"); the Discussion's sentence on the first encoder's deleted training record removed (not a limitation of the reported work); readers are PGY2.
