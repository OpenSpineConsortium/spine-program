# Reviewing the transitional-vertebra tree

*For the two reviewers. The rules behind this page are `docs/ruleclass/PREREG_rules.md` (draft v1). Questions to Greg.*

## What you are looking at

A computer pass over about 21,000 CTs flagged spines whose lumbosacral or thoraco-lumbar junction looks unusual.
Each flagged CT is one **case**: a short README, the rule evidence, image previews, and the volumes (CT, masks,
and for 850 people a radiograph of the same person). No case tells you what an earlier reader or database said
about it; that is deliberate.

Two people look at every case, in order. **Stage 1 (screen, Ashley):** is the case what its type says?
**Stage 2 (confirm, senior reviewer):** the same question, on the cases stage 1 accepted or could not decide,
without seeing stage 1's answer, reason or name. Rejected cases stop at stage 1. Both verdicts, reasons and times
are joined in an audit table Greg reads.

## The types, one line each

- **L6** — six free bodies between the lowest full rib and the sacrum: a true sixth lumbar vertebra, or a T12
  that lost its ribs (then the count is really an ordinary five).
- **T13** — a thirteenth rib-bearing vertebra; decidable only when the whole rib cage is in the picture.
- **four_lumbar** — four free bodies: L5 fused into the sacrum, or L1 carrying a rib and counted out.
- **complete_sacralisation** — the lowest body sits more than half inside the sacrum label.
- **castellvi_II_IV** — the lowest body touches the sacrum (10–50 % inside the label): a partly fused
  transitional vertebra or a transverse process articulating with the sacrum.
- **lumbarisation** — a free, mobile body lying wholly below where the sacrum should start (a free S1).
- **lumbar_rib** — a short rib on the first lumbar-shaped body.
- **stump_rib** — the lowest rib is 38 mm or shorter, not cut off by the picture edge, under a normal rib above.
- **sacral_shape** — pelvis or sacrum measures outside the usual range. No proven cut-off yet: a hint, not a call.
- **labeller_disagreement** — the two segmentation programs disagree on the count or on what the sacrum swallowed.
- **no_anchor** — the sacrum could not anchor a count (missing, tiny, at the bottom edge, or the two programs put
  its top more than 20 mm apart). A person has to look.
- **ordinary_control** — a spine the rules called normal, mixed in as a control. Review it like the rest.

## Stage 1: accept / reject / unsure

Count for yourself from the anatomy, then compare with the evidence.

1. **Find the lowest real rib** — longer than about 4 cm (38 mm is the published cut) and not chopped by the
   picture edge. Its vertebra is the last thoracic one. A 2–3 cm rib under a normal rib is a *stump*; its
   vertebra still counts as thoracic.
2. **Find the top of the sacrum** — the first segment whose sides flare into wings. The evidence gives, per body,
   the fraction `f` inside the sacrum label: under 0.10 free, 0.10–0.50 touching, 0.50 or more absorbed.
3. **Count the free bodies in between.** Five is ordinary; six or four is what most cases claim.
4. **For a six, look at the top body's shape.** Facet joints facing front-to-back, transverse processes in front
   of the facet: lumbar. Facet joints facing side-to-side, a short process level with the facet, a costal pit on
   the body: thoracic — a T12 without ribs, and the count is really five.
5. **If the picture is cut** so the lowest real rib or the top of the sacrum is not in it, the count cannot be
   made. That is **unsure**, never accept — the rules call it `no_count` and so must you.

**Accept** when what you see matches the type. **Reject** when it plainly does not (a full rib on the "sixth"
body; five ordinary bodies; a "stump" that is a rib cut by the edge; a segmentation error rather than anatomy).
**Unsure** when the field is cut, the masks hide the answer, or you would want a second opinion. Always write
one line of reason in your own words. Took a case by mistake? Press *Release*. Expect 3–5 minutes per case from
the previews, 8–12 with the volumes open; the app measures it and the numbers are revised after twenty cases.

## Stage 2: confirm / overturn / unsure

Same anatomy, same steps, on stage 1's accepts and unsures only, with nothing stage 1 wrote. **Confirm** when the
case is what its type says; **overturn** when it is not; **unsure** when the pictures cannot decide it. One line
of reason. About 2–4 minutes per case.

## Opening a case

**3D Slicer** (macOS 14+ on Apple Silicon, Windows 11). Install the current *Stable Release* from
https://download.slicer.org, then *View > Extensions Manager*: install **SlicerIGT** and **SlicerRT**, restart.
*File > Load Data* on the case's `case.mrb` (or *View > Python Console* and run
`exec(open(r"<case folder>/make_slicer_scene.py").read())`; the app prints the exact line). Paired scenes hold
the CT, masks, the radiograph as a one-slice volume in its true position, and a matching DRR. In *Modules > IGT >
Volume Reslice Driver* set the red slice's driver to the radiograph's transform, mode *Inplane*, and the slice
follows the film's plane through the CT. Film is the background layer, DRR the foreground: drag the foreground
opacity slider to toggle between them.

**ITK-SNAP 4.4** for CT and masks alone (volumes only; it cannot place a radiograph). Installers for macOS Apple
Silicon and Windows x64: http://www.itksnap.org/pmwiki/pmwiki.php?n=Downloads.SNAP4. From the case folder:
`itksnap -g ct.nii.gz -s masks/<mask>.nii.gz -l labels/<labels>.txt` (the app shows it filled in). On a Mac the
binary is `/Applications/ITK-SNAP.app/Contents/bin/itksnap`; on Windows it is under `C:\Program Files\ITK-SNAP 4.4\bin`.

**ImFusion Suite** (paid): Starter licence plus the X-Ray & CT module, EUR 2,100 per user per year, 30-day trial,
Windows / Ubuntu / macOS. Open the CT and import the case's `xr_<view>_P.txt` as the projection matrix (OpenCV
convention, world to pixel, 3 × 4); the film lands on the CT with a live DRR overlay you can nudge. Worth it if
you will do more than a few dozen **paired** cases; not for CT-only cases, which are most of the tree.

## The review app

URL from Greg (a private Hugging Face Space; you must be signed in to an account he added). Log in with the user
name and token he sent, or your own `hf_` token from `hf auth login`. Press **next case**: the app claims the next
case for you (paired cases first) and holds it for three days. Pick a verdict, write the reason, press **Submit
and take the next case**. Your name never appears on the dashboard, and neither reviewer can see the other's answers.
