"""Count Appendix A rows in a rendered tables/search_strings.tex: blocks, 'run not run' rows, and
'(no string recorded)' rows, listing the ids. Usage: python tests/count_appendix_rows.py <search_strings.tex>"""
import re
import sys

t = open(sys.argv[1], encoding="utf-8").read()
heads = [l for l in t.splitlines() if "\\textbf{\\texttt{" in l]


def qid(l: str) -> str:
    m = re.search(r"\\texttt\{(.*?)\}\} ---", l)
    return m.group(1).replace("\\allowbreak{}", "").replace("\\_", "_") if m else "?"


notrun = [qid(l) for l in heads if "run not run" in l]
nostr = [qid(l) for l in heads if "(no string recorded)" in l]
print("blocks", len(heads))
print("not run", len(notrun), notrun)
print("no string", len(nostr), nostr)
