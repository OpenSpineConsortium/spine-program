# VOID: recall vs C-arm angle, scored on the detectors' own selection subjects

**Do not quote any number in this directory.** It is kept so the replacement can be compared with it, and because
`tests/test_eval_gate.py::test_real_arc_leak_every_scored_detector` uses it as the case the gate must refuse.
The replacement is `SchwingNet/results/arc/recall_vs_angle_unseen/`.

## What this is

`recall_vs_angle.{json,md}` and `fig_recall_vs_angle.png`. Written 2026-09-23 16:16 by `tools/arc_recall_eval.py`
(grid job 40419573) on the render set `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep` (job 40419572).
That set is 17 TotalSegmentator subjects swung around the Surgio-B51 arc: lat -90 to +90 in 10-degree steps, tilt
-15, 0 and +15, anchor `case29/AP`, styled under two cards (surgio_b51_dr, elekta_xvi). Four detectors were scored:
dc_P_pooled, dc_A_held_surgio_b51_dr, dc_B_held_surgio_b51_dr_s1 and rx_lodo_carmlspine_1024.
Until this rename the directory was `recall_vs_angle/`. On the grid, `devcorpus_arc/recall_vs_angle/` and the copies
in `or_ready/arc/` were moved the same way by `slurm/arc_unseen.sh` (STAGE=score).

## Why it is void

1. **All 17 subjects were checkpoint-SELECTION subjects for three of the four detectors.** The 17 are s0585 s0970
   s1045 s1062 s1159 s1384 s1535 s1579 s1700 s1836 s1842 s1872 s1880 s1883 s1902 s2033 s2053. They were read from
   `devcorpus/styled/surgio_b51_dr__surgio_b51_dr/STYLE_INFO.json` `val_subjects`. They are exactly the validation
   subjects of dc_P_pooled, dc_A and dc_B. The weights scored were `best.pt`, which Ultralytics keeps by fitness on
   that validation set, and that set held AP, lateral and Cios-geometry renders of these same 17 CTs. They took no
   part in the gradient updates, but they did choose the checkpoint, so they are seen. The arc poses themselves were
   new; the patients were not.
2. **The "real-only" detector was not real-only.** The label was "Real-only LODO, no C-ArmLSpine". But
   rx_lodo_carmlspine_1024 was initialised from `runs/pose/anchor_none_v2_17-1882/weights/best.pt`, which TRAINED on
   renders of s0585, s0970, s1045, s1159 and s1384 and was SELECTED on s1062. Its recall on these renders was about
   zero everywhere, so the leak inflated nothing you could measure. The label was still wrong about what the network
   had seen.

Source: `SchwingNet/results/arc/ARC_CHECK.md` item 4 (grid job 40424737). It is the fourth leak of this kind.

## Why nothing stopped it, and what does now

In that version of the code the check was OPT-IN, and `arc_recall_eval.py` never called it. `tools/holdout.py`
counted only `split == "train"` as seen. Nothing recorded what a checkpoint had been initialised from.

`tools/eval_gate.py` now closes all three gaps. It is called before scoring and refuses this set:
`SeenInEvaluation` for 17 of 17 subjects on dc_P_pooled and dc_A (each in `#val`), and for 6 of 17 on
rx_lodo_carmlspine_1024 through its ancestor anchor_none_v2_17-1882 (5 `#train`, 1 `#val`). See
`SchwingNet/results/eval_gate/smoke_gate/arc17.json` (job 40427457) and the refused run in
`smoke_gate/job_40427586.log`. dc_B is refused the same way (17 of 17 in `#val`): `leaked17` in
`../recall_vs_angle_unseen/subjects.json`. A scan of the training lists that does not use the gate code agrees on
every count (grid job 40429294; `../recall_vs_angle_unseen/recall_vs_angle.md`). The rule is in `docs/DATA_ACCOUNTING.md` s5.2-5.3. An item is held out for a
checkpoint only if its patient is in neither the train nor the val set of that checkpoint, nor of any ancestor in
its initialisation chain.

## What the held-out curve showed about this one (2026-09-24)

The replacement was scored on 40 subjects that no detector, nor anything it was initialised from, trained or was
selected on. The render and the scorer were the same as here.
- Pooled recall at lat 0 is unchanged: 0.87 against 0.89 on Elekta, 0.92 against 0.91 on Surgio.
- The falloff angles are unchanged: about ±30°.
- The lateral end moved UP: Elekta ±90° went from 0.39/0.35 to 0.64/0.69, and Surgio −90° from 0.79 to 0.99.

So the selection leak did not measurably inflate this curve. Its lateral values were lower for a reason that belongs
to its subjects (10 of the 17 were polytrauma CTs). They are still void. The replacement also found that on an arc
set centred on one anchor, another subject's truth boxes alone score about 0.67 body recall at every angle. Numbers
from either curve have to be read against that floor. Details:
`../recall_vs_angle_unseen/recall_vs_angle.md`.

## What still stands from this run

Nothing in the rule depends on the render geometry, so ARC_CHECK.md items 1-3 still hold: the arc span, the sign
convention, and that the JSON matches the figure. The exposure confound also still holds. It belongs to the card:
under surgio_b51_dr the thick lateral view is photon-starved mottle and the spine cannot be seen. The recall values
and falloff angles do not stand.
