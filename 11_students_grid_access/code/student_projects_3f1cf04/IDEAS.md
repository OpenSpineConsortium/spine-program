<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path IDEAS.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# Project ideas

A menu, not a syllabus. Each entry is a question the released data can answer, with the
measurement written the way a proposal has to state it (identifiers, axis, unit), a
comparison, a difficulty, and where the idea comes from. Pick one, or bring your own with
the same shape. `/onboard` and `/new-project` in Claude Code will walk you from an entry
here to a proposal pull request.

Identifiers are v10 (`dataset_labels.json`): vertebrae 1–25 (T11 = 18, T12 = 19, L1–L6 =
20–25), sacrum 26, T13 28, S1 29, hips 30/31, femora 32/33, ribs 34–46 left and 47–59
right, lumbar ribs 60/61, hardware 62–68. The manifest carries `sex`, `age`, `position`,
`lstv_vertebral`, `lstv_pelvic`, `castellvi`, `has_l6`, `lumbar_rib`, `hardware_labelled`.
Read `KNOWN_ISSUES.md` first: exclude the 11 hardware records from any gap or distance
measurement, never pool prone and supine for a postural angle, and treat a null Castellvi
grade as ungraded.

Difficulty: **1** a week with the demo as a template; **2** a few weeks, a new measurement
or a second dataset; **3** a semester, usually with a GPU.

---

## A. Straight from the demo (difficulty 1)

**A1. Which pelvic dimension is the most sexually dimorphic?**
The demo found hip joint separation over L4 body width at d = 1.09. Add the pelvic inlet
(minimum left–right distance between the two hip labels 30/31 at the level of the sacral
promontory, mm), the outer bicoxofemoral width, and the bi-iliac width, all divided by the
same body width, and rank them by effect size. Compare female against male, excluding
hardware. Source: the demo's own limitation.

**A2. Does posture change a distance?**
Every distance in the demo should be identical prone and supine; every angle should not.
Measure femoral head distance and L4 body width grouped by `position` instead of `sex`,
then measure L5–S1 lordosis the same way, and show that one moves and the other does not.
Source: KNOWN_ISSUES §4.

**A3. Vertebral body width by level, with its spread.**
The demo measures L4 only. Measure the anterior-slab width of every vertebra 18–25 present,
plot median, interquartile range and 5th–95th percentile by level, and compare with the
level atlas already published on the site. Source: the level atlas.

**A4. Femoral head size and neck length by sex and age.**
Head diameter from the femur labels (32/33, the top 30 mm, mm), neck length as the
distance from head centre to the trochanteric axis. Compare by sex and by decade of age.
Source: the proximal-femur panel in the dataset paper.

## B. Transitional anatomy, the reason the dataset exists (difficulty 1–2)

**B1. Are lumbar ribs and stump twelfth ribs different objects?**
The cohort has 98 records with a stump twelfth rib (length ratio to the eleventh below
0.33) and 16 with a lumbar rib. Measure rib length (mm), the shape of the vertebra each
sits on (transverse-process span, body width-to-depth ratio, pedicle width, all normalised
by the patient's own median across levels), and test whether the two rib classes sit on
morphologically different vertebrae. Source: paper, thoracolumbar section; Du Plessis
2018; Poolman 2023. Difficulty 2.

**B2. Do rib and lumbosacral anomalies co-occur?**
Nagata 2025 reports hypoplastic twelfth ribs with sacralization and lumbar ribs with
lumbarization. The paper tested this on the 33 graded records and found an odds ratio of
2.8 that did not reach significance. Repeat it with `lstv_vertebral` and `lstv_pelvic`
across all 802, with rib length as a continuous variable rather than a threshold. Source:
paper, future directions. Difficulty 1.

**B3. Where does the last lumbar transverse process sit relative to the sacral ala?**
For every record measure the minimum distance (mm) between the transverse process of the
lowest lumbar label and the sacrum label (26) on each side, and its height (mm). Castellvi
grade I is a process over 19 mm high; II touches; III fuses. Plot the distribution and see
whether the 33 graded records fall where the grades say they should. The gallery cases
0268, 0349 and 0033 show what the extremes look like. Source: CASTELLVI_SCREEN_BLIND_SPOT
in the dataset repository. Difficulty 2.

**B4. The nine four-lumbar records: is the fused segment a lumbar-type body?**
In records 0094, 0151, 0156, 0158, 0760, 0785, 0787, 0875 and 1031 the S1 identifier holds
a fused transitional vertebra. Measure the S1 label's height, anterior wedge angle and
width-to-depth ratio in those nine against the other 793 and against L5 in the same
records. Source: paper, future directions; KNOWN_ISSUES §2. Difficulty 2.

**B5. A better S1 carve.**
The S1/S2 split is a plane placed to preserve TotalSegmentator's volume. Design one that
follows anatomy (the S1 superior endplate and the first sacral foramina), apply it to all
802, and report how much sacral slope and pelvic incidence move. Source: paper, future
directions. Difficulty 2–3.

**B6. Six lumbar vertebrae, three readings.**
Eighteen records carry an L6. Is it a true L6, a T12 with aplastic ribs, or a lumbarized
S1? For each, measure the lowest rib-bearing vertebra's shape (T12 versus L1 morphology)
and the L6–sacrum interface, and assign a probability to each reading. Gallery case 1153
is the worked example. Source: paper, introduction. Difficulty 2.

## C. Reference morphometry no one has measured at this size (difficulty 1–2)

**C1. Spinal canal cross-sectional area by level.**
The released canal measure is a diameter. Sum the canal per axial slice (mm²) for
T11–L5, report the distribution, and count how many asymptomatic screening patients fall
under the 100 mm² severe-stenosis threshold. Source: COLLABORATOR_TASKS B3. Difficulty 1.

**C2. Degenerative lumbar scoliosis prevalence.**
Axial rotation of each lumbar body from its principal axes (degrees) and the coronal Cobb
angle between T12 and L5. Prevalence by decade and sex. Source: COLLABORATOR_TASKS B2.
Difficulty 2.

**C3. Sacroiliac joint width and ankylosis.**
The joint space is the gap between the sacrum (26) and each hip (30/31): its median width
(mm) and the fraction of the facing surface with no gap at all. Compare by age and sex.
Source: COLLABORATOR_TASKS B1. Difficulty 2.

**C4. Rib cage geometry.**
Thoracic index, rib angles and chest-wall dimensions from the per-level rib labels,
limited to the levels the field of view carries (T8 down). Normative values by sex and
age. Source: COLLABORATOR_TASKS B4. Difficulty 1–2.

**C5. Pelvic incidence, sacral slope and pelvic tilt from the labels alone.**
Derive the three parameters from the sacral endplate (29) and the femoral head centres
(32/33), compare with the published normal ranges, and report them by position; the
OpenSpineToolkit already implements the geometry. Source: paper, applications. Difficulty
1–2.

**C6. Pedicle width and the screw that fits.**
Pedicle width (mm) at every lumbar level against the standard pedicle-screw diameters;
what fraction of L1 pedicles in this population would not take a 6.5 mm screw? Source:
level atlas, Zindrick 1987. Difficulty 1.

## D. Postural and paired designs (difficulty 2)

**D1. Prone against supine in the same patient.**
351 patients were scanned twice in different positions. Measure lumbar lordosis and
segmental angles in both, and report the within-patient change segment by segment: a
mobility measurement no cross-sectional cohort can make. Needs the paired series, which
the manifest names. Source: ROADMAP, prone/supine. Difficulty 2–3.

## E. Machine learning (difficulty 3, GPU)

**E1. Train a level-numbering model and find where it breaks.**
Train a segmenter on the frozen five-fold splits and report per-level accuracy as a
function of transitional status. The released checkpoints are the baseline. Source:
COLLABORATOR_TASKS C1; the dataset paper's stated purpose.

**E2. T12 versus L1 from shape alone, with a network.**
Plain logistic regression on eleven size-normalised shape features already separates T12
from L1 at AUC 0.99. Train a small 3-D CNN on vertebra crops and see what the image adds
(costal facets, facet-joint orientation). Source: paper, thoracolumbar section.

**E3. Predict trabecular attenuation from geometry.**
The release carries trabecular HU and full 3-D shape per vertebra. Can shape predict
density? Source: COLLABORATOR_TASKS C2.

**E4. Transfer to VerSe.**
Apply the released weights to VerSe to add S1 and the anomaly classes to a bone-kernel
collection, and measure agreement on the VerSe L6 cases. Source: paper, future directions.

## F. Reading projects, no code (difficulty 1)

**F1. A Castellvi read of the whole cohort.**
Only 33 records carry a grade. A student with anatomy training, reading the coronal
reformats of every record with a low L5 transverse process, would let B2 and B3 run at
full power. Pairs with a coding partner who builds the reading sheet. Source: paper,
future directions.

**F2. The gallery, extended.**
The site gallery shows nine records. Find ten more that illustrate a phenotype the
current set lacks (a unilateral lumbar rib, a bilateral grade II, a hip prosthesis with
an intact spine) and write their captions from the labels and the manifest.
