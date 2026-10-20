# SPECIFICATION

**Draft for patent counsel. This is the technical disclosure intended to be filed as the specification of a
provisional application under 35 U.S.C. §111(b). It is written to enable the claims in `CLAIMS.md`. Counsel
should reformat to USPTO conventions and revise the language; the engineering content is complete as written.**

---

## TITLE OF THE INVENTION

**Determining Vertebral Level from Limited-Field Projection Images by Linking Overlapping Exposures into a
Patient-Specific Chain, and Commanding Further Acquisition Therefrom**

*(Alternative titles for counsel: "Registration-Free Vertebral Level Identification and Imaging-Device
Control"; "Chain-Constrained Vertebral Naming from Successive Radiographic Exposures".)*

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

None.

---

## FIELD

[0001] The present disclosure relates to medical imaging, and more particularly to determining which vertebra
of a subject's vertebral column appears in a projection image acquired by a radiographic or fluoroscopic
imaging device, and to controlling the subsequent operation of that imaging device based upon that
determination.

---

## BACKGROUND

[0002] During a surgical procedure on the vertebral column, the operator must know which vertebra is shown in
the intraoperative image. A mobile fluoroscopic imaging device with a nine-inch image intensifier presents a
field of view of approximately 140 millimetres at the plane of the spine, which contains between two and four
vertebral bodies and, ordinarily, no anatomical landmark — no sacrum, no rib-bearing transition, no skull
base.

[0003] Adjacent vertebrae closely resemble one another. The information that distinguishes one vertebra from
its neighbour is therefore not contained in the appearance of the vertebra itself but in its **position within
a sequence whose end is known**. A limited field of view does not contain that information. This is a
structural property of the acquisition, not a deficiency of any particular image-analysis technique, and it
cannot be remedied by improving the analysis of a single image.

[0004] Known automated systems do not derive the answer from the intraoperative images. They **import** it.
Such systems register a previously acquired three-dimensional volumetric study — a computed-tomography or
magnetic-resonance volume in which a human operator has already assigned numbers to the vertebrae — onto the
live projection image, and transfer the numbering across the registration. Three consequences follow. First,
the technique is unavailable when no preoperative volumetric study exists, which is a large fraction of cases.
Second, an error in the preoperative numbering is transferred onto the intraoperative image faithfully and
with full apparent confidence, so the failure mode is silent. Third, the subject's volumetric study must be
transported to, and processed by, the registration system, which imposes a data-handling and network
dependency in the operating theatre.

[0005] Counting downward from a visible landmark is likewise unavailable, because a limited field ordinarily
contains no landmark; and where a landmark is visible in a separate exposure, nothing in the prior art
establishes that the vertebrae in the two exposures are consecutive members of one run.

[0006] Further, a portion of the population carries a **supernumerary or transitional segment** — a sixth
lumbar vertebra, or a thirteenth rib-bearing level, or a segment partially assimilated to the sacrum. In such
a subject, counting from a landmark yields a different answer depending on which convention the counter
applies, and a classifier trained on the general population has seen too few such subjects to name the
variant. Known systems do not address this population, which is precisely the population in which level
errors occur.

[0007] The practical consequence of the foregoing is measurable. At one quaternary referral centre, 179
preoperative percutaneous gold-fiducial marker placements were performed over 38 months — 176 of them in the
thoracic spine — at a mean procedure time of 52 minutes and a mean radiation dose of 183 milligray each,
solely to place a physical mark that would allow the operating surgeon to identify a level. Each such
placement is a separately scheduled invasive procedure, undertaken because the level was judged
undeterminable by intraoperative imaging alone.

[0008] There is accordingly a need for a technique that determines vertebral level from intraoperative
projection images alone; that requires no preoperative volumetric study, no optical or electromagnetic
tracking device, no calibration phantom and no implanted or applied fiducial; that indicates when it cannot
determine the level rather than answering wrongly; that, when it cannot, **directs the acquisition of the
particular further image that would resolve the question**; and that accommodates a supernumerary segment.

---

## SUMMARY

[0009] In one aspect, a sequence of projection images is acquired along the subject's vertebral column such
that each image overlaps the preceding image by a predetermined number of vertebral bodies. Successive images
are **linked on the vertebrae they share**, the shared vertebrae being determined from image content in the
region of overlap rather than from any external measurement of the position of the imaging device. The
resulting linked structure — referred to herein as a **chain** — is specific to the subject and supplies the
two facts absent from any single limited field: that its vertebrae are consecutive members of one run, and
where that run terminates.

[0010] In a further aspect, a later-acquired limited-field image is **registered onto the chain** by image
content, and each vertebra visible in that later image is assigned the identity of the chain member onto which
it registers. The later image therefore obtains an identity that its own pixels do not contain.

[0011] In a further aspect, a confidence value is computed at run time, without reference to any ground truth,
from two independent quantities: the lowest per-vertebra probability in the assigned naming, and a **chain
margin** measuring, for the weakest link, how much better the accepted registration of that link is than the
best registration displaced by more than half a vertebral spacing. When the confidence falls below a
threshold, the system **computes the distance and direction through which the imaging device must be moved**
in order to acquire a further image that would resolve the ambiguity, and emits that displacement both as a
control signal for a motorised positioner and as an instruction to a human operator. The displacement is
expressed in units of length and is derived from the subject's own vertebral spacing as observed in the image
in hand, so that no calibration metadata, phantom or tracker is required.

[0012] In a further aspect, candidate namings of the chain are scored against a plurality of **alternative
alphabets**, each alphabet being a different admissible ordered sequence of level identities, at least one of
which contains a supernumerary segment. A naming must be a contiguous run within one alphabet, and a declared
landmark pins one end of the run. The alphabet achieving the best score is output together with its margin
over the best ordinary alphabet. A supernumerary segment is thereby represented as **a different alphabet
rather than as an additional and vanishingly rare class**.

[0013] In a further aspect, upon confirmation of a level, a **persistent digital marker** is placed at the
coordinates of that vertebra in the image, and is carried forward into each subsequently acquired image by
registering that image onto the same chain and re-projecting the marker. The marker is retained when a
subsequent image is declined. The marker thereby performs the function of the physical fiducial of [0007]
without a separate invasive procedure.

[0014] In a further aspect, all of the foregoing computation is performed by a computing unit at the imaging
device, such that no image of the subject is transmitted outside the room in which the imaging device is
situated, and no previously acquired volumetric study is transported or processed.

---

## BRIEF DESCRIPTION OF THE DRAWINGS

[0015] FIG. 1 is a block diagram of an imaging system according to an embodiment.

[0016] FIG. 2 illustrates the acquisition geometry, showing successive projection images acquired along the
vertebral column with a region of overlap between adjacent images.

[0017] FIG. 3 is a flowchart of a method according to an embodiment.

[0018] FIG. 4 illustrates the linking of two successive projection images on the vertebral bodies they share.

[0019] FIG. 5 illustrates the chain data structure, in which each node corresponds to one vertebra and
aggregates the observations of that vertebra across the images in which it appears.

[0020] FIG. 6 illustrates the plurality of alternative alphabets and the scoring of a candidate naming
against them.

[0021] FIG. 7 is a flowchart of the confidence computation and the resulting commanded displacement.

[0022] FIG. 8 illustrates registration of a later-acquired limited-field image onto the chain.

[0023] FIG. 9 illustrates placement of a persistent digital marker and its propagation across subsequent
images.

[0024] FIG. 10 illustrates output of a prediction set and of a region-level fallback in place of a single
identity.

[0025] FIG. 11 illustrates repair of detected vertebra positions using the locally observed spacing.

[0025a] FIG. 12 illustrates determination of the direction of the vertebral column in the image from the
located landmark, and the transformation of a commanded displacement into the imaging device's axes.

[0025b] FIG. 13 illustrates the displacement commanded toward an ambiguous link, as distinct from a
displacement continuing the chain.

---

## DETAILED DESCRIPTION

### I. System (FIG. 1)

[0026] Referring to FIG. 1, an imaging system **100** comprises an imaging device **102** having a radiation
source **104** and a detector **106** carried on a positioner **108**. The positioner **108** may be a mobile
C-arm displaced manually by an operator, a motorised C-arm, a robotic gantry, or a fixed fluoroscopy
installation with a movable table; where the positioner is motorised it is operated by a positioner controller
**110**. The imaging device **102** is arranged to acquire projection images of a region of a subject **112**
containing a portion of a vertebral column **114**.

[0027] A computing unit **120**, comprising a processor **122** and a memory **124**, is situated at the
imaging device **102** or is attached thereto as an embedded module. A display **126** and an operator
interface **128** are coupled to the computing unit **120**.

[0028] The memory **124** holds instructions implementing: a detection module **130**, which determines the
image coordinates of individual vertebral bodies within a projection image; a naming module **132**, which
produces for each detected vertebral body a probability distribution over a set of candidate level identities
and further produces a feature vector characterising that body; a linking module **134**, which determines
which vertebral bodies are shared between two projection images; a chain store **136**; a decode module
**138**; a confidence module **140**; a displacement module **142**; and a marker module **144**.

[0029] In an embodiment the computing unit **120** has no network interface enabled during use, or has a
network interface **150** that is disabled for image data, such that no projection image of the subject
**112** leaves the room containing the imaging device **102**. The computation requires no previously acquired
volumetric study of the subject, no optical or electromagnetic tracking device monitoring the position of the
imaging device, no calibration phantom, and no fiducial marker applied to or implanted in the subject.

[0030] The naming module **132** is a trained model. Any model that emits, for each detected vertebral body, a
distribution over candidate level identities together with a feature vector is suitable; the particular
architecture is not material to the operation described herein and the described method does not depend upon
it. In one implementation the naming module comprises a convolutional feature extractor operating on an
image region cropped about each detected body at a fixed physical scale, together with a sequence model that
pools the feature vectors of several consecutive bodies before emitting the distributions, whereby the
distribution emitted for a given body is informed by the appearance of its neighbours. In a further
implementation the crop supplied to the feature extractor is accompanied by an auxiliary channel indicating
which body within the crop is the body to be named, so that a crop containing several bodies is unambiguous.

### II. Acquisition geometry (FIG. 2)

[0031] Referring to FIG. 2, the imaging device **102** acquires a sequence of projection images **200**
comprising a first projection image **202**, a second projection image **204** and a third projection image
**206**, at successive positions along the vertebral column **114**. Each image spans a field **210** of
extent *S* at the plane of the spine. Each image overlaps its predecessor in a region of overlap **208**
containing a number *O* of vertebral bodies **216**.

[0032] In one implementation the imaging device is a mobile C-arm with a nine-inch image intensifier. The
useful field at the plane of the spine is derived as follows: an entrance field of approximately 230
millimetres, of which approximately ninety per cent is usable after vignetting and collimation, reduced by a
geometric magnification of approximately 1.5 between the spine and the detector, yields approximately
230 × 0.9 ÷ 1.5 ≈ 140 millimetres at the spine. A twelve-inch intensifier yields approximately 190
millimetres and a 30-centimetre flat-panel detector approximately 200 millimetres by the same derivation, and
a collimated field may be as small as 100 millimetres. The method operates at any of these; the field extent
enters the computation only as the quantity *S*.

[0033] The sequence is begun at a declared anatomical landmark **214** — in one implementation the sacral
promontory, the first sacral body being the caudal terminus of the presacral run; in another the second
cervical vertebra, being the cranial terminus. The operator declares which landmark was used. The declaration
pins one end of the run and is the only external information the method consumes. It is a statement of where
the operator began, not a measurement.

[0034] The commanded step between successive positions is

&nbsp;&nbsp;&nbsp;&nbsp;**step = S − (O × p)**

where *p* is the vertebral spacing expressed in the same units as *S*. The overlap *O* is a parameter of the
acquisition protocol.

[0035] The choice of *O* is not a matter of indifference and the relationship is **not monotone**. Measured
across 801 subjects at a 140-millimetre field, naming accuracy on frames containing two vertebral bodies was
86.6 per cent at *O* = 0.5, 93.6 per cent at *O* = 1, 95.1 per cent at *O* = 2, 95.2 per cent at *O* = 3 and
93.2 per cent at *O* = 4, while the proportion of subjects for whom the chain was completed fell from 94.2 per
cent to 80.4 per cent over the same range. Beyond two bodies of overlap, each further image adds another link
that may be joined incorrectly faster than it adds evidence. Two bodies is accordingly the operating point in
the preferred embodiment, and the protocol parameter is claimed as "a predetermined number of vertebral
bodies" so that any operating point is within scope.

[0036] The number of exposures required is correspondingly small: 2.5 exposures per sweep at *O* = 0.5 with
the chain completed on 86.7 per cent of subjects; 2.6 at *O* = 1 with 95.0 per cent; 3.0 at *O* = 2 with 96.7
per cent; and 6.9 at *O* = 4 with 80.0 per cent. Determining the level in approximately three exposures,
without a preoperative study, is a reduction in both radiation dose and procedure time relative to the
practice the technique displaces.

### III. Recovery of physical scale from the subject's own anatomy

[0037] Many intraoperative images carry no reliable calibration metadata relating image pixels to physical
distance, and the geometric magnification of a mobile C-arm varies with the position of the subject between
source and detector. The method therefore recovers the scale from the anatomy visible in the image.

[0038] The detection module **130** yields, for each vertebral body in the image, a bounding region; the
centre of each region is taken. The distances between the centres of vertically adjacent bodies are formed,
and their median is taken as the **observed spacing** *p* in pixels. The observed spacing is divided by an
anatomical spacing constant for the region of the column concerned to yield a pixel-per-millimetre ratio. In
one implementation the anatomical spacing constants are 19 millimetres in the cervical region, 27 millimetres
in the thoracic region and 34 millimetres in the lumbar and sacral regions, these being population medians of
centre-to-centre vertebral spacing. Where the image does carry a trustworthy pixel-spacing value, that value
is used in preference and the anatomical path is not taken.

[0039] The consequence is that every quantity the method emits in units of length — in particular the
commanded displacement of §VII — is derived from the subject's own vertebrae as seen in the image in hand. No
phantom, no tracker, no grid, and no metadata are required. Because the ratio is a median over several
independent spacings, a single mis-detected body perturbs it little.

### IV. Detection and repair of vertebra positions (FIG. 11)

[0040] The detection module **130** emits a bounding region per vertebral body. Two systematic errors are
correctable from the geometry of the column without reference to the model that produced them, because the
bodies in one image lie in a line at nearly constant spacing, which is a constraint the detector — scoring
each candidate region independently — does not use.

[0041] Referring to FIG. 11, the detected regions **1102** are sorted along the axis of the column and the
differences between successive centres are formed; the median of those differences is the local spacing
**1104**. Where two regions are separated by less than a first fraction of the local spacing (0.45 in one
implementation) they are treated as **one vertebra detected twice** and are replaced by the union of the two
regions, shown at **1106**. Where two regions are separated by more than a second fraction (1.55 in one
implementation) they are treated as having **a vertebra missed between them**, and one or more regions are
interpolated between them at positions determined by the local spacing and with the median observed dimensions
of the regions present, shown at **1108**.

[0042] Two refusals are essential and are part of the invention rather than incidental to it.

[0043] **First, the number of vertebrae is never assumed.** The local spacing is measured from the regions
actually present in this image, so a column carrying six lumbar vertebrae is repaired by the same rule as one
carrying five. A technique that instead decodes a fixed number of regions — one per level, on the premise that
the human spine has five lumbar vertebrae — will, in a subject with a supernumerary segment, drop a vertebra
or place the last region on the sacrum, *by construction*, and will do so in exactly the population in which
level determination matters most.

[0044] **Second, nothing is interpolated past the ends of the run, and not more than a small number (two in
one implementation) of bodies is interpolated into any one gap.** Beyond that, the spacing estimate is being
extrapolated further than it will carry, and a run of invented positions is worse than an acknowledged
absence. In particular, a landmark absent at the end of the run is never invented, since the landmark is the
constraint upon which the whole determination rests.

### V. Linking two images on the vertebrae they share (FIG. 4)

[0045] Referring to FIG. 4, a lower image **402** and an upper image **404** overlap in a band **406**. The
linking module **134** determines the relative displacement of the two images, and thence which vertebral
bodies they share, as follows.

#### V.a Determining the displacement

[0046] A displacement (*dy*, *dx*) is sought such that content of the upper image at row *r* coincides with
content of the lower image at row *r* + *dy*. For each candidate displacement, the overlapping portions are
extracted and a normalised measure of similarity is computed between them; in one implementation this is the
normalised cross-correlation of the overlapping pixel arrays, but any measure of similarity between
overlapping image content may be substituted without altering the method.

[0047] The search window is **asymmetric about the commanded step**, and the asymmetry is load-bearing:

- The far bound extends approximately **0.6 of a vertebral spacing beyond the commanded step**, accommodating
  an operator who moved further than instructed.
- The near bound is a step of approximately **half a vertebral spacing**, accommodating the final image of a
  sweep, which is shortened where the anatomy ends.

[0048] The lower bound of the search window is what defeats **periodic aliasing**. A column of vertebrae is
approximately periodic in appearance at the vertebral spacing. A similarity search permitted to range freely
will, at an overlap of one body, find a strong spurious peak at a displacement differing from the true one by
exactly one vertebral spacing, and the resulting chain will be wrong by one at every position above the
faulty link, with no local indication that anything has gone wrong. Confining the search to displacements
consistent with the commanded step removes the competing peak from the window. A lateral search of
approximately ±0.3 of a vertebral spacing is also performed, accommodating lateral drift of the positioner.

[0049] Candidate displacements at which the overlapping band is shorter than approximately 0.4 of a vertebral
spacing, or narrower than a small number of columns, are rejected as providing insufficient support.

[0050] The search returns the displacement of greatest similarity, that similarity value, and a **margin**:
the similarity at the accepted displacement less the greatest similarity attained at any displacement
differing from it by more than half a vertebral spacing. The margin is a direct measurement of whether this
link can distinguish its own offset from an offset of one vertebra, and it is available at run time without
any reference to truth. Its use is described in §VII.

#### V.b Determining which bodies are shared

[0051] The accepted displacement is applied to the centres of the bodies detected in the upper image. A
displaced upper centre falling within a tolerance of a lower centre identifies that pair as the same vertebra.
The tolerance is **anisotropic** — in one implementation the distance measure weights lateral displacement at
half the weight of axial displacement, and the tolerance is approximately 0.4 of the observed vertebral
spacing — because the axial direction is the direction in which an error changes the identity assigned, while
lateral displacement of a body's centre carries no identity information and should not be permitted to break a
correct pairing.

[0052] The set of pairs so obtained is then constrained to **the only arrangement a sweep can produce**: the
lowest *m* bodies of the upper image correspond to the highest *m* bodies of the lower image, for some *m*.

[0053] The manner of choosing *m* is material. A strict rule takes the largest *m* for which *every* implied
pair is supported by the displacement. That rule is correct when the detected regions are exact and is
**wrong when they are the output of a detector**: a single missed or spurious region inside the shared block
fails the test, *m* collapses, and every genuinely shared vertebra is entered into the chain as a new and
distinct vertebra. In measurements on real radiographs, the detector missed only 2.2 per cent of bodies while
17.9 per cent of bodies were entered twice — the duplication being this rule failing, not the detector failing
to see the bone.

[0054] A **robust rule** is therefore used. Each candidate *m* is scored by the number of its implied pairs
that the displacement supports, less a fractional penalty (one half in one implementation) for each pair it
does not support; candidate blocks in which fewer than a majority fraction (0.6 in one implementation) of
pairs are supported are rejected outright so that a long unsupported block cannot prevail on size alone; and
the whole block at the winning *m* is accepted. A single erroneous region then costs one mispaired body
instead of the entire link.

[0055] In a further implementation the feature vectors emitted by the naming module **132** for the paired
bodies are compared, and their agreement is recorded as an independent check upon the pairing obtained from
image displacement; and the value of *m* that the feature vectors alone would have selected is recorded
alongside, so that disagreement between the two routes is visible rather than silent.

### VI. The chain (FIG. 5) and its naming (FIG. 6)

#### VI.a Structure

[0056] Referring to FIG. 5, the chain **500** comprises an ordered sequence of nodes **502**, each node
corresponding to one physical vertebra of the subject. A node holds the list of (image, region) observations
of that vertebra — a vertebra appearing in two overlapping images has two observations **504**. Construction
proceeds from the image containing the landmark: the bodies of the first image become the initial nodes; for
each further image, bodies identified as shared are appended as further observations of existing nodes, and
bodies not so identified are inserted as new nodes at the appropriate end of the chain.

[0057] For each node, the probability distributions emitted for its several observations are pooled — by
arithmetic mean in one implementation — and its feature vectors likewise. **Pooling across views is a benefit
of the chain that no single image affords**: a vertebra seen at the edge of one field, foreshortened or
obscured by the collimator, is also seen near the centre of the adjacent field, and the chain knows that these
are the same bone.

#### VI.b Decoding under the alphabet constraint

[0058] Referring to FIG. 6, the chain is named as a whole, not vertebra by vertebra. Two constraints apply
jointly:

1. **Contiguity.** The names assigned to the chain must be a contiguous run of one admissible ordered sequence
   of level identities. Nodes are consecutive vertebrae by construction, so their names must be consecutive.
2. **The landmark pins one end.** Where the declared landmark is caudal, the last node bears the landmark
   identity; where cranial, the first node does.

[0059] A plurality of **alternative alphabets** **602**, **604**, **606**, **608** is constructed. Each
alphabet is a complete admissible ordering of level identities for a vertebral column:

- an **ordinary** alphabet **602**: C1…C7, T1…T12, L1…L5, sacrum;
- an alphabet **604** including a thirteenth rib-bearing level: …T12, T13, L1…;
- an alphabet **606** including a sixth lumbar vertebra: …L5, L6, sacrum;
- an alphabet **608** including both.

Further alphabets corresponding to further anatomical variants may be added without retraining the naming
module, because an alphabet is a constraint applied at decoding and not a class the model must learn.

[0060] For each alphabet, and for each starting offset within that alphabet that satisfies the landmark
constraint, the implied naming of the chain is scored — in one implementation by the mean over nodes of the
logarithm of the probability that the naming module assigned to the name so implied. The best-scoring naming
within each alphabet is retained, and the best over all alphabets is emitted as the naming of the chain.

[0061] The **identity of the winning alphabet is the variant call**, and its score less the best score
attainable under the ordinary alphabet is the **variant margin**, being the confidence in that call expressed
in the same units as the score. Critically, all four alphabets draw their symbols from **one output space** of
the naming module; adding an alphabet adds no class and requires no retraining. A supernumerary segment is
thus represented as **a different alphabet, never as a rare class** — which matters because such segments are
too infrequent in any training corpus to be learned as classes, yet are exactly the subjects in which level
errors occur.

[0062] **A single limited-field image cannot make this determination, and a chain reaching a landmark can.**
An alphabet differs from another only in a segment that may lie outside any one field; only a run pinned at a
landmark exposes the difference.

[0063] The magnitude of the decoding step is measurable because the naming module is held fixed. Taking the
most probable identity independently for each node named 85.8 per cent of vertebrae correctly; decoding the
identical distributions as one sequence against the four alphabets named 95.5 per cent — 9.7 percentage points
attributable to the decoding constraint alone.

[0064] In a further implementation a **transition-role output** is additionally provided, emitting for each
body the probability that it is the last thoracic body, the first lumbar body, or the last presacral body;
the agreement of a candidate naming with that output is added to the score, and only those bodies to which the
candidate assigns a role are scored, so that a run containing no junction is unaffected. *This variation was
implemented and measured and did not improve the result, the competing alphabets already placing the junctions
at different positions. It is disclosed for completeness and as a fallback position, not as a preferred
embodiment.*

[0065] In a further implementation the delimitation of a transitional segment follows a convention based upon
**the presence of an intervertebral disc** rather than upon the extent of osseous fusion, the disc being the
feature that is decidable on a projection image.

### VII. Confidence and the commanded displacement (FIG. 7)

[0066] Referring to FIG. 7, the confidence module **140** computes at **702** a confidence in the naming of a
given image, from two quantities that fail independently:

&nbsp;&nbsp;&nbsp;&nbsp;**confidence = *a* × clip(*b* / τ, 0, 1)**

where

- ***a*** is the **lowest** probability assigned by the naming module to any of the identities assigned to the
  vertebrae of that image (**704**). This term detects ambiguity of *appearance*. The minimum, not the mean,
  is taken, because a single uncertain vertebra makes the whole assignment doubtful.
- ***b*** is the **chain margin** (**706**): the minimum over the links of the chain of the margin defined in
  [0050]. This term detects ambiguity of *geometry*. Its significance is that a link unable to distinguish its
  own displacement from a displacement of one vertebra places every identity above it wrong, and the margin
  says so **before any identity is emitted**, without reference to truth.
- τ is a scaling constant (0.2 in one implementation) above which the geometric term is treated as saturated.

[0067] Both quantities are available at the time of acquisition and neither requires knowledge of the correct
answer. The product is low if either is low, which is correct: an assignment is trustworthy only if both the
appearance and the geometry are unambiguous.

[0068] Where the confidence exceeds a threshold, the naming is emitted at **708**. Where it does not, the
displacement module **142** computes at **710** a **commanded displacement** — a signed distance in units of
length together with a direction along the axis of the column — and the system emits it at **712** in two
forms derived from one computation:

- a **control value** transmitted to the positioner controller **110**, causing the positioner **108** to
  displace the imaging device **102** by that distance; and
- an **instruction rendered on the display 126** in units of length and a direction ("move 38 mm caudal"),
  for an operator displacing the device manually.

The two forms are the same number. The installed base of imaging devices is overwhelmingly manually
positioned, so an embodiment that addressed only motorised positioners would be of limited use; the emitted
displacement is therefore itself an output of the system, whether or not anything acts upon it.

[0069] **The remedy commanded depends upon which term is low**, and this is the substance of the closed loop:

- Where ***a*** is low — the appearance is ambiguous — the commanded displacement is a **full step toward the
  declared landmark**: step = *S* − (*O* × *p*), converted to units of length by the ratio of §III. This
  extends the chain toward the landmark, adding the constraint that the appearance alone could not supply.
- Where ***b*** is low — the geometry is ambiguous — the commanded displacement is a **shorter step, so as to
  increase the overlap on the weak link**: step = *S* − (*O*′ × *p*) with *O*′ > *O*. This supplies the
  additional shared anatomy that the ambiguous link lacked.

[0070] **A measurement constrains this aspect and is disclosed so that the distinction is understood.**
Simply re-acquiring the same view does **not** help: across 4,792 query images, re-acquiring an image whose
confidence was low and re-naming the replacement scored no better than the image it replaced — 95.7 per cent
under decline-and-re-acquire against 95.3 per cent under answering every image, a difference within the
measurement interval. What does help is **overlap between linking images**: at one body of overlap the
proportion of images answerable at 99 per cent accuracy is 42 per cent, and at two bodies it is 82 per cent.

[0071] Accordingly the further image whose acquisition is commanded is **a further linking image that extends
the chain or increases its overlap**, and is not a re-acquisition of the image that was declined. This is both
the honest statement of the mechanism and the stronger one, being the version the measurement supports.

#### VII.a The commanded displacement is directed at the ambiguous link

[0071a] Where the ambiguous quantity is the geometry, the displacement commanded is **not** merely a shorter
step. A shorter step adds an image at the end of the chain, and a link that is ambiguous several images back
is not overlapped by anything acquired there. The system therefore computes the displacement from the
present position of the imaging device **to the midpoint between the two images forming the ambiguous link**,
those positions being known from the accepted displacements of the links themselves. The commanded distance
is thus derived from a measurement of where the imaging device actually went, not from the protocol's
expectation of where it should have gone.

[0071b] The escalation is bounded. Increasing the overlap in a field spanning four vertebral bodies reaches a
commanded step of a few millimetres, which is a re-acquisition of substantially the same image — the remedy
[0070] shows does not work. The overlap is therefore bounded such that at least one further vertebra enters
the field, and where the ambiguity cannot be resolved within that bound the system emits a refusal
identifying the link, rather than reissuing a remedy that has been measured not to move the quantity it was
aimed at.

#### VII.b The displacement is measured rather than accumulated

[0071c] The distance back to a previously imaged position — in particular the return to the operative field
in the embodiment of [0011] — is computed from the accepted displacements of the links, and not from the sum
of the displacements previously commanded. An operator does not execute a commanded displacement exactly, and
over four or five exposures that error accumulates; the links are a measurement of where the device went. On
a synthetic subject, after four displacements executed with ten per cent error, the position of every image
was recovered from image content alone to within 1.2 millimetres, the system being given no information about
the operator's execution.

#### VII.c Selecting the landmark and bounding the run

[0071d] The vertebral column has two termini usable as landmarks, and the number of exposures required
depends on which is chosen. For an operation at a cervical level the cranial terminus is two or three
vertebrae distant and the sacrum is the length of a subject; for a lower lumbar level the converse holds. The
system therefore computes, from the level to be operated upon and the field extent, the distance to each
landmark and the exposures each would require, and selects the nearer — reducing a run of fifteen exposures to
one or two. The mid-thoracic region is that in which both landmarks are distant, in which no single field
contains a landmark, and in which the measured improvement is largest; it is the region for which the method
is principally intended, and no claim should be drafted so as to confine the disclosure to the lumbar spine.

#### VII.d Determining the direction of the vertebral column in the image

[0071e] The foregoing all presuppose knowledge of which direction in the image is cranial. A projection image
from a mobile imaging device carries no such guarantee: the image intensifier may be rotated to any angle and
the detector readout may be inverted. Commanding a displacement in the belief that cranial is one way when it
is the other does not degrade the result — **the successive images do not overlap at all**, no link can be
formed, and no chain exists.

[0071f] The direction is therefore determined, as follows:

1. the landmark is located by the distribution the naming module emits **over every detected body in the
   field**, and not by the position of any body in the image, since that position is precisely what is
   unknown;
2. an axis is fitted to the centres of the detected bodies, which determines the **line** of the column but
   not which of its two directions is cranial, a line being an equally good fit either way;
3. the located landmark determines the **sign**, the sacrum being the caudal terminus of the presacral run
   and the second cervical vertebra the cranial one;
4. each image is transformed into that direction before the linking of §V is performed, so that all
   subsequent processing operates in a single convention;
5. the commanded displacement is transformed back into the imaging device's own axes for a positioner, while
   the instruction given to a human operator is expressed anatomically ("38 mm cranial") and requires no
   transformation, being independent of how the image is presented.

[0071g] In an embodiment in which the first image contains no landmark, the line is determined as above and
the cranial direction is provisionally taken to be the one conventionally presented. That provisional
assignment is not relied upon: were it incorrect, the first commanded displacement moves the device away from
the region of overlap and the linking step returns no usable displacement at all — a detectable condition,
upon which the assigned direction is inverted and the linking repeated.

### VIII. Naming a later limited-field image (FIG. 8)

[0072] Referring to FIG. 8, a later image **802** is acquired — at an arbitrary time during the procedure,
after the imaging device has been moved, and without the chain being rebuilt. The chain is rendered as a
composite image **804** by placing each constituent image at its accepted displacement. The later image
**802** is then registered onto the composite by the similarity measure, over a range of scales (0.9 to 1.1 in
one implementation, in steps of 0.05) accommodating change in geometric magnification when the imaging device
has been moved toward or away from the subject.

[0073] The registration is performed at a **fixed working resolution at which a vertebra subtends a
predetermined number of pixels**, both images being reduced to that resolution before the search and the
located position being mapped back afterwards. The cost of a template search is the product of the search area
and the template area, so the cost at full radiographic resolution exceeds the cost at working resolution by
approximately three orders of magnitude. Locating a body requires a small fraction of the resolution that
naming one requires, so nothing upon which the located position depends is lost. This is a requirement of
practical operation, not an optimisation.

[0074] The centres of the bodies detected in the later image are carried through the accepted registration
and each is assigned to the nearest chain node within a tolerance of the observed spacing; each body then
takes the identity of that node. Where the assignments so obtained are consecutive, they are accepted; where
they are not, the assignment is flagged as inconsistent, and in one implementation the first confidently
assigned body sets the offset and the remainder follow from contiguity.

[0075] In a further implementation, or where the registration by image content does not attain a minimum
similarity, an alternative route is used: the position along the chain is chosen that maximises the mean
agreement between the feature vectors of the later image's bodies and those of the corresponding chain nodes,
and the **margin** of that position over the next best is computed. Where the margin is below a threshold the
system declines rather than emitting an identity.

[0076] The improvement this affords is the central measured result. On 801 subjects, images containing two
vertebral bodies were named correctly 69.6 per cent of the time from the image alone and **95.1 per cent** of
the time when registered onto the chain; three bodies, 85.9 against 95.0 per cent; four bodies, 91.2 against
95.7 per cent. In the thoracic region, where no landmark is within reach of any single field, the effect is
larger still: on 76 whole-spine subjects swept from the second cervical vertebra, images containing three
bodies were named correctly 31.1 per cent of the time from the image alone and **99.3 per cent** of the time
when registered onto the chain. On the nine subjects in that set carrying transitional anatomy, every
registered image at every length was named correctly.

### IX. Prediction sets and region fallback (FIG. 10)

[0077] Referring to FIG. 10, in place of a single identity the system may emit a **set** of identities
guaranteed, at a calibrated confidence level, to contain the correct one. A threshold *q* is obtained from a
held-out calibration collection as an appropriate empirical quantile of the non-conformity scores — one minus
the probability assigned to the correct identity — and the emitted set for a new vertebra is those identities
whose non-conformity does not exceed *q*.

[0078] Where the set is a singleton **1002**, a single identity is emitted. Where it is not, the members are
compared against a hierarchy of anatomical regions **1004** — cervical, thoracic, lumbar, sacral. Where every
member of the set falls within one region, that **region** is emitted **1006** — "this is a lumbar vertebra,
though not which" — which is actionable, whereas a bare refusal is not. Where the members straddle regions,
the system declines **1008**, and in that event the commanded displacement of §VII is computed.

[0079] The calibration collection is partitioned **by subject and never by vertebra**, since vertebrae of one
subject are not exchangeable with one another and a partition by vertebra would render the guarantee invalid
while appearing to hold.

### X. The persistent digital marker (FIG. 9)

[0080] Referring to FIG. 9, upon a level being confirmed — by the confidence of §VII exceeding its threshold,
or by an operator's confirmation entered at the interface **128** — the marker module **144** places a
**digital marker 902** at the image coordinates of the confirmed vertebra. The marker record comprises the
image coordinates, the assigned identity, the confidence at the time of placement, and the state of any
declination.

[0081] Each subsequently acquired image **904** is registered onto the chain by the procedure of §VIII, and
the marker is **re-projected** into that image at **906** through the accepted registration, so that the mark
appears upon the correct vertebra although the imaging device has been moved, the magnification has changed
and the anatomy is presented differently.

[0082] **The re-projection is what makes this a fiducial rather than a caption**, and it re-uses the
registration machinery already described rather than requiring any further apparatus. Every placement, every
propagation and every loss of registration is recorded.

[0083] The marker is **retained when a subsequent image is declined** — that is, the marker persists at the
level last confidently determined, and the system indicates that the current image could not be registered,
rather than removing the mark. A mark that disappears whenever confidence falls does not perform the function
of a fiducial.

[0083a] **A position is asserted only where the registration carrying it can exclude a displacement of one
vertebra.** The vertebral column is approximately periodic at the vertebral spacing, so a later image
correlates nearly as well at a displacement of one body as at the correct displacement, and the peak
similarity does not distinguish the two. The registration of §VIII therefore also yields a **margin** — the
peak similarity less the greatest similarity attainable at any displacement differing by more than half a
vertebral spacing — and where that margin is below a threshold the marker is **retained, indicated as
unsupported by the present image, and reported together with its last supported position**, rather than being
placed. In testing, a marker placed at one level projected onto the adjacent level in two later images of
five, upon the adjacent body's centre to within one pixel, at peak similarities of 0.78 against 0.83 for the
correct placements. With the margin condition applied, every asserted position fell upon the marked vertebra
and the remainder were withheld. A marker silently placed upon the adjacent vertebra is the precise failure
this disclosure exists to prevent, and the margin condition is accordingly a part of the invention and not an
optimisation of it.

[0083b] Where the marked vertebra lies outside the current field, the projection is nevertheless computed and
the **distance and direction to it are emitted in units of length** — a further commanded displacement, and
the answer an operator searching for a marked level requires.

[0084] The marker so placed performs the function of the physical gold fiducial described at [0007] — marking
a level so that the surgeon may find it — without a separately scheduled invasive procedure, without
additional radiation exposure, and without an implanted foreign body. The comparison is to a concretely
measured practice: 179 placements over 38 months at a mean of 52 minutes and 183 milligray each.

### XI. Operation without the imaging leaving the room

[0085] All computation described herein is performed by the computing unit **120** at the imaging device. No
image of the subject is transmitted beyond the room, no volumetric study of the subject is transported or
processed, and no network link is required for the system to function.

[0086] This is a structural difference from registration-based techniques rather than a difference of degree:
a technique that registers a preoperative volume must have that volume present at the place of registration,
whereas the present technique consumes only images that the imaging device has just produced.

[0087] *Measured support, and its present limits.* On a datacentre graphics processor, naming one vertebra
required 2.29 milliseconds and detecting the vertebrae in one image 22.94 milliseconds; on eight processor
threads, 18.30 and 330.58 milliseconds respectively. **The linking, composition and registration stages have
not yet been separately timed, and any representation as to end-to-end latency should await that
measurement.**

### XII. Variations

[0088] The following variations are within the scope of the disclosure:

1. **Imaging device.** Mobile C-arm, motorised C-arm, robotic gantry, fixed fluoroscopy installation, or any
   device acquiring successive projection images at positions along the vertebral column. The technique is
   indifferent to the mechanism by which the device is displaced.
2. **Similarity measure.** Normalised cross-correlation, mutual information, phase correlation, a learned
   similarity, or feature-point correspondence — any measure of similarity between content in the region of
   overlap.
3. **Landmark.** The sacral promontory, the second cervical vertebra, the rib-bearing transition, an implanted
   device of known level, or any structure of declared identity within any image of the sequence.
4. **Direction.** Cranial to caudal or caudal to cranial; the sequence need not be monotone in direction
   provided each image overlaps some other image of the sequence.
5. **Region of the column.** Cervical, thoracic, lumbar or sacral, or any combination. The largest measured
   improvement is thoracic, which is also the region of greatest clinical difficulty; the disclosure is not to
   be read as confined to the lumbar spine.
6. **Anatomy.** Human or veterinary; the anatomical spacing constants and the alphabets are parameters.
7. **Alphabets.** Any number of admissible orderings, including orderings for assimilated or partially
   assimilated segments, for a subject with a surgically absent vertebra, and for a subject with previously
   instrumented levels.
8. **Naming module.** Any trained model emitting a distribution over identities and a feature vector per
   detected body.
9. **Confidence.** Any combination of an appearance term and a geometric-margin term; the product and the
   clipping are one convenient form.
10. **Commanded displacement.** Emitted as a control value, as an operator instruction, as an overlay upon the
    display indicating the target position, or as an audible or haptic indication.
11. **Marker.** Placed at one level or several; propagated into every subsequent image or only upon request;
    exported with the procedure record.
12. **Modality.** Radiographic or fluoroscopic projection images; also applicable, with the anatomical
    constants changed, to any imaging modality producing overlapping limited-field views of a serially
    repeating structure whose members must be individually identified.

### XIII. Advantages

[0089] The described technique: requires no preoperative volumetric study; requires no optical or
electromagnetic tracking device; requires no calibration phantom, grid or applied fiducial; recovers physical
scale from the subject's own anatomy; determines level from images the imaging device has just produced;
indicates when it cannot determine a level, from quantities available without knowledge of the correct answer;
commands the particular further acquisition that would resolve the question, in units of length, to a
positioner or to an operator; accommodates a supernumerary segment without adding a class to any trained
model; emits a calibrated set or an anatomical region where a single identity cannot be supported; places a
persistent digital mark in place of an invasive physical fiducial; and performs all of the foregoing without
any image of the subject leaving the room.

---

## NOTE ON THE STATE OF REDUCTION TO PRACTICE

*This note is for counsel and is not part of the disclosure to be filed.*

Implemented, exercised end to end, and unit-tested: the acquisition protocol and its overlap parameter; the
recovery of scale from anatomy; detection repair; linking with its asymmetric window, anisotropic tolerance
and robust block scoring; the chain and its margin; the alternative-alphabet decode; the two-term confidence;
the commanded displacement in both forms, including its direction at an ambiguous link and its bounding short
of a re-acquisition; the determination of the column's direction and the transformation of the displacement;
the selection of landmark and the bounding of the run; registration of a later image onto the chain; and the
marker with its propagation, its retention on refusal and its margin condition.

Measured on the render corpus (801 subjects): the naming results at §II, §VI and §VIII, and the overlap
relationship at [0035]–[0036].

Measured on a synthetic subject only, and stated as such throughout: the geometry recovery at [0071c] and the
marker results at [0083a]. The corresponding measurement on the render corpus is in progress.

**Not measured, and no representation should be made:** the latency of the linking, composition and
registration stages (§XI records the two networks that have been timed and states plainly that the remainder
have not); the behaviour of any part of this on real intraoperative fluoroscopy; and the transfer of the
geometric threshold, whose value is a property of image texture, from renders to film.

---

*End of specification.*
