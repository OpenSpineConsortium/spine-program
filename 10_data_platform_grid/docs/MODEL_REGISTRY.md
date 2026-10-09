# Model registry

Every trained weight file the pipeline produces is stored once, immutably, under its content hash; ledgered;
logged to MLflow; and mirrored off the cluster. Nothing in the pipeline addresses a model by a mutable path
that a later step could overwrite.

## Why

On 15 September 2026 a chain step ran `ln -sf model_rung_1_aug2.pt model_rung_1_aug2.pt`, which replaces the
file with a link to itself. A model that took 2 h 25 min to train was gone two minutes after it was written,
and the night's dependent jobs ran on nothing. The registry makes that class of loss impossible rather than
unlikely: the store is content-addressed (the directory name *is* the hash, so no write can land on an existing
entry), files are made read-only, and every registration is pushed to a private Hugging Face repo so a lost
cluster directory is a `restore`, not a retrain.

## Layout

| Piece | Where | What it is |
|---|---|---|
| store | `~/model_registry/<sha256[:16]>/<file>` | one read-only directory per artifact |
| ledger | `~/model_registry/registry.jsonl` | append-only; one line per registration: name, sha, bytes, metrics, params, bank, git commit, source path, mirror path |
| aliases | `~/model_registry/aliases/<name>` | symlink to the newest registration of that name, moved atomically |
| tracking | `~/mlflow/mlflow.db` (SQLite) | MLflow experiments by stage; one run per registration with the metrics, params, tags and the weight file as an artifact |
| mirror | `hf://gregoryschwingmdphd/level-id-weights/registry/<name>/<sha>.<ext>` | private repo; the off-cluster copy |
| MLflow map | `~/model_registry/mlflow_runs.jsonl` | sha → run id for registrations logged after the fact by `sync` |

`MODEL_REGISTRY`, `MLFLOW_DIR`, `MLFLOW_TRACKING_URI` and `MODEL_MIRROR_REPO` override the defaults.

## How models get in

**Trainers register themselves.** Right after `torch.save`, each trainer calls `model_registry.try_register`,
which never raises (a registry failure is a line on stderr, not a lost training run):

- `tools/train_level_classifier.py` → alias `<bank>_rung_<tag>` (for example
  `allspine_v2_fov96_ctx_rung_1_aug2`), stage `level_model`, metrics exact / within1 / region / n_val.
- `tools/finetune_level_fluoro.py` → alias `fluoro_ft_<tag>`, stage `level_model_finetuned`, metrics from the
  last epoch (film_val, fluoro_holdout, kept_frac).
- `tools/drr2fluoro_cut.py` → alias `cut_drr2fluoro_G`, stage `translator`.

Compute nodes have no route out and their envs carry no MLflow, so a trainer's registration is store + ledger
+ alias only (`push=False`). **Chains call `model_registry.py sync` from the login node** after each training
step; `sync` mirrors every unmirrored entry and logs every unlogged entry to MLflow. It is idempotent.

**Chains never `ln -sf` a model.** A fixed-name path that inference expects (`runs/model_rung_1_aug2.pt`) is
placed with `model_registry.py link <name> <dest>`, which refuses to replace a real file and only ever swaps a
link, atomically.

**Inference records what ran.** `fluorocap_infer_v2.py` writes the SHA-256 of every level model it loaded
into `infer_v2_<tag>_meta.json` (`weights_sha256.level_model_<i>`), which is the registry key of that model.

## Commands

```
python tools/model_registry.py list                                   # newest registration per name
python tools/model_registry.py register PATH --name NAME --stage STAGE [--metrics result.json] [--bank DIR] [--no-push]
python tools/model_registry.py resolve NAME [--sha PREFIX]            # store path of the newest (or named) registration
python tools/model_registry.py link NAME DEST                         # safe alias at DEST
python tools/model_registry.py restore SHA_PREFIX                     # pull a store entry back from the mirror
python tools/model_registry.py sync                                   # mirror + MLflow for whatever is missing either
python tools/model_registry.py backfill                               # register the pre-registry weight files listed in BACKFILL
```

Run the CLI under an env that has `huggingface_hub` and MLflow with SQLAlchemy (see below). The mirror push
reads the personal token at `~/.cache/huggingface/token` and is skipped, with a note in the ledger, when it is
absent.

MLflow UI on the login node: `mlflow ui --backend-store-uri sqlite:///$HOME/mlflow/mlflow.db --port 5000`,
then `ssh -L 5000:localhost:5000 grid`.

## Environments

`mlflow-skinny` alone cannot open a SQLite store (its file store is deprecated in MLflow 3 and raises), and
`pip install mlflow` fails on the grid because `pyarrow` and `greenlet` have no prebuilt wheels for the
`spineps` interpreter. What works, and is in use: `spineps` (Python 3.11) with
`pip install --no-deps "sqlalchemy>=2,<3" alembic Mako MarkupSafe` — greenlet is only needed for async
SQLAlchemy — giving mlflow-skinny 3.16 a working SQLite backend. Keep one MLflow version per SQLite file: a
second env with a different MLflow would run its own schema migrations on the same database.

## What is registered

Sixteen pre-registry models were backfilled on 15 September (level models films_all2 rungs 1–2 with and without
augmentation, all-spine v1, the recurrent head, detectors v5z final / epoch 25 / v6f, anchor detectors v1–v2,
orientation net, hardware detectors v1–v2, panel classifier, the FluoroGen LoRA, the CUT generator) and are
mirrored: 1.1 GB. `model_registry.py list` is the current inventory.

## What it does not do

It does not version datasets or banks (`~/allspine_v2_fov96_ctx` and the like are rebuilt from scripts; their
`meta.json` names every source render). It is not a DAG scheduler: the overnight chains are still shell scripts
that wait on markers. Both are the natural next steps (DVC for the banks, a Snakemake or Prefect DAG for the
chains); the registry is the piece that had to exist first, because it is the one whose absence lost a model.
