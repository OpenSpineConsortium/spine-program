# Confidential memorandum: publication timing and prior public availability

**For patent counsel only. Attorney work-product material. Not part of any filing.**

Not legal advice. This sets down facts an attorney needs in order to advise, and separates what is
established from what is not. It accompanies `INVENTION_DISCLOSURE.md` and does not travel with it.

---

## 1. Why this memorandum exists

37 CFR 1.56 imposes a duty of candour on everyone substantively involved in prosecution. A patent obtained
while a known disclosure was withheld can be held unenforceable in its entirety. The facts below are recorded
so counsel can decide what, if anything, must be cited — a decision that is counsel's and not the inventor's.

The favourable frame, stated once: under 35 U.S.C. §102(b)(1) an inventor's own disclosure within the
preceding year is **not** a bar in the United States. A filing made now is unaffected domestically by
anything below. The exposure question bears on EP/JP/CN, which have no grace period.

## 2. What was publicly reachable, and when

Observed by uncredentialed request at **2026-09-18T20:40:37Z**. Closed at **2026-09-18T20:42:16Z**.
Closure verified the only way that counts — an anonymous request now returns HTTP 401.

| Surface | Created | Anonymous status when observed |
|---|---|---|
| `anonymous-mlhc/CTSpinoPelvic1K-review-spine` | 2026-06-21 | **public**; `app.py` HTTP 200 |
| `anonymous-mlhc/CTSpinoPelvic1K-review-ribs` | 2026-06-21 | **public**; `app.py` HTTP 200 |
| `gregoryschwingmdphd/CTSpinoPelvic1K-review` | 2026-05-26 | **public**; `app.py`, `carm.py`, `viewport.py` HTTP 200 |

Confirmed **not** reachable at the same observation: both GitHub repositories (HTTP 404 anonymously — which
cannot distinguish private from absent), all four private dataset repositories including the model weights,
and the inference endpoint `level-id.openspineconsortium.org`.

The exposed bytes are preserved with SHA-256 in `docs/disclosure_evidence/`, together with the API metadata
captured while the Spaces were still open. Visibility was changed; **nothing was deleted**, deliberately,
since deletion would destroy the record.

## 3. What the exposed text contains, element by element

This is the question that decides the matter, and it precedes any argument about accessibility. A keyword
scan is not evidence; what governs is whether a person skilled in the art could practise a claim from the
text.

| Aspect put forward | Present in the exposed text? |
|---|---|
| A — acquisition chain: overlap, linking rule, similarity search, frame-to-chain registration | **absent** |
| B — determining level in fewer exposures | **absent** |
| D — computation without the imaging leaving the room | **absent** |
| E — persistent digital marker and its propagation | **absent** |
| model weights, architecture, training procedure | **absent** |
| C — monotone consecutive-run decode | **concept stated in one sentence**; no implementation |
| C — a supernumerary segment changes the alphabet rather than the offset | **concept stated in one sentence**; no implementation |

The two sentences, verbatim:

> "When it is wrong it is almost always wrong by an OFFSET … and almost never scrambled, because the decode
> is monotone by construction."
>
> "An offset cannot express a spine with six lumbar vertebrae or thirteen rib-bearing levels. Those change
> the alphabet itself."

The same file states, contemporaneously:

> "This file is a user interface: it contains no model, no weights and no naming algorithm, only a form over
> a manifest."

**The lead aspect (A) is untouched.** No scoring function, alphabet construction or landmark constraint
appears anywhere in the exposed text.

## 4. Assessment, for counsel to test

Anticipation requires every element of a claim, arranged as in the claim, and enabled. A sentence stating
that a supernumerary segment changes the alphabet does not anticipate a claim to candidate namings scored
against alternative alphabets with a declared landmark pinning one end of a contiguous run. The realistic
question is §103 obviousness, and only as to aspect C.

On accessibility, should it be reached: *SRI International v. Internet Security Systems* (Fed. Cir. 2008)
held a paper on a public FTP server for seven days **not** a printed publication, absent indexing,
cataloguing, or evidence that a skilled person would have located it. The distinguishing fact here is that
HuggingFace indexes and search-ranks Spaces. Against that: these Spaces are named for a CT dataset review
task, under an organisation name unrelated to level identification, and nothing indicates any access. This is
an evidentiary question, not a settled one.

## 5. Established by third-party records

Three questions were open. All three are now answered, from append-only records outside anyone's control
here, on **2026-09-18T21:01Z**. Method and raw results: `tools/disclosure_forensics.py`,
`docs/disclosure_forensics.json`.

### 5.1 The method was never in a public repository

GitHub emits an event into a user's **public** event stream for every push to a **public** repository. The
retained window at the time of checking was **2026-09-07T15:43Z to 2026-09-15T05:51Z**, containing 96 events,
of which 92 were pushes:

| repository appearing in the public stream | events |
|---|---|
| `Gregory-Schwing-MD-PhD/CTSpinoPelvic1K` | 38 |
| `OpenSpineConsortium/CTSpinoPelvic1K` | 35 |
| `OpenSpineConsortium/openspineconsortium.github.io` | 9 |
| `Gregory-Schwing-MD-PhD/OpenSpineToolkit` | 7 |
| `OpenSpineConsortium/OpenSpineToolkit` | 3 |
| others | 4 |
| **`spinesurg-ct-nnunet`** | **0** |

The method repository received pushes throughout 14 September (the last at 17:53:52 local) and again from
00:31:17 on 15 September. **None of them appears in the public stream, while pushes to five other
repositories of the same account in the same period do.** A public repository's pushes are emitted; a private
repository's are not. The repository was therefore private for the whole window, from **at least 2026-09-07**
— earlier than the 14 September date the earlier document asserted, and the assertion is now superseded by
evidence rather than resting on prose.

The sweep method's first commit is **2026-09-17T22:11:18 EDT**, after that window, and the repository is
private now (anonymous HTTP 404). No public event of any kind was emitted by this account after
2026-09-15T05:51Z, which is consistent with subsequent work being private.

Neither repository URL has ever been captured by the Internet Archive.

**Conclusion: the method was never in a public repository.** The window does not extend before 7 September,
but the method did not exist before 17 September, so that gap is immaterial.

### 5.2 The inference endpoint was never live

**No TLS certificate has ever been issued for `level-id.openspineconsortium.org`, nor for
`openspineconsortium.org` at all.** Certificate Transparency logs record issuance by the certificate
authority, are append-only, and cannot be retracted by a site operator. Four certificates exist, all for
`openspineconsortium.com` and `www.openspineconsortium.com` (2026-06-21 and 2026-08-20 issuances).

An HTTPS endpoint cannot serve without a certificate. The hostname hard-coded in the public `remote.js` was
therefore **aspirational and never served**. It is also unreachable now, and the Internet Archive holds no
capture of it.

This is the strongest of the three findings: absence from Certificate Transparency is meaningful in a way
that absence from a crawl index is not.

### 5.3 The project page was never published

The public website repository was fetched and compared against its remote (195 commits, local and remote
identical). Across its **entire history**, zero objects match `rsnai`, `paper/`, `sweep`, `level-id` or
`onnx`. The Internet Archive holds no capture of any `paper/` or `rsnai/` path on either domain.

`paper/rsnai/web/index.html` — which does describe the method in full, including the overlap parameter and
the measured results — exists only in the private repository. **It was never published.**

The same search resolves a separate question in the project's favour: the corner-detector ONNX weights served
from the website between approximately 2026-08-09 and 2026-09-14 were **never committed** to the repository,
so they are not in its public history. An earlier project note stating they "remain in the site's public git
history until that history is rewritten" is incorrect. In any case that detector is a single-class vertebra
corner finder that names nothing.

### 5.4 What remains unverified

The account's own audit log has still not been exported, and remains the only first-party record. The
evidence above is third-party and circumstantial, but it is independent of this project and, in the case of
Certificate Transparency, cannot be altered retroactively. Exporting the audit log would convert 5.1 from a
strong inference into a direct record, and is worth doing before filing.

## 6. Other public artefacts, assessed

- **The public website and viewer.** Its published source states the detector "finds vertebrae; it does not
  name them," and the level assignment visible in public code is a trivial sort-and-count. No aspect above is
  disclosed.
- **The CT dataset (HuggingFace, Zenodo DOI).** Volumes and labels. Contains no method.
- **Conference material.** Reviewed; the posters and presentations concern CT morphometry and spine MRI, not
  level identification from radiographs.

## 7. Recommended sequence

1. Export the GitHub audit log, to convert §5.1 from inference to record.
2. File the provisional **before** the manuscript is submitted. The manuscript is complete and held for this
   purpose; it is the one unambiguously enabling disclosure in existence and it is not yet public.
4. Counsel determines what is cited in the Information Disclosure Statement at the non-provisional stage. The
   provisional itself contains no representation as to prior disclosure.

## 8. One item requiring a decision

The manuscript's title page carries a conflict-of-interest declaration stating a commercial interest in a
level-confirmation product. It is a journal requirement and should not be removed. It is also a public
statement made before filing, and counsel should see it before submission.
