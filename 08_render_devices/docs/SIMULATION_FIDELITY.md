# How real is the simulated C-arm, in plain terms

This file exists so the fidelity question can be answered without reading the physics code. It says what
is modelled, how we know each piece is right, what is guessed, and what is missing. Where a number was
wrong and got corrected, that is recorded rather than quietly replaced.

The short version: **the simulation is built from measured constants, not tuned until it looked right,
and it is checked against five numbers that came from outside it. Four agree. One does not, and the
reason is the real images have been through a printing press.**

---

## What a frame goes through, in the order the physics happens

Each step is what actually happens to X-rays between the tube and the screen. Nothing here is a filter
chosen because it made the picture look better.

| # | step | what it does | where the number comes from |
|---|---|---|---|
| 1 | **geometry** | magnifies the anatomy, warps it if the receptor is a round tube | magnification 1.2–1.6 measured on prone intraoperative spine fluoroscopy |
| 2 | **primary transmission** | the beam is absorbed passing through the patient | attenuation of water at the beam's effective energy, from published half-value layers |
| 3 | **beam hardening** | the beam gets more penetrating as it crosses more tissue | computed from X-ray spectra, checked against three national calibration beams |
| 4 | **heel effect and vignetting** | the beam is not equally bright across the field | 22 % top-to-bottom, measured on a Siemens mobile C-arm |
| 5 | **scatter** | a haze from X-rays bouncing inside the patient | scatter-to-primary from measured curves, per anti-scatter grid ratio |
| 6 | **dose control** | the machine raises output until the detector gets its target dose | the increment that doubles required output, 4.2 cm, agreed by two sources |
| 7 | **generator ceiling** | on a thick patient the machine runs out and the image degrades | mobile C-arms top out near 120–125 kV at 18–20 mA |
| 8 | **quantum noise** | X-rays arrive as countable particles, so the image is grainy | 10–70 nanogray per frame, measured on a mobile C-arm |
| 9 | **blur** | the focal spot and the detector are not infinitely sharp | manufacturer resolution figures for real C-arm receptors |
| 10 | **veiling glare** | light spreads sideways inside the receptor | 4–15 % for a tube, 8 % for a panel |
| 11 | **readout noise** | the electronics add their own grain | derived from each receptor's published noise-equivalent dose |
| 12 | **field stop** | the image is a **circle** on a tube, a square on a panel, and the collimator stops it down further | the tube is round; how far operators collimate is not published |
| 13 | **saturation** | the detector clips where the beam misses the patient | assumed |
| 14 | **display** | log and auto-window, the way a C-arm renders its own image | matches the existing renders |

---

## The five outside checks

A simulation can be tuned until it agrees with itself. These are numbers other people measured, which
this simulation could not have produced.

| what | this simulation | what others measured | verdict |
|---|---|---|---|
| photons arriving per pixel | 427 (IQR 258–734) | 219–1532 | **agrees** |
| does the machine run out of output where thickness says it should | only above the ceiling, never below | should pin only on thick patients | **agrees** |
| how uneven the scatter haze is across a field | 2.9 | 1.4–2.9 | **agrees, at the top of the range** |
| grain coarseness, after accounting for publication | centroid 0.46 | 0.45 | **agrees** |
| grain coarseness, raw | centroid 0.68 | 0.45 | **disagrees — see below** |

**The one disagreement, and what it turned out to be.** Raw simulated frames have finer grain than
published fluoroscopy images. Two things could cause that. The obvious one is that every C-arm smooths
its live image by averaging frames, and published pictures are usually screen-grabs of that. That was
tested first and **refuted**: averaging frames makes noise fainter, not coarser. The real cause is what
happens to a picture on its way into a journal — it gets shrunk and JPEG-compressed, both of which
remove fine detail. Putting the simulated frames through the same treatment moves them to 0.46 against
a measured 0.45. So the disagreement was never the physics; it was comparing a raw frame against a
printed one.

---

## What is guessed, and how much it matters

Five of nineteen parameters are stated guesses because nobody publishes them. They are named so that a
reader can discount them.

| guessed | why nobody knows | what we do about it |
|---|---|---|
| how fast the dose control settles after the C-arm moves | no settling time for any fluoroscope exists in the literature | swept from "fully caught up" to "not moved at all" |
| how much of the scatter haze is perfectly flat | no paper states it | checked against the measured unevenness of a real scatter field |
| brightness falloff to the edge of a tube | only described in words, never measured | held inside the quality-control tolerance so a failing tube is out of scope |
| how far operators collimate | not published | swept |
| where the detector clips | no manufacturer publishes it | set above the brightest thing in the frame |

---

## What is deliberately not modelled, and why

Omissions with reasons, so they are not mistaken for oversights.

- **Anti-scatter grid lines.** A mobile C-arm's grid runs 40 to 74 lines per centimetre, a period of
  0.14 to 0.25 mm. These frames are 0.8 mm per pixel, so a grid line is a fifth to a third of one pixel.
  It cannot be resolved. Drawing one would invent structure the sampling forbids.
- **Frame averaging.** Every C-arm smooths its live picture, but it throws away the first three to nine
  frames after any change and needs three to thirty to settle. A protocol that moves the C-arm and takes
  **one** exposure sits inside that window, so there is nothing to average. Modelling it would make
  these frames cleaner than the protocol can actually deliver.
- **Cone-beam divergence.** The underlying projection is parallel, so magnification here is a uniform
  scale rather than true perspective. This is why the field-size study reports a scale mismatch rather
  than a source-to-object distance.
- **Patient motion, detector lag, and the console's edge enhancement.** Not modelled. The first two
  would make things worse; the third would make the simulation look sharper without being more
  informative.

---

## Three things that were wrong and are now right

Recorded because the interesting part of a fidelity claim is what it survived.

1. **The photon budget was ten times too generous.** It was set from a detector dose figure that belongs
   to digital subtraction and cine imaging, not fluoroscopy. Every simulated frame was about ten times
   cleaner than a real one, which would have made every robustness number look better than it is.
2. **The exposure term did nothing at all.** It was applied after the logarithm, and the automatic
   window that follows removes a multiplicative change exactly. It produced byte-identical frames for
   any value. Moving it before the photon count fixed it, and the insight underneath is that brightness
   mismatch between two frames is *not* the threat it appears to be — the noise is.
3. **The blur was two to four times too large, and the electronic noise two to eight times too small.**
   Both were caught by published receptor figures, and the blur independently by the fact that a real
   detector's noise correlation is far lower than the old blur implied.

---

## What this buys, and what it costs

Counting was 99.7 % exact on the frames this project used before: a bone-only projection with brightness
and contrast jitter. On physically simulated frames, on the same spines with the same seed:

| frames | exact |
|---|---|
| the old degradation | 99.7 % |
| physics, good anti-scatter grid | 89.4 % |
| physics, weaker grid | 78.4 % |
| physics, no grid | 59.4 % |

**The grid matters thirty points; the detector matters two.** Mobile C-arms are often run without a
grid in orthopaedic work, and there is published argument that it is unnecessary on dose grounds. For
this task it is not optional.

The reason is measurable. In a lateral projection the total attenuation through a disc space is within
about one per cent of that through a vertebral body — at the disc the beam crosses the facets and the
pedicle, which are dense bone. So vertebrae are not countable from brightness; they are countable from
**pattern**, and scatter is a haze that attacks pattern.
