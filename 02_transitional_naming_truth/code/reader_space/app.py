# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: reader_space/app.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Assisted vertebral level naming: does a surgeon do better with this system than without it?

WHY THIS EXISTS, AND WHY NO ACCURACY NUMBER REPLACES IT.
Every accuracy figure in this project is the machine judged alone against a reference standard. The
clinical comparator is not a machine: it is a surgeon with a CT-registration overlay, reported at 97.6 %
against 69.6 % unaided. Those are human-plus-machine numbers. A human plus an imperfect aid can land either
side of either alone -- a wrong suggestion that is overruled costs nothing, while a confident wrong one can
talk a reader out of a correct answer. Only a reader study measures which happens.

THE DESIGN.
Two blocks. Every reader names every film once UNAIDED, then names the same films again with the system's
answer shown. Unaided must come first: a reader who has seen the suggestion cannot un-see it. The second
block is block one ROTATED BY HALF, so every film is re-read at least N/2 films after its first
reading. The rotation is doing work: shuffle the second block independently instead and the film that falls
last in block one lands first in block two, re-read one film later, which is exactly the recall two blocks
exist to prevent.

THE CONFOUND, STATED RATHER THAN HIDDEN.
Because unaided always comes first, the assisted block also carries any learning or familiarity gained
during the first. This design cannot separate the aid's effect from that. A crossover -- half the readers
seeing film set A aided and set B unaided, half the reverse -- removes it, and needs twice the readers and
two matched film sets. Until then the assisted figure is an upper bound on the aid's contribution, and the
paper should say so.

WHAT IS RECORDED, AND WHY EACH.
  the answer          -- the measurement
  confidence          -- an aid that makes readers more confident without making them more right is a
                         hazard, and that is only visible if confidence is captured
  seconds on the film -- an aid that helps but doubles reading time may not be usable in theatre
  whether they changed their mind in block two, and in which direction

THE FOUR NUMBERS IT PRODUCES.
  unaided accuracy    -- this group's own baseline, not a published one
  assisted accuracy   -- the figure comparable to the 97.6 %
  RESCUE              -- wrong unaided, right aided: the benefit
  HARM                -- right unaided, wrong aided: the cost, which this class of aid rarely reports
McNemar's exact test on the discordant pairs is the right test for a paired binary outcome, and it uses
exactly those two cells.

No reader is ever shown the correct answer. The truth lives in the manifest and never reaches the page.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import math
import os
import random
import time
from pathlib import Path

import gradio as gr
from huggingface_hub import HfApi, hf_hub_download
from PIL import Image, ImageDraw, ImageFont

import viewport

DATA_REPO = os.environ.get("READER_DATA_REPO", "gregoryschwingmdphd/reader-study-films")
LEDGER_REPO = os.environ.get("READER_LEDGER_REPO", "gregoryschwingmdphd/reader-study-ledger")
NAMES = ([f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + ["T13"]
         + [f"L{i}" for i in range(1, 7)] + ["sacrum"])
CONF = ["certain", "fairly sure", "a guess"]

# who may read: "name:code,name:code". A code identifies a person; a typed name identifies nobody.
CODE_TO_NAME = {}
for _p in os.environ.get("READER_CODES", "").split(","):
    if ":" in _p:
        _n, _c = _p.split(":", 1)
        CODE_TO_NAME[_c.strip()] = _n.strip()


def _token():
    t = os.environ.get("HF_TOKEN")
    if t:
        return t
    for p in (Path.home() / ".cache" / "huggingface" / "token", Path.home() / ".huggingface" / "token"):
        try:
            if p.exists():
                return p.read_text().strip()
        except Exception:  # noqa: BLE001
            pass
    return None


TOKEN = _token()
if TOKEN is None:
    raise SystemExit(f"No HuggingFace token. Set HF_TOKEN for access to {DATA_REPO}.")
api = HfApi(token=TOKEN)
MANIFEST = json.load(open(hf_hub_download(DATA_REPO, "manifest.json", repo_type="dataset", token=TOKEN)))
ITEMS = MANIFEST["items"]
BY_ID = {i["id"]: i for i in ITEMS}
N = len(ITEMS)


# ------------------------------------------------------------------------------------- who is reading
def who(code: str) -> str:
    return CODE_TO_NAME.get((code or "").strip(), "")


# --------------------------------------------------------------------------------------- the sequence
def sequence_for(reader: str):
    """[(item_id, 'unaided'), ... all of them ..., (item_id, 'assisted'), ...]

    Block one is shuffled from a seed derived from the reader, so two readers meet the films in different
    orders and an order effect cannot masquerade as an effect of the aid.

    Block two is that same order ROTATED BY HALF, and the rotation is the point. Shuffling block two
    independently looks more random and is worse: the film that happens to fall last in block one and
    first in block two is then re-read one film later, which is precisely the recall the two-block design
    exists to prevent. Under the rotation every film is re-read at least N/2 films after its first
    reading, and no film is ever re-read soon after it was seen.
    """
    ids = [i["id"] for i in ITEMS]
    r1 = random.Random(int(hashlib.sha256((reader + "|1").encode()).hexdigest()[:8], 16))
    a = ids[:]
    r1.shuffle(a)
    half = max(1, len(a) // 2)
    b = a[half:] + a[:half]
    return [(x, "unaided") for x in a] + [(x, "assisted") for x in b]


def min_gap(reader: str) -> int:
    """The smallest number of films between the two readings of any one film, for this reader."""
    seq = sequence_for(reader)
    first = {}
    for pos, (iid, cond) in enumerate(seq):
        first.setdefault((iid, cond), pos)
    return min(first[(i, "assisted")] - first[(i, "unaided")] for i, _ in seq)


def _ledger():
    try:
        return api.list_repo_files(LEDGER_REPO, repo_type="dataset", token=TOKEN)
    except Exception:  # noqa: BLE001
        return []


def done_by(reader: str):
    pre = f"reads/{reader}/"
    out = set()
    for f in _ledger():
        if f.startswith(pre) and f.endswith(".json"):
            stem = Path(f).stem            # "<id>__<condition>"
            if "__" in stem:
                i, c = stem.rsplit("__", 1)
                out.add((i, c))
    return out


def next_for(reader: str):
    seq = sequence_for(reader)
    done = done_by(reader)
    for k, (iid, cond) in enumerate(seq):
        if (iid, cond) not in done:
            return k, iid, cond
    return None, None, None


# ------------------------------------------------------------------------------------------- drawing
def draw(iid: str, show_ai: bool):
    rec = BY_ID[iid]
    p = hf_hub_download(DATA_REPO, rec["image"], repo_type="dataset", token=TOKEN)
    im = Image.open(p).convert("RGB")
    dr = ImageDraw.Draw(im)
    size = max(15, im.size[1] // 24)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    for k, b in enumerate(rec["boxes"]):
        last = k == len(rec["boxes"]) - 1
        dr.rectangle(b, outline=(255, 60, 60) if last else (255, 196, 0), width=5 if last else 2)
    if show_ai:
        b = rec["boxes"][-1]
        lab = f"  system says: {rec['ai_answer']}  "
        w = int(size * 0.62 * len(lab))
        y = max(0, b[1] - size - 12)
        dr.rectangle([b[2] + 6, y, b[2] + 6 + w, y + size + 10], fill=(27, 91, 118))
        dr.text((b[2] + 12, y + 4), lab.strip(), fill=(255, 255, 255), font=font)
    return im


def show(iid: str, show_ai: bool, token: str):
    """(html, is_carm) for one film: the C-arm when the pack carries a strip, the old crop when it does not."""
    rec = BY_ID[iid]
    if rec.get("strip"):
        sp = Path(hf_hub_download(DATA_REPO, rec["strip"], repo_type="dataset", token=TOKEN))
        return viewport.viewport_html(rec, sp, show_ai, token), True
    im = draw(iid, show_ai)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f'<div id="carm-root" data-token="{token}" style="text-align:center">'
            f'<img src="data:image/png;base64,{b64}" style="max-width:100%;border-radius:10px"></div>'), False


GUIDE = """
## What you are being asked to do

You are looking at a **C-arm over a patient**. The patient is lying on the table, drawn in white; the
circle is the machine's field of view, and you can only see bone where the machine is pointing.

- **Drag the picture left and right**, or use the **left and right arrow keys**, to move the C-arm along the
  patient.
- **Zoom** with the buttons or the scroll wheel. The field is drawn true to size &mdash; a 9-inch
  intensifier covers about 140&nbsp;mm of a 1.8&nbsp;m adult &mdash; so you will want to zoom in to read.
- A yellow arrow at the edge of the field points the way back to the vertebra you are being asked about if
  you have moved off it.

**Name the vertebra in the red box.**

Moving the machine costs you an exposure, and the counter in the corner shows how many you have taken. Take
the ones you need and no more, exactly as you would in theatre; the count is recorded with your answer.

You will not find a landmark. The strip of film each C-arm can travel over was cut so that it stops short of
the sacrum, the skull and the first two cervical vertebrae, because a reader who reaches one of those will
count from it, and counting is not what this study is measuring.

You will see every film **twice**. The first time you will be on your own. The second time, later in the
series and in a different order, the same film will carry **a suggestion from an automatic system**. The
suggestion is sometimes wrong. You are not being asked to agree with it; you are being asked what you
think.

## Why it is arranged this way

The question is not whether the software is accurate on its own &mdash; that is measured elsewhere. It is
whether **a surgeon is more accurate with it than without it**, which is the only thing that matters in
theatre and the only claim worth making. That requires the same reader on the same film in both conditions.

You are never shown the correct answer, during or after. Please do not look anything up between the two
readings.

## Please also record

- **How sure you are.** An aid that makes people more confident without making them more right is a hazard,
  and it is invisible unless confidence is recorded.
- Take the time you would take in theatre. Reading time is recorded, because an aid that helps but doubles
  the time may not be usable.

## What happens to your answers

Each read is written to a private repository as it happens, so you can stop and resume at any point. Your
individual results are not reported separately in any publication.
"""


# --------------------------------------------------------------------------------------------- actions
def load_next(code, state):
    reader = who(code)
    if not reader:
        return None, "### Enter your reader code to begin.", "", gr.update(), gr.update(), state, ""
    k, iid, cond = next_for(reader)
    if iid is None:
        return (None, f"### Finished &mdash; all {N} films in both conditions. Thank you.",
                "", gr.update(), gr.update(), state, "")
    rec = BY_ID[iid]
    blk = "1 of 2 &mdash; on your own" if cond == "unaided" else "2 of 2 &mdash; with the system's suggestion"
    token = f"{iid}|{cond}|{time.time():.0f}"
    html, is_carm = show(iid, cond == "assisted", token)
    head = (f"### Film {k % N + 1} of {N} &nbsp;|&nbsp; block {blk}\n\n"
            + ("Move the C-arm along the patient and name the vertebra in the **red** box."
               if is_carm else
               f"Name the vertebra in the **red** box. {rec['n_vertebrae']} vertebrae are in view."))
    st = {"reader": reader, "id": iid, "cond": cond, "t0": time.time(), "carm": is_carm}
    return html, head, iid, gr.update(value="L4"), gr.update(value=CONF[1]), st, ""


def save(code, answer, confidence, telemetry, state):
    reader = who(code)
    if not reader or not state or state.get("reader") != reader:
        return None, "### Enter your reader code and press Begin.", "", gr.update(), gr.update(), state, ""
    iid, cond = state["id"], state["cond"]
    rec = BY_ID[iid]
    secs = round(time.time() - float(state.get("t0", time.time())), 1)
    try:
        tel = json.loads(telemetry) if telemetry else {}
    except Exception:  # noqa: BLE001
        tel = {}
    row = {"reader": reader, "film": iid, "condition": cond, "answer": answer,
           "confidence": confidence, "seconds": secs,
           "viewport": "carm" if state.get("carm") else "static",
           "exposures": tel.get("shots"), "panned_mm": tel.get("pan_mm"),
           "zoom": tel.get("zoom"), "first_move_ms": tel.get("first_move_ms"),
           "anterior_known": tel.get("anterior_known"),
           "n_vertebrae": rec["n_vertebrae"], "spine_class": rec.get("spine_class"),
           "ai_answer": rec["ai_answer"] if cond == "assisted" else None,
           "correct": bool(answer == rec["truth"]),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    api.upload_file(path_or_fileobj=io.BytesIO(json.dumps(row, indent=1).encode()),
                    path_in_repo=f"reads/{reader}/{iid}__{cond}.json", repo_id=LEDGER_REPO,
                    repo_type="dataset", token=TOKEN, commit_message=f"{reader} {iid} {cond}")
    img, head, fid, ans, conf, st, _ = load_next(code, state)
    return img, "Recorded.\n\n" + head, fid, ans, conf, st, ""


# ------------------------------------------------------------------------------------------- analysis
def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar on the discordant pairs. b = rescued, c = harmed."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def wilson(k, n):
    if n == 0:
        return (float("nan"), float("nan"))
    z = 1.959963985
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def results():
    files = [f for f in _ledger() if f.startswith("reads/") and f.endswith(".json")]
    if not files:
        return "### No reads yet."
    rows = []
    for f in files:
        try:
            rows.append(json.load(open(hf_hub_download(LEDGER_REPO, f, repo_type="dataset", token=TOKEN))))
        except Exception:  # noqa: BLE001
            pass
    if not rows:
        return "### No reads could be read back."
    paired = {}
    for r in rows:
        paired.setdefault((r["reader"], r["film"]), {})[r["condition"]] = r
    both = {k: v for k, v in paired.items() if "unaided" in v and "assisted" in v}

    un = [r for r in rows if r["condition"] == "unaided"]
    asd = [r for r in rows if r["condition"] == "assisted"]
    lines = [f"## {len(rows)} reads from {len({r['reader'] for r in rows})} readers",
             f"{len(both)} films have been read in **both** conditions; those are what the comparison uses.",
             "", "| | n | correct | 95% CI |", "|---|---|---|---|"]
    for lab, rs in (("Unaided", un), ("With the system", asd)):
        k = sum(r["correct"] for r in rs)
        lo, hi = wilson(k, len(rs))
        lines.append(f"| {lab} | {len(rs)} | {100*k/max(len(rs),1):.1f}% | {100*lo:.1f}&ndash;{100*hi:.1f}% |")

    if both:
        rescue = sum(1 for v in both.values() if not v["unaided"]["correct"] and v["assisted"]["correct"])
        harm = sum(1 for v in both.values() if v["unaided"]["correct"] and not v["assisted"]["correct"])
        same = len(both) - rescue - harm
        p = mcnemar_exact(rescue, harm)
        lines += ["", "### Paired outcome, the part that decides it", "",
                  "| | n |", "|---|---|",
                  f"| **Rescued** &mdash; wrong alone, right with the system | **{rescue}** |",
                  f"| **Harmed** &mdash; right alone, wrong with the system | **{harm}** |",
                  f"| Unchanged | {same} |",
                  "", f"McNemar exact two-sided **p = {p:.4f}** on the {rescue + harm} discordant pairs.",
                  "", "_Rescue minus harm is the aid's net effect. Harm is the number this class of aid "
                      "usually does not report; it is reported first here on purpose._"]
        # did the aid change confidence without changing correctness?
        conf_rank = {c: i for i, c in enumerate(CONF)}
        moved = [(conf_rank.get(v["unaided"]["confidence"], 1) - conf_rank.get(v["assisted"]["confidence"], 1))
                 for v in both.values()]
        more_sure = sum(1 for m in moved if m > 0)
        wrong_and_surer = sum(1 for v in both.values()
                              if not v["assisted"]["correct"]
                              and conf_rank.get(v["unaided"]["confidence"], 1) >
                              conf_rank.get(v["assisted"]["confidence"], 1))
        lines += ["", f"Readers were more confident with the system on {more_sure} of {len(both)} films; "
                      f"on **{wrong_and_surer}** of those they were more confident *and still wrong*, which "
                      f"is the hazard worth watching."]
        tu = sum(v["unaided"].get("seconds", 0) for v in both.values()) / max(len(both), 1)
        ta = sum(v["assisted"].get("seconds", 0) for v in both.values()) / max(len(both), 1)
        lines.append(f"Median-ish reading time: {tu:.1f} s unaided against {ta:.1f} s with the system.")

    lines += ["", "---", "", "_Unaided always precedes assisted, so the assisted figure also carries any "
                          "learning from the first block. It is an upper bound on the aid's contribution. "
                          "A crossover with two matched film sets would separate them._"]
    return "\n".join(lines)


with gr.Blocks(title="Assisted level naming", theme=gr.themes.Soft(),
               head=viewport.CARM_JS) as demo:
    gr.Markdown("# Assisted vertebral level naming\n"
                "A reader study: the same films, named once on your own and once with an automatic "
                "suggestion.")
    with gr.Tabs():
        with gr.Tab("Read"):
            with gr.Row():
                with gr.Column(scale=5):
                    img = gr.HTML()
                    carm_out = gr.Textbox(visible=False, elem_id="carm_out")
                with gr.Column(scale=3):
                    code = gr.Textbox(label="Your reader code", type="password")
                    begin = gr.Button("Begin / next film", variant="primary")
                    head = gr.Markdown()
                    fid = gr.Textbox(label="Film", interactive=False)
                    answer = gr.Dropdown(NAMES, label="The vertebra in the red box is", value="L4")
                    confidence = gr.Radio(CONF, label="How sure are you?", value=CONF[1])
                    submit = gr.Button("Record and go on", variant="primary")
                    state = gr.State({})
                    spare = gr.Textbox(visible=False)
        with gr.Tab("Instructions"):
            gr.Markdown(GUIDE)
        with gr.Tab("Results"):
            res = gr.Markdown()
            gr.Button("Refresh").click(results, None, res)

    begin.click(load_next, [code, state], [img, head, fid, answer, confidence, state, spare])
    submit.click(save, [code, answer, confidence, carm_out, state],
                 [img, head, fid, answer, confidence, state, spare])

if __name__ == "__main__":
    demo.launch(server_name=os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0"),
                server_port=int(os.environ.get("PORT", "7860")),
                show_api=False)
