---
title: Assisted Level Naming
emoji: "🩻"
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
hf_oauth: true
---

# Assisted vertebral level naming — a reader study

Surgeons name the vertebra in a limited-field radiograph twice: once unaided, and once with an automatic
system's suggestion shown. The films, the answers and every read live in **private** dataset repositories;
this Space holds no model, no weights and no naming algorithm — only the form and the arithmetic.

## The question

Not "is the software accurate", which is measured elsewhere, but **is a surgeon more accurate with it than
without it** — which is the only claim that matters in theatre. The published comparator is a surgeon with
a CT-registration overlay at 97.6% against 69.6% unaided; both are human-plus-machine figures, and no
machine-alone accuracy answers them.

## The design, and its one confound

Two blocks: every film unaided, then every film again with the suggestion, reordered. Unaided must come
first because a reader who has seen a suggestion cannot un-see it — which means the assisted block also
carries any learning from the first, and the assisted figure is therefore an **upper bound** on the aid's
contribution. A crossover with two matched film sets and twice the readers would separate them.

## What it reports

Unaided accuracy for this group, assisted accuracy, and the two paired cells that decide it: **rescued**
(wrong alone, right with the aid) and **harmed** (right alone, wrong with the aid), tested with McNemar's
exact test. Harm is the number this class of aid usually does not report. Confidence and reading time are
recorded too: an aid that makes readers surer without making them righter is a hazard, and one that doubles
reading time may not be usable.

Readers are never shown the correct answer.
