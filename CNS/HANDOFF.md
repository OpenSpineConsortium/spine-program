# CNS 2026 talks: handoff

For the next account or session. Greg asked that the two jobs below NOT be done on the account
that wrote this file, so nothing below has been started.

| Talk | When | Deck |
|---|---|---|
| Abstract 418, LITT in U251 (SSTU02) | Mon 2 Nov 2026, 7:00 AM, 6 min | `u251_litt/` |
| Not All Spines Are Created Equal (MP4SP1) | Mon 2 Nov 2026, 5:21 PM, 6 min | `not_all_spines/` |

Open jobs: issue #247 (rebuild the slide after Benzel) and issue #248 (the video). Claim them
the usual way. A session of Greg's merges its own pull request once the required check is green.

Both decks live in the CNS template. Edit `CNS2026_Schwing_NotAllSpines_public_v14_6min.pptx` in
place with python-pptx: speaker notes on slides 2 and 3 were shortened after the generator last
ran, so a generator rerun reverts them, and the copy in `not_all_spines/generator/` has the
annotators' names replaced by [student A-K] as this repo's text copies do.

## Job 1, issue #247: replace slide 5

Done 2026-10-31: `CNS2026_Schwing_NotAllSpines_public_v15_6min.pptx` and its instructions, built from v14 by
`generator/make_cns_deck_v15_6min.py` (slide 5 alone changes) from the panels `generator/prep_v15_benzel_profile.py`
draws. Gold tier 3 and 4 is 2,290 whole-spine CTs, one a person (1,620 tier 3, 670 tier 4), measured by
bordercall's morphometry engine; the aggregates are `generator/figs_v15_6min/profile.json` from SchwingNet grid jobs
40906591 and 40906695 (`generator/grid/`). Benzel's lines are black as in the book, the gold tier mean and SD blue,
on Benzel's own axes and ranges with T13 and L6 added. The brief below is kept as the record of the ask.

v16, the same evening (`make_cns_deck_v16_6min.py`, `prep_v16_benzel_profile.py`, `figs_v16_6min/`): Panjabi's 12
cadavers added in red, and each gold tier line drawn only where the measuring code read the measure by its own
definition (profile job 40906874, `as_defined`). The neck's widths are not drawn: the code finds the foramen
transversarium closed in under one cervical vertebra in ten and both pedicles in about one in a hundred, so the body
is cut at the canal's walls and the canal's width is a stand-in; every label source and slice thickness agrees, so
it is the code, not the labels. Canal width is now the greatest interpedicular distance (Eisenstein 1977, Panjabi's
SCW), 0.6 mm from Panjabi on average from T2 to L4. Use v16.

Slide 4 is the textbook: Benzel, chapter 1, Fig. 1.1 (vertebral body width and depth by level) and
Fig. 1.9 (spinal canal width and depth by level). Slide 5 today is a violin of end-plate width.
Greg rejected it. He wants, in his words, "an actual rerendition of the slide exactly the same ...
literally the exact same slides with the phantom and all, but using my gold tier3/4 data and
benzels data plotted as a reference."

So the new slide 5 is slide 4 again, with his data:

- The same two panels, same size and position on the slide, same axes, ranges and tick labels
  (body 15 to 60 mm, canal 10 to 30 mm, cervical, thoracic, lumbar along the bottom).
- The same line code: width solid, depth dashed, black on white, same in-plot labels.
- The same vertebra phantom with its arrows, in the same place in each panel. Crop it from the
  scan or redraw it faithfully. This is the part he named, so do not drop it.
- His data are the main lines. Benzel's curves are plotted on top as the reference, in a visibly
  different treatment, with a legend.
- Caption one line, 60 words or fewer: says what is his, what is Benzel's, that Benzel's values
  were digitised, and "permission pending".

Sources in `not_all_spines/generator/figs_v14_6min/` (the Benzel panels as extracted). Digitise the
curves from those images, overlay the result on the original to check it, and say in the caption
that they are digitised. Fig. 1.1 prints "12" on the axis where L1 belongs. That is the book's
error: plot the true level and mention it in the instructions.

Not what he wants: `03_ctspinopelvic1k_dataset/mdpa/scripts/plot_anomaly_benzel.py` is called
Benzel-style but is a horizontal per-anomaly plot.

**Stop and ask first: what is "gold tier3/4"?** No file readable from the last session defines
it. The ruleclass census records tier 1 and tier 2 only (see `ruleclass/tiers/TIERS.md` under
`/rs/rs_grp_oschome/go2432/`, which is on the grid and was not read). Read that, then ask Greg
rather than guess. Do not quietly use `level_atlas.csv` in its place: that is the data he just
rejected the presentation of, and CTSpinoPelvic1K's labels are abdominopelvic (about T11 down),
while Benzel's axes run from C2 or C3, so a whole-spine source decides how much of each panel can
be filled. If his data do not reach cervical, leave those levels empty and say so on the slide.

Traps, from `CTSpinoPelvic1K-1/CLAUDE.md`:

- Match Benzel's definitions, not just his units. A maximum extent is not a diameter, and a
  first-slice-that-works is not a plane. Canal depth is a midsagittal chord at a named plane.
- L5 end-plate width was withheld on purpose: the transverse processes fall in front of the cut.
  Render the mask before trusting any L5 width.
- Resolve labels with `ostk.labels.labels_for(volume)`, never a fixed map. The release is v11.
- Compare the spread, not only the median, against something outside the computation.

Slide 6 (canal rows) overlaps the new right panel. Keep it unless Greg says to delete it. The
talk has about 1:25 spare at 140 words a minute by word count; nobody has timed it aloud.

Every slide needs short, natural speaker notes that explain the figure. Render through PowerPoint
and look at the slide before calling it done.

## Job 2, issue #248: the video

Greg wants a video of SchwingNet detecting vertebrae on a fluoroscopic pan. Generate frames from a
gold tier 3 full spine CT, stitch them into an mp4, and make it look real.

Deliverable: `not_all_spines/schwingnet_pan_demo.mp4`, H.264, 1920x1080, 30 fps, about 15 to 25 s,
tested inside PowerPoint in slideshow mode, plus a version of the deck with it embedded.

Start from `01_carm_level_detection/docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md`, which already names
the weights and the flags. In short:

- Frames: a single full-spine CT, with no vertebra the encoder trained on (`unseen_v9.txt`),
  projected along a smooth craniocaudal pan with the project's DRR code. Read
  `drr-row-spacing-defect` and `physics-three-defects-measured` first.
- Look: circular collimation, magnification, quantum noise, contrast, vignette. Keep the histogram
  match to `~/films_drr` on.
- Detection: the real stack, run on every frame: `--detector
  /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt --model
  ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt --head
  ~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt --no-orient --flag --conf 0.35`.
- Boxes and names are the model's raw output. No hand-placed boxes, no edited labels, no re-runs
  until it looks right. If you smooth over time, say so in the notes.
- GPU work through Slurm (`gmsap` or `gvohp`), outputs on `/rs/rs_grp_oschome/go2432/`, nothing on
  the login node, nothing container-related on warrior.

Two conditions. Do not drop either without Greg's word.

1. **Burn in a caption: "Simulated from CT."** Realistic is what he asked for and it should be.
   But the frames are synthetic, and a CME audience of surgeons will take unlabelled fluoroscopy
   as a real patient exposure. Say it in the speaker notes too.
2. **Disclosure.** A pan with detection on X-ray-like frames is what the v11 public cut removed
   from the talk: Part B and the sweep. The record says the tech transfer office had not cleared
   Part B and the sweep was in no filing. Build the video and keep it in this internal repo. Do
   not put it in the public deck, upload it or show it until Greg confirms after hearing that.

## Waiting on Greg

- Slide 8 of Not All Spines is unpublished, shows only crops the model read correctly, and has the
  same disclosure question. Delete it if he is unsure; the talk then runs about 4:10 by word count.
- Benzel permission (Thieme). Both figures are marked permission pending.
- Whether the invention disclosure changes the ACCME financial relationship (education@cns.org).
- U251: Nagaraja 2021 video permission; whether the contralateral slides go in before the
  manuscript is submitted.

## Rules that apply here

Never use the word Greg bans in this repo's docs. Captions 60 words or fewer. Charts as lines or
donuts, never a sideways bar. A slide is the figure plus one caption line; text cut from it goes in
the notes. No number from memory: read it from the result file. The instrument sentences in the
U251 talk stay conditional: migration in life and carry-over at dissection cannot be separated.
