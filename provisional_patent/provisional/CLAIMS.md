# DRAFT CLAIMS

**For counsel to redraft. Claims are not required in a provisional application (37 CFR 1.51(c)) and these
are not intended to be filed as claims.** They are here for one reason: a provisional is worth only what its
specification enables, and the way to check that the specification enables enough is to write down what will
be claimed in twelve months and confirm every limitation is supported. Each claim below carries a pointer to
the paragraph of `SPECIFICATION.md` that supports it.

Two drafting constraints run through all of them, both from *Dental Monitoring S.A.S.* (Fed. Cir. No.
24-2270, 7 July 2026): the technical advance must appear **in the claim language**, not be argued from the
specification; and **no off-the-shelf network is named anywhere**, because naming commercially available
models is what destroyed the *Berkheimer* dispute in that case. A third, from *Recentive* (134 F.4th 1205)
and the 2024 USPTO guidance: **no claim recites an accuracy**. The measured results are support, never
limitations.

---

## Family A — closed-loop acquisition control

*The lead family. Pattern: USPTO Example 47 claim 3 — detect, then **act** in the physical world.*

**1.** A method of controlling a projection imaging device, comprising:

&nbsp;&nbsp;(a) acquiring, with an imaging device, a plurality of projection images at successive positions
along a vertebral column of a subject, each image after the first overlapping a preceding image in a region
containing at least one vertebral body; *[0031]–[0036]*

&nbsp;&nbsp;(b) determining, from image content within said region of overlap, a spatial displacement between
each such pair of images, and therefrom which vertebral bodies the pair has in common; *[0045]–[0055]*

&nbsp;&nbsp;(c) forming an ordered structure in which each element corresponds to one vertebral body of the
subject and aggregates the appearances of that body across the images in which it appears; *[0056]–[0057]*

&nbsp;&nbsp;(d) assigning level identities to the elements of the ordered structure, subject to the
constraint that the identities are consecutive within an admissible ordering and that a declared landmark
occupies a terminus of the ordering; *[0058]–[0061]*

&nbsp;&nbsp;(e) computing a confidence from (i) a lowest probability assigned to any identity assigned to a
body appearing in a given image and (ii) a margin, for at least one said pair, between the similarity at the
determined displacement and a greatest similarity attainable at a displacement differing therefrom by more
than half a spacing between adjacent vertebral bodies; *[0066]–[0067]*

&nbsp;&nbsp;(f) responsive to the confidence failing a criterion, computing a displacement **expressed in
units of length** through which the imaging device is to be moved in order to acquire a further image that
overlaps an image of said plurality, the displacement being derived from a spacing between adjacent vertebral
bodies observed in at least one said image; and *[0068]–[0069]*, *[0037]–[0039]*

&nbsp;&nbsp;(g) emitting the computed displacement as at least one of a control signal to a positioner
carrying the imaging device and an instruction to an operator of the imaging device. *[0068]*

> **On (f).** "A further image that overlaps an image of said plurality" is the limitation that excludes a
> re-acquisition of the failing image, which [0070] measures as not working. Do not soften it.
> **On (g).** Drafted in the alternative so that a product which merely *emits* the instruction infringes
> without moving anything, and so that the overwhelmingly manual installed base is reached.

**2.** The method of claim 1, wherein the displacement of (f) is computed, where the margin of (e)(ii) fails
the criterion, as a displacement from a present position of the imaging device to a position intermediate
the positions of the two images forming the pair whose margin failed, said positions being determined from
the displacements of (b). *[0071a]*

**3.** The method of claim 1, wherein the displacement of (f) is bounded such that the further image
contains at least one vertebral body not contained in the image most recently acquired. *[0071b]*

**4.** The method of claim 1, further comprising computing a displacement from a present position of the
imaging device to a position at which an earlier image of said plurality was acquired, said displacement
being determined from the displacements of (b) rather than from a sum of displacements previously commanded.
*[0071c]*

**5.** The method of claim 1, further comprising selecting the declared landmark from a plurality of
candidate termini of the vertebral column by computing, for each, a number of images required to reach a
level of interest, and selecting the candidate requiring the fewer. *[0071d]*

**6.** The method of claim 1, further comprising, prior to (b), determining a direction of the vertebral
column within the images by (i) locating the landmark by a distribution emitted over every detected body in
an image, independently of the position of any body within that image, (ii) fitting an axis to positions of
the detected bodies, and (iii) resolving a sense of the axis using the located landmark; and transforming
the images into that direction. *[0071e]–[0071f]*

**7.** The method of claim 6, wherein the displacement of claim 1(g) is emitted to the positioner as a
vector in axes of the imaging device obtained by transforming the displacement by the determined direction,
and is emitted to the operator as a distance and an anatomical direction. *[0071e]*, *[0071f](5)*

**8.** The method of claim 6, wherein, where the landmark is absent from a first image, the sense of the
axis is provisionally assigned, and is inverted and the determining of (b) repeated responsive to a failure
of (b) to return a displacement. *[0071g]*

**9.** The method of claim 1, wherein the spacing of (f) is obtained as a measure of central tendency of
distances between centres of adjacent detected bodies, divided by a stored anatomical spacing for a region
of the vertebral column, whereby no calibration datum, phantom or tracking device is required. *[0037]–[0039]*

**10.** An apparatus comprising an imaging device, a positioner, and a processor configured to perform the
method of claim 1.

**11.** A non-transitory computer-readable medium storing instructions that, when executed, cause a
processor to perform the method of claim 1.

**12.** A control signal emitted by the method of claim 1, comprising a displacement in units of length and
a direction along a vertebral column, computed from a confidence determined per claim 1(e).

> **On 12.** Counsel to advise whether a signal claim is available; if not, capture the same scope in an
> apparatus claim reciting an output interface.

---

## Family B — determining level in fewer exposures

*Pattern: Example 48 claim 2 — an improvement to the functioning of the imaging modality, not to the
accuracy of a prediction. This is the framing that sidesteps* Recentive.

**13.** A method of reducing the number of radiographic exposures required to determine the identity of a
vertebra appearing in a projection image whose field of view spans fewer vertebral bodies than are required
to reach an anatomical landmark, comprising the steps of claim 1(a)–(d) and assigning to the vertebra the
identity of the element of the ordered structure onto which it registers, wherein the images of claim 1(a)
overlap by a predetermined number of vertebral bodies selected such that the number of exposures required is
reduced relative to acquiring images spanning the distance to the landmark. *[0035]–[0036]*, *[0072]–[0076]*

**14.** The method of claim 13, wherein the predetermined number is at least one and not more than three
vertebral bodies. *[0035]*

---

## Family C — transitional anatomy

*The strongest novelty. No surveyed method addresses transitional spines at all.*

**15.** A method of assigning level identities to vertebral bodies of a subject, comprising: obtaining, for
each of a plurality of detected bodies, a distribution over candidate identities; constructing a plurality of
admissible orderings of identities, at least one of said orderings containing a segment absent from another
of said orderings; scoring, for each ordering, assignments in which the identities assigned to the bodies are
consecutive within that ordering and a declared landmark occupies a terminus; and outputting the assignment
of the best-scoring ordering together with an indication of which ordering it was and a margin over a
best-scoring assignment within a different ordering. *[0058]–[0062]*

**16.** The method of claim 15, wherein each said ordering draws its identities from a single output space,
whereby an ordering containing a supernumerary segment is accommodated without an additional class and
without retraining. *[0061]*

**17.** The method of claim 15, wherein the bodies are drawn from a plurality of projection images linked
per claim 1(b)–(c), whereby the orderings are distinguishable although no single image contains the segment
that distinguishes them. *[0062]*

**18.** The method of claim 15, further comprising delimiting a transitional segment by presence of an
intervertebral disc rather than by extent of osseous fusion. *[0065]*

---

## Family D — determining level without the imaging leaving the room

**19.** A method per claim 1 or claim 13, wherein every step is performed by a computing unit situated at
the imaging device, such that no projection image of the subject is transmitted beyond a room containing the
imaging device and no previously acquired volumetric study of the subject is transported to or processed by
the computing unit. *[0029]*, *[0085]–[0086]*

> **Do not file a latency limitation.** [0087] states plainly that the linking, composition and registration
> stages have never been timed. A claim reciting a time bound would not be supported.

---

## Family E — the persistent digital marker

*Pattern: Example 49 claim 2 — specificity of the act is what carries it. "Place a marker at the vertebra
identified by the chain, at the mapped coordinates, and propagate it by re-registering later images onto the
same chain" is that level of specificity.*

**20.** A method comprising: forming an ordered structure per claim 1(a)–(d); responsive to confirmation of
an identity, storing a marker associated with an element of the ordered structure, with coordinates of the
corresponding body in an image; and, for each subsequently acquired projection image, registering that image
onto the ordered structure by image content and projecting the stored marker into that image through the
registration. *[0080]–[0082]*

**21.** The method of claim 20, wherein the projecting is performed only where a margin of said
registration, between a similarity at the accepted registration and a greatest similarity attainable at a
displacement differing therefrom by more than half a spacing between adjacent vertebral bodies, satisfies a
criterion; and wherein, where it does not, the marker is retained and an indication is emitted that the
present image does not support it, together with a last supported position. *[0083a]*

**22.** The method of claim 20, wherein, where the marked body lies outside a field of a subsequently
acquired image, a distance and direction from that field to the marked body are emitted in units of length.
*[0083b]*

**23.** The method of claim 20, wherein the marker is retained across an image for which no identity is
asserted. *[0083]*

> **Divided infringement.** Every step of 20–23 is performed by the system. Do not add a step performed by
> a surgeon.

---

## Supporting subject matter also disclosed, for dependents or a continuation

| | supported at |
|---|---|
| asymmetric search window about the commanded step, and the aliasing it defeats | *[0047]–[0048]* |
| anisotropic assignment tolerance derived from observed spacing | *[0051]* |
| robust block scoring tolerating unsupported pairs | *[0052]–[0055]* |
| pooling a body's appearances across the images containing it | *[0057]* |
| repair of detected positions from local spacing, never assuming a body count | *[0040]–[0044]* |
| refusal to interpolate past the ends of a run or to invent a landmark | *[0044]* |
| registration at a fixed working resolution, and why it is required | *[0073]* |
| prediction set, anatomical-region fallback, calibration partitioned by subject | *[0077]–[0079]* |
| transition-role output *(implemented, measured, did not help — disclosed as a fallback)* | *[0064]* |

---

## Not to be claimed

- **Trained weights and the training corpus.** *Recentive* holds that curating training data earns nothing
  at §101. Both are better held as trade secret, which the deployment already supports.
- **Any accuracy figure.** Support, never a limitation.
- **A latency bound.** Not measured. See [0087].
