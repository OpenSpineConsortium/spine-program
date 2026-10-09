# `sweep_map --perturb physics` frames show no spine (looked at 2026-09-22)

> **CORRECTED 2026-09-22, same day.** The title's diagnosis is WRONG. The missing bone term is not why the spine is
> invisible: the merged density path already carries the bone, and rendering the same frame from the water+bone pair
> gives the identical box spread (24.0) and noise (9.2). What actually hid the spine on the CARD path was the
> exposure model extrapolated outside its fitted thickness range, and on every path the display window set over a
> whole 38 cm abdomen. Measurements, and what each fix did, are in
> `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`; read that first. The observations below stand; the causal
> claims in "Why, as far as the code says" do not.

## What was seen

Figure 1 row (f) was run through `tools/fig_story_rows.py --perturb physics` (job 40414145) on VerSe 547, 602 and
631 (C1 to L5 with a thirteenth thoracic vertebra, instrument on T13, counted from the top) and on CTSpinoPelvic1K
149, 167 and 175 (six lumbar vertebrae, instrument on L6, counted from the sacrum), several seeds each.

Rendered and viewed: `or_ready/story_rows/fig1_row2_stitch_physics_verse602_t13_s1.png` and
`fig1_row2_stitch_physics_CTSP_COLONOG_175_l6_s1.png`. Every exposure is a smooth soft-tissue gradient with
quantum noise, the dark air above the skin, the collimator disc on intensifier draws, and the table edge. No
vertebral body, end plate, pedicle or disc is visible. The truth boxes sit over empty-looking anatomy.

The outcomes follow from that: VerSe chains had 27 to 32 nodes for about 25 bodies, CTSpinoPelvic1K chains 7 to
14 for 9 to 11, and not one confirmation located the transitional level.

The same geometry under `--perturb film` (CTSpinoPelvic1K 1) shows the spine clearly, links to 9 nodes for 9
bodies, and the confirmation located L2 correctly (rows b and c of Figure 1).

## Why, as far as the code says

The physics mode renders from ONE map, `path/<case>.npy`, the water-equivalent path from
`make_drr_dataset.water_path_cm`: density linear in HU (`1 + HU/1000`), summed along the lateral ray. Its own
docstring says it understates cortical bone at diagnostic energies (no photoelectric term). A lumbar body then
adds a few per cent to a lateral path near 30 cm, which the drawn scatter pedestal and quantum noise bury. The
row (e) corpus builder uses separate water and bone paths; the sweep's physics mode does not.

This is an explanation consistent with the code and the images. It was later tested (13:45 update below): adding the
bone term with the cards' own definitions did NOT by itself make the spine visible on these lateral abdomens, because
28-38 cm of water photon-starves the frame and the colonography gas takes the window. The missing bone term is one
cause, not the only one.

## What it affects, and what it does not

- Anything measured with `sweep_map --perturb physics` measured linking on soft-tissue texture. That includes
  the physics-linking results in `docs/HANDOFF_PHYSICS.md` (for example the circular-field figure). Those frames
  should be rendered and looked at before any such number is quoted; this note does not judge them.
- Not affected: `--perturb film`, the training corpus (`devcorpus_build`, separate water and bone integrals), the
  device cards themselves (fitted on real frames), and every real-image result. The figure tool's `--perturb card`
  WAS affected; see the update below (an earlier version of this note wrongly listed it as unaffected).

## Next

Job 40414314 reruns row (f) on the same spines and seeds with clean frames, with device-card styling before
linking, and with physics at three bodies of overlap, printing nodes against bodies for each. A physics render
that shows bone needs a bone path with its own attenuation, as the corpus builder has.

## Update, 13:25 EDT: the figure tool's device-card styling had the same defect

`tools/fig_story_rows.py restyle` passed the merged density path as water and an all-zero bone path to
`device_style.style_paths`. Frames styled this way also showed no spine (looked at: Cios card, CTSpinoPelvic1K 149).
The card arms of job 40414332 (45 exact chains / 23 L6 located for Cios and Elekta, 21 / 1 for BV Pulsera, of 54)
were therefore measured on bone-free frames; they are void and were removed from the claims ledger. Their exact
chains most likely came from the linker's commanded-displacement prior on a flat correlation surface.

The training corpus is NOT affected: `devcorpus_build` ray-casts separate water and bone integrals
(`deepfluoro_render.raycast`) and styles those.

Fix: `make_drr_dataset --paths2-only` writes `path2/<case>.npz` with water and bone line integrals under the
cards' own definitions (water capped at water density; bone = positive-HU excess x MU_RATIO_E0), and the figure tool
styles from that pair, refusing card mode without it. Job 40414408 computes the pairs for the 18 L6 spines and
CTSP_COLONOG_1 and reruns the arms; 40414409 redraws the rows.

Clean frames (no styling) were valid in 40414332: 45 of 54 chains exact, L6 located in 36; the misses with exact
chains were two spines landing one body caudal (on L5) on every seed and one spine never matching.

## Update, 13:45 EDT: with bone, the pelvic/hip/CBCT cards still show no spine on a lateral lumbar sweep

With `path2` (water + bone) the Cios-card frames of CTSpinoPelvic1K 149 still show no vertebrae. The maps are not
the cause: rendered side by side (`paths_149.png`, scratch), the bone path shows the whole spine (0.24 / 1.14 /
2.92 cm at p50 / p90 / p99) aligned with the bone render. The water path is 28.6 cm at the median and 38 cm at p99:
a lateral abdomen, with the insufflated colon of CT colonography visible as large gas pockets. At the Cios card's
photon count the transmitted signal through 30+ cm is a handful of quanta per pixel, and the gas pockets take the
display window. The Cios (pelvic AP cadavers), BV Pulsera (hip phantom) and Elekta XVI (cone-beam kV) cards were
fitted on thinner paths; lateral lumbar is outside all three. The C-ArmLSpine card (FIRST Surgio-B51, real lateral
lumbar frames) is the right one; its fit is running (40414081 -> reperframe 40414082) and row (f) is queued behind
it (40414418, drawing 40414419). The fourth pass (40414408) still runs the three out-of-range cards; read its
numbers as out-of-range, not as the method.

## Update, 14:10 EDT: the term is the photon count, and the thickness is outside every card's fit

`tools/diag_card_lateral.py` (job 40414506) renders one frame six ways, changing one term at a time
(CTSpinoPelvic1K 149 and 267, PIXIUM 4600 and Cios Fusion cards). On 149, 27.6 cm of water at the centre, the
bone in the L4 box is 0.61 cm at the median and the bone's primary modulation is 19.1 % -- ample. Removing
scatter entirely, or dividing it by five, changes the box SD by 2 to 4 grey levels. **Quantum noise is what
removes the spine**: the noiseless render of the same frame shows the vertebral bodies and the ribs plainly.
At the PIXIUM card's 4,607 photons/mm^2 and 0.8 mm pixels, about a dozen quanta per pixel survive 28 cm of
water, so the per-pixel noise exceeds the bone's modulation.

The cards do not extrapolate there, and they say so themselves: `distribution.aec.log10_photons_on_thickness`
has `x_range` 9.3-11.5 cm (PIXIUM, n = 18) and 9.7-19.7 cm (Cios, n = 366), with R^2 0.19 and 0.15. A lateral
abdomen at 28-38 cm is outside both, and the PIXIUM slope is negative, so the sampler gives a thick lateral
FEWER photons. A real C-arm's automatic exposure control raises output until the detector sees enough signal;
the fitted regression, extrapolated, does not.

What this does NOT invalidate: the styled training corpus, whose frames are AP-ish views of 10-20 cm at the
devices' own poses and do show the spine (looked at: cios_fusion__cios_fusion val frames).

So row (f) is drawn under the film noise model (fitted to real radiograph statistics, and it shows bone) over all
18 L6 spines and 3 seeds (job 40414514), with the clean render as the control, and the manuscript states that
device styling of a lateral abdomen is outside every fitted card's exposure range.
