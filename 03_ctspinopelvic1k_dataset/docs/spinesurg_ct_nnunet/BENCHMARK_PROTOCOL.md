# Head-to-head protocol: the same scans, the same truth, the same metric

Written 2026-09-22, before any comparator was run, so that the design cannot be chosen after seeing the numbers.
Every arm below is scored on the SAME cases with the SAME truth and the SAME metric; where a comparator cannot be
run at all, that is recorded as a fact about the comparator rather than converted into a favourable number.

## The rule that makes it fair

1. **Same cases.** Each axis names a fixed case list, by patient key, written to a file before the runs.
2. **Same truth.** One truth per axis, made once, independent of every arm.
3. **Same metric.** Per-body detection recall and precision at a matched box convention, and per-body counting
   correctness; both with case-level bootstrap intervals, because frames within a case are not independent (the
   measured cost of ignoring this: a naive 95 % interval covers 70.8 %, `tools/test_stats_compare.py`).
4. **Same budget where an arm is retrained.** Identical training data, identical schedule, identical
   initialisation policy, one seed per arm at minimum and three where the arm is cheap.
5. **A comparator that cannot run is reported as such**, with the reason (no weights, no code, needs an input this
   setting does not have), never as a zero and never omitted.
6. **Nothing is tuned on the test split.** Operating points are chosen on validation and frozen; the frozen value
   is written into the protocol file before scoring.

## Axis 1 — detection and counting on real intraoperative C-arm frames

The paper's claim. Cases: the C-ArmLSpine intraoperative series, truth from the registered cone-beam CT labelled
by two independent segmentation tools, scoring only levels the two agree on.

| Arm | What it needs | Status |
|---|---|---|
| ours, POOLED: one detector over every device (design P), tested on every device's real test split | a labelled frame set from each device in the fleet | to run — the deployable case |
| ours: detector trained leave-one-device-out on the physics-styled corpus | no data from the test device | to run |
| a detector trained on this device's own real frames | labelled frames from the target device | have (same-device control) |
| a detector trained on real plain film only | film corpus | have (cross-domain control) |
| a detector trained on naive renders only | CT renders | have: 71.7 % per-body recall on real film against 99.1 % for the film-trained one |
| published architectures retrained on OUR data: YOLOv8, RT-DETR, Faster R-CNN | same training set and schedule | to run — this is the architecture-versus-data test |
| 3-D-to-2-D registration to the patient's own scan (the LevelCheck route) | a preoperative or intraoperative 3-D scan of the same patient | to run, and its requirement is the point: it is the clinical state of the art and it costs a CT |

The registration arm is a CEILING, not a rival: it is given the patient's own 3-D scan, which our method is not.
Reporting it honestly is what makes the comparison unarguable — "this is what the established route achieves, this
is what it needs, and here is what we achieve without it".

The pooled arm and the leave-one-device-out arm answer DIFFERENT questions and neither substitutes for the other.
Pooled: every device in the fleet is represented in training, which is the deployable case for a vendor who can
collect frames from each unit it ships to; its test split is disjoint by SPECIMEN, and `devcorpus_build.py lists
--design P` refuses to write the lists if a specimen or a CT subject falls on two sides. Leave-one-device-out: the
model meets a machine that did not exist when it was trained, which is the harder question and the one a regulatory
submission is asked. Both are reported, with the pooled number never quoted without the LODO number beside it.

## Axis 2 — vertebra naming on plain radiographs

Cases: the held-out plain-film corpora, split by patient. Comparators: published open film models (VertXNet,
SpineCLUE and any other that ships weights), run unmodified on the same films, scored with our metric. Published
numbers that cannot be reproduced on these films are quoted separately and labelled not metric-comparable, with
the reason.

## Axis 3 — the dataset itself, on every CT here, not one collection

Cases: every CT collection on this machine, by distinct subject, as `tools/ct_inventory.py` counts them
(`docs/CT_INVENTORY.md`). Written 2026-09-22 to replace an earlier version of this axis that named only the 802
CTSpinoPelvic1K records; those are abdominopelvic and see the lower spine alone, so scoring a whole-spine counting
claim on them understates both the anatomy the method meets and the number of scans behind it.

| collection | distinct subjects | truth | what it adds |
|---|---:|---|---|
| CTSpinoPelvic1K | 801 | release labels, per level + ribs + pelvis | the lumbosacral junction, and the transitional cases |
| TotalSegmentator v2 | 1,170 | TS labels mapped by name | whole body, wide anatomy range |
| TotalSegmentator v3 | 1,735 | TS v3 labels mapped by name | as above, larger and more recent |
| VerSe 19/20 | 374 | VerSe masks, C1-L6 | the only whole-spine collection with named cervical levels |
| C-ArmLSpine | 120 | SPINEPS + TotalSegmentator agreement | intraoperative CBCT, the deployment anatomy |
| AASCE | 457 | pseudolabels | scoliotic spines |
| SpinalAI | 44 | pseudolabels | few subjects, heavy pose multiplication -- reported separately |

Comparators already staged in `benchmark/`: TotalSegmentator v2, SPINEPS + VERIDAH, VISTA3D lineage, RibSeg v2, each
mapped BY NAME into the one-shot label space (`benchmark/mappings/<system>.json`) and scored with the same two scorers
as our folds. The axis is scored per collection AND pooled, because a pooled number over collections of unequal size
hides which one carries it.

Two honesty conditions specific to this axis. A collection whose truth is pseudolabelled cannot be used to claim we
beat the tool that produced the pseudolabels, so AASCE and SpinalAI are reported as coverage and failure counts only,
never as an accuracy comparison. And the subject counts above are NOT additive: several render banks hold the same
collection, so the case list is drawn on patient keys over the union (`tools/patient_keys.py`).

## Axis 4 — the anomalous cases, where counting actually fails

Cases: the transitional spines (sixth lumbar vertebra, thirteenth thoracic). Every arm above, scored on this
subset alone, because a method that is excellent on ordinary anatomy and fails on the anomaly is worth less in
this application than its headline number suggests.

## What gets reported either way

- A table of every arm on every axis, with intervals and the paired test against ours.
- Every arm that could not run, and why.
- Every axis on which ours is NOT ahead, stated in the text rather than left for a reviewer to find.
- The protocol file, the case lists by patient key, the frozen operating points, and the commit that produced
  each number.
