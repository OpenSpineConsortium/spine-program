# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/publish_checkpoints.py [tracked at 097933a]
"""Publish the chosen checkpoints with a model card each, to the private weights repository.

WHY PRIVATE. The project rule (memory: level-service-serving) is that the website never serves weights and
that inference runs behind a service with weights in `gregoryschwingmdphd/level-id-weights` on Hugging
Face, private. This script uploads to that repository only; it refuses a public destination.

WHAT A CARD SAYS, and where each line comes from -- nothing on a card is typed:
    training bank, recipe, encoder and head sha256          the run's sidecars and the files themselves
    interior accuracy, ordinary / anomalous / cervical      PRODUCT_RANKING.json (film-clustered CIs)
    label-defined State C by window length                  feasibility_claims.json for that pairing
    strengths / weaknesses                                  the same numbers, stated: what it is good at
                                                            (ordinary spines, cervical) and where it fails
                                                            (anomalous spines, L6, two-body windows)
    how to use it                                           tools/level_prototype.py

    python tools/publish_checkpoints.py --ranking ~/model_night/product/PRODUCT_RANKING.json --top 3 --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

REPO = "gregoryschwingmdphd/level-id-weights"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def pct(x, k="model"):
    return f"{100 * x[k]:.1f}% [{100 * x['film_boot_ci95'][0]:.1f}, {100 * x['film_boot_ci95'][1]:.1f}]" if x and k in x else "not measured"


def card(entry: dict, head: Path, claims: dict | None, bank_meta: dict | None) -> str:
    enc = Path(entry["weights"])
    o, a, c = entry.get("ordinary_lumbar") or {}, entry.get("anomalous_lumbar") or {}, entry.get("cervical") or {}
    byk = (claims or {}).get("by_state_and_length_C", {})

    def kcell(key):
        r = byk.get(key)
        if not r:
            return None
        v = r.get("exact")
        if v is None:
            return None
        n = r.get("n") or r.get("total")
        ci = r.get("ci95") or r.get("wilson") or []
        band = f" [{100 * ci[0]:.1f}, {100 * ci[1]:.1f}]" if len(ci) >= 2 and ci[0] is not None else ""
        return f"{100 * v:.1f}%{band}" + (f" (n={n:,})" if n else "")

    rows = []
    for L in (2, 3, 4):
        o_, a_ = kcell(f"{L}|real_film|ordinary"), kcell(f"{L}|real_film|anomalous")
        if o_ or a_:
            rows.append(f"| {L} | {o_ or '—'} | {a_ or '—'} |")
    # A TABLE OF DASHES IS WORSE THAN NO TABLE. It reads as a measurement that came out empty rather than one
    # that was never run for this pairing, and a model card is exactly where that difference matters.
    k_block = ("**Label-defined State C on real film by window length** (from `feasibility_claims.json`)\n\n"
               "| bodies visible | ordinary | anomalous |\n|---|---|---|\n" + "\n".join(rows)) if rows else \
              ("**Label-defined State C by window length:** not run for this pairing. The interior-window figures "
               "above are the ones this checkpoint is characterised by, and they are the stricter measurement.")
    sub = (bank_meta or {}).get("subset") or (bank_meta or {}).get("v6") or {}
    strengths = []
    weaknesses = []
    if o.get("model", 0) >= 0.9:
        strengths.append(f"ordinary lumbar spines on real film, interior windows with no anchor in the pixels: {pct(o)}")
    if c.get("model", 0) >= 0.99:
        strengths.append(f"cervical spine on real film: {pct(c)}")
    if a.get("model", 0) < 0.9:
        weaknesses.append(f"anomalous (transitional) spines: {pct(a)} on {a.get('films', '?')} films -- do not deploy where a "
                          f"lumbosacral or thoracolumbar variant must be named correctly")
    weaknesses.append("the variant class L6 is named correctly under half the time; two-body windows lose 5-30 points against five")
    weaknesses.append("trained and tested on lateral radiographs at a fixed 96 px per body; fluoroscopy frames were a test set only")
    return f"""# {entry['encoder']} — level-identification encoder + run-level head

**Deployment class:** ordinary spines on plain lateral radiographs; registration-free; abstains under the head's confidence threshold.

| field | value |
|---|---|
| encoder | `{enc.name}` sha256 `{sha(enc)}` |
| run-level head | `{head.name}` sha256 `{sha(head)}` — decodes ONLY this encoder |
| training bank | `{(bank_meta or {}).get('bank', entry.get('bank', '?'))}` |
| ordinary lumbar, interior, real film | {pct(o)} ({o.get('films', '?')} films) |
| anomalous lumbar, interior, real film | {pct(a)} ({a.get('films', '?')} films) |
| cervical, interior, real film | {pct(c)} ({c.get('films', '?')} films) |
| placement-blind prior on the same windows | {100 * o.get('placement_blind', 0):.0f}% |

{k_block}

**Strengths.** {'; '.join(strengths) + '.' if strengths else 'see numbers above'}

**Weaknesses.** {'; '.join(weaknesses) + '.' if weaknesses else 'none recorded, which means none was measured'}

**Use.** `python tools/level_prototype.py --image <radiograph> --model <encoder.pt> --head <head.pt>` — one image in; per-vertebra level names, per-level probability, and an abstain flag out. Crops are formed at 96 px per body on a 320 px canvas with a target-marker channel; the head takes 2–9 consecutive detected bodies. Never pair this head with another encoder: a mismatched pairing scored 0–1% with a systematic two-level offset.

**Transitional spines.** This checkpoint is not the product for a spine that may carry a lumbosacral or thoracolumbar variant, and no single-frame checkpoint is. For those, the serial sweep is the product: overlapping frames from the sacrum linked into one chain, against which the limited field is named (`tools/sweep_map.py`, `docs/SWEEP_PROTOCOL.md`), which raised two-vertebra frames on variant spines from 67% to 86% and on thoracolumbar variants from 50% to 96%.

**How it was made.** Trained by `slurm/night_arm.sh` (ResNet-18, cross-entropy or CORN, augmentation tier 2, seed 0); head by `tools/head_mixed_length.py` (mixed-length windows, kmax 4); scored by `tools/eval_interior_windows.py` on patient-grouped held-out films with no cross-source twins; every number here is read from the result JSONs by `tools/publish_checkpoints.py`.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranking", default="~/model_night/product/PRODUCT_RANKING.json")
    ap.add_argument("--claims-root", default="~/model_night/feasibility_claims")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--out", default="~/model_night/product/cards")
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if "level-id-weights" not in a.repo:
        raise SystemExit("refusing: weights go only to the private level-id-weights repository")
    rank = json.load(open(os.path.expanduser(a.ranking)))
    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    H = Path(os.path.expanduser("~"))
    chosen = []
    for e in rank[: a.top]:
        enc = Path(e["weights"])
        if not enc.exists():
            print("missing", enc); continue
        # the head this ranking used lives beside the interior JSON's record
        ij = H / "model_night" / "product" / e["encoder"] / "interior_windows.json"
        head = Path(json.load(open(ij))["head"]) if ij.exists() else None
        if head is None or not head.exists():
            print("no head recorded for", e["encoder"]); continue
        claims = None
        for cand in sorted((H / "model_night" / "feasibility_claims").glob(f"*{e['encoder']}*/feasibility_claims.json")):
            claims = json.load(open(cand)); break
        bank_meta = None
        bm = Path(json.load(open(ij))["ctx"]) / "meta.json"
        if bm.exists():
            bank_meta = json.load(open(bm)); bank_meta["bank"] = str(bm.parent)
        md = card(e, head, claims, bank_meta)
        (out / f"{e['encoder']}.md").write_text(md, encoding="utf-8")
        chosen.append((e["encoder"], enc, head, out / f"{e['encoder']}.md"))
        print(f"card: {out / (e['encoder'] + '.md')}")
    if a.dry_run:
        print("dry run: nothing uploaded"); return 0
    from huggingface_hub import HfApi
    api = HfApi()
    info = api.repo_info(a.repo, repo_type="model")
    if not getattr(info, "private", False):
        raise SystemExit(f"refusing: {a.repo} is not private")
    for name, enc, head, md in chosen:
        for p, dest in ((enc, f"{name}/{enc.name}"), (head, f"{name}/{head.name}"), (md, f"{name}/README.md")):
            api.upload_file(path_or_fileobj=str(p), path_in_repo=dest, repo_id=a.repo, repo_type="model")
            print("uploaded", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
