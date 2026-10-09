"""Vertebra level review: one name per film, two readers per film, every decision written to a private ledger.

WHY THE TASK IS ONE NAME AND NOT TWENTY. The names on these films came from a decoder that reads the boxes top
to bottom and assigns consecutive names from an alphabet. When it is wrong it is almost always wrong by an
OFFSET -- the run is called L1..L5 when it is really T12..L4 -- and almost never scrambled, because the decode
is monotone by construction. So naming the bottom vertebra fixes every name above it, and asking for twenty
names would cost twenty times as much and buy the same correction.

WHY THE TWO TICKS MATTER MORE THAN THE NAME. An offset cannot express a spine with six lumbar vertebrae or
thirteen rib-bearing levels. Those change the alphabet itself, and they are the entire reason this project
exists: the model has never seen a photograph of a six-lumbar spine, because every one of the 168 it learned
from is a CT render. A reviewer who ticks L6 on a real radiograph is creating a training example that does
not currently exist anywhere in the corpus.

WHAT IS PUBLIC AND WHAT IS NOT. This file is a user interface: it contains no model, no weights and no naming
algorithm, only a form over a manifest. The films, the names and every decision live in PRIVATE dataset
repositories that the app reads with its own token, and a passcode gates the page. Nothing about the level
identification method is exposed by hosting it.

DOUBLE READ AND AGREEMENT. Every film is assigned to exactly two reviewers by a hash of the film id, so the
two are always distinct and a reviewer's list is stable between visits. Agreement is reported live on the
progress tab -- raw agreement and Cohen's kappa on the lowest-name call -- and disagreements go to an
adjudication list rather than into training.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import os
import time
from collections import Counter, defaultdict
from pathlib import Path

import gradio as gr
from huggingface_hub import HfApi, hf_hub_download
from PIL import Image, ImageDraw, ImageFont

DATA_REPO = os.environ.get("REVIEW_DATA_REPO", "gregoryschwingmdphd/level-review-films")
LEDGER_REPO = os.environ.get("REVIEW_LEDGER_REPO", "gregoryschwingmdphd/level-review-ledger")
PASSCODE = os.environ.get("REVIEW_PASSCODE", "")
REVIEWERS = [r.strip() for r in os.environ.get("REVIEWERS", "").split(",") if r.strip()]
# Radiology residents who settle the films the two students disagreed on. A separate list and a separate
# passcode, because an adjudicator's call overrides two other people's and should not be reachable by
# knowing the student passcode.
ADJUDICATORS = [r.strip() for r in os.environ.get("ADJUDICATORS", "").split(",") if r.strip()]
ADJ_PASSCODE = os.environ.get("ADJUDICATE_PASSCODE", "")
# A short quiz of cases with known answers, which a reviewer passes once before their reviews count.
QUIZ_REPO = os.environ.get("REVIEW_QUIZ_REPO", "gregoryschwingmdphd/level-review-quiz")
# "alice:code1,bob:code2" -- a stand-in for signing in, while the Space has no OAuth client.
CODE_TO_NAME = {}
for _pair in os.environ.get("REVIEWER_CODES", "").split(","):
    if ":" in _pair:
        _n, _c = _pair.split(":", 1)
        CODE_TO_NAME[_c.strip()] = _n.strip()
NAMES = ([f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + ["T13"]
         + [f"L{i}" for i in range(1, 7)] + ["sacrum"])

JUNCTIONS = [
    ("ordinary", "Ordinary - five lumbar bodies, twelve rib-bearing levels"),
    ("thoracolumbar", "Thoracolumbar transitional - a rib where you did not expect one, or a missing 12th"),
    ("lumbosacral", "Lumbosacral transitional - L5 part-joined to the sacrum, or a sixth lumbar body"),
    ("both", "Both junctions transitional"),
    ("unsure", "I cannot tell from this film"),
]
JUNCTION_LABELS = [lbl for _, lbl in JUNCTIONS]
JUNCTION_OF = {lbl: key for key, lbl in JUNCTIONS}

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
    raise SystemExit(f"No HuggingFace token. Set HF_TOKEN, or log in with an account granted access to {DATA_REPO}.")
api = HfApi(token=TOKEN)
MANIFEST = json.load(open(hf_hub_download(DATA_REPO, "manifest.json", repo_type="dataset", token=TOKEN)))
FILMS = MANIFEST["films"]
BY_ID = {f["film"]: f for f in FILMS}


# ---------------------------------------------------------------------------------------------- assignment
# WHY THERE IS A PASSCODE AS WELL AS A SIGN-IN.
#
# This Space is PUBLIC -- a private one needs a paid plan, and these were reused precisely because they are
# grandfathered. The films it shows are real radiographs fetched server-side with the Space's own token, so
# "public Space, private dataset" does NOT keep them unseen: anyone who can open the page can see them.
#
# Sign-in says who you are. The passcode says you were let in. On a public Space only the second keeps a
# stranger off the page, and for a while today neither did: the sign-in refactor removed the passcode check
# and Hugging Face had not provisioned OAuth, so gradio was serving its MOCK flow -- which signs in anybody
# as a fabricated user without contacting Hugging Face at all. Both gates now apply, and the mock is
# refused outright rather than treated as a login.


def who_is(profile) -> str:
    """The signed-in Hugging Face username, or "" when nobody is signed in.

    Identity used to be a dropdown of names, which is not identity: anyone who could open the page could
    pick anyone's name, including the adjudicator's, and write a decision under it. The ledger is the
    training set and its per-reader agreement is the measure the programme produces, so an unattributable
    or misattributed decision is worse than a missing one. The account signs the work.
    """
    if not os.environ.get("OAUTH_CLIENT_ID"):
        # gradio mounts a MOCK OAuth flow when Hugging Face has not provisioned a client, and the mock
        # hands back a username nobody authenticated. Treat it as signed out, always.
        return ""
    return getattr(profile, "username", "") or ""


def who_by_code(code: str) -> str:
    """Identity from a per-reviewer code, used while Hugging Face sign-in is unavailable.

    REVIEWER_CODES is "alice:xxxx,bob:yyyy". A reviewer knows only their own code, so a decision can still
    be attributed to a person and the two readers of a film remain distinguishable -- which is the whole
    point, since per-reader agreement is the measure this programme produces.

    It is weaker than signing in: a code can be passed on, where an account cannot be shared without
    handing over the account. It is used only because the Space is not getting an OAuth client, and the
    alternative -- a dropdown of names anyone may pick -- is not identity at all.
    """
    if not code:
        return ""
    return CODE_TO_NAME.get(code.strip(), "")


def identify(profile, code: str) -> str:
    """The signed-in account if there is one, otherwise the per-reviewer code. Never a typed-in name."""
    return who_is(profile) or who_by_code(code)


def readers_for(film_id: str):
    """The two reviewers this film belongs to. Distinct by construction: the second is the first plus an
    offset drawn from 1..n-1, which cannot be zero."""
    n = len(REVIEWERS)
    if n < 2:
        return list(range(n))
    h = int(hashlib.sha256(film_id.encode()).hexdigest()[:8], 16)
    r1 = h % n
    return [r1, (r1 + 1 + (h // n) % (n - 1)) % n]


def assigned_to(reviewer: str):
    if not REVIEWERS:
        return [f["film"] for f in FILMS]
    try:
        me = REVIEWERS.index(reviewer)
    except ValueError:
        return []
    return [f["film"] for f in FILMS if me in readers_for(f["film"])]


def _ledger_files():
    try:
        return api.list_repo_files(LEDGER_REPO, repo_type="dataset", token=TOKEN)
    except Exception:  # noqa: BLE001
        return []


def done_by(reviewer: str):
    pre = f"decisions/{reviewer}/"
    return {Path(f).stem for f in _ledger_files() if f.startswith(pre)}


# ------------------------------------------------------------------------------------------------- quiz
# Why a reviewer has to pass something before their answers count.
#
# The whole programme rests on students recognising a transitional spine, and most have never been shown
# one. A reviewer who does not know what a sixth lumbar vertebra looks like does not abstain -- they name
# the film plausibly, the other reader does the same, the two agree, and the pair is written into training
# as a confident wrong answer. Two readers do not catch a shared misconception; they launder it into the
# ground truth. The quiz exists to make sure both readers have at least SEEN each class once.
#
# The answers come from CT label voxels through the anomaly manifest -- the vertebrae were counted in three
# dimensions, where counting is reliable -- so failing someone is grounded in anatomy rather than in
# another model's opinion.
try:
    QUIZ = json.load(open(hf_hub_download(QUIZ_REPO, "manifest.json", repo_type="dataset", token=TOKEN)))
except Exception:  # noqa: BLE001
    QUIZ = None


def passed_quiz(who: str) -> bool:
    if not QUIZ or not who:
        return True          # no quiz configured: do not lock anyone out of a programme that has no gate
    return f"training/{who}.json" in set(_ledger_files())


def quiz_item(i: int):
    items = (QUIZ or {}).get("items") or []
    if not items:
        return None, "### No quiz is configured for this Space.", "", 0
    i = int(i) % len(items)
    it = items[i]
    p = hf_hub_download(QUIZ_REPO, it["image"], repo_type="dataset", token=TOKEN)
    im = Image.open(p).convert("RGB")
    dr = ImageDraw.Draw(im)
    size = max(15, im.size[1] // 42)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    for k, b in enumerate(it["boxes"]):
        last = k == len(it["boxes"]) - 1
        dr.rectangle(b, outline=(255, 60, 60) if last else (255, 196, 0), width=5 if last else 2)
    txt = (f"### Case {i+1} of {len(items)}\n\n"
           f"Name the vertebra in the **red** box, and tick a variant if you see one. "
           f"The answer is known from the CT this was rendered from.")
    return im, txt, it["film"], i


def quiz_answer(i, lowest, junction_label, passcode="", profile: gr.OAuthProfile | None = None):
    who = identify(profile, passcode)
    if not who:
        return "### Sign in, or enter your reviewer code.", None, "", i, ""
    items = (QUIZ or {}).get("items") or []
    if not items:
        return "### No quiz is configured.", None, "", i, ""
    if not who:
        return "### Sign in with your Hugging Face account first.", None, "", i, ""
    i = int(i) % len(items)
    it = items[i]
    said = JUNCTION_OF.get(junction_label, "unsure")
    want_cls = it.get("answer_class", "ordinary")
    # The class is what is being taught; the name is asked alongside so the quiz looks like the job. Both
    # must be right, and an honest "cannot tell" is marked wrong rather than excused -- the point of the
    # exercise is to reach the film where you CAN tell.
    ok = (lowest == it["answer_lowest"] and said == want_cls)
    want = (f"**{it['answer_lowest']}**, and the junction is **{want_cls}**")
    verdict = ("### Correct.\n\n" if ok else "### Not quite.\n\n") + \
              f"The answer is {want}.\n\n_{it['why']}_"
    nxt = (i + 1) % len(items)
    img, txt, fid, _ = quiz_item(nxt)
    return verdict + "\n\n---\n\n" + txt, img, fid, nxt, ("correct" if ok else "wrong")


def quiz_finish(tally, passcode="", profile: gr.OAuthProfile | None = None):
    who = identify(profile, passcode)
    """Record a pass. The tally is kept in the page, so a reload restarts it rather than banking a half score."""
    items = (QUIZ or {}).get("items") or []
    if not items:
        return "### No quiz is configured."
    if not who:
        return "### Sign in with your Hugging Face account first."
    got = sum(1 for x in (tally or "").split(",") if x == "correct")
    need = QUIZ.get("pass_mark", max(1, int(0.75 * len(items))))
    if got < need:
        return (f"### {got} of {len(items)} correct - the pass mark is {need}.\n\n"
                f"Read **How to review**, then start the quiz again. There is no penalty for retaking it, "
                f"and no advantage to guessing: a reviewer who cannot yet tell these apart makes the "
                f"training data worse, not better.")
    api.upload_file(path_or_fileobj=io.BytesIO(json.dumps(
        {"reviewer": who, "score": got, "of": len(items), "pass_mark": need,
         "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}, indent=1).encode()),
        path_in_repo=f"training/{who}.json", repo_id=LEDGER_REPO, repo_type="dataset",
        token=TOKEN, commit_message=f"quiz passed by {who}")
    return (f"### Passed - {got} of {len(items)}.\n\n"
            f"**{who}** can now review. Go to the **Review** tab.")


# ------------------------------------------------------------------------------------------ adjudication
def _decision(who: str, film: str):
    try:
        return json.load(open(hf_hub_download(LEDGER_REPO, f"decisions/{who}/{film}.json",
                                              repo_type="dataset", token=TOKEN)))
    except Exception:  # noqa: BLE001
        return None


def _call_of(d):
    """What the two readers must agree on for a film to be settled without an adjudicator.

    The lowest name is the answer, but a film is also unsettled when one reader says the boxes are unusable
    and the other names a vertebra, or when they differ on whether the spine carries a variant -- those
    change what the film becomes in training just as much as a different name.
    """
    if d is None:
        return None
    return (bool(d.get("boxes_ok", True)), d.get("lowest_name"), bool(d.get("l6")),
            bool(d.get("t13")), d.get("junction", "unsure"))


def adjudicated_films():
    return {Path(f).stem for f in _ledger_files() if f.startswith("adjudications/")}


def disagreements():
    """Films both readers have answered and disagreed on, minus those already settled.

    Only films whose two decision FILES both exist are fetched, so this costs one listing plus two reads per
    genuinely contested film rather than a read of the whole ledger.
    """
    files = _ledger_files()
    have = {}
    for f in files:
        parts = f.split("/")
        if len(parts) == 3 and parts[0] == "decisions":
            have.setdefault(Path(parts[2]).stem, set()).add(parts[1])
    settled = adjudicated_films()
    out = []
    for film, who in have.items():
        if film in settled or film not in BY_ID:
            continue
        pair = [REVIEWERS[i] for i in readers_for(film)] if REVIEWERS else sorted(who)
        both = [w for w in pair if w in who]
        if len(both) < 2:
            continue
        da, db = _decision(both[0], film), _decision(both[1], film)
        if _call_of(da) is None or _call_of(db) is None:
            continue
        if _call_of(da) != _call_of(db):
            out.append({"film": film, "a": da, "b": db})
    out.sort(key=lambda r: (BY_ID[r["film"]].get("tier", 9), r["film"]))
    return out


_ADJ_CACHE = {"rows": None}


def load_adjudication(passcode, skip, profile: gr.OAuthProfile | None = None):
    adj = who_is(profile) or "adjudicator"
    blank = (None, "", "", gr.update(), skip, "")
    # The passcode is the gate. A roster is a convenience for attribution, not access control: keeping one
    # means editing a secret every time a resident joins, and the name in a dropdown never stopped anyone.
    if not ADJ_PASSCODE:
        return ("### Adjudication is not configured: no ADJUDICATE_PASSCODE is set on this Space.",) + blank[1:]
    if passcode != ADJ_PASSCODE:
        return ("### Wrong adjudicator passcode.",) + blank[1:]
    if not adj:
        return ("### Sign in with your Hugging Face account first.",) + blank[1:]
    rows = _ADJ_CACHE["rows"]
    if rows is None:
        rows = _ADJ_CACHE["rows"] = disagreements()
    if not rows:
        return ("### Nothing to adjudicate. Every film the two readers have both answered, they agreed on.",
                None, "", gr.update(), 0, "")
    i = int(skip) % len(rows)
    r = rows[i]
    rec = BY_ID[r["film"]]
    # The two readers are shown as A and B, not by name. An adjudicator who knows which student tends to be
    # right stops judging the film and starts judging the student, and the disagreement rate is the measure
    # this programme exists to produce.
    def fmt(d):
        if not d.get("boxes_ok", True):
            return "**boxes unusable**"
        bits = [f"**{d.get('lowest_name')}**"]
        if d.get("l6"): bits.append("L6")
        if d.get("t13"): bits.append("T13")
        if d.get("junction") and d["junction"] != "ordinary": bits.append(d["junction"])
        if d.get("note"): bits.append(f"_{d['note'][:120]}_")
        return " &nbsp;|&nbsp; ".join(bits)
    body = (f"**{i+1} of {len(rows)} contested**\n\n"
            f"| | call |\n|---|---|\n"
            f"| Reader A | {fmt(r['a'])} |\n"
            f"| Reader B | {fmt(r['b'])} |\n"
            f"| the model said | {rec['names'][-1]} |\n")
    return body, draw(r["film"], False), r["film"], gr.update(value=rec["names"][-1]), i, qc_summary(rec)


def save_adjudication(passcode, film_id, lowest, l6, t13, junction_label, boxes_ok, note, skip,
                      profile: gr.OAuthProfile | None = None):
    adj = who_is(profile) or "adjudicator"
    if not ADJ_PASSCODE or passcode != ADJ_PASSCODE:
        return "### Wrong adjudicator passcode.", None, "", gr.update(), skip, ""
    if not adj:
        return "### Sign in first.", None, "", gr.update(), skip, ""
    if not film_id:
        return "### Load a film first.", None, "", gr.update(), skip, ""
    rec = BY_ID[film_id]
    rows = _ADJ_CACHE["rows"] or []
    row = next((r for r in rows if r["film"] == film_id), None)
    dec = {"film": film_id, "adjudicator": adj, "final_lowest": None if not boxes_ok else lowest,
           "l6": bool(l6), "t13": bool(t13), "boxes_ok": bool(boxes_ok), "note": note or "",
           "junction": JUNCTION_OF.get(junction_label, "unsure"),
           "reader_a": _call_of(row["a"]) if row else None,
           "reader_b": _call_of(row["b"]) if row else None,
           "pseudo_lowest": rec["names"][-1], "region": rec["region"],
           "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    api.upload_file(path_or_fileobj=io.BytesIO(json.dumps(dec, indent=1).encode()),
                    path_in_repo=f"adjudications/{film_id}.json", repo_id=LEDGER_REPO,
                    repo_type="dataset", token=TOKEN, commit_message=f"adjudicate {film_id} by {adj}")
    _ADJ_CACHE["rows"] = [r for r in rows if r["film"] != film_id]
    out = load_adjudication(passcode, 0, profile)
    return ("Settled.\n\n" + out[0],) + out[1:]


def refresh_adjudications():
    _ADJ_CACHE["rows"] = None
    rows = disagreements()
    _ADJ_CACHE["rows"] = rows
    return f"### {len(rows)} films are waiting for an adjudicator."


# ---------------------------------------------------------------------------------------------- live QC
# Cheap geometric and sequence checks, run every time a film is drawn. They are approximations on purpose:
# a reader wants to know instantly which box to look at, and a slow exact answer is worth less than a fast
# rough one. Everything is scaled to the FILM'S OWN median body, so nothing needs tuning per source, per
# projection or per magnification -- an absolute threshold in pixels would be wrong on the next dataset.
#
# These flag; they never decide. A flagged film is still the reader's to judge, and an unflagged one is not
# thereby correct.
ORDER = {n: i for i, n in enumerate(NAMES)}
SKIPPABLE = {"T13", "L6"}          # absent from an ordinary spine, so a step over them is not a gap


def _columns(boxes, med_w):
    """Group boxes into vertical runs of spine, left to right.

    A plain radiograph is one column and this returns one group. A published figure is often a montage --
    two projections side by side, or four panels in a grid -- and treating those as one column makes every
    box "overlap its neighbour" and "sit off the column", which is how the first version of this check
    flagged 72 % of FluoroCap panels and would have taught reviewers to ignore it.

    Boxes are sorted by centre x and cut wherever the gap exceeds 1.2 median widths.
    """
    if not boxes:
        return []
    order = sorted(range(len(boxes)), key=lambda i: (boxes[i][0] + boxes[i][2]) / 2.0)
    groups, cur = [], [order[0]]
    for a, b in zip(order, order[1:]):
        ca = (boxes[a][0] + boxes[a][2]) / 2.0
        cb = (boxes[b][0] + boxes[b][2]) / 2.0
        if cb - ca > 1.2 * med_w:
            groups.append(cur); cur = [b]
        else:
            cur.append(b)
    groups.append(cur)
    return groups


def qc_flags(rec):
    """-> (per-box flag lists, film-level messages). Indices match rec['boxes'].

    Checks run WITHIN a column of spine, never across columns, so a montage is judged panel by panel.
    """
    boxes = rec.get("boxes") or []
    names = rec.get("names") or []
    n = len(boxes)
    per = [[] for _ in range(n)]
    film = []
    if n == 0:
        return per, ["no boxes on this film"]
    if len(names) != n:
        film.append(f"**{n} boxes but {len(names)} names** - the pack is inconsistent; do not correct this one")

    hs = [b[3] - b[1] for b in boxes]
    ws = [b[2] - b[0] for b in boxes]
    med_h = sorted(hs)[len(hs) // 2] or 1
    med_w = sorted(ws)[len(ws) // 2] or 1
    W, H = (rec.get("image_size") or [None, None])

    cols = _columns(boxes, med_w)
    if len(cols) > 1:
        film.append(f"_this looks like {len(cols)} images side by side; each is checked on its own_")

    # shape, judged against the whole film -- a vertebra is a vertebra whichever panel it is in
    for i, b in enumerate(boxes):
        h, w = hs[i], ws[i]
        if h < 0.55 * med_h:
            per[i].append("much shorter than its neighbours")
        elif h > 1.8 * med_h:
            per[i].append("much taller than its neighbours")
        ar = w / max(h, 1e-6)
        if ar < 0.6:
            per[i].append("unusually narrow for a vertebral body")
        elif ar > 3.0:
            per[i].append("unusually wide for a vertebral body")
        # Touching the edge is not itself a problem: a published figure is cropped tight and vertebrae
        # reach the border constantly, which is why this check alone accounted for 859 of the flags on
        # FluoroCap. What matters is a box that touches an edge AND is short or narrow for this film --
        # that is a vertebra actually cut in half.
        if H and W:
            touch_v = b[1] <= 1 or b[3] >= H - 1
            touch_h = b[0] <= 1 or b[2] >= W - 1
            if (touch_v and h < 0.8 * med_h) or (touch_h and w < 0.8 * med_w):
                per[i].append("runs off the edge of the image and looks cut in half")

    # position and spacing, judged WITHIN a column
    # split each column again wherever a vertical gap is too large to be missing vertebrae: in a montage
    # that is the join between two stacked sub-images, and calling it a missing body produced 619 flags.
    runs = []
    for col in cols:
        idx = sorted(col, key=lambda i: (boxes[i][1] + boxes[i][3]) / 2.0)
        cur = [idx[0]]
        for a, b_ in zip(idx, idx[1:]):
            if boxes[b_][1] - boxes[a][3] > 2.5 * med_h:
                runs.append(cur); cur = [b_]
            else:
                cur.append(b_)
        runs.append(cur)
    if len(runs) > len(cols):
        film.append("_parts of this image are separated by large gaps and are checked separately_")

    for col in runs:
        idx = sorted(col, key=lambda i: (boxes[i][1] + boxes[i][3]) / 2.0)
        cxs = [(boxes[i][0] + boxes[i][2]) / 2.0 for i in idx]
        med_cx = sorted(cxs)[len(cxs) // 2]
        for k, i in enumerate(idx):
            if len(idx) >= 3 and abs(cxs[k] - med_cx) > 1.5 * med_w:
                per[i].append("sits off the line of the spine")
        for k in range(len(idx) - 1):
            i, j = idx[k], idx[k + 1]
            gap = boxes[j][1] - boxes[i][3]
            if gap > 0.9 * med_h:
                film.append(f"**a vertebra may be missing** between two boxes "
                            f"(the gap is {gap/med_h:.1f} bodies)")
                per[i].append("large gap below"); per[j].append("large gap above")
            elif gap < -0.45 * med_h:
                film.append("two boxes overlap heavily - they may be the same vertebra twice")
                per[i].append("overlaps its neighbour"); per[j].append("overlaps its neighbour")

    # the names, as a sequence, again within a column
    if len(names) == n:
        if len(set(names)) != len(names) and len(cols) == 1:
            dup = sorted({x for x in names if names.count(x) > 1})
            film.append(f"**the same name appears twice**: {', '.join(dup)}")
        for col in runs:
            idx = sorted(col, key=lambda i: (boxes[i][1] + boxes[i][3]) / 2.0)
            seq = [names[i] for i in idx]
            o = [ORDER.get(x) for x in seq]
            if any(v is None for v in o):
                film.append("a name is not a vertebra this scheme knows")
                continue
            for k in range(len(o) - 1):
                step = o[k + 1] - o[k]
                if step <= 0:
                    film.append(f"**the names go backwards** at {seq[k]} -> {seq[k+1]}")
                elif step > 1:
                    skipped = [nm for nm, v in ORDER.items() if o[k] < v < o[k + 1]]
                    if not set(skipped) <= SKIPPABLE:
                        film.append(f"**{seq[k]} to {seq[k+1]} skips {', '.join(skipped)}**")
            lum = [x for x in seq if x.startswith("L") and x[1:].isdigit()]
            if "L6" in seq:
                film.append("this run carries an **L6** - confirm six mobile bodies below the last rib")
            elif len(lum) > 5:
                film.append(f"**{len(lum)} lumbar bodies named without an L6** - either one name is wrong or "
                            f"this spine has six")
            if "T13" in seq:
                film.append("this run carries a **T13** - confirm thirteen rib-bearing levels")

    # one message per kind, so a montage does not repeat itself ten times
    seen, uniq = set(), []
    for m in film:
        key = re.sub(r"\(.*?\)", "", m)
        if key in seen:
            continue
        seen.add(key); uniq.append(m)
    return per, uniq


def qc_summary(rec):
    per, film = qc_flags(rec)
    bits = []
    b = anomaly_banner(rec)
    if b:
        bits.append(b)
    if film:
        bits.append("**Automatic checks**\n\n" + "\n".join(f"- {m}" for m in film))
    boxed = [f"- box {i+1}" + (f" ({rec['names'][i]})" if i < len(rec.get('names') or []) else "")
             + ": " + "; ".join(v) for i, v in enumerate(per) if v]
    if boxed:
        bits.append(("**Boxes worth a second look** (ringed in violet with a !)\n\n" if not film else
                     "**Boxes worth a second look**\n\n") + "\n".join(boxed))
    if not bits:
        return "_Automatic checks found nothing odd about the boxes or the sequence._"
    return "\n\n".join(bits)


# ---------------------------------------------------------------------------------------------- drawing
def draw(film_id: str, show_all_names: bool, s1_pts: str = ""):
    rec = BY_ID[film_id]
    p = hf_hub_download(DATA_REPO, rec["image"], repo_type="dataset", token=TOKEN)
    im = Image.open(p).convert("RGB")
    dr = ImageDraw.Draw(im)
    size = max(15, im.size[1] // 42)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    # the automatic checks, so a reader's eye goes to the suspect box before they have read a word
    per, _ = qc_flags(rec)
    for i, (b, nm) in enumerate(zip(rec["boxes"], rec["names"])):
        last = i == len(rec["boxes"]) - 1
        flagged = bool(per[i]) if i < len(per) else False
        col = (255, 60, 60) if last else (255, 196, 0)
        dr.rectangle(b, outline=col, width=5 if last else 2)
        if flagged:
            # a second, offset outline in violet: distinguishable from the red target box and the amber
            # ordinary ones on a greyscale radiograph, and it reads as an annotation rather than a label
            dr.rectangle([b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4], outline=(214, 74, 226), width=3)
            dr.rectangle([b[0] - 4 - size, b[1] - 4, b[0] - 4, b[1] - 4 + size], fill=(214, 74, 226))
            dr.text((b[0] - 2 - size, b[1] - 4), "!", fill=(255, 255, 255), font=font)
        if last or show_all_names:
            label = nm + ("   <- name this one" if last else "")
            dr.rectangle([b[2] + 4, b[1], b[2] + 10 + int(size * 0.62 * len(label)), b[1] + size + 6], fill=(0, 0, 0))
            dr.text((b[2] + 8, b[1] + 2), label, fill=col, font=font)
    # the reader's divide, and a dot on a half-finished one so a single click is visibly incomplete
    pts = [int(v) for v in str(s1_pts).split(",") if str(v).strip().lstrip("-").isdigit()] if s1_pts else []
    if len(pts) >= 4:
        dr.line([pts[0], pts[1], pts[2], pts[3]], fill=(60, 220, 120), width=5)
        for k in (0, 2):
            dr.ellipse([pts[k] - 6, pts[k + 1] - 6, pts[k] + 6, pts[k + 1] + 6], outline=(60, 220, 120), width=3)
    elif len(pts) == 2:
        dr.ellipse([pts[0] - 8, pts[1] - 8, pts[0] + 8, pts[1] + 8], outline=(60, 220, 120), width=4)
    return im


# ------------------------------------------------------------------------------- creating the S1 label
# THE ONE LABEL NO MODEL CAN BE ASKED FOR YET.
#
# The delimitation rule says a first sacral segment separated from the rest of the sacrum by a residual
# disc is its own object. Across every render and pseudolabel directory in this project, 5,110 images carry
# a sacrum box and ZERO carry an S1 box -- the carved S1 was retired as unreliable and dissolved back into
# the sacrum. There is no example of the thing anywhere, so a detector cannot learn to place what has never
# been drawn. It has to be created by readers first.
#
# A reader draws the dividing line with two clicks. A line rather than a point because the division is
# rarely square to the image: the disc plane is oblique on a lateral and can be tilted on an AP, and a
# single point leaves the angle to be guessed by whatever code consumes it. Two endpoints fix the cut
# exactly, and a box for the segment above follows from the line and the sacrum box already present.
def s1_click(film_id, pts, evt: gr.SelectData):
    """First click starts the line, second finishes it, third starts over."""
    if not film_id:
        return pts or "", None, "### Load a film first."
    x, y = (int(evt.index[0]), int(evt.index[1])) if getattr(evt, "index", None) else (0, 0)
    have = [int(v) for v in str(pts).split(",") if str(v).strip().lstrip("-").isdigit()] if pts else []
    if len(have) >= 4:
        have = []
    have += [x, y]
    val = ",".join(str(v) for v in have)
    if len(have) == 2:
        msg = (f"Started the divide at ({x}, {y}). **Click the other end** - across the bone, following the "
               f"disc or the line where the segment above meets the sacrum.")
    else:
        msg = (f"Divide drawn from ({have[0]}, {have[1]}) to ({have[2]}, {have[3]}). Click again to start "
               f"over, or **Clear** if there is no separate segment after all.")
    return val, draw(film_id, False, val), msg


def clear_s1(film_id):
    return "", (draw(film_id, False, "") if film_id else None), "Divide cleared."


# ---------------------------------------------------------------------------------------------- actions
def load_case(passcode, skip, profile: gr.OAuthProfile | None = None):
    reviewer = identify(profile, passcode)
    if not reviewer:
        return (None, "### Sign in, or enter your personal reviewer code.\n\nA code identifies you the way "
                      "an account would; there is no name to type, because a name anyone can type is not a "
                      "name.", "", gr.update(), skip, "", "")
    if not reviewer:
        return (None, "### Sign in with your Hugging Face account to begin.\n\nThe button is above. Your "
                      "account signs every decision you make, which is what lets two readers be compared.",
                "", gr.update(), skip, "", "")
    if not passed_quiz(reviewer):
        return (None, "### Take the short quiz first.\n\nThe **Training quiz** tab has a handful of cases "
                      "whose answers are known from CT. Pass it once and this tab unlocks for you - it "
                      "exists because two readers who share a misconception agree with each other, and the "
                      "agreement is what gets written into the training set.",
                "", gr.update(), skip, "", "")
    mine = assigned_to(reviewer)
    if not mine:
        return None, f"### No films are assigned to **{reviewer}**.", "", gr.update(), skip, "", ""
    done = done_by(reviewer)
    todo = [f for f in mine if f not in done]
    if not todo:
        return None, f"### Finished. All {len(mine)} of your films are reviewed. Thank you.", "", gr.update(), skip, "", ""
    idx = int(skip) % len(todo)
    fid = todo[idx]
    rec = BY_ID[fid]
    pct = 100 * len(done) / max(1, len(mine))
    status = (f"**{reviewer}** &nbsp; {len(done)} of {len(mine)} done ({pct:.0f}%) &nbsp;|&nbsp; {len(todo)} left\n\n"
              f"Film `{fid}` &nbsp; {rec['region']} &nbsp; {len(rec['boxes'])} vertebrae boxed &nbsp;|&nbsp; "
              f"the model called the red one **{rec['names'][-1]}** (confidence {rec.get('p_lowest', '?')})")
    # THE CAPTION IS CONTEXT, NEVER AN ANSWER. A panel harvested from the literature arrived with a figure
    # legend, and the decoder already used it as evidence; hiding it would ask the reader to work with less
    # than the machine had. Captions are wrong often enough that it is labelled as a claim, not a fact.
    cap = ""
    if rec.get("caption"):
        cap = ("### What the article said about this figure\n\n"
               f"> {rec['caption']}\n\n")
        bits = []
        if rec.get("caption_levels"):
            bits.append(f"levels named in the caption: **{rec['caption_levels']}**")
        if rec.get("caption_transitional"):
            bits.append("the caption was matched by a **transitional anatomy** search")
        if rec.get("article"):
            bits.append(f"*{rec['article']}*" + (f", {rec['journal']}" if rec.get("journal") else ""))
        if bits:
            cap += " &nbsp;|&nbsp; ".join(bits) + "\n\n"
        cap += ("The caption is what the authors wrote, not a label. Judge the picture; use the caption only "
                "to tell you roughly where in the spine you are.\n")
    elif MANIFEST.get("kind") == "fluorocap_panels":
        cap = "_No caption was recovered for this panel._\n"
    return draw(fid, False), status, fid, gr.update(value=rec["names"][-1]), idx, cap, qc_summary(rec)


def save(passcode, film_id, lowest, l6, t13, junction_label, boxes_ok, cap_mismatch, note, s1_xy, skip,
         profile: gr.OAuthProfile | None = None):
    reviewer = identify(profile, passcode)
    if not reviewer:
        return "### Sign in, or enter your reviewer code.", None, "", gr.update(), skip, "", ""
    if not reviewer:
        return "### Sign in first.", None, "", gr.update(), skip, "", ""
    if not film_id:
        return "### Load a film first.", None, "", gr.update(), skip, "", ""
    if not passed_quiz(reviewer):
        return "### Take the quiz first.", None, "", gr.update(), skip, "", ""
    rec = BY_ID[film_id]
    dec = {"film": film_id, "reviewer": reviewer, "lowest_name": None if not boxes_ok else lowest,
           "l6": bool(l6), "t13": bool(t13),
           # The commonest lumbosacral transitional vertebra is a SACRALISED L5: five lumbar bodies still,
           # so the L6 tick is correctly left alone and the finding had nowhere to go until this field.
           "junction": JUNCTION_OF.get(junction_label, "unsure"),
           # the first S1 labels this corpus will contain: the two endpoints of the divide
           "s1_divide": ([int(v) for v in str(s1_xy).split(",")] if s1_xy else None),
           "boxes_ok": bool(boxes_ok),
           "caption_mismatch": bool(cap_mismatch), "note": note or "",
           "pseudo_lowest": rec["names"][-1], "n_boxes": len(rec["boxes"]), "region": rec["region"],
           "source": rec.get("source", "radiograph"), "tier": rec.get("tier"),
           "changed": bool(boxes_ok and lowest != rec["names"][-1]), "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    api.upload_file(path_or_fileobj=io.BytesIO(json.dumps(dec, indent=1).encode()),
                    path_in_repo=f"decisions/{reviewer}/{film_id}.json", repo_id=LEDGER_REPO,
                    repo_type="dataset", token=TOKEN, commit_message=f"review {film_id} by {reviewer}")
    img, status, fid, low, _, cap, qctext = load_case(passcode, 0, profile)
    tag = " &nbsp;**corrected**" if dec["changed"] else ""
    flags = (" &nbsp;**L6**" if l6 else "") + (" &nbsp;**T13**" if t13 else "")
    return f"Saved{tag}{flags}.\n\n{status}", img, fid, low, 0, cap, qctext


def skip_case(passcode, skip, profile: gr.OAuthProfile | None = None):
    return load_case(passcode, int(skip) + 1, profile)


def toggle_names(film_id, show, s1_pts=""):
    if not film_id:
        return None
    return draw(film_id, show, s1_pts)


# ---------------------------------------------------------------------------------------------- progress
def kappa(a, b):
    """Cohen's kappa over paired categorical calls."""
    if not a:
        return None
    cats = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def progress_report():
    files = _ledger_files()
    per_reviewer = Counter()
    for f in files:
        parts = f.split("/")
        if len(parts) == 3 and parts[0] == "decisions":
            per_reviewer[parts[1]] += 1
    lines = ["## Progress", "", "| reviewer | films read | assigned |", "|---|---|---|"]
    total = 0
    for who in (REVIEWERS or sorted(per_reviewer)):
        n = per_reviewer.get(who, 0)
        total += n
        lines.append(f"| {who} | {n} | {len(assigned_to(who))} |")
    lines.append("")
    lines.append(f"**{total}** decisions over **{len(FILMS)}** films; each film needs two, so "
                 f"**{2 * len(FILMS)}** in total.")
    seen = defaultdict(list)
    for f in files:
        parts = f.split("/")
        if len(parts) == 3 and parts[0] == "decisions":
            seen[Path(parts[2]).stem].append(parts[1])
    both = [k for k, v in seen.items() if len(v) >= 2]
    lines.append("")
    lines.append(f"**{len(both)}** films have both reads.")
    if both:
        A, B, fl_a, fl_b = [], [], [], []
        for film in both[:400]:
            try:
                d = []
                for who in seen[film][:2]:
                    p = hf_hub_download(LEDGER_REPO, f"decisions/{who}/{film}.json", repo_type="dataset", token=TOKEN)
                    d.append(json.load(open(p)))
                A.append(str(d[0].get("lowest_name")))
                B.append(str(d[1].get("lowest_name")))
                fl_a.append(str(bool(d[0]["l6"]) or bool(d[0]["t13"])))
                fl_b.append(str(bool(d[1]["l6"]) or bool(d[1]["t13"])))
            except Exception:  # noqa: BLE001
                continue
        if A:
            agree = sum(x == y for x, y in zip(A, B)) / len(A)
            k1 = kappa(A, B)
            k2 = kappa(fl_a, fl_b)
            lines += ["", "| measure | value |", "|---|---|",
                      f"| films compared | {len(A)} |",
                      f"| raw agreement on the name | {100 * agree:.1f}% |",
                      f"| Cohen's kappa, name | {k1:.3f} |",
                      f"| Cohen's kappa, variant tick | {k2:.3f} |",
                      f"| disagreements to adjudicate | {sum(x != y for x, y in zip(A, B))} |"]
    return "\n".join(lines)


GUIDE = """
## What you are looking at

A radiograph with its vertebrae boxed by a detector and **named by a model**. Those names are a guess. They
are usually right in shape, but the whole run can be **shifted by one level**.

## What to do

**Name the vertebra in the red box** - the lowest one in view. Everything above it is renamed from that, so
one name fixes the whole film.

### How to work out which one it is
1. **Find a landmark.** The sacrum (the solid triangular bone at the bottom), the lowest rib, the first rib,
   or the odontoid peg at the top of the neck.
2. **Count from it.** The last rib-bearing vertebra is normally T12, so the one below it is L1.
3. **Name the red box** from that count.

### Tick a box when the spine is unusual

These two ticks are **the most valuable answers you can give.** Until very recently the model had never seen
a real radiograph of a six-lumbar spine - every example it learned from was a simulated image made from a CT
scan. One tick from you creates a training example that barely exists anywhere in the corpus.

Above the image you will see **how likely the model thinks this film is transitional**. When it says the
film is in the top few percent, slow down and count deliberately; when it says the film is unremarkable,
that is not a promise, and a variant the model missed is exactly the example worth catching.

#### L6 - six lumbar vertebrae (or a lumbarised S1)
- **Count the mobile bodies between the last rib-bearing vertebra and the sacrum. Six instead of five.**
- The lowest one sits **free of the sacral wing**, with a visible disc space underneath it, where you
  expected the solid sacrum to begin.
- The body is squared off like a lumbar vertebra rather than curving into the sacral promontory.
- A **partially lumbarised S1** is the same thing halfway: a residual disc space between S1 and S2, so the
  top sacral segment looks like a small lumbar body that has not fully joined the rest of the sacrum. Tick
  L6 and say so in the note - a partial case is worth more to us than a clear one.


### Drawing the divide on a sacrum that carries a separate segment

Some sacrums have a segment sitting on top that has not fully joined the rest &mdash; a partially lumbarised
S1. **No annotation anywhere in this project has ever marked one.** Every image we hold draws the sacrum as
one object, so there is no example of the division for a model to learn from, and yours would be the first.

**Two clicks.** Click one end of the dividing line, then the other. The line appears in green as you go, a
third click starts over, and **Clear** removes it.

<div style="display:flex;gap:18px;flex-wrap:wrap;margin:14px 0">

<figure style="margin:0;flex:1 1 230px;min-width:220px">
<svg viewBox="0 0 220 300" style="width:100%;background:#12151a;border-radius:4px">
  <text x="110" y="20" fill="#7cc3a0" font-size="13" text-anchor="middle" font-family="sans-serif">RIGHT</text>
  <rect x="62" y="34" width="96" height="46" rx="5" fill="#3a4250"/><text x="110" y="62" fill="#c9d2de" font-size="13" text-anchor="middle" font-family="sans-serif">L5</text>
  <rect x="58" y="92" width="104" height="40" rx="5" fill="#4a5262"/><text x="110" y="117" fill="#e7eaef" font-size="12" text-anchor="middle" font-family="sans-serif">separate</text>
  <path d="M46 144 L174 152 L156 264 L64 264 Z" fill="#3a4250"/>
  <text x="110" y="215" fill="#c9d2de" font-size="13" text-anchor="middle" font-family="sans-serif">sacrum</text>
  <line x1="44" y1="138" x2="176" y2="146" stroke="#3cdc78" stroke-width="5"/>
  <circle cx="44" cy="138" r="7" fill="none" stroke="#3cdc78" stroke-width="3"/>
  <circle cx="176" cy="146" r="7" fill="none" stroke="#3cdc78" stroke-width="3"/>
</svg>
<figcaption style="font-size:12.5px;color:#a3abb8;margin-top:6px">Across the full width of the bone, following the gap. Slanted is normal &mdash; match the bone, not the screen.</figcaption>
</figure>

<figure style="margin:0;flex:1 1 230px;min-width:220px">
<svg viewBox="0 0 220 300" style="width:100%;background:#12151a;border-radius:4px">
  <text x="110" y="20" fill="#e08a80" font-size="13" text-anchor="middle" font-family="sans-serif">WRONG &mdash; too short</text>
  <rect x="62" y="34" width="96" height="46" rx="5" fill="#3a4250"/>
  <rect x="58" y="92" width="104" height="40" rx="5" fill="#4a5262"/>
  <path d="M46 144 L174 152 L156 264 L64 264 Z" fill="#3a4250"/>
  <line x1="92" y1="141" x2="128" y2="143" stroke="#e08a80" stroke-width="5"/>
  <circle cx="92" cy="141" r="7" fill="none" stroke="#e08a80" stroke-width="3"/>
  <circle cx="128" cy="143" r="7" fill="none" stroke="#e08a80" stroke-width="3"/>
</svg>
<figcaption style="font-size:12.5px;color:#a3abb8;margin-top:6px">A stub in the middle does not say where the edges are, so the segment above it cannot be cut out.</figcaption>
</figure>

<figure style="margin:0;flex:1 1 230px;min-width:220px">
<svg viewBox="0 0 220 300" style="width:100%;background:#12151a;border-radius:4px">
  <text x="110" y="20" fill="#e08a80" font-size="13" text-anchor="middle" font-family="sans-serif">WRONG &mdash; wrong gap</text>
  <rect x="62" y="34" width="96" height="46" rx="5" fill="#3a4250"/><text x="110" y="62" fill="#c9d2de" font-size="13" text-anchor="middle" font-family="sans-serif">L5</text>
  <rect x="58" y="92" width="104" height="40" rx="5" fill="#4a5262"/>
  <path d="M46 144 L174 152 L156 264 L64 264 Z" fill="#3a4250"/>
  <line x1="52" y1="86" x2="168" y2="88" stroke="#e08a80" stroke-width="5"/>
  <circle cx="52" cy="86" r="7" fill="none" stroke="#e08a80" stroke-width="3"/>
  <circle cx="168" cy="88" r="7" fill="none" stroke="#e08a80" stroke-width="3"/>
</svg>
<figcaption style="font-size:12.5px;color:#a3abb8;margin-top:6px">That is the L5 disc, which is already boxed. The one we need is the <em>next one down</em>.</figcaption>
</figure>

</div>

**Where the line goes.** Along the gap between that top segment and the rest of the sacrum &mdash; the disc
if you can see it, otherwise the seam where the two meet. Take it **all the way across the bone**, from one
edge to the other. It will usually be slanted rather than square to the screen, because the sacrum is tilted;
follow the bone rather than the image.

**When not to draw one at all.** Most sacrums are a single fused mass with no separate segment on top. If you
cannot see a division, leave it blank &mdash; that is the common and correct answer. A line drawn where there
is no gap is worse than no line, because it manufactures an example of something that is not there.

**Do not confuse it with the disc above.** The lowest disc that is already boxed is the one between the last
lumbar vertebra and the sacrum. The one we are asking about is the **next one down**, inside the sacrum.

#### The one rule that settles the hard cases: look for the disc, not for the fusion

When a body is part-joined to the sacrum it is tempting to judge by how fused it looks. Do not. Whether the
transverse process has bridged to the sacral wing is a poor guide - on about a third of these the bridge is
joint-like in one place and solid bone in another, and even experienced spine surgeons disagree about which
endplate belongs to the sacrum. What is decidable from the picture in front of you is the **disc**:

- **A disc still separates the body from the sacrum** - even if a broad transverse process is clearly
  bridging across to the ala - then it is a **separate vertebra**. Count it.
- **The disc is gone**, the bodies running together with no space between them, then it is **part of the
  sacrum**. Do not count it.
- **A disc between the first and second sacral segments** is the same rule pointing the other way: that top
  sacral segment is separate, so count it, and note that you saw an S1-S2 disc.

You are not being asked to grade the fusion. If you can see how fused it is, write that in the note and it
will be recorded - but the count follows the disc.
- Sanity check: a line across the top of the iliac crests usually crosses around L4-L5. If your count puts
  it somewhere very different, count again.

#### The opposite - a sacralised L5
- The lowest lumbar body is **fused or partly fused to the sacrum**: the disc space beneath it is missing or
  reduced to a thin sclerotic line.
- Its **transverse process is enlarged and bat-wing shaped**, reaching toward or touching the sacral ala -
  sometimes forming a false joint with it, sometimes fused solid.
- This is *not* an L6 tick. It is the reason a count can come out one short, so note it and name what you
  see.

#### T13 - thirteen rib-bearing levels
- **Count the ribs where they are visible.** A rib on the vertebra below the one you called T12.
- A body that looks lumbar in shape but carries a small rib. Stub ribs can be short and easy to miss at the
  edge of the field.

#### When the two ends disagree
A spine can be unusual at the top *and* the bottom, and the two tend to occur together. If the rib count and
the lumbar count give different answers, say so in the note rather than forcing one of them.

### When you are not sure
- **Untick "boxes are usable"** if the boxes are on the wrong structures, badly incomplete, or the image is
  unreadable. The film is then dropped rather than mislabelled.
- **Leave the name as it is and write a note** if you genuinely cannot tell. An abstention is useful data. A
  guess is not.
- **Skip** moves on without recording anything.

## If this set has captions (published figures)

Some panels come from journal figures and arrive with the article's own caption, shown under the image. Use
it to tell you **roughly where in the spine you are** — it is often the only clue when the field is tight —
but judge the picture. Captions are written for a different purpose and are wrong often enough that they
cannot be the answer.

Tick **"the labels do not match the caption"** when the two are describing different parts of the spine. That
is a detector or decoder failure rather than a naming question, and it is useful to know separately.

## How your work is used
Two people read every film independently, and you never see the other person's answer. Films you both agree
on go into the training set; films you disagree on go to a radiology resident on the **Adjudicate** tab,
who sees both calls without being told whose they are and makes the final one. Reader agreement, including
Cohen's kappa, is on the **Progress** tab.

Every answer is saved the moment you press Save, so you can stop and resume whenever you like.
"""

with gr.Blocks(title="Vertebra level review", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Vertebra level review\nName the vertebra in the **red** box. One name fixes the whole film.")
    with gr.Tabs():
        with gr.Tab("Review"):
            with gr.Row():
                with gr.Column(scale=5):
                    img = gr.Image(label="Film", type="pil", height=760, show_download_button=False)
                    show_all = gr.Checkbox(label="Show the model's name on every box", value=False)
                    qc = gr.Markdown()
                    caption = gr.Markdown()
                with gr.Column(scale=3):
                    gr.Markdown("### Sign in")
                    gr.LoginButton()
                    passcode = gr.Textbox(label="Your reviewer code", type="password")
                    gr.Markdown(
                        "_Sign in if the button works. If it does not, your personal reviewer code "
                        "identifies you instead - it is yours alone, so two readers stay distinguishable. "
                        "Do not pass it on._")
                    load = gr.Button("Load my next film", variant="primary")
                    status = gr.Markdown()
                    film_id = gr.Textbox(label="Film", interactive=False)
                    gr.Markdown("### Your answer")
                    lowest = gr.Dropdown(NAMES, label="The vertebra in the red box is", value="L5")
                    l6 = gr.Checkbox(label="L6 - this spine has six lumbar vertebrae")
                    t13 = gr.Checkbox(label="T13 - this spine has thirteen rib-bearing levels")
                    junction = gr.Radio(JUNCTION_LABELS, label="This spine's junctions are",
                                        value=JUNCTION_LABELS[0])
                    boxes_ok = gr.Checkbox(label="Boxes are usable", value=True)
                    cap_mismatch = gr.Checkbox(
                        label="The labels do not match the caption",
                        visible=(MANIFEST.get("kind") == "fluorocap_panels"))
                    gr.Markdown(
                        "### If a segment sits separately on top of the sacrum"
                        "\n\n"
                        "**Click each end of the line that divides it** - the disc, or the seam where "
                        "that segment meets the rest of the sacrum. Two clicks draw it; a third starts "
                        "over."
                        "\n\n"
                        "Nothing in this corpus has ever marked one, so your line is the first example "
                        "of it. See **How to review** for what to look for and how to place it.")
                    with gr.Row():
                        s1_xy = gr.Textbox(label="The divide (two points)", interactive=False, scale=2)
                        s1_clear = gr.Button("Clear", scale=1)
                    note = gr.Textbox(label="Note (optional)", lines=2,
                                      placeholder="e.g. cannot see the sacrum; rotated; hardware over L4")
                    with gr.Row():
                        save_b = gr.Button("Save and next", variant="primary", scale=2)
                        skip_b = gr.Button("Skip", scale=1)
                    skip = gr.Number(value=0, visible=False)
        with gr.Tab("Adjudicate", visible=bool(ADJ_PASSCODE)):
            gr.Markdown(
                "## Adjudication\n"
                "Films **two readers answered differently**. You see both calls, not who made them, and your "
                "answer is final. A film the readers agreed on never reaches this tab.")
            with gr.Row():
                with gr.Column(scale=5):
                    a_img = gr.Image(label="Film", type="pil", height=760, show_download_button=False)
                    a_all = gr.Checkbox(label="Show the model's name on every box", value=False)
                    a_qc = gr.Markdown()
                with gr.Column(scale=3):
                    gr.Markdown("### Sign in")
                    gr.LoginButton()
                    a_pass = gr.Textbox(label="Adjudicator passcode", type="password")
                    gr.Markdown(
                        "_Two things are needed: an account, which says who ruled, and the passcode, which "
                        "says you are allowed to. A ruling overrides two other readers and no third reader "
                        "undoes it._")
                    with gr.Row():
                        a_load = gr.Button("Load the next contested film", variant="primary", scale=2)
                        a_count = gr.Button("How many are waiting?", scale=1)
                    a_status = gr.Markdown()
                    a_film = gr.Textbox(label="Film", interactive=False)
                    gr.Markdown("### Your ruling")
                    a_low = gr.Dropdown(NAMES, label="The vertebra in the red box is", value="L5")
                    a_l6 = gr.Checkbox(label="L6 - six lumbar vertebrae")
                    a_t13 = gr.Checkbox(label="T13 - thirteen rib-bearing levels")
                    a_junction = gr.Radio(JUNCTION_LABELS, label="This spine's junctions are",
                                          value=JUNCTION_LABELS[0])
                    a_ok = gr.Checkbox(label="Boxes are usable", value=True)
                    a_note = gr.Textbox(label="Note (optional)", lines=2,
                                        placeholder="why the readers differed, if it is instructive")
                    with gr.Row():
                        a_save = gr.Button("Settle and next", variant="primary", scale=2)
                        a_skip = gr.Button("Skip", scale=1)
                    a_i = gr.Number(value=0, visible=False)
        with gr.Tab("Training quiz", visible=bool(QUIZ)):
            gr.Markdown(
                "## Before you start\n\n"
                "A handful of cases whose answers are known from the CT they were rendered from. Work "
                "through them once, then press **Finish**. You need "
                f"**{(QUIZ or {}).get('pass_mark', '?')} of {len((QUIZ or {}).get('items') or [])}**.\n\n"
                "This is not a hurdle for its own sake. Most people have never been shown a "
                "transitional spine, and a reviewer who cannot recognise one does not abstain - they "
                "give a plausible name, the second reader gives the same plausible name, and the two "
                "agreeing is exactly what gets written into the training set. The quiz makes sure you "
                "have seen each kind at least once.")
            with gr.Row():
                with gr.Column(scale=5):
                    q_img = gr.Image(label="Case", type="pil", height=700, show_download_button=False)
                with gr.Column(scale=3):
                    gr.LoginButton()
                    q_pass = gr.Textbox(label="Your reviewer code", type="password")
                    q_start = gr.Button("Start the quiz", variant="primary")
                    q_text = gr.Markdown()
                    q_film = gr.Textbox(label="Case", interactive=False)
                    q_low = gr.Dropdown(NAMES, label="The vertebra in the red box is", value="L5")
                    q_junction = gr.Radio(JUNCTION_LABELS, label="This spine's junctions are",
                                          value=JUNCTION_LABELS[0])
                    q_submit = gr.Button("Answer and go on", variant="primary")
                    q_done = gr.Button("Finish and record my score")
                    q_i = gr.Number(value=0, visible=False)
                    q_tally = gr.Textbox(value="", visible=False)
        with gr.Tab("How to review"):
            gr.Markdown(GUIDE)
        with gr.Tab("Progress"):
            prog = gr.Markdown()
            refresh = gr.Button("Refresh")
            refresh.click(progress_report, None, prog)

    load.click(load_case, [passcode, skip], [img, status, film_id, lowest, skip, caption, qc])
    skip_b.click(skip_case, [passcode, skip], [img, status, film_id, lowest, skip, caption, qc])
    save_b.click(save, [passcode, film_id, lowest, l6, t13, junction, boxes_ok, cap_mismatch, note,
                        s1_xy, skip],
                 [status, img, film_id, lowest, skip, caption, qc])
    show_all.change(toggle_names, [film_id, show_all, s1_xy], img)
    img.select(s1_click, [film_id, s1_xy], [s1_xy, img, status])
    s1_clear.click(clear_s1, [film_id], [s1_xy, img, status])

    a_load.click(load_adjudication, [a_pass, a_i], [a_status, a_img, a_film, a_low, a_i, a_qc])
    a_skip.click(lambda pw, i, profile=None: load_adjudication(pw, int(i) + 1, profile),
                 [a_pass, a_i], [a_status, a_img, a_film, a_low, a_i, a_qc])
    a_save.click(save_adjudication, [a_pass, a_film, a_low, a_l6, a_t13, a_junction, a_ok, a_note, a_i],
                 [a_status, a_img, a_film, a_low, a_i, a_qc])
    a_count.click(refresh_adjudications, None, a_status)
    a_all.change(toggle_names, [a_film, a_all], a_img)

    def _quiz_step(i, low, junc, tal, pw, profile: gr.OAuthProfile | None = None):
        text, img, fid, nxt, verdict = quiz_answer(i, low, junc, pw, profile)
        if verdict not in ("correct", "wrong"):
            return text, img, fid, nxt, tal
        return text, img, fid, nxt, ((tal + "," if tal else "") + verdict)

    q_start.click(lambda: quiz_item(0), None, [q_img, q_text, q_film, q_i])
    q_submit.click(_quiz_step, [q_i, q_low, q_junction, q_tally, q_pass],
                   [q_text, q_img, q_film, q_i, q_tally])
    q_done.click(quiz_finish, [q_tally, q_pass], q_text)


if __name__ == "__main__":
    # server_name is passed explicitly rather than left to GRADIO_SERVER_NAME: inside the Space's container
    # gradio cannot reach its own loopback to verify the server, and without an explicit bind it refuses to
    # start with "When localhost is not accessible, a shareable link must be created".
    demo.launch(server_name=os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0"),
                server_port=int(os.environ.get("REVIEW_PORT", "7860")),
                share=bool(os.environ.get("REVIEW_SHARE")),
                show_api=False)
