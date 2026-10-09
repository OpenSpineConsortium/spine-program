# Copied 2026-10-08 into spine-program/09_wrong_level_clinical_qi/code/ from spinesurg-ct-nnunet
# (private, branch L6_Class, commit 097933a) tools/prior_art_wrong_level.py; last commit 8180a63 2026-09-14. The repository is the
# source of truth; this copy is a record. Its default paths (~/review, ~/FluoroCap_lstv, ~/FluoroCap_s2)
# are the laptop's WSL home, not the grid: see MANIFEST_GRID.md and TODO.md step 0.
"""Prior art: imaging causes of wrong-level spine surgery, transitional anatomy, and learning rare classes.
OpenAlex, top cited per query, deduplicated; writes a markdown table to stdout and a JSON of the rows."""
import json, re, sys, urllib.parse, urllib.request

QUERIES = {
    "wrong-level surgery": ["wrong level spine surgery incidence causes", "wrong site surgery spine intraoperative localization", "wrong level lumbar surgery transitional vertebra",
                            "intraoperative level verification spine fluoroscopy error", "wrong level cervical spine surgery localization", "spine surgery level localization obese patient fluoroscopy",
                            "counting vertebrae error imaging", "thoracic spine localization wrong level count ribs"],
    "transitional anatomy": ["lumbosacral transitional vertebra prevalence Castellvi", "lumbosacral transitional vertebra numbering MRI radiograph", "sacralization lumbarization identification radiograph",
                             "thoracolumbar transitional vertebra 13th rib", "cervical rib prevalence radiograph", "vertebral numbering convention iliolumbar ligament", "six lumbar vertebrae surgery",
                             "hemivertebra block vertebra congenital spine imaging", "Klippel-Feil fusion cervical imaging"],
    "detecting transitional anatomy with AI": ["deep learning lumbosacral transitional vertebra detection", "automatic vertebra labeling transitional vertebrae", "vertebra identification anomalies deep learning L6",
                                              "spine level identification robustness anatomical variants"],
    "learning rare classes": ["long-tailed recognition class imbalance deep learning", "logit adjustment long tail", "class-balanced loss effective number of samples", "learning with rare classes medical imaging",
                              "few-shot rare disease classification medical image", "synthetic oversampling rare class medical imaging"],
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "FluoroCap/1.2 prior-art scan"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


seen = {}; rows = []
for theme, qs in QUERIES.items():
    for q in qs:
        try:
            d = get("https://api.openalex.org/works?search=" + urllib.parse.quote(q) + "&per-page=12&sort=cited_by_count:desc&select=id,doi,title,publication_year,cited_by_count,primary_location")
        except Exception as e:
            print("fail", q, e, file=sys.stderr); continue
        for w in d.get("results", []):
            t = w.get("title") or ""
            if w["id"] in seen or not re.search(r"spine|spinal|vertebr|lumbar|cervical|thoracic|surgery|surgical|long-tail|imbalance|rare|few-shot|logit|class-balanced", t, re.I):
                continue
            seen[w["id"]] = 1
            rows.append({"theme": theme, "q": q, "year": w.get("publication_year"), "title": t, "cited": w.get("cited_by_count"), "doi": w.get("doi"),
                         "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name")})
json.dump(rows, open("prior_art_wrong_level.json", "w"), indent=1)
for theme in QUERIES:
    print(f"\n### {theme}\n\n| Year | Title | Venue | Cited |\n|---|---|---|---|")
    for r in sorted([r for r in rows if r["theme"] == theme], key=lambda r: -(r["cited"] or 0))[:18]:
        print(f"| {r['year']} | {r['title'][:110]} | {(r['venue'] or '')[:34]} | {r['cited']} |")
print(len(rows), "papers", file=sys.stderr)
