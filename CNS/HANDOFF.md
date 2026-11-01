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
SCW), 0.6 mm from Panjabi on average from T2 to L4. 

v17, the same night: the canal read on the CT itself (soft tissue flood-filled behind the body inside a ring of bone,
200 HU), 0.7 mm from Panjabi's SCW on average and within 1.8 at every level, the neck included; the body's width
the upper end plate's over its front half on its own layer (pedicle bases and transverse-process roots left out),
from T1 down. Every full spine, grid job 40906993 (`generator/grid/`, `figs_v17_6min/`); the gaps that remain and
why are SchwingNet docs/research/morphometry-against-panjabi.md.

v18 (Greg's words of the same night): the body's width drawn from C3, read at the lower end plate (beside Panjabi's
EPWl), whose width no uncinate process joins, and the depth at the upper end plate (EPDu), whose depth no anterior
lip joins; no standard deviation drawn, means alone.

v19 (Greg's ask the same night): the gold tier means reweighted to Panjabi's twelve cadavers' sex and age (each
specimen matched to our adults of its sex within 5 years of its age; 984 adults whose sex and age are read;
`make_profile_v19.py`, `grid/standardise.py`, job 40912660). Against Panjabi within 1 mm: the canal's width at 14
of 17 levels, the body's depth at 11 of 16, its width at 10 of 17; height as well or instead matched no better.

v20 (Greg's ask the same night): slide 5 in four clicks, four slides (5 to 8) joined by Morph so the lines move:
the v19 line in purple; divided into men (blue) and women (red), each matched to Panjabi's own 8 men and 4 women;
our adults inside Tan 2004's age, height and weight ranges (73, 16 of them men; green) beside Tan's ten Chinese
Singaporean cadavers; our adults reweighted to Alonge 2021's sex and age (orange) beside Alonge's 120 Nigerian CTs,
the lumbar canal only. No series in the 39 papers measures these chords in African Americans (Yu 2015's Hamann-Todd
skeletons give pedicles, Shin 2024 discs). The lines and reference points are PowerPoint shapes of one name on all
four slides (`prep_v20_benzel_profile.py` writes `figs_v20_6min/geometry.json`, `grid/reweight.py`, job 40915304);
an older PowerPoint fades instead. Panjabi is gray now, since red is the women. Slide 7 (now 10) is redrawn in
Benzel's style (`prep_v20_spinopelvic.py`): grey histograms, closed black frame, inward ticks, the published means as
black dashed and dotted lines. Later slides are numbered three higher; the clock is 5:26. Use v20.

v21 (Greg's asks of the same night, the provisional filed): `make_cns_deck_v21_6min.py`. Benzel's two scans are
every click's base, in slide 4's exact boxes, with the lines laid over them in the scans' own calibration
(`prep_v21_benzel_profile.py`) and his vertebra drawing laid over the lines as a transparent copy, so the step from
slide 5 (Benzel) to 6 and every click after it moves only the lines. Slides 6 to 10 share one title: purple
(reweighted to Panjabi), men and women, Tan, Alonge, then every decade of each sex (blue and red, deeper the farther
from his cadavers' 46; `grid/bands.py`, job 40928273). Slide 11 is a film (`render_v21_fingerprint.py`) that opens
on slide 10 exactly: the decades turned into depth, four ideal spines (the pan's CT, scaled to a decade's means)
lit gold with their lines, the lines leaving as snakes and settling as a fingerprint. Slide 12 is that fingerprint
beside bordercall's synthetic naming against bodies in view (`prep_v21_bodies.py`). Slide 13 is v14's masks slide.
Slide 14 is the pan film (`render_v21_pan.py`), patent pending on the slide's foot and nothing written in the film:
ENHANCE.PET CT 0036 (thinnest slices, normal by its labels, no metal under C2) projected laterally, made real by
FLUX.2 klein-9B as released (`grid/pan_render.py`), cut as a 30 fps prone pan from the sacrum to C2; the reported
detector, encoder and head on every frame (`grid/pan_detect.sbatch`); names from `pan_link.py` (frames registered by
phase correlation, counted up from the L5 the model named, the model's own reads above the shoulders; on this CT 17
named, all as its labels; T4 to C6 never seen, placed between the two ends in a muted shade); the CT's vertebrae in
3D filling in below. The spinopelvic slide moves to 4 and the canal rows go after the end as a backup.

The grid, for the next run of it: hpcworker's gpu class offers gmsap, gvohp and galhp only, all full of month-long
jobs that night; the films' FLUX job ran on reqp's RTX PRO 4500 (32 GB) by `sbatch --partition=reqp --qos=requeue
--gres=gpu:nvidia_rtx_pro_4500_blackwell:1`, inside SchwingNet's bookworm container (`grid/box.sh`), since the realism
venv needs a newer glibc than the nodes' CentOS 7; the detector ran on reqp's A30 in the fluorogen env. The film
histogram reference `~/films_drr` was pruned, so the prototype ran without it. Use v21.

v22 (Greg's asks of 1 November): `make_cns_deck_v22_6min.py`, 17 slides, about 6:00. The pan film missed the
thoracic, so its frames were made again (`grid/pan_render.py`, runs 6 to 8 on the same CT 0036): the shoulder
girdle and arm bones taken down to soft tissue, a slab about the spine from T6 up cut after the body is found
(170 mm at T6, 110 at T3, 80 from T1 up), and the bodies from C5 to T12 weighted up as a swimmer's view lifts
them. On run 8 the linker counts unbroken from the L5 the model named to C3, 22 of 22 as the CT labels them;
the detector boxed no C2, which stays unlit in the 3D map (`render_v22_pan.py` also lights a counted body only
after the one below it). Slide 14's plot is bordercall's smooth build-up figure (records/curve-2026-10-28,
`prep_v22_bodies.py`): named exactly, named at 99 per cent certainty, and right when so named, against measures
added, for 1, 3 and 9 bodies. New slide 4 turns the gallery's eight anomalous spines (`render_v22_anomalies.py`,
the website's own meshes, the focus structures gold), its gallery page linked on the slide and the film. The canal
level by level moves from the backup to slide 6. The end slide shows the website's home page in a browser window
linked to the site (`prep_v22_site.py`). The scripts of slides 5, 7 and 15 were cut to pay for the new slides.
Use v22.

The same afternoon Greg saw the detector stop at the lumbar-thoracic turn and then box the thoracic bodies all at
once. At the reported floor of 0.35, and even at 0.05, the detector boxed nothing from T12 to T8 while the lumbar
bodies filled the field; the mirrored frame boxed T12 at 0.8. So the film now uses run 9: T7 to T12 weighted up by
40 per cent, the detector run over each frame and its mirror image at a floor of 0.05 (`grid/pan_detect.sbatch` takes
CONF, DET and FACING), and the linker reading both at 0.10, pooled, a weaker box kept only on the column the
reported floor's boxes trace (`pan_link.py --det det_low_L --floor 0.1 --flip det_low_R`). It names 23 of 23 by count
from L5 to C2, and each body from T12 up is boxed within about half a second of entering the field; the film carries
a named box through up to 8 frames the detector misses. At 0.05 a stray box enters the count and every name above it
is one level off, so the floor is not a free choice.

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

## U251 v8 (2026-11-01)

`u251_litt/CNS2026_Schwing_Abstract418_CNStemplate_v8_6min.pptx` and its instructions replace v7 for the 7:00 AM talk,
5:41 by word count. Greg asked for the figures a Cell or Nature recurrence paper uses, no slide offering the
opposite-hemisphere U251N as contamination, Raj's ablation video at 4K, and the pre- and post-LITT biology and drug
targets emphasized. The model is Varn FS, et al. Cell 2022;185:2184-2199: slide 4 is per-lesion composition columns
with an arm track and arm averages (tumor share p = 0.10, microglia p = 0.40 by the exact test over the 20 splits, so
no star), slide 10 the recurrence-phenotype schematic in place of v7's two readings, and slide 11 new: the DSigDB drug
screen on the published ranking and on the two RUVSeq rankings whose factors come from the three control samples
(job 40935350). 6 of the 16 published signatures hold at two factors, all hypoxia-led (ciclopirox, deferoxamine,
dimethyloxalylglycine); the ribosomal-protein drugs fall to q > 0.8; at one factor the direction holds but q is
0.62-0.67. The sizing slide drops the pieces cut after a tumor. The video is a 2160-pixel render of the 64-pixel
original. Built by `SLIDES/20_v8_figures.py`, `21_build_deck_v8.py` and `22_instructions_v8.py` in the U251 study's
folder, with the screen in its `ANALYSIS/drug_controls/`; that repository is public, so none of it is pushed there.

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
the notes. No number from memory: read it from the result file. In the U251 talk, Greg's word of 2026-11-01: the
opposite-hemisphere slides show the measurement and raise no alternative reading of it.
