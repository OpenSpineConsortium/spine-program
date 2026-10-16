"""Win back the two lines the real contact lines take on the cover, without dropping a fact."""
import re, sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()

def swap(old, new):
    global text
    pat = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
    hits = pat.findall(text)
    assert len(hits) == 1, (len(hits), old[:70])
    text = pat.sub(lambda m: new, text, count=1)

swap("reads the image through the Open Spine Consortium's own X-ray detector and level model,",
     "reads the image through the Open Spine Consortium's X-ray detector and level model,")
swap("an imaging platform mined for the problem (211 catalogued sources,", "an imaging platform (211 catalogued sources,")
swap("on CooperBench's pairs first and SWE-bench after.", "on CooperBench's pairs and SWE-bench.")
swap("the detection gap closed with the 372,000 COBRA projections no model has seen,",
     "the detection gap closed with 372,000 unseen COBRA projections,")
swap("their literature questions go to the RAG-LLM's text half on the grid.",
     "their literature questions go to the RAG-LLM on the grid.")
swap("lines B to D buy goods and services from WSU units and vendors, and Aim 3 uses WSU's own C-arm.",
     "lines B to D buy goods and services, and Aim 3 uses WSU's own C-arm.")
open(path, "w", encoding="utf-8").write(text)
print("tex ok")
