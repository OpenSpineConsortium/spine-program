# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/unseen_cases.py [tracked at 097933a]
"""tools/unseen_cases.py — the cases of one or more render banks that a checkpoint, through its whole initialisation
chain, never trained or was selected on: the eval gate's own keying (tools/eval_gate.key_items) against the gate's
own lineage store (chain_of), so what this writes is exactly what the gate will let through. One annotation stem per
line, for tools/sweep_map.py --cases. Grid only (the lineage store and the keying context live there).

    python tools/unseen_cases.py --ckpt ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt \\
        --drr ~/ts_drr ~/ctsp_drr ~/verse_drr --out ~/model_night/sweep_v3/cns/unseen_v9.txt
"""
import argparse
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_gate as EG  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--drr", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    store = EG.load_store()
    ck = EG.norm_path(os.path.expanduser(a.ckpt))
    k, e, nodes, how = EG.chain_of(ck, store)
    seen = set()
    for nk, ne in nodes:
        if ne is None:
            raise SystemExit(f"ancestor {nk} has no lineage row: what it saw is unknown")
        for side in ("train", "val"):
            seen |= EG._canon_set(ne.get(f"{side}_keys"))
    seen |= EG._canon_set(e.get("touched_keys"))
    print(f"{ck}: {len(seen):,} seen patient keys over {len(nodes)} lineage node(s); {how[:160]}", flush=True)
    print("  by corpus:", dict(Counter(x.split(':', 1)[0] for x in seen)), flush=True)
    kept = []
    for root in a.drr:
        items = EG.drr_items(root)
        n_seen = n_unk = 0
        for it in items:
            keys, _, unkeyed = EG.key_items([it])
            if unkeyed or not keys:
                n_unk += 1
                continue
            if keys & seen:
                n_seen += 1
                continue
            kept.append(it["case"])
        print(f"{root}: {len(items)} cases; {n_seen} seen, {n_unk} unkeyed, {len(items) - n_seen - n_unk} never seen", flush=True)
    Path(os.path.expanduser(a.out)).write_text("\n".join(kept) + "\n")
    print(f"wrote {len(kept)} never-seen cases to {a.out}")


if __name__ == "__main__":
    main()
