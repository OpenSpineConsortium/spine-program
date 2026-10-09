#!/usr/bin/env python3
"""Compare a source tree with its copy after an rsync: every path, size, symlink target and hard-link group, plus
the SHA-256 of a stratified sample of files. Standard library only; Python 3.6+. Read-only on both sides.

    python3 verify_transfer.py --src ~/deepfluoro --dst /rs/rs_grp_oschome/go2432/data/deepfluoro_h5/raw/deepfluoro \
        --sample 200 --out verify_B00_deepfluoro.json
    python3 verify_transfer.py --links-only --src ~/allspine_v9_fov96_ctx     # preflight: links that leave the item

Exit 0 when the copy is complete and every sampled file hashes equal; 1 otherwise. The JSON names every difference
(capped at 50 per kind) so a failed batch says what is wrong, not only that something is.

Besides names, sizes and the sample, two things fail a copy that is complete byte for byte but broken in use:
  * a symlink that resolved at the source and does not resolve at the copy (typically a relative link that leaves
    the item, such as ../verse_drr/x inside a bank: after the move it points at a sibling path that is not there);
    links that dangled already at the source (Dataset813's container paths) are reported, not failed;
  * a file whose hard-link count differs between source and copy: a partner inode outside the copied set was not
    copied with it (two items that share inodes copied in separate rsync calls end up as two copies). Use
    --allow-nlink-loss after reviewing nlink_differs when the partner is meant to stay behind.

Why a sample and not every byte: a full checksum pass reads both copies in full (Panasas and CephFS), which costs
hours per TB; size + name + link structure catches a truncated or missing file, and the sample catches silent
corruption at a known rate. A full pass is still available: `--sample 0 --all` hashes every file.
"""
import argparse
import hashlib
import json
import os
import random
import sys
import time


def walk(root):
    """{relpath: (kind, size, link_target, inode_key, nlink)} for every entry below root (root itself excluded)."""
    out = {}
    root = root.rstrip("/")
    if os.path.isfile(root) and not os.path.islink(root):
        st = os.lstat(root)
        out["."] = ("f", st.st_size, None, (st.st_dev, st.st_ino) if st.st_nlink > 1 else None, st.st_nlink)
        return out
    for dp, dn, fn in os.walk(root, followlinks=False):
        rel_dp = os.path.relpath(dp, root)
        for d in list(dn):
            p = os.path.join(dp, d)
            rel = os.path.normpath(os.path.join(rel_dp, d))
            if os.path.islink(p):
                out[rel] = ("l", 0, os.readlink(p), None, 1)
                dn.remove(d)
            else:
                out[rel] = ("d", 0, None, None, 1)
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.normpath(os.path.join(rel_dp, f))
            try:
                st = os.lstat(p)
            except OSError:
                out[rel] = ("?", -1, None, None, 0)
                continue
            if os.path.islink(p):
                out[rel] = ("l", 0, os.readlink(p), None, 1)
            else:
                out[rel] = ("f", st.st_size, None, (st.st_dev, st.st_ino) if st.st_nlink > 1 else None, st.st_nlink)
    return out


def sha256(path, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def stratified_sample(files, n, seed=20261008):
    """Pick about n files spread over the top-level subfolders and over size bins (every bin and folder gets one)."""
    if n <= 0 or not files:
        return []
    rnd = random.Random(seed)
    strata = {}
    for rel, size in files:
        top = rel.split(os.sep, 1)[0] if os.sep in rel else "."
        b = 0 if size <= 0 else min(12, int(size).bit_length() // 3)
        strata.setdefault((top, b), []).append(rel)
    keys = sorted(strata)
    pick = []
    for k in keys:
        pick.append(rnd.choice(strata[k]))
    rest = [rel for rel, _ in files if rel not in set(pick)]
    rnd.shuffle(rest)
    pick.extend(rest[:max(0, n - len(pick))])
    return sorted(set(pick))


def link_report(root, tree):
    """Per symlink: absolute or relative, whether it resolves, and whether a relative one leaves the item."""
    root = os.path.abspath(root.rstrip("/"))
    rep = dict(absolute=[], relative_outside=[], dangling=[], resolves={})
    for rel, v in tree.items():
        if v[0] != "l":
            continue
        p = os.path.join(root, rel)
        tgt = v[2]
        ok = os.path.exists(p)
        rep["resolves"][rel] = ok
        if not ok:
            rep["dangling"].append(rel)
        if tgt.startswith("/"):
            rep["absolute"].append(rel)
        else:
            res = os.path.normpath(os.path.join(os.path.dirname(p), tgt))
            if not (res == root or res.startswith(root + os.sep)):
                rep["relative_outside"].append(rel)
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst")
    ap.add_argument("--sample", type=int, default=200, help="files to hash on both sides (0 = none)")
    ap.add_argument("--all", action="store_true", help="hash every file (slow)")
    ap.add_argument("--allow-nlink-loss", action="store_true", help="do not fail on hard-link counts that differ")
    ap.add_argument("--links-only", action="store_true", help="only report the symlinks of --src (preflight)")
    ap.add_argument("--out")
    a = ap.parse_args()
    t0 = time.time()
    if a.links_only:
        lr = link_report(a.src, walk(a.src))
        print("links absolute %d relative_outside %d dangling %d" % (len(lr["absolute"]), len(lr["relative_outside"]), len(lr["dangling"])))
        if a.out:
            json.dump(dict(src=a.src, absolute=lr["absolute"][:200], relative_outside=lr["relative_outside"][:200],
                           dangling=lr["dangling"][:200]), open(a.out, "w"), indent=1)
        return 0
    if not (a.dst and a.out):
        ap.error("--dst and --out are required unless --links-only")
    src, dst = walk(a.src), walk(a.dst)
    res = dict(src=a.src, dst=a.dst, started=time.strftime("%Y-%m-%dT%H:%M:%S"))
    only_src = sorted(set(src) - set(dst))
    only_dst = sorted(set(dst) - set(src))
    size_diff, kind_diff, link_diff, nlink_diff = [], [], [], []
    for rel in sorted(set(src) & set(dst)):
        s, d = src[rel], dst[rel]
        if s[0] != d[0]:
            kind_diff.append(rel)
        elif s[0] == "f" and s[1] != d[1]:
            size_diff.append(rel)
        elif s[0] == "l" and s[2] != d[2]:
            link_diff.append(rel)
        if s[0] == "f" and d[0] == "f" and s[4] != d[4]:
            nlink_diff.append("%s (src %d, dst %d)" % (rel, s[4], d[4]))

    # hard-link groups: files sharing an inode in src must share one in dst, and vice versa
    def groups(t):
        g = {}
        for rel, v in t.items():
            if v[0] == "f" and v[3] is not None:
                g.setdefault(v[3], []).append(rel)
        return sorted(tuple(sorted(x)) for x in g.values() if len(x) > 1)
    hl_src, hl_dst = groups(src), groups(dst)
    # symlinks: one that resolved at the source must resolve at the copy
    lsrc, ldst = link_report(a.src, src), link_report(a.dst, dst)
    broken = sorted(rel for rel, ok in lsrc["resolves"].items() if ok and not ldst["resolves"].get(rel, False))
    files = [(rel, v[1]) for rel, v in src.items() if v[0] == "f"]
    sample = [rel for rel, _ in files] if a.all else stratified_sample(files, a.sample)
    hash_diff = []
    for rel in sample:
        if rel in only_src or rel in size_diff or rel in kind_diff:
            continue
        sp = a.src if rel == "." else os.path.join(a.src, rel)
        dp = a.dst if rel == "." else os.path.join(a.dst, rel)
        if sha256(sp) != sha256(dp):
            hash_diff.append(rel)
    count = lambda t, k: sum(1 for v in t.values() if v[0] == k)
    res.update(
        src_counts=dict(files=count(src, "f"), dirs=count(src, "d"), links=count(src, "l"), bytes=sum(v[1] for v in src.values() if v[0] == "f")),
        dst_counts=dict(files=count(dst, "f"), dirs=count(dst, "d"), links=count(dst, "l"), bytes=sum(v[1] for v in dst.values() if v[0] == "f")),
        only_in_src=only_src[:50], n_only_in_src=len(only_src),
        only_in_dst=only_dst[:50], n_only_in_dst=len(only_dst),
        size_differs=size_diff[:50], n_size_differs=len(size_diff),
        kind_differs=kind_diff[:50], n_kind_differs=len(kind_diff),
        link_target_differs=link_diff[:50], n_link_target_differs=len(link_diff),
        hardlink_groups_src=len(hl_src), hardlink_groups_dst=len(hl_dst), hardlink_groups_equal=hl_src == hl_dst,
        nlink_differs=nlink_diff[:50], n_nlink_differs=len(nlink_diff), nlink_loss_allowed=a.allow_nlink_loss,
        links_broken_by_move=broken[:50], n_links_broken_by_move=len(broken),
        relative_links_leaving_item=lsrc["relative_outside"][:50], n_relative_links_leaving_item=len(lsrc["relative_outside"]),
        dangling_at_source=lsrc["dangling"][:50], n_dangling_at_source=len(lsrc["dangling"]),
        absolute_symlinks_in_src=lsrc["absolute"][:50], n_absolute_symlinks_in_src=len(lsrc["absolute"]),
        sampled=len(sample), hashed_all=a.all, hash_differs=hash_diff[:50], n_hash_differs=len(hash_diff),
        seconds=round(time.time() - t0, 1))
    res["ok"] = (not only_src and not size_diff and not kind_diff and not link_diff and not hash_diff and res["hardlink_groups_equal"]
                 and not broken and (a.allow_nlink_loss or not nlink_diff))
    notes = []
    if lsrc["absolute"]:
        notes.append("absolute symlinks were copied as they are; each resolves after the move only through the old path")
    if nlink_diff and a.allow_nlink_loss:
        notes.append("hard-link counts differ (allowed): partner inodes outside this copy were not carried")
    if lsrc["dangling"]:
        notes.append("links that dangled at the source dangle at the copy too (not a failure)")
    res["note"] = "; ".join(notes)
    json.dump(res, open(a.out, "w"), indent=1)
    print(("VERIFY_OK" if res["ok"] else "VERIFY_FAILED"), a.src, "->", a.dst,
          "files %d/%d bytes %d/%d sampled %d%s%s" % (res["src_counts"]["files"], res["dst_counts"]["files"],
                                                      res["src_counts"]["bytes"], res["dst_counts"]["bytes"], len(sample),
                                                      " links_broken %d" % len(broken) if broken else "",
                                                      " nlink_differs %d" % len(nlink_diff) if nlink_diff else ""))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
