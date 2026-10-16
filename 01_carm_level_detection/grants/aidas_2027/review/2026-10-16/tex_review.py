"""Apply the review of 2026-10-16 to main.tex: wording that the files support, nothing the owner did not ask for."""
import re, sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()

def swap(old, new):
    global text
    pat = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
    hits = pat.findall(text)
    assert len(hits) == 1, (len(hits), old[:70])
    text = pat.sub(lambda m: new, text, count=1)

# 1 invention wording
swap("license, as an invention-disclosure review clears), the RAG-LLM's first release",
     "license, as WSU's technology-transfer review clears), the RAG-LLM's first release")
# 2 ScienceDirect: the owner's word, said as WSU's rights rather than Elsevier's approval
swap("multimedia) under the text and data mining and AI rights Elsevier approved for WSU; no passage trains a model or",
     "multimedia) under WSU's text and data mining and AI rights from Elsevier; no passage trains a model or")
# 3b hours and in-kind lines for the RAG-LLM's first release
swap("the imaging session, the literature index and the pending protocol.",
     "the imaging session, the literature index, the RAG-LLM's first release and the pending protocol.")
swap("the trainee program, grid, Beethoven, Symphony, pipelines and faculty time come in kind;",
     "the trainee program, grid, Beethoven, Symphony, pipelines, the RAG-LLM's first release and faculty time come in kind;")
swap("and 80 checking the agent's leave-one-device-out and latency runs against their gates.",
     "and 80 checking the agent's leave-one-device-out, latency and RAG-LLM runs against their gates.")
# 5, 6, 7, 8, 27 the platform paragraph
swap("the data platform under it: a card for each of 211 imaging sources (5.3 TB on the grid), every item keyed to a person, nine leakage checks, and 563 quoted numbers audited against their models' training persons. Its CT census, 21,622 CTs from 21,603 persons, was mined for the anatomy on which counting fails: two automatic labelers chosen to fail differently screened 18 public collections (843 GPU-hours) into a registry of 6,108 persons holding 146 with a sixth lumbar vertebra, 103 on an expert read, and 14 with a thirteenth thoracic, under a stopping rule fixed before any download that turned 29,479 chest CTs away; a labeler's 9.3\\pct{} rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4\\pct{} once a rib on the named body was required, the check outside the computation that this project's gates make routine.",
     "the data platform under it: a card for each of 211 imaging sources, 115 of them on the grid (5.3 TB), every item keyed to a person, nine leakage checks (seven run on the frozen split), and 563 quoted numbers audited against their models' training persons. Its CT census, 21,622 CTs from 21,603 persons, was mined for the anatomy on which counting fails: two automatic labelers chosen to fail differently filled a registry of 6,108 persons from five CT collections, 146 of them with a sixth lumbar vertebra, 103 on an expert read, and 14 with a thirteenth thoracic, and screened 18 further public collections (843 GPU-hours) under a stopping rule, fixed before any download, that turned 29,479 mostly chest CTs away. A labeler's 9.3\\pct{} rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4\\pct{} (5 of 367) once a rib on the named body was required, the check outside the computation that this project's gates make routine.")
# 23 and 7 in the abstract
swap("(211 catalogued sources, 5.3 TB on the grid: a census of 21,622 public CTs screened for the anatomy on which counting fails,",
     "(211 catalogued sources, 115 on the grid at 5.3 TB: a census of 21,622 public CTs mined for the anatomy on which counting fails,")
# 30
swap("the frames that carry it that far coming from 145 of COBRA's 692 cases.",
     "145 of COBRA's 692 cases among the frames that carry it that far.")
# 16 abstract and premise and Aim 3
swap("fine-tuned on images paired with clinical charts under the consortium's pending IRB protocol (about 4,000",
     "fine-tuned, in its second release, on images paired with clinical charts under the consortium's pending IRB protocol (about 4,000")
swap("a multimodal model fine-tuned on images paired with charts (the pending protocol's own stated purpose),",
     "a multimodal model fine-tuned on images paired with charts (a stated purpose of the pending protocol),")
swap("IRB-26-03-8648, whose stated purpose is a locally hosted multimodal spine LLM, amended as the work requires;",
     "IRB-26-03-8648, whose stated purposes include a locally hosted multimodal spine LLM, amended as the work requires;")
# 13
swap("17\\pct{} followed by legal action, and about half of respondents report at least one [2,3].",
     "17\\pct{} followed by legal action or a settlement, and about half of respondents report at least one [2,3].")
# 31
swap("finds 98.8\\pct{} of 161 lumbar vertebrae on 17 spines it never saw;",
     "finds 98.8\\pct{} (at 0.25) of 161 lumbar vertebrae on 17 spines it never saw;")
# 26
swap("Closing that gap takes hundreds of GPU jobs run, checked and recorded on a shared cluster;",
     "Closing that gap takes many GPU jobs run, checked and recorded on a shared cluster;")
# 9
swap("and profiled prompts, a standing routine proposing the next experiment from the last record: continuous, autonomous research under the gates.",
     "and profiled prompts; and a standing routine proposes the next experiment from the last record: continuous, autonomous research under the gates.")
# 22
swap("frameworks that make it durable (LangGraph's fan-out with checkpointing, Temporal's sagas, OpenHands sandboxes, schema-validated outputs);",
     "frameworks that make such a script durable (LangGraph's checkpointed fan-out, Temporal's sagas, OpenHands sandboxes, typed outputs);")
# 12
swap("all ten went to a national meeting as abstracts,", "all ten were submitted to a national meeting as abstracts,")
# 10, 25, 28, 11 the COBRA paragraph
swap("each case with its exact acquisition geometry and a registered planning CT [29]; 145 Elekta cases, 24 frames each, are in any training bank, and 322 Elekta and all 225 Varian cases train nothing.",
     "each case with its acquisition geometry and a registered planning CT [29]; 145 Elekta cases, 24 frames each, are in any frame bank (110 of them, 2,640 frames, train the detector), and 322 Elekta and all 225 Varian cases train nothing.")
swap("and cutting the Elekta frames from 2,640 to 240 costs 47.7 points",
     "and cutting the Elekta training frames from 2,640 to 240 costs 47.7 points")
swap("with a CT whose labels project onto every one,", "with a CT whose automatic labels project onto every one,")
swap("its median age is 66 with 7 transitional persons found and 91 calls unread, and naming on it is weak today",
     "the median age of its exported cases is 66 (known for 115 of 145), 7 transitional persons are found and 91 calls unread, and naming on it is weak today")
# 14
swap("the stack names a frame in under 1\\,s on a workstation GPU;",
     "the stack names a frame in under 1\\,s on one GPU (no latency of the stack is on file yet);")
# 19
swap("\\emph{Quarter 2:} Aim 1's runs (months 4--8), 1b's routine, wave 1 (months 4--7),",
     "\\emph{Quarter 2:} Aim 1's runs (months 4--8), 1b's routine, the wizard and the grid bridge, wave 1 (months 4--7),")
# 29
swap("lines B2, B5, C1 and D buy goods and services, and Aim 3 uses WSU's own C-arm.",
     "lines B to D buy goods and services from WSU units and vendors, and Aim 3 uses WSU's own C-arm.")
# 24 the PDF's metadata title
n = len(re.findall(r"pdftitle=\{[^}]*\}", text))
assert n == 1, n
text = re.sub(r"pdftitle=\{[^}]*\}", "pdftitle={Semi-Autonomous AI Research on the Wayne State Grid: Building a Customizable Spine RAG-LLM in One Year}", text)
open(path, "w", encoding="utf-8").write(text)
print("tex ok")
