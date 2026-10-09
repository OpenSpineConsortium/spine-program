# The consortium mark

Two sets of files, both copied on 2026-10-08 (`../../MANIFEST_LOCAL.md` records the source of each):

- `assets/`: the generator `osc_logo.py`, the vector `osc_logo.svg` and six PNG renders (40, 64, 256, 512, 1024 px and a
  preview). Tracked in the public repository `CTSpinoPelvic1K` under `assets/` since commit 7af09ed ("a mark for the
  consortium that survives being 40 pixels wide"; repository head 7ddfe38 on 2026-10-08). The docstring of `osc_logo.py`
  records the design: a lumbar column with one vertebra picked out in gold, the identified level known without the
  count; two colours and one accent, no gradients, no thin strokes, because a Zenodo community avatar is seen at about
  40 px. Regenerate with `python osc_logo.py` (matplotlib; see its argument parser).
- `OpenSpineConsortium-logo/`: ten renders dated 2026-09-28 (128, 256 and 512 px; plain, white, inverse and flat
  variants; PNG and JPG). Which script produced them is not recorded; they are the renders the Beethoven pages and store
  listing use (the inventory of the other spine folders, 2026-10-08).

The site's own copies live in `assets/` of the website repository and are stamped by the build. Edit the generator, not
a render.
