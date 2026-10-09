# Rebuilding the published methods, and asking whether a consensus of them beats any one alone

## Why this exists

Every published method for naming vertebrae without a preoperative CT reports its own number, on its own
cohort, at its own field of view, under its own metric. A verified survey of the literature
(`docs/research_registration_free_2026-09-18.json`) found **eight different quantities** in circulation —
registration convergence, geometric label placement given a correct CT, a surgeon questionnaire, detection
F<sub>1</sub>, Panoptic Quality, same-patient segment matching, a CT identification rate, and actual
radiographic naming — and exactly one of them is the thing this project measures. It also found that **no
method in the space releases code or weights.**

So a comparison table built from published figures cannot be read as a ranking, and saying so in a caption is
not enough. The only way to get a ranking is to rebuild each method from its stated architecture, train it on
one corpus, and score it with one function on one held-out set. That is what `tools/train_competitors.py`
does, and `tools/ensemble_eval.py` then asks the question that follows: if these methods fail in different
ways, does a consensus of them beat the best one alone?

## Run it

    make competitors            # submits slurm/competitor_ensemble.sh
    make ensemble-report        # prints the result once the job has finished

One job, not a chain of five. Every method has to be read out on the *same* held-out crops in the *same* row
order; five jobs writing five files that a sixth assumes are aligned is precisely the arrangement that
produces a silent misalignment. The whole thing is minutes of GPU per paradigm on 96-pixel crops. The
ensemble step refuses to fuse arrays whose `case` column does not match, so a misalignment stops the run
rather than changing the answer.

## The paradigms, and what each does when the anchor is gone

| Key | Method | Alphabet | With no landmark in the window |
|---|---|---|---|
| `ours` | encoder + mixed-length head | all 27 classes | names it |
| `cina` | two-step whole-film labeller (Cina 2021) | **L1–L5 only** | still names it — a guess with a confident posterior |
| `kim` | L5-only detector (Kim 2024) | L5 | abstains |
| `vertx` | anchor-and-zip (VertXNet 2024) | all, via the zip | **abstains** — there is no place to start |
| `konya` | count up from the sacrum (Konya 2021) | all, via the count | **abstains** |

Three of the four abstain by construction. That is not a handicap being imposed on them; it is what the
methods are. `cina` is the interesting one: its five-class output space **cannot represent a sixth lumbar
vertebra**, which is the cardinality trap written as an architecture rather than as a bug.

`konya` is a rule, not a network — nothing to fit. It is included because it is the honest floor, and because
on a whole film with the sacrum in view it scores the same as everything else, which is what makes whole-film
benchmarks useless for this question.

### What is faithful here, and what is not

Each paradigm gets its **own** backbone, from the same initialisation, for the same epochs, on the same
crops — so the comparison is the architecture and its decision rule, not a head bolted onto our encoder.

What is **not** faithful is the input. These methods were built for whole films and we hand them the same
limited-field crops we hand ours. That is the point of the exercise and also its main limitation, and it is
why each paradigm declares in its output what it does when its assumption fails. A method that abstains is
doing something different from a method that answers wrongly; both are recorded, and abstention is never
scored as a miss.

## What "with the map" means

The sweep supplies one thing the individual crops do not have: the knowledge that the vertebrae in a window
are **consecutive**. The ablation is exactly that constraint and nothing else.

- **Without the map** — each frame is named by the argmax of its own last crop. Every crop judged alone.
- **With the map** — a single global offset is fitted across the window, the one maximising the summed
  log-posterior over all its crops, and the name is read off that.

The posteriors are identical in both arms. Only the ordering constraint differs. That makes this a clean
ablation of the map rather than a comparison of two different systems.

## The trap this is built to avoid

Five methods give 31 non-empty subsets; times two fusion rules times two map settings is **124 cells**. Take
the best cell and report it and you have reported the maximum of 124 noisy numbers, which beats the best
single method nearly every time and means nothing.

So:

1. Films are split in half, **disjoint by patient**.
2. The combination is **chosen** on one half.
3. It is **reported** on the other.
4. The **dev-to-test drop is printed**. That drop is the selection effect, and it is the number that decides
   whether an ensemble gain is real.

The verdict line is explicit about all three outcomes: no gain, a gain smaller than the selection effect
(treated as not shown), or a gain that survives. A cell with fewer than `--min-n` windows is refused a
headline regardless of what it says.

## What comes out

| Path | What it is |
|---|---|
| `~/model_night/competitors/<paradigm>.pt` | trained weights, registered content-addressed with bank and commit |
| `~/model_night/competitors/<paradigm>.json` | what was trained, on what, its validation accuracy, its registry sha |
| `~/model_night/competitors/<paradigm>_val.npz` | per-crop posteriors on the held-out split, aligned row-for-row |
| `~/model_night/ensemble/ensemble.json` | all 124 cells, with dev and test accuracy and n for each |

Every checkpoint goes through `model_registry.try_register` with `push=False` — compute nodes have no route
out, so the login node's `sync` does the mirror.

## Reading the result honestly

Three of five methods abstain on an interior window, so on interior frames the ensemble largely reduces to
`ours` and any gain should be small. Where a consensus can help is on **anchored** frames, where the
counting methods have something to say and disagree with the shape reading — and disagreement there is
itself the signal, because that is the transitional case.

If the ensemble does win, it will most likely win on anchored frames and by a margin comparable to the
selection effect. That is the outcome to expect, and the reason the dev/test split is not optional.

## Related

- `docs/SWEEP_PROTOCOL.md` — the acquisition the map assumes, in the radiographer's terms
- `docs/research_registration_free_2026-09-18.json` — the verified survey, claim by claim with sources
- `docs/PIPELINE_RESUME.md` — where these two stages sit in the pipeline
- `tools/benchmark_cina.py` — the whole-film, sacrum-anchored task, which these methods were built for
