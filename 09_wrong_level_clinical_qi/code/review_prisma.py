# Copied 2026-10-08 into spine-program/09_wrong_level_clinical_qi/code/ from spinesurg-ct-nnunet
# (private, branch L6_Class, commit 097933a) tools/review_prisma.py; last commit 3d91ecd 2026-09-15. The repository is the
# source of truth; this copy is a record. Its default paths (~/review, ~/FluoroCap_lstv, ~/FluoroCap_s2)
# are the laptop's WSL home, not the grid: see MANIFEST_GRID.md and TODO.md step 0.
"""PRISMA 2020 / PRISMA-ScR flow counts and diagram for the wrong-level scoping review.

Reads the screening ledger written by review_screen.py and counts the boxes of the flow diagram:
records identified per source, duplicates removed by key, records screened, records excluded at the
automated screen with a reason for each, full texts sought, full texts not retrieved and why,
records assessed, records excluded at assessment with reasons, records included.

The diagram is drawn as plain SVG - rectangles, lines and text, no external library - so it renders
in a browser and in a manuscript without a toolchain.

    python tools/review_prisma.py --screening ~/review/screening.jsonl --out ~/review
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_patterns import CRITERIA  # noqa: E402
from review_screen import read_jsonl  # noqa: E402


def esc(s):
    return html.escape(str(s))


def build_prisma2020_svg(f, prev=None):
    """The conventional PRISMA 2020 flow: identification, screening, eligibility, included, with the
    exclusions beside the step they belong to and a stage band down the left. Both screening passes are
    carried in every box, because the screen was revised and the protocol reports both.

    Plain SVG - rects, lines, text - so it renders in a browser and drops into a manuscript unchanged.
    """
    W = 1200
    # The stage labels are horizontal in a wide band rather than rotated in a narrow one. Rotated text
    # is valid SVG, but the only rasteriser on this machine draws it in the wrong place, and a diagram
    # that cannot be rendered and checked here should not be shipped.
    BX, BW = 14, 98                       # stage band
    LX, LW = 128, 452                     # flow column
    RX_, RW = 638, 548                    # exclusion column
    PAD, LEAD, FS = 13, 16, 12.0
    TOP = 62
    two = prev is not None

    def lines_for(title, pairs):
        out = [("b", title)]
        for label, key in pairs:
            if two:
                out.append(("n", "%s%s / %s" % (label, f[key], prev[key])))
            else:
                out.append(("n", "%s%s" % (label, f[key])))
        return out

    def box_h(lines):
        return PAD * 2 + LEAD * len(lines)

    def draw_box(x, y, w, lines, fill, stroke="#1b1b1b"):
        p = ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="1.3"/>'
             % (x, y, w, box_h(lines), fill, stroke)]
        ty = y + PAD + FS
        for kind, s in lines:
            weight = "700" if kind == "b" else "400"
            size = FS if kind != "s" else FS - 1.5
            colour = "#111" if kind != "s" else "#555"
            p.append('<text x="%d" y="%.1f" font-family="Helvetica,Arial,sans-serif" font-size="%.1f" '
                     'font-weight="%s" fill="%s">%s</text>' % (x + 12, ty, size, weight, colour, esc(s)))
            ty += LEAD
        return "".join(p)

    # Arrowheads are drawn as polygons, not as marker-end. Markers are valid SVG and the rasteriser
    # available here does not draw them, which would have shipped a flow diagram with no arrows on it.
    def vline(x, y1, y2):
        return ('<line x1="%d" y1="%d" x2="%d" y2="%.1f" stroke="#1b1b1b" stroke-width="1.3"/>'
                '<polygon points="%d,%d %.1f,%.1f %.1f,%.1f" fill="#1b1b1b"/>'
                % (x, y1, x, y2 - 7, x, y2, x - 4.5, y2 - 8.0, x + 4.5, y2 - 8.0))

    def hline(x1, x2, y):
        return ('<line x1="%d" y1="%d" x2="%.1f" y2="%d" stroke="#1b1b1b" stroke-width="1.3"/>'
                '<polygon points="%d,%d %.1f,%.1f %.1f,%.1f" fill="#1b1b1b"/>'
                % (x1, y, x2 - 7, y, x2, y, x2 - 8.0, y - 4.5, x2 - 8.0, y + 4.5))

    def reasons(title, d, prev_d, limit=9, wrapw=52):
        out = [("b", title)]
        keys = list(d.keys())
        for k in (prev_d or {}):
            if k not in keys:
                keys.append(k)
        keys = keys[:limit]
        for k in keys:
            txt = "%s: %s" % (k, d.get(k, 0))
            if two:
                txt = "%s: %s / %s" % (k, d.get(k, 0), (prev_d or {}).get(k, 0))
            for i, ln in enumerate(wrap(txt, wrapw)):
                out.append(("n", ln if i == 0 else "    " + ln))
        return out

    body = []
    y = TOP

    # 1 identification
    l1 = lines_for("Records identified", [("Total: ", "identified_total")])
    for s, n in f["identified_per_source"].items():
        l1.append(("s", "   %s: %d" % (s, n)))
    r1 = [("b", "Records removed before screening")]
    for k, n in f["duplicates_removed_by_key"].items():
        r1.append(("n", "Duplicates matched on %s: %d" % (k, n)))
    r1.append(("n", "Total removed: %d" % f["duplicates_removed_total"]))
    h = max(box_h(l1), box_h(r1))
    body += [draw_box(LX, y, LW, l1, "#eaf0f6"), draw_box(RX_, y, RW, r1, "#f6f1ec"),
             hline(LX + LW, RX_, y + box_h(l1) // 2)]
    id_top, id_bot = y, y + h
    y += h + 34

    # 2 screening
    l2 = lines_for("Records screened", [("", "records_screened")])
    r2 = reasons("Records excluded by the automated screen",
                 f["excluded_at_screen_by_reason"], (prev or {}).get("excluded_at_screen_by_reason"))
    r2.append(("n", "Total: %s" % ("%d / %d" % (f["excluded_at_screen_total"], prev["excluded_at_screen_total"])
                                   if two else f["excluded_at_screen_total"])))
    body += [vline(LX + LW // 2, y - 34, y - 3)]
    h = max(box_h(l2), box_h(r2))
    body += [draw_box(LX, y, LW, l2, "#eaf0f6"), draw_box(RX_, y, RW, r2, "#f6f1ec"),
             hline(LX + LW, RX_, y + box_h(l2) // 2)]
    scr_top, scr_bot = y, y + h
    y += h + 34

    # 3 reports sought
    groups = {"No abstract and no open full text": 0, "Text held but no review term matched": 0,
              "Fetch failure (HTTP or network)": 0}
    pgroups = dict.fromkeys(groups, 0)
    for src, dst in ((f, groups), (prev or {}, pgroups)):
        for k, n in (src.get("fulltext_not_retrieved_by_reason") or {}).items():
            if k.startswith("fetch failure"):
                dst["Fetch failure (HTTP or network)"] += n
            elif "no passage matched" in k or "no review term matched" in k:
                dst["Text held but no review term matched"] += n
            else:
                dst["No abstract and no open full text"] += n
    l3 = lines_for("Reports sought for retrieval", [("", "fulltext_sought")])
    r3 = [("b", "Reports not retrieved")]
    for k in groups:
        r3.append(("n", "%s: %s" % (k, "%d / %d" % (groups[k], pgroups[k]) if two else groups[k])))
    r3.append(("n", "Total: %s" % ("%d / %d" % (f["fulltext_not_retrieved_total"],
                                                prev["fulltext_not_retrieved_total"]) if two
                                   else f["fulltext_not_retrieved_total"])))
    r3.append(("s", "PRISMA_FLOW.md lists each HTTP code"))
    body += [vline(LX + LW // 2, y - 34, y - 3)]
    h = max(box_h(l3), box_h(r3))
    body += [draw_box(LX, y, LW, l3, "#eaf0f6"), draw_box(RX_, y, RW, r3, "#f6f1ec"),
             hline(LX + LW, RX_, y + box_h(l3) // 2)]
    el_top = y
    y += h + 34

    # 4 assessed
    l4 = lines_for("Reports assessed for eligibility", [("", "records_assessed")])
    r4 = reasons("Reports excluded at assessment",
                 f["excluded_at_assessment_by_reason"], (prev or {}).get("excluded_at_assessment_by_reason"))
    r4.append(("n", "Total: %s" % ("%d / %d" % (f["excluded_at_assessment_total"],
                                                prev["excluded_at_assessment_total"]) if two
                                   else f["excluded_at_assessment_total"])))
    body += [vline(LX + LW // 2, y - 34, y - 3)]
    h = max(box_h(l4), box_h(r4))
    body += [draw_box(LX, y, LW, l4, "#eaf0f6"), draw_box(RX_, y, RW, r4, "#f6f1ec"),
             hline(LX + LW, RX_, y + box_h(l4) // 2)]
    el_bot = y + h
    y += h + 34

    # 5 included
    l5 = lines_for("Sources included in the review", [("", "records_included")])
    l5.append(("s", "with a denominator and a numerator: %s"
               % ("%d / %d" % (f.get("with_denominator_and_numerator", 0),
                               prev.get("with_denominator_and_numerator", 0)) if two
                  else f.get("with_denominator_and_numerator", 0))))
    body += [vline(LX + LW // 2, y - 34, y - 3), draw_box(LX, y, LW, l5, "#e7efe6")]
    inc_top, inc_bot = y, y + box_h(l5)
    y = inc_bot

    # stage bands
    bands = [("Identification", id_top, id_bot), ("Screening", scr_top, scr_bot),
             ("Eligibility", el_top, el_bot), ("Included", inc_top, inc_bot)]
    for name, t, b in bands:
        body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#dfe6ee" stroke="#9aa8b6" '
                    'stroke-width="1"/>' % (BX, t, BW, b - t))
        parts = wrap(name, 13)
        cy = (t + b) / 2.0 - (len(parts) - 1) * 7.5 + 4
        for i, ln in enumerate(parts):
            body.append('<text x="%.1f" y="%.1f" font-family="Helvetica,Arial,sans-serif" font-size="12.5" '
                        'font-weight="700" fill="#2b3946" text-anchor="middle">%s</text>'
                        % (BX + BW / 2.0, cy + i * 15, esc(ln)))

    head = ('<text x="128" y="30" font-family="Helvetica,Arial,sans-serif" font-size="16" '
            'font-weight="700" fill="#111">PRISMA 2020 flow: wrong-level and wrong-site spine surgery, '
            'a scoping review</text>')
    key = ('<text x="128" y="50" font-family="Helvetica,Arial,sans-serif" font-size="11.5" fill="#444">'
           'Every count is pass 2 (title + abstract) / pass 1 (title only). The screen was revised after '
           'the abstracts were fetched, and the protocol reports both passes.</text>') if two else ''
    foot = ('<text x="128" y="%.1f" font-family="Helvetica,Arial,sans-serif" font-size="10.5" fill="#555">'
            'tools/review_prisma.py from review/screening.jsonl and screening_titleonly.jsonl. Screening '
            'is machine-assisted; the 200-row validation sample is unread, so the counts describe what the '
            'patterns decided.</text>' % (y + 26))
    H = y + 44
    defs = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="7.5" '
            'markerHeight="7.5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#1b1b1b"/></marker></defs>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'font-family="Helvetica,Arial,sans-serif"><rect width="100%%" height="100%%" fill="#ffffff"/>'
            '%s%s%s%s%s</svg>' % (W, H, W, H, defs, head, key, "".join(body), foot))


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def svg_box(x, y, w, h, lines, fill="#ffffff", bold_first=True, size=11):
    parts = ['<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="#222" stroke-width="1.2"/>'
             % (x, y, w, h, fill)]
    ty = y + 18
    for i, ln in enumerate(lines):
        weight = "600" if (i == 0 and bold_first) else "400"
        parts.append('<text x="%d" y="%d" font-family="Helvetica,Arial,sans-serif" font-size="%d" '
                     'font-weight="%s" fill="#111">%s</text>' % (x + 10, ty, size, weight, html.escape(ln)))
        ty += size + 4
    return "".join(parts)


def svg_arrow(x1, y1, x2, y2):
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#222" stroke-width="1.2" '
            'marker-end="url(#a)"/>' % (x1, y1, x2, y2))


def build_svg(f):
    W = 1000
    LX, LW = 60, 430          # left column (flow)
    RX_, RW = 560, 380        # right column (exclusions)
    y = 60
    body = []
    heights = []

    def box(x, w, lines, fill="#ffffff"):
        h = 16 + (len(lines) * 15) + 8
        return h, svg_box(x, y, w, h, lines, fill)

    ident = ["Records identified (n = %d)" % f["identified_total"]]
    for s, n in f["identified_per_source"].items():
        ident.append("   %s: n = %d" % (s, n))
    h1, b1 = box(LX, LW, ident, "#eef2f7")
    body.append(b1)

    dup_lines = ["Duplicate records removed (n = %d)" % f["duplicates_removed_total"]]
    for k, n in f["duplicates_removed_by_key"].items():
        dup_lines.append("   matched on %s: n = %d" % (k, n))
    hd, bd = box(RX_, RW, dup_lines, "#f7f2ee")
    body.append(bd)
    body.append(svg_arrow(LX + LW, y + h1 // 2, RX_, y + h1 // 2))
    y += max(h1, hd) + 42
    body.append(svg_arrow(LX + LW // 2, y - 42, LX + LW // 2, y - 4))

    withabs = f.get("screen_pass") == "title_and_abstract"
    h2, b2 = box(LX, LW, [("Records screened on title, abstract and publication type (n = %d)" if withabs
                           else "Records screened on title and publication type (n = %d)")
                          % f["records_screened"]], "#eef2f7")
    body.append(b2)
    ex1 = ["Records excluded at the automated screen (n = %d)" % f["excluded_at_screen_total"]]
    for k, n in f["excluded_at_screen_by_reason"].items():
        ex1.append("   %s: n = %d" % (k, n))
    he1, be1 = box(RX_, RW, ex1, "#f7f2ee")
    body.append(be1)
    body.append(svg_arrow(LX + LW, y + h2 // 2, RX_, y + h2 // 2))
    y += max(h2, he1) + 42
    body.append(svg_arrow(LX + LW // 2, y - 42, LX + LW // 2, y - 4))

    h3, b3 = box(LX, LW, [(("Abstracts and full texts sought (n = %d)" if withabs
                            else "Full texts sought from the held corpus (n = %d)") % f["fulltext_sought"])], "#eef2f7")
    body.append(b3)
    # The per-record HTTP codes belong in the table, not in a box on a diagram; group them here.
    groups = {"no open full text": 0, "full text held but no review term matched": 0,
              "fetch failure (HTTP or network)": 0}
    for k, n in f["fulltext_not_retrieved_by_reason"].items():
        if k.startswith("fetch failure"):
            groups["fetch failure (HTTP or network)"] += n
        elif "no passage matched" in k or "no review term matched" in k:
            groups["full text held but no review term matched"] += n
        else:
            groups["no open full text"] += n
    ex2 = [("No abstract and no full text retrieved (n = %d)" if withabs
            else "Full texts not retrieved (n = %d)") % f["fulltext_not_retrieved_total"]]
    for k, n in groups.items():
        if n:
            for ln in wrap("%s: n = %d" % (k, n), 46):
                ex2.append("   " + ln)
    ex2.append("   (the table in PRISMA_FLOW.md gives each HTTP code)")
    he2, be2 = box(RX_, RW, ex2, "#f7f2ee")
    body.append(be2)
    body.append(svg_arrow(LX + LW, y + h3 // 2, RX_, y + h3 // 2))
    y += max(h3, he2) + 42
    body.append(svg_arrow(LX + LW // 2, y - 42, LX + LW // 2, y - 4))

    h4, b4 = box(LX, LW, ["Records assessed against the criteria (n = %d)" % f["records_assessed"]], "#eef2f7")
    body.append(b4)
    ex3 = ["Records excluded at assessment (n = %d)" % f["excluded_at_assessment_total"]]
    for k, n in f["excluded_at_assessment_by_reason"].items():
        ex3.append("   %s: n = %d" % (k, n))
    he3, be3 = box(RX_, RW, ex3, "#f7f2ee")
    body.append(be3)
    body.append(svg_arrow(LX + LW, y + h4 // 2, RX_, y + h4 // 2))
    y += max(h4, he3) + 42
    body.append(svg_arrow(LX + LW // 2, y - 42, LX + LW // 2, y - 4))

    inc = ["Records included in the review (n = %d)" % f["records_included"],
           "   with an extractable denominator and numerator: n = %d" % f.get("with_denominator_and_numerator", 0)]
    h5, b5 = box(LX, LW, inc, "#e6efe6")
    body.append(b5)
    y += h5 + 40
    heights.append(y)

    head = ('<text x="60" y="34" font-family="Helvetica,Arial,sans-serif" font-size="15" font-weight="600" '
            'fill="#111">PRISMA-ScR flow: wrong-level and wrong-site spine surgery scoping review</text>')
    foot = ('<text x="60" y="%d" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#555">'
            'Counts from review/PRISMA_FLOW.json, produced by tools/review_prisma.py from '
            'review/screening.jsonl. Screening is machine-assisted; the validation sample is unread.</text>' % (y + 6))
    defs = ('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#222"/></marker></defs>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<rect width="100%%" height="100%%" fill="#ffffff"/>%s%s%s%s</svg>'
            % (W, y + 24, W, y + 24, defs, head, "".join(body), foot))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screening", default=os.path.expanduser("~/review/screening.jsonl"))
    ap.add_argument("--extraction", default=os.path.expanduser("~/review/extraction.jsonl"))
    ap.add_argument("--incidence", default=os.path.expanduser("~/review/incidence.csv"))
    ap.add_argument("--out", default=os.path.expanduser("~/review"))
    ap.add_argument("--previous", default="", help="a directory holding the earlier pass's "
                                                   "PRISMA_FLOW.json; both passes are then drawn")
    a = ap.parse_args()
    out = os.path.expanduser(a.out)

    header = None
    rows = []
    for r in read_jsonl(os.path.expanduser(a.screening)):
        if r.get("record_type") == "criteria":
            header = r
        else:
            rows.append(r)
    if header is None:
        print("no criteria header in the screening ledger")
        return 1
    dd = header["dedup"]

    by_stage = Counter()
    ex_screen, ex_ft, ex_assess = Counter(), Counter(), Counter()
    for r in rows:
        by_stage[(r["stage"], r["decision"])] += 1
        if r["decision"] != "exclude":
            continue
        if r["stage"] == "screen":
            ex_screen[r["reason"]] += 1
        elif r["stage"] == "fulltext_retrieval":
            ex_ft[r["reason_text"]] += 1
        else:
            ex_assess[r["reason"]] += 1

    screened = len(rows)
    ex_screen_total = sum(ex_screen.values())
    sought = screened - ex_screen_total
    ft_missing = sum(ex_ft.values())
    assessed = sought - ft_missing
    ex_assess_total = sum(ex_assess.values())
    included = assessed - ex_assess_total

    n_incidence = 0
    if os.path.exists(os.path.expanduser(a.incidence)):
        with open(os.path.expanduser(a.incidence), encoding="utf-8") as fh:
            n_incidence = max(0, sum(1 for _ in fh) - 1)

    reason_text = dict(CRITERIA["exclusions"])
    flow = {
        "review_title": CRITERIA["review_title"],
        "criteria_id": CRITERIA["criteria_id"],
        "screen_pass": header.get("screen_pass", "title_only"),
        "abstracts_used": header.get("abstracts_used", 0),
        "identified_total": dd["identified_total"],
        "identified_per_source": dd["identified_per_source"],
        "duplicates_removed_total": dd["removed_total"],
        "duplicates_removed_by_key": dd["removed_by_key"],
        "duplicates_removed_by_key_and_scope": dd["removed_by_key_and_scope"],
        "records_screened": screened,
        "excluded_at_screen_total": ex_screen_total,
        "excluded_at_screen_by_reason": dict(ex_screen.most_common()),
        "fulltext_sought": sought,
        "fulltext_not_retrieved_total": ft_missing,
        "fulltext_not_retrieved_by_reason": dict(ex_ft.most_common()),
        "records_assessed": assessed,
        "excluded_at_assessment_total": ex_assess_total,
        "excluded_at_assessment_by_reason": dict(ex_assess.most_common()),
        "records_included": included,
        "with_denominator_and_numerator": n_incidence,
        "reason_codes": reason_text,
        "note": ("Records with no retrieved text are counted in the full-text box rather than at the "
                 "automated screen, so that the flow separates 'not judged' from 'judged and excluded'."),
    }
    with open(os.path.join(out, "PRISMA_FLOW.json"), "w", encoding="utf-8") as fh:
        json.dump(flow, fh, indent=1)

    L = ["# PRISMA-ScR flow", "",
         "_" + CRITERIA["review_title"] + "_", "",
         "Counts produced by `tools/review_prisma.py` from `review/screening.jsonl`. Every count below is a "
         "count of rows in that file carrying the named stage and reason code; no count is entered by hand.", "",
         "## Identification", "", "| source | records identified |", "|---|---:|"]
    for s, n in flow["identified_per_source"].items():
        L.append("| %s | %d |" % (s, n))
    L.append("| **total** | **%d** |" % flow["identified_total"])
    L += ["", "### Duplicates removed", "", "| matched on | removed |", "|---|---:|"]
    for k, n in flow["duplicates_removed_by_key"].items():
        L.append("| %s | %d |" % (k, n))
    L.append("| **total** | **%d** |" % flow["duplicates_removed_total"])
    L += ["", "Split by whether the duplicate came from the other source or the same one:", "",
          "| matched on / scope | removed |", "|---|---:|"]
    for k, n in flow["duplicates_removed_by_key_and_scope"].items():
        L.append("| %s | %d |" % (k, n))

    L += ["", "## Screening", "",
          "Records screened: **%d**" % flow["records_screened"], "",
          "### Excluded at the automated screen (title and publication type)", "",
          "| reason | n | what the reason means |", "|---|---:|---|"]
    for k, n in flow["excluded_at_screen_by_reason"].items():
        L.append("| `%s` | %d | %s |" % (k, n, reason_text.get(k, "")))
    L.append("| **total** | **%d** | |" % flow["excluded_at_screen_total"])

    L += ["", "## Full text", "",
          "Full texts sought from the held corpus: **%d**" % flow["fulltext_sought"], "",
          "### Full texts not retrieved", "", "| reason | n |", "|---|---:|"]
    for k, n in flow["fulltext_not_retrieved_by_reason"].items():
        L.append("| %s | %d |" % (k.replace("|", "/"), n))
    L.append("| **total** | **%d** |" % flow["fulltext_not_retrieved_total"])

    L += ["", "## Assessment", "",
          "Records assessed against the criteria: **%d**" % flow["records_assessed"], "",
          "### Excluded at assessment", "", "| reason | n | what the reason means |", "|---|---:|---|"]
    for k, n in flow["excluded_at_assessment_by_reason"].items():
        L.append("| `%s` | %d | %s |" % (k, n, reason_text.get(k, "")))
    L.append("| **total** | **%d** | |" % flow["excluded_at_assessment_total"])

    L += ["", "## Included", "",
          "Records included: **%d**" % flow["records_included"], "",
          "Of those, records carrying both a denominator and a numerator, and so usable for a proportion "
          "synthesis: **%d** (`review/incidence.csv`)." % flow["with_denominator_and_numerator"], "",
          "![PRISMA flow](prisma_flow.svg)", "",
          "## A note on where the boxes sit", "", flow["note"], "",
          "The screen is machine-assisted. Its precision and recall are not known and cannot be stated until the "
          "`human_decision` column of `review/validation_sample.csv` is filled in.", ""]
    with open(os.path.join(out, "PRISMA_FLOW.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))

    prev = None
    if a.previous:
        pp = os.path.join(os.path.expanduser(a.previous), "PRISMA_FLOW.json")
        if os.path.exists(pp):
            prev = json.load(open(pp, encoding="utf-8"))
        else:
            print("no previous flow at " + pp + "; drawing one pass")
    with open(os.path.join(out, "prisma_flow.svg"), "w", encoding="utf-8") as fh:
        fh.write(build_prisma2020_svg(flow, prev))
    with open(os.path.join(out, "prisma_flow_simple.svg"), "w", encoding="utf-8") as fh:
        fh.write(build_svg(flow))

    print("identified %d, dedup -%d, screened %d, excluded %d, sought %d, not retrieved %d, assessed %d, "
          "excluded %d, included %d, incidence %d"
          % (flow["identified_total"], flow["duplicates_removed_total"], flow["records_screened"],
             flow["excluded_at_screen_total"], flow["fulltext_sought"], flow["fulltext_not_retrieved_total"],
             flow["records_assessed"], flow["excluded_at_assessment_total"], flow["records_included"],
             flow["with_denominator_and_numerator"]))
    print("wrote PRISMA_FLOW.md, PRISMA_FLOW.json, prisma_flow.svg in " + out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
