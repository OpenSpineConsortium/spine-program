import pathlib, sys
p = pathlib.Path('/home/user/spine-program/01_carm_level_detection/grants/aidas_2027/latex/main.tex')
s = p.read_text()

def rep(old, new):
    global s
    n = s.count(old); assert n == 1, (n, old[:90]); s = s.replace(old, new)

def rep_span(start, end, new, keep_end=False):
    """Replace from the unique text `start` through the unique text `end` (inclusive unless keep_end)."""
    global s
    i = s.find(start); assert i >= 0 and s.count(start) == 1, start[:60]
    j = s.find(end, i); assert j >= 0 and s.count(end) == 1, end[:60]
    stop = j if keep_end else j + len(end)
    s = s[:i] + new + s[stop:]

# 1. Title: the goal in the title, the case example in the abstract.
rep(r"From Labeled CT to C-Arm Level Localization,\\[1pt] with Medical Trainees Driving the Agents\par}",
    r"Building a Customizable Spine RAG-LLM in One Year,\\[1pt] with Medical Trainees Driving the Agents\par}")

# 2. The cover's area 4 line.
rep(r"""AI for Health (area 4; Aim 3): intraoperative imaging decision support, an advisory level label per C-arm
image that the surgeon confirms and the stack withholds when its checks disagree.\\[2pt]""",
    r"""AI for Health (area 4; Aim 3): a customizable, locally hosted spine RAG-LLM that reads the image through the
consortium's detectors and answers with cited quotations, and an advisory level label per C-arm image that the surgeon
confirms.\\[2pt]""")

# 3. The abstract and keywords.
new_abstract = r"""{\small
{\bfseries Abstract.} Wrong-level spine surgery is a never event, unpaid by Medicare since 2009 [21] and reported to the
Joint Commission 9 times in 2024, 7 of them spinal [22]; paid US malpractice claims for surgical never events reached
\$1.3 billion over 1990--2010 [23]. It persists because surgeons confirm the level by counting vertebrae on an X-ray
from a C-arm, the operating room's mobile fluoroscope, and the count fails in patients with an extra or missing lumbar
segment and on images that show too few vertebrae. This project's goal is a customizable, locally hosted
retrieval-augmented language model for spine care (a RAG-LLM): a multimodal model on the WSU grid that reads the image
through the Open Spine Consortium's own X-ray detector and level model, retrieves from the consortium's index of Scopus
and ScienceDirect spine literature (text, images and multimedia, under WSU's text and data mining rights) and answers
with verbatim, cited quotations; fine-tuned on images paired with clinical charts under the consortium's pending IRB
protocol (about 4,000 Detroit Medical Center spine surgery patients; amended as the work requires); compared with
OpenEvidence's clinical evidence service through its plug-in for Claude [31]; and customizable in that a lab swaps in its
own corpus, detectors and records. The consortium's spine program is the case example of what an organized,
AI-assisted workflow builds in a short time: an imaging platform mined for the problem (211 catalogued sources, 5.3 TB
on the grid: a census of 21,622 public CTs screened for the anatomy on which counting fails, 39,705 plain radiographs,
COBRA's 692 radiotherapy cone-beam cases with 375,618 projections); 802 CTs with every vertebra labeled
(CTSpinoPelvic1K, a NeurIPS 2026 benchmark); a physics renderer; and a level model that, never trained on a C-arm
image, names the level of 96.4\pct{} of the lateral vertebrae a film-trained detector finds on a public C-arm dataset,
while detection on that C-arm stays at 80.5\pct{} (90.6\pct{} at a lower threshold) against the 97\pct{} set in
advance, the frames that carry it that far coming from 145 of COBRA's 692 cases. Aim 1 studies the workflow: an AI
agent iterates the scientific method inside the consortium's frameworks (the cluster's job rules, a code gate,
reporting protocols, multi-agent coordination on GitHub), a result counting only when a test sealed before the run
passes and a person merges it, on tasks with a planted fault submitting a wrong result, we expect, in under a fifth of
runs against over half without the checks; from the same records Aim 1 measures what each run costs in tokens, tool
calls and context, and Symphony's claim protocol against the worktree and framework orchestrators it competes with, on
CooperBench's pairs first and SWE-bench after. Aim 2 gives the agent to eight medical trainees and measures, task
against matched task, what it adds over a coding assistant; their literature questions go to the RAG-LLM's text half
on the grid. Aim 3 builds the case example through to the RAG-LLM: the detection gap closed with the 372,000 COBRA
projections no model has seen, learned X-ray simulation and a CT-paired cadaver set imaged at WSU, then the multimodal
model that reads the image and the chart. Deliverables: Aim 1's tasks, records, benchmark suites and report (MIT
license, as an invention-disclosure review clears), the RAG-LLM's first release on the public corpus with its graded
question set, the cadaver set, an FDA Pre-Submission, and NSF CAREER and NIH R21 proposals.

\vspace{2pt}
{\bfseries Keywords.} agentic systems; AI for science; reproducibility; coordination protocols; retrieval-augmented
generation; multimodal models; high-performance computing; medical education; fluoroscopy; spine surgery}"""
rep_span(r"{\bfseries Abstract.} Wrong-level spine surgery",
         r"high-performance computing; medical education; fluoroscopy; 3-D Gaussian splatting; domain transfer; spine surgery",
         new_abstract)

# 4. The premise paragraph in section 1.
new_premise = r"""Our premise is that the bottleneck has moved from the model to the experiments; that an AI agent can run them if
strict frameworks, not the model, decide which results count; that the same frameworks, which record every run,
let us measure the agents; and that what such a workflow builds in a year is best shown on one case, this spine program,
whose end product is a customizable, locally hosted RAG-LLM: the consortium's detectors reading the image, its indexed
literature answering with cited quotations, a multimodal model fine-tuned on images paired with charts (the pending
protocol's own stated purpose), compared with OpenEvidence's evidence service through its Claude plug-in [31], with no
indexed passage and no patient record leaving the grid. Three aims test it (Figure~1). \aim{Aim 1} has the agent iterate the scientific method
inside the consortium's frameworks: Beethoven runs Claude Code on the grid and keeps the grid's profile as checked data
and its job rules in writing; beethoven-qa checks the agent's code; beethoven-research holds REFORMS [10] rules for
machine-learning science and plans the CLAIM [11] checklist for imaging AI; and Symphony (public, MIT) gives each
piece of work to one agent through a claim that is a git branch, which GitHub lets exactly one of two racing agents
create, with the board and the release of idle claims as deterministic CI jobs and no server. The methodological contribution measures \emph{framework-bound scientific iteration}: how many wrong but
plausible results a research agent submits when the rules are only written, and when checks enforce them, and, from
the same records, what its work costs and how the protocol fares against the orchestrators it competes with.
Benchmarks score agents' code edits [12], machine-learning engineering [13] or papers [14], and studies of research
agents probe their leakage and tampering [15,16]; CooperBench found two agents in separate workspaces,
talking only by message, passing 183 of 652 feature pairs against 315 for one (GPT-5), most failures duplicated or
incompatible work [27]. We plant the faults an agent inherits from a lab's data and code, count those it passes on,
and meter the coordination. \aim{Aim 2} puts the agent in medical trainees' hands through Beethoven (Figure~2).
\aim{Aim 3} builds the case example: it turns the agent on the detection gap, with COBRA's unused projections, a paired
CT and C-arm cadaver set imaged at WSU and a differentiable 3-D Gaussian X-ray renderer, as in [17,18], built on the
PI's Gaussian-splatting work, and then on the multimodal model that reads the image and the chart."""
rep_span("Our premise is that the bottleneck has moved from the model to the experiments;",
         "as in [17,18], built on the PI's Gaussian-splatting work.", new_premise)

# 5. 1b, shorter parenthetical.
rep(r"""what each run cost (a usage trailer on every commit, a usage artifact per Actions run, aggregated by its metrics
workflow); 1b adds""",
    r"""what each run cost (a usage trailer on every commit, a usage artifact per Actions run); 1b adds""")

# 6. 1d, tighter.
new_1d = r"""\emph{1d, the
control plane.} A web control panel driven by Claude's own browser (repositories, the board, CI, tasks, workers,
prompts) that shows each run's cost beside the same work on unsorry or Copilot's cloud agent; a wizard that stores a
lab's Claude tokens as saved environment secrets; Beethoven as the bridge from Actions to the grid, a worker in Actions
submitting the Slurm job and posting results and logs back to the pull request; and the extension's one click, today
from Claude Code, brought to the claude.ai Project each trainee works in. """
rep_span(r"\emph{1d, the", r"\emph{Preliminary work.}", new_1d, keep_end=True)

# 7. Preliminary work, shorter Symphony clause.
rep(r"""Symphony (its tests catch all 93
mutated rules; its protocol library is checked over every interleaving of a few workers against an oracle written from
its spec), coordbench and the taxonomy.""",
    r"""Symphony (its tests catch all 93
mutated rules; every interleaving of a few workers is checked against an oracle from its spec), coordbench and the taxonomy.""")

# 8. Aim 2's literature sentence names the RAG-LLM's text half and ScienceDirect.
rep(r"""Literature questions go to a language model on the grid that quotes verbatim, with
citation and DOI, from indexed spine-related Scopus abstracts under the text and data mining and AI rights Elsevier
approved for WSU; no passage trains a model or reaches an outside AI service;""",
    r"""Literature questions go to the RAG-LLM's text half, a language model on the grid that quotes verbatim, with
citation and DOI, from the consortium's index of spine literature (Scopus, and ScienceDirect's text, images and
multimedia) under the text and data mining and AI rights Elsevier approved for WSU; no passage trains a model or
reaches an outside AI service;""")

# 9. Aim 3's heading.
rep(r"\aim{Aim 3 (AI for Health): labeled 3-D structure into 2-D fluoroscopy, at low latency.}",
    r"\aim{Aim 3 (AI for Health): the case example, from labeled 3-D structure to 2-D fluoroscopy to a spine RAG-LLM.}")

# 10. COBRA's limits, shorter.
rep("Its limits: a linac's kV imager, swept round a supine patient for treatment setup, is not a surgical C-arm; a",
    "Its limits: a linac's kV imager is not a surgical C-arm; a")

# 11. The RAG-LLM paragraph, H3 and the measures.
rep(r"""unmeasured; Aim 3 measures it first. \emph{H3:} on each held-out C-arm the detector finds 97\pct{} of vertebrae and of
sacra with no more false detections than today's at 0.74; the stack names a frame in under 1\,s on a workstation GPU;
and on every cadaver frame it names the right level or abstains. \emph{Measures:} recall at 0.74 and 0.25, false
detections, exact level, abstention, corner error, latency (median, 95th percentile) and render-to-real
separability, leave-one-device-out with case-clustered intervals, the cadaver set opened once, models hashed first.""",
    r"""unmeasured; Aim 3 measures it first. \emph{The RAG-LLM.} The detector and level model become tools of a multimodal
model hosted on the grid, which takes the image, the detectors' boxes and names and the retrieved passages and answers
a clinical question with the level, the finding and verbatim quotations. Its first release is fine-tuned on the public
corpus (CTSpinoPelvic1K, the films and their reports, COBRA); its second on images paired with operative notes and
radiology reports under IRB-26-03-8648, whose stated purpose is a locally hosted multimodal spine LLM, amended as the
work requires; and it is customizable: a lab swaps in its own corpus, detectors and records. On a held-out question set
the mentors write, its answers and OpenEvidence's, obtained through OpenEvidence's plug-in for Claude [31], are graded
side by side for correctness and for quotations that support them; our detectors' reading of an image can be handed
to OpenEvidence as a tool, while no indexed passage and no patient record leaves the grid. \emph{H3:} on each held-out
C-arm the detector finds 97\pct{} of vertebrae and of sacra with no more false detections than today's at 0.74; the
stack names a frame in under 1\,s on a workstation GPU; on every cadaver frame it names the right level or abstains;
and on the question set the RAG-LLM is graded correct at least as often as OpenEvidence where the question needs the
image, with no unsupported quotation. \emph{Measures:} recall at 0.74 and 0.25, false detections, exact level,
abstention, corner error, latency (median, 95th percentile), render-to-real separability, graded correctness and
quotation support against OpenEvidence, leave-one-device-out with case-clustered intervals, the cadaver set opened
once, models hashed first.""")

# 12. Section 3 folded into the outcomes section.
rep(r"""\subsection*{3. Evaluation}
H1 to H3 and the measures above are written before any run; none is a powered test; H1 and H2 size the CAREER and CyberTraining proposals.

\subsection*{4. Expected outcomes, deliverables and timeline}
Within the award: Aim 1's tasks, records and report, its benchmark suites (efficiency, orchestration, the taxonomy)
released through coordbench, the control panel, the wizard and the grid bridge; the cohort's outcomes; the cadaver
set, deposited beside CTSpinoPelvic1K as the Body Bequest Program's terms allow, and a transfer and latency
manuscript; an FDA Pre-Submission; and the CAREER and R21.""",
    r"""\subsection*{3. Expected outcomes, deliverables and timeline}
H1 to H3 and the measures above are written before any run; none is a powered test; H1 and H2 size the CAREER and
CyberTraining proposals. Within the award: Aim 1's tasks, records and report, its benchmark suites (efficiency,
orchestration, the taxonomy) released through coordbench, the control panel, the wizard and the grid bridge; the
cohort's outcomes; the RAG-LLM's first release, on the public corpus, with its question set and grades; the cadaver
set, deposited beside CTSpinoPelvic1K as the Body Bequest Program's terms allow, and a transfer and latency
manuscript; an FDA Pre-Submission; and the CAREER and R21.""")

# 13. The quarters.
rep(r"""\emph{Quarter 3:} CAREER, 1c's suites, wave 2 (months 8--11), the renderer's fit, the control panel.
\emph{Quarter 4:} R21, final report, symposium.""",
    r"""\emph{Quarter 3:} CAREER, 1c's suites, wave 2 (months 8--11), the renderer's fit, the control panel, the RAG-LLM's
first fine-tune. \emph{Quarter 4:} R21, the question set graded, final report, symposium.""")

# 14. Reference 31.
rep(r"[30] C-ArmLSpine. Med Image Anal 2024;97:103283.",
    r"""[30] C-ArmLSpine. Med Image Anal 2024;97:103283.
[31] OpenEvidence. openevidence.com; its API set-up skill for Claude Code, mcpmarket.com/tools/skills/openevidence-api-setup-auth.""")

# 15. Alignment page: the R21 item and the team paragraph.
rep(r"""consortium's pending protocol IRB-26-03-8648 (about 4,000 adult DMC spine surgery patients, their CT and records),
  where 99 patients""",
    r"""consortium's pending protocol IRB-26-03-8648 (about 4,000 adult DMC spine surgery patients, their CT and records,
  the RAG-LLM's paired images and charts), where 99 patients""")
rep(r"""and builds the 3-D-to-2-D model, including the Gaussian X-ray renderer;""",
    r"""and builds the 3-D-to-2-D model, the Gaussian X-ray renderer and the multimodal RAG-LLM;""")

# 16. Budget: storage holds the literature index too.
rep(r"Storage holds the render banks, the COBRA export, the cadaver set and Aim 1's run records for the award year;",
    r"Storage holds the render banks, the COBRA export, the literature index, the cadaver set and Aim 1's run records for the award year;")

p.write_text(s); print("reframe applied")
