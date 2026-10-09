#!/usr/bin/env python
"""Build the front documents of the submission packet from SchwingNet/packet_src/ into packet_src/build/.

    python SchwingNet/packet_src/build_packet_src.py            # draft: reports every open item, exits 0 unless a
                                                                  # number is wrong or a source file is missing
    python SchwingNet/packet_src/build_packet_src.py --strict   # submission: also fails on any PENDING, CONFIRM,
                                                                  # unresolved CLAIM anchor or anonymization hit

Reads (never writes) main.tex, sections/, tables/, supplement.tex, refs.bib, results/ and tools/check_limits.py.
Writes only packet_src/build/:

  cover_letter.docx / .md         from cover_letter.md + front_matter.json; every number checked (numbers.json)
  full_title_page.docx / .md      from title_page.md + front_matter.json + statements.md; word counts computed here
                                  with check_limits.py's own counter
  claim_checklist_2024.docx       the 44 CLAIM 2024 items (claim2024/items.json, verbatim) with Yes/No/NA and the
  CLAIM_CHECKLIST_2024.md / .json location of each, resolved from claim2024/map.json anchors against today's tree
  BUILD_REPORT.md                 what is complete, what waits on which gate, what waits on the author

Markers: [[PENDING Gx: what]] waits on a gate; [[CONFIRM: what]] waits on the author. Both print bold red in the
.docx. No number is typed in this script: numbers come from the result files through numbers.json, word counts
from the tex through check_limits.py, and the comparator's commit dates and times from git.

Checks (2026-09-24 additions marked +): every letter number traced; + every commit that touched LEVELCHECK_MODEL.md is
listed in front_matter, its time equals git's, it is an ancestor of HEAD, and the letter names it; + no
self-evaluation, priority claim or regulatory pathway in the letter or title page; + no cited self-reference other
than the required overlap citation; + every CLAIM item carries a six-figure placement ('expect') and anchors that
land outside it are listed; + open author decisions (front_matter author_decisions) are listed and hold --strict.
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import re
import subprocess
import sys
from pathlib import Path

PS = Path(__file__).resolve().parent
SN = PS.parent
REPO = SN.parent
OUT = PS / "build"
sys.path.insert(0, str(SN / "tools"))
import check_limits as CL  # noqa: E402  (expand() and words(): the journal counter, reused, not copied)

MARK = re.compile(r"\[\[(PENDING [^\]]*|CONFIRM: [^\]]*)\]\]")


# ------------------------------------------------------------------------------------------------ the manuscript
def main_expanded() -> str:
    return CL.expand(SN / "main.tex")


def strip_comments(s: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", s)


def tex_plain(s: str) -> str:
    s = s.replace("--", "\N{EN DASH}").replace("\\,\\%", "%").replace("\\%", "%").replace("\\,", " ")
    s = s.replace("~", " ")
    s = re.sub(r"\\textsuperscript\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"[{}]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def title() -> str:
    m = re.search(r"\\title\{((?:[^{}]|\{[^{}]*\})*)\}", io.open(SN / "main.tex", encoding="utf-8").read())
    # the full title page and the cover letter are never anonymized: the network's name, which the tex prints
    # through \netname{} (SchwingNet / [AuthorLastName]-Net), is SchwingNet here (TITLE.md, 2026-09-25)
    return tex_plain(CL.mode_text(m.group(1), True))


def counts() -> dict:
    s = main_expanded()
    body = s[s.index("\\begin{document}"):]
    parts = re.split(r"\\section\*?\{([^}]*)\}", body)
    tot = sum(CL.words(parts[i + 1]) for i in range(1, len(parts), 2)
              if parts[i].strip().lower() in ("introduction", "materials and methods", "results", "discussion"))
    m = re.search(r"\\section\*\{Abstract\}(.*?)\\clearpage", body, flags=re.S)
    cited = []
    for mm in re.finditer(r"\\cite[pt]?\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}", strip_comments(s)):
        for k in mm.group(1).split(","):
            if k.strip() and k.strip() not in cited:
                cited.append(k.strip())
    return {"WORDS_BODY": f"{tot:,}", "WORDS_ABSTRACT": str(CL.words(m.group(1)) if m else -1),
            "N_FIGURES": str(len(re.findall(r"\\begin\{figure\}", strip_comments(body)))),
            "N_TABLES": str(len(re.findall(r"\\begin\{table\}", strip_comments(s)))),
            "N_REFS": str(len(cited))}


def git(*a) -> str:
    return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True, text=True).stdout.strip()


# ------------------------------------------------------------------------------------------------ front matter
def load_front() -> dict:
    return json.load(io.open(PS / "front_matter.json", encoding="utf-8"))


def fm(front: dict, path: str) -> str:
    """Value at a dotted path; an unconfirmed field prints with a [[CONFIRM]] marker, a missing one as one."""
    node, confirmed = front, True
    for part in path.split("."):
        if isinstance(node, dict) and node.get("confirmed") is False:
            confirmed = False
        node = node[int(part)] if isinstance(node, list) else node.get(part) if isinstance(node, dict) else None
        if node is None:
            return f"[[CONFIRM: {path} (not recorded)]]"
    if isinstance(node, dict):
        if node.get("confirmed") is False:
            confirmed = False
        node = node.get("value")
    if node is None:
        return f"[[CONFIRM: {path} (not recorded)]]"
    if isinstance(node, list):
        node = "; ".join(map(str, node))
    return str(node) + ("" if confirmed else f" [[CONFIRM: {path}]]")


def statements() -> dict:
    s = io.open(PS / "statements.md", encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^## BLOCK: (\w+)\n(.*?)(?=^## BLOCK: |\Z)", s, flags=re.S | re.M):
        out[m.group(1)] = m.group(2).strip()
    return out


def fill(template: str, front: dict, tokens: dict) -> str:
    t = re.sub(r"<!--.*?-->", "", template, flags=re.S).strip() + "\n"
    t = re.sub(r"\{\{fm\.([A-Za-z0-9_.]+)\}\}", lambda m: fm(front, m.group(1)), t)
    t = re.sub(r"\{\{([A-Z_0-9]+)\}\}", lambda m: tokens.get(m.group(1), f"[[CONFIRM: token {m.group(1)}]]"), t)
    t = re.sub(r"\{\{([A-Z_0-9]+)\}\}", lambda m: tokens.get(m.group(1), m.group(0)), t)  # tokens inside blocks
    return t


# ------------------------------------------------------------------------------------------------ numbers
def read_path(file: Path, path: list, md_heading: str | None):
    if file.suffix == ".md":
        s = io.open(file, encoding="utf-8").read()
        s = s[s.index(md_heading):]
        node = json.loads(s[s.index("```json") + 7:s.index("```", s.index("```json") + 7)])
    else:
        node = json.load(io.open(file, encoding="utf-8"))
    for k in path:
        node = node[k]
    return node


def norm_main(s: str) -> str:
    s = strip_comments(s).replace("\\,\\%", "%").replace("\\%", "%").replace("\\,", " ").replace("~", " ")
    return re.sub(r"\s+", " ", s)


def check_numbers(problems: list, notes: list) -> set:
    spec = json.load(io.open(PS / "numbers.json", encoding="utf-8"))
    mtext = norm_main(main_expanded())
    printed = set()
    for n in spec["numbers"]:
        f = SN / n["file"]
        try:
            v = read_path(f, n["path"], n.get("md_heading"))
        except Exception as e:  # a moved key is a wrong number waiting to happen: fail
            problems.append(f"number {n['id']}: cannot read {n['file']} {n['path']}: {e!r}")
            continue
        want = n["printed"].replace(",", "")
        if n["kind"] == "rate_k":
            try:
                den = read_path(f, n["times"], n.get("md_heading"))
            except Exception as e:
                problems.append(f"number {n['id']}: cannot read denominator {n.get('times')}: {e!r}")
                continue
            got = str(int(round(float(v) * float(den))))
        else:
            got = {"int": lambda x: str(int(x)), "pct1": lambda x: f"{100 * float(x):.1f}",
                   "dec2": lambda x: f"{float(x):.2f}"}[n["kind"]](v)
        if got != want:
            problems.append(f"number {n['id']}: file gives {got}, printed {n['printed']} ({n['file']})")
        if n.get("in_main") and not re.search(r"(?<![\d.])" + re.escape(n["printed"]) + r"(?![\d])", mtext):
            problems.append(f"number {n['id']} = {n['printed']} is not in the expanded main.tex")
        printed.add(n["printed"])
    for t in spec.get("text_only", []):
        if t.get("in_main") and t["printed"] not in mtext:
            problems.append(f"text number {t['printed']} is not in the expanded main.tex ({t['source']})")
        printed.add(t["printed"])
        printed.update(re.findall(r"\d[\d,]*(?:\.\d+)?", t["printed"]))
    notes.append(f"{len(spec['numbers'])} numbers re-read from their result files; "
                 f"{len(spec.get('text_only', []))} more checked against the manuscript text")
    return printed


def letter_numbers(letter_md: str, printed: set, commit_tokens: set, problems: list):
    """Every number in the letter is a result (numbers.json), a date or time of a comparator commit read from git
    (commit_tokens), the confidence level 95 or the checklist year 2024. Nothing else may be typed."""
    body = re.sub(r"<!--.*?-->", "", letter_md, flags=re.S)
    body = re.sub(r"\{\{[^}]*\}\}|\[\[[^\]]*\]\]", " ", body)
    floats = set(float_numbers().values())  # a float the letter names must exist under that number in the tree
    for ref in re.findall(r"\b(?:Figure|Table) S?\d+\b", body):
        if ref not in floats:
            problems.append(f"cover letter names {ref}, which the tree does not have")
    body = re.sub(r"\b(?:Figure|Table) S?\d+\b", " ", body)
    allowed = printed | commit_tokens | {"95", "2024"}
    for tok in re.findall(r"(?<![\w.])\d[\d,:]*(?:\.\d+)?(?![\w])", body):
        tok = tok.rstrip(",.")
        if tok not in allowed:
            problems.append(f"cover letter number '{tok}' is not in numbers.json or the comparator commits")


LC_FILE = "SchwingNet/LEVELCHECK_MODEL.md"


def check_comparator_commits(front: dict, letter_src: str, problems: list, notes: list) -> set:
    """The pre-specification claim rests on git: every commit that touched the comparator file is listed in
    front_matter (so an amendment cannot go unmentioned), each listed time equals git's, each is an ancestor of HEAD,
    and each marked in_letter is named in the letter. Returns the day, year and HH:MM tokens the letter may print."""
    lc = front["levelcheck_prespecification"]
    listed = lc["commits"]
    in_git = [ln.split() for ln in git("log", "--format=%H %cI", "--", LC_FILE).splitlines() if ln.strip()]
    tokens = set()
    for full, t in in_git:
        if not any(full.startswith(c["sha"]) for c in listed):
            problems.append(f"{LC_FILE} commit {full[:7]} ({t}) is not in front_matter levelcheck_prespecification.commits "
                            "(every amendment must be accounted for in the letter)")
    for c in listed:
        t = git("show", "-s", "--format=%cI", c["sha"])
        if not t:
            problems.append(f"comparator commit {c['sha'][:7]} is not in this repository")
            continue
        if t != c["time"]:
            problems.append(f"comparator commit {c['sha'][:7]}: front_matter time {c['time']} but git says {t}")
        anc = subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", c["sha"], "HEAD"]).returncode == 0
        if not anc:
            problems.append(f"comparator commit {c['sha'][:7]} is not an ancestor of HEAD")
        if c.get("in_letter") and c["sha"][:7] not in letter_src:
            problems.append(f"comparator commit {c['sha'][:7]} is marked in_letter but the letter does not name it")
        d = dt.datetime.fromisoformat(c["time"])
        tokens |= {str(d.year), str(d.day), d.strftime("%H:%M"), c["sha"][:7]}  # a short SHA can be all digits
    remote = git("branch", "-r", "--contains", listed[-1]["sha"]).split()
    notes.append(f"comparator commits: {len(listed)} listed, {len(in_git)} in git; newest "
                 f"{listed[-1]['sha'][:7]} on remote branches {remote or 'NONE (push before submission)'}")
    return tokens


# ------------------------------------------------------------------------------------------------ CLAIM anchors
SECTION_OF = {"sections/introduction.tex": "Introduction", "sections/methods.tex": "Materials and Methods",
              "sections/results.tex": "Results", "sections/discussion_motivation.tex": "Discussion",
              "sections/discussion_limits.tex": "Discussion", "supplement.tex": "Supplement"}


def float_numbers() -> dict:
    s = strip_comments(main_expanded())
    body = s[s.index("\\begin{document}"):]
    num = {}
    figs = re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", body, flags=re.S)
    for i, f in enumerate(figs, 1):
        for lab in re.findall(r"\\label\{(fig:[^}]*)\}", f):
            num[lab] = f"Figure {i}"
    tabs = re.findall(r"\\begin\{table\}.*?\\end\{table\}", body, flags=re.S)
    for i, t in enumerate(tabs, 1):
        for lab in re.findall(r"\\label\{(tab:[^}]*)\}", t):
            num[lab] = f"Table {i}"
    sup = strip_comments(CL.expand(SN / "supplement.tex"))
    for i, f in enumerate(re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", sup, flags=re.S), 1):
        for lab in re.findall(r"\\label\{(fig:[^}]*)\}", f):
            num[lab] = f"Figure S{i}"
    # Supplement tables in document order: table environments and, since 2026-09-24 (Table S1 prints as a
    # non-floating minipage so endfloat does not move it), \captionof{table}, which also steps LaTeX's counter;
    # its label sits in the caption argument, before the tabular.
    i = 0
    for m in re.finditer(r"\\begin\{table\}.*?\\end\{table\}|\\captionof\{table\}", sup, flags=re.S):
        i += 1
        if m.group(0) == "\\captionof{table}":
            seg = sup[m.end():m.end() + 2000].split("\\begin{tabular}")[0]
            labs = re.findall(r"\\label\{(tab:[^}]*)\}", seg)
        else:
            labs = re.findall(r"\\label\{(tab:[^}]*)\}", m.group(0))
        for lab in labs:
            num[lab] = f"Table S{i}"
    return num


def citation_order_check(num: dict, problems: list):
    """The journal numbers floats by first citation: the float order must equal the first-\\ref order."""
    s = strip_comments(main_expanded())
    body = s[s.index("\\section*{Introduction}") if "\\section*{Introduction}" in s else 0:]
    body = re.sub(r"\\begin\{(figure|table)\}.*?\\end\{(figure|table)\}", " ", body, flags=re.S)
    for kind in ("fig", "tab"):
        seen = []
        for lab in re.findall(r"\\ref\{(" + kind + r":[^}]*)\}", body):
            if lab not in seen and num.get(lab, "").split(" ")[-1].isdigit():
                seen.append(lab)
        order = [int(num[l].split(" ")[-1]) for l in seen]
        if order != sorted(order):
            problems.append(f"{kind} first-citation order {[num[l] for l in seen]} differs from the float order")


def resolve_text(src: str, pats: list):
    f = SN / src
    if not f.exists():
        return None
    raw = io.open(f, encoding="utf-8").read()
    lines = raw.splitlines()
    flat, starts = "", []
    for ln in lines:  # comments blanked (same length), so an anchor never lands in a % comment
        starts.append(len(flat))
        flat += re.sub(r"(?<!\\)%.*", lambda m: " " * len(m.group(0)), ln).lower() + " "
    # map squashed positions back to lines: rebuild with a position table
    pos_map, out = [], []
    prev_space = False
    for i, ch in enumerate(flat):
        if ch.isspace():
            if prev_space:
                continue
            prev_space = True
            out.append(" ")
        else:
            prev_space = False
            out.append(ch)
        pos_map.append(i)
    squash = "".join(out)
    for p in pats:
        q = re.sub(r"\s+", " ", p.lower())
        k = squash.find(q)
        if k < 0:
            continue
        orig = pos_map[k]
        line = max(i for i, st in enumerate(starts) if st <= orig)
        para = ""
        for j in range(line, -1, -1):
            m = re.search(r"\\paragraph\{([^}]*)\}", lines[j]) or \
                (re.match(r"\\textbf\{([^}]*)\}", lines[j]) if src == "main.tex" else None)
            if m:
                para = m.group(1).rstrip(".:")
                break
        if "section*{" in lines[line]:
            para = ""
        if src == "main.tex":
            before = "\n".join(lines[:line + 1])
            if "\\section*{Other information}" in before:
                sec = "Other information"
            elif "\\section*{Abstract}" in before and "\\clearpage\n\\input{sections/introduction}" not in before:
                sec = "Abstract"
            else:
                sec = "Title page"
            if sec == "Title page" and "\\title{" in lines[line]:
                para = "Title"
        else:
            sec = SECTION_OF.get(src, src)
        return {"file": f"{src}:{line + 1}", "where": sec + (f", {para}" if para else "")}
    return None


def resolve_item(it: dict, num: dict, unresolved: list) -> tuple[str, str]:
    where, files = [], []
    for a in it["anchors"]:
        if "label" in a:
            w = num.get(a["label"])
            if w is None:
                unresolved.append(f"item {it['item']}: label {a['label']} not found")
                continue
            where.append(w)
        elif "front" in a:
            where.append(f"Full title page ({a['front']})")
        else:
            r = resolve_text(a["src"], a["find"])
            if r is None:
                unresolved.append(f"item {it['item']}: none of {a['find']} found in {a['src']}")
                continue
            where.append(r["where"])
            files.append(r["file"])
    uniq = []
    for w in where:
        if w not in uniq:
            uniq.append(w)
    return "; ".join(uniq), ", ".join(files)


def expected_where(r: dict, num: dict) -> str:
    """The six-figure placement the item should resolve to (claim2024/map.json 'expect'): section and paragraph
    names plus float labels, the labels turned into the numbers the tree gives them today."""
    e = r.get("expect") or {}
    parts = list(e.get("where", []))
    parts += [num.get(lab, f"{lab} (not in the tree)") for lab in e.get("floats", [])]
    parts += [f"Full title page ({x})" for x in e.get("front", [])]
    return "; ".join(parts)


def placement_mismatch(where: str, expected: str) -> bool:
    """True when every resolved anchor lands in a top-level section the six-figure map does not expect."""
    top = lambda s: {p.split(",")[0].strip() for p in s.split(";") if p.strip()}
    got, exp = top(where), top(expected)
    return bool(got and exp and not (got & exp))


def build_claim(problems: list, unresolved: list, mismatches: list | None = None) -> dict:
    items = json.load(io.open(PS / "claim2024" / "items.json", encoding="utf-8"))
    cmap = json.load(io.open(PS / "claim2024" / "map.json", encoding="utf-8"))
    by = {r["item"]: r for r in cmap["items"]}
    if [i["item"] for i in items["items"]] != list(range(1, 45)) or sorted(by) != list(range(1, 45)):
        problems.append("CLAIM 2024: items.json and map.json must both hold items 1-44")
    num = float_numbers()
    citation_order_check(num, problems)
    rows = []
    for it in items["items"]:
        r = by[it["item"]]
        if r["response"] not in ("Yes", "No", "NA"):
            problems.append(f"CLAIM item {it['item']}: response {r['response']!r}")
        if r["response"] in ("No", "NA") and not r["note"]:
            problems.append(f"CLAIM item {it['item']}: {r['response']} without an explanation")
        if not r.get("expect"):
            problems.append(f"CLAIM item {it['item']}: no six-figure placement ('expect') in map.json")
        n_unres = len(unresolved)
        where, files = resolve_item(r, num, unresolved)
        expected = expected_where(r, num)
        if mismatches is not None and placement_mismatch(where, expected):
            mismatches.append(f"item {it['item']}: anchors land in '{where}', the six-figure map expects '{expected}'")
        rows.append({**it, "response": r["response"], "status": r["status"], "gate": r["gate"],
                     "location": where or "-", "expected": expected, "anchors_resolved": files,
                     "reanchor": len(unresolved) > n_unres, "note": r["note"], "todo": r["todo"]})
    return {"checklist": items["citation"], "instruction": items["instruction"],
            "source_pdf": items["source_pdf"], "source_pdf_sha256": items["source_pdf_sha256"],
            "built": dt.datetime.now().isoformat(timespec="seconds"), "git_head": git("rev-parse", "--short", "HEAD"),
            "float_numbers": num, "rows": rows,
            "tally": {s: sum(1 for x in rows if x["status"] == s) for s in ("READY", "PENDING", "NEEDS-EDIT")},
            "responses": {s: sum(1 for x in rows if x["response"] == s) for s in ("Yes", "No", "NA")}}


def claim_md(c: dict) -> str:
    out = ["# CLAIM 2024 checklist, SchwingNet manuscript", "",
           f"{c['checklist']}. Items verbatim from the published table ({c['source_pdf']}, sha256 "
           f"{c['source_pdf_sha256'][:12]}...). Built {c['built']} at {c['git_head']} by "
           "`packet_src/build_packet_src.py` from `claim2024/map.json`; locations resolved against the tree of "
           "that moment. The submitted .docx has no page or line numbers (journal instruction), so each location "
           "is the section and paragraph a reader sees; the file:line column is for us.", "",
           f"Responses: {c['responses']}. Status: {c['tally']} (PENDING = a gate must land; NEEDS-EDIT = the "
           "wrapped text lacks what the item asks).", "",
           "'Expected' is the six-figure placement (`claim2024/map.json` field `expect`, float labels numbered from "
           "the tree): after the wrap, re-point every anchor marked RE-ANCHOR to text inside that placement.", "",
           "| No. | Section / Topic | Item | Response | Location | Expected (six-figure structure) | file:line | Status | Note | Still owed |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in c["rows"]:
        st = r["status"] + (f" ({r['gate']})" if r["gate"] else "") + (" RE-ANCHOR" if r.get("reanchor") else "")
        topic = r["section"] + (f" / {r['topic']}" if r["topic"] else "")
        out.append(f"| {r['item']} | {topic} | {r['text']} | {r['response']} | {r['location']} | "
                   f"{r.get('expected') or '-'} | {r['anchors_resolved'] or '-'} | {st} | {r['note']} | "
                   f"{r['todo'] or '-'} |")
    out += ["", "2020 to 2024 crosswalk: `claim2024/items.json` field `claim_2020_item` (the 2020 map is "
            "SchwingNet/CLAIM_CHECKLIST.md)."]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ .docx
def new_doc():
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(11)
    st.paragraph_format.line_spacing = 2.0
    return d


def add_runs(p, text: str):
    from docx.shared import RGBColor
    pos = 0
    pat = re.compile(r"\[\[[^\]]*\]\]|\*\*[^*]+\*\*|\*[^*]+\*|\^[^^]+\^")
    for m in pat.finditer(text):
        if m.start() > pos:
            p.add_run(text[pos:m.start()])
        tok = m.group(0)
        if tok.startswith("[["):
            r = p.add_run(tok)
            r.bold = True
            r.font.color.rgb = RGBColor(0xC0, 0, 0)
        elif tok.startswith("**"):
            p.add_run(tok[2:-2]).bold = True
        elif tok.startswith("^"):
            p.add_run(tok[1:-1]).font.superscript = True
        else:
            p.add_run(tok[1:-1]).italic = True
        pos = m.end()
    if pos < len(text):
        p.add_run(text[pos:])


def md_to_docx(md: str, path: Path):
    from docx.shared import Pt
    d = new_doc()
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", md) if b.strip()]
    for b in blocks:
        if b.startswith("# "):
            p = d.add_paragraph()
            r = p.add_run(b[2:].strip())
            r.bold = True
            r.font.size = Pt(14)
        else:
            p = d.add_paragraph()
            lines = b.split("\n")
            for i, ln in enumerate(lines):
                add_runs(p, ln)
                if i < len(lines) - 1:
                    p.add_run().add_break()
    d.save(str(path))


def claim_docx(c: dict, path: Path):
    from docx.shared import Pt
    d = new_doc()
    d.styles["Normal"].paragraph_format.line_spacing = 1.0
    p = d.add_paragraph()
    r = p.add_run("CLAIM: Checklist for Artificial Intelligence in Medical Imaging, 2024 Update")
    r.bold = True
    r.font.size = Pt(13)
    d.add_paragraph(c["checklist"])
    d.add_paragraph(c["instruction"] + " The manuscript file carries no page or line numbers (journal "
                    "instruction), so each location is given by section and paragraph heading.")
    t = d.add_table(rows=1, cols=6)
    t.style = "Table Grid"
    for i, h in enumerate(["Section / Topic", "No.", "Item", "Yes / No / NA", "Location in the manuscript",
                           "Explanation (for No or NA) and status"]):
        t.rows[0].cells[i].text = h
        for run in t.rows[0].cells[i].paragraphs[0].runs:
            run.bold = True
    for r in c["rows"]:
        cells = t.add_row().cells
        cells[0].text = r["section"] + (f" / {r['topic']}" if r["topic"] else "")
        cells[1].text = str(r["item"])
        cells[2].text = r["text"]
        cells[3].text = r["response"]
        if r.get("reanchor"):
            cells[4].text = ""
            add_runs(cells[4].paragraphs[0], (r.get("expected") or "-") + " [[PENDING re-anchor]]")
        else:
            cells[4].text = r["location"]
        expl = r["note"] if r["response"] in ("No", "NA") else ""
        if r["status"] != "READY":
            tag = (f"PENDING {r['gate']}" if r["status"] == "PENDING" else
                   "PENDING edit" + (f" and {r['gate']}" if r["gate"] not in ("", "edit") else ""))
            expl = (expl + " " if expl else "") + f"[[{tag}: {r['todo']}]]"
        cells[5].text = ""
        add_runs(cells[5].paragraphs[0], expl)
    # column widths (inches, 6.5 in text width): Word otherwise splits the narrow response column mid-word ("Ye s")
    from docx.shared import Inches
    t.autofit = False
    widths = [1.0, 0.35, 1.3, 0.5, 1.6, 1.75]
    for row in t.rows:
        for j, cell in enumerate(row.cells):
            cell.width = Inches(widths[j])
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(9)
    d.save(str(path))


# ------------------------------------------------------------------------------------------------ checks
ANON = [(r"sole author", "sole authorship"), (r"\bGuarantor\b", "guarantor statement"),
        (r"commercial interest", "conflict statement"), (r"Wayne State|\bWSU\b", "institution"),
        (r"Detroit", "city of the institution"), (r"General Surgery", "department"),
        (r"Schwing", "surname"), (r"Gregory", "first name"),
        (r"OpenSpineConsortium|Gregory-Schwing|gschwing|gregoryschwingmdphd", "account name")]


def cited_keys() -> list:
    out = []
    # the review copy's citations: a \selfcite is withheld there and cites nothing (2026-09-25)
    for mm in re.finditer(r"\\cite[pt]?\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}",
                          CL.mode_text(strip_comments(main_expanded()), False)):
        for k in mm.group(1).split(","):
            if k.strip() and k.strip() not in out:
                out.append(k.strip())
    return out


def bib_entries() -> dict:
    s = io.open(SN / "refs.bib", encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"@\w+\{([^,\s]+),(.*?)\n\}", s, flags=re.S):
        out[m.group(1)] = m.group(2)
    return out


def anonymization(problems_soft: list, front: dict):
    # the review copy as it prints (rsnastyle.tex: \netname -> [AuthorLastName]-Net, \withheldurl and \selfcite ->
    # their withheld markers; TITLE.md 2026-09-25); the name may appear in no form
    s = CL.mode_text(strip_comments(main_expanded()), False)
    s = s[s.index("\\begin{document}"):]
    for pat, what in ANON:
        n = len(re.findall(pat, s))
        if n:
            problems_soft.append(f"anonymized manuscript carries a {what} ({n} x /{pat}/)")
    if re.search(r"SchwingNet", s):
        problems_soft.append("the network's name SchwingNet is in the review copy: it must print through \\netname{} "
                             "(rsnastyle.tex; TITLE.md)")
    # the reference list is part of the anonymized file: a cited self-reference other than the overlap citation the
    # journal requires (the CTSpinoPelvic1K descriptor) identifies the author (refs.bib schwing2026mixed does, with the
    # account URL; it is uncited today)
    allowed = set(front.get("anonymisation", {}).get("allowed_self_citations", ["ctsp1k"]))
    bib = bib_entries()
    for k in cited_keys():
        e = bib.get(k, "")
        if k not in allowed and re.search(r"author\s*=\s*\{[^}]*Schwing|Gregory-Schwing|gregoryschwing", e):
            problems_soft.append(f"cited reference '{k}' names the author or the author's account (allowed: "
                                 f"{sorted(allowed)})")


OVERCLAIM = [(r"\bnovel\b", "novel"), (r"\bunique\b", "unique"), (r"state[- ]of[- ]the[- ]art|\bSOTA\b", "state of the art"),
             (r"\bfirst (to|time|study|report|method|network|model|system)\b|for the first time", "a priority claim"),
             (r"\boutperform", "outperform"), (r"ground-?breaking|unprecedented", "self-evaluation"),
             (r"510\(k\)|\bde novo\b|FDA (clearance|approval)", "a regulatory pathway")]


def overclaim(text: str, where: str, problems: list):
    """The journal bars self-evaluation and priority claims; the conflict rule bars naming a regulatory pathway."""
    body = re.sub(r"<!--.*?-->|\[\[[^\]]*\]\]", " ", text, flags=re.S)
    for pat, what in OVERCLAIM:
        if re.search(pat, body, flags=re.I):
            problems.append(f"{where} carries {what} (/{pat}/)")


def open_decisions(front: dict) -> list:
    return [d for d in front.get("author_decisions", {}).get("items", []) if not d.get("confirmed")]


def banned(paths: list, problems: list):
    for p in paths:
        if re.search("proven" + "ance", io.open(p, encoding="utf-8", errors="ignore").read(), flags=re.I):
            problems.append(f"banned word in {p.name}")


# ------------------------------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    problems, soft, notes, unresolved = [], [], [], []
    front = load_front()
    blocks = statements()
    tokens = {"TITLE": title(), "DATE": dt.date.today().strftime("%-d %B %Y") if sys.platform != "win32"
              else dt.date.today().strftime("%#d %B %Y"), "GIT_HEAD": git("rev-parse", "--short", "HEAD")}
    tokens.update(counts())
    au = front["authors"][0]
    tokens["AUTHOR_LINE"] = f"{au['first']} {au['middle_initial']} {au['last']}, {au['degrees']}^1^"
    tokens["CREDIT"] = f"{au['first']} {au['middle_initial']} {au['last']}: " + fm(front, "credit_roles")
    tokens["ETHICS_FULL"] = blocks["ETHICS_FULL"]
    tokens["DATA_SHARING_FULL"] = blocks["DATA_SHARING_FULL"]
    others = [o for o in front["subject_overlap"][1:]]
    tokens["OVERLAP_OTHERS"] = " ".join(
        ((o.get("letter_sentence") or f"The same subjects appear in {o['work']} ({o['status']}).") if o.get("confirmed")
         else f"[[CONFIRM: name it or delete it, {o['work']} ({o['status']}); proposed sentence: "
              f"{o.get('letter_sentence') or '-'}]]") for o in others)

    printed = check_numbers(problems, notes)
    letter_src = io.open(PS / "cover_letter.md", encoding="utf-8").read()
    commit_tokens = check_comparator_commits(front, letter_src, problems, notes)
    letter_numbers(letter_src, printed, commit_tokens, problems)
    letter = fill(letter_src, front, tokens)
    tp = fill(io.open(PS / "title_page.md", encoding="utf-8").read(), front, tokens)
    overclaim(letter, "cover letter", problems)
    overclaim(tp, "title page", problems)
    io.open(OUT / "cover_letter.md", "w", encoding="utf-8", newline="\n").write(letter)
    io.open(OUT / "full_title_page.md", "w", encoding="utf-8", newline="\n").write(tp)
    md_to_docx(letter, OUT / "cover_letter.docx")
    md_to_docx(tp, OUT / "full_title_page.docx")

    mismatches = []
    c = build_claim(problems, unresolved, mismatches)
    io.open(OUT / "claim_checklist_2024.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(c, indent=1, ensure_ascii=False) + "\n")
    io.open(OUT / "CLAIM_CHECKLIST_2024.md", "w", encoding="utf-8", newline="\n").write(claim_md(c))
    claim_docx(c, OUT / "claim_checklist_2024.docx")

    anonymization(soft, front)
    decisions = open_decisions(front)
    banned([p for p in PS.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".py", ".tex")], problems)

    marks = {}
    for name, txt in (("cover letter", letter), ("title page", tp),
                      ("CLAIM checklist", json.dumps(c["rows"], ensure_ascii=False))):
        for m in MARK.findall(txt):
            marks.setdefault(name, []).append(m)
    for r in c["rows"]:
        if r["status"] != "READY":
            marks.setdefault("CLAIM checklist", [])
    dirty = git("status", "--porcelain", "--", "SchwingNet")
    rep = ["# packet_src build report", "",
           f"Built {dt.datetime.now().isoformat(timespec='seconds')} at {tokens['GIT_HEAD']}"
           f"{' with uncommitted SchwingNet changes (' + str(len(dirty.splitlines())) + ' paths)' if dirty else ''}.",
           f"Title: {tokens['TITLE']}", "",
           f"Counts (check_limits.py counter): body {tokens['WORDS_BODY']} words, abstract {tokens['WORDS_ABSTRACT']}, "
           f"{tokens['N_FIGURES']} figures, {tokens['N_TABLES']} tables, {tokens['N_REFS']} references.", "",
           "## Hard problems (a wrong number, a missing source, a broken structure)", ""]
    rep += [f"- {x}" for x in problems] or ["- none"]
    rep += ["", "## Decisions only the author can make (front_matter.json author_decisions; --strict fails while open)", ""]
    rep += [f"- **{d['id']}**: {d['what']} (blocks: {', '.join(d.get('blocks', []))})" for d in decisions] or ["- none"]
    rep += ["", "## CLAIM 2024", "", f"Responses {c['responses']}; status {c['tally']}.",
            f"Float numbers resolved from the tree: {c['float_numbers']}", "", "Unresolved anchors (re-point in map.json):", ""]
    rep += [f"- {x}" for x in unresolved] or ["- none"]
    rep += ["", "Anchors that resolve outside the six-figure placement (check the anchor, or the placement):", ""]
    rep += [f"- {x}" for x in mismatches] or ["- none"]
    rep += ["", "Items not READY:", ""]
    rep += [f"- {r['item']} {r['text']}: {r['status']} {r['gate']} - {r['todo']}" for r in c["rows"]
            if r["status"] != "READY"] or ["- none"]
    rep += ["", "## Open markers in the front documents", ""]
    for name, ms in marks.items():
        if name == "CLAIM checklist":
            continue
        rep.append(f"**{name}** ({len(ms)}):")
        rep += [f"- [[{m}]]" for m in ms]
        rep.append("")
    rep += ["## Anonymization of the manuscript file (main.tex expanded, comments stripped)", ""]
    rep += [f"- {x}" for x in soft] or ["- clean"]
    rep += ["", "## Notes", ""] + [f"- {x}" for x in notes]
    io.open(OUT / "BUILD_REPORT.md", "w", encoding="utf-8", newline="\n").write("\n".join(rep) + "\n")
    n_marks = sum(len(v) for k, v in marks.items() if k != "CLAIM checklist")
    print(f"built {OUT}: {len(problems)} hard problems, {len(unresolved)} unresolved CLAIM anchors, "
          f"{len(mismatches)} placement mismatches, {n_marks} open markers in letter + title page, CLAIM {c['tally']}, "
          f"anonymization hits {len(soft)}, open author decisions {len(decisions)}")
    for x in problems:
        print("PROBLEM:", x)
    if problems:
        return 1
    if a.strict and (unresolved or n_marks or decisions or c["tally"]["PENDING"] or c["tally"]["NEEDS-EDIT"]
                     or [x for x in soft if "SchwingNet" not in x]):
        print("STRICT: not ready for submission (see build/BUILD_REPORT.md)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
