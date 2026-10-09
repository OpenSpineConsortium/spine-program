<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path RECIPE.md. Copied 2026-10-08. Redactions applied by kind: banned word (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# The Lab Recipe

How a question becomes a paper in this lab, written so a medical student can run it, a lead can
run a team on it, and anyone can pick it up cold after a month away. The board of projects, with
who leads each and how to join, is [BOARD.md](BOARD.md).

The method in one sentence: **a paper is a chain of files, each written by a script that recorded
what it read, and a number enters the manuscript only through that chain.** Every section below is
one link of the chain. Each gives the rule, the incident that made it a rule, and the command or
file that carries it. The incidents are real and dated; they are in this document because the
same mistake was made more than once before it was written down.

Contents: 0 roles · 1 the shape of a project · 2 pre-register and freeze · 3 data rules ·
4 code and environment · 5 the grid · 6 Nextflow · 7 results to manuscript · 8 checking a number ·
9 working with Claude · 10 leaving, handover, credit · 11 checklists · A the worked example ·
B what is not yet true.

---

## 0. Roles

Every project on the board has three roles, and the board names the people.

| role | owes the project | how many |
|---|---|---|
| **lead** | the question, the frozen pre-registration, the manuscript; answers project email within two working days; runs a 15-minute weekly check-in; merges pull requests | one |
| **co-lead** | everything the lead can do; takes over when the lead leaves; the second reader on every freeze | one; a project without one is **unstaffed** |
| **members** | tasks: annotate, measure, render, check, draft a section; each task is a card line with a name on it | any number |

Above the projects: Ashley Schehr (senior scientist, co-PI) screens; Dr Tech (senior clinical PI)
confirms clinical reads; Greg Schwing signs off on every freeze and every submission.

**Joining.** Read the board, pick a project, email its lead with the subject `Join: <project id>`
and the hours per week you can give. The lead adds you to the card by pull request within the
week and points you at one open task. You do not need permission to read any public project.

**Leaving.** Section 10. Nobody leaves by going quiet; a project with a silent member for three
weeks is a project the lead re-staffs.

---

## 1. The shape of a project

A project is a folder with this layout, whether it is a semester measurement or a flagship paper.
A **task** is the unit of work: one script, one job script, one results file, and the manifest keys
that quote it. A task that does not end in a results file is not finished.

```
<project>/
  PREREG.md               what will be measured, and what counts as failure; frozen before the first number
  PREREG.md.sha256        its fingerprint; every producing job checks it and refuses on mismatch
  DEVIATIONS.md           every departure from PREREG.md, dated, with the reason
  JOURNAL.md              dated entries: what ran, job ids, what came out, what is next
  code/                   one script per task; each writes exactly one results file
  slurm/                  one job script per task; the header says what it produces and how to resume it
  results/                one JSON per task, each carrying its own _run block (section 4)
  numbers_manifest.json   key -> results file, JSON pointer, format, job id, PREREG item (section 7)
  paper/                  the tex; numbers only as \RESULT{key}; generated/numbers.tex is written at build
  RESUME.md               newest-first checkpoint blocks (section 9)
  env/<name>.lock.txt     the exact environment the results came from (make env-lock)
```

The board card for the project lives in `board.json` at the root of Student_Projects and is
rendered into `BOARD.md` by `tools/render_board.py`.

---

## 2. Before the first number: pre-register and freeze

**Rule.** Write `PREREG.md` before any script produces a number, freeze it with its hash, and never
edit it again. Departures go in `DEVIATIONS.md`.

**Why.** Pre-stated rules are what make a negative result reportable instead of embarrassing. The
render-ablation rule for the SchwingNet paper was written before the numbers (REVISION_LOG3 §13);
when one corpus came out the other way, that cell went into the manuscript as a result. In the
U251 work the primary endpoint's bar was pre-stated at 0.50; it failed, and the manifest note
reads "PRIMARY ENDPOINT. Pre-stated threshold was > 0.50; it failed."

**What PREREG.md contains.**

1. The question, in one sentence a clinician would recognise.
2. Population and inputs: which dataset release (by version and DOI), which files, their hashes,
   and the exclusions with the reason for each.
3. Each measurement as a proposal states it: identifiers, axis, unit, and the anatomical plane
   or landmark by name. "Maximum extent" is not a diameter; "first slice that works" is not a plane.
4. Each hypothesis with its **bar**: the number that counts as pass, taken from a published value
   or a power calculation, never from the data you are about to look at.
5. What counts as failure, and the sentence you will write if it fails.
6. The analysis plan, including which sets are held out and who reads what blind.
7. A freeze block at the end: date, author, and "no further edits".

**Freeze.**

```bash
sha256sum PREREG.md > PREREG.md.sha256
git add PREREG.md PREREG.md.sha256 && git commit -m "PREREG v1 frozen"
```

**Every producing job starts with the check**, and writes the hash into its result:

```bash
sha256sum -c PREREG.md.sha256 || { echo "STOP: PREREG.md changed since the freeze"; exit 90; }
```

A version 2 of the pre-registration is a new file (`PREREG_v2.md`) with its own freeze, and
`DEVIATIONS.md` says why. No fractional versions of anything, ever: v1, v2, v3.

---

## 3. Data rules that never bend

| rule | statement | why |
|---|---|---|
| **IRB umbrella** | A dataset is under HPR 2026-269 only if all five hold: public and de-identified by the source; downloadable without application, permission or data-use agreement; not restricted-use; no key or relationship that could re-identify; no linkage attempt. Anything else needs its own IRB filing **before** use. | one dataset was used before the separate filing item 7 promised |
| **Licences** | CTSpinoPelvic1K labels are CC BY-NC-SA 4.0, CT is CC BY 3.0, code is Apache-2.0. Cite the DOI. Never redistribute volumes; `.gitignore` blocks `*.nii.gz`, `*.dcm`, `*.zip`. | the SA clause is inherited from CTSpine1K and cannot be dropped |
| **Private forever** | Level-identification code, FluoroCap, model weights, the spinesurg-ct-nnunet and XRSpinoPelvic1K repositories. Never in a public repository, never on the website (inference runs behind a service). | the website shipped 121 MB of detector weights until 2026-09-14 and its history had to be rewritten |
| **Credentials** | Read from files (`~/.hf_*`, `~/.fluorocap/credentials.env`, `~/.zenodo_token`); never echoed, never in `sbatch --export`, never committed. Students use their own Hugging Face **read** token; the write token lives only in the review Space. | a token in a command line is a token in the shell history and the job log |
| **Personal data** | Survey CSVs with names, contact spreadsheets, IRB staff lists: never in any repository. | a filled staff list with work emails sat in a public folder for 171 commits |
| **Labels** | Read identifiers from `dataset_labels.json` of the release you are using; never type them from memory; never import a fixed map. In code call `ostk.labels.labels_for(volume)`. Two schemes exist (release: L1 = 20 … L5 = 24, sacrum 26, hips 30/31, femora 32/33; legacy: L1 = 1, femora 11/12) and resolving against the wrong one returns a finite, plausible, wrong answer: `femur_left` comes back **T4**. Identifier 29 (the v10 carved S1) is retired in v11 and dissolved back into the sacrum; the public mirror still served v10 on 2026-09-27, so student materials name v10 correctly until v11 ships, and then every check that gates on 29 goes with it. | pelvic incidence was once computed for the whole release against the legacy map; the only symptom was a QC flag; a retired gate on 29 later swapped a figure panel silently |
| **Volumes** | Canonicalise to RAS to **analyse**; never reorient when you **write**. Volumes are stored P,I,R. `as_closest_canonical` + `nib.save` silently transposes a label away from its CT. | it happened |
| **Case ids** | Zero-padded in the release (`0001`); `zfill(4)` before any join or diff. | every row looked changed |
| **Two tracks** | Students, the WSU grid and non-commercial data are the research track. Nothing from it moves to any commercial track. If a task would, stop and say so. | written policy |

---

## 4. Code and environment

**Scripts are files in the repository.** Not heredocs over ssh, not `sbatch --wrap`, not `python -c`
with backslashes. Write the file with the editor, commit, pull on the grid, run it by path. On
Windows the network calls go through `wsl -e bash -lc '...'`. Never name a scratch script after a
standard-library module (`numbers.py`, `io.py`, `pdb.py`); it shadows the import.

**`set -u`, not `set -e`.** With `-e` a script dies at the first non-zero status without saying which
check failed, and a job that dies silently looks the same as a job that was never run. Use
`set -uo pipefail` and write the checks yourself, each with its own message and exit code.

**Refuse early. An empty, missing, ambiguous or defaulted input stops the run.** This is the single
habit that would have prevented the most recorded incidents in this lab (16 of 29 tallied on
2026-09-27): a missing held-out bank that made the held-out set empty and flattered every result; a
wrong label map that returned T4 for a femur; a retired gate on identifier 29 that silently swapped a
figure panel; a trimming step that exited 0 with empty output; a dictionary parsed as a list that
reported zero annotators with confidence. In every job:

```bash
LIST=${LIST:?set LIST}                                   # required variables fail loudly
for p in "$IN" "$MODEL" "$PREREG"; do [ -e "$p" ] || { echo "REFUSING: missing $p"; exit 1; }; done
[ -s "$IN" ] || { echo "REFUSING: $IN is empty"; exit 1; }
[ "$(wc -l < "$LIST")" -eq "$EXPECTED_N" ] || { echo "REFUSING: $LIST has the wrong count"; exit 1; }
sha256sum -c inputs.sha256 || { echo "REFUSING: an input changed"; exit 1; }
```

In Python the same: a lookup that can return `None` raises instead; a set that can be empty is
asserted non-empty before it is used; a default argument that would change a result is not a
default.

**Pin the environment.** Containers by digest or by a pre-unpacked sandbox path, never a moving
tag (`:latest`). Python environments are exported from the machine that ran the jobs, not from a
`requirements.txt` of ranges: `make env-lock` writes `env/<name>.lock.txt` with the commit, host,
interpreter, torch and CUDA build, and refuses to write a lock that came back without the torch
line. Regenerate the lock at every freeze; a nine-day-old lock describes a different pipeline.

**Every results file carries its own record.** This is the link Nextflow, Slurm and git do not make
for you. The producing script writes a `_run` block:

```python
import datetime, hashlib, json, os, subprocess, sys

def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

def run_record(inputs, prereg_sha_file="PREREG.md.sha256"):
    """What produced this file. Refuses outside a git checkout: a result with no commit cannot be reproduced."""
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if not head:
        raise SystemExit("REFUSING: not inside a git checkout; commit the code first")
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip() != ""
    rec = {
        "job": os.environ.get("SLURM_JOB_ID"), "task": os.environ.get("SLURM_ARRAY_TASK_ID"),
        "host": os.uname().nodename, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_head": head, "git_dirty": dirty,
        "script": os.path.relpath(sys.argv[0]), "script_sha256": sha256(sys.argv[0]), "argv": sys.argv[1:],
        "inputs": {p: sha256(p) for p in inputs},
        "prereg_sha256": open(prereg_sha_file).read().split()[0] if os.path.exists(prereg_sha_file) else None,
    }
    if rec["git_dirty"] and os.environ.get("ALLOW_DIRTY") != "1":
        raise SystemExit("REFUSING: uncommitted changes; the result would not point at a commit")
    return rec

# at the end of every producing script:
# out["_run"] = run_record([ct_path, label_path, "PREREG.md"]); json.dump(out, open(dst, "w"), indent=1)
```

Write the file to a `.part` name and rename it into place only after your own checks pass, so a
killed job never leaves a half-written result that looks finished.

---

## 5. Running on the grid

The rules, each with the incident behind it. They apply to every job, including a ten-record test.

| # | rule | the incident |
|---|---|---|
| 1 | The login node (`warrior`) runs only `sbatch`, `squeue`, `scancel`, `ls`, `tail`, `git`. Everything else, including downloads, is a job; compute nodes have internet. | a session ran dozens of smoke tests and a download on a node shared by ~95 users (2026-09-21) |
| 2 | `sbatch -D <dir> script.sh`: `#SBATCH --output` resolves against the **submit** directory. | logs landing where nobody looked |
| 3 | Chain with `--dependency=afterany`, never `afterok`; the child reads a file (`READY`, `BUILD_OK`, `DECISION.json`) to decide whether the parent succeeded. `afterok` on a parent that already finished is rejected outright. | a prep job hit its 8 h limit and the whole chain went `DependencyNeverSatisfied` (2026-09-09); a child sat cancelled for seven hours after its parent was marked out-of-memory but had actually completed |
| 4 | `/tmp` is node-local **and swept**. Per-job scratch and IPC go under `/dev/shm/${USER}_<name>_${SLURM_JOB_ID}` with `trap 'rm -rf "$W"' EXIT`. | a cleaner deleted the multiprocessing sockets of two 18-hour training runs at the same minute; a FastQC task died writing its cache there (40468032) |
| 5 | Large outputs go on the lab's CephFS volume, not the home directory. Home is a 4.3 TB soft quota read with `pan_quota`, not `df`; the volume with `df-ceph oschome`. | home reached 97 %; 260 GB of banks were deleted to get under, and ~90 scripts then read an **empty** held-out set |
| 6 | CPU: `--partition=reqp --qos=requeue`. GPU: `--partition=gmsap,gvohp,galhp --qos=gpu --gres=gpu:1`. Ask for what the job needs; small jobs start sooner. | GPU partitions accept only the `gpu` QOS; other QOS names are refused |
| 7 | Containers: `$HOME/mambaforge/envs/nextflow/bin/singularity` (never `~/.local/bin`, never a module), a pre-unpacked sandbox, `-B <the specific CephFS path> -B $HOME -B $W:/tmp`. Probe the route in step 0 with a one-line command before staging anything. | three jobs lost in a row: exit 127, "starter not found", a bind that did not expose the tree |
| 8 | Arrays share **one** list through atomic claims (`mkdir` or `O_EXCL`), a stale takeover after N hours, a heartbeat, a GPU self-test before the first case, and a failure-streak stop. Any number of tasks and GPU types can then walk the same list. | Blackwell nodes under a CUDA 12.4 build would have stamped every claimed case failed |
| 9 | A dependent job whose inputs are not ready resubmits itself `afterany` on the producer (or `--begin=now+30minutes`) and exits 0. It never waits on a node. | design rule |
| 10 | `--no-requeue` unless the script is re-entrant (`.done/` markers, `-resume`); then `--requeue --open-mode=append`. | a requeued job that restarts from the top must not mix two attempts' files |
| 11 | One LaTeX compile at a time in a source directory (`flock`), or chain them. | two compiles interleaved on `main.aux`; one died, and a **stale** `main.pdf` from the previous good build stayed on disk |
| 12 | Before cancelling anything, record it: job id, state, elapsed, work directory, script, and the script's own header as the resume instruction (`docs/grid_records/JOBS_RECORD_<date>.md`). | Greg, 2026-09-27: "first record where each one is and what has to be done" |
| 13 | `sbatch --parsable`, strip the cluster suffix `${ID%%;*}`, and write the id with a timestamp and any replacement note into the project's `JOBS.txt`. | ids that lived only in a terminal |
| 14 | A pre-registered decision gate sits between a timing run and a production array: the timing job writes `DECISION.json` from a rule stated beforehand; the array refuses to start without it. | cost control on a 21,622-CT census |

**The job-script skeleton** (assembled from the scripts that run today):

```bash
#!/bin/bash
# <PROJECT>, <task>: one sentence on what this job produces and where.
# Resumable: resubmitting skips finished cases (claims in _claims/, outputs are .part then renamed).
#   run:    sbatch -D <workdir> --array=0-23 --export=ALL,LIST=<list> slurm/<task>.sh
#   retry:  add EXTRA=--retry-failed
# Exit codes: 0 done; 1 refused (missing input / probe failed); 3 nothing to do; 4 a step failed (resubmit to resume)
#SBATCH --job-name=<short>
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%A_%a.out
set -uo pipefail
LIST=${LIST:?set LIST}
W=/dev/shm/${USER}_<task>_${SLURM_JOB_ID:-x}_${SLURM_ARRAY_TASK_ID:-0}; mkdir -p "$W"; trap 'rm -rf "$W"' EXIT
export PYTHONNOUSERSITE=1 TMPDIR=$W OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo "<TASK>_START job=${SLURM_JOB_ID:-} task=${SLURM_ARRAY_TASK_ID:-} host=$(hostname) $(date)"
# step 0: refuse early
sha256sum -c PREREG.md.sha256 || { echo "STOP: PREREG.md changed"; exit 90; }
for p in "$LIST" code/<task>.py; do [ -s "$p" ] || { echo "REFUSING: missing or empty $p"; exit 1; }; done
# the work
python code/<task>.py --list "$LIST" --out results/ --shard "${SLURM_ARRAY_TASK_ID:-0}" --nshards "${SLURM_ARRAY_TASK_COUNT:-1}"
rc=$?
echo "<TASK>_END rc=$rc $(date)"
exit $rc
```

**Estimate before you submit, and write the estimate down.** Per-item cost × items ÷ parallelism
+ queue wait. Put the job ids and the ETA in `JOURNAL.md` and in the checkpoint (section 9). Then
stop; the grid does the work.

---

## 6. Nextflow: when it helps, how we run it, and what it does not do

**When.** A pipeline of three or more stages over many cases, mostly on CPU, mostly other people's
tools: fetch → align → quantify → differential expression is Nextflow work, and the nf-core
pipelines are the route (rnaseq 3.22.2, differentialabundance 1.5.0, fetchngs 1.12.0, methylarray,
each pinned by revision). A GPU census that shares one list across mixed GPU types is already
built as Slurm arrays with atomic claims; do not rewrite it.

**How, on this grid** (the config block every u251 pipeline uses; copy it as `grid.config`):

```groovy
process {
  executor = 'slurm'; queue = 'reqp'; clusterOptions = '--qos=requeue'
  maxRetries = 3
  errorStrategy = { task.exitStatus in ((130..145) + 104 + (175..177)) ? 'retry' : 'finish' }
  resourceLimits = [ cpus: 40, memory: 240.GB, time: 96.h ]
}
executor { queueSize = 50; submitRateLimit = '20/1min' }
singularity {
  enabled = true; autoMounts = true
  cacheDir = '<CephFS>/singularity_cache'
  runOptions = '-B <CephFS>/<project>/tmp:/tmp'          // node-local /tmp is swept
  pullTimeout = '60 min'
}
```

The head job is one `sbatch` on `reqp --qos=requeue --requeue --open-mode=append`, 2–4 CPUs, days
of wall time. It owns **one launch directory per run** on CephFS (a different launch directory is a
different session and resumes nothing), sets `NXF_HOME`, `NXF_TEMP`, `TMPDIR` and the singularity
cache on CephFS, always passes `-resume -ansi-log false`, writes the exit code to `NEXTFLOW_EXIT`
and the pipeline commit to the log, and refuses to start if `git status --porcelain` is non-empty.
A check job chained `afterany` reads `NEXTFLOW_EXIT` and the hard checks before anything is deleted.

**What re-runs a cached task on `-resume`, and what does not** (from the Nextflow documentation
and our runs):

| change | re-runs? | what we do about it |
|---|---|---|
| the process `script:` text, after interpolation | yes | — |
| a `bin/` script **named** in the script block | yes | — |
| a `path` input (full path, mtime, size) | yes | copy with `cp -a`; rsync with `-t`; otherwise spurious re-runs |
| a `val` input or an `ext.args` string | yes, by string value | — |
| the **content** behind a path passed as a string | **no** | name the file by its own hash: `rat_exclusion_list.<sha16>.txt`, verify name == content on every run |
| the content behind a container tag or a sandbox directory | **no** | pin by digest; record the digest in the result |
| files read from absolute paths but not declared as inputs (R libraries, caches) | **no** | frozen copies, hashed outside Nextflow |
| `cpus`, `memory`, `time`, `queue`, `publishDir` | no | — |
| outputs already present in `storeDir` | skipped regardless of hash | never put a stage whose script may change under `storeDir` |
| a different launch directory | nothing resumes | one launch directory per run |

**The rule that follows.** Nextflow's task hash never reaches the paper. The producing task still
writes the `_run` block of section 4 into its result, and the trace is enabled with
`hash,native_id,process,tag,status,exit,attempt,container,workdir,script` so every task's Slurm job
id and cache key are on disk beside the results.

**A minimal skeleton** for segment → measure → results → manifest → compile. Untested; it follows the
documented semantics and the patterns above.

```groovy
params.cases = null; params.outdir = '<CephFS>/<study>/results'; params.code_sha = null

workflow {
  ch = Channel.fromPath(params.cases).splitCsv(header: true)
              .map { r -> tuple(r.case_id, file(r.ct, checkIfExists: true)) }
  SEGMENT(ch)
  MEASURE(SEGMENT.out.mask, file("${projectDir}/bin/measure.py"))   // the script is a path input: its content is hashed
  MANIFEST(MEASURE.out.json.collect())
  COMPILE(MANIFEST.out.runs, MEASURE.out.json.collect(), file("${projectDir}/paper"))
}
process SEGMENT {
  tag "$case_id"; label 'gpu'
  container '<CephFS>/containers/<engine>.sandbox'        // a path or a digest, never a moving tag
  input:  tuple val(case_id), path(ct)
  output: tuple val(case_id), path("${case_id}_seg.nii.gz"), emit: mask
  script: "segment.sh $ct ${case_id}_seg.nii.gz"
}
process MEASURE {
  tag "$case_id"; label 'cpu_small'; publishDir "${params.outdir}/measure", mode: 'copy'
  input:  tuple val(case_id), path(mask); path measure_py
  output: path "${case_id}.json", emit: json
  script: "python $measure_py $mask --code-sha ${params.code_sha} --session ${workflow.sessionId} > ${case_id}.json"
}
```

---

## 7. From results to manuscript

This is the chain the SchwingNet and U251 manuscripts compile through. Nothing in it is typed by
hand between the results file and the PDF.

**1. `results/<task>.json`** — your numbers plus `_run` (section 4).

**2. `numbers_manifest.json`** — one entry per number the manuscript quotes:

```json
"naming_lat_whole_cv": {
  "file": "results/eval_gate/closure/cv_v9/cv_v9.json",
  "pointer": "/families/pre:cv5_det/cells/LAT/kfull/exact_pct",
  "fmt": "pct1", "kind": "number",
  "job": "40456123",
  "prereg": "H1",
  "note": "Table 3 row 1; case-grouped five-fold"
}
```

`pointer` is an RFC 6901 JSON pointer into the file. `job` is a Slurm job id, digits only; free text
is refused. `prereg` names the hypothesis or measurement in `PREREG.md` this number answers, so the
audit can list every pre-registered item beside the number that closed it.

**3. In the tex, `\RESULT{key}`** and nothing else. This applies to **tables**, not just prose:
tables are written by a tool from the manifest (or their body is generated), never typed. As of
2026-09-27 the SchwingNet prose has 0 bare result numerals and the tables have 167, because the
check scanned only the prose. The check now covers every tex file.

**4. The build** runs the same steps every time, on the grid, one compile per directory:

```
results_macros.py            manifest -> generated/numbers.tex + numbers_audit.md (value, file, sha256, time per key)
results_macros.py --check    exit 1 on any pending key, any unused key, any bare numeral in any tex file
compose_figures.py --check   every figure panel's sha256 matches the recorded one
check_limits.py              the journal's word, abstract, figure, table and reference limits, measured on the built PDF
check_claim_checklist.py     every claim in CLAIMS_LEDGER.md has its evidence file and verdict
latexmk                      under flock
```

A missing result prints as red `XXX Result Pending-<job>` in the PDF; the strict build fails until
it is gone. Two copies (double-anonymised review, camera-ready) come from **one source** through
`\ifcameraready`. Page and word limits are measured by the build on the published format; the
submission form's count is meaningless against them.

**5. The closed loop.** Every paper has one `make reproduce`-style target that submits the arms,
collects the results, prints the tables the document quotes, and compares them with a headline
dictionary `{arm: (value, tolerance)}`, exiting non-zero on `MISSING` or `MOVED`. The model is
`make physics` in spinesurg-ct-nnunet: "a reproduction that cannot fail is not a reproduction."

**6. Figures and captions.** Captions are at most 60 words; the argument belongs in the text.
Every panel is drawn by a committed tool from a committed results file. Never the word
"origin".

---

## 8. Checking a number

The recurring failure in this lab is a number that is wrong but plausible. Three separate
estimators produced finite, reasonable values from the wrong bone, the wrong surface, or the wrong
label map, and none of them raised. Internal consistency did not catch any of them: the identity
PI = SS + PT held throughout an error that moved sacral slope by 9° and lordosis by 12°, because
both shared one bad landmark and the errors cancelled.

So a number is checked against something **outside** the computation, and the check is committed
beside the claim.

1. **A published value.** Every measure compares itself with a normative series; anything that
   fails is withheld, not disclosed as a caveat.
2. **Spread, not the median.** Canal depth and end-plate width both had medians near the published
   means at every level while 21 % of L3 canals read below any value ever reported in a living
   adult. Compare the SD with the widest published SD, and the share below a threshold with the
   published prevalence of the condition the threshold defines.
3. **Reproduce the definition, not the units.** A midsagittal chord at a named plane is not a
   maximum extent on a first slice that works.
4. **Render the mask.** Three analytically reasonable fixes to one measurement were all wrong in
   ways the numbers did not reveal; one render of the retained mask showed what was there. Look at
   every figure and every mask before believing the number under it.
5. **Test the tidy explanation.** The 28 % of cases with an identity violation had an innocent
   reading (anteverted pelvis, lost sign) that was wrong; the distribution showed a second surface.
6. **An independent implementation** where one exists (TotalSegmentator against ours; a published
   formula against the estimator).
7. **The verifier is committed beside the claim it verified.** The script that re-read 375 targets
   before a submission, the script that ordered a byline from the annotation ledgers, and the
   generator of the job record all lived in scratch folders. A student cannot re-run a check that is
   not in the repository, and one of those scripts had earlier produced a confident "nobody is
   missing" from a structural mistake (a dictionary parsed as a list).
8. **Say plainly what is not known.** "An unexplained failure in 128 records" is the preferred
   form; a guess at its cause is not.

**The four audits before a freeze.** Numbers (`results_macros.py --check`); figures
(`compose_figures.py --check`); claims (`CLAIMS_LEDGER.md`, every row with an evidence file and a
verdict); identity (`front_matter.json`, every field with `source` and `confirmed`; an unconfirmed
field prints a visible marker and holds the strict build at FAIL). A wrong department was printed
on manuscripts, cards, a datasheet and a model card before the confirmed flags existed.

---

## 9. Working with Claude: sessions, checkpoints, resume

Claude Code runs on the laptop; the grid does the computing. A session ends when its limit is hit,
so the state of the work must live in files, never in the conversation.

**Session start.** `git status` locally; `ssh -o BatchMode=yes grid hostname` (expect `warrior`);
`squeue -u $USER`; `git pull` on the grid; read the top block of `RESUME.md` and the last five lines
of `JOURNAL.md`; run `pipeline_state.py` where the project has one. Then decide what to do. Before
any step, check whether its output already exists; never redo finished work.

**Submit → estimate → checkpoint → stop.** An agent that submits returns the job ids, an ETA, and
the exact files to collect. That goes into the checkpoint, and the turn ends. No `while squeue`
loop beyond about ten minutes: on 2026-09-24 polling agents burned a session limit four times in
one day while the grid was doing the real work, and every relaunch re-ran agents whose outputs
already existed. On "check again" or "reactivate", one collect pass reads the table, collects only
what finished, submits only what is missing, updates the table, stops.

**The checkpoint block** at the top of `RESUME.md`, newest first (the top block is always the
resume point):

```markdown
## CHECKPOINT 2026-09-27 17:40 EDT (grid clock): <one-line state> (Greg: "<the directive, verbatim>")

DONE: <what exists, with paths, job ids, timestamps, and the sha256 of every frozen input>

PENDING JOBS
| job | what | submitted | ETA | output | collect step |
|---|---|---|---|---|---|

WHEN THE JOBS FINISH: 1. read <file> first; 2. <gate> stays pending until <file> exists; 3. rerun <exact command> if <condition>
WORKFLOWS: | run id | what | where results land | ; resume with Workflow({scriptPath, resumeFromRunId}); journal at <path>
DO NOT REDO: <the specific things a fresh session must not repeat>
NOTHING COMMITTED BY ANY WORKFLOW (or: commits <ids>)
FOR GREG / WAITING ON: <decisions only the PI can make; items waiting on collaborators>
LIMITS TO STATE: <the confounds every write-up of this must carry>
```

**Status is computed, not written.** A hand-written PENDING table listed a job as pending three
hours after `sacct` showed it cancelled. `tools/pipeline_state.py` declares, for every stage, the
artefact whose existence means it finished, and prints done / running / ready / blocked / failed
from the disk and the queue. When you add a stage, add it there; a stage that exists only in a
shell history is a stage that will be lost.

**Before cancelling anything**, write the job record (section 5, rule 12).

**Memory.** One fact per file, with a `Why` (the incident) and a `How to apply` (the command), and
a one-line pointer in `MEMORY.md`. The first entry of the index is the handoff note that names the
current resume files.

**Workflows** (multi-agent runs) are recorded in the checkpoint with their run id, script path and
journal path, so a new session can resume them without re-running finished agents.

---

## 10. Leaving, handover, credit

**Leaving a project** is a pull request, merged by the lead within a week, that does three things:

1. Appends a `HANDOVER <date> <name>` block to `JOURNAL.md`: what is done (paths, job ids,
   hashes), what is pending (the PENDING table), what must not be redone, where the frozen inputs
   are, and the one thing the next person will get wrong if nobody tells them.
2. Moves your name on the board card from `members` to `alumni`, and names who takes each of your
   open tasks (or marks them open).
3. If you are the lead: the co-lead becomes lead and a new co-lead is named in the same pull
   request. A project is never left without both.

**Credit is recorded as the work proceeds**, not reconstructed at the end: the annotation ledgers
(who reviewed which case), git history, `JOURNAL.md`, and the board's task lines. Authorship on
anything published follows the ICMJE criteria (substantial contribution to design, data or
analysis; drafting or critical revision; approval of the final version; accountability). Among
those who qualify, the middle of the byline is ordered by recorded volume (annotation ledgers,
merged tasks); first and senior authorship is set at the pre-registration and changed only in
`DEVIATIONS.md`. Every author's name, degrees, affiliation and role live in the manuscript's
`front_matter.json` with `source` and `confirmed`; nothing unconfirmed prints.

---

## 11. Checklists

**Before the first number**
- [ ] `PREREG.md` frozen, `PREREG.md.sha256` committed, the bars taken from published values
- [ ] the dataset passes the five IRB criteria or has its own filing; licence and DOI recorded
- [ ] identifiers read from `dataset_labels.json` of the named release; exclusions listed with reasons
- [ ] `env/<name>.lock.txt` written from the grid
- [ ] the board card exists with lead, co-lead, contact

**Before a freeze (a number becomes quotable)**
- [ ] every results file carries `_run` with job id, commit, script hash, input hashes, PREREG hash
- [ ] every quoted number has a manifest key with a digit-only `job` and a `prereg` item
- [ ] `results_macros.py --check` passes on every tex file, tables included
- [ ] every figure panel's hash recorded; every mask behind a headline number rendered and looked at
- [ ] each headline number checked against something outside the computation, and the check committed
- [ ] the environment lock regenerated; the code committed; the grid clone at the same commit

**Before a submission**
- [ ] `check_limits.py` passes on the built PDF; captions ≤ 60 words
- [ ] `CLAIMS_LEDGER.md` complete; `front_matter.json` all `confirmed: true`
- [ ] the `make reproduce` target ran clean from the committed tree
- [ ] `DEVIATIONS.md` current; failed bars reported as failures
- [ ] nothing private in the submission (weights, level-identification code, credentials, personal data)

**Before leaving a project**
- [ ] the HANDOVER block, the board change, the task reassignment — one pull request, merged

---

## Appendix A. The worked example: SchwingNet

The paper on naming vertebral levels from C-arm exposures is the reference implementation of the
chain. The repository is private; the shape is what matters.

| link | file | what it does |
|---|---|---|
| pre-registration | `REVISION_LOG3.md §13`, `PREREG_rules.md` | rules stated before the numbers; the ablation verdict cells (N = 5, 25, all × three corpora) were fixed in advance |
| results | `results/**/*.json` (e.g. `results/coverage/film_ncurve/ablation/ablation_read.json`) | one JSON per task; readers write them from committed tools |
| manifest | `SchwingNet/numbers_manifest.json` (79 keys) | key → file, pointer, format, job, note |
| macros | `SchwingNet/tools/results_macros.py` | `generated/numbers.tex`, `numbers_audit.md`, `pending.json`; `--check` |
| figures | `SchwingNet/tools/compose_figures.py` | panels → figures with recorded hashes |
| limits | `SchwingNet/tools/check_limits.py` | 3,000 words, 250-word abstract, 6 figures, 4 tables, 35 references |
| claims | `SchwingNet/CLAIMS_LEDGER.md` | every claim, its evidence file, its verdict, both directions |
| identity | `SchwingNet/packet_src/front_matter.json` | every author field with `source` and `confirmed` |
| build | `SchwingNet/slurm/compile.sh` | on the grid, under `flock`, two copies from one source |
| environment | `env/spineps.lock.txt` via `make env-lock` | commit, host, interpreter, torch, CUDA |
| state | `tools/pipeline_state.py` | stage status from disk predicates |
| closed loop | `make physics` (`tools/reproduce_physics.py`) | submit → collect → compare with the document → exit non-zero if a headline moved |
| resume | `docs/RESUME_*.md` newest-first blocks; `docs/grid_records/JOBS_RECORD_*.md` | the checkpoint and the job record |

The U251 multi-omics work is the same chain with Nextflow underneath (nf-core pipelines pinned by
revision, one head job per run, content-addressed inputs, `env.sh run_header` printing the PREREG
hash and every code file's sha256 before the first number).

---

## Appendix B. What is not yet true (so nobody assumes it)

Written 2026-09-27. Each line is a gap between this recipe and the repositories today, and who
closes it.

| gap | state | closes when |
|---|---|---|
| Tables through macros | SchwingNet tables carry 167 bare numerals; `--check` scanned only the prose | `results_macros.py --check` scans every tex file and the tables are tool-written (in progress) |
| `job` is a job id | 0 of the SchwingNet manifest's 79 keys begin with a Slurm job id; the field holds free text | the manifest loader refuses a non-numeric `job`; entries are repointed as each task is re-run |
| `_run` block in every result | the manifest-path JSONs (`cv_v9`, `film_ncurve`, `a5`, `power`, `det_fill`) carry no commit, job id or script hash | the producing tools call `run_record()` and are re-run |
| `prereg` field | no manifest entry names its pre-registered item | added with the loader change above |
| Compile lock on the grid | committed locally 2026-09-27; the grid checkout is behind | `git pull` on the grid (this session) |
| Pelvis decision gate | written and pre-stated; `DECISION.json` has not yet been produced once | the timing job completes |
| Verifiers committed | `verify_numbers.py`, `_roster5.py`, the job-record generator were scratch scripts | committed beside their claims |
| A grid data path students can read | the lab's CephFS group has two members; the PI's home is not group-readable | a group-readable export or ACL, decided by Greg |
| Student templates | `templates/slurm_job.sh` and `templates/CLAUDE.md` prescribed `-q primary`, `/tmp` scratch and `set -euo pipefail` against these rules | fixed 2026-09-27 with this recipe |
| One authorship rule | three statements existed (ledger volume; ICMJE; code pull requests) | section 10 states one; Greg confirms |
| A project board | projects were listed in five unlinked places with no lead, member or contact field | `board.json` + `BOARD.md`, from this recipe |
| Nextflow for the imaging pipelines | none of the imaging repositories runs Nextflow; the public tutorial says otherwise | the tutorial is corrected; Nextflow is adopted where section 6 says it helps |
| v11 on the public mirror | the Hugging Face mirror is at v10 (revision of 2026-09-23; `dataset_labels.json` still carries 29); Zenodo v10 was published 2026-09-07 | Greg publishes v11; then `IDEAS.md`, the templates and the onboarding text move to the v11 identifiers |
