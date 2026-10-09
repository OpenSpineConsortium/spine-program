<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path templates/proposal_template.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# <Project title: a question, stated as a question>

**Student:** <name, program, year>
**Mentor requested:** <name>
**Email for the ClickUp invitation:** <address>
**Dataset:** <name, version, DOI>
**Date:** <YYYY-MM-DD>

## 1. The question

One paragraph. What do you want to know, in whom, and why would a clinician or a modeler
care about the answer? End with the single sentence you hope to be able to write when the
project is done.

## 2. What is already known

Three to five sentences with two to five references. What has been measured before, on what
kind of sample (cadavers, radiographs, CT), and what is missing that this dataset can supply
(scale, both sexes, both postures, the pelvis and spine together, the anomaly classes).

## 3. What will be measured

Be exact. For each measurement: the label identifiers it comes from, the axis or plane it
is measured along, the unit, and how it is normalized. A reviewer should be able to
implement it from this section alone.

| measurement | from identifiers | how | unit |
|---|---|---|---|
| | | | |

## 4. Who is compared

The manifest fields you group by (for example `sex`, `age_band`, `position`,
`castellvi_type`, `has_l6`) and the exclusions you apply and why (hardware, ungraded
Castellvi, records lacking the structure, prone and supine not pooled).

## 5. Analysis plan

The comparison (means with a t test, a regression on age, a correlation), the effect size
you will report, and what figure will carry the result. State the number of records you
expect to analyze after exclusions.

## 6. Outputs

What the finished project delivers: a per-record CSV, one or two figures, a short write-up
(abstract length), and, if it holds up, a poster or a paper section.

## 7. Timeline and milestones

Four to six milestones with dates. These become ClickUp tasks.

| milestone | date |
|---|---|
| environment set up, demo study reproduced | |
| measurement script runs on 10 records | |
| measurement script runs on all records, CSV committed | |
| analysis and figure | |
| write-up draft | |
| final pull request | |

## 8. What could go wrong

Two or three sentences. Which records might break the measurement, and how you will detect
that (a plausibility range, a visual check of the outliers).
