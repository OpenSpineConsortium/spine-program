# code/: the scripts this project needs without a clone

Every file carries a header line naming its repository path and its state at commit 097933a of `spinesurg-ct-nnunet`
(branch `L6_Class`): "tracked", "working tree, uncommitted edit" or "untracked (laptop copy of 2026-10-08)". The
repository is the home of record (`../MANIFEST_CODE.md`); these copies exist so that a reader with this folder and grid
access can run S0 to S2 of `../TODO.md`. Run everything on the grid as an `sbatch` job (`../docs/handoff/RECIPES.md`
section 0); the GPU environment is `~/mambaforge/envs/fluorogen/bin/python`, the CPU one `~/mambaforge/envs/spineps/bin/python`.

| path | what | state at 097933a |
|---|---|---|
| `service/` (`README.md`, `app.py`, `model_defs.py`, `Dockerfile`, `requirements.txt`, `modal_app.py`) | the level-identification service: FastAPI `POST /infer` and `GET /health`; pulls weights from the private HF repository at start-up; `model_defs.py` holds the crop transform that must match training (`TGT_PX` on a `SIZE` canvas, band of 2 x rung + 1 heights, marker channel) and the `contiguous_run` decode. **Serves the older release** (`detect_v5z_epoch25` + M19), no sacrum count, coupling or abstain flag; S2 replaces it | tracked |
| `deploy_service.py` | hashes the weights, writes `registry.json`, uploads to the private repository, refuses a public one, reads the token from a file | tracked |
| `level_prototype.py` | the gated reference inference the parity gate is defined against (abstain rule at L355) | working tree, uncommitted edit |
| `alphabet_couple.py`, `count_from_sacrum_eval.py` | coupling and stop signal; count from the detected sacrum | tracked |
| `eval_gate.py`, `holdout.py`, `checkpoint_lineage.py`, `unseen_cases.py`, `patient_keys.py` (edited), `excluded_sources.py` | the evaluation gate and the identity rules | tracked |
| `stats_compare.py`, `model_registry.py`, `publish_checkpoints.py`, `latency_bench.py`, `eval_runtime_cost.py`, `level_flags.py`, `eval_calibration.py`, `level_selective.py`, `sweep_map.py` | statistics, the registry CLI (S0), the two latency tools (S1), flags, calibration (OQ C12), selective prediction (OQ C13), the sweep map (PRIVATE) | tracked |
| `cine_eval.py`, `cine_latency.py`, `bournemouth_qf_eval.py` | the cine scorer with the causal tracker (constants in `../results/schwingnet/cine/tracker_config.json`, frozen 2026-09-26), the per-frame latency timer with the 1e-5 parity gate (never run), the Bournemouth quantitative-fluoroscopy loader (no frame scored yet) | untracked |
| `device_census.py` | the DICOM header census S3 runs on the hospital's exposures | tracked |
| `fluoro_video/` | rule-based extraction of fluoroscopy panels from composite videos (22 files, pinned environment in `environment.yml` and `explicit_lock.txt`, Slurm scripts, tests); produced `$RS/data/external/fluoro_video/clips/` | untracked |
| `spine_detector_src_snapshot/` | `src/` and `tests/` of the private `OpenSpineConsortium/spine-detector` as found on the laptop (no `.git`, commit unknown, files 2026-09-01 to 2026-09-12); `src/manifest.py::canonical_slots` is the corner slot order; the manifest field named for where an image came from was renamed `lineage` in this copy (seven files, consistently) under the standing word rule; the repository keeps its original name | snapshot |
| `handoff_builders/` | `copy_context.py`, `refresh_context.py`, `build_context_index.py`, `build_context_export.py`, `check_paths.py`, `check_refs.py`, `patch_helper.py`: the scripts that made `../docs/handoff/context/` and its index; they expect the repository layout (`HANDOFF/`, the live memory folder) | tracked |

6 files carried laptop paths in defaults or comments as a record of where they ran; on copy those paths became the
marker prefixes of `../MANIFEST_LOCAL.md` section 4 (`spinesurg-ct-nnunet:`, `memory:`, `laptop-scratchpad:`, `laptop:Desktop/`),
which are not paths: set a real path before running them anywhere.
