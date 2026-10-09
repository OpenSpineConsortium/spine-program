# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/sourcetext.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""What the SOURCE says about frame rate or playback speed (evidence (b) for the speed factor).

YouTube: <id>.info.json (title, description, chapters, tags) and <id>.description.
PMC: the article's JATS XML from Europe PMC (fetched once, cached under work/source_text/, sha256 recorded). The
caption of the <supplementary-material>/<media> element whose xlink:href names the video file is attached to that
file; rate statements elsewhere in the article are attached to every video of the article only when they state one
single acquisition rate.
Commons: the file page's ImageDescription (MediaWiki API extmetadata), fetched once and cached.

Patterns: an ACQUISITION RATE ("7.5 frames/s", "15 fps", "30 frames per second", "4 pulses/s", "7.5 f/s") and a
PLAYBACK SPEED ("2x speed", "played at 2x", "slow motion", "sped up", "real time", "time-lapse"). Only a numeric
statement can set a speed factor; words such as "real time" are recorded as text evidence only.
"""
from __future__ import annotations

import html
import json
import re
import urllib.request
from pathlib import Path

from .common import sha256_file

RATE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:-\s*)?(fps|f/s|frames?\s*(?:/|per)\s*s(?:ec(?:ond)?)?|images?\s*(?:/|per)\s*s(?:ec(?:ond)?)?|"
    r"pulses?\s*(?:/|per)\s*s(?:ec(?:ond)?)?|pps|p/s|frames?\s+per\s+second|Hz)\b", re.I)
SPEED_RE = re.compile(r"(?:(?:played|shown|displayed|sped up|accelerated|speed(?:ed)?)\s*(?:up\s*)?(?:at|to|by)?\s*"
                      r"(\d+(?:\.\d+)?)\s*(?:x|×)\b)|(?:\b(\d+(?:\.\d+)?)\s*(?:x|×)\s*(?:speed|faster|slower|"
                      r"real[- ]?time)\b)", re.I)
WORDS_RE = re.compile(r"\b(slow[- ]motion|sped[- ]up|accelerated|time[- ]lapse|real[- ]?time|fast[- ]forward)\b", re.I)


def sentences(text):
    text = re.sub(r"\s+", " ", text or "")
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def statements(text, where):
    out = []
    for s in sentences(text):
        for m in RATE_RE.finditer(s):
            v = float(m.group(1))
            if 0.5 <= v <= 120:
                out.append(dict(kind="rate", value=v, unit=m.group(2), text=s[:300], where=where))
        for m in SPEED_RE.finditer(s):
            v = float(m.group(1) or m.group(2))
            if 0.05 <= v <= 20:
                out.append(dict(kind="speed", value=v, text=s[:300], where=where))
        for m in WORDS_RE.finditer(s):
            out.append(dict(kind="words", value=m.group(1).lower(), text=s[:300], where=where))
    return out


def _fetch(url, dest, timeout=60):
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        return dest, "cache"
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "fluoro_video research pipeline"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    dest.write_bytes(data)
    return dest, "fetched"


def _xml_text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def pmc_statements(pmcid, cache_dir, allow_fetch=True):
    """{file name: [statements]} for supplementary videos, plus '*' for article-level statements."""
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    dest = Path(cache_dir) / f"{pmcid}.xml"
    info = dict(url=url, cache=str(dest.name))
    try:
        if not dest.exists() and not allow_fetch:
            raise FileNotFoundError("not cached and fetching disabled")
        p, how = _fetch(url, dest)
        info.update(status=how, sha256=sha256_file(p))
    except Exception as e:           # recorded, not guessed: no source text -> no (b) evidence
        info.update(status=f"unavailable: {type(e).__name__}: {e}"[:200])
        return {}, info
    x = dest.read_text(encoding="utf-8", errors="replace")
    per = {}
    for m in re.finditer(r"<(supplementary-material|media)\b([^>]*)>(.*?)</\1>", x, re.S):
        attrs, body = m.group(2), m.group(3)
        hrefs = re.findall(r'xlink:href="([^"]+)"', attrs + body)
        cap = _xml_text(body)
        for h in hrefs:
            per.setdefault(Path(h).name, []).extend(statements(cap, f"caption of {Path(h).name}"))
    body = _xml_text(re.sub(r"<(supplementary-material|media)\b.*?</\1>", " ", x, flags=re.S))
    per["*"] = statements(body, "article text")
    return per, info


def commons_statements(fname, cache_dir, allow_fetch=True):
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=extmetadata"
           f"&titles=File:{urllib.request.quote(fname)}")
    dest = Path(cache_dir) / (re.sub(r"[^A-Za-z0-9_.-]+", "_", fname) + ".json")
    info = dict(url=url, cache=dest.name)
    try:
        if not dest.exists() and not allow_fetch:
            raise FileNotFoundError("not cached and fetching disabled")
        p, how = _fetch(url, dest)
        info.update(status=how, sha256=sha256_file(p))
        d = json.loads(dest.read_text(encoding="utf-8"))
        pages = d.get("query", {}).get("pages", {})
        txt = []
        for pg in pages.values():
            for ii in pg.get("imageinfo", []):
                em = ii.get("extmetadata", {})
                for k in ("ImageDescription", "ObjectName"):
                    if k in em:
                        txt.append(_xml_text(str(em[k].get("value", ""))))
        return statements(" ".join(txt), "commons description"), info
    except Exception as e:
        info.update(status=f"unavailable: {type(e).__name__}: {e}"[:200])
        return [], info


def youtube_statements(folder, vid):
    out, info = [], dict(files=[])
    ij = Path(folder) / f"{vid}.info.json"
    if ij.exists():
        info["files"].append(dict(name=ij.name, sha256=sha256_file(ij)))
        d = json.loads(ij.read_text(encoding="utf-8", errors="replace"))
        for k in ("title", "description"):
            out += statements(str(d.get(k) or ""), f"info.json {k}")
        for c in d.get("chapters") or []:
            out += statements(str(c.get("title") or ""), "info.json chapter")
        info["container_fps_in_info_json"] = d.get("fps")
    de = Path(folder) / f"{vid}.description"
    if de.exists():
        info["files"].append(dict(name=de.name, sha256=sha256_file(de)))
        out += statements(de.read_text(encoding="utf-8", errors="replace"), ".description")
    # the same sentence can appear in info.json and .description: keep one
    seen, uniq = set(), []
    for s in out:
        k = (s["kind"], s["value"], s["text"])
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    return uniq, info


def for_video(entry, cache_dir, allow_fetch=True):
    """Statements that apply to one inventory entry, and where they came from."""
    src, path = entry["source"], Path(entry["path"])
    if src == "youtube":
        st, info = youtube_statements(path.parent, entry["source_id"])
        return st, info
    if src == "pmc":
        per, info = pmc_statements(entry["source_id"], cache_dir, allow_fetch)
        st = list(per.get(path.name, []))
        # the viewer transcode names differ from the original; match on the stem before '-pmcvs'
        art = per.get("*", [])
        rates = {s["value"] for s in art if s["kind"] == "rate"}
        info["article_rates"] = sorted(rates)
        if len(rates) == 1:
            st += art
        else:
            info["article_rates_not_attached"] = ("several distinct rates in the article text; not attributed to one "
                                                  "video" if rates else "none")
            st += [s for s in art if s["kind"] == "words"]
        return st, info
    if src == "commons":
        return commons_statements(path.name, cache_dir, allow_fetch)
    return [], {}
