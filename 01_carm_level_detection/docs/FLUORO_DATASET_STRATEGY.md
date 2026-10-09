# Fluoroscopic dataset strategy

Written 2026-09-20. Which external datasets to acquire, in what order, and what each is for.

**The rule that orders everything below: annotate only what cannot be labelled for free.** Two of these
sets carry the geometry needed to generate exact labels automatically. Those come first *because* they
cost no annotation, and the annotation budget is then spent where nothing can label automatically.

**What this is measured against.** Two constraints block the product, and every dataset is judged on
which one it touches:

- **(a) Nothing can be evaluated.** There is no labelled real *spine* fluoroscopy anywhere in this
  project, so no number states what any of it achieves on a C-arm image. Detection is the binding
  constraint at ~60 points against 11–28 for realistic physics, and the only detection figure on real
  images is 71.67 % recall for a render-trained detector against 99.14 % for the film-trained one.
- **(b) The sweep is untested.** The method needs consecutive overlapping frames of one patient at a
  *known* displacement. The number of such pairs available today is zero.

See `docs/HANDOFF_PHYSICS.md` for the measurements behind both.

---

## Tier 1 — exact labels on real fluoroscopy, for free. Do first.

### DeepFluoro (Grupp et al., IPCAI 2020, Johns Hopkins)

6 cadaveric pelvic CTs, **366 real fluoroscopic X-rays**, 24–111 per subject, with the **calibrated
C-arm intrinsic matrix and the ground-truth pose (extrinsics) of every image**, plus 14 manual landmarks
per CT. Public via `DiffDRR-Datasets` (https://github.com/eigenvivek/DiffDRR-Datasets); original
annotation code at https://github.com/rg2/DeepFluoroLabeling-IPCAI2020.

**Why it dominates.** CT *and* pose together mean the labels can be generated rather than drawn:
segment the vertebrae in the CT — the v11 scheme already has sacrum 26 and L1–L5 at 20–24 — project
them through the known extrinsics, and you have **exact 2D vertebra boxes on real fluoroscopic images
with zero annotation**. That is constraint (a), solved for free, today. It also contains the **sacrum**,
which is the anchor the caudal sweep depends on.

**And it may touch (b).** Every pose is known, so the relative displacement between any two frames of
one specimen is a computation, not a study. Select the pairs that happen to be cranio-caudal
translations and you have real frame pairs at a known step — the thing no corpus was thought to supply.
Whether usable pairs exist is an empirical question that a query answers in an hour.

**One addition from verification.** This is the SAME 366-image / 6-specimen / Siemens CIOS Fusion
corpus that SyntheX and the 2026 diffusion paper already used, so the achievable ceiling on it is
partly known in advance — about 6 mm landmark error and Dice 0.86 for hip structures. SyntheX also
evaluates a held-out **60-image BrainLab LoopX** set (6.16 +/- 5.15 mm), a second real-device
domain-shift test that is small and free.

**Limits, stated up front.** Six specimens, pelvis-centred, so few vertebral levels; cadaveric, not
live; the poses were chosen to vary angle for registration validation, so translated pairs may be rare
or absent. It will not be the whole answer. It is free and exact, which nothing else here is.

---

## Tier 2 — where the annotation budget goes, because nothing can label it automatically

### Coronary angiography — CADICA, ARCADE, XCAD, AngioCAD

Real fluoroscopy at volume, in video sequences, with the **thoracic spine in the background**.
CADICA: 42 patients, DICOM at 10 fps, 512×512, runs of 1–151 frames. ARCADE: 3,000 images.
XCAD: 1,747 images from a GE Innova IGS 520. AngioCAD: 413 patients with video sequences.

**Why this matters more than it looks.** Thoracic is where the method is weakest (94.5 % against
99.7 % lumbar) and where wrong-level surgery is most common (0.42 % against 0.12 % overall). And the
corpus is nearly empty there: the spine-detector manifest holds **219 lateral thoracic corner quads
against 26,306 cervical**. No lateral T2–T11 corner exists anywhere in it. Coronary angiography is the
only large source of real fluoroscopic thoracic spine available without a DUA.

**Confounders to carry:** heavy iodinated contrast, which the detector has never seen; and the C-arm
rotates LAO/RAO rather than translating, so this serves (a) and not (b).

### Pediatric IRI — 95,308 images, 1,357 sequences

Real fluoroscopy at volume with the **lumbar spine in field** — abdominal angiography images the aorta,
which lies directly on the spine — and, crucially, **not press-degraded** the way FluoroCap is (72.8 %
of FluoroCap panels have `noise_mad` exactly 0.000).

**Three uses, in descending certainty.**
1. **Calibrate the augmentation.** `make_zoom_dataset.fluoro_degrade` uses a photon budget of 80–800
   per pixel, which is a *guess*. `tools/check_fluoro_degrade.py --films` already prints grain before
   and after (4.21 → 8.77 grey levels on real crops). Point it at real fluoroscopy and the photon range
   stops being a guess. Hours, no annotation, and it improves a model that is training now.
2. **Annotate 150–200 frames as a test set**, stratified AP/lateral and contrast/no-contrast.
3. **Unlabelled adaptation pool.** The largest real-fluoro pool this project could have — about 40× the
   usable FluoroCap tier. Caveat: detector self-training has already been measured as a wash here once,
   so pseudo-labelling is not free money.

**Confounders:** pediatric vertebrae are small with unfused ring apophyses, so a detector trained on
adults may fail for reasons that have nothing to do with fluoroscopy — that would read as a domain
problem and be an anatomy problem. DSA **subtraction frames remove bone by construction** and must be
excluded. And a pediatric abdomen is thinner than the 25.9 cm adult path the renderer is calibrated for,
so the grain target from use (1) is offset in a direction worth estimating rather than ignoring.

---

## Tier 3 — raw fluoroscopy as a statistics target. No annotation, no anatomy needed.

### Veriserum (ETH Zürich) and the TMVR robotic sheath set

Veriserum: ~110,000 dual-plane fluoroscopic images of knee implant phantoms with calibration and
ground-truth poses. TMVR: 800×800 bi-plane frames of a cardiac phantom with catheter masks.

**The one job they do.** The renderer's two panel-comparison rows — histogram total-variation distance
0.187 and noise power spectrum shape 0.862 raw / 0.986 matched — are scored against **27 FluoroCap
panels that are the corpus's top decile by grain and resolution, about 9 % of it**. So the renderer was
validated against FluoroCap's best tenth, not against FluoroCap. These sets are raw fluoroscopy that
never went through a journal, and replace that target.

**Be clear what this buys.** It improves the *credibility of the measurements*, not the performance of
the system. It will not move 21.5 %. TMVR is closer to abdominal thickness; Veriserum is far larger.

---

## Tier 4 — WITHDRAWN. Pelphix is not a check on this number.

### Pelphix (Killeen, Unberath et al., MICCAI 2023)

This tier previously read that Pelphix's 99.2 % -> 71.7 % sim-to-cadaver drop lands within 0.03 points
of the 71.67 % measured here for a render-trained detector, and proposed citing the agreement in the
Discussion. **That was a false equivalence and it is withdrawn.**

Pelphix's 99.2 -> 71.7 is **average surgical-phase recognition accuracy** over four sequence
classification heads — corridor, activity, view, frame — with the cadaver breakdown 84/60/65/77 %. Its
only localization figures are DICE 0.72 and landmark error 1.01 +/- 0.153 px, and both are
**simulation-only**. No cadaver DICE or landmark error is reported, or computable: the 257 cadaver
frames carry phase labels alone. The paper says so — *"Although segmentation masks and anatomical
landmarks are not available for these images, we observe qualitatively satisfactory segmentation
masks"*. The number is also not stable across versions: arXiv v1 reported 93.8 / 67.57.

So the agreement with a per-vertebra recall is a coincidence between two different quantities, and a
reviewer who checked would find it. The dataset remains worth having as simulated sequence data. It is
not an external check on a detection number.

*(PMC11016332; doi:10.1007/978-3-031-43996-4_13; arXiv:2304.09285.)*

---

## What actually closes the gap — the methods, which this document previously omitted entirely

The first version of this file was a dataset-acquisition plan written as though data were the only
lever. The field's own matched controls say otherwise, and rank three levers. Every number below comes
from an experiment that varied **one thing**, with both arms evaluated on **real** images.

### 1. Simulation fidelity — already done here, and worth the most

Naive DRR to DeepDRR moves real-image landmark error **78.2 +/- 26.5 -> 34.4 -> 26.9 -> 24.7 +/- 21.3
mm** across the ablation, and roughly **68 % of the total gain comes from the polyenergetic
multi-material attenuation step alone**. Scatter and learned material decomposition are the small
remainder. Same training protocol in both arms, evaluated on cadaver C-arm radiographs — 78 real
X-rays for landmarks, 87 for the end-effector task — at *p* < 0.01.
*(Unberath et al., IJCARS 2019;14(9):1517-28; PMID 31187399.)*

**`tools/render_physics_drr.py` already implements this** — HU to a water / cortical-bone / titanium
basis over a six-bin polychromatic spectrum, plus scatter, Poisson, MTF and vignetting. That is
DeepDRR Ablation 4 modulo learned decomposition and Monte-Carlo scatter.

This also explains a local result rather than leaving it puzzling. Adding physics-correct noise to real
labelled radiographs measured at 11.6 points here. Noise realism is the **smallest** component of
DeepDRR's real-image gain, so that is about the expected size of the effect.

### 2. Strong domain randomization — the lever that was not pulled

On 366 real cadaveric C-arm images, DeepDRR **plus strong DR** reached **6.44 +/- 7.05 mm** against
**6.46 +/- 8.21** for the same architecture trained on real images — a zero-to-negative gap — with Dice
**0.86 +/- 0.21** against **0.79 +/- 0.25** at *P* = 2.3e-5. The ordering on real images is
realistic + strong DR about equal to real-data training, better than heuristic DRR, far better than
naive DRR (10.50 +/- 12.34 mm).
*(SyntheX; Nat Mach Intell 5:294-308, 2023; doi:10.1038/s42256-023-00629-1, Table 1.)*

`render_physics_drr.py` randomizes only **physically plausible** parameters — source-to-detector
550-780 mm, yaw +/-12 deg, scatter 0.03-0.30, gamma 0.7-1.4. In SyntheX's taxonomy that is *regular*
DR, and regular-to-strong is exactly the step that moved realistic simulation from below real-data
training to level with it. `tools/strong_dr.py` is that step, and `slurm/dr_chain.sh` runs it as a 2x2
against the noise term with a matched control that is proven rather than assumed.

**Two caveats the parity number cannot travel without.** The landmark difference is explicitly *not*
significant (*P* = 0.14) — an underpowered null, evidence of no *large* gap rather than of parity. And
the real-trained control is data-starved, about 310 cadaver images per leave-one-specimen-out fold.
SyntheX shows synthetic beats a *small* real set. It does not show synthetic matches a large real film
corpus like the 13,781 labelled films in hand here.

### 3. Scale

1k to 10k renders moved 6.61 -> 5.95 mm and collapsed the SD from 7.27 to 3.52. Training here uses
6,650 DRRs. Ten thousand renders is a grid job, not a dataset acquisition.

### What NOT to spend time on

**Learned image translation.** CycleGAN on top of realistic simulation plus strong DR scored
**6.62 +/- 6.82 mm** against **6.44 +/- 7.05** for no adaptation at all, and ADDA 6.41 +/- 6.27 — all
three inside each other's confidence intervals, with CycleGAN's point estimate *worse*. Both methods
also require real target-domain images at training time, in sufficient quantity and diversity to avoid
overfitting, which is precisely the thing that is scarce. *(Same table.)*

This is the direct answer to "can a network convert the DRR corpus into a fluoroscopic corpus, the way
DeepDRR converts CT into DRRs". Measured, against a matched control, on real images: it can, and it
buys nothing, and randomization gets there without the prerequisite.

### The caveat that matters most here

Every parity figure above is measured at **high confidence and low coverage**. The 2026 follow-up from
the same lab states the limitation itself: performance shows *"a rapid decline ... with less confident
predictions at lower thresholds"*. On DeepFluoro, synthetic-CT training beats real-CT at NCC 0.60
(5.82 vs 7.83 mm), ties at 0.40 (12.36 vs 12.32) and **loses** at 0.20 (23.64 vs 17.92) — the advantage
inverts with coverage, and every arm degrades hard, including the one trained on real X-rays.

A counting system cannot live at the high-confidence end. Recall compounds: 0.97 per body is 0.74 per
case over ten bodies. So every recall number here is reported as a **curve**, and the operating point
is wherever recall reaches 0.97, not wherever it looks best. *(arXiv:2606.21414.)*

---

## The honest ceiling

**There is no published system that detects vertebrae on real intraoperative fluoroscopy from image
content at per-body recall high enough to support counting, and there is no published per-vertebra
recall on real fluoroscopy at all.** Three candidate counterexamples were checked and all three fail
the comparison:

- **LevelCheck** transfers labels from the *same patient's* preoperative CT or MRI onto the radiograph
  by 3D-2D registration. Its 100 % is a geometric label-placement success metric — projection distance
  error 4.3 +/- 2.6 mm, 0 % failure rate — not detection or naming from radiograph content, and it
  cannot run without a per-patient prior volume carrying human annotations. *(PMID 27035579, 28050972.)*
- **Pelphix** — phase classification; no per-structure cadaver metric exists. See above.
- **The DeepDRR / SyntheX line** reports landmark millimetre error only. Recall is never reported: the
  method *discards* landmarks whose belief map peaks below 0.4, and the discarded fraction is not
  stated anywhere. All real-image evaluation is cadaver hip and pelvis, never live intraoperative
  spine, and per-structure error on 14 spatially distinct hip landmarks does not compound the way
  counting does.

Two consequences. The 71.67 % figure has **no published peer**, which is a hazard — there is no
baseline to sit against — and an opportunity, because the compounding metric a counting system
actually needs is one nobody reports. That gap is the contribution available here, and it belongs in
the manuscript as a stated finding rather than being hunted for as a number to beat.

---

## VerSe is regional; TotalSegmentator is the whole-spine source

Measured 2026-09-21 on `~/VerSeFusion/data/unified` (374 CT+mask pairs, ~0.3 × 1.25 mm, LPS): of 120
masks, 31 contain C2 and **one** runs from C2 to the lumbar spine. The common spans are L1–L5 (17),
T8–L5 (13) and C1–T3 (23). So VerSe supplies vertebral *shapes* at every level but almost never a
continuous C2 → sacrum volume. For a simulated whole-spine sweep the anatomy source is TotalSegmentator's
whole-body CTs, which carry `vertebrae_C2` and `sacrum` as separate masks; see `docs/DEEPFLUORO_FORMATION.md`.

## Not worth acquiring

| | why |
|---|---|
| Multi-modal Femoral Head Imaging | only 10 patients uploaded; labels are ONFH stage I–IV, not landmarks; images pre-cropped to the femoral head so the centre is the centre by construction; AP, where PI is measured on lateral. The 802 CTs here with hips 30/31 and femora 32/33 give exact bicoxofemoral landmarks projected into any view, for nothing. |
| Hip fracture x-rays (YOLO) | plain radiography, wrong anatomy; 13,781 labelled real films already in hand |
| Lumbar spine MRI, 1,038 mid-sagittal | right anatomy, wrong modality entirely |
| Femoropopliteal stent, 128 images | same use as Tier 3 but smaller, and a fluoroscopy *room* rather than a mobile C-arm |
| CM Spine, 208 intraoperative lumbar G-arm | genuinely relevant but email-request only; send the email, do not wait on it |

---

## What none of these supply

**The commanded sweep on a live patient.** Every published fluoroscopic figure and every set above is
either a single exposure, a rotational run, or a cadaver. The method needs consecutive overlapping
frames of one patient at a known cranio-caudal step, and the only routes to that are a **phantom on a
real C-arm** (no IRB, weeks, and the cheapest instrument that touches the untested mechanism), a
retrospective PACS protocol, or the LevelCheck DUA. DeepFluoro is the one external set that could
partially substitute, and only if translated pairs turn out to exist in it.
