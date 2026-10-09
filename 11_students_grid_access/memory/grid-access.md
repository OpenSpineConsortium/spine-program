---
name: grid-access
description: Wayne State HPC login is go2432@grid.wayne.edu; project root and where CTs vs labels live
metadata: 
  node_type: memory
  type: reference
  originSessionId: 601aef39-3c17-45b7-9ce6-4f172acc8773
  modified: 2026-08-21T04:30:33.093Z
---

> **Copy record (11_students_grid_access, 2026-10-08).** Status in `HANDOFF/context/INDEX.md`: PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4). Source: HANDOFF/context (redacted copy set) (context/grid-access.md). Redactions by kind: none. Partly superseded: aliases resolve (windows-ssh-to-grid); CTSP data moved to `~/data/CTSpinoPelvic1K` and the Ceph volume (grid-ceph-volume-oschome). Standing-rule note tagged `all`: every project folder carries it.


Wayne State HPC: `ssh go2432@grid.wayne.edu` (key is in WSL at `~/.ssh/id_ed25519`, not
in the Windows `.ssh`; run all grid commands through WSL — see [[wsl-for-network]]).
The host alias `grid` and `warrior` do NOT resolve; use the full hostname. The login node
is `warrior` — never run work there, see [[no-login-node-jobs]].

Project root: `/wsu/home/go/go24/go2432/CTSpinoPelvic1K`

Where things are, which cost time to find:
- release labels — `data/v5_final/{case}_label.nii.gz`
- matching CTs — `data/hf_export/ct/{case}_ct.nii.gz` (NOT under `data/placed/`, which
  holds source masks named by DICOM UID, not by case token)
- ITK-SNAP descriptor — `data/itksnap_v5_labels.txt`
- logs — `logs/{jobname}_{jobid}.out`

`sbatch --dependency=afterok:JOBID` is rejected if the named job has already finished, so
chain only against a job still in the queue.

Local ITK-SNAP: `C:\Program Files\ITK-SNAP 4.4\bin\ITK-SNAP.exe`, launched with
`-g CT -s LABEL -l DESCRIPTOR`. Launch it with PowerShell `Start-Process`, since running
it in the foreground blocks.
