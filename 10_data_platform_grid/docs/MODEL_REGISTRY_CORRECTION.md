# MODEL_REGISTRY.md: two corrections (2026-10-08)

`MODEL_REGISTRY.md` beside this file is the registry document as committed in spinesurg-ct-nnunet at 097933a
(`docs/MODEL_REGISTRY.md`, last edited 2026-09-15). Two of its sentences predate the login-node ban and are wrong
today (`docs/handoff/INFRASTRUCTURE.md` section 13 rows 5 and 6; `docs/handoff/OPEN_QUESTIONS.md` F10). Everything else in
it stands.

## 1. "Chains call `model_registry.py sync` from the login node"

Wrong since the C&IT rule of 2026-09-28: nothing of ours computes on warrior, which terminates python by name
(`memory/no-jobs-on-login-node.md`, `memory/grid-ssh-second-factor.md`). The premise behind the sentence, "compute nodes
have no route out", is also wrong: compute nodes have internet (job 40409460; `INFRASTRUCTURE.md` section 13 row 6).
So `sync` runs as a job on a compute node, from the `spineps` environment, with the Hugging Face token read from its
file by the library (never echoed, never in `--export`):

```bash
cd /wsu/home/go/go24/go2432/spinesurg-ct-nnunet
sbatch -D "$PWD" -p reqp --qos=requeue --time=01:00:00 -o logs/registry_sync_%j.out \
  --wrap 'export PYTHONNOUSERSITE=1; ~/mambaforge/envs/spineps/bin/python tools/model_registry.py sync'
```

A chain step that needs the mirror pushed appends such a job with `--dependency=afterany:<training job id>`
(`afterany`, never `afterok`: `memory/no-jobs-on-login-node.md`; `docs/handoff/RECIPES.md` section 0 item 3). The
`try_register` call inside a trainer (store + ledger + alias, `push=False`) is unchanged.

## 2. "MLflow UI on the login node: `mlflow ui ... --port 5000`, then `ssh -L 5000:localhost:5000 grid`"

`mlflow ui` is a Python server and cannot run on warrior. Two routes that do not touch the login node:

- **Read the SQLite store on the laptop.** Copy `/wsu/home/go/go24/go2432/mlflow/mlflow.db` (1,028,096 B on
  2026-10-08) with `scp` through WSL and open it locally with the same MLflow version (3.16 with
  `sqlalchemy>=2,<3`; one MLflow version per SQLite file, as the document says). This is the route that needs
  nothing from the site.
- **Serve it from a compute node and tunnel through warrior.** Run `mlflow ui --backend-store-uri
  sqlite:///$HOME/mlflow/mlflow.db --host 0.0.0.0 --port 5000` inside an `sbatch` job, read the node name from
  `squeue`, then from the laptop `ssh -L 5000:<node>:5000 wsu-grid`. The port forward is plain ssh through the login
  node and runs nothing there; whether the site permits forwarding to compute nodes is not recorded (untested on
  2026-10-08).

## 3. Unchanged, and worth restating

Never `ln -sf` a model (a 2 h 25 min model was destroyed by `ln -sf model.pt model.pt` on 2026-09-15); place
fixed-name paths with `model_registry.py link NAME DEST`. The store is content-addressed and read-only; the ledger is
append-only; inference records the SHA-256 of every weight file it loaded. The ledger's seventeen identical
`orientation_net_v2` lines of 2026-09-15 (the first registration at 15:39:56 and sixteen repeats, one every twenty minutes, to 20:57:21) are a sync loop
re-registering one sha, so the 106-line ledger is not 106 models (`MANIFEST_GRID.md` section 4).
