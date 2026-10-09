# Naming vertebrae on fluoroscopy panels — reader's guide

*Everything on this page; nothing else to read. Page 2 is reference.*

**What you are doing.** We have ~5,400 spine radiographs and fluoroscopy frames cut out of published figures.
One computer drew a box round each vertebra and named it. A second computer read the figure's caption and named
the same boxes. On real radiographs the two agree almost always; on these figure panels they agree on about one
vertebra in five, and **no human has ever read one of these panels**, so nobody knows which side is wrong. You
are the first. You do not have to be right about everything — you have to be honest about what you can and
cannot see.

## 1. The naming convention

**C1 C2 C3 C4 C5 C6 C7 · T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 · L1 L2 L3 L4 L5 · sacrum**

Write it exactly like that — capital letter, no space, no zero padding: `C7`, `T12`, `L4`, `sacrum`. Everything
at or below the sacral promontory, S1 included, is `sacrum`. There is no `S1` in this scheme.

**T13 and L6 are variant names, used only when you can see the extra bone.** They are not "the next one down".

- **L6** — six lumbar-type (rib-free, mobile) vertebrae between the last rib-bearing vertebra and the sacrum.
- **T13** — thirteen rib-bearing vertebrae: a rib on the level below the twelfth rib-bearing one.

If you cannot see the ribs, or cannot see the sacrum, you cannot establish either, and the answer is not
"probably L6" — it is `unreadable`. Carrino and colleagues (*Radiology*, 2011) found a numerical variant in
about 12% of lumbar MRI, so if you are calling L6 on a quarter of your panels something has gone wrong. Our
labels claim a T13 or an L6 on 146 of 3,328 panels and the model claims one on 35; at least one of those two is
badly off, and finding out which is much of why you are reading these.

## 2. Name only what the picture supports

Do not count down from C2 unless C2 is in the picture.

| if you can see | then |
|---|---|
| skull base and odontoid | the ring under the skull is C1, the peg is C2, count down |
| the last rib | that vertebra is normally T12 — count from there |
| the sacrum / sacral ala | the mobile vertebra just above it is normally L5 — count up |
| letters printed in the image (`L4`, an arrow, a ruler) | trust them over both computers |
| hardware the caption names | anchor on it, but check the metal is where the caption says |

**The caption is evidence, not truth.** One caption covers a whole figure, and a figure often holds panels (a),
(b), (c) of different patients, different regions, even a CT. A caption may say "C1–C2 fusion" over a lumbar
film. That mismatch is what we are hunting: when caption and image disagree, **believe the image**.

## 3. When the film is cut off

Cropping is normal and does not by itself make a panel unreadable.

- **A naming landmark is still visible** (last rib, sacrum, skull base, printed label, named implant) → name it.
- **No landmark at all** — four look-alike lumbar bodies with nothing above or below → mark every vertebra row
  `unreadable`. Do **not** fall back on the caption and do **not** guess from vertebral shape alone.
- **Some boxes nameable, some not** → judge each row separately.

"Lumbar, but I cannot say which lumbar" is a useful answer: `verdict = unreadable`, `notes = lumbar`.

## 4. When you are unsure

Put `1` in `unsure` and still give your best verdict; we count those separately. If you truly cannot choose,
`verdict = unreadable`. **Never leave a row blank** — a blank row cannot be counted. If a panel confuses you for
more than about a minute, put a word in `notes` and move on. Read at ward speed; don't look things up to raise
your score.

## 5. The words you type

One row per vertebra. The `allowed_verdicts` column already tells you which words that row takes.

**They disagree** (`they_agree = 0`): `label` (blue caption name is right) · `model` (orange model name is
right) · `both_wrong` (+ the right name in `correct_name`) · `unreadable`.

**They already agree** (`they_agree = 1`): `both_right` · `both_wrong` (+ `correct_name`) · `unreadable`.

**Whole-panel problems** go in `..._panels.csv` under `panel_verdict`, and then you may leave that panel's
vertebra rows `unreadable`: `readable` · `not_a_radiograph` (CT, MRI, photo, drawing) ·
`montage_multiple_films` (one panel holding two or more separate films) · `too_blurry_to_name` ·
`no_spine_visible`. `not_a_radiograph` and `montage_multiple_films` are currently guesses a computer made that
nobody has ever checked — your call on those two is a result in itself, so make it even when it is boring.

---

# Reference

## Your files — `FluoroCap/student_pack/`, you are `student_NN`

| file | what it is |
|---|---|
| `sheets/student_NN/sheet_01.png` | a contact sheet of 12 panels — an index, start here |
| `panels/<image_id>.png` | the full-size panel you actually read |
| `verdicts/student_NN_vertebrae.csv` | **one row per vertebra — fill in `verdict`** |
| `verdicts/student_NN_panels.csv` | one row per panel: whole-panel problems, and your timing |

On a panel rendering: **green box** = caption label and model agree; **red box** = they disagree, blue name is
the **label**, orange name is the **model**. The **number in the box corner** is `box_no` in your CSV — find
your row by `image_id` + `box_no`, never by row number. The header gives the panel's true size in pixels and the
magnification: `shown at 3.00x` means a blown-up thumbnail, so expect softness and do not read it as pathology.

Save as CSV, not .xlsx. Keep the column order. Do not rename the file.

## Timing

When you finish a sheet, put the minutes it took in `minutes_for_this_sheet` on that sheet's first row in the
panels CSV. One number per sheet.

The pack is 372 panels / 2,553 vertebrae; with double reads, 428 panel-readings and 3,027 rows — **about 33
panels and 233 rows each** across thirteen readers, in three sheets of twelve. Median panel has 4 vertebrae, a
few have over twenty. We estimate **30–60 panels an hour** (230–410 rows), from an assumed 25–40 s to orient on
a panel plus 5–10 s per row, since the row already names both candidates and you choose one word. **That has
never been measured on a person** — which is what the timing box is for.

| job | student-hours | staffing |
|---|---|---|
| your share | 0.6 – 1.1 h | one sitting |
| the whole 372-panel pack, once | 7 – 14 h | thirteen readers, one morning |
| the 200-panel priority sample only | 3.5 – 7 h | **one** student in a day, or two in a morning |
| that sample read **twice**, for reader agreement | 7 – 14 h | **two** students in a day |

Some panels are double-read on purpose. If one looks familiar, it may well be. Read it again as if for the
first time; do not go looking for your earlier answer.

---

*A panel that fits none of these categories is the most interesting thing you can find. Put it in `notes` and
tell Greg.*
