# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/render.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/render.py -- HTML for the dashboard, the login page and the case page. No template engine, no JS
framework; a small Markdown subset for the case README (headings, lists, fenced code, tables as preformatted
text, bold and inline code), everything HTML-escaped first so a README cannot inject markup.

Run: not a script; imported by app.py.
"""
from __future__ import annotations

import html
import json
import re
from typing import Dict, List, Optional

CSS = """
body{font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f9;color:#1b1f23}
header{background:#22303c;color:#fff;padding:.6rem 1.2rem;display:flex;gap:1.2rem;align-items:center}
header a{color:#cfe3ff;text-decoration:none}header .sp{flex:1}
main{max-width:1100px;margin:1rem auto;padding:0 1rem}
.card{background:#fff;border:1px solid #dde2e8;border-radius:8px;padding:1rem 1.2rem;margin-bottom:1rem}
h1{font-size:1.35rem;margin:.2rem 0 .6rem}h2{font-size:1.1rem;margin:.9rem 0 .4rem}h3{font-size:1rem;margin:.7rem 0 .3rem}
table{border-collapse:collapse;font-size:.92rem}td,th{border:1px solid #d5dbe3;padding:.25rem .55rem;vertical-align:top}
th{background:#eef2f6;text-align:left}
code,pre{font:.86rem/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre{background:#f0f2f5;border:1px solid #e1e5ea;border-radius:6px;padding:.6rem .8rem;overflow:auto;white-space:pre-wrap}
.tag{display:inline-block;background:#e8eef7;border:1px solid #c9d6ea;border-radius:4px;padding:0 .4rem;margin:0 .2rem .2rem 0;font-size:.85rem}
.paired{background:#fde9c8;border-color:#f3c98a}
.warn{background:#fff4e5;border:1px solid #f3c98a;border-radius:6px;padding:.5rem .8rem}
.err{background:#fdecea;border:1px solid #f5b5b0;border-radius:6px;padding:.5rem .8rem}
.previews img{max-width:100%;height:auto;border:1px solid #d5dbe3;border-radius:4px;margin:.3rem 0}
.verdicts label{display:inline-block;margin-right:1.2rem;font-weight:600}
textarea{width:100%;min-height:5rem;font:inherit;padding:.4rem}
button{font:inherit;padding:.45rem 1rem;border-radius:6px;border:1px solid #2f6fdd;background:#2f6fdd;color:#fff;cursor:pointer}
button.secondary{background:#fff;color:#2f6fdd}
.muted{color:#5a6673;font-size:.9rem}.kv td:first-child{font-weight:600;white-space:nowrap}
"""


def esc(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def page(title: str, body: str, user: Optional[str] = None, role: Optional[str] = None,
         app_title: str = "Transitional-vertebra review") -> str:
    who = f"<span class=muted>{esc(user)} · {esc(role)}</span> <a href=/logout>log out</a>" if user else \
        "<a href=/login>log in</a>"
    return (f"<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width'>"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body>"
            f"<header><a href=/><b>{esc(app_title)}</b></a><a href=/work>next case</a>"
            f"<span class=sp></span>{who}</header><main>{body}</main></body></html>")


# ── Markdown subset ──────────────────────────────────────────────────────────

_INLINE = [(re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
           (re.compile(r"\*\*([^*]+)\*\*"), r"<b>\1</b>"),
           (re.compile(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])"), r"<i>\1</i>")]


def _inline(s: str) -> str:
    s = esc(s)
    for rx, rep in _INLINE:
        s = rx.sub(rep, s)
    return s


def md_to_html(text: str) -> str:
    out: List[str] = []
    lines = text.splitlines()
    i = 0
    in_list = None
    para: List[str] = []

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + " ".join(_inline(x) for x in para) + "</p>")
            para = []

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            flush_para(); close_list()
            j = i + 1
            block = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                block.append(lines[j]); j += 1
            out.append("<pre>" + esc("\n".join(block)) + "</pre>")
            i = j + 1
            continue
        if ln.lstrip().startswith("|"):
            flush_para(); close_list()
            j = i
            block = []
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                block.append(lines[j]); j += 1
            out.append("<pre>" + esc("\n".join(block)) + "</pre>")
            i = j
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            flush_para(); close_list()
            lvl = min(len(m.group(1)) + 1, 4)
            out.append(f"<h{lvl}>{_inline(m.group(2).strip())}</h{lvl}>")
            i += 1
            continue
        m = re.match(r"^\s*([-*+]|\d+[.)])\s+(.*)$", ln)
        if m:
            flush_para()
            kind = "ol" if m.group(1)[0].isdigit() else "ul"
            if in_list != kind:
                close_list()
                out.append(f"<{kind}>")
                in_list = kind
            out.append(f"<li>{_inline(m.group(2))}</li>")
            i += 1
            continue
        if not ln.strip():
            flush_para(); close_list()
            i += 1
            continue
        para.append(ln.strip())
        i += 1
    flush_para(); close_list()
    return "\n".join(out)


# ── pieces ───────────────────────────────────────────────────────────────────

def kv_table(d: Dict, cls: str = "kv") -> str:
    if not d:
        return "<p class=muted>(none)</p>"
    rows = []
    for k, v in d.items():
        if isinstance(v, (dict, list)):
            v = f"<pre>{esc(json.dumps(v, indent=1, ensure_ascii=False))}</pre>"
        else:
            v = esc(v)
        rows.append(f"<tr><td>{esc(k)}</td><td>{v}</td></tr>")
    return f"<table class='{cls}'>{''.join(rows)}</table>"


def evidence_html(ev) -> str:
    if ev is None:
        return "<p class=muted>No evidence.json for this case.</p>"
    if isinstance(ev, dict):
        return kv_table(ev)
    return f"<pre>{esc(json.dumps(ev, indent=1, ensure_ascii=False))}</pre>"


def case_page(p: dict, user: str, role: str, app_title: str, message: str = "") -> str:
    stage = p["stage"]
    tags = "".join(f"<span class=tag>{esc(f)}</span>" for f in p.get("flags", []))
    rules = "".join(f"<span class=tag>{esc(f)}</span>" for f in p.get("rules", []))
    paired = "<span class='tag paired'>paired: radiograph of the same person exists</span>" if p["paired"] else \
        "<span class=tag>CT only</span>"
    head = (f"<div class=card><h1>Case {esc(p['case_id'])} <span class=muted>· stage {stage} "
            f"({'screen' if stage == 1 else 'confirm'})</span></h1>"
            f"<p><b>Type:</b> {esc(p['type'])} — {esc(p['type_meaning'])}</p>"
            f"<p>{paired} {tags}</p>"
            + (f"<p><b>Rules that raised it:</b> {rules}</p>" if rules else "")
            + (f"<p class=muted>Collection {esc(p['collection'])} · person {esc(p['person_key'])} · claimed "
               f"{esc(p['claimed_at'])} · claim expires {esc(p['expires_at'])}</p>")
            + (f"<div class=warn>{esc(message)}</div>" if message else "")
            + (f"<div class=err><b>Tree problems on this case:</b> {esc('; '.join(p['missing']))}</div>"
               if p.get("missing") else "")
            + "</div>")
    readme = (f"<div class=card><h2>Case README</h2>{md_to_html(p['readme_md'])}</div>" if p.get("readme_md")
              else "<div class=card><h2>Case README</h2><p class=err>README.md missing in the tree.</p></div>")
    previews = ""
    if p.get("previews"):
        imgs = "".join(f"<figure><img src='{esc(u)}' alt='{esc(u.rsplit('/', 1)[-1])}'>"
                       f"<figcaption class=muted>{esc(u.rsplit('/', 1)[-1])}</figcaption></figure>"
                       for u in p["previews"])
        previews = f"<div class='card previews'><h2>Previews</h2>{imgs}</div>"
    else:
        previews = ("<div class=card><h2>Previews</h2><p class=muted>No PNG previews in the tree for this case; "
                    "open the volumes in a viewer with the commands below.</p></div>")
    files = p.get("files") or {}
    flist = "".join(f"<tr><td>{esc(k)}</td><td>{'<br>'.join(esc(x) for x in v)}</td></tr>" for k, v in files.items())
    cmds = "".join(f"<h3>{esc(k)}</h3><pre>{esc(v)}</pre>" for k, v in (p.get("open_commands") or {}).items())
    viewer = (f"<div class=card><h2>Open in a viewer</h2><p class=muted>Tree root on your machine: "
              f"<code>{esc(p['tree_root'])}</code>. Paths below are relative to it.</p>"
              f"{'<table>' + flist + '</table>' if flist else '<p class=muted>No volumes listed for this case.</p>'}"
              f"{cmds}</div>")
    ev = f"<div class=card><h2>Rule evidence</h2>{evidence_html(p.get('evidence'))}" \
         f"{kv_table(p.get('manifest') or {}) if p.get('manifest') else ''}</div>"
    prior = ""
    if p.get("prior"):
        prior = f"<div class=card><h2>Prior call (shown to the confirmer by configuration)</h2>{kv_table(p['prior'])}</div>"
    labels = {"accept": "accept — the case is what its type says", "reject": "reject — it is not",
              "unsure": "unsure — cannot decide from what is here",
              "confirm": "confirm — the case is what its type says", "overturn": "overturn — it is not"}
    radios = "".join(f"<label><input type=radio name=verdict value='{v}' required> {esc(labels.get(v, v))}</label><br>"
                     for v in p["verdicts"])
    req = "required" if p.get("reason_required") else ""
    form = (f"<div class=card><h2>Your verdict</h2><form method=post action=/submit>"
            f"<input type=hidden name=claim_token value='{esc(p['claim_token'])}'>"
            f"<div class=verdicts>{radios}</div>"
            f"<p><textarea name=reason placeholder='Reason, in your own words (what you saw that decided it)' {req}></textarea></p>"
            f"<button type=submit>Submit and take the next case</button> "
            f"<button type=submit class=secondary formaction=/release formnovalidate>Release this case (no verdict)</button>"
            f"</form></div>")
    return page(f"Case {p['case_id']}", head + readme + previews + viewer + ev + prior + form, user, role, app_title)


def dashboard(s: dict, public_names: bool, app_title: str, user: Optional[str], role: Optional[str]) -> str:
    fin = "".join(f"<tr><td>{esc(k)}</td><td>{v}</td></tr>" for k, v in s["by_final"].items())
    finals = ["pending_stage1", "rejected", "pending_stage2", "confirmed", "overturned", "unresolved"]
    th = "".join(f"<th>{f}</th>" for f in finals)
    bt = "".join(f"<tr><td>{esc(t)}</td>" + "".join(f"<td>{c.get(f, 0)}</td>" for f in finals) +
                 f"<td>{sum(c.values())}</td></tr>" for t, c in s["by_type"].items())
    users = ""
    if public_names:
        users = "<h2>Verdicts by reviewer</h2><table><tr><th>reviewer</th><th>n</th></tr>" + "".join(
            f"<tr><td>{esc(k)}</td><td>{v}</td></tr>" for k, v in s["reviews_by_user"].items()) + "</table>"
    body = (f"<div class=card><h1>{esc(app_title)}</h1>"
            f"<p>{s['n_cases']} cases · {s['paired'].get('paired', 0)} paired · stage-1 queue {s['queue_stage1']} · "
            f"stage-2 queue {s['queue_stage2']} · {s['n_review_records']} verdict records on disk</p>"
            f"<p class=muted>PREREG {esc(s['prereg_status'])} {esc((s['prereg_sha256'] or '')[:12])} · code "
            f"{esc((s['git_sha'] or 'unknown')[:12])} · {esc(s['tool'])} v{esc(s['tool_version'])}</p></div>"
            f"<div class=card><h2>By status</h2><table><tr><th>status</th><th>n</th></tr>{fin}</table>"
            f"<h2>By type</h2><table><tr><th>type</th>{th}<th>total</th></tr>{bt}</table>{users}</div>")
    return page(app_title, body, user, role, app_title)


def login_page(app_title: str, error: str = "", dev: bool = False) -> str:
    note = ("<div class=warn>Development mode: no REVIEW_USERS configured, the token is your user name.</div>"
            if dev else "")
    err = f"<div class=err>{esc(error)}</div>" if error else ""
    body = (f"<div class=card><h1>Log in</h1>{note}{err}<form method=post action=/login>"
            f"<p><label>User name<br><input name=user autocomplete=username></label></p>"
            f"<p><label>Token<br><input name=token type=password autocomplete=current-password></label></p>"
            f"<button type=submit>Log in</button></form>"
            f"<p class=muted>Your token was given to you by the maintainer; an <code>hf_</code> token from "
            f"<code>hf auth login</code> also works when the Space is configured for it.</p></div>")
    return page("Log in", body, None, None, app_title)


def audit_page(rows: List[dict], app_title: str, user: str, role: str) -> str:
    if not rows:
        return page("Audit", "<div class=card><p>No cases.</p></div>", user, role, app_title)
    cols = [c for c in rows[0].keys() if not c.startswith(("prereg", "git_sha", "tool"))]
    th = "".join(f"<th>{esc(c)}</th>" for c in cols)
    tr = "".join("<tr>" + "".join(f"<td>{esc(r.get(c, ''))}</td>" for c in cols) + "</tr>" for r in rows)
    body = (f"<div class=card><h1>Audit</h1><p><a href=/audit.csv>download audit.csv</a></p>"
            f"<div style='overflow:auto'><table><tr>{th}</tr>{tr}</table></div></div>")
    return page("Audit", body, user, role, app_title)
