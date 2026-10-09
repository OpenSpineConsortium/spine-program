# Seven cases for ITK-SNAP

Load the CT as the main image, `*_label.nii.gz` as segmentation, and
**`itksnap_v5_labels.txt`** as the label descriptor
(`Segmentation > Import Label Descriptions`).

Use the v5 descriptor, not the v4 one on the grid. v4 has no entry for ids 74/75, so the
lumbar-rib class renders as Clear Label and you would look straight past the structure
these cases are about. In v5 it is teal — deliberately outside the rib colour ramp, so a
13th rib reads as a different *kind* of structure rather than one more rib in the run.

Label ids you will want: `74` rib_left_lumbar · `75` rib_right_lumbar · ribs `34–45` left
1–12 and `46–57` right 1–12 · `8–19` T1–T12 · `20–25` L1–L6 · `26` sacrum · `29` S1.

The house rule everything below is measured against: **anchor at S1, count up; a rib is
named for the vertebra it articulates with; a rib never renames a vertebra.**

---

## 0008 — does this case have a lumbar rib, or a sacralized L5?

The one that matters most, because we already changed it.

The manifest labels it `SACRALIZATION`, and it is the **only case of the fourteen where
the two readers disagreed** (`lstv_agreement: false`). We reclassed its 12th rib pair to
74/75 and shifted the rest `+1`, on the reading that the rib sits on L1.

If instead L5 is sacralized, the count from the sacrum is shifted by one, that body is
**T12**, its "lumbar rib" is an ordinary T12 rib, and our edit is wrong.

Tell them apart on the sacrum, not the count: four anterior foramina pairs is a normal
sacrum, five means it absorbed L5. Its sacrum also measures 182 mm tall against a cohort
range of roughly 131–166, which is suggestive but not decisive.

Original preserved at `qc_rib_incidence_v5_fixed/pre_rib_review/0008_label.nii.gz` on the
grid — say the word and I revert.

## 0344 — what are ribs 6 and 7 actually attached to?

Left ribs **6 and 7** are recorded as reaching **L3 and L5**. A 6th rib cannot reach L3,
so this is not a numbering error and no renumber can fix it. Expect either a grossly
mislabelled structure or a displaced fragment carrying a rib id.

The only case still counted as an unclassed lumbar-rib case in the final QC.

## 0389 and 0720 — is the rib above the L1 rib really on T12?

Both end with **no rib 12 at all**. Their 13th rib was correctly moved to 74/75, but
neither has a single labelled thoracic vertebra anywhere in the volume, so nothing could
anchor the renumber and the script declined rather than guessed.

Rib order alone would fix both — the rib above an L1 rib is on T12 — but that inference
assumes the body carrying the lumbar rib really is L1. Same question as 0008.

**0720 also has an unresolved left side**: its left rib 12 points at L1 but sits beyond
the 15 mm contact threshold, so it was never reclassed. Either the case is bilateral and
the left rib is under-segmented, or that left rib 12 is a fragment.

## 0179 and 0412 — which ribs are miscounted, and by how much?

Both cages **disagree with themselves**: offsets of −1 *and* −2 on the same case, so no
single shift satisfies the rule and both were left alone.

On 0179 the whole cage reads one level low, nothing is correct, T12 carries no rib, and
**T5/T6 are stacked at the FOV edge** — which is probably what produced the −2s. The real
question is whether this is a rib-less T12 or a 12th rib that TotalSegmentator counted
from a cervical rib.

## 1153 — reannotate

Right cage is fragmented into speckle across ribs 8–11; left ribs 11 and 12 are noise
blobs near L1. T6/T7 also stacked at the FOV edge. Not a numbering problem — the
segmentation itself needs redoing.

---

## What to write down

For 0008, 0389 and 0720 the single most useful output is: **how many anterior sacral
foramina pairs, and is the lowest rib-bearing body L1 or T12?** Those two answers settle
whether the lumbar-rib class was applied correctly and whether the ordering inference is
safe to run on the remaining two.
