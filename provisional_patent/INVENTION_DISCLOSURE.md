# Invention disclosure — registration-free intraoperative vertebral level identification

**For the technology transfer office and patent counsel. Internal. Not for distribution.**

Not legal advice. This is an engineering disclosure written so that counsel can draft from facts. Every
mechanism below is implemented and measured; file and line references are to the working code.

---

## 1. The problem, stated as a technical problem

A surgeon operating on the spine must know which vertebra is in the fluoroscopic image. The image typically
shows two to four vertebral bodies and no anatomical landmark — no sacrum, no ribs, no skull. Adjacent
vertebrae closely resemble one another, so the information that distinguishes them is not position in the
image but **position in a chain whose end is known**, and that information is not present in the pixels of a
limited field.

Existing automated solutions do not solve this; they **import** the answer. Every deployed system registers a
preoperative CT or MRI, in which a human has already numbered the vertebrae, onto the live radiograph. Three
consequences follow: it is unavailable when no preoperative volume exists; a miscounted preoperative scan is
transferred onto the radiograph faithfully and with full confidence; and the patient's volumetric imaging
must be transported to and processed by the registration system.

The consequence in practice is measurable. One quaternary centre performed **179 preoperative percutaneous
gold-fiducial placements over 38 months, 176 of them thoracic, at a mean of 52 minutes and 183 mGy each**,
solely to mark a level for the surgeon — a second invasive procedure, scheduled in advance, because the level
was judged undeterminable in theatre.

## 2. The invention

A sequence of overlapping projection images is acquired along the spine and **linked on the vertebrae the
successive images share**, forming an ordered chain specific to that patient. The chain supplies the two
facts a single limited field lacks: that its vertebrae are consecutive, and where the run terminates. Later
limited-field images are registered onto that chain and named under its ordering constraint.

The chain is built **from the radiographs themselves**. There is no preoperative volume, no optical or
electromagnetic tracker, no calibration phantom, and no fiducial. The physical scale is recovered from the
patient's own anatomy.

Five aspects are put forward for protection. Each is implemented; each is measured.

---

## 3. What is put forward, and the mechanism of each

### A. Closed-loop acquisition control — commanding where the imaging device must move

A confidence is computed at run time, with no access to ground truth, from **two independent failure modes**:

```
confidence = (lowest per-vertebra probability in the decoded naming)
             × clip(chain_margin / τ, 0, 1)
```

where `chain_margin` is, for the weakest link in the chain, the peak image-similarity score minus the best
score achievable at any displacement differing by more than half a vertebral spacing
(`tools/sweep_map.py:550-552`, `:1239-1241`). The first term fails when the appearance is ambiguous; the
second when the geometry is — a link that cannot distinguish its own offset from a one-vertebra offset puts
every name above it wrong, and it says so before any answer is given.

When the confidence falls below threshold the system **computes the distance the imaging device must travel
and emits it**, as a signed displacement with a direction. The same value serves a robotic gantry as a
control signal and a human operator as an instruction.

The displacement is derived from the image in hand:

```
step = field_span − (overlap_in_vertebrae × observed_vertebral_spacing)
```

with the pixel-to-millimetre conversion recovered from the **patient's own vertebral spacing** — the median
observed centre-to-centre distance divided by the regional anatomical spacing constant
(`body_pitch_px`, `:135-148`; `prior_dy`, `:1096`). On an image carrying no calibration metadata this is the
only scale available, and it is sufficient.

Which remedy is commanded depends on **which** term is low: an ambiguous appearance calls for extending the
chain toward the landmark; an ambiguous geometry calls for a shorter step that increases overlap on the weak
link.

> **Measured, and it constrains the claim.** Simply re-acquiring the same view does *not* help: across 4,792
> query frames the retake scored the same as the frame it replaced at every coverage level (95.7 % against
> 95.3 % for answering everything). What helps is **overlap between linking frames** — at one vertebra of
> overlap the share of frames answerable at 99 % accuracy halves, 82 % → 42 %. The claim must therefore
> recite acquiring a further *linking* image, not re-acquiring the query image.

**Implemented and exercised end to end** (`tools/acquisition.py`, `tests/test_acquisition.py`,
`tools/guided_console.py`; measurement on the render corpus running as `slurm/guided_validate.sh`). Four
further elements emerged from building it, and each is worth reciting because each was arrived at by a
failure that the obvious version does not survive:

1. **The direction of the column is determined from the landmark, not assumed.** An intraoperative image
   carries no promise that the head is at the top: the intensifier rotates and the readout flips. The
   landmark is located by posterior over every body in the field — *not* by its position, which is the
   unknown — the column's axis is taken from the body centres, which fixes the line, and the landmark fixes
   the sign, a sacrum being the caudal end of the run by definition. Each image is then rectified into that
   direction, and the commanded displacement is transformed back into the device's own axes. The operator is
   told anatomy, which needs no transform; a positioner is given the vector. Photographed at 0°, 90° and 180°
   the same subject gives the same run and the same names. **Without this the failure is not a worse answer:
   the images do not overlap at all and no run exists.**
2. **The remedy is directed at the ambiguous seam, not at the end of the run.** Commanding a shorter step
   adds an image at the end of the run; an ambiguous link three images back is not overlapped by anything
   acquired there. The system computes the displacement from where the device is now **to the midpoint of
   the seam that will not link**, from the link shifts themselves. In testing, the run that had been
   reporting the same margin three times over and declaring the geometry irreducible completed in four
   exposures with every name correct.
3. **The escalation is capped short of a re-acquisition.** Increasing overlap in a field that holds four
   bodies reaches a step of a few millimetres — the same image again, the one remedy already measured not to
   work. The overlap is bounded so a whole further vertebra always enters the field, and when it cannot be,
   the system declines.
4. **The displacement is measured, not accumulated.** The distance back to the operative field comes from
   the link shifts rather than from the sum of what was commanded, so an operator's execution error does not
   accumulate. On a synthetic subject, after four steps executed with ten per cent error, every image's
   position was recovered from the images alone to within **1.2 mm**, the system never being told where the
   operator went.

### B. Determining level in fewer exposures

The chain constraint reduces the number of exposures needed to reach a stated confidence — a reduction in
radiation dose and in procedure time.

| Overlap | Exposures per sweep | Chain complete |
|---|---|---|
| half a vertebra | 2.5 | 86.7 % |
| one vertebra | 2.6 | 95.0 % |
| **two vertebrae** | **3.0** | **96.7 %** |
| four vertebrae | 6.9 | 80.0 % |

The relationship is not monotone: past two vertebrae of overlap each additional image is another link that
can be joined wrongly, so more exposures make the result worse. Two vertebrae is the operating point.

### C. Representing a supernumerary segment without a rare class

A vertebral column may carry a sixth lumbar or a thirteenth rib-bearing segment. Treating these as
additional classes fails, because they are vanishingly rare in any training corpus.

Instead, candidate namings are scored against **several alternative alphabets**, each a different admissible
sequence of level names, one of which contains the extra segment (`alphabet()`, `:652-657`;
`decode_alphabets()`, `:687-728`). A naming must be a **contiguous run** of one alphabet, and a declared
landmark pins one end of the run. The winning alphabet is the variant call; its margin over the best ordinary
naming is the confidence in that call. A variant is therefore a **different alphabet, never a rare class**.

An accompanying convention delimits a transitional segment by **the presence of a disc** rather than by the
extent of fusion — the disc being the feature that is actually visible and decidable.

### D. Determining level without the imaging leaving the room

All computation runs on the imaging device or an attached embedded module. No patient image is transmitted,
no network link is required, and no preoperative volume is transported. This is a structural distinction from
every registration-based method, which requires the volumetric study to be moved to and processed by the
registration system.

*Measured support:* 2.29 ms to name a vertebra and 22.94 ms to detect vertebrae in a frame on a datacentre
GPU; 18.30 ms and 330.58 ms on eight CPU threads (`benchmark/data/latency_v100.json`). **Timing for the
linking, stitching and registration stages is not yet measured and must be before this aspect is relied on.**

### E. Placing a persistent digital marker at a confirmed level

Once a level is confirmed, the system **places a marker at that vertebra and carries it forward** — each
subsequent image is registered onto the same chain and the marker re-projected into it, so the mark persists
across exposures and across movement of the imaging device. It is retained when a later frame is declined,
because a marker that disappears when confidence dips is not serving its purpose.

This displaces the physical fiducial placement described in §1: an invasive, separately scheduled procedure,
replaced by a computed one.

**Implemented** (`FiducialBoard`, `tools/acquisition.py`). One element must be recited with it, and it was
found by testing rather than by reasoning: **the marker is asserted only when the registration carrying it
can rule out a displacement of one vertebra.** A column is periodic at the vertebral spacing, so a later
image correlates nearly as well one body off as in the right place. A mark placed on L1 projected onto T12
in two later images of five — on T12's centre to within a pixel, at peak correlation 0.78 against 0.83 for
the correct ones, which is not a quantity that separates them. The projection now carries the same margin
the linking step uses, and where the margin is insufficient the mark is **retained, flagged, and reported
with its last good position** rather than placed. Of the positions asserted in testing, every one is on the
marked vertebra. A marker that silently sits on the vertebra above is the exact failure this work exists to
prevent, so the guard is not an optimisation; it is part of the invention.

---

## 4. Claim scope — the claims must reach competitors, not only this implementation

The common failure is claiming the embodiment. A claim reciting a particular network, a particular similarity
measure and a particular field size is designed around by substituting any of them.

| Do not recite in an independent claim | Recite instead |
|---|---|
| a named network architecture | "a trained model producing, for each detected vertebra, a distribution over level identities" |
| normalised cross-correlation | "determining a spatial offset between successive images from content in their overlapping region" |
| a C-arm | "an imaging device acquiring successive projection images at positions along a subject's spine" |
| specific tolerances (0.4×, 0.6×, 45 %, 155 %) | "a tolerance derived from the spacing between adjacent vertebrae observed in the image" |
| a 9-inch field / 140 mm | "a field of view spanning fewer vertebrae than are required to reach an anatomical landmark" |
| "L6", "T13" | "an alphabet admitting a repeated symbol, such that a supernumerary segment is represented without adding a class" |
| any accuracy figure | nothing — accuracy belongs in the specification as support, never in a claim |

Further:

- **Claim both sides.** A method claim, an apparatus claim and a computer-readable-medium claim, so software
  sold alone is reached as well as a machine. For aspect A, also claim **the emitted displacement itself**,
  so a product that merely issues the instruction infringes without moving anything.
- **Do not let "spine" narrow to "lumbar."** The largest measured effect is thoracic.
- The specific values above belong in **dependent** claims, where they are fallback positions if an
  independent claim is narrowed during prosecution.

---

## 5. Subject-matter eligibility — the principal drafting risk

The risk here is §101, not prior art, and the controlling authorities are recent and specific.

**Do not claim accuracy.** The 2024 USPTO guidance adopts the position that improving the accuracy of a
computed prediction is an improvement to the **abstract idea**, not to technology. The measured results in
the accompanying manuscript are an accuracy argument; **the claims must not be.**

**Hardware plus an acquisition loop is not sufficient on its own.** In *Dental Monitoring S.A.S.* (Fed. Cir.
No. 24-2270, 7 July 2026) claims requiring a specific acquisition device, an image-quality comparison, and a
message guiding the operator to retake the image were held abstract — "collecting information, analyzing it,
and displaying certain results."

**What survives is an act that changes the technical system.** The USPTO's own examples make the distinction
within a single invention:

- *Example 47, claim 2* — a network detects anomalies. **Ineligible.**
- *Example 47, claim 3* — same detection, then *detect the source address, drop the packets, block future
  traffic*, in real time. **Eligible**, as an improvement in the technical field.
- *Example 49, claim 1* — "administering an appropriate treatment." **Ineligible.**
- *Example 49, claim 2* — "wherein the appropriate treatment is Compound X eye drops." **Eligible.**

The difference in each pair is that the claim **acts**, and that the act is **specific**.

Aspect A is drafted to that pattern: it does not stop at a level name, it computes a physical displacement
and causes the imaging device to move or the operator to move it. That is not a display of results. Aspect E
follows Example 49's shape, with specificity supplied by what is placed and where.

**Two drafting constraints, both from the same opinion:**

1. The technical advance must appear **in the claim language**. The court refused to credit an advance argued
   from the specification or by attorney characterisation.
2. **Do not describe the model as selectable from off-the-shelf networks.** The court found no genuine issue
   of fact on conventionality *because the patents' own text named commercially available networks*, which
   destroyed the *Berkheimer* dispute that would otherwise have defeated summary judgment.

A curated training corpus earns nothing at §101 (*Recentive Analytics v. Fox Corp.*, 134 F.4th 1205, 1212
(Fed. Cir. 2025)) — which is a reason to hold the corpus as a trade secret rather than describe it.

---

## 6. Freedom to operate

| Patent | Assignee | Required limitation we do not practise | Status |
|---|---|---|---|
| **US 11,284,846 B2** | Siemens Healthineers + JHU | claim 1 step (a): *"acquiring a preoperative 3D computer-tomography (CT) image of a vertebra"*. Only 3 claims total, 1 independent; the C-arm limitation is in dependent claim 3, which still inherits step (a) | **Clear** — expires 2034-09-14 |
| **US 10,368,956 B2** | Johns Hopkins | all four independent claims require *"a preoperative 3D magnetic resonance image"*, **and** a final step displaying that volume *registered onto* the 2-D image | **Clear** — expires 2037-02-16 |
| **US 12,223,118 B2** | — | sole independent claim requires the stored image be *"based on a three-dimensional representation of the surgical field"* | **Clear** |
| **US 8,718,346 B2** | **NuVasive** (orig. Saferay Spine) | claims 1, 33, 47 require *"digitally manipulating a previously-acquired high resolution baseline image to produce a baseline image set... at a plurality of permutations of movements in 4D or 6D space"*; claim 36 requires *"a tracking device that monitors position of the imaging device"* | **Clear** — we produce no permuted baseline set and use no tracker. Expires 2031-10-05 |

Under the all-elements rule, a claim is infringed only if every limitation is present. Each row names a
limitation we affirmatively do not practise.

**Prior art regardless of infringement.** US 10,368,956's specification discloses automatic vertebra
labelling on intraoperative fluoroscopy for wrong-level prevention — in registration-dependent form. US
8,718,346 discloses, but does not claim, stitching multiple C-arm exposures into a composite, and displaying
vertebral level labels on such a composite — but **the labelling there is an explicit manual act by the
surgeon via a pull-down menu and drag-and-drop**, with no automatic determination of which vertebra is which,
and **no claim recites labelling, naming or identifying a vertebra at all**.

**Not yet done:** the INPADOC family sweep for continuations and divisionals of all four. A continuation with
broader claims is where a blocking claim would live, and this is the first search to commission.

---

## 7. Novelty over the published literature

A verified survey found **one** published system naming vertebral levels on intraoperative radiographs
without registering to a preoperative volume: a multi-perspective CNN on long-length images, **88.3 %
labelling accuracy**, 13 cadaveric specimens, at a **full ~64 cm field of view** where the entire spine is
visible. Its widely quoted ">96 %" is a *detection* score, not naming.

Everything else imports identity (from a preoperative CT, from the same patient's prior full-length film, or
from implanted hardware), counts from a landmark and is undefined when that landmark is out of frame, or
operates on volumetric CT rather than radiographs.

Three findings cut across the field: **no method addresses transitional anatomy**; **no method releases code
or weights**; and no two report the same quantity — registration convergence, label placement conditioned on
a correct CT, surgeon questionnaire scores, detection F-scores and naming accuracy are routinely tabulated as
though comparable.

---

## 8. What a provisional must contain

Sufficient detail to enable the claims later drafted — a placeholder that names the idea will not support
them. All of the following exists and must be written as disclosure:

- the acquisition protocol and its overlap parameter, with the field-size derivation (a 23 cm detector, ~90 %
  usable, at ~1.5× magnification, giving ~140 mm at the spine);
- the linking rule: the asymmetric search window about the commanded step, the overlap-band validity gates,
  the anisotropic assignment metric and its tolerance, and the block-scoring rule that tolerates unsupported
  pairs rather than requiring unanimity;
- the chain structure, multi-view pooling, and the chain margin;
- the alternative-alphabet decode, its scoring, and the landmark constraint;
- the two-term confidence and the displacement it commands, in both machine and operator form;
- the prediction-set and region output, and how its threshold is calibrated;
- the box-repair rule derived from local spacing, with its two refusals — never more than two inserted
  bodies, never beyond the ends of the run;
- the recovery of physical scale from anatomy on uncalibrated images;
- the marker placement, its propagation across frames, and the margin condition under which a position is
  asserted rather than retained;
- the determination of the column's direction from the landmark, the rectification, and the transformation
  of the commanded displacement into the device's axes;
- the selection of which landmark to run from, and the number of exposures that implies, from the level
  being operated on: cervical work is one exposure from C2 and six from the sacrum, lumbar work the
  converse, and the mid-thoracic spine — where both landmarks are distant, where no single field contains
  one, and where the measured gain is largest — is the case the whole method is for.

**What is NOT yet measured, and must not be implied.** The acquisition loop's numbers above are from a
synthetic subject; the measurement on the render corpus is running and is not in hand. The linking,
composition and registration stages have still never been timed, so no latency representation should be made.
The marker has never been exercised on real fluoroscopy. The geometric threshold is calibrated on renders,
and its value is a property of image texture.

---

## 9. What not to patent

- **Trained weights.** A patent publishes the method; weights are better held as trade secret, protected by
  the deployment already in place (inference behind a service, weights in a private repository, never served).
- **The training corpus and its curation.** *Recentive* and *Dental Monitoring* say plainly this earns
  nothing at §101. It is a practical moat and worth nothing in a claim.
- **The dataset.** Not patentable subject matter; protect by licence.

---

## 10. First questions for counsel

1. The **INPADOC family sweep** for continuations of the four patents in §6.
2. Whether aspect A's commanded-displacement step survives *Dental Monitoring* — our distinction is that the
   act changes the **geometry** of the next acquisition rather than its quality, and is computed from a
   run-time confidence. That is an argument, not a settled answer.
3. Divided infringement on aspect E, and whether drafting the marking and propagation as system-performed
   avoids it.
4. University ownership: the disclosure process, timing, and what happens if the university declines to file.
5. The accompanying confidential memorandum on publication timing.
