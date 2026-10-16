"""Do not attribute the Claude plug-in to OpenEvidence (the mcpmarket skill is a third party's); say what goes to it."""
import re, sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()

def swap(old, new):
    global text
    pat = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
    hits = pat.findall(text)
    assert len(hits) == 1, (len(hits), old[:60])
    text = pat.sub(lambda m: new, text, count=1)

swap("compared with OpenEvidence's clinical evidence service through its plug-in for Claude [31];",
     "compared with OpenEvidence's clinical evidence service through a Claude plug-in [31];")
swap("compared with OpenEvidence's evidence service through its Claude plug-in [31], with no",
     "compared with OpenEvidence's evidence service through a Claude plug-in [31], with no")
swap("On a held-out question set the mentors write, its answers and OpenEvidence's, through OpenEvidence's plug-in for Claude [31], are graded side by side for correctness and for quotations that support them; our detectors' reading of an image can be handed to OpenEvidence as a tool, while no indexed passage and no patient record leaves the grid.",
     "On a held-out question set the mentors write on public images, its answers and OpenEvidence's, through a Claude plug-in [31], are graded side by side for correctness and for quotations that support them; the detectors' reading of an image may go to OpenEvidence with the question, while no indexed passage and no patient record leaves the grid.")
swap("[31] OpenEvidence, openevidence.com; its Claude Code set-up skill, mcpmarket.com/\\allowbreak tools/\\allowbreak skills/\\allowbreak openevidence-api-setup-auth.",
     "[31] OpenEvidence, openevidence.com; a Claude Code set-up skill for its API, mcpmarket.com/\\allowbreak tools/\\allowbreak skills/\\allowbreak openevidence-api-setup-auth.")
open(path, "w", encoding="utf-8").write(text)
print("tex ok")
