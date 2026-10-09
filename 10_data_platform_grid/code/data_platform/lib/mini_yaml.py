#!/usr/bin/env python3
"""A small YAML reader and writer for the subset this folder uses. Standard library only; Python 3.6+.

WHY. The grid login node and some job environments have no PyYAML, and the planning files (sources.yaml, the
per-source README.yaml files) must be readable everywhere. `dump` writes a strict subset that both PyYAML and
`load` read identically; `load` also accepts the hand-written forms a person types into a README.yaml.

Subset:
  - block mappings (`key: value`, nested by indentation of 2 or more spaces)
  - block sequences (`- value`, `- key: value` starting a mapping item)
  - scalars: double-quoted strings (JSON escapes), single-quoted strings ('' for a quote), plain strings,
    integers, floats, true/false, null/~, and the flow forms [] and {} (empty) or a one-line [a, b, "c"]
  - comments: a line whose first non-blank character is '#', or ' #' after a plain scalar
Not supported: anchors, aliases, tags, multi-document streams, block scalars (| and >), multi-line flow.

    from mini_yaml import load, dump
    data = load(open("sources.yaml", encoding="utf-8").read())
"""
import json
import re

__all__ = ["load", "dump", "loads", "dumps"]

_INT = re.compile(r"^[-+]?[0-9]+$")
_FLOAT = re.compile(r"^[-+]?([0-9]+\.[0-9]*|\.[0-9]+|[0-9]+)([eE][-+]?[0-9]+)?$")
_KEY = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_.\-/ ]*?|\"(?:[^\"\\]|\\.)*\"|'(?:[^']|'')*')\s*:(\s+|$)(.*)$")


class YamlError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ writing
def _scalar(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        r = repr(v)
        return r if ("." in r or "e" in r or "inf" in r or "nan" in r) else r + ".0"
    return json.dumps(str(v), ensure_ascii=False)


def _key(k):
    k = str(k)
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", k) and k.lower() not in ("true", "false", "null", "yes", "no", "on", "off", "y", "n"):
        return k
    return json.dumps(k, ensure_ascii=False)


def _dump(v, ind, out):
    sp = " " * ind
    if isinstance(v, dict):
        if not v:
            out.append(sp + "{}")
            return
        for k, x in v.items():
            if isinstance(x, (dict, list)) and x:
                out.append("%s%s:" % (sp, _key(k)))
                _dump(x, ind + 2, out)
            elif isinstance(x, dict):
                out.append("%s%s: {}" % (sp, _key(k)))
            elif isinstance(x, list):
                out.append("%s%s: []" % (sp, _key(k)))
            else:
                out.append("%s%s: %s" % (sp, _key(k), _scalar(x)))
    elif isinstance(v, list):
        if not v:
            out.append(sp + "[]")
            return
        for x in v:
            if isinstance(x, dict) and x:
                sub = []
                _dump(x, ind + 2, sub)
                sub[0] = sp + "- " + sub[0][ind + 2:]
                out.extend(sub)
            elif isinstance(x, list) and x:
                out.append(sp + "-")
                _dump(x, ind + 2, out)
            elif isinstance(x, dict):
                out.append(sp + "- {}")
            elif isinstance(x, list):
                out.append(sp + "- []")
            else:
                out.append(sp + "- " + _scalar(x))
    else:
        out.append(sp + _scalar(v))


def dumps(data, header=None):
    out = []
    if header:
        out.extend("# " + h if h else "#" for h in header.splitlines())
    _dump(data, 0, out)
    return "\n".join(out) + "\n"


def dump(data, fh=None, header=None):
    s = dumps(data, header)
    if fh is not None:
        fh.write(s)
    return s


# ------------------------------------------------------------------------------------------------ reading
def _strip_comment(s):
    """Remove a trailing ' #...' comment from a plain scalar line (quoted strings are handled by the caller)."""
    m = re.search(r"\s#", s)
    return s[:m.start()].rstrip() if m else s.rstrip()


def _parse_quoted(s):
    s = s.strip()
    if s.startswith('"'):
        # find the closing quote of a JSON string
        i, esc = 1, False
        while i < len(s):
            c = s[i]
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                break
            i += 1
        if i >= len(s):
            raise YamlError("unterminated double-quoted string: %r" % s)
        val = json.loads(s[:i + 1].replace("\\/", "/"))
        rest = s[i + 1:].strip()
        return val, rest
    if s.startswith("'"):
        i = 1
        buf = []
        while i < len(s):
            if s[i] == "'":
                if i + 1 < len(s) and s[i + 1] == "'":
                    buf.append("'")
                    i += 2
                    continue
                break
            buf.append(s[i])
            i += 1
        if i >= len(s):
            raise YamlError("unterminated single-quoted string: %r" % s)
        return "".join(buf), s[i + 1:].strip()
    raise YamlError("not a quoted string: %r" % s)


def _is_quoted_scalar(s):
    """True when s is one complete quoted string (with an optional comment), not a quoted mapping key."""
    if not s or s[0] not in "\"'":
        return False
    try:
        _, rest = _parse_quoted(s)
    except YamlError:
        return False
    return rest == "" or rest.startswith("#")


def _split_flow(body):
    items, buf, q, esc = [], [], None, False
    for c in body:
        if q:
            buf.append(c)
            if q == '"' and c == "\\" and not esc:
                esc = True
                continue
            if c == q and not esc:
                q = None
            esc = False
        elif c in "\"'":
            q = c
            buf.append(c)
        elif c == ",":
            items.append("".join(buf).strip())
            buf = []
        else:
            buf.append(c)
    if "".join(buf).strip():
        items.append("".join(buf).strip())
    return items


def _value(s):
    s = s.strip()
    if s == "" or s == "~" or s == "null" or s == "Null" or s == "NULL":
        return None
    if s[0] in "\"'":
        v, rest = _parse_quoted(s)
        if rest and not rest.startswith("#"):
            raise YamlError("text after a quoted scalar: %r" % s)
        return v
    s = _strip_comment(s)
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    if s in ("null", "~", ""):
        return None
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if s.startswith("[") and s.endswith("]"):
        return [_value(x) for x in _split_flow(s[1:-1])]
    if _INT.match(s):
        return int(s)
    if _FLOAT.match(s):
        return float(s)
    return s


def _lines(text):
    out = []
    for no, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[:len(raw) - len(raw.lstrip())]:
            raise YamlError("line %d: tab in indentation" % no)
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped in ("---", "..."):
            continue
        out.append((len(raw) - len(raw.lstrip(" ")), raw.strip(), no))
    return out


def _parse_block(lines, i, ind):
    """Parse the block whose items sit at indentation `ind`, starting at lines[i]."""
    if i >= len(lines):
        return None, i
    if lines[i][1].startswith("- ") or lines[i][1] == "-":
        return _parse_seq(lines, i, ind)
    return _parse_map(lines, i, ind)


def _parse_key(text, no):
    m = _KEY.match(text)
    if not m:
        raise YamlError("line %d: expected 'key: value', got %r" % (no, text))
    k = m.group(1)
    if k[0] in "\"'":
        k, _ = _parse_quoted(k)
    return k, m.group(3)


def _parse_map(lines, i, ind):
    out = {}
    while i < len(lines):
        li, text, no = lines[i]
        if li < ind:
            break
        if li > ind:
            raise YamlError("line %d: unexpected indentation" % no)
        if text.startswith("- "):
            break
        k, rest = _parse_key(text, no)
        i += 1
        if rest.strip() == "" or rest.strip().startswith("#"):
            if i < len(lines) and (lines[i][0] > ind or (lines[i][0] == ind and lines[i][1].startswith("- "))):
                child_ind = lines[i][0]
                v, i = _parse_block(lines, i, child_ind)
            else:
                v = None
        else:
            v = _value(rest)
        out[k] = v
    return out, i


def _parse_seq(lines, i, ind):
    out = []
    while i < len(lines):
        li, text, no = lines[i]
        if li < ind or not (text.startswith("- ") or text == "-"):
            break
        if li > ind:
            raise YamlError("line %d: unexpected indentation in a sequence" % no)
        rest = text[1:].strip()
        if rest == "" or rest.startswith("#"):
            i += 1
            if i < len(lines) and lines[i][0] > ind:
                v, i = _parse_block(lines, i, lines[i][0])
            else:
                v = None
            out.append(v)
            continue
        if _KEY.match(rest) and not rest.startswith(("[", "{")) and not _is_quoted_scalar(rest):
            # a mapping item: re-read it as a map whose first line sits at ind + 2
            item_ind = ind + 2
            lines[i] = (item_ind, rest, no)
            v, i = _parse_map(lines, i, item_ind)
            out.append(v)
            continue
        out.append(_value(rest))
        i += 1
    return out, i


def loads(text):
    lines = _lines(text)
    if not lines:
        return None
    v, i = _parse_block(lines, 0, lines[0][0])
    if i != len(lines):
        raise YamlError("line %d: could not parse past here" % lines[i][2])
    return v


def load(src):
    """Load from a string or an open file."""
    if hasattr(src, "read"):
        src = src.read()
    return loads(src)
