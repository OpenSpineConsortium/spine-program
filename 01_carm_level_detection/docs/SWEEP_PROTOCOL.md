Written for: the radiographer or radiologic technologist at the C-arm, and the surgeon who asks for the sweep.

# The level-map sweep

## What this is

A short, ordered series of overlapping fluoroscopic exposures that builds a map of the patient's own spine,
from a landmark to the level you are working at. Every later spot image is matched onto that map, so the
software can name the vertebrae in it even though the spot image itself contains no landmark.

It replaces counting by eye, and it replaces the preoperative CT that registration systems need. It does not
replace your judgement: the system says what it is unsure about, and when it is unsure you count.

## Before you start

- Lateral is the primary sweep. Add an anteroposterior sweep when the surgeon asks for one, or when the
  lateral cannot show the anatomy (large habitus, upper thoracic, severe scoliosis).
- Use the same field size for the whole sweep. Do not zoom part-way through. If you change magnification, the
  sweep restarts.
- Keep the patient still. A sweep takes under a minute; a sweep across a position change is two sweeps.
- Collimate as you normally would. Field size barely moved the naming in testing (93–95% at two vertebrae
  across a collimated, a 9-inch and a 12-inch field, one body of overlap). A larger field needs fewer
  exposures and so has fewer links to get wrong — the chain came out complete on 92% of spines with a
  collimated field, 96% with a 9-inch and 99% with a 12-inch — while a tighter field gives more frames and
  more overlap. Use what you would have used.

## The sweep, step by step

**1. Find the landmark and put it at the edge of the field.**

- *Lumbar or thoracolumbar work:* the sacrum. Position so the S1 body and the sacral promontory sit at the
  **bottom** of the field. This is frame 1.
- *Cervical or upper thoracic work:* C2. Position so the odontoid and the C2 body sit at the **top** of the
  field. This is frame 1, and the sweep runs downward instead of upward.

**2. Expose. Save the image. Do not move the table.**

**3. Move one field, minus two vertebrae.**

Move the C-arm toward the level of interest by a little less than the height of the field: leave **two
vertebral bodies of the previous picture still in view**. That overlap is what lets the software know the two
pictures are of the same spine, and two is the measured optimum — one body loses two points of chain
completeness, half a body loses sixteen, three bodies loses seven and four loses fifteen, because every
extra exposure is another link that can be joined wrongly. Roughly:

| Detector | Field at the spine | Move by about | Vertebrae in view |
|---|---|---|---|
| 9-inch image intensifier | 14 cm | 7 cm | 4 lumbar |
| 12-inch image intensifier | 19 cm | 12 cm | 5–6 lumbar |
| 30 cm flat panel | 20 cm | 13 cm | 6 lumbar |
| collimated field | 10 cm | 3 cm | 3 lumbar |

Erring toward **more** overlap is safe; erring toward less is not. The software can sometimes link two
pictures that share no whole vertebra, from the partial bodies at the edges — but that is the case a small
patient movement or a change in C-arm angle breaks, and it will not tell you it was working from scraps.
Leave a body in view.

**4. Expose. Save. Repeat step 3** until the level of interest is in the field.

**5. Stop.** You do not have to sweep the whole spine. Sweep from the landmark to where you are working. For
most lumbar cases that is three or four exposures; for a mid-thoracic case from the sacrum it is six or
seven.

**The last move is a full move or none.** If the level of interest comes into the field after a full
step, stop there; do not take an extra exposure a little higher to centre it. A final frame that moves
less than half a vertebra is nearly the same picture twice, and the software cannot tell such a step from
one a whole body longer. In testing every incomplete chain at two bodies of overlap was that frame: refusing
it, or telling the software the last step may be short, completed 120 of 120 sweeps.

## What the software gives back

- A stitched picture of the whole swept segment, with every vertebra boxed and named.
- Two readings of those names: one by **counting** from the landmark, one by the **shape** of the bones. When
  they agree, the naming is settled. When they disagree, that disagreement is the flag for transitional
  anatomy — a sixth lumbar vertebra, or a thirteenth rib-bearing level — and it is displayed, not hidden.
- For each later spot image: where it sits on the map and what its vertebrae are called, or an explicit
  **"cannot place this image"**.

## When it declines, and what to do

The system declines rather than guess in three situations. In each, the remedy is one more exposure, not a
different button.

1. **A link is uncertain** — two consecutive frames did not share enough structure. *Repeat the last frame
   with more overlap.*
2. **A spot image will not place** — it is too far from anything in the sweep, or the anatomy has moved.
   *Take one frame that includes part of the sweep and part of the current field.*
3. **The naming is low-confidence** — usually a transitional spine. *Sweep the rest of the way to the
   landmark at the other end, or accept that the level is to be confirmed by count.*

## Why the landmark, and why the overlap

The spine is nearly periodic: one lumbar vertebra looks much like the next. That is why a single spot image
cannot be named reliably, and why counting from a landmark is the standard of care. The sacrum and C2 are the
only two places where the pattern breaks unmistakably.

The overlap is what turns a pile of pictures into one map. With a vertebra shared between neighbours, the
software can prove that the fourth body of one picture is the first body of the next. Without it, it can only
guess, and a one-vertebra guess is exactly the error that causes wrong-level surgery.

## What is measured, and what is not

On CT scans rendered as radiographs and swept as above, at a 9-inch field, each frame independently degraded
to look like a separate exposure:

On 120 abdominopelvic scans (sacrum to about T10) that the naming model had never seen, with two bodies of
overlap and the step jittered by ±0.3 body around the instruction above:

- the chain of vertebrae came out complete on **97.5%** of spines, from a mean of 3.4 frames, and on
  **100%** once the final short move was handled as the rule above says;
- a spot image showing two vertebrae was named correctly **72%** of the time on its own pixels and **95%**
  when matched onto the sweep; three vertebrae, 87% and 95%; four, 90% and 95%;
- a spot image showing three vertebrae was named correctly **99.5% of the time on the 80% of images** the
  software was most confident about, the rest declined; at four vertebrae, 98% on 80%.

The same 120 scans swept exactly as step 3 says — a fixed move of one field minus two bodies, no jitter,
last move a full move or none — gave a complete chain on **120 of 120** spines and named a two-, three-
and four-vertebra spot image on the sweep **95%, 96% and 94%** of the time. The instruction on this page
is the protocol that was measured. (An earlier version of these numbers was on renders whose field was
7.5% too large at the median, from a wrong voxel spacing; they were withdrawn and re-measured.)

On 25 real lumbar radiographs the model had never seen, every chain came out complete, and a two-vertebra
spot image went from **79%** on its own pixels to **94%** on the sweep; four vertebrae, 92% to 100%.

On 12 whole-spine scans the model had never seen, swept downward from C2 — the thoracic spine, where
counting by eye is hardest — from a mean of 2.9 frames:

- the chain came out complete on **every** spine;
- a two-vertebra spot image went from **10%** on its own pixels to **100%** matched onto the sweep, and a
  three-vertebra one from **25%** to **100%**, with nothing declined.

Twelve is few, and the direction, not the value, is what that arm establishes.

On 522 routine clinical CTs from another institution (TotalSegmentator's public release), which no model
here was trained on, the protocol as written on this page — fixed step, last move a full move or none —
gave a complete chain on **98.5%** of spines from 4.2 exposures and named a two-, three- and four-vertebra
spot image on the sweep **94%, 95% and 94%** of the time, from 51%, 73% and 83% on its own pixels; those
frames are mostly thoracic. Swept downward from C2 on 203 scans that hold it, **95%** of chains completed
from 2.8 exposures and a two-vertebra spot image went from **19%** to **94%**. Only one transitional spine
survives that holdout, so nothing is claimed about transitional anatomy from the C2 sweep. Larger figures
were reported earlier from 801, 170 and 76 spines; most of those spines were ones the model had been
trained on, and those figures were withdrawn.

Not yet measured: sweeps on real patients, parallax between exposures taken at different C-arm positions, and
patient motion during a sweep. All three make the *linking* harder and none changes the naming, but none has
been measured, and until it has, the counts on the screen are to be treated as a second opinion and not as a
substitute for your own.
