# Provisional application package

**Not legal advice. Nothing here is filed until counsel has reviewed it.** This folder is what an attorney
needs in order to draft and file a provisional application under 35 U.S.C. §111(b), assembled so that the
engineering content is complete and the claims it must support are written down.

| file | what it is | who it goes to |
|---|---|---|
| `SPECIFICATION.md` | the technical disclosure, written to enable | filed (reformatted by counsel) |
| `CLAIMS.md` | what will be claimed in twelve months, each limitation pointed at its support | **not filed**; a check that the specification enables enough |
| `COVER_SHEET.md` | the data for form SB/16 | filed |
| `FILING_CHECKLIST.md` | what must happen, in order | internal |
| `../INVENTION_DISCLOSURE.md` | the same invention for the technology transfer office, with freedom-to-operate and the §101 strategy | tech transfer + counsel |
| `../DISCLOSURE_MEMO.md` | publication timing and prior public availability | **counsel only**; does not travel with the rest |

---

## The one question this package is built around

A provisional is worth exactly what its specification enables. A placeholder that names an idea supports
nothing, and the priority date it appears to secure evaporates when the non-provisional claims are tested
against it. So the specification is written as disclosure rather than assembled as a reading list, and
`CLAIMS.md` exists to check that every limitation anyone will want in twelve months has a paragraph behind
it.

## What is built, and what is only described

This distinction is load-bearing and is marked in both documents. A provisional that overstates what exists
is worse than one that is narrow.

**Implemented, exercised end to end, and unit-tested.** The acquisition protocol and its overlap parameter;
recovery of physical scale from the subject's own vertebrae; repair of detected positions from local
spacing; linking with its asymmetric window, anisotropic tolerance and robust block scoring; the chain and
its margin; the alternative-alphabet decode; the two-term confidence; the commanded displacement in both
forms, including its direction at an ambiguous link, its bounding short of a re-acquisition, and its
derivation from measurement rather than accumulation; determination of the column's direction from the
landmark and transformation of the displacement into the device's axes; selection of which landmark to run
from and the exposures that implies; registration of a later image onto the chain; the marker, its
propagation, its retention on refusal, and the margin condition under which a position is asserted.

**Measured on 801 subjects (CT renders).** The naming results, and the overlap relationship.

**Measured on a synthetic subject only** — and labelled as such in both documents: the geometry recovery
(1.2 mm) and the marker results. The corresponding measurement on the render corpus is running; see
`docs/GUIDED_ACQUISITION.md`.

**Not measured, and no representation is made.** The latency of the linking, composition and registration
stages — two networks are timed, the machinery that distinguishes this work is not. Anything on real
intraoperative fluoroscopy. Transfer of the geometric threshold from renders to film.

## Reading order for counsel

1. `../DISCLOSURE_MEMO.md` — first, because it bears on when anything else may go out.
2. `SPECIFICATION.md` §§I–XIII.
3. `CLAIMS.md`, then back to the specification for any limitation whose support looks thin.
4. `../INVENTION_DISCLOSURE.md` §5 (§101 strategy) and §6 (freedom to operate).
5. `FILING_CHECKLIST.md`.

## Where the implementation is

| | |
|---|---|
| `tools/sweep_map.py` | linking, chain, alphabets, panorama, query registration |
| `tools/acquisition.py` | the confidence, the commanded displacement, the orientation, the marker |
| `tools/validate_guided.py`, `slurm/guided_validate.sh` | the closed-loop measurement |
| `tools/guided_console.py` | one image in, one instruction out |
| `tests/test_acquisition.py` | the phantom and the checks |
| `docs/GUIDED_ACQUISITION.md` | what it does, how to run it, and what is open |
| `README.md` | the measured results the specification cites |

## Figures

The specification references FIG. 1–13 and describes what each must show ([0015]–[0025b]). They have not
been drawn. A provisional may be filed with informal drawings, and the brief descriptions are written so a
draftsman can work from them. **Do not file without them where a figure carries a limitation** — in
particular FIG. 4 (linking), FIG. 6 (alternative alphabets), FIG. 7 (the confidence and the commanded
displacement), FIG. 9 (marker propagation), FIG. 12 (direction of the column) and FIG. 13 (displacement
toward an ambiguous link).
