<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path examples/proposal_example/proposal.md. Copied 2026-10-08. Redactions applied by kind: lead address (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# Is relative pelvic width different between females and males, and by how much?

**Student:** Gregory Schwing (worked example for the onboarding primer)
**Mentor requested:** Gregory Schwing
**Email for the ClickUp invitation:** [the lead's university address]
**Dataset:** CTSpinoPelvic1K v10, https://doi.org/10.5281/zenodo.22642578
**Date:** 2026-09-07

## 1. The question

The female pelvis is wider than the male pelvis; every anatomy text says so, and forensic
anthropology sexes skeletons on it. What the texts rarely give is the size of the
difference in living adults measured the same way on the same scanner protocol, and whether
it survives normalization to the rest of the skeleton. CTSpinoPelvic1K labels both femora and
every lumbar vertebra on one coordinate frame in 802 adults, so how far apart the hip joints
sit, and the size of the skeleton they sit on, are available in every record. The sentence I
hope to write: "Relative to vertebral body width, the female hip joints sit X percent further
apart than the male, with an effect size of d, in about 730 adults over 50."

## 2. What is already known

Pelvic sexual dimorphism is the most reliable skeletal sex indicator, with the greater
sciatic notch, subpubic angle and iliac flare the classic features (Phenice 1969; Bruzek
2002). CT-based studies report bi-iliac and inlet widths larger in females by roughly 5 to
10 percent, mostly in samples of a few hundred (Tague 1989 on skeletal remains; Franklin
2014 and Decker 2011 on CT). Few normalize to a co-registered structure of the same
skeleton, and none that I know of use a single-protocol cohort of this size with the sacrum
segmented separately.

## 3. What will be measured

| measurement | from identifiers | how | unit |
|---|---|---|---|
| bi-iliac width (the naive comparison) | 30 (left hip), 31 (right hip) | left–right extent of the union of both hip labels, along the axis the affine marks L/R | mm |
| femoral head centre | 32 (left femur), 33 (right femur) | centroid of the medial-most 28 mm of the top 30 mm of each femur label: the head, not the greater trochanter | mm, world coordinates |
| femoral head distance | 32, 33 | Euclidean distance between the two head centres (the bicoxofemoral axis) | mm |
| outer width on that axis | 32, 33 | the bicoxofemoral line extended outward through each femur mask to its last voxel, outer edge to outer edge | mm |
| vertebral body width | 23 (L4), else 24 (L5) | left–right extent of the anterior 18 mm of the vertebra label, which is the body without the transverse processes or facets | mm |
| relative hip separation | 32, 33, 23 | femoral head distance divided by vertebral body width | none |

Extents are voxel counts along an axis times the voxel size on that axis; axes and their
directions are read from each file's affine, never assumed. The bi-iliac width is kept as
the first thing anyone would try, so the write-up can show why it fails.

## 4. Who is compared

Grouped by `sex` from `manifest.json` (393 female, 345 male; 11 "other" and 53 missing are
listed in the CSV and excluded from the test). Excluded: the 11 records with surgical
hardware (`hardware_labelled`), because eight carry hip arthroplasties, and any record
lacking either femoral head or an L4/L5 label. Prone and supine records are pooled for
distances measured between bones, which posture does not change; the CSV keeps `position`
so that claim can be checked.

## 5. Analysis plan

Means, medians and standard deviations by sex for every measurement; Welch's t test and
Cohen's d for the relative hip separation; a three-panel box-and-dot figure (pelvis width
absolute, hip joint separation absolute, separation relative to skeletal size). The
expectation from the literature is that the absolute separation differs little between the
sexes while the male skeleton is larger, so the relative separation is higher in females.
If that holds, a secondary check regresses relative separation on age within each sex.
About 730 records analyzed after exclusions.

## 6. Outputs

`results/pelvic_width.csv` (one row per record), `results/report.txt`,
`results/pelvic_width.png`, and a 250-word write-up in `WRITEUP.md`. If the effect holds,
an abstract for the medical student research day.

## 7. Timeline and milestones

| milestone | date |
|---|---|
| environment set up, demo study reproduced | 2026-09-14 |
| measurement script runs on 10 records | 2026-09-21 |
| measurement script runs on all records, CSV committed | 2026-09-28 |
| analysis and figure | 2026-10-05 |
| write-up draft | 2026-10-12 |
| final pull request | 2026-10-19 |

## 8. What could go wrong

A femur label cut by the field of view below the head would still carry the head, but a
femur absent altogether removes the record; I will report how many. A head centroid pulled
toward the trochanter would inflate the separation, so I will check the head distances
against the 150 to 190 mm range and look at every outlier. The body-width proxy runs about
5 mm wider than the release's endplate widths on a validation sample; the ratio, not the
absolute width, is the endpoint, and the proxy is applied identically to both sexes.
