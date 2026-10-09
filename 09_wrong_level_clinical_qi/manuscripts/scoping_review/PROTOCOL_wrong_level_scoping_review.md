# Protocol: wrong-level and wrong-site spine surgery — mechanisms, the imaging step that fails, and decision support

**A scoping review, reported to PRISMA-ScR.**

**Version 1.0, 15 September 2026.** Written for the review team.

---

## Declaration about this protocol, first, because it governs how everything below may be reported

**This protocol was written after the searches were run and after a first descriptive count of the corpus was
produced.** It is therefore a *post hoc* protocol. It is dated, versioned and filed before any study is charted
into the final extraction table, before any human screening decision is recorded, and before the manuscript is
drafted, but it was not registered prospectively and must never be presented as though it were. PRISMA-ScR item 2
asks whether a protocol exists and where it can be accessed; the answer this review will give is: *a protocol was
prepared after the initial searches, is available as a supplement, and was not prospectively registered*. The
first count that preceded it is reported in the Results as a preliminary count and its numbers are superseded by
the charted table.

Two consequences follow, and both are accepted here rather than argued away:

1. **The search strategy cannot be presented as a hypothesis-blind design.** It was built to serve an engineering
   project and then repurposed. The Limitations section says so.
2. **No outcome may be described as pre-specified.** Everything in the synthesis is descriptive and exploratory.

Registration on the Open Science Framework is intended before submission, with the same declaration attached.
Prospective registration is not claimed retroactively.

---

## 1. Rationale

Operating on the wrong vertebral level is the archetypal never-event of spine surgery, and unlike most
never-events its proximate cause is usually an *imaging* step rather than a marking or consent step: somebody
counts vertebrae on an image, and the count is wrong. Two facts make the count fragile. About one person in six
has a lumbosacral transitional vertebra, and a smaller share has a numerical variant — 23 or 25 presacral
segments — which cannot be recognised at all without imaging that spans the whole spine. And the accuracy of the
call falls sharply with the modality used to make it: against a full reference standard, blinded readers detect a
transitional vertebra on CT with about 76% sensitivity and substantial agreement, on MRI with about 54%, and on
conventional radiographs with about 32% and agreement of 0.16 to 0.32.

The prevention literature, by contrast, is weighted toward process controls. In a preliminary count over 1,678
passages drawn from 529 works in this corpus, a surgical time-out or protocol was named in 144 passages and
navigation or computer assistance in 83, while counting from a fixed landmark appeared in 26, an intraoperative
radiograph with a marker in 8, and comparing against the preoperative study in 3. If that asymmetry survives
charting, it is the review's central observation: the controls the field reaches for are organisational, while
the failure it is trying to prevent is radiological.

No published map of this literature exists that holds the three strands — event frequency, the imaging step, and
the anatomical variant — in one frame. That is the gap this review fills.

## 2. Review question and objectives

**Primary question.** In spine surgery and spinal intervention, what does the literature report about wrong-level
and wrong-site events: how often they occur, by what mechanism, at which imaging step the level determination
fails, and what has been proposed or tested to prevent them?

**Objectives.**

1. Map the reported frequency of wrong-level and wrong-site events by setting, region and era, and identify the
   subset of reports with an extractable numerator and denominator.
2. Chart the mechanisms named by authors, distinguishing an anatomical cause (transitional or numerical variant,
   deformity, prior surgery, habitus) from a process cause (communication, documentation, time-out) and from an
   imaging cause (misread, marker failure, poor visualisation, level lost between studies).
3. Chart the imaging modality and the counting convention used to determine level, and where authors state a
   reference standard, record it.
4. Chart proposed and evaluated countermeasures, and record for each whether it was evaluated against an outcome,
   against surgeon confidence, or only proposed.
5. Identify what is missing: which questions the literature cannot currently answer, and what data would answer
   them.

**Why a scoping review rather than a systematic review.** The question is broad, the designs are heterogeneous
(case reports, registries, closed-claims series, surveys, technical evaluations), and much of the evidence is
descriptive. A scoping review is the correct instrument for mapping such a field and for stating what cannot yet
be synthesised. A quantitative synthesis is planned only for the narrow subset described in section 8, and is
labelled as such.

## 3. Eligibility criteria

**Population.** Human patients undergoing spine surgery or an image-guided spinal intervention, or human imaging
studies whose subject is vertebral enumeration or transitional anatomy.

**Concept.** Any of: a wrong-level, wrong-site or incorrect-level event; its frequency; its mechanism; the imaging
step by which the operative level was determined; the accuracy or reliability of vertebral enumeration; a method
intended to prevent a level error, including transitional-vertebra detection, numbering conventions, intraoperative
localisation and computer-assisted labelling.

**Context.** Any country, any care setting, any year. Any language, provided an English title and abstract exist.

**Include** primary studies of any design, case reports and series, registry and closed-claims analyses, surveys,
technical evaluations with a clinical claim, and systematic or narrative reviews (reviews are charted separately
and are not counted as primary evidence).

**Exclude** animal-only or cadaver-only work with no clinical claim; wrong-site surgery outside the spine;
technical imaging papers with no level-determination claim; editorials, letters and commentary without data; and
records for which neither an abstract nor full text can be retrieved.

## 4. Information sources

1. **Europe PMC full text**, searched with the transitional-anatomy and wrong-level query (section 5), restricted
   to records carrying full text. Search executed 15 September 2026; 6,007 records.
2. **Semantic Scholar**, bulk search over the same concepts, adding records without Europe PMC full text.
   Executed 15 September 2026; 6,287 records before deduplication against source 1.
3. **Reference and citation expansion** from the transitional-anatomy seed papers, through the same interface.

Sources 1 and 2 are deduplicated by PubMed Central identifier, then digital object identifier, then normalised
title. Two further corpora exist in this project — a fluoroscopy corpus of 158,955 records and a pathology corpus
— and are **not** part of this review's search; their overlap with the included set is reported for transparency
only.

**Known coverage limits, stated here rather than discovered later.** A full-text-restricted Europe PMC query
under-covers closed-access journals, and several of the field's most cited series sit in journals whose full text
is not open. Semantic Scholar partly compensates but supplies abstracts rather than full text for many records.
No hand-search of conference proceedings, no grey literature search, and no contact with authors is planned.

## 5. Search strategy

The executed query, verbatim, is reproduced in Appendix A of the manuscript and in the repository as the constant
`QUERY_EXTRA` in `tools/fluorocap.py`. Its three blocks are combined with AND: a variant-and-error block (wrong
level, wrong site, incorrect level, lumbosacral transitional, transitional vertebra, Castellvi, Bertolotti,
sacralization, lumbarization, sixth lumbar, L6 vertebra, thoracolumbar transitional, 13th rib, thirteenth rib,
lumbar rib, cervical rib, eleven ribs, hemivertebra, block vertebra, Klippel-Feil, numerical variant, vertebral
numbering, level localization, level verification, plus Spanish, Italian, German, Japanese and Chinese
equivalents); an imaging block (radiograph, x-ray, fluoroscopy, C-arm, roentgen, plain film, intraoperative); and
a spine block (spine, spinal, vertebra, lumbar, lumbosacral, thoracolumbar, cervical).

## 6. Selection process

Screening is **machine-assisted**, and this review's methodological obligation is to measure that rather than to
present it as equivalent to dual human screening.

**Stage 1, automated.** Every record is screened by explicit, published patterns over title, abstract and, where
retrieved, full text. Each decision is recorded with its reason and the exact strings that triggered it, in
`screening.jsonl`. No record is excluded by a model whose reasoning cannot be inspected.

**Stage 2, human validation of the automated screen.** A random sample of 200 records, stratified as 100 included
and 100 excluded, is screened independently by two human reviewers blinded to the automated decision. From this
sample the review reports the automated screen's sensitivity and specificity against the human decision, with
exact binomial confidence intervals, and the agreement between the two human reviewers as Cohen's kappa.
**No screening performance may be claimed until this sample is complete.** If sensitivity is below 0.90 the
automated screen is revised and the whole corpus is re-screened, and both passes are reported.

**Stage 3, human charting.** Every record that reaches extraction is read by a human reviewer, who confirms
eligibility and completes the charting form. Disagreement is resolved by discussion with a third reviewer. The
automated extraction (section 7) supplies a pre-filled draft; the human reviewer's entry is the record of truth,
and the fraction of automated fields corrected is reported.

## 7. Data charting

Charting is piloted on 20 records by two reviewers before the full pass, and the form is revised if the pilot
shows ambiguity. Items:

- Identifiers: record identifier, source, year, journal, country, care setting.
- Design: case report, case series, cohort, registry or claims analysis, survey, technical evaluation, review.
- Denominator: patients or procedures, and the interval covered.
- Numerator: wrong-level or wrong-site events, and the definition the authors used.
- Reported frequency, verbatim, with its denominator.
- Spinal region.
- Transitional or numerical anatomy: implicated, present but not implicated, not mentioned.
- Mechanism, coded to the named list, with the source sentence.
- Imaging modality used to determine level, the counting convention, and any reference standard.
- Countermeasure, coded to the named list, and its evaluation status: outcome-evaluated, confidence-evaluated,
  proposed only.
- For every coded field: whether the value was explicit, inferred, or absent.

Every extracted field carries the sentence it came from, so that a claim and its source stay together.

## 8. Synthesis

**Descriptive mapping** is the primary output: counts and cross-tabulations of design, region, mechanism,
imaging step and countermeasure, with the evaluation status of each countermeasure shown alongside it.

**Quantitative synthesis is restricted** to records with both a numerator and a denominator and a definition of
the event. For those, a random-effects synthesis of proportions on the logit scale, with a Freeman-Tukey
sensitivity analysis, heterogeneity reported as tau-squared and I-squared, and prediction intervals rather than
confidence intervals alone. Pre-specified subgroups: region (cervical, thoracic, lumbar), design (registry or
claims versus institutional series), and era (before and after 2010).

**A pooled incidence will be reported only if it is defensible.** Denominators in this literature range from a
single institution's consecutive series to national claims databases, event definitions differ, and ascertainment
is systematically incomplete for an event that is under-reported by construction. If heterogeneity or definitional
inconsistency makes a pooled figure misleading, the review reports the range and the studies, and says why it did
not pool. That decision, and its reasoning, is reported either way.

**No quality or risk-of-bias assessment** is performed, in keeping with PRISMA-ScR, which does not require it. The
consequence — that this review maps what has been claimed, not what is true — is stated in the Limitations.

## 9. Reporting

PRISMA-ScR checklist completed and submitted as a supplement. Flow diagram in PRISMA 2020 form, generated from the
screening ledger, with the counts for each source, deduplication, automated exclusion by reason, full text sought
and not retrieved, and inclusion. All code, the executed queries, the screening ledger and the charting table are
released with the manuscript.

## 10. Roles and contributions

Two human reviewers for the validation sample and for charting; a third for disagreements; one author responsible
for the corpus, the screening code and the analysis. Contributions to be recorded by CRediT taxonomy. Machine
assistance in screening and first-pass extraction is described in the Methods, not only acknowledged.

## 11. Amendments

Any change after this version is recorded in a dated amendment table in the supplement, with its reason and
whether it preceded or followed the charting of any record.

---

## Appendix: what this review can and cannot support

It can establish what the literature reports about the frequency, mechanisms and imaging failures of wrong-level
surgery, and where the evidence is thin. It can show whether the prevention literature addresses the step that
fails.

It cannot establish that any particular method, including one developed by the authors, is superior. A scoping
review maps claims; it does not compare interventions, and it applies no risk-of-bias assessment. A claim of
superiority requires a benchmark against named comparators on data the comparator's authors did not choose, with
a reference standard defined before the comparison. That is a separate study, and this review's role toward it is
to define the gap and the performance envelope it would have to beat.
