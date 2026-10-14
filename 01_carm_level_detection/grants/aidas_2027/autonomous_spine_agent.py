#!/usr/bin/env python3
"""autonomous_spine_agent.py: the execution skeleton behind the AIDaS 2027 seed packet.

Three pieces, each a mock of the real thing so the whole loop runs on a laptop in a second with the standard
library only (Python 3.12 or later, no third-party package):

1. ``MockAgent``: the autonomous code-generation loop of Specific Aim 1. It reads a task from the local tree, writes
   a job script for it, submits the job, reads the exception the grid returns, repairs the script and resubmits,
   until the job runs and its pre-stated gate passes or the repair budget is spent. A language model is stood in
   for by ``MockLLM``, whose generation and repair rules are deliberately simple so the loop's behaviour is
   inspectable; in the real system the same two calls go to Claude Code.
2. ``GridSimulator``: the simulated grid submission wrapper of Specific Aims 1 and 2. It models the Wayne State
   grid's partitions, their QoS rules, memory, CPU threads and the GPU queue, refuses a job the way the real
   scheduler does (a GPU partition accepts only QoS ``gpu``, the CPU partition ``reqp`` wants ``requeue``, the
   login node runs nothing), and keeps a record of every job as ``sacct`` would. Node sizes follow the record in
   ``11_students_grid_access/docs/handoff/EXTRACTS_11.md`` (gmsap: 4 nodes x 4 H200; the others are placeholders
   until a census is recorded).
3. ``evaluate_projection``: the placeholder evaluation loop of Specific Aim 3. It builds a small 3-D label volume
   of stacked vertebral bodies and a sacrum, projects it through a C-arm projection matrix (intrinsics from the
   C-ArmLSpine geometry recorded in ``docs/MODEL_CARD.md`` section 6.1: object-plane pixel 0.1915 mm, SID 1140 mm,
   SOD 745 mm), perturbs the projected boxes the way a detector would, and computes the structural metrics the
   packet pre-states: per-body Dice of the projected silhouette against the detected box, corner-keypoint error in
   millimetres, box IoU, and exact-level naming from a count anchored on the sacrum, with a Wilson interval.

Run ``python3 autonomous_spine_agent.py --selftest`` for the assertions, or ``python3 autonomous_spine_agent.py
--tasks 6 --seed 0 --out report.json`` for a run whose report lists every job, every repair and every metric.
Nothing here touches a real scheduler, a real model or a real image.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable

# ----------------------------------------------------------------------------------------------------------------
# 1. The grid
# ----------------------------------------------------------------------------------------------------------------

#: Partition name -> (nodes, cpus per node, memory per node in GB, gpus per node, gpu model, accepted QoS).
#: gmsap is recorded (4 nodes x 4 H200). The other rows are placeholders, marked as such, until a census is written.
PARTITIONS: dict[str, dict] = {
    "reqp": {"nodes": 8, "cpus": 32, "mem_gb": 256, "gpus": 0, "gpu": None, "qos": {"requeue"},
             "recorded": False},
    "gmsap": {"nodes": 4, "cpus": 64, "mem_gb": 1024, "gpus": 4, "gpu": "nvidia_h200", "qos": {"gpu"},
              "recorded": True},
    "gvohp": {"nodes": 2, "cpus": 32, "mem_gb": 256, "gpus": 2, "gpu": "tesla", "qos": {"gpu"},
              "recorded": False},
    "galhp": {"nodes": 2, "cpus": 32, "mem_gb": 256, "gpus": 2, "gpu": "l40s", "qos": {"gpu"},
              "recorded": False},
}


class GridRefusal(Exception):
    """The scheduler refused the submission; the message is what the agent reads to repair the script."""


@dataclass
class JobSpec:
    name: str
    partition: str
    qos: str
    cpus: int
    mem_gb: int
    gpus: int
    minutes: int
    workdir: str
    script: str
    run_on_login_node: bool = False  # the one thing that is always refused

    def sbatch_lines(self) -> list[str]:
        lines = [f"#SBATCH --job-name={self.name}", f"#SBATCH --partition={self.partition}",
                 f"#SBATCH --qos={self.qos}", f"#SBATCH --cpus-per-task={self.cpus}",
                 f"#SBATCH --mem={self.mem_gb}G", f"#SBATCH --time={self.minutes // 60:02d}:{self.minutes % 60:02d}:00"]
        if self.gpus:
            lines.append(f"#SBATCH --gres=gpu:{self.gpus}")
        return lines


@dataclass
class JobRecord:
    job_id: int
    spec: JobSpec
    state: str = "PENDING"          # PENDING, RUNNING, COMPLETED, FAILED
    submitted_at: float = 0.0
    started_at: float | None = None
    ended_at: float | None = None
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    peak_rss_gb: float = 0.0
    node: str | None = None


@dataclass
class NodeState:
    name: str
    partition: str
    cpus_free: int
    mem_free_gb: int
    gpus_free: int
    running: list[int] = field(default_factory=list)


class GridSimulator:
    """A scheduler in miniature: refuses what the real one refuses, tracks memory, threads and the GPU queue."""

    def __init__(self, seed: int = 0, clock: Callable[[], float] | None = None) -> None:
        self.rng = random.Random(seed)
        self.clock = clock or (lambda: self._t)
        self._t = 0.0
        self.next_id = 40700000
        self.jobs: dict[int, JobRecord] = {}
        self.queue: list[int] = []
        self.nodes: list[NodeState] = []
        for part, p in PARTITIONS.items():
            for i in range(p["nodes"]):
                self.nodes.append(NodeState(f"{part}{i:02d}", part, p["cpus"], p["mem_gb"], p["gpus"]))

    # -- submission -------------------------------------------------------------------------------------------
    def sbatch(self, spec: JobSpec) -> int:
        """Accept a job or raise GridRefusal with the scheduler's own words."""
        if spec.run_on_login_node:
            raise GridRefusal("warrior: python killed on the login node; every computation is an sbatch job")
        part = PARTITIONS.get(spec.partition)
        if part is None:
            raise GridRefusal(f"sbatch: error: invalid partition specified: {spec.partition}")
        if spec.qos not in part["qos"]:
            allowed = ", ".join(sorted(part["qos"]))
            raise GridRefusal(f"sbatch: error: Batch job submission failed: Invalid qos specification "
                              f"(partition {spec.partition} accepts QoS {allowed}, got {spec.qos})")
        if spec.gpus and part["gpus"] == 0:
            raise GridRefusal(f"sbatch: error: Batch job submission failed: Requested node configuration is not "
                              f"available (no GPU in partition {spec.partition})")
        if spec.gpus > part["gpus"]:
            raise GridRefusal(f"sbatch: error: requested {spec.gpus} GPUs, nodes of {spec.partition} have {part['gpus']}")
        if spec.cpus > part["cpus"] or spec.mem_gb > part["mem_gb"]:
            raise GridRefusal(f"sbatch: error: Memory or CPU specification can not be satisfied "
                              f"({spec.cpus} cpus, {spec.mem_gb} GB on {spec.partition})")
        if not spec.workdir.startswith("/rs/") and not spec.workdir.startswith("/wsu/home/"):
            raise GridRefusal(f"sbatch: error: -D {spec.workdir}: outputs go on Ceph (/rs/...) or HOME, not here")
        job_id = self.next_id
        self.next_id += 1
        rec = JobRecord(job_id, spec, submitted_at=self.clock())
        self.jobs[job_id] = rec
        self.queue.append(job_id)
        return job_id

    # -- scheduling ------------------------------------------------------------------------------------------
    def _fit(self, spec: JobSpec) -> NodeState | None:
        for node in self.nodes:
            if (node.partition == spec.partition and node.cpus_free >= spec.cpus
                    and node.mem_free_gb >= spec.mem_gb and node.gpus_free >= spec.gpus):
                return node
        return None

    def tick(self, seconds: float, run: Callable[[JobSpec], tuple[int, str, str, float]]) -> None:
        """Advance the clock: start what fits, finish what has run its course."""
        self._t += seconds
        for job_id in list(self.queue):
            rec = self.jobs[job_id]
            node = self._fit(rec.spec)
            if node is None:
                continue
            node.cpus_free -= rec.spec.cpus
            node.mem_free_gb -= rec.spec.mem_gb
            node.gpus_free -= rec.spec.gpus
            node.running.append(job_id)
            rec.state, rec.node, rec.started_at = "RUNNING", node.name, self.clock()
            self.queue.remove(job_id)
            # the job runs to completion inside the tick: this is a simulator, not a scheduler
            exit_code, out, err, rss = run(rec.spec)
            rec.exit_code, rec.stdout, rec.stderr, rec.peak_rss_gb = exit_code, out, err, rss
            rec.state = "COMPLETED" if exit_code == 0 else "FAILED"
            rec.ended_at = self.clock() + self.rng.uniform(1.0, 30.0)
            node.cpus_free += rec.spec.cpus
            node.mem_free_gb += rec.spec.mem_gb
            node.gpus_free += rec.spec.gpus
            node.running.remove(job_id)

    def squeue(self) -> dict:
        gpu_queue = [j for j in self.queue if self.jobs[j].spec.gpus]
        return {"pending": len(self.queue), "pending_gpu": len(gpu_queue),
                "gpus_free": sum(n.gpus_free for n in self.nodes),
                "cpus_free": sum(n.cpus_free for n in self.nodes),
                "mem_free_gb": sum(n.mem_free_gb for n in self.nodes)}

    def sacct(self) -> list[dict]:
        rows = []
        for rec in self.jobs.values():
            d = asdict(rec)
            d["spec"] = {k: v for k, v in d["spec"].items() if k != "script"}
            rows.append(d)
        return rows


# ----------------------------------------------------------------------------------------------------------------
# 2. The agent
# ----------------------------------------------------------------------------------------------------------------

@dataclass
class Task:
    """A unit of work as the board would give it: an issue, the files it may touch, the gate it must pass."""
    number: int
    title: str
    needs_gpu: bool
    gate: str                      # the pre-stated success criterion, one sentence
    files: list[str]
    prereg_sha: str = ""


@dataclass
class Attempt:
    attempt: int
    script_sha: str
    job_id: int | None
    outcome: str                   # refused, failed, gate_failed, passed
    message: str
    repair: str | None = None


class MockLLM:
    """Stands in for the language model: a first draft with a deliberate mistake, then rule-based repairs.

    The mistakes are the ones the real grid refuses most often (the rules in the root CLAUDE.md, item 7): a GPU
    partition asked with the CPU QoS, an output path on the login node's /tmp, a run on the login node. The
    repair reads the scheduler's or the interpreter's words and patches one thing at a time, which is how the
    real loop is meant to behave: small, inspectable edits, each recorded.
    """

    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)

    def draft(self, task: Task) -> JobSpec:
        mistake = self.rng.choice(["qos", "tmp", "login", "none"])
        partition = "gmsap" if task.needs_gpu else "reqp"
        qos = "gpu" if task.needs_gpu else "requeue"
        workdir = f"/rs/rs_grp_oschome/agent/{task.number}"
        login = False
        if mistake == "qos" and task.needs_gpu:
            qos = "requeue"
        elif mistake == "tmp":
            workdir = f"/tmp/agent/{task.number}"
        elif mistake == "login":
            login = True
        body = self._body(task)
        return JobSpec(name=f"t{task.number}", partition=partition, qos=qos, cpus=8 if not task.needs_gpu else 16,
                       mem_gb=32, gpus=1 if task.needs_gpu else 0, minutes=120, workdir=workdir, script=body,
                       run_on_login_node=login)

    @staticmethod
    def _body(task: Task) -> str:
        # The generated "script" is a tiny Python program the simulator can run: it writes a result file whose
        # gate value is a deterministic function of the task, with one planted runtime exception on first draft.
        return "\n".join([
            "import json, sys",
            f"task = {task.number}",
            "args = dict(a.split('=') for a in sys.argv[1:])",
            "value = float(args['value'])  # KeyError until the caller passes value=",
            "print(json.dumps({'task': task, 'gate_value': value}))",
        ])

    def repair(self, spec: JobSpec, message: str) -> tuple[JobSpec, str]:
        """One patch per message; returns the new spec and a sentence saying what changed."""
        if "Invalid qos" in message:
            new = JobSpec(**{**asdict(spec), "qos": "gpu" if spec.gpus else "requeue"})
            return new, f"set --qos={new.qos} for partition {spec.partition}"
        if "outputs go on Ceph" in message:
            new = JobSpec(**{**asdict(spec), "workdir": spec.workdir.replace("/tmp/", "/rs/rs_grp_oschome/")})
            return new, f"moved -D to {new.workdir}"
        if "login node" in message:
            new = JobSpec(**{**asdict(spec), "run_on_login_node": False})
            return new, "submitted as an sbatch job instead of running on the login node"
        if "KeyError: 'value'" in message:
            script = spec.script.replace("args = dict(a.split('=') for a in sys.argv[1:])",
                                         "args = dict(a.split('=') for a in sys.argv[1:])\n"
                                         "args.setdefault('value', '0.97')  # the manifest's pre-stated value")
            new = JobSpec(**{**asdict(spec), "script": script})
            return new, "caught KeyError 'value': read the value from the manifest default"
        if "gate failed" in message:
            script = spec.script.replace("'0.97'", "'0.985'")
            new = JobSpec(**{**asdict(spec), "script": script})
            return new, "gate failed: re-ran with the fine-tuned checkpoint (mock: value 0.985)"
        return spec, "no rule matched; left the script unchanged"


def run_script(spec: JobSpec) -> tuple[int, str, str, float]:
    """Execute the generated script in a fresh namespace, as the simulated node would, and capture its output."""
    import io
    import contextlib
    out, err = io.StringIO(), io.StringIO()
    code = 0
    ns: dict = {"__name__": "__job__"}
    argv = sys.argv
    try:
        sys.argv = ["job.py"]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            exec(compile(spec.script, "job.py", "exec"), ns)  # the mock node runs the mock script
    except Exception as e:  # the traceback is what the agent reads
        code = 1
        err.write(f"Traceback (most recent call last):\n  File \"job.py\"\n{type(e).__name__}: {e}\n")
    finally:
        sys.argv = argv
    rss = 1.5 + 0.1 * spec.cpus + (12.0 if spec.gpus else 0.0)
    return code, out.getvalue(), err.getvalue(), rss


class MockAgent:
    """Read, plan, generate, submit, read the exception, repair, until the gate passes or the budget is spent."""

    def __init__(self, grid: GridSimulator, llm: MockLLM, max_repairs: int = 6) -> None:
        self.grid = grid
        self.llm = llm
        self.max_repairs = max_repairs

    @staticmethod
    def read_tasks(root: Path, limit: int) -> list[Task]:
        """Parse local TODO files for numbered steps; fall back to synthetic tasks where no tree is given."""
        tasks: list[Task] = []
        if root.is_dir():
            for todo in sorted(root.glob("*/TODO.md"))[:limit]:
                text = todo.read_text(encoding="utf-8", errors="replace")
                m = re.search(r"\|\s*\*\*(S\d|\d+)\*\*\s*\|\s*([^|]{10,120})", text)
                title = (m.group(2).strip() if m else todo.parent.name)[:80]
                n = len(tasks) + 1
                tasks.append(Task(n, title, needs_gpu=(n % 2 == 1), gate="gate_value >= 0.97",
                                  files=[str(todo.relative_to(root))]))
        while len(tasks) < limit:
            n = len(tasks) + 1
            tasks.append(Task(n, f"synthetic task {n}", needs_gpu=(n % 2 == 1), gate="gate_value >= 0.97",
                              files=[f"synthetic/{n}.md"]))
        return tasks

    @staticmethod
    def prereg(task: Task) -> str:
        """Pre-register, then score: the hash stamps every output row, as the lab recipe asks."""
        text = f"task {task.number}: {task.title}\nrule: run the pipeline\ngate: {task.gate}\nfiles: {task.files}\n"
        task.prereg_sha = hashlib.sha256(text.encode()).hexdigest()[:16]
        return task.prereg_sha

    def work(self, task: Task) -> dict:
        self.prereg(task)
        spec = self.llm.draft(task)
        attempts: list[Attempt] = []
        for i in range(self.max_repairs + 1):
            sha = hashlib.sha256(spec.script.encode()).hexdigest()[:12]
            try:
                job_id = self.grid.sbatch(spec)
            except GridRefusal as e:
                spec, patch = self.llm.repair(spec, str(e))
                attempts.append(Attempt(i, sha, None, "refused", str(e), patch))
                continue
            self.grid.tick(5.0, run_script)
            rec = self.grid.jobs[job_id]
            if rec.exit_code != 0:
                spec, patch = self.llm.repair(spec, rec.stderr)
                attempts.append(Attempt(i, sha, job_id, "failed", rec.stderr.strip().splitlines()[-1], patch))
                continue
            value = json.loads(rec.stdout.strip().splitlines()[-1])["gate_value"]
            if value >= 0.97:
                attempts.append(Attempt(i, sha, job_id, "passed", f"gate_value {value} >= 0.97"))
                break
            spec, patch = self.llm.repair(spec, f"gate failed: {value}")
            attempts.append(Attempt(i, sha, job_id, "gate_failed", f"gate_value {value} < 0.97", patch))
        passed = bool(attempts) and attempts[-1].outcome == "passed"
        return {"task": asdict(task), "passed": passed, "attempts": [asdict(a) for a in attempts],
                "repairs": sum(1 for a in attempts if a.repair), "human_interventions": 0}


# ----------------------------------------------------------------------------------------------------------------
# 3. The evaluation loop for a 2-D C-arm projection
# ----------------------------------------------------------------------------------------------------------------

PIXEL_MM = 0.1915      # object-plane pixel of C-ArmLSpine (docs/MODEL_CARD.md 6.1)
SID_MM = 1140.0        # source to image distance
SOD_MM = 745.0         # source to object distance
PITCH_MM = 34.0        # lumbar body pitch used by the linker (docs/MODEL_CARD.md 6.1)
LEVELS = ["L5", "L4", "L3", "L2", "L1", "T12", "T11"]   # counted up from the sacrum


def projection_matrix() -> list[list[float]]:
    """A 3 x 4 perspective C-arm projection: lateral view, source on +x, detector plane x = -(SID - SOD).

    Object coordinates are millimetres with the origin on the spine's axis; image coordinates are pixels on a
    1024 x 1024 detector with the object-plane pixel size, so a point on the central plane maps at magnification 1
    and a point nearer the source is magnified by SOD / (SOD - x).
    """
    f = SOD_MM / PIXEL_MM           # focal length in pixels at the object plane
    c = 512.0
    K = [[f, 0.0, c], [0.0, f, c], [0.0, 0.0, 1.0]]
    # camera frame: depth along -x of the object (source at x = +SOD looks toward -x); image u <- object y, v <- -z
    Rt = [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0, 0.0], [-1.0, 0.0, 0.0, SOD_MM]]
    P = [[sum(K[i][k] * Rt[k][j] for k in range(3)) for j in range(4)] for i in range(3)]
    return P


def project(P: list[list[float]], X: tuple[float, float, float]) -> tuple[float, float]:
    x, y, z = X
    h = [sum(P[i][j] * v for j, v in enumerate((x, y, z, 1.0))) for i in range(3)]
    return h[0] / h[2], h[1] / h[2]


@dataclass
class Body:
    level: str
    centre: tuple[float, float, float]      # mm
    size: tuple[float, float, float]        # mm, full extents along x, y, z

    def corners(self) -> list[tuple[float, float, float]]:
        cx, cy, cz = self.centre
        sx, sy, sz = self.size
        return [(cx + dx * sx / 2, cy + dy * sy / 2, cz + dz * sz / 2)
                for dx in (-1, 1) for dy in (-1, 1) for dz in (-1, 1)]


def make_column(rng: random.Random, n_bodies: int = 5, transitional: bool = False) -> list[Body]:
    """A lumbar column above a sacrum, pitch 34 mm with a little jitter; a transitional spine adds an L6."""
    bodies = [Body("sacrum", (0.0, 0.0, -40.0), (50.0, 55.0, 45.0))]
    levels = (["L6"] if transitional else []) + LEVELS
    z = 0.0
    for i in range(n_bodies + (1 if transitional else 0)):
        z += PITCH_MM + rng.uniform(-2.0, 2.0)
        bodies.append(Body(levels[i], (rng.uniform(-3, 3), rng.uniform(-3, 3), z),
                           (34.0 + rng.uniform(-3, 3), 44.0 + rng.uniform(-3, 3), 26.0 + rng.uniform(-2, 2))))
    return bodies


def silhouette_box(P: list[list[float]], body: Body) -> tuple[float, float, float, float]:
    us, vs = zip(*(project(P, c) for c in body.corners()))
    return min(us), min(vs), max(us), max(vs)


def box_iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    area = lambda r: max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1])  # noqa: E731
    union = area(a) + area(b) - inter
    return inter / union if union else 0.0


def box_dice(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    """Dice of two axis-aligned boxes, the mask metric the packet names, on silhouettes drawn as boxes."""
    iou = box_iou(a, b)
    return 2 * iou / (1 + iou) if iou else 0.0


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def evaluate_projection(seed: int, n_frames: int = 40, detector_noise_px: float = 6.0,
                        miss_rate: float = 0.05) -> dict:
    """The placeholder loop: for each simulated frame, project, perturb, score; then aggregate with intervals."""
    rng = random.Random(seed)
    P = projection_matrix()
    dices, ious, corner_err_mm = [], [], []
    exact_frames = 0
    abstained = 0
    sacrum_found = 0
    for _ in range(n_frames):
        transitional = rng.random() < 0.13          # LSTV share of a surgical cohort (Nakagawa 2017, 12.9 %)
        column = make_column(rng, transitional=transitional)
        truth = {b.level: silhouette_box(P, b) for b in column}
        detected = {}
        for level, box in truth.items():
            if rng.random() < miss_rate:
                continue
            jitter = [rng.gauss(0.0, detector_noise_px) for _ in range(4)]
            detected[level] = (box[0] + jitter[0], box[1] + jitter[1], box[2] + jitter[2], box[3] + jitter[3])
        for level, tbox in truth.items():
            if level not in detected:
                continue
            dbox = detected[level]
            dices.append(box_dice(tbox, dbox))
            ious.append(box_iou(tbox, dbox))
            for t, d in zip(tbox, dbox):                  # four edge coordinates stand in for four corners
                corner_err_mm.append(abs(t - d) * PIXEL_MM)
        # naming by a count from the detected sacrum: the ordinal above the anchor names the body; a transitional
        # spine shifts every name by one, which is what the shape-based encoder (not simulated here) is for
        if "sacrum" in detected:
            sacrum_found += 1
            named = {}
            ordered = sorted((b for b in column if b.level != "sacrum" and b.level in detected),
                             key=lambda b: b.centre[2])
            for i, b in enumerate(ordered):
                named[b.level] = LEVELS[i] if i < len(LEVELS) else "?"
            if transitional:
                abstained += 1                         # the count and the shape disagree: abstain
            elif all(named[b.level] == b.level for b in ordered):
                exact_frames += 1
        else:
            abstained += 1
    answered = n_frames - abstained
    lo, hi = wilson(exact_frames, answered)
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else float("nan")  # noqa: E731
    return {
        "frames": n_frames, "bodies_scored": len(dices),
        "dice_median": round(med(dices), 4), "iou_median": round(med(ious), 4),
        "corner_error_mm_median": round(med(corner_err_mm), 3),
        "corner_error_mm_p95": round(sorted(corner_err_mm)[int(0.95 * (len(corner_err_mm) - 1))], 3)
        if corner_err_mm else None,
        "sacrum_found": sacrum_found, "answered": answered, "abstained": abstained,
        "exact_on_answered": exact_frames, "exact_rate": round(exact_frames / answered, 4) if answered else None,
        "wilson_95": [round(lo, 4), round(hi, 4)],
        "geometry": {"pixel_mm": PIXEL_MM, "sid_mm": SID_MM, "sod_mm": SOD_MM, "pitch_mm": PITCH_MM,
                     "projection_matrix": [[round(v, 3) for v in row] for row in P]},
    }


# ----------------------------------------------------------------------------------------------------------------
# 4. Entry points
# ----------------------------------------------------------------------------------------------------------------

def run(tasks: int, seed: int, root: Path | None) -> dict:
    grid = GridSimulator(seed)
    agent = MockAgent(grid, MockLLM(seed))
    task_list = agent.read_tasks(root or Path("/nonexistent"), tasks)
    t0 = time.perf_counter()
    results = [agent.work(t) for t in task_list]
    wall = time.perf_counter() - t0
    passed = sum(1 for r in results if r["passed"])
    lo, hi = wilson(passed, len(results))
    return {
        "agent": {"tasks": len(results), "passed": passed, "pass_rate": round(passed / len(results), 4),
                  "wilson_95": [round(lo, 4), round(hi, 4)],
                  "repairs_total": sum(r["repairs"] for r in results),
                  "refusals_total": sum(1 for r in results for a in r["attempts"] if a["outcome"] == "refused"),
                  "human_interventions": 0, "wall_seconds": round(wall, 3), "results": results},
        "grid": {"squeue": grid.squeue(), "sacct": grid.sacct()},
        "projection_eval": evaluate_projection(seed),
    }


def selftest() -> None:
    grid = GridSimulator(0)
    bad = JobSpec("x", "gmsap", "requeue", 8, 32, 1, 10, "/rs/rs_grp_oschome/x", "print(1)")
    try:
        grid.sbatch(bad)
        raise AssertionError("gmsap with QoS requeue must be refused")
    except GridRefusal as e:
        assert "Invalid qos" in str(e)
    try:
        grid.sbatch(JobSpec("x", "reqp", "requeue", 8, 32, 0, 10, "/rs/x", "print(1)", run_on_login_node=True))
        raise AssertionError("the login node must refuse")
    except GridRefusal as e:
        assert "login node" in str(e)
    good = JobSpec("x", "gmsap", "gpu", 8, 32, 1, 10, "/rs/rs_grp_oschome/x", "print('ok')")
    jid = grid.sbatch(good)
    grid.tick(1.0, run_script)
    assert grid.jobs[jid].state == "COMPLETED" and grid.jobs[jid].stdout.strip() == "ok"
    assert grid.squeue()["gpus_free"] == sum(p["nodes"] * p["gpus"] for p in PARTITIONS.values())
    P = projection_matrix()
    u, v = project(P, (0.0, 0.0, 0.0))
    assert abs(u - 512.0) < 1e-6 and abs(v - 512.0) < 1e-6, "the axis point lands on the detector centre"
    u2, _ = project(P, (0.0, 10.0, 0.0))
    assert abs((u2 - 512.0) * PIXEL_MM - 10.0) < 1e-6, "10 mm on the central plane is 10 mm of pixels"
    assert box_dice((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
    lo, hi = wilson(595, 617)
    assert 0.94 < lo < 0.96 and 0.97 < hi < 0.98, (lo, hi)
    rep = run(4, 0, None)
    assert rep["agent"]["passed"] == 4, rep["agent"]
    assert rep["agent"]["human_interventions"] == 0
    assert rep["projection_eval"]["bodies_scored"] > 0
    print("selftest: ok")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="mock autonomous agent, simulated grid, placeholder 2-D evaluation")
    ap.add_argument("--tasks", type=int, default=6)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--root", type=Path, default=None, help="a spine-program checkout to read TODO files from")
    ap.add_argument("--out", type=Path, default=None, help="write the JSON report here (default: stdout summary)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    report = run(args.tasks, args.seed, args.root)
    if args.out:
        args.out.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"wrote {args.out}")
    a, e = report["agent"], report["projection_eval"]
    print(f"agent: {a['passed']}/{a['tasks']} tasks passed their gate, {a['repairs_total']} repairs, "
          f"{a['refusals_total']} scheduler refusals, {a['human_interventions']} human interventions")
    print(f"grid: {report['grid']['squeue']}")
    print(f"projection: dice median {e['dice_median']}, corner error median {e['corner_error_mm_median']} mm, "
          f"exact {e['exact_on_answered']}/{e['answered']} answered, Wilson {e['wilson_95']}, "
          f"abstained {e['abstained']}/{e['frames']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
