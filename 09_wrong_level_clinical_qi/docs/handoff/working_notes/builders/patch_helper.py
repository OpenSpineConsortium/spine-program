"""Exact-string patch helper for the handoff fixes.

apply(path, [(old, new), ...]) replaces each old string, which must occur exactly once (or `n` times when a
triple (old, new, n) is given). Nothing is written unless every replacement matches. Line endings are kept.
"""
import io
import sys

H = "<spinesurg-ct-nnunet 097933a>/HANDOFF/"


def apply(path, pairs):
    if not path.startswith("C:"):
        path = H + path
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()
    crlf = "\r\n" in text
    if crlf:
        text = text.replace("\r\n", "\n")
    bad = []
    for item in pairs:
        old, new = item[0], item[1]
        n = item[2] if len(item) > 2 else 1
        c = text.count(old)
        if c != n:
            bad.append((c, n, old[:90]))
            continue
        text = text.replace(old, new)
    if bad:
        for c, n, o in bad:
            print("NO MATCH (found %d, want %d): %r" % (c, n, o))
        print("NOT WRITTEN:", path)
        sys.exit(1)
    if crlf:
        text = text.replace("\n", "\r\n")
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    print("patched %s (%d replacements)" % (path, len(pairs)))


def append(path, block):
    if not path.startswith("C:"):
        path = H + path
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()
    if not text.endswith("\n"):
        text += "\n"
    text += block
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    print("appended to", path)
