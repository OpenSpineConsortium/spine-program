# Linking under a circular field and realistic physics

What was measured on 2026-09-20, including the things that did not work and the two results that had to
be withdrawn after being believed. The tool is `tools/link_probe.py`; the reason it exists is at the end.

## Read this first: detection is the binding constraint, and its threshold was miscalibrated

Every other number in this note is measured with the vertebrae GIVEN — the linker is handed boxes and
asked only which of them are the same bone across two frames. Same corpus, same protocol, same seed,
only the box source and the frame model changed:

| | walks reached | exact |
|---|---:|---:|
| clean film, annotation's boxes | 6,238 | **99.74 %** |
| clean film, the detector's boxes | 5,942 | 29.06 % |
| physics, annotation's boxes | 6,123 | 71.73 % |
| physics, the detector's boxes, conf 0.25 | 255 | 5.1 % |
| physics, the detector's boxes, conf 0.05 | **4,702** | **21.5 %** |
| clean film, the detector's boxes, conf 0.05 | 6,189 | 39.52 % |

**That last row was measured at one confidence threshold, 0.25, and the threshold was wrong.** Swept:

| detector confidence | physics: reached | exact | clean film: reached | exact |
|---:|---:|---:|---:|---:|
| 0.25 | 255 | 5.1 % | 5,942 | 29.06 % |
| 0.10 | 2,533 | 17.05 % | | |
| 0.05 | **4,702** | **21.5 %** | **6,189** | **39.52 %** |
| 0.02 | 6,025 | 10.36 % | | |

The detector was under-confident on physics frames, not blind. Dropping the threshold from 0.25 to 0.05
takes reach from 255 to 4,702 — eighteenfold — and exactness from 5.1 % to 21.5 %. At 0.02 reach is
nearly complete but false boxes halve the exactness again, so 0.05 is where it sits.

**And 0.25 is wrong on clean film too**, which matters beyond this note: 29.06 % at 0.25 against
39.52 % at 0.05, on the same spines. The 30.06 % the manuscript reports for detector boxes is measured
at a threshold that costs it about ten points.

So the honest statement is the middle one, not either extreme. Detection is still the binding
constraint — 21.5 % under physics and 39.5 % on clean film against 71.73 % and 99.74 % with the boxes
given — but it is a detector calibrated for a different image class, not a detector that cannot see.
Physics costs about 18 points of detection on top of whatever the detector costs anyway.

Two things that do NOT help, measured rather than assumed. Box repair is worth 0.8 points at this
threshold (21.5 % against 20.68 % with it off), and it was already on in every detector arm run here
because `--box-repair` defaults to 1. And the exposure lever, which was worth 4.6 points of LINKING,
costs detection: 20.84 % at 4× against 21.5 % at 1×, with reach falling from 4,702 to 3,124. A brighter
frame does not make the vertebrae easier to find.

The detector has still never seen a frame with a fluoroscopic photon budget, a scatter pedestal and a
generator pinned by a thick abdomen, and training it on those remains the substantial fix. It is
harder than it looks: the detector is a POSE model predicting four corners per vertebra, and the render
annotations carry boxes and centroids but no corners, so that training data does not currently exist in
usable form. The renderer is calibrated, so the frames can be made; the labels are the missing half.

## The walk, end to end

Exactness on 801 abdominopelvic spines, circular field, masked correlation, the annotation's boxes:

| step | exposures | clean film | physics |
|---|---:|---:|---:|
| 2.5 body (published) | 1.98 | 99.74 % | 71.73 % |
| 1.5 body | 2.41 | 99.76 % | 76.88 % |
| 0.5 body | 3.64 | 99.17 % | **88.43 %** |

The short step is worth 16.7 points under physics and costs clean film 0.6, at 1.8 times the exposures.
It is the only change measured here that moves the physics walk by more than five points.

Two things confirm it rather than flatter it. With the C-arm's move disturbed by 0.3 of a body it reads
89.77 %, slightly ABOVE the undisturbed figure, so the narrow search window a half-body step implies is
not the fragility it looked like. And with no anti-scatter grid at all — the worst condition in a mobile
fleet — it still reads 78.97 %, above the published step's 71.73 % with a good grid.

The second lever, a deliberate stored exposure instead of a live screening frame, is worth 4.6 points at
the published step (71.73 to 76.28) and 3.1 at a body and a half (76.88 to 80.02). It does not compose
with the first: the short step has already taken what both were reaching for.

### A third thing works, and the prediction about why it would not was wrong

`build_chain_global` measures every SKIP pair (i, i+2) as well as every consecutive pair and solves all
the measurements at once under a robust loss. It had never been reachable from `fiducial_walk`, which
has no `--solve` flag, so no published arm had used it.

The prediction written into `slurm/physics_global_walk.sh` was that it could do nothing at the published
step, because a skip link only exists where frames two apart still share anatomy, and at a 2.5-body step
on a 4.5-body field they are five bodies apart and share none. That reasoning was correct about the skip
links and wrong about the method:

| | pairwise | global |
|---|---:|---:|
| physics, 2.5-body step | 71.73 % | **77.19 %** |
| physics, 1.5-body step | 76.88 % | 75.51 % |

It gains 5.5 points exactly where it was predicted to be inert, and loses 1.4 where it was predicted to
help. The reason is that the global solve differs from the pairwise chain in TWO ways, and only one of
them was reasoned about. It adds skip links, which at this step genuinely do not exist. It also builds
nodes by CLUSTERING box centres in a common frame rather than by pairing them link to link, and that
part works at any step — its own docstring says so, and it went unread: "Clustering, not pairing, is
what makes a duplicated detector box across two frames ONE node."

So the gain is not the redundancy it was built for. It is the node construction, which is a different
mechanism that happened to ship in the same function. That is worth separating before it is relied on,
because the two would behave differently with a real detector: clustering is about duplicate boxes, and
duplicate boxes are what a low confidence threshold produces.

## The short version

Two questions were open. One is now closed and one is not.

**A circular field is solved.** Correlating only the pixels both receptors exposed recovers the whole
loss and slightly improves on the square baseline: 99.74 % and 99.90 % at the walk, against square
baselines of 99.66 % and 99.90 %.

**Realistic physics is not solved**, and nine separate attempts to solve it in the correlation are
refuted below, including the one with the strongest prior. Two things move it and both are protocol
rather than algorithm — how far the C-arm travels between exposures, and whether the exposure is a live
screening frame or a deliberate stored one. They do not compose, and together they reach about 98 % of
links against 100 % on clean film. That is a ceiling, not a result: a walk multiplies its links, so the
walk number is lower, and **no configuration measured here supports 99.7 % under physics.**

The physics penalty may be regional, which would matter more than the headline, and the evidence for it
is currently too thin to state as a finding. VerSe — cervical and thoracic at a 14.6 to 25.9 cm water
path — reaches 87.9 % and 91.4 % of links under physics at two and three bodies of overlap, against
70.0 % and 84.4 % on the abdominopelvic corpus, with a correlation margin of 0.23 rather than 0.04. It
is the only corpus here where the physics arm's error spread is TIGHTER than its own film arm's — an
interquartile error of 0.09 body against 0.28 — because a low-dose frame of a neck is still a good
picture of a neck.
CTSpinoPelvic1K sits at 31.2 cm against a generator ceiling of 32 and pins on about 80 % of frames, so a
thickness mechanism is available and already measured.

The sample is 29 spines and 33 to 39 links, over the whole corpus rather than a slice of it. That is
about 1.1 links per spine, which says what these studies are: the cranial anchor needs a scan containing
C2, and the scans in that corpus which contain C2 are short cervical studies that a 140 mm frame covers
in two exposures. So this is not "the whole spine is easier under physics". It is 29 short cervical
studies against 801 abdominopelvic ones, and the two differ in region, in study length, in links per
patient and in water path all at once.

The direction is consistent across every arm and the mechanism is measured rather than supposed — 31.2
cm against a generator ceiling of 32, pinning on about 80 % of frames. But a claim that the cost of
realistic physics falls on thick patients, which is the least convenient and most clinically important
thing measured here, needs a comparison that varies thickness and holds the rest still. Nothing run here
does that. The honest form is that the two corpora differ by 18 points in the direction thickness
predicts, and that four other things differ with it.

## The circular field

A C-arm with an image intensifier exposes a disc, not a rectangle. Cutting the corners off the frames
cost 5.2 points on CTSpinoPelvic1K and 25.2 on VerSe.

| | square | circle | circle, masked correlation |
|---|---:|---:|---:|
| CTSpinoPelvic1K | 99.66 % | 94.46 % | **99.74 %** |
| VerSe | 99.90 % | 74.65 % | **99.90 %** |

The mechanism is not subtle once it is looked at. The blanked corners are fixed to the RECEPTOR, so they
are in the same place in both frames and they correlate perfectly when the two discs coincide. They
collapse the margin over the one-body alias from 0.430 to 0.020. Correlating only the jointly exposed
pixels restores it to 0.378. `tools/test_masked_link.py`.

Masking ends at 99.74 % against a square baseline of 99.66 %, and that difference is NOT a difference:
21 wrong walks became 16, out of 6,238. Read as a sign test on the most generous discordant set
available without the paired records, p = 0.51. The claim is that masking RECOVERS what the circular
field costs, not that it improves on a square one, and an earlier version of this note said the latter
on the strength of five walks.

## Physics: what moves it

Links are scored against the true displacement, which `make_stations` knows exactly as the difference of
two frame origins. `paired` is the tolerance the linker actually applies when it decides two boxes are
the same bone, so it is the number that predicts a walk; `correct` is a stricter test reported beside it.

Under full physics with a circular field and masked correlation. The 9-inch ladder is the one with
the evidence behind it, and it is clean:

| field | overlap | step (bodies) | links | paired, physics | paired, film | one-body alias |
|---|---:|---:|---:|---:|---:|---:|
| 9-inch | 2 | 2.5 | 103 | 71.8 % | 99.0 % | 12.6 % |
| 9-inch | 3 | 1.5 | 157 | 81.5 % | 99.4 % | 3.8 % |
| 9-inch | 4 | 0.5 | 361 | **98.6 %** | 99.7 % | **0.0 %** |

At a half-body step the physics arm reaches the clean-film link rate and aliasing disappears entirely.

The cost in exposures is smaller than the link count suggests and the correction is worth making: the
probe builds a whole sweep and gets nine links per spine at this overlap, but a walk stops when it
reaches its target, and at the walk the mean is **3.82 exposures against 1.98** at the published step.
Roughly double, not quadruple.

It is not free on the other side either. Clean film FALLS from 99.74 % to 99.17 % over the same change,
because every extra exposure is another link to get wrong, and on frames that are already easy the extra
links cost more than the shorter move buys. The short step is a trade that only pays when the individual
links are unreliable, which under physics they are and on clean film they are not.

**Why the aliasing goes to zero is geometric, not a matter of the correlation getting better, and that
is the stronger claim.** The search runs from 0.6 of a body below the commanded step up to a step of
half a body. At a 2.5-body step that window reaches from 3.1 bodies down to 0.5 and therefore CONTAINS
the shift one body short of the truth; at a half-body step there is no room below the truth for a
one-body error to sit, so the alias is not improbable, it is unreachable. Shortening the move does not
persuade the correlation to be right. It removes the thing it could have been wrong about.

The larger fields do NOT extend this into a single ordering, and an earlier version of this note claimed
they did:

| field | overlap | step (bodies) | links | paired, physics |
|---|---:|---:|---:|---:|
| 12-inch | 2 | 4.1 | 48 | 56.2 % |
| 12-inch | 3 | 3.1 | 66 | 59.1 % |
| flat panel | 2 | 5.4 | 41 | 63.4 % |
| flat panel | 3 | 4.4 | 41 | 61.0 % |
| flat panel | 4 | 3.4 | 47 | 83.0 % |

More overlap helps within each field size. Across field sizes the ranking is not established: a
3.4-body step on the flat panel reaches 83.0 per cent where a 3.1-body step on the 12-inch field reached
59.1, so the step alone does not order them. These rows carry 41 to 66 links against 103 to 361 for the
9-inch ladder, because a large field covers a spine in one or two frames, and that is not enough to
separate 59 per cent from 83. What the larger fields show for certain is only that every one of their
physics links is flat -- 100 per cent below a margin of 0.05, at correlations of 0.985 and above.

### The second lever: what the exposure is

The renderer gives every frame 10 to 70 nGy at the detector, the low-dose CONTINUOUS FLUOROSCOPY range
measured on a mobile C-arm (PMID 30339271). But this protocol does not screen: it commands a move and
takes an exposure to be counted on, and the same measurement reports the same unit operating over 5 to
800 nGy per frame. A stored spot exposure sits at the upper end. Which one a theatre takes is a protocol
decision, exactly like the step length.

Links paired under physics with a circular field, at the published two-body step:

| exposure | | paired | IQR of error | correlation | one-body alias |
|---|---|---:|---:|---:|---:|
| 1× | live low-dose fluoroscopy frame | 73.0 % | 0.31 body | 0.948 | 10 % |
| 4× | stored spot exposure | 80.0 % | 0.10 | 0.972 | 7 % |
| 10× | stored spot exposure | **87.0 %** | 0.18 | 0.971 | 3 % |

Monotone, as a photon budget should be. Fourteen points for taking a deliberate exposure rather than
reading a live screening frame.

**The two levers do not compose**, and that is what bounds the whole physics arm:

| step | 1× | 4× | 10× |
|---|---:|---:|---:|
| 2.5 body | 73.0 % | 80.0 % | 87.0 % |
| 1.5 body | 84.4 % | 87.7 % | 85.7 % |
| 0.5 body | **98.3 %** | 96.5 % | 97.1 % |

The exposure is worth fourteen points at the published step, three at a body and a half, and nothing at
half a body, where the three arms are within noise and the 4× one is the lowest. They are redundant
because they attack the same limitation and the short step has already taken all of it. So the
recommendation has a cheap half and an expensive half rather than a sum: a theatre unwilling to pay nine
exposures takes a deliberate stored exposure instead of reading a live screening frame and gets most of
the way; a theatre willing to pay the exposures does not need the dose.

It also bounds the claim. Under this physics model the ceiling on links is about 98 % against 100 % on
clean film, and no configuration tried here passes it. A walk multiplies its links, so the walk number
is below that. **Nothing here supports 99.7 % under physics**, and the walk arms will say what it is.

**The exposure lever rests on an assumed parameter, and that has to be said plainly.** `tools/param_census.py`
shows 22 physics parameters: 7 measured, 10 derived, 5 assumed. `full_well_photons` is one of the five
assumed — no published value was found for it — and the exposure arm both depends on it and scales it.
So this lever has the weakest footing of anything reported here, and a real detector's well capacity
would settle it in one measurement.

This arm was broken the first time it ran and the first numbers from it must not be quoted: raising the
kerma without touching the full-well capacity saturated the receptor, the per-frame window then stretched
only the thick unsaturated regions, and the frames came out inverted — correlation between two views of
one spine reached −0.42. The well is a property of the detector at a GAIN SETTING and a real unit selects
a gain to suit the exposure, which is why a real panel does not simply saturate when the dose rises.
Scaling the well with the exposure models that selection. This is the one change here that makes every
image better rather than measuring something, so: the justification is a property of the detector rather
than the result, a well that does not move when the operating point does is wrong at any dose, and the
saturated fraction is recorded per frame so the claim stays checkable.

## Physics: what does not move it

Every one of these was tried against the true displacement. The baseline is 71.8 % paired.

| | paired | why it was expected to work | what actually happened |
|---|---:|---|---|
| vertical derivative | 40.8 % | endplates are horizontal edges, and that is what a reader counts on | correlation fell to 0.053; a derivative amplifies exactly the band a fluoroscopic photon budget fills with noise |
| high-pass, 7 widths | 32–46 % | scatter, heel and vignette are all low frequency | biased to a short step by +0.7 to +1.5 bodies at every width |
| high-pass normalised over the exposed field | 32–46 % | the plain version blurs the blanked exterior inward and leaves a ring at the stop | the ring is real and removing it does not recover the arm |
| column demeaning | 41.7 % | the anterior-posterior silhouette is the same at every height, so it correlates at every shift | did exactly what was predicted to the margin — 0.048 to 0.109, flat links 75.7 % to 26.2 % — and lost 28 points |
| detrending along the column | 42.7 % | the heel and vignette are ramps down the frame | no |
| mask erosion | withdrawn, see below | keep the correlation clear of the stop | an artefact |
| tighter search window | SUSPENDED | the code searches 2.1 bodies where the paper describes 1.2 | the probe applied it to the final link, which the chain exempts; see below |
| band about the spine | 48.5–65.0 % | correlate the vertebrae, not the abdomen | monotonically worse the tighter the band |
| phase correlation | 3.2–4.0 % | whitening normalises each frequency instead of subtracting the nuisance, so it does not pay for the removal in signal-to-noise | collapses; median error +0.9 to +1.9 bodies, and 53.9 % of links a whole body out at three bodies of overlap. Costs clean film 4 to 8 points as well |

Phase correlation deserves its own line because it was the one candidate with a strong prior — it is
what long-length radiograph stitching converged on, and it is invariant to the per-frame illumination
difference that a normalised correlation only partly removes. It had also been implemented here and
then left unreachable: `SHIFT_MODE` was exposed only through `sweep_map`'s own CLI and `fiducial_walk`
has no `--shift`, so no published arm had ever used it. It fails the same way the vertical derivative
did. Whitening lifts the top of the band, and this photon budget has a great deal of noise there. Two
independent methods now say the same thing about what that band contains.

The band sweep is the one that explains the rest. Confining the correlation to a column about the
vertebrae makes it worse in proportion to how much is confined — 48.5 % at one body wide, 65.0 % at
three, 71.8 % on the whole frame — so the correlation is living on abdominal texture rather than on the
vertebrae. Every filter in the list deletes signal to suppress a nuisance that a normalised correlation
was already handling.

Two more possibilities were excluded before being blamed. The physics frames look like fog, but the
spine band keeps 121 distinct grey levels against 251 on film and a row-profile standard deviation of
23.9 grey levels against 12.8 — MORE vertical modulation than clean film carries, not less. Quantisation
is not the problem and the vertebral signal is not weak.

## Two results that were withdrawn

**Mask erosion, 48.5 % to 82.5 % of links.** Keeping the correlated region three quarters of a body
clear of the field stop appeared to recover most of the physics gap, with an interquartile error of
0.10 body, tighter than clean film. It is an artefact. Eroding by that much shrinks each mask until two
frames a commanded step apart barely overlap, so `_ncc` refuses 21 % of the search window and the argmax
lands at the edge of the region it can still score — which sits near the true shift because the window
is centred on the prior. The giveaway was in the sweep and was nearly missed: the median bias runs
−0.51, −0.03 and +0.72 of a body at erosion radii of 0.50, 0.75 and 1.00, almost independently of the
filter width. An estimate whose bias is set by a tuning constant is not an estimate, and 0.75 would have
been chosen because it centres the bias, which is fitting the constant to the answer.

Nothing in the summary statistics could have caught it. `correct`, `paired`, `alias`, the median, the
IQR, the correlation and the margin are all computed over the shifts that were SCORED, and not one of
them says how few there were. It took a render of the correlation surface, which is the third time in
this project that a picture has settled something several rounds of argument from numbers got wrong.
`ncc_shift` now returns the fraction of its window it could score and refuses the link below
`MIN_COVER`; a refused shift no longer enters the table as a correlation of −1, because a sentinel that
is a valid correlation gets ranked against real ones.

**The search window verdict is suspended, twice.** The code searches from 0.6 of a body below the
commanded step up to a step of half a body, where the paper describes a window symmetric about the
commanded step: 2.1 bodies against 1.2. Two measurements said the code was right and the manuscript
wrong, and both were measuring a fault in the probe rather than the window — first the wrong end rule,
then the missing exemption for the final link. The question is open and is being remeasured with the
probe matched to the chain. At the WALK level, where the chain has always been correct, the tight window
under physics at two bodies of overlap reaches 75.75 % exact, which is above the physics baseline rather
than below it — the opposite sign from what the probe reported twice.

## Two defects found by an adversarial audit

Neither would have been caught by anything the pipeline reports.

**`--field-stop circle` does not set the field shape under physics.** The shape comes from the
RECEPTOR: `fluoro_physics` gives an image intensifier a disc and everything else a square, while
`FIELD_STOP` only gates whether the collimation fraction is stated or drawn. `--receptor` defaults to
`mix` and the physics walk scripts never set it, so every walk arm labelled "circular field under
physics" was about two thirds SQUARE frames — and the two frames of one link could carry differently
shaped stops, which no mask can repair, because masking assumes both frames were stopped the same way.
Asking for a disc now forces the receptor that has one. The affected walk arms were cancelled and rerun.

**The probe and the walk drew different receptors from identical flags.** The `mix` draw reads
`rng.randint` behind a `hasattr` guard falling back to index 0. `link_probe` used
`np.random.default_rng`, a Generator, which has no `randint`; `fiducial_walk` uses `RandomState`, which
does. So the probe pinned every frame to an intensifier while the walk mixed. The fallback is deleted
rather than repaired, and the probe now uses `RandomState`.

A third finding is recorded rather than fixed: **physics frames get no roll and no scale jitter, and
the film frames they are compared against get both.** The physics branch returns before the block that
applies `ROT_JITTER` and `MAG_JITTER`, so two consecutive physics frames differ by a pure translation —
exactly the transform the search solves for. Fixing it properly means rendering at a jittered
magnification rather than resampling afterwards. Its direction matters for reading every table here:
film is being made HARDER on the one axis the correlation solves, and film still wins by thirty points,
so the physics penalty is understated rather than flattered, and every refutation measured against it
stands.

## Two defects found in the probe itself

Both were found by checking the probe against the walk rather than by anything the probe reported, and
both invalidate results above. They are the reason the tight-window verdict has been suspended twice.

**The probe ran a configuration nothing publishes.** `sweep_map` carried `END_RULE = "clamp"` and
`LAST_LINK = "protocol"`. `fiducial_walk`, which produces every published number, overrides both on
every run to `"skip"` and `"open"`, and `make_count_figures` sets the same pair by hand — so the module
defaults were seen only by code that had forgotten to set them, and the probe forgot on the day it was
written. Under `clamp` the final frame of a sweep is shortened to whatever is left, so a large share of
links move less than commanded; under `skip` it is not taken at all. The defaults are now the protocol,
because a default that differs between two tools in one repository is a trap rather than a default, and
the probe prints which rules it ran. Remeasured, the physics ladder barely moved — 71.8 % paired to
70.0 % at two bodies of overlap — but clean film went from 99.0 % to 100.0 %, so the correction matters
most where the margin is thinnest.

**The probe gave the final link the wrong window.** It called `ncc_shift` directly and passed no bound,
so `TIGHT_WINDOW` applied to every link including the last. `build_chain` exempts that link
deliberately: it is the only one the protocol allows to be short, because the sweep ends where the
anatomy does. The verdict "the tight window costs clean film thirteen points" was a measurement of that
exemption being missing. Switching the end rule did not fix it and could not have — `skip` declines a
final frame that would move less than half a body and keeps one that moves 0.8 of a body when 2.5 was
commanded.

## Two defects found in the simulator itself

**The receptor blur happened before the quanta were counted.** The renderer blurred the signal by the
system MTF and then drew Poisson counts from it, which makes the signal correlated and the noise white.
A real detector does neither: a quantum is absorbed at a point and the light or charge it releases
spreads from there, so one blur shapes the signal and the quantum noise together. The focal-spot share
of the unsharpness happens in the beam and correctly precedes detection; the receptor share does not,
and now follows the draw. The electronic noise stays after and stays white, because it arises at the
readout.

**The noise-correlation row of the validation table measured its own filter.** It computed the
nearest-neighbour correlation of `a - median_filter(a, size=3)` and compared it against r(1)=0.20
measured on a real panel raw (PMID 24593724). A 3×3 median subtracts a value that contains the
neighbour, so its output is anticorrelated at lag one for any input — about −0.25 on noise with no
spatial correlation at all. The row could not have read positive for any detector, which is why it read
−0.128 before the blur order was corrected and −0.097 after. Its own note said it was how the blur error
was caught, so the receptor blur was sized against a measurement that could not measure it.

Replacing the median with a wider kernel did not fix it either, and the row went through four versions
before it measured the detector rather than something else. That sequence, and where it ends up, is in
*The simulator passes every external check it has* below; the short form is that it now reads 0.145 on a
flat field with the receptor shading removed, and agrees. The receptor blur turns out to have been right
on its merits — moving it after the Poisson draw is what puts r(1) in range at all, because quanta
counted after a blur come out white — but it was right by luck, since the row that was said to have
sized it could not have sized anything.

This is the trap this project already has a name for: a maximum extent is not a diameter, a
first-slice-that-works is not a plane, and a median-filtered residual is not raw noise.

## The physics arm has two known biases, and they point opposite ways

Neither is a defect to be fixed tonight. Both are things a reader has to be told before a number from
this arm means anything, and netting them against each other would be arithmetic on two quantities
neither of which is measured.

**Scatter is overstated, so the arm is too hard.** The scatter-to-primary ratio is the single parameter
with the largest effect on the result — the grid regime alone was worth thirty points — and it is
derived from the Fetterly 2007 thickness curve (PMID 17671340), cross-checked against an independent
Monte Carlo (PMID 36407382) to about 20 % and against a measured adult-abdomen Bucky factor of 5.87
(PMID 37491809). Its own note records what it leaves out: a mobile C-arm has a large air gap between
patient and receptor, and an air gap rejects scatter, so true values should sit BELOW these (PMID
1584148, PMID 22225284). The air gap is not modelled. How much it is worth here is not known, and
inventing a factor for it would be fitting a parameter to a result.

**Physics frames get no roll and no scale jitter, so the comparison is too kind.** The film frames they
are set against get ±3° of roll and up to about 10 % of scale mismatch between the two frames of a link;
the physics branch returns before that block, so two consecutive physics frames differ by a pure
translation — exactly the transform the search solves for. Film is being made harder on the one axis the
correlation actually works on.

So the physics arm is a hard case of unknown pessimism against a film baseline of unknown generosity,
and the honest reading of "71.7 % against 99.7 %" is that the gap is real and large and that neither end
of it is calibrated.

## The simulator passes every external check it has

This is a withdrawal. Earlier today this note said the synthetic noise power spectrum was
anti-correlated with real fluoroscopy at −0.52, and used that to argue the physics arm was not a
calibrated proxy for a theatre. That was the measurement, not the simulator, and the argument built on
it is withdrawn.

| quantity | this simulator | external target | |
|---|---|---|---|
| photons per render pixel at the detector | 414 (IQR 268–620) | 219–1532 (PMID 30339271) | agrees |
| scatter-to-primary map, p95 over median | 2.76 (IQR 2.19–3.78) | 1.42–2.85 (PMID 38942002) | agrees |
| nearest-neighbour noise correlation | 0.145 (IQR 0.120–0.218) | 0.02–0.20 (PMID 24593724) | agrees |
| generator pins by thickness | 100 % above 32 cm, 0 % below | pins only above the ceiling | agrees |
| noise power spectrum shape, raw | 0.862 | 1 = same shape | agrees |
| noise power spectrum shape, matched | 0.986 | 1 = same shape | agrees |

The noise-correlation row took four versions to measure one number, and the sequence is the useful part:
−0.128 on a 3×3 median residual, which forces a negative answer for any detector because the median
contains the neighbour; +0.707 on a wide-kernel residual, which counts trabeculae and cortical edges as
grain; +0.803 on a raw flat field, which measures the vignette; and 0.145 on a flat field with the
shading removed, which is the detector. Each version compared a number computed here against one
computed somewhere else without reproducing how the other was computed.

The spectrum row had the same fault in a different place: it compared raw synthetic frames against real
panels that had been downsampled to a journal column and JPEG compressed. Putting both through the same
press takes the agreement from 0.862 to 0.986, and the gap between those two is what the publisher did.

**The physics arm is therefore a calibrated proxy on every axis that can be checked**, and the 71.7 %
against 99.7 % is a real gap rather than an artefact of a pessimistic model. What remains uncertain is
stated in the section above: scatter is overstated because the air gap is not modelled, and the film
comparison is generous because physics frames get no roll or scale jitter. Neither of those is measured,
and neither is fixed by anything here.

## One question is answered

The step jitter was the one real doubt about the short step: a half-body commanded step leaves a search
window only 0.6 of a body wide, and the published mobile C-arm repositioning error is 16.7 ± 6.3 mm,
about half a lumbar body — comparable to the whole window. It does not break. At half a body of jitter
the short step holds 97.9 % of links paired against 98.6 % at none, and clean film falls from 99.7 % to
98.2 % over the same range. At the walk, physics at the published step moves from 71.73 % to 72.12 % at
0.3 body of jitter and 70.90 % at 0.5.

## What is still not known

**Every physics arm here uses ground-truth boxes.** The linker is handed the vertebrae and asked only
which of them are the same bone across two frames. Whether a detector finds vertebrae at all in a frame
that carries a realistic photon budget, a scatter pedestal and a pinned generator is not tested by
anything above, and it is the question a deployment meets first. The manuscript's own summary of this —
the linking is solved, the detection is not — was written about clean frames, and nothing here extends
it to physics. A physics number measured on given boxes is an upper bound on a physics number measured
on found ones.

**The thickness claim is not isolated.** The two corpora differ by 18 points in the direction thickness
predicts, and they also differ in region, in study length and in links per patient. A comparison that
varies water path and holds the rest still has not been run, and CTSpinoPelvic1K contains the thickness
spread to do it with.

**The two biases above are not quantified.** Scatter is overstated because the air gap is not modelled;
the film comparison is generous because physics frames get no roll or scale jitter. Both are named, and
neither has a number.

**No physics arm has run on real fluoroscopy.** The simulator now agrees with real panels on every
statistic that survives an 8-bit windowed JPEG, which is the histogram shape and the noise spectrum. It
has never been asked to link two real consecutive C-arm exposures of one patient, because no such pair
exists in any corpus here.

## The published configuration still produces the published number

A day of changes to `sweep_map` — a refused shift no longer entering the correlation table as −1, links
refused below `MIN_COVER`, new module defaults for the end rules, a receptor draw that no longer falls
back silently, four prefilters and three new globals — is supposed to be inert in the configuration the
manuscript reports. Tonight produced four separate cases of a change that looked inert and was not, so
it was checked rather than assumed.

| | measured | manuscript |
|---|---:|---:|
| CTSpinoPelvic1K, square field, clean film | **0.9966** on 6,255 walks | 0.9966 |
| whole-spine corpus, square field, clean film | 0.9990 on 953 walks | 0.9990 |

It reproduces to four figures. `slurm/regression_baseline.sh`.

## Why the probe exists

Four candidate fixes were adopted and then refuted on walk accuracy alone, at a fleet run apiece,
because a walk number cannot separate "the correlation found the wrong shift" from "the correlation was
right and the chain lost the vertebra elsewhere". `tools/link_probe.py` scores every link against the
displacement that produced it and refutes a candidate in about three minutes. It reports the SHAPE of
the error rather than its mean, because noise spreads about zero and aliasing piles at one body and a
walk number shows neither, and it reports the correlation and the margin beside them because a high
correlation with no margin is the dangerous case.

It lives in the repository because the first version of it lived in `/tmp` on a compute node and was
swept.
