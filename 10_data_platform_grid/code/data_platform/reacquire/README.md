# Re-acquiring the holding

`reacquire.py` reads `../sources.json` (the same data as `../sources.yaml`) and, for any source id or for all of them,
prints or runs the commands that fetch that source again, then checks the result. Every command comes from the
source's card in `../DATA_MANIFEST.md` and uses the tools that exist in this repository today. Where a card's recipe
text and `sources.json` differ, `sources.json` is the runnable form.

## What it does

- **Dry run (default).** Prints, per source: the route and mode, the resolved commands, the checks that prove the copy
  complete (with every key a check uses: field, glob, recursive, minimum size), and the manual steps of a gated
  source. Nothing is executed. Runs anywhere (standard library, Python 3.6+). `--grid` resolves the paths with the
  grid's HOME (`/wsu/home/go/go24/go2432`) instead of this machine's.
- **`--run`.** Executes the commands, inside a Slurm job only. On the login node (hostname `warrior*`) or outside a
  job it refuses and prints the sbatch line instead (`reacquire.sbatch`). The helpers (`zenodo-get`, `hf-get`,
  `http-get`, `github-zip`, `nifti-check`) refuse the same way when called by hand (`--outside-slurm` for tests). Per
  source it writes a state folder, by default `$RS/data/<folder>/meta/reacquire/<id>/`: `commands.sh` (the exact
  script), `log.txt`, `verified.jsonl` and `failed.jsonl` (one line per command and per check, as
  `tools/acquisition_fetch.py` writes them), and `REACQUIRE_STATUS.json`.
- **`--verify`.** Runs only the checks (count, bytes, md5, sha256, a SHA256SUMS file, a JSON field such as
  `FETCH_STATUS.json` `unresolved_failures`, the distinct units of a `verified.jsonl` (optionally one collection's),
  a full read of every member of an archive, and the content-list hash of `tools/data_manifest.py` for the roots in
  `docs/RSNAI_DATA_MANIFEST.json`).

Modes in `sources.json`: `run` (the commands do the work in this job), `submit` (the commands submit the
repository's own sbatch wrappers, such as `slurm/acquisition_fetch.sh` or `slurm/cobra_fetch_all.sh`; run `--verify`
after those jobs end), `manual` (a form, a DUA, a subscription, a request, a GPU rebuild whose inputs are not
recorded, or no route: the steps are printed and never executed). A manual entry with `covered_by` is re-acquired by
another source: the 39 per-collection IDC entries are covered by `idc_tier1`, the one pooled, resumable fetch of all
3,600 series into `$RS/data/idc` (they share `data/idc/fetch/`, so running them side by side would fetch overlapping
series into one state folder). `reacquire.py` refuses a selection in which two runnable sources share one
acquisition state folder.

**Resuming.** Every download goes to `<dest>.part` with an HTTP Range resume, is checked (size, md5, sha256 as the
source records them) and only then renamed over `<dest>`; a complete file that fails its hash is set aside as
`<dest>.bad`, never over a good copy, and an existing copy that verifies is kept without a download. A requeued job
keeps its Slurm job id, and `reacquire.py` skips the submit-mode commands that already ran in that job, so a
preemption does not submit child jobs twice. `--resume` skips every command already recorded as done.

## Routes

| route | tool | verification |
|---|---|---|
| `idc`, `nbia`, `hf`, `zenodo`, `s3` (family B) | `tools/acquisition_fetch.py` through `slurm/acquisition_fetch.sh`; manifests read from `SchwingNet/results/transitional_registry/acquisition/manifests/` in the repository; `$D/logs` created before each sbatch | instance count per series; zip + instance count; LFS sha256; record md5 + member CRC; object size; per-collection IDC: that collection's distinct series in `data/idc/fetch/verified.jsonl` |
| `zenodo_http` | `reacquire.py zenodo-get` (Zenodo record API, HTTP Range resume) | size and the record's md5 per file, checked before the rename; CTPelvic1K also reads every tar member |
| `hf_hub` | `reacquire.py hf-get` (huggingface_hub `snapshot_download`, pinned to the revision it resolves) | size and LFS sha256 per file |
| `http` | `reacquire.py http-get` (stdlib; `--impersonate` uses curl_cffi with a Chrome fingerprint for Cloudflare-fronted archives); `reacquire.py github-zip` for a GitHub mirror (codeload zip of the default branch, as `tools/thoracic_xr_fetch.py` fetched the AASCE mirror) | size, md5 or sha256 as the card records, checked on the `.part` |
| `cobra_fetch` | `tools/cobra_fetch.py`, `slurm/cobra_fetch_all.sh`, `slurm/cobra_verify.sh` | every catalogued file at its catalogued size (`COBRA_COMPLETE.md`) |
| `jhu_dataverse`, `dl_deepfluoro` | `tools/jhu_dataverse_fetch.py`, `tools/dl_deepfluoro.py`; the vendor unpack runs in the same job | byte count against the deposit; the manifest's list hash |
| `spinesac_fetch` | `tools/spinesac_fetch.py` | file count and sizes against `drive_tree.json` |
| `other_ct_fetch` | `tools/other_ct_fetch.py` (CTSpine1K from HF; RibFrac unzip) | size + LFS sha256 per file; member sizes |
| `tcia_ctsp_download` | CTSpinoPelvic1K `slurm/download_raw.sh` with `DATA_DIR` on Ceph (the script binds it into its container), the conda singularity on PATH and the SIF checked first | DICOM directories per series |
| `zenodo_http+ctsp_fetch_from_tcia` | the v11 record, then the release's `fetch_from_tcia.py` into a fresh tree with a conda-forge `dcm2niix` (the GitHub binaries need glibc 2.29, the nodes have 2.17) | record md5; 802 CTs and labels; `reacquire.py nifti-check` (gzip integrity of every CT, affine and shape against the label); `tools/ctsp0533_verify.py` for 0533 |
| `kaggle`, `osf_verse`, `git`, `physionet_wget` | the spineps env's Kaggle CLI; VerSeFusion `slurm/download_raw.sh` with `DATA_DIR`/`RAW_DIR` on Ceph; git clone (with `git lfs pull` when the repository declares LFS); credentialed wget | zip size; `download_manifest.json` `n_failed`; file counts that ignore LFS pointer stubs; SHA256SUMS |
| `rebuild` | the builder named in the card, with its source and destination on the Ceph layout; GPU builders are `manual` and keep their own partition and QoS | counts named in the card |

## Use

```bash
cd ~/spinesurg-ct-nnunet/data_platform/reacquire
python3 reacquire.py --list                                   # on a laptop or in a job: python is banned on warrior
python3 reacquire.py --grid carmlspine ctspinopelvic1k        # dry run, grid paths
python3 reacquire.py --grid --all --modes run submit          # dry run of everything that runs unattended
mkdir -p logs                                                 # Slurm opens --output before the script runs
sbatch -D "$PWD" --export=ALL,IDS="carmlspine geneva_hip",MODE=--run reacquire.sbatch
sbatch -D "$PWD" --export=ALL,IDS="carmlspine",MODE=--verify reacquire.sbatch
python3 test_reacquire.py -v
```

`data_platform/` must be committed and pulled on the grid first: the sbatch script runs
`$HOME/spinesurg-ct-nnunet/data_platform/reacquire/reacquire.py` and stops if it is not there.

Variables in the commands are resolved from the environment, with these defaults: `RS=/rs/rs_grp_oschome/go2432`,
`DATA=$RS/data`, `REPO=$HOME/spinesurg-ct-nnunet`, `DP=$REPO/data_platform`, `CTSP_REPO=$HOME/CTSpinoPelvic1K`,
`VFR_REPO=$HOME/VerSeFusion`, `XRSP_REPO=$HOME/XRSpinoPelvic1K`, `SDET_REPO=$HOME/spine-detector`,
`ACQ=$DATA/anomaly_harvest/acquisition`; per source `DEST` (the layout path: `<folder>/<subpath>` when the layout
names one, such as `derived/verse_drr`, else `<folder>/raw`), `STATE` and `PY` (the environment the source's tool
needs: spineps, fluorogen or the acquisition env). `PHYSIONET_USER` is supplied by the person who runs the
credentialed VinDr source. Secrets (HF_TOKEN for a gated repository, KAGGLE_API_TOKEN) are passed in the environment
of the submit line; nothing here reads a token file. No recipe writes under `$HOME` (the test suite checks it); the
CephFS layout is the destination of every fetch and rebuild.

## Limits

- The web drifts. HF routes resolve a revision at run time unless the card pins one (`deepfluoro_xvr_hf` is pinned);
  the IDC route uses whatever release the installed idc-index serves (a series withdrawn after v24 would fail); the
  AASCE mirror is fetched at its branch head (no commit is recorded), so a moved head fails its md5 by design;
  FluoroCap and the public videos cannot be rebuilt bit for bit. The cards say so.
- Gated sources (VinDr, BUU, CSXA, IEEE DataPort, Stanford AIMI, RSNA MIRA, CT-RATE, CADS, MAGIC-CT) need a person:
  their steps are printed and nothing is run.
- Family-B planned collections without a written include pattern (`<pattern to be chosen ...>`) are `manual` until
  someone writes the pattern into `slurm/acquisition_submit.sh`.
- GPU rebuilds (`lstv_flag_renders`, `physics_drr`, `implant_ct_synthetic`, `nnunet_dataset815`) are `manual`: their
  scripts need inputs no card records (`PSRC`, `TS_SRC`, an array size) or hard-code HOME paths, and they must be
  submitted with their own GPU partition and QoS, never with `reqp`/`requeue`.
- The CTSpinoPelvic1K rebuild needs `tcia_utils` in the spineps env (the commands check the import and stop) and
  builds `dcm2niix` from conda-forge under `$RS/envs/dcm2niix` on first use.
- Fetch scripts that exist only on the grid (`slurm/download_nhanes_full.sh`, `~/spine-detector/scripts/download_sources.py`,
  `~/data/ribs/dl.sh`, the TotalSegmentator download scripts) are replaced by the equivalents the cards propose; the
  NHANES loop is marked "not yet run" in its card.
