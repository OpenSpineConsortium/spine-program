# The title

**SchwingNet: a convolutional-recurrent network for level naming in spine surgery**

In the double-anonymized review copy the same title prints as

**[AuthorLastName]-Net: a convolutional-recurrent network for level naming in spine surgery**

Set 2026-09-24 ~22:15 by Greg: "If it's not robust to transitional anatomy, then it should be removed from the title".
The clause went the way of the comparison clause; both belong to paper 2. The 2026-09-24 evening title is kept below as record.

~~SchwingNet: a convolutional-recurrent network for level naming in spine surgery, robust to transitional anatomy~~

Set 2026-09-24 (evening) when Greg moved the comparison with registration-assisted neurosurgeons into a second
paper ("I'd like to move the comparison to neurosurgeons / all the LevelCheck stuff into a new paper, remove it from
the current paper"; `REVISION_LOG3.md` section 8, `PAPER1_SCOPE.md`). The clause "versus registration-assisted
neurosurgeons" went with the comparison (`paper2_levelcheck/MOVED_FROM_PAPER1.md` item 7). The title fixed by Greg
on 2026-09-23 was:

> SchwingNet: a convolutional-recurrent network for level naming in spine surgery, robust to transitional anatomy,
> versus registration-assisted neurosurgeons

and is the natural title of paper 2's comparison. Whether "robust to transitional anatomy" stays in paper 1's title
is Greg's decision: `CLAIMS_LEDGER.md` records it as resting on the embedding (selection split) and the coupled
alphabets, with three real cross-validation patients; the restructure did not change that evidence.

## Rules for every agent and every pass (2026-09-25: ANONYMISED-VARIANT = yes, by one programmatic flag)

- The network is named **SchwingNet** in the title, the abstract, the key points, the figures and the released
  weights. This is the author's decision and is not open to rewriting.
- `Radiology: Artificial Intelligence` reviews double-anonymized, and a network named after the author is an
  identity signal. Greg (2026-09-25): the review copy carries the journal's placeholder, and the two copies come
  from ONE source through ONE flag:
  - `rsnastyle.tex` defines `\newif\ifcameraready`, FALSE by default (= the review copy), and inputs
    `cameraready.flag.tex` (`\camerareadytrue`) when it exists. Only `slurm/compile.sh` writes that file, when it
    runs with the environment variable `CAMERAREADY=1` (`sbatch --export=ALL,CAMERAREADY=1`); it removes it otherwise.
  - The name is **never typed in the tex** (comments excepted). `\netname{}` prints `SchwingNet` in the camera-ready
    copy and exactly `[AuthorLastName]-Net` in the review copy. `\withheldurl{url}` prints the URL or
    `[URL withheld for review]`. `\selfcite{key}` prints `\citep{key}` or `[reference withheld for review]`, and in
    review mode the entry is not cited at all, so it leaves the reference list and the numbering stays consecutive.
    The self-citations are `ctsp1k` (the CTSpinoPelvic1K Zenodo record) and `ctsp1kdescriptor` (its arXiv
    descriptor); both name the author and both are `\selfcite`. Public third-party dataset URLs and DOIs may stay
    bare. Today the manuscript body carries no URL at all (the Code and model availability statement names a private
    repository without an address), so `\withheldurl` has no use yet; it is the macro any address must go through.
  - Figures: the ten figure scripts take the name from the environment variable `NETNAME` (default `SchwingNet`)
    wherever they write it; text extraction of every figure PDF on 2026-09-25 found the name in none of them (only
    `figure3.caption.txt` and the `record.json` files carry it), so no review rendering was needed.
    `rsnaresults.sty`'s `\RESULTFIG` draws `figures/review/<file>` in review mode when that file exists and the
    camera-ready file otherwise; `tools/check_limits.py` lists which review files are absent and fails if the file
    drawn carries the name.
  - `tools/check_limits.py` measures the copy the environment selects (default review; `CAMERAREADY=1` camera-ready),
    prints the other copy's counts beside it, and always fails if the review tex, the fetched review PDFs
    (`packet_build/review/`) or the drawn figures contain `SchwingNet`, `Wayne State`, the surname or an unwrapped
    URL or identifier of the authors' repositories. `tools/make_packet.py` builds the review packet (`packet/`) by
    default and the camera-ready packet (`packet_cameraready/`) with `CAMERAREADY=1`; its anonymization grep no
    longer allows the name.
- Everywhere outside the anonymized manuscript file — the full title page, the cover letter, the preprint, the
  released weights, the model card, ERAS — the name is **SchwingNet**.

ERAS entry (Peer Reviewed Journal Articles/Abstracts, other than published):

> Schwing G. SchwingNet: a convolutional-recurrent network for level naming in spine surgery. *Radiology: Artificial Intelligence*. Submitted
> September 2026.
