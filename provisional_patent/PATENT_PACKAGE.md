# Patent package — superseded

This document has been split in two, because it mixed a technical disclosure with a record of public
availability, and those two things go to different readers for different purposes.

| Document | For | Contains |
|---|---|---|
| **[`INVENTION_DISCLOSURE.md`](INVENTION_DISCLOSURE.md)** | technology transfer office and patent counsel | the invention, the five aspects put forward with their mechanisms, claim scope, subject-matter eligibility strategy, freedom to operate, novelty over the literature, and what a provisional must contain |
| **[`DISCLOSURE_MEMO.md`](DISCLOSURE_MEMO.md)** | patent counsel only | publication timing and prior public availability, element by element, with what is established and what is not |

A provisional application is a technical specification and contains no representation about prior
disclosure, so the two documents do not need to travel together. The memorandum exists because counsel
cannot advise without it.

---

## Corrections this supersedes

Three statements in the earlier version were wrong and are corrected in the split documents. They are
recorded here rather than quietly dropped.

**"US 8,718,346 is not cleared."** It is NuVasive, originally Saferay Spine, and its four independent claims
require either a previously-acquired baseline image digitally manipulated into a set of permutations in 4D or
6D space, or a tracking device monitoring the imaging device's position. We produce no permuted baseline set
and use no tracker. It is clear, and it expires 2031-10-05.

**"The review Spaces are public but not enabling — they display a label, not the method."** That was read off
intent rather than off the API. The deploy script uploads `app.py` verbatim and it was readable
uncredentialed. What it contains is still thin — two concept sentences, no algorithm, no weights, and nothing
of the acquisition chain — but "not enabling" was a conclusion reached without checking.

**"The clock has not started; nothing public discloses the method."** All three Spaces were serving
`private: false` at the moment of checking on 2026-09-18, not during an eight-hour window as recorded. They
are now private, verified by anonymous HTTP 401. The element-by-element assessment is in the memorandum.

A fourth item was not wrong but was unsourced, and is flagged as such: the date the main repository changed
visibility rests on prose alone. GitHub's audit log is the only authoritative record and the §102(a)(1)
analysis turns on it.

---

## Standing instruction

`tools/disclosure_audit.py` re-runs the whole public-surface check anonymously and closes what it finds, with
verification. Run it before any submission, talk or release. A prose inventory of what is public is worth
nothing; a query is worth something.
