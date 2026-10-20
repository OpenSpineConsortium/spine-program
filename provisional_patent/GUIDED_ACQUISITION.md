# Guided acquisition: telling the operator where to move, and leaving a mark that stays

Everything else in this project answers *what is this vertebra* from pictures already taken. This runs the
other way: the system holds the run as it is being built, and when it cannot be sure it computes **how far
the imaging device must travel**, in millimetres, and says so — once as a sentence for a person, once as a
vector for a gantry.

---

## STATUS — 2026-09-18, end of session

**Read this first.** Everything below it is the design; this is where the work actually stands.

| | |
|---|---|
| the engine, the orientation, `plan_run`, the fiducial | **built** |
| unit tests (`python tests/test_acquisition.py`) | **all passing**, deterministic under `PYTHONHASHSEED=random` |
| the operator's console (`tools/guided_console.py`) | **built**, never run on real images |
| measurement on the render corpus | **running** — grid job **40376577** |
| any corpus number | **none is trustworthy yet. Do not quote one.** |

### What to do when you come back

```bash
ssh go2432@grid.wayne.edu
tail -60 ~/model_night/logs/guided_40376577.out     # start here
python tools/pipeline_state.py                       # guided_calibrate, guided_validate
```

**Check the control first.** The `frame` arm must land near what `sweep_map` publishes for a single frame on
this corpus — about 85 % at three vertebrae. It is the only quantity in the harness whose value is known
independently, and it exists so that a broken harness announces itself. **If `frame` is far from 85 %, stop
and fix the harness; the other two arms mean nothing until it is right.** That check is the single most
important line in the log.

Resubmitting `sbatch -D ~/spinesurg-ct-nnunet slurm/guided_validate.sh` skips every arm whose `guided.json`
already exists, so it is always safe.

### Four jobs, none of them quotable

| job | what happened |
|---|---|
| **40375024** | completed and produced nonsense — τ had silently defaulted to 0.200 |
| **40375063** | the new guard refused to invent a threshold. Correct, but it would not say why |
| **40375064** | same, because the diagnostic patch meant to explain it had silently done nothing: a `str.replace` whose search string a shell heredoc mangled, with no assertion on the result — the exact trap this repository's notes describe |
| **40375066** | **the calibration finally worked**: τ = 0.033, from 59 correctly-paired links, 1st/5th/50th percentile 0.015 / 0.033 / 0.131. Every arm downstream still inherited two faults (below) |
| **40376577** | both faults fixed. Running. |

### The faults, in the order they were found

1. **τ = 0 is NaN, not "no gate."** The calibration pass ran at `--tau 0.0`, which reads as turning the
   geometric gate off and does the opposite: τ is a divisor, a single frame has no links so its margin is
   zero, `0/0` is NaN, every comparison against NaN is False, and the run fell through to `done` after **one
   exposure**. One exposure is no link, no link is no pair, no pair is nothing to calibrate from. τ ≤ 0 is
   now refused at construction; calibration runs at 0.001.
2. **The frame-alone control was not the control.** `sweep_map` means `anchor_decode` over the frame's
   posteriors — a monotone within-frame decode. Mine was a raw per-box argmax, a much weaker reading, which
   is why it read 31 % against a published 85 %. It now uses `sweep_map`'s own `make_queries` and its own
   computation, so it is a control that can fail.
3. **The geometry was compared against the wrong exposures.** A reposition after a failed anchor is taken by
   the operator but correctly *not* entered into the run, so the truth array grew while the run did not and
   every later index was off by the number of repositions. Thirty runs in 120 issued `anchor_not_found`,
   which is why recovered geometry read 58 mm at the median against 1.2 mm on the phantom. Each exposure is
   stamped with its index now.
4. **The calibration needed the answer it was computing** — margins came only from completed runs. Collected
   from every run now, and an empty calibration is an **error** rather than a default.
5. **The spacing constant lagged the run** — the region came from the newest frame, so a run leaving the
   lumbar spine kept dividing by 34 mm where 27 was right and commanded every distance a quarter too long.
6. **The phantom was not a spine** — equal spacing with thoracic names, which is why the tests could not see
   fault 5. Bodies are spaced at their own regional pitch now.

### The one thing not to lose

Aspects A and E of the patent package are marked **implemented but phantom-measured only**, in
`docs/provisional/SPECIFICATION.md` (the note on reduction to practice) and `docs/INVENTION_DISCLOSURE.md`
§8. Those two places are what gets updated when a trustworthy corpus number exists. If the numbers are bad,
the honest move is to narrow the claims — not to requote the phantom.

---

**Status of the design below.** Implemented and unit-tested against a phantom. What is measured on the
phantom is labelled as such throughout; nothing here is a corpus result.

---

## The loop a radiographer can be handed

```
$ python tools/guided_console.py            # or drive GuidanceEngine directly

  Place the field on the sacral promontory and acquire.  The run will be walked cranial to T12.
> [exposure]
  Field contains L3, L4, L5, sacrum.  T12 is 5 levels cranial.
  Move 72 mm cranial and acquire (capped to keep the overlap; more steps to follow).
> [exposure]
  Field contains L1, L2, L3, L4.  T12 is 3 levels cranial.  Move 72 mm cranial and acquire.
> [exposure]
  The link at seam 2 is ambiguous (margin 0.03) — it cannot rule out an offset of one vertebra, and no
  exposure at the end of the run overlaps it.  Move 27 mm caudal, back over that seam, and acquire.
> [exposure]
  Field contains T12, L1, L2, L3.
```

Four exposures. The operator was never told where they actually went; every distance after the first came
out of the images.

### Two ways to start, and why both exist

| `start=` | The first exposure goes | Ends with |
|---|---|---|
| `"landmark"` | on the pelvis (or C2) | the run walked out to a named target level |
| `"target"` | on the level being operated on | the run walked back to the anchor, the operative field named retrospectively, and the **return distance** commanded |

`landmark` is the one to ask a radiographer for: the run is pinned from the first exposure, so every
vertebra is named as it goes. `target` is what a surgeon does — shoot what you are working on, then find out
what it is.

### The run is planned before it starts

```python
>>> from acquisition import plan_run
>>> plan_run("C5")["from"],  plan_run("C5")["exposures"]        # ('C2', 1)
>>> plan_run("L4")["from"],  plan_run("L4")["exposures"]        # ('sacrum', 1)
>>> plan_run("T7")["from"],  plan_run("T7")["exposures"]        # ('C2', 4)   sacrum would be 5
```

**Mapping the whole column is never the point.** The run only has to be long enough to carry a name from an
anchor to the level being operated on, and there are two anchors. Cervical work is one exposure from C2 and
six from the sacrum; L4 is one from the sacrum and eight from C2. The mid-thoracic spine is where both
anchors are far — and it is the same region where a single field contains no landmark at all, and where the
measured gain is largest (31.1 % from one frame against 99.3 % mapped onto a run). **That is the region this
is for.**

---

## How it decides

### The confidence, and why it is a product of two things

```
confidence = appearance × clip(geometry / τ, 0, 1)
```

- **appearance** — the lowest probability the namer gave any body in the field. The minimum, not the mean: a
  single uncertain vertebra makes the whole field doubtful.
- **geometry** — the smallest margin over the run's links, where a link's margin is its peak correlation less
  the best correlation at any shift more than half a vertebral spacing away. A link that cannot tell its own
  offset from a one-vertebra offset puts **every name beyond it wrong**, and this says so before any name is
  emitted.

Neither term needs the answer. Both are available at the moment of acquisition.

### The remedies differ, because the failures do

| what is low | what is commanded |
|---|---|
| appearance | a full step toward the anchor — more reach, more constraint |
| geometry | **go back over the ambiguous seam**, at a distance measured from the link shifts |
| neither, target not yet reached | a step toward the target, capped so the overlap survives |

**The seam remedy is the one that took three attempts to get right.** The first version commanded a short
step, which adds a frame at the *end* of the run — and the ambiguous seam was three frames back, where
nothing acquired at the end overlaps it at all. The margin was reported at 0.03 three times running, the
ladder declared the geometry irreducible, and the run failed at a fault the remedy could not reach. The
command now names the seam and the distance back to it.

### It stops rather than repeating itself

A remedy is checked against the term it was meant to move. If the margin does not rise, one more attempt is
made with more overlap, and then the run **declines** — because a name beyond a link that cannot rule out a
one-vertebra offset is wrong, and saying so is the entire point of measuring the margin.

The escalation is also capped so it cannot converge on a retake. Asking for four bodies of overlap in a field
that holds four leaves a step of a few millimetres: the same picture again, which is the one remedy already
measured **not** to work — 95.7 % declining-and-retaking against 95.3 % answering everything, over 4,792
query frames. What helps is overlap between *linking* frames: 42 % of frames answerable at 99 % accuracy at
one body of overlap, 82 % at two.

---

## Which way the spine runs

An intraoperative frame carries no promise that the head is at the top. The intensifier rotates, the readout
flips, the patient may be prone or lateral. Commanding "cranial" while believing cranial is up when it is
down does not degrade the answer — **the frames do not overlap at all** and no run can be built.

So the direction is measured:

1. the anchor is found by **posterior over every body in the field**, not by where it sits, because where it
   sits is exactly what is unknown;
2. the column's axis comes from the principal axis of the body centres, which fixes the *line*;
3. the anchor fixes the *sign* — a sacrum is the caudal end of the run by definition;
4. every frame is rectified into that direction before any of the existing machinery touches it;
5. the operator is told anatomy ("38 mm cranial"), which needs no transform; a gantry is given
   `delta_row_mm` / `delta_col_mm` in the device's own axes, with the measured `axis_angle_deg`.

Photographed at 0°, 90° and 180°, the same phantom gives the same run and the same names.

In `start="target"` mode the first frame holds no anchor, so only the line is known and the head is
provisionally taken to be up. That assumption is not relied on: if it was wrong, the first commanded step
moved away from the overlap, the linker finds nothing at all, and the run flips and re-links.

---

## The digital fiducial

A mark placed on a confirmed vertebra and carried into every later exposure.

**What makes it a fiducial rather than a caption** is that it is anchored to a vertebra *of the run*, and
every later frame is registered onto the run and the mark re-projected through that registration. The C-arm
can be moved, the magnification changed, the patient rolled; the mark stays on the bone. It reuses the
registration the naming already needs.

**It does not blink out.** A frame that cannot be registered keeps the mark, flags it stale, and reports the
last good position. A mark that vanishes whenever the picture gets poor is not doing the job a gold fiducial
does, which is to still be there when the picture is poor.

**Off the edge is still an answer** — "the level you marked is 41 mm caudal of where you are looking" is
another commanded displacement, and it is what a surgeon hunting for a level actually wants.

**The aliasing guard, which the tests forced.** A mark placed on L1 projected onto T12 in two frames of five
— and not approximately: on T12's centre to within a pixel. The query registration had locked onto the wrong
period, at peak correlation 0.78 against 0.83 for the correct ones, which is not a quantity that separates
them. The registration now carries the same margin the linker has, and a position is asserted only when a
one-vertebra offset can be ruled out. On the phantom, **every asserted position is on the marked vertebra**;
the rest are refused rather than guessed.

The comparator is concrete: one centre performed 179 preoperative percutaneous gold-fiducial placements over
38 months, 176 of them thoracic, at a mean of 52 minutes and 183 mGy each, solely to mark a level.

---

## Running it

### Tests — no data, no models, no GPU

```bash
python tests/test_acquisition.py
```

Builds a synthetic column, photographs it at any angle, and drives the whole loop with an operator who
misses by ten per cent. Ten sections. Deterministic under `PYTHONHASHSEED=random` (it was not, once: see
below).

### Validation on the render corpus

```bash
sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/guided_validate.sh
```

Calibration runs first and on its own cases, then five arms. **Every arm skips itself if its `guided.json`
exists**, so the job can be resubmitted after a pre-emption without redoing anything. Progress:

```bash
python tools/pipeline_state.py            # guided_calibrate, guided_validate
```

One arm, by hand:

```bash
python tools/validate_guided.py \
    --drr ~/ctsp_drr --drr ~/verse_drr \
    --model ~/model_night/runs/model_r18_la_v7.pt \
    --head  ~/model_night/heads_mixed/head_r18_la_v7_v7.pt \
    --detector ~/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt \
    --anchor-detector ~/FluoroCap/anchor_det_v1.pt \
    --boxes det --span ii9 --overlap 2 --perturb film --link robust \
    --holdout-bank ~/allspine_v7_fov96_ctx --tau 0.09 \
    --levels-from-anchor 5 --slop 0.10 --rotate-max 0 \
    --out ~/model_night/guided/main
```

`--calibrate` measures the margin and stops. Refuses to run without `--holdout-bank` unless
`--allow-trained-on` is passed, which writes that fact into the record.

### The three arms, and why there are three

| arm | what it is | what it answers |
|---|---|---|
| `guided` | the engine commands every exposure | the thing being claimed |
| `fixed` | **the same number of exposures**, constant step from the anchor | is the guidance doing anything, or would any run of that length have done? |
| `frame` | the query frame alone, no run | the floor |

All three are scored on **identical query frames**, so the comparison is about the run and not the pixels.

---

## What is measured

| | |
|---|---|
| naming | a limited field mapped onto the run, per arm, same frames |
| exposures | per run, against what `plan_run` predicted before it began |
| geometry | where each exposure really was, against what the images say — the engine is never told |
| refusals | how often it declined, and which term stopped it |
| fiducial | of the positions asserted, how many are on the marked bone; how often it refused instead |

**On the phantom** (not the corpus; the corpus numbers land in `guided.json`): every exposure's position
recovered to within **1.2 mm** from the images alone, after four steps executed with ten per cent slop. That
is what lets the return to the operative field be commanded at all.

---

## Defects found by the tests, recorded because they were real

- **The remedy could not reach the fault.** Described above. The run that had been declaring its geometry
  irreducible finishes in four exposures with every name right.
- **The ladder converged on a retake** — an 8 mm step, which is the one thing already measured not to work.
- **A remedy was reissued forever** — nine identical instructions and then a refusal.
- **The mark projected onto the wrong vertebra**, on its centre, with a confident-looking correlation.
- **One run in four failed, nondeterministically.** `max(set(rs), key=rs.count)` iterates a set of *strings*,
  whose order depends on Python's per-process hash randomisation. A frame holding two thoracic and two lumbar
  bodies resolved either way; the spacing constant moved from 27 mm to 34; every commanded distance moved
  with it. Sorted before the max. Six for six since.
- **The anchor gate refused a field the sacrum was in.** The threshold was a guess (0.30 of the posterior on
  one of 27 classes), and the harness was discarding the engine's own commanded reposition and scoring the
  run as a failure to anchor.

---

## The first corpus run said the harness was broken, and it was

The `main` arm of job 40375024 returned guided 25.6 %, fixed 19.2 %, **frame alone 30.8 %** — the frame
beating both runs, on a corpus where `sweep_map` reaches 95.1 %. That is not a result about the method; it
is a result about this harness, and three causes were found.

1. **The calibration collected nothing and said so where nobody would look.** τ printed as 0.200 — exactly
   the default the calibration existed to replace. Margins were only gathered from runs that *completed*,
   and completing a run needs a workable τ, so the calibration required the answer it was computing. Zero
   margins were collected and the shell fell back to `0.200` silently. Five arms then ran at a hand-picked
   threshold that read as a measured one. Margins are now collected from every run, and **an empty
   calibration is an error**: the job refuses to run the arms rather than invent a threshold.
2. **The spacing constant lagged the run.** The region was taken from the newest frame, so a run walking
   cranially out of the lumbar spine kept calling itself lumbar, divided the observed pitch by 34 mm where
   27 is right, and commanded every distance about a quarter too long. Recovered geometry was out by a
   median of **35 mm** against 1.2 mm on the phantom — about the size this predicts. The region is now taken
   from every body named so far.
3. **The phantom was not a spine.** It spaced every body equally and named them thoracic — a column of
   thoracic vertebrae as far apart as lumbar ones — so the engine's regional scale was correct and the
   fixture's was not, and the whole class of error above was invisible to the tests. Bodies are now spaced
   at their own regional pitch.

τ = 0.200 was also **higher than the corpus supports**: `cover_seam` fired 268 times across 120 runs and
60 of them ended `geometry_irreducible`. Whether that resolves once τ is genuinely calibrated is the thing
the next run answers. **No number from that run should be quoted.**

## Open, and honestly so

- **τ is calibrated on renders.** Its value is a property of image texture, and real fluoroscopy is not a
  render. The calibration procedure transfers; the number should be re-measured on film.
- **No C2 detector exists.** The cranial anchor falls back to the namer's posterior.
  `tools/build_sacrum_dataset.py` is the recipe for one, and the anchor detector already carries a `skull`
  class that would serve as a second signal.
- **The linking, composition and registration stages have never been timed.** Two networks are benchmarked;
  the machinery that distinguishes this work is not. No latency claim should be made until they are.
- **The fiducial has been exercised on renders and a phantom, never on real fluoroscopy.**
- **The marker's aliasing guard reduces wrong assertions; it does not eliminate them.** On a phantom
  spaced at its own regional pitch, about one asserted position in four still lands on a neighbouring
  vertebra. The test asserts the property that matters — that the system refuses rather than guessing, and
  that what it asserts is mostly right — and prints the residual, because tuning the threshold until the
  test passes would be fitting a constant to the fixture.
- **`start="target"` carries a 180° ambiguity** until the run reaches the anchor. The recovery is
  implemented and tested, but it costs an exposure when it fires.

---

## Where the code is

| | |
|---|---|
| `tools/acquisition.py` | the engine, the orientation, `plan_run`, the fiducial board |
| `tools/validate_guided.py` | the closed-loop harness and the three arms |
| `tests/test_acquisition.py` | the phantom and ten sections of checks |
| `slurm/guided_validate.sh` | calibration then five arms, resumable |
| `tools/sweep_map.py` | the run machinery this builds on: linking, chain, alphabets, panorama |
