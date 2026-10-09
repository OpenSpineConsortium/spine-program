# The three physics defects, fixed and then MEASURED — and what actually hides the spine

Written 2026-09-22 after fixing all three and measuring each one's effect on the image. It corrects
`docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`, whose title and first section blame the wrong term.

## The short version

| # | Defect | Real? | Measured effect on the image | Status |
|---|---|---|---|---|
| 1 | `sweep_map --perturb physics` rendered from the merged density path, with no separate bone term | code inconsistency, **not** the cause | **none**: box spread 24.0 and noise 9.2 with the merged path, 24.0 and 9.2 with the water+bone pair | fixed anyway |
| 2 | `fig_story_rows` styled device frames with an all-zero bone path | code inconsistency, **not** the cause | small and in the OTHER direction: box spread 62 with the defect, 56 correct | fixed |
| 3 | the cards' exposure model extrapolated outside its fitted thickness range | **yes, this is the one** | PIXIUM 4600: 4,607 -> 103,084 photons/mm², and the frame stops being speckle | fixed |
| 4 | (not on the original list) the display window is set over the WHOLE exposed field | **yes** | collimating to the spine raises the box spread from 27 to 153 grey levels | open: a protocol choice, not a bug |

## Why defects 1 and 2 could not have been the cause, algebraically and by measurement

`make_drr_dataset.water_path_cm` integrates `1 + HU/1000`, so the bone's density is already inside it. The
cards' pair is water capped at water density plus the positive-HU excess times the 70 keV water/cortical ratio.
At the effective energy the two are the same attenuation:

    mu_w·min(1+HU/1000, 1) + mu_b·(HU/1000)·(mu_w/mu_b) = mu_w·(1 + HU/1000)

What the pair adds is the bone's own SPECTRUM, which only the polyenergetic card path uses. Measured on
CTSpinoPelvic1K 149 (34.6 cm of water through the L4 box, bone 0.61 cm at the median):

- `fluoro_physics.render`, merged path versus the pair, same seed: spread 24.0 / sd 9.2 in both, to the digit.
- `device_style.style_paths`, the pair versus the defect (merged path as water, bone zeroed): 56 versus 62 grey
  levels of box spread. The defect made the frame slightly BRIGHTER-ranged, not flatter.

So the earlier statement "the physics mode has no bone term, which is why no spine is visible" was wrong. The bone
was always there. Both tools now use the cards' convention because consistency is worth having, and because the
record each render writes now says which input it had (`bone_term`), but neither fix changes an image.

## What defect 3 was, and what fixing it did

A card's AEC is a regression of log10 photons on water-equivalent thickness fitted over the thicknesses its paired
frames contained: 9.3-11.5 cm (PIXIUM 4600, n=18, R² 0.19, slope NEGATIVE) and 9.7-19.7 cm (Cios Fusion, n=366,
R² 0.15). A lateral abdomen is 28-38 cm. Extrapolated there, the PIXIUM card gives a thick patient FEWER photons.

`tools/device_style.aec_gain` now does what a real C-arm does: outside the fitted range it raises output until the
DETECTOR sees what it saw at the fitted edge, `exp(mu_water·(thickness - fitted_max))`, capped at
`AEC_MAX_GAIN = 30` because a tube saturates. Inside the range nothing changes, so no existing corpus moves unless
it was rendered thicker than its card's fit. Every frame carries `aec_gain`, `aec_fit_thickness_max_cm` and
`aec_extrapolated`, so a number drawn from an extrapolated frame can be labelled as one.

Measured, same frame and seed (CTSpinoPelvic1K 149):

| card | AEC | photons/mm² | box spread | box sd |
|---|---|---:|---:|---:|
| PIXIUM 4600 | off | 4,607 | 109 | 44.1 |
| PIXIUM 4600 | hold detector | 103,084 (×22.4) | 56 | 21.1 |
| Cios Fusion | off | 18,237 | 58 | 20.9 |
| Cios Fusion | hold detector | 83,805 (×4.6) | 55 | 20.1 |

The spread falls because the speckle that inflated it is gone: the PIXIUM frame goes from salt-and-pepper noise to
a readable lateral abdomen (looked at).

## What still hides the vertebrae, and it is not a bug

Even with clean statistics, a 34 cm lateral abdomen from a CT COLONOGRAPHY scan shows no vertebral bodies, because
the display window is set over the whole exposed field and the insufflated colon spans most of it. The bone's own
primary contrast across the L4 box is 33 %, and the per-pixel contrast-to-noise is about 2.5, so the signal is
there; it is the window that spends its range elsewhere. Collimating to the spine, which is what a lateral lumbar
exposure does, moves the box spread from 27 to 153 grey levels:

| field (fraction of the frame) | box spread, grey levels |
|---|---:|
| 1.00 | 27 |
| 0.60 | 31 |
| 0.35 | 56 |
| 0.22 | 153 |

So a device-styled lateral sweep needs BOTH the AEC fix and a collimation typical of the view. That is a protocol
decision (how tightly the surgeon collimates), and it is an arm to be run, not a default to be assumed.

## Reproduce

    python tools/diag_card_lateral.py --drr ~/ctsp_drr --case CTSP_COLONOG_149 --card pixium_4600 --out <dir>
    # and the three local diagnostics kept in the session scratch: diag_sweep_bone.py (defect 1),
    # diag_bone_share.py (defect 2), diag_aec_effect.py (defect 3), diag_sweep_collimate.py (the window)
