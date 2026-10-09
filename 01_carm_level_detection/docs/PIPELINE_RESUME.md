# Resume here

You are picking up the FluoroCap vertebra-level pipeline. Read this page, then run the state tool. Do not trust
any status written in prose, including this page's examples — the numbers below are illustrative of the format,
and the tool is the record.

```
ssh go2432@grid.wayne.edu
~/mambaforge/envs/spineps/bin/python ~/spinesurg-ct-nnunet/tools/pipeline_state.py
```

It prints what is done, running, ready and blocked, writes `~/model_night/PIPELINE_STATE.md` and a machine
readable `PIPELINE_STATE.json` beside it, and gives the exact command for every stage that is ready. It changes
nothing and submits nothing. Every stage declares the artefact that proves it finished, so a stage cannot read
as done because a directory was created when its job started.

**If you add a stage, add it to `tools/pipeline_state.py`.** A stage that exists only in a shell history is a
stage that will be lost. That is not hypothetical; see the first trap below.

## What this project is

Name every vertebra in a radiograph or an intra-operative fluoroscopic frame, robustly enough to be useful
against wrong-level spine surgery, and in particular do not be fooled by transitional anatomy: a lumbosacral
transitional vertebra, a sixth lumbar, or a thirteenth thoracic. Those spines have 25 or 26 presacral segments
instead of 24, so anything that counts down from a landmark mislabels every vertebra below the extra one.

## Traps that have already cost time

**A hard-coded filename silently retired the best model.** `recurrent_order.py` opened `rung_0.npz` by name.
Every crop bank built after 14 September 2026 has rung 1 only, so the script could not open them and the
run-level head simply stopped being run. It also never saved its weights. Both are fixed. The same bug class
appeared twice more in `level_prototype.py`, which hard-coded `resnet18` and a 512-wide head and therefore could
not load any model the backbone trainer produced. **When a script names a file, a rung or an architecture as a
constant, check that the thing still exists.**

**A head is only valid with the encoder it was trained on.** Pair it with another and it returns 27 confident,
meaningless names. `level_prototype.py` now refuses a head whose sidecar names a different base model, and picks
its default by matching the encoder's checksum. Do not remove that check.

**Accuracy numbers are not comparable across banks or across protocols.** The long-quoted 98.7% came from
`films_ann_fov96_ctx`, where only 14 of the 27 classes exist at all and 94% of the test set is cervical, and it
was a run-level number being compared against a single-crop one. Whenever you quote an accuracy, state the bank,
the class count and whether a head was used.

**Real radiographs and CT renders must be reported separately.** A pooled number over both is dominated by
whichever group is larger and describes neither. `tools/eval_raw_films.py` does the split.

**Weak labels are not ground truth.** The literature fluoroscopy panels carry decoder placements constrained by
captions, not readings. Agreement with them is agreement with a weak label, and no panel has ever been read by a
human. Say so every time.

**Inline python heredocs collapse backslashes in the agent Bash tool.** Write the script to a file and run it by
path. Network calls go through WSL.

## The shape of the pipeline

Raw films and labelled CT become **render directories** (`img/*.npy` plus `ann/*.json` with per-vertebra boxes
and names). `make_context_crops.py` turns those into **crop banks** (`rung_N.npz`), where each vertebra is
resampled to 96 pixels on a 320 pixel canvas with a marker channel. A **per-vertebra classifier** gives
posteriors over 27 classes. A **run-level head** reads the whole ordered run. A **decoder** turns posteriors into
names. **Flags** say when not to trust the answer.

Unannotated radiographs are labelled by `tools/pseudolabel_real_films.py`, which does not count from a landmark.
It fits the whole detected run against four whole-spine templates over every offset, marginalises over the
placements, and emits the strongest true statement per vertebra: an exact name, a candidate set, a region, or
nothing. Every film is kept at some tier; ambiguity weakens the claim rather than discarding the image. A film
whose posterior favours a transitional template is flagged and its junction bodies are left unnamed.

## Key files

| what | where |
|---|---|
| pipeline state | `tools/pipeline_state.py` |
| which datasets are used, and why not | `tools/xray_dataset_usage.py`, `docs/XRAY_DATASET_USAGE.md` |
| template decoder and placement posterior | `tools/ordinal_spine_decode.py` |
| pseudo-labeller with supervision tiers | `tools/pseudolabel_real_films.py` |
| star loss for incomplete names | `tools/stc_head.py`, `tools/train_stc_head.py` |
| run-level head | `tools/recurrent_order.py`, `tools/head_mixed_length.py` |
| the deployed prototype | `tools/level_prototype.py` |
| flags and their operating points | `tools/level_flags.py`, `tools/eval_level_flags.py` |
| real film versus render accuracy | `tools/eval_raw_films.py` |
| why the literature panels are hard | `tools/panel_vs_film_stats.py` and the three audits beside it |
| corpus expansion chain | `slurm/corpus_expand.sh` |
| what was lost and restored | `docs/PIPELINE_SWEEP_LOST_COMPONENTS.md` |
| every dataset, model and result | `docs/MANIFEST_DATA_MODELS_RESULTS.md` |

## Conventions

The label alphabet is 27 classes: C1–C7, T1–T12, **T13**, L1–L6, sacrum. T13 and L6 are variant classes. A
normal spine is counted C1–C7, T1–T12, L1–L5, sacrum, **skipping T13 and L6**. Walking the full alphabet to
count a normal spine shifts every lumbar name by one; that bug has occurred here at least twice.

Splits are by patient, never by crop or by film. Two films of one person, or two projection angles of one CT,
must not straddle a split. `tools/build_allspine_v3.py` re-splits by case when merging banks, and it found a
real leak of 9,194 crops the first time it ran.

## Published methods, rebuilt (added 2026-09-18)

| stage | what | done when |
|---|---|---|
| `competitor_train` | re-implement Cina / Kim / VertXNet / Konya and train them on the newest bank | `~/model_night/competitors/*_val.npz` for at least three paradigms |
| `ensemble_eval` | does any combination beat the best single method, with and without the map | `~/model_night/ensemble/ensemble.json` |

Both run inside one job (`slurm/competitor_ensemble.sh`, `make competitors`) because every method must be
read out on the same held-out crops in the same row order. Read the result with `make ensemble-report`.

The bank is resolved at submit time as the newest directory holding `meta.json` **and** a rung file — not the
newest with a `READY` marker, because v7's build logged `V7_DONE` without writing one and requiring the
marker would silently fall back a version while the job name still claimed the newer data.
