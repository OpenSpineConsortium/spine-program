Written for: the students reviewing the pseudolabelled films, and whoever sets the review up.

# Vertebra level review

You will be shown a radiograph with its vertebrae boxed and named by a model. The names are a guess. Your job
is to name **one** vertebra — the one in the red box, the lowest one in view — and everything above it is
renamed from that. Most films take a few seconds.

## Why one name fixes the whole film

The names came from a decoder that reads the boxes top to bottom and assigns consecutive names. When it is
wrong it is almost always wrong by an *offset*: the run is called L1–L5 when it is really T12–L4. It is
almost never scrambled, because the decode is monotone by construction. So naming the bottom vertebra fixes
every name above it, and asking you for twenty names would cost twenty times as much and buy the same
correction.

Two things an offset cannot express, so they are separate ticks:

- **L6** — this spine has six lumbar vertebrae.
- **T13** — this spine has a thirteenth rib-bearing level.

These are the cases the whole project exists for. They matter more than the ordinary films.

And two honest ways out:

- **Untick "boxes are usable"** if the boxes are on the wrong thing, badly incomplete, or the image is
  unreadable. The film is dropped rather than mislabelled.
- **Leave the name alone and write a note** if you cannot tell. An abstention is data. A guess is not.

Two people review every film independently, and you never see the other person's answer. Films you disagree
on go to an adjudication list rather than into training.

## Setting yourself up (once, about five minutes)

1. Make a free account at <https://huggingface.co/join> if you do not have one, and tell the maintainer your
   username so they can grant you access to the private film repository.
2. Create a token at <https://huggingface.co/settings/tokens> with **write** access, then sign in:

   ```bash
   pip install "gradio==5.9.1" "huggingface_hub>=0.26" pillow
   huggingface-cli login          # paste the token
   ```

3. Run the app:

   ```bash
   REVIEWERS="<your-username>" python app.py
   ```

   It prints a local address. Open it, pick your name, and press **Load my next film**.

`REVIEWERS` should be the full comma-separated roster when the maintainer runs it, because that list is what
decides which films are yours; with only your own name in it you will be shown every film.

## What happens to your answers

Each decision is written immediately as one small file in a private dataset repository — the film, your
username, the name you gave, the two ticks, your note, and the model's original guess. Nothing is kept only
in the app, so closing the browser loses nothing and you can stop and resume whenever you like.

## For the maintainer

`tools/build_review_pack.py` packs the films worth reviewing — those whose decode reached no landmark first,
then the ones flagged as variants, then the least confident — into a private dataset repository and, if the
account can host one, a private Space. **A private Space needs a paid Hugging Face plan**; without one the
script uploads the films and prints these instructions instead of creating a public Space, because the films
are real radiographs and this code is not public.

Grant each reviewer read access to the films repository and write access to the ledger repository, then send
them this page. When the reviews are in:

```bash
huggingface-cli download gregoryschwingmdphd/level-review-ledger --repo-type dataset --local-dir ~/review_ledger
python tools/apply_review_corrections.py --pack ~/review_pack --ledger ~/review_ledger \
    --src ~/nhanes_pseudo --out ~/nhanes_reviewed
```

That writes out only the films both reviewers agreed on, sends the rest to `ADJUDICATION.csv`, and reports
the agreement rate, the correction rate, and where the corrections fell.
