# Lumbar Lordosis & LDI Pipeline

Automated lumbar lordosis and **Lordosis Distribution Index (LDI)** measurement
from CT + segmentation-label NIfTI pairs. Detects the superior endplate corners
of **L1**, **L4**, and **S1** and computes:

- **Global Lumbar Lordosis** (L1–S1)
- **Lower Lumbar Lordosis** (L4–S1)
- **LDI** = Lower / Global × 100, with category
  (`<50` Hypolordotic · `50–80` Normal · `>80` Hyperlordotic maldistribution)

S1 endplate detection uses the same CT-based per-AP-column scan as L1/L4, with
the search window anchored to the L5 vertebral body so it stays on the S1 body
surface instead of snapping to the sacral promontory or superior articular
processes (the highest points of the sacrum).

## Contents

| File | Purpose |
|------|---------|
| [automated_lordosis.py](automated_lordosis.py) | Core pipeline: corner detection, LDI, visualisation. Runs on local NIfTI files. |
| [run_hf_sample.py](run_hf_sample.py) | Lazily pulls token(s) from the HuggingFace sample dataset and runs the pipeline. |
| [dataset_interface.py](dataset_interface.py) | Dataset loader for the `CTSpinoPelvic1K` HF export (lazy NIfTI fetch). |
| [environment.yml](environment.yml) | Conda/mamba environment definition. |

---

## 1. Install mamba (macOS)

We use **Miniforge**, which ships `mamba`/`conda` pre-configured for the
`conda-forge` channel. Pick **one** of the following.

### Option A — Homebrew (simplest)

```bash
brew install miniforge
mamba init zsh          # or: mamba init bash, if you use bash
exec $SHELL             # reload the shell so `mamba` is on PATH
```

### Option B — official installer script

Apple Silicon (M1/M2/M3 — most modern Macs):

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
bash Miniforge3-MacOSX-arm64.sh
```

Intel Macs:

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh"
bash Miniforge3-MacOSX-x86_64.sh
```

Accept the prompts, then restart your terminal (or `exec $SHELL`). Not sure
which chip you have? Run `uname -m` — `arm64` = Apple Silicon, `x86_64` = Intel.

Verify:

```bash
mamba --version
```

---

## 2. Create the environment

From the project directory (the folder containing `environment.yml`):

```bash
mamba env create -f environment.yml
mamba activate ldi
```

This installs Python 3.11 plus `numpy`, `scipy`, `nibabel`, `scikit-image`,
`matplotlib`, and `huggingface_hub`.

> To update after editing `environment.yml`:
> `mamba env update -f environment.yml --prune`

---

## 3. Run on the HuggingFace sample dataset

[run_hf_sample.py](run_hf_sample.py) downloads **only metadata** first, then
fetches a token's NIfTIs on demand (label first to vet the case, CT only if it
qualifies). Files are cached by `huggingface_hub`, so re-runs are instant.

```bash
# auto-pick the first fused case that has L5 + sacrum, render + measure
python run_hf_sample.py

# a specific token, requiring the full LDI label set (L1, L4, L5, sacrum)
python run_hf_sample.py --token 0071 --require 1,4,5,7

# first 3 suitable fused cases, metrics only (no images)
python run_hf_sample.py --limit 3 --no-viz
```

Key flags:

| Flag | Default | Meaning |
|------|---------|---------|
| `--repo` | `anonymous-neurips-ED/CTSpinoPelvic1K-Sample` | HF dataset repo id |
| `--token` | _(auto)_ | Run a specific token instead of auto-picking |
| `--config` | `fused` | Config filter; falls back to all cases if empty |
| `--require` | `5,7` | Label ids that must be present (5=L5, 7=sacrum; use `1,4,5,7` for full LDI) |
| `--limit` | `1` | How many suitable cases to run |
| `--max-scan` | `8` | Max candidate cases to inspect while searching |
| `--out` | `results_auto` | Output directory |
| `--no-viz` | off | Skip PNG rendering |

The sample dataset is public, so no auth is needed. For a private repo, export
a token first: `export HF_TOKEN=hf_...`

If you see `No suitable case found`, the sample may use a different `config`
name or token format — check the `ds.stats()` block printed at the top and pass
an explicit `--token`, or loosen `--require`.

---

## 4. Run on your own local NIfTI files

[automated_lordosis.py](automated_lordosis.py) works directly on local files —
no HuggingFace required.

**Single case:**

```bash
python automated_lordosis.py \
    --ct    /path/to/0071_ct.nii.gz \
    --label /path/to/0071_label.nii.gz \
    --token 0071 \
    --out   ./results
```

**Whole dataset** (reads `manifest.json` at the root):

```bash
python automated_lordosis.py --root /path/to/spine_dataset --out ./results
```

Expected label map: `1=L1 … 5=L5 (6=L6) 7=Sacrum`.

---

## 5. Outputs

Both runners write to the `--out` directory (default `results_auto/`):

- `sagittal_<token>.png` — mid-sagittal CT with colored segmentation overlay,
  the L1 (red) / L4 (cyan) / S1 (gold) endplate lines, and the Cobb angle arcs.
- `lordosis_metrics.csv` — one row per case:

  | column | meaning |
  |--------|---------|
  | `token` | case id |
  | `global_lordosis_deg` | L1–S1 Cobb angle |
  | `lower_lordosis_deg` | L4–S1 Cobb angle |
  | `ldi_percent` | LDI = lower / global × 100 |
  | `ldi_category` | Hypolordotic / Normal / Hyperlordotic |
  | `L1_tilt_deg`, `L4_tilt_deg`, `S1_tilt_deg` | individual endplate tilts |

---

## 6. Tuning S1 detection

If the gold S1 line lands off the true superior endplate, three knobs in
`find_s1_corners` ([automated_lordosis.py](automated_lordosis.py)) control it:

- **`ant_trim`** (default `0.05`) — how much of the L5-body anterior edge to
  drop. Lower toward `0` if the anterior corner sits behind the promontory.
- **`post_trim`** (default `0.10`) — how much of the posterior body to drop.
  Raise it if the posterior corner drifts toward the sacral canal / articular
  processes.
- **`bone_hu`** (default `200`) — HU threshold for accepting a cortical-bone
  endplate voxel. Raise it if soft-tissue / partial-volume voxels sneak in.

On transitional (LSTV) anatomy the L5 anchor itself gets ambiguous, and a
manually placed S1 corner remains the most reliable fallback there.

---

## Troubleshooting

- **`mamba: command not found`** — you didn't run `mamba init zsh` (or your
  shell isn't zsh). Run it, then `exec $SHELL`.
- **`ModuleNotFoundError`** — the `ldi` env isn't active. Run `mamba activate ldi`.
- **`SSLError` / download hangs on first run** — corporate proxy/VPN blocking
  huggingface.co; the NIfTIs are fetched over HTTPS on first access.
