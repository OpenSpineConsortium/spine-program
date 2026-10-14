#!/usr/bin/env python3
"""autonomous_spine_agent.py: the execution skeleton behind the AIDaS 2027 seed packet.

Three pieces, each a mock of the real thing so the whole loop runs on a laptop in a second with the standard
library only (Python 3.12 or later, no third-party package). Run it on a laptop or as an sbatch job, never on the
grid's login node (root CLAUDE.md rule 7). Every number it prints is simulated; the packet quotes none of them.

1. ``MockAgent``: the autonomous code-generation loop of Specific Aim 1. It reads a task from the local tree,
   pre-registers the rule, the gate and the inputs as one hash, writes a job script, submits the job, reads the
   message the grid returns, repairs the script and resubmits, until the job runs and its gate passes, the repair
   budget is spent, or no repair rule matches, which hands the task to a person and is counted as an intervention.
   A language model is stood in for by ``MockLLM``, whose drafting and repair rules are deliberately simple so the
   loop's behaviour is inspectable; in the real system the same two calls go to Claude Code.
2. ``GridSimulator``: the simulated grid submission wrapper of Specific Aims 1 and 2. It models the Wayne State
   grid's partitions and their QoS rules, tracks memory, CPU threads and the GPU queue, refuses a job the way the
   real scheduler does (a GPU partition accepts only QoS ``gpu``, the CPU partition ``reqp`` wants ``requeue``, the
   login node runs nothing), lets a job span several clock ticks so that a queue can form, and keeps a record of
   every job as ``sacct`` would, stamped with the task's pre-registration hash. What the record supports is marked
   per field in ``PARTITIONS``; the rest are placeholders until a census is written.
3. ``evaluate_projection``: the placeholder evaluation loop of Specific Aim 3. It builds a small 3-D label volume
   of stacked vertebral bodies and a sacrum, projects it through a C-arm projection matrix at the C-ArmLSpine
   geometry (``docs/MODEL_CARD.md`` section 6.1), keeps the bodies that fall on the detector, perturbs their boxes
   the way a detector would, and computes the structural metrics the packet names: per-body Dice and IoU of the
   projected silhouette box against the detected box, corner-keypoint error in millimetres, and exact-level naming
   from a count anchored on the detected sacrum, with a Wilson interval.

Run ``python3 autonomous_spine_agent.py --selftest`` for the assertions, or ``python3 autonomous_spine_agent.py
--tasks 6 --seed 0 --out report.json`` for a run whose report lists every job, every repair and every metric.
Nothing here touches a real scheduler, a real model or a real image.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import posixpath
import random
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

# ----------------------------------------------------------------------------------------------------------------
# 1. The grid
# ----------------------------------------------------------------------------------------------------------------

#: Partition name -> nodes, cpus per node, memory per node in GB, gpus per node, gpu model, accepted QoS, the
#: longest wall time in minutes, and ``recorded``: the fields the record supports
#: (11_students_grid_access/docs/handoff/EXTRACTS_11.md, the Slurm rows: reqp takes QoS requeue, secp takes
#: secondary with a 90-day wall, the GPU partitions take only QoS gpu, gmsap is 4 nodes x 4 H200, gvohp is Tesla
#: with the model not recorded, galhp is L40S). Every other value is a placeholder until a census is written.
PARTITIONS: dict[str, dict] = {
    "reqp": {"nodes": 8, "cpus": 32, "mem_gb": 256, "gpus": 0, "gpu": None, "qos": {"requeue"},
             "max_minutes": 7 * 24 * 60, "recorded": {"qos"}},
    "secp": {"nodes": 2, "cpus": 32, "mem_gb": 256, "gpus": 0, "gpu": None, "qos": {"secondary"},
             "max_minutes": 90 * 24 * 60, "recorded": {"qos", "max_minutes"}},
    "gmsap": {"nodes": 4, "cpus": 64, "mem_gb": 1024, "gpus": 4, "gpu": "nvidia_h200", "qos": {"gpu"},
              "max_minutes": 7 * 24 * 60, "recorded": {"nodes", "gpus", "gpu", "qos"}},
    "gvohp": {"nodes": 2, "cpus": 32, "mem_gb": 256, "gpus": 2, "gpu": "tesla", "qos": {"gpu"},
              "max_minutes": 7 * 24 * 60, "recorded": {"gpu", "qos"}},
    "galhp": {"nodes": 2, "cpus": 32, "mem_gb": 256, "gpus": 2, "gpu": "l40s", "qos": {"gpu"},
              "max_minutes": 7 * 24 * 60, "recorded": {"gpu", "qos"}},
}
RESEARCH_VOLUMES = ("/rs/", "/wsu/home/")       # where a job's working directory may be (root CLAUDE.md rule 7)
TICK_SECONDS = 60.0                              # the clock step the agent waits by
MAX_WAIT_TICKS = 20_000                          # about two weeks of mock time, longer than any wall limit here


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
    prereg_sha: str = ""             # the task's pre-registration hash, carried into the scheduler's record

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
    state: str = "PENDING"          # PENDING, RUNNING, COMPLETED, FAILED, TIMEOUT
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


Runner = Callable[[JobSpec], tuple[int, str, str, float]]


class GridSimulator:
    """A scheduler in miniature: refuses what the real one refuses, tracks memory, threads and the GPU queue.

    A job starts when a node of its partition has the cores, memory and GPUs free, runs for a mock duration drawn
    once at its start, and ends on the first tick after that; until then it holds its node's resources and later
    submissions queue behind it. The script's outcome is computed at the start and revealed at the end.
    """

    def __init__(self, seed: int = 0, run: Runner | None = None) -> None:
        self.rng = random.Random(seed)
        self.run = run or run_script
        self._t = 0.0
        self.next_id = 40700000
        self.jobs: dict[int, JobRecord] = {}
        self.queue: list[int] = []
        self.nodes: list[NodeState] = []
        self._outcome: dict[int, tuple[int, str, str, float]] = {}
        for part, p in PARTITIONS.items():
            for i in range(p["nodes"]):
                self.nodes.append(NodeState(f"{part}{i:02d}", part, p["cpus"], p["mem_gb"], p["gpus"]))

    def now(self) -> float:
        return self._t

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
        if spec.cpus < 1 or spec.mem_gb < 1 or spec.gpus < 0 or spec.minutes < 1:
            raise GridRefusal(f"sbatch: error: Invalid resource specification ({spec.cpus} cpus, {spec.mem_gb} GB, "
                              f"{spec.gpus} gpus, {spec.minutes} minutes)")
        if spec.minutes > part["max_minutes"]:
            raise GridRefusal(f"sbatch: error: Requested time limit is invalid (exceeds partition "
                              f"{spec.partition}'s {part['max_minutes']} minutes)")
        if spec.gpus and part["gpus"] == 0:
            raise GridRefusal(f"sbatch: error: Batch job submission failed: Requested node configuration is not "
                              f"available (no GPU in partition {spec.partition})")
        if spec.gpus > part["gpus"]:
            raise GridRefusal(f"sbatch: error: requested {spec.gpus} GPUs, nodes of {spec.partition} have {part['gpus']}")
        if spec.cpus > part["cpus"] or spec.mem_gb > part["mem_gb"]:
            raise GridRefusal(f"sbatch: error: Memory or CPU specification can not be satisfied "
                              f"({spec.cpus} cpus, {spec.mem_gb} GB on {spec.partition})")
        workdir = posixpath.normpath(spec.workdir)
        if not workdir.startswith(RESEARCH_VOLUMES):
            raise GridRefusal(f"sbatch: error: -D {spec.workdir}: outputs go on Ceph (/rs/...) or HOME, not here")
        job_id = self.next_id
        self.next_id += 1
        self.jobs[job_id] = JobRecord(job_id, spec, submitted_at=self.now())
        self.queue.append(job_id)
        return job_id

    # -- scheduling ------------------------------------------------------------------------------------------
    def _fit(self, spec: JobSpec) -> NodeState | None:
        for node in self.nodes:
            if (node.partition == spec.partition and node.cpus_free >= spec.cpus
                    and node.mem_free_gb >= spec.mem_gb and node.gpus_free >= spec.gpus):
                return node
        return None

    def _finish(self, node: NodeState, rec: JobRecord) -> None:
        exit_code, out, err, rss = self._outcome.pop(rec.job_id)
        rec.exit_code, rec.stdout, rec.stderr, rec.peak_rss_gb = exit_code, out, err, rss
        rec.state = "TIMEOUT" if exit_code == 124 else "COMPLETED" if exit_code == 0 else "FAILED"
        node.cpus_free += rec.spec.cpus
        node.mem_free_gb += rec.spec.mem_gb
        node.gpus_free += rec.spec.gpus
        node.running.remove(rec.job_id)

    def _start(self, node: NodeState, rec: JobRecord) -> None:
        node.cpus_free -= rec.spec.cpus
        node.mem_free_gb -= rec.spec.mem_gb
        node.gpus_free -= rec.spec.gpus
        node.running.append(rec.job_id)
        rec.state, rec.node, rec.started_at = "RUNNING", node.name, self.now()
        self.queue.remove(rec.job_id)
        exit_code, out, err, rss = self.run(rec.spec)
        duration = self.rng.uniform(60.0, 600.0)          # a mock run of one to ten minutes
        limit = rec.spec.minutes * 60.0
        if duration > limit:                               # the scheduler kills it at its wall limit
            exit_code, err = 124, err + "slurmstepd: error: JOB CANCELLED DUE TO TIME LIMIT\n"
            duration = limit
        self._outcome[rec.job_id] = (exit_code, out, err, rss)
        rec.ended_at = self.now() + duration

    def tick(self, seconds: float = TICK_SECONDS) -> None:
        """Advance the clock: end the jobs that have run their course, then start the queued jobs that fit."""
        self._t += seconds
        for node in self.nodes:
            for job_id in list(node.running):
                rec = self.jobs[job_id]
                if rec.ended_at is not None and rec.ended_at <= self.now():
                    self._finish(node, rec)
        for job_id in list(self.queue):
            rec = self.jobs[job_id]
            node = self._fit(rec.spec)
            if node is not None:
                self._start(node, rec)

    def wait(self, job_id: int, max_ticks: int = MAX_WAIT_TICKS) -> JobRecord:
        """Tick until the job has ended; a job still running after max_ticks is left as it stands."""
        rec = self.jobs[job_id]
        ticks = 0
        while rec.state in ("PENDING", "RUNNING") and ticks < max_ticks:
            self.tick()
            ticks += 1
        return rec

    def squeue(self) -> dict:
        gpu_queue = [j for j in self.queue if self.jobs[j].spec.gpus]
        return {"pending": len(self.queue), "pending_gpu": len(gpu_queue),
                "running": sum(len(n.running) for n in self.nodes),
                "gpus_free": sum(n.gpus_free for n in self.nodes),
                "cpus_free": sum(n.cpus_free for n in self.nodes),
                "mem_free_gb": sum(n.mem_free_gb for n in self.nodes)}

    def sacct(self) -> list[dict]:
        rows = []
        for rec in self.jobs.values():
            d = asdict(rec)
            d["spec"] = {k: v for k, v in d["spec"].items() if k != "script"}
            d["prereg_sha"] = rec.spec.prereg_sha
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
    gate: str                      # the pre-stated success criterion, one sentence, e.g. "gate_value >= 0.97"
    files: list[str]
    prereg_sha: str = ""

    def threshold(self) -> float:
        m = re.search(r"gate_value\s*>=\s*([0-9]+(?:\.[0-9]+)?)", self.gate)
        if not m:
            raise ValueError(f"task {self.number}: the gate '{self.gate}' names no threshold")
        return float(m.group(1))


@dataclass
class Plan:
    """What the agent fixes before the first draft: the rule, the resources and the seed, all hashed."""
    partition: str
    qos: str
    seed: int
    rule: str = "run the pipeline on the task's inputs and write one result line"


@dataclass
class Attempt:
    attempt: int
    script_sha: str
    prereg_sha: str
    job_id: int | None
    outcome: str                   # refused, failed, gate_failed, passed
    message: str
    repair: str | None = None      # the patch applied after this attempt, when one was
    stopped: str | None = None     # why the loop stopped here without a pass, when it did


class MockLLM:
    """Stands in for the language model: a first draft with a deliberate mistake, then rule-based repairs.

    The mistakes are the ones the real grid refuses most often (root CLAUDE.md rule 7): a GPU partition asked with
    the CPU QoS, a working directory under /tmp, a run on the login node; and one runtime exception, a command-line
    argument the caller never passes. The repair reads the scheduler's or the interpreter's words and patches one
    thing at a time, which is how the real loop is meant to behave: small, inspectable edits, each recorded. A
    gate that fails is answered once, by switching to the fine-tuned checkpoint; a second failure matches no rule.
    """

    def __init__(self, seed: int) -> None:
        self.seed = seed
        self.rng = random.Random(seed)

    def draft(self, task: Task, plan: Plan) -> JobSpec:
        mistake = self.rng.choice(["qos", "tmp", "login", "none"])
        qos, workdir, login = plan.qos, f"/rs/rs_grp_oschome/agent/{task.number}", False
        if mistake == "qos" and task.needs_gpu:
            qos = "requeue"
        elif mistake == "tmp":
            workdir = f"/tmp/agent/{task.number}"
        elif mistake == "login":
            login = True
        return JobSpec(name=f"t{task.number}", partition=plan.partition, qos=qos, cpus=16 if task.needs_gpu else 8,
                       mem_gb=32, gpus=1 if task.needs_gpu else 0, minutes=120, workdir=workdir,
                       script=self._body(task, plan), run_on_login_node=login, prereg_sha=task.prereg_sha)

    @staticmethod
    def _body(task: Task, plan: Plan) -> str:
        # The generated "script" is a tiny Python program the simulator can run. Its gate value is a deterministic
        # function of the task and the seed, so some tasks fall under the gate and the loop can fail; the first
        # draft reads a command-line argument the caller never passes, the planted runtime exception.
        frac = ((task.number * 7919 + plan.seed * 104729) % 1000) / 1000.0
        return "\n".join([
            "import json, sys",
            f"task = {task.number}",
            f"manifest = {{'checkpoint': 'base', 'frac': {frac}}}",
            "args = dict(a.split('=', 1) for a in sys.argv[1:])",
            "checkpoint = args['checkpoint']  # KeyError until the script reads the manifest instead",
            "value = 0.945 + 0.05 * manifest['frac'] + (0.02 if checkpoint == 'fine-tuned' else 0.0)",
            "print(json.dumps({'task': task, 'gate_value': round(value, 4), 'checkpoint': checkpoint}))",
        ])

    def repair(self, spec: JobSpec, message: str) -> tuple[JobSpec, str]:
        """One patch per message; returns the new spec and a sentence saying what changed, or the spec unchanged."""
        if "Invalid qos" in message:
            new = JobSpec(**{**asdict(spec), "qos": "gpu" if spec.gpus else "requeue"})
            return new, f"set --qos={new.qos} for partition {spec.partition}"
        if "outputs go on Ceph" in message:
            new = JobSpec(**{**asdict(spec), "workdir": "/rs/rs_grp_oschome/" + spec.workdir.lstrip("/").split("/", 1)[-1]})
            return new, f"moved -D to {new.workdir}"
        if "login node" in message:
            new = JobSpec(**{**asdict(spec), "run_on_login_node": False})
            return new, "submitted as an sbatch job instead of running on the login node"
        if "KeyError: 'checkpoint'" in message and "args['checkpoint']" in spec.script:
            script = spec.script.replace("checkpoint = args['checkpoint']",
                                         "checkpoint = args.get('checkpoint', manifest['checkpoint'])")
            new = JobSpec(**{**asdict(spec), "script": script})
            return new, "caught KeyError 'checkpoint': read the checkpoint from the manifest when no argument names it"
        if "gate failed" in message and "'checkpoint': 'base'" in spec.script:
            script = spec.script.replace("'checkpoint': 'base'", "'checkpoint': 'fine-tuned'")
            new = JobSpec(**{**asdict(spec), "script": script})
            return new, "gate failed: switched the manifest's checkpoint to the fine-tuned one"
        return spec, "no rule matched"


def run_script(spec: JobSpec) -> tuple[int, str, str, float]:
    """Execute the generated script in a fresh namespace, as the simulated node would, and capture its output.

    Anything the script raises, SystemExit included, becomes a failed job with the traceback on stderr, since
    that is what the agent reads; only a keyboard interrupt is passed up to the person running the mock.
    """
    out, err = io.StringIO(), io.StringIO()
    code = 0
    ns: dict = {"__name__": "__job__"}
    argv = sys.argv
    try:
        sys.argv = ["job.py"]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            exec(compile(spec.script, "job.py", "exec"), ns)  # the mock node runs the mock script
    except KeyboardInterrupt:
        raise
    except BaseException as e:  # the traceback is what the agent reads
        code = 1
        err.write(f"Traceback (most recent call last):\n  File \"job.py\"\n{type(e).__name__}: {e}\n")
    finally:
        sys.argv = argv
    rss = 1.5 + 0.1 * spec.cpus + (12.0 if spec.gpus else 0.0)   # a mock peak memory, GB
    return code, out.getvalue(), err.getvalue(), rss


def result_line(stdout: str) -> dict | None:
    """The last non-empty line of stdout as the result, when it is a JSON object with a numeric gate_value."""
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        return None
    try:
        obj = json.loads(lines[-1])
    except ValueError:
        return None
    if not isinstance(obj, dict) or not isinstance(obj.get("gate_value"), (int, float)):
        return None
    return obj


class MockAgent:
    """Read, plan, generate, submit, read the exception, repair, until the gate passes or the budget is spent."""

    MAX_TODO_BYTES = 1_000_000

    def __init__(self, grid: GridSimulator, llm: MockLLM, max_repairs: int = 6) -> None:
        self.grid = grid
        self.llm = llm
        self.max_repairs = max_repairs

    @classmethod
    def read_tasks(cls, root: Path, limit: int) -> list[Task]:
        """Parse local TODO files for numbered steps; fall back to synthetic tasks where no tree is given."""
        tasks: list[Task] = []
        if root.is_dir():
            for todo in sorted(root.glob("*/TODO.md")):
                if len(tasks) >= limit:
                    break
                try:
                    if not todo.is_file() or todo.stat().st_size > cls.MAX_TODO_BYTES:
                        continue
                    text = todo.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
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

    def plan(self, task: Task) -> Plan:
        """Fix the resources before any draft; the mistakes the drafter plants are departures from this plan."""
        if task.needs_gpu:
            return Plan("gmsap", "gpu", self.llm.seed)
        return Plan("reqp", "requeue", self.llm.seed)

    @staticmethod
    def prereg(task: Task, plan: Plan) -> str:
        """Pre-register, then score: the hash covers the rule, the gate, the inputs, the resources and the seed,
        and is stamped on every attempt and every scheduler row (docs/handoff/RECIPES.md)."""
        text = "\n".join([f"task {task.number}: {task.title}", f"rule: {plan.rule}", f"gate: {task.gate}",
                          f"files: {task.files}", f"partition: {plan.partition} qos: {plan.qos}",
                          f"seed: {plan.seed}"])
        task.prereg_sha = hashlib.sha256(text.encode()).hexdigest()[:16]
        return task.prereg_sha

    def work(self, task: Task) -> dict:
        plan = self.plan(task)
        self.prereg(task, plan)
        threshold = task.threshold()
        spec = self.llm.draft(task, plan)
        attempts: list[Attempt] = []
        handed_to_person = False
        for i in range(self.max_repairs + 1):
            sha = hashlib.sha256(spec.script.encode()).hexdigest()[:12]
            attempt = Attempt(i, sha, task.prereg_sha, None, "", "")
            try:
                attempt.job_id = self.grid.sbatch(spec)
            except GridRefusal as e:
                attempt.outcome, attempt.message = "refused", str(e)
            else:
                rec = self.grid.wait(attempt.job_id)
                result = result_line(rec.stdout) if rec.state == "COMPLETED" else None
                if rec.state != "COMPLETED":
                    tail = rec.stderr.strip().splitlines()
                    attempt.outcome = "failed"
                    attempt.message = tail[-1] if tail else f"job ended in state {rec.state}"
                elif result is None:
                    attempt.outcome, attempt.message = "failed", "no result line in stdout"
                elif result["gate_value"] >= threshold:
                    attempt.outcome = "passed"
                    attempt.message = f"gate_value {result['gate_value']} >= {threshold}"
                    attempts.append(attempt)
                    break
                else:
                    attempt.outcome = "gate_failed"
                    attempt.message = f"gate failed: gate_value {result['gate_value']} < {threshold}"
            if i == self.max_repairs:
                attempt.stopped = "repair budget exhausted"
                attempts.append(attempt)
                break
            new_spec, patch = self.llm.repair(spec, attempt.message)
            if new_spec == spec:
                attempt.stopped = "no rule matched: handed to a person"
                handed_to_person = True
                attempts.append(attempt)
                break
            attempt.repair = patch
            attempts.append(attempt)
            spec = new_spec
        passed = bool(attempts) and attempts[-1].outcome == "passed"
        return {"task": asdict(task), "plan": asdict(plan), "passed": passed,
                "attempts": [asdict(a) for a in attempts],
                "repairs": sum(1 for a in attempts if a.repair),
                "refusals": sum(1 for a in attempts if a.outcome == "refused"),
                "human_interventions": 1 if handed_to_person else 0}


# ----------------------------------------------------------------------------------------------------------------
# 3. The evaluation loop for a 2-D C-arm projection
# ----------------------------------------------------------------------------------------------------------------

PIXEL_MM = 0.1915      # object-plane pixel of C-ArmLSpine (docs/MODEL_CARD.md 6.1; 0.2930 mm at the detector)
SID_MM = 1140.0        # source to image distance, recorded with the geometry; the image plane here is the object plane
SOD_MM = 745.0         # source to object distance
PITCH_MM = 34.0        # lumbar body pitch used by the linker (docs/MODEL_CARD.md 6.1)
DETECTOR_PX = 1024     # the square image the detector sees
FIELD_CENTER_MM = 50.0  # the detector's centre sits this far above the sacrum's reference, so a lumbar field
#                         of 196 mm holds the sacrum's top and three or four bodies, as a spot frame does
LEVELS = ["L5", "L4", "L3", "L2", "L1", "T12", "T11"]   # counted up from the sacrum
LSTV_SHARE = 0.129     # lumbosacral transitional vertebrae in 550 surgical patients (Nakagawa 2017;
#                        02_transitional_naming_truth/docs/LEVELCHECK_CLAIM.md)

Box = tuple[float, float, float, float]


def projection_matrix() -> list[list[float]]:
    """A 3 x 4 perspective C-arm projection for a lateral view: the source on +x, looking toward -x.

    Object coordinates are millimetres with the origin on the spine's axis at the field's centre; image
    coordinates are pixels on a DETECTOR_PX square whose pixel is the object-plane pixel (0.1915 mm), so the
    image plane is placed at the object plane: a point on that plane maps at magnification 1 and a point nearer
    the source is magnified by SOD / (SOD - x). SID is recorded beside SOD because the detector-plane pixel is
    PIXEL_MM * SID / SOD (0.2930 mm); it does not enter this matrix.
    """
    f = SOD_MM / PIXEL_MM           # focal length in pixels at the object plane
    c = DETECTOR_PX / 2.0
    K = [[f, 0.0, c], [0.0, f, c], [0.0, 0.0, 1.0]]
    # camera frame: depth along -x of the object (source at x = +SOD looks toward -x); image u <- object y, v <- -z
    Rt = [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0, 0.0], [-1.0, 0.0, 0.0, SOD_MM]]
    return [[sum(K[i][k] * Rt[k][j] for k in range(3)) for j in range(4)] for i in range(3)]


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
    """A lumbar column above a sacrum, pitch 34 mm with a little jitter; a transitional spine adds an L6.

    Heights are measured from the sacrum's reference and shifted so that the field's centre is the origin.
    """
    bodies = [Body("sacrum", (0.0, 0.0, -40.0 - FIELD_CENTER_MM), (50.0, 55.0, 45.0))]
    levels = (["L6"] if transitional else []) + LEVELS
    z = 0.0
    for i in range(n_bodies + (1 if transitional else 0)):
        z += PITCH_MM + rng.uniform(-2.0, 2.0)
        bodies.append(Body(levels[i], (rng.uniform(-3, 3), rng.uniform(-3, 3), z - FIELD_CENTER_MM),
                           (34.0 + rng.uniform(-3, 3), 44.0 + rng.uniform(-3, 3), 26.0 + rng.uniform(-2, 2))))
    return bodies


def silhouette_box(P: list[list[float]], body: Body) -> Box:
    us, vs = zip(*(project(P, c) for c in body.corners()))
    return min(us), min(vs), max(us), max(vs)


def box_area(r: Box) -> float:
    return max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1])


def clip_box(r: Box, size: int = DETECTOR_PX) -> Box:
    """The part of a box that lies on the detector."""
    return (min(max(r[0], 0.0), size), min(max(r[1], 0.0), size), min(max(r[2], 0.0), size), min(max(r[3], 0.0), size))


def in_field(r: Box, size: int = DETECTOR_PX, least: float = 0.5) -> bool:
    """A body counts as in the field when at least half its silhouette lies on the detector."""
    full = box_area(r)
    return full > 0.0 and box_area(clip_box(r, size)) / full >= least


def box_iou(a: Box, b: Box) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = box_area(a) + box_area(b) - inter
    return inter / union if union else 0.0


def box_dice(a: Box, b: Box) -> float:
    """Dice of two axis-aligned boxes: the overlap metric on silhouettes drawn as boxes, not on masks."""
    iou = box_iou(a, b)
    return 2 * iou / (1 + iou) if iou else 0.0


def corner_errors_mm(a: Box, b: Box) -> list[float]:
    """The 2-D distance between each of the four corners of two boxes, in millimetres at the object plane."""
    ca = [(a[0], a[1]), (a[2], a[1]), (a[0], a[3]), (a[2], a[3])]
    cb = [(b[0], b[1]), (b[2], b[1]), (b[0], b[3]), (b[2], b[3])]
    return [math.hypot(p[0] - q[0], p[1] - q[1]) * PIXEL_MM for p, q in zip(ca, cb)]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def median(xs: list[float]) -> float:
    return sorted(xs)[len(xs) // 2] if xs else float("nan")


def evaluate_projection(seed: int, n_frames: int = 40, detector_noise_px: float = 6.0,
                        miss_rate: float = 0.05) -> dict:
    """The placeholder loop: for each simulated frame, project, keep what is on the detector, perturb, score.

    Naming counts up from the detected sacrum along the detected boxes, which is what a count-only method does;
    a transitional spine would shift every name by one, and the shape-based encoder that catches it is not
    simulated here, so the loop abstains on those frames by construction: the abstention is an oracle, and the
    report says so.
    """
    rng = random.Random(seed)
    P = projection_matrix()
    dices, ious, corner_err_mm = [], [], []
    exact_frames = answered = abstained = sacrum_found = bodies_in_field = 0
    for _ in range(n_frames):
        transitional = rng.random() < LSTV_SHARE
        column = make_column(rng, transitional=transitional)
        truth = {b.level: clip_box(silhouette_box(P, b)) for b in column if in_field(silhouette_box(P, b))}
        bodies_in_field += len(truth)
        detected: dict[str, Box] = {}
        for level, box in truth.items():
            if rng.random() < miss_rate:
                continue
            jitter = [rng.gauss(0.0, detector_noise_px) for _ in range(4)]
            detected[level] = clip_box((box[0] + jitter[0], box[1] + jitter[1], box[2] + jitter[2], box[3] + jitter[3]))
        for level, tbox in truth.items():
            if level in detected:
                dices.append(box_dice(tbox, detected[level]))
                ious.append(box_iou(tbox, detected[level]))
                corner_err_mm.extend(corner_errors_mm(tbox, detected[level]))
        # naming by a count from the detected sacrum: the detected boxes, ordered bottom-up by their centre on the
        # image (v grows downward), take the names L5, L4, ... in turn
        bodies = [lvl for lvl in detected if lvl != "sacrum"]
        if "sacrum" in detected:
            sacrum_found += 1
        if "sacrum" not in detected or not bodies or transitional:
            abstained += 1
            continue
        ordered = sorted(bodies, key=lambda lvl: -(detected[lvl][1] + detected[lvl][3]) / 2)
        answered += 1
        if all(LEVELS[i] == lvl if i < len(LEVELS) else False for i, lvl in enumerate(ordered)):
            exact_frames += 1
    lo, hi = wilson(exact_frames, answered)
    return {
        "mock": True, "frames": n_frames, "bodies_in_field": bodies_in_field, "bodies_scored": len(dices),
        "box_dice_median": round(median(dices), 4), "box_iou_median": round(median(ious), 4),
        "corner_error_mm_median": round(median(corner_err_mm), 3),
        "corner_error_mm_p95": round(sorted(corner_err_mm)[int(0.95 * (len(corner_err_mm) - 1))], 3)
        if corner_err_mm else None,
        "sacrum_found": sacrum_found, "answered": answered, "abstained": abstained,
        "abstention_is_oracle": True,
        "exact_on_answered": exact_frames, "exact_rate": round(exact_frames / answered, 4) if answered else None,
        "wilson_95": [round(lo, 4), round(hi, 4)],
        "geometry": {"pixel_mm": PIXEL_MM, "sid_mm": SID_MM, "sod_mm": SOD_MM, "pitch_mm": PITCH_MM,
                     "detector_px": DETECTOR_PX, "field_center_mm": FIELD_CENTER_MM,
                     "projection_matrix": [[round(v, 3) for v in row] for row in P]},
    }


# ----------------------------------------------------------------------------------------------------------------
# 4. Entry points
# ----------------------------------------------------------------------------------------------------------------

def run(tasks: int, seed: int, root: Path | None) -> dict:
    if tasks < 1:
        raise ValueError("tasks must be at least 1")
    grid = GridSimulator(seed)
    agent = MockAgent(grid, MockLLM(seed))
    task_list = agent.read_tasks(root or Path("/nonexistent"), tasks)
    t0 = time.perf_counter()
    results = [agent.work(t) for t in task_list]
    wall = time.perf_counter() - t0
    passed = sum(1 for r in results if r["passed"])
    lo, hi = wilson(passed, len(results))
    return {
        "mock": True,
        "agent": {"tasks": len(results), "passed": passed, "failed": len(results) - passed,
                  "pass_rate": round(passed / len(results), 4), "wilson_95": [round(lo, 4), round(hi, 4)],
                  "repairs_total": sum(r["repairs"] for r in results),
                  "refusals_total": sum(r["refusals"] for r in results),
                  "human_interventions": sum(r["human_interventions"] for r in results),
                  "mock_clock_seconds": grid.now(), "wall_seconds": round(wall, 3), "results": results},
        "grid": {"squeue": grid.squeue(), "sacct": grid.sacct()},
        "projection_eval": evaluate_projection(seed),
    }


def selftest() -> None:
    grid = GridSimulator(0)
    refused = [
        (JobSpec("x", "gmsap", "requeue", 8, 32, 1, 10, "/rs/rs_grp_oschome/x", "print(1)"), "Invalid qos"),
        (JobSpec("x", "reqp", "requeue", 8, 32, 0, 10, "/rs/x", "print(1)", run_on_login_node=True), "login node"),
        (JobSpec("x", "reqp", "requeue", 8, 32, 0, 10, "/rs/../tmp/x", "print(1)"), "outputs go on Ceph"),
        (JobSpec("x", "reqp", "requeue", 0, 32, 0, 10, "/rs/x", "print(1)"), "Invalid resource"),
        (JobSpec("x", "reqp", "requeue", 8, 32, 0, 8 * 24 * 60, "/rs/x", "print(1)"), "time limit"),
        (JobSpec("x", "reqp", "requeue", 8, 32, 1, 10, "/rs/x", "print(1)"), "no GPU"),
    ]
    for spec, words in refused:
        try:
            grid.sbatch(spec)
            raise AssertionError(f"must be refused: {words}")
        except GridRefusal as e:
            assert words in str(e), (words, str(e))
    good = JobSpec("x", "gmsap", "gpu", 8, 32, 1, 10, "/rs/rs_grp_oschome/x", "print('ok')", prereg_sha="abc")
    jid = grid.sbatch(good)
    grid.tick(1.0)
    assert grid.jobs[jid].state == "RUNNING", "a job holds its node across ticks"
    assert grid.squeue()["gpus_free"] == sum(p["nodes"] * p["gpus"] for p in PARTITIONS.values()) - 1
    rec = grid.wait(jid)
    assert rec.state == "COMPLETED" and rec.stdout.strip() == "ok" and rec.ended_at <= grid.now()
    assert grid.squeue()["gpus_free"] == sum(p["nodes"] * p["gpus"] for p in PARTITIONS.values())
    assert grid.sacct()[-1]["prereg_sha"] == "abc", "the hash reaches the scheduler's record"
    slow = JobSpec("s", "reqp", "requeue", 8, 32, 0, 1, "/rs/x", "print('late')")
    assert grid.wait(grid.sbatch(slow)).state == "TIMEOUT", "a one-minute limit kills a longer mock run"
    crash = JobSpec("c", "reqp", "requeue", 8, 32, 0, 10, "/rs/x", "raise SystemExit(3)")
    assert grid.wait(grid.sbatch(crash)).state == "FAILED", "SystemExit is a failed job, not an exit of the mock"
    assert result_line("") is None and result_line("not json") is None and result_line('{"gate_value": "x"}') is None
    assert result_line('{"gate_value": 0.5}') == {"gate_value": 0.5}
    P = projection_matrix()
    u, v = project(P, (0.0, 0.0, 0.0))
    assert abs(u - 512.0) < 1e-6 and abs(v - 512.0) < 1e-6, "the axis point lands on the detector centre"
    u2, _ = project(P, (0.0, 10.0, 0.0))
    assert abs((u2 - 512.0) * PIXEL_MM - 10.0) < 1e-6, "10 mm on the central plane is 10 mm of pixels"
    assert box_dice((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
    assert clip_box((-5, -5, 5, 5)) == (0, 0, 5, 5) and not in_field((-20, 0, 5, 10)) and in_field((0, 0, 10, 10))
    assert corner_errors_mm((0, 0, 10, 10), (3, 4, 13, 14)) == [5 * PIXEL_MM] * 4
    column = make_column(random.Random(0))
    on_detector = [b.level for b in column if in_field(silhouette_box(P, b))]
    assert "sacrum" in on_detector and "L5" in on_detector and "L1" not in on_detector, on_detector
    lo, hi = wilson(595, 617)
    assert 0.94 < lo < 0.96 and 0.97 < hi < 0.98, (lo, hi)
    assert Task(1, "t", False, "gate_value >= 0.95", []).threshold() == 0.95
    rep = run(12, 0, None)
    a = rep["agent"]
    assert a["passed"] + a["failed"] == 12 and a["repairs_total"] > 0 and a["refusals_total"] > 0, a
    for r in a["results"]:
        last = r["attempts"][-1]
        assert last["outcome"] == "passed" or last["stopped"], r["task"]["number"]
        assert all(att["prereg_sha"] == r["task"]["prereg_sha"] for att in r["attempts"])
    assert any(r["human_interventions"] for r in a["results"]), "task 12 of seed 0 misses its gate twice"
    assert rep["projection_eval"]["bodies_scored"] > 0 and rep["projection_eval"]["abstention_is_oracle"]
    for bad in (0, -1):
        try:
            run(bad, 0, None)
            raise AssertionError("tasks < 1 must be refused")
        except ValueError:
            pass
    print("selftest: ok")


def positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return value


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="mock autonomous agent, simulated grid, placeholder 2-D evaluation")
    ap.add_argument("--tasks", type=positive_int, default=6)
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
    print("mock run: every number below is simulated")
    print(f"agent: {a['passed']}/{a['tasks']} tasks passed their gate, {a['repairs_total']} repairs, "
          f"{a['refusals_total']} scheduler refusals, {a['human_interventions']} handed to a person")
    print(f"grid: {report['grid']['squeue']}")
    print(f"projection: box dice median {e['box_dice_median']}, corner error median {e['corner_error_mm_median']} mm, "
          f"exact {e['exact_on_answered']}/{e['answered']} answered, Wilson {e['wilson_95']}, "
          f"abstained {e['abstained']}/{e['frames']} (oracle)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
