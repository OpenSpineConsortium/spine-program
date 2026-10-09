# spinesurg-ct-nnunet

Part of the [OpenSpineConsortium](https://openspineconsortium.com) · dataset
[CTSpinoPelvic1K](https://huggingface.co/datasets/gschwing/CTSpinoPelvic1K) · this repository is private
while it holds the FluoroCap harvest code; the feasibility line of work below is written to be readable
when it is not.

---

Wrong-level surgery is a never event that still happens, and the established way to prevent it — register the
patient's intraoperative image to a preoperative 3-D scan — imports the level identity from that scan rather than
reading it off the image. This repository asks whether a C-arm alone is enough: expose, detect the bodies, link
consecutive frames, chain them into one panorama, count from an anatomical anchor, and confirm by placing the
instrument frame back on the chain.

![Figure 1](paper/rsnai/figures/fig1_story.png)

*Expose, detect, link, chain, count, confirm. Only the shaded boxes are learned; the rest is geometry. Row (b) is a
real sweep counted from the sacral anchor. Row (c) places an instrument frame on that chain and reads L2 —
correctly — with a correlation margin of 0.18 over being one body off. Row (f) does the same on frames styled by a
fitted Siemens Cios Fusion card and finds a sixth lumbar vertebra, the anomaly that makes counting fail in practice.
Row (d) renders when its job finishes.*

---

## Preliminary results

Every number here is verified against a file on disk by `tools/claims_check.py` reading `docs/RSNAI_CLAIMS.json`;
54 claims, each with the path and the field it was read from. A number that moves fails the check.

### Naming the level on real intraoperative C-arm frames

Five-fold cross-validation over 141 cases and 617 vertebrae, split by case.

| | exact level | within one |
|---|---:|---:|
| lateral, whole frame | **98.22 %** | 100 % |
| AP, whole frame | **96.67 %** | 100 % |
| lateral, five vertebrae in the field | 97.00 % | — |
| lateral, three vertebrae in the field | 92.86 % | — |
| lateral, one vertebra in the field | 72.85 % | 90.23 % |
| **zero-shot**, lateral — no data from this collection in training | **96.27 %** | — |
| zero-shot, AP | 37.88 % | — |

95 % case-bootstrap confidence interval on the lateral whole-frame figure: lower bound 95.71 %. Frames within a
case are not independent; a naive interval covers 70.8 % of the time (measured, `tools/test_stats_compare.py`), so
every interval in this repository is clustered at the case.

### Naming the level on plain radiographs, held out by patient

| | exact level | n |
|---|---:|---:|
| CSXA cervical, random 2–9 vertebra window | **99.87 %** | 3,720 |
| BUU-LSPINE lumbar, random window | **98.04 %** | 2,698 |
| BUU-LSPINE, only three vertebrae visible | 94.89 % | — |

### Where this is behind, stated first rather than buried

Detection, not naming, is the binding constraint. On a device held out entirely, per-body recall is **90.6 %**
(whole-vertebra outline truth, IoU 0.5, confidence 0.25) and the sacrum is found in 83.9 % of frames. Published
class-agnostic C-arm detection reaches 0.96–0.98. Recall compounds over eight to twelve bodies, so 90.6 % is not
counting-grade.

A detector trained on 6,650 renders and no real image reaches **71.67 %** per-body recall on real radiographs
against **99.14 %** for the same architecture trained on real film. That ~28-point simulation-to-reality tax
matches what the field reports elsewhere almost exactly.

The same predictions score 5.2 % against vertebral-*body* truth. That is a box-convention mismatch, not a failure,
and it is reported because a reader who saw only the 90.6 % would have no way to know the convention mattered.

---

## How this repository tries not to fool itself

The recurring failure mode in this work is a number that is wrong but plausible. Several estimators have produced
finite, reasonable-looking values from the wrong bone, the wrong surface, or the wrong label map, and none of them
raised an error. Internal consistency caught none of them. What follows is the machinery built in response.

### 1. Every claim is bound to the file that produced it

`docs/RSNAI_CLAIMS.json` holds one record per published number: an id, the expected value, the file and JSON path
it is read from, a tolerance, and prose describing what it measures. `tools/claims_check.py` re-reads every source
and fails if any value has moved. `tools/claims_fill.py` writes the numbers into the manuscript, so a figure in the
text cannot disagree with the file it came from.

Generated documents are generated, never hand-maintained. `docs/DEVICE_PARAM_AUDIT.md`,
`docs/DEVICE_SPREAD_SWEEP.md` and `docs/CT_INVENTORY.md` are written by their tools from the underlying cards and
data, so they cannot drift from the code they describe.

### 2. One split, drawn over people, and it refuses rather than warns

A train/validation split drawn per source directory puts one person on both sides when two directories name them
differently — and no score can reveal it. This happened twice here before it was caught:

- **NHANES II.** One bank carried the films as `nhanes_00160`, another as `NH_00160_c`. In three successive banks,
  48 of 54 validation patients had their other copy in training.
- **CTSpinoPelvic1K.** One bank named a case by its nnU-Net stem, another by its release id, tied only by a
  symlink. 371 people sat on both sides of the split; 357 of them purely because of the naming.

The fix is structural, not a patch. `tools/patient_keys.py` resolves one key per *person* across every naming
scheme; `tools/make_context_crops.py` takes that key file, draws **one** split over people across all sources,
records the key file in the bank's metadata, **refuses** any case it cannot key, and exits non-zero if any person
still appears on both sides. `tools/test_patient_keys.py` asserts that both historical defects collapse.

Synthetic data inherits its source's split. A rendered or styled frame is never on the opposite side from the CT it
came from, and geometries are not mixed across training and test — verified by comparing the recorded validation
subjects of every styled corpus.

### 3. Content-addressed data accounting, proved on a corpus with a planted leak

`tools/data_ledger.py` walks every image, render, crop and volume and records content hashes — byte hash, pixel
hash, volume hash, and a perceptual hash — so that the same data under two names is detectable regardless of
filename. `tools/data_alias.py` groups those into canonical items; `tools/data_lineage.py` builds the graph from
source collection to trained model; `tools/leak_check.py` runs the checks across that graph and writes a report;
`tools/fig_data_flow.py` draws it.

The chain is not trusted because it runs. `tools/diagnostics/make_fake_corpus.py` builds a small synthetic corpus
with a **planted** leak — the NHANES defect in miniature, one person present under two names in opposite splits,
byte-identical — and a matching clean corpus. The leaking tree must make the chain exit non-zero and the clean tree
must make it pass. A leak detector that has never caught a leak is an untested leak detector.

Aliased datasets are handled explicitly: a vendor release and a de-identified subset of the *same* acquisitions are
one dataset in two representations and are never counted as two.

### 4. Statistics that respect the unit of independence

`tools/stats_compare.py` provides case-level (cluster) bootstrap intervals, paired bootstrap comparisons, McNemar
and permutation tests, with Holm/BH correction across families. The naive alternative was measured against it: a
naive 95 % interval on this data covers 70.8 % of the time. Its own behaviour is asserted in
`tools/test_stats_compare.py`.

### 5. A pre-registered benchmark protocol, written before any comparator ran

`docs/BENCHMARK_PROTOCOL.md` was written before results existed, so the design could not be chosen after seeing the
numbers. It fixes: the same cases by patient key, one truth per axis made independently, the same metric, the same
training budget where an arm is retrained, operating points frozen on validation, and — the rule that costs
something — **a comparator that cannot run is reported as unable to run, with the reason, never as a zero and never
omitted.** The registration-based arm is reported as a *ceiling*, not a rival: it is given the patient's own 3-D
scan, which this method is not.

The CT axis covers every collection here by distinct subject, not one convenient collection
(`tools/ct_inventory.py` → `docs/CT_INVENTORY.md`). Collections whose truth is pseudolabelled are reported as
coverage and failure counts only; they cannot support a claim of beating the tool that produced their labels.

### 6. Two device designs, because they answer different questions

A **pooled** detector trains on every C-arm and is tested on a holdout spanning every device — the deployable case.
A **leave-one-device-out** detector never sees the test device at all — the harder question, and the one a
regulatory reviewer asks. Both are reported and the pooled number is never quoted without the LODO number beside
it. The list builder refuses to write its lists if a CT subject or a real specimen falls on two sides of the split.

### 7. Image formation is fitted physics, and the fit is audited

Each C-arm is described by a card of physical terms fitted to real paired frames, with held-out coverage measured
per device. `tools/device_param_audit.py` generates a table naming, for all 114 device × parameter pairs, where the
value came from (DICOM header, fitted per frame, fitted global, physics default), how many real frames stand behind
it, whether a rendered frame draws it or holds it fixed, and what the draw is conditioned on. It also names the
DICOM tags this machine holds that the renderer does **not** consume, with the reason for each.

That audit found a real defect. A clip intended to prevent implausible draws was a marginal operation applied to
8–11 correlated terms at once, and it saturated rather than truncated — an out-of-band draw was pinned to the
boundary value, not redrawn. Measured exactly under each card's own fitted correlation: a styled frame reached
**1.7 %–5.1 %** of its device's fitted joint distribution, and **94.9 %–98.3 %** of styled frames carried at least
one pinned term. The replacement keeps every marginal and rejects only atypical *combinations*, using the same
statistic each card is already validated against; it reaches 99 % of the joint distribution, and
`tools/test_device_gate.py` asserts that it preserves the marginals it claims to.

**It is implemented and not adopted.** A sampler that reaches more of the distribution is not automatically better
training data, so the default is unchanged until an A/B on real frames decides it. This repository does not adopt a
change on the strength of the argument for it.

### 8. Look at the image

Two of the defects above were invisible in the numbers and obvious in one rendering. The clipped kilovoltage
histogram is a set of stacked spikes rather than a narrowed distribution; three analytically reasonable fixes to an
earlier measurement were all wrong in ways only a rendered mask revealed. Rendering the thing is part of the
method, not a courtesy to the reader.

### 9. Everything heavy runs as a batch job, and says where its answer lands

No analysis runs on a login node. Each stage is a Slurm script under `slurm/` that writes a named output and a
completion marker, so a resumed session can compute what is done, running, ready and blocked from the disk rather
than from memory.

---

## Reproducing

```
tools/claims_check.py                     # every published number against its source file
tools/test_patient_keys.py                # both historical split leaks collapse under the keyer
tools/test_stats_compare.py               # interval coverage, including the naive baseline that fails
tools/test_leak_check.py                  # the leak checks themselves
tools/test_device_gate.py                 # the sampler preserves the marginals it claims to
tools/diagnostics/make_fake_corpus.py     # build a corpus with a planted leak, then run the accounting chain
```

`docs/RESUME_2026-09-22_PM.md` carries the current state: what is running, where each answer lands, what was found,
and what is still open.

## Layout

```
tools/          analysis, rendering, audit and figure code; every file's docstring says why it exists
slurm/          one batch script per stage, each naming its output and its completion marker
docs/           generated audits, the benchmark protocol, the claims file, resume notes
paper/rsnai/    the manuscript and its figures
benchmark/      comparator systems mapped by name into a shared label space
```

## Standing caveats

- Numbers from the level banks built before the split fix should not be quoted; the clean rebuild supersedes them.
- Whether a CTSpinoPelvic1K release id denotes one person is **under audit**: the source collection scans each
  patient prone and supine, and if two ids are one person the corpus is mis-split. This is written down rather than
  assumed away.
- `docs/SPINOPELVIC_ESTIMATOR.md` records an unexplained failure in 128 records rather than a guess at its cause.
  That is the preferred form here.
