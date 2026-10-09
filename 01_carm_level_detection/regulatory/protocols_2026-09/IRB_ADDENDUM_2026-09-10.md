# IRB addendum — commercial track

Companion to `COMMERCIALIZATION.md`. **Gitignored. Does not go in the repository, the
eProtocol cover sheets that get shared, or any student-facing document.**

Status: draft, 2026-09-10. Not legal advice. Every item needs confirmation from the IRB
office (Andreea Geamanu) and from a startup IP attorney before it is relied on.

---

## The one-sentence problem

`proposals/irb/IRB_PLAN.md` writes Protocol 1's release language as *"de-identified images
and labels may be shared under a restricted data use agreement and model weights may be
released, each after a WSU determination."* That is a **research** release path. It gives
the commercial track nothing, and — worse — it sets the approved purpose in a way that
makes later commercial use a use outside the protocol.

An IRB cannot grant a commercial licence to DMC/Tenet data. That is a **data use agreement
negotiated with DMC/Tenet legal**, on a parallel track, starting now. The IRB will not wait
for it and will not produce it.

## The asymmetry that governs every edit below

| where | commercial intent |
|---|---|
| the eProtocol submitted to WSU/DMC | **must be disclosed** — this is the regulatory requirement, and non-public |
| the COI disclosure | **must be disclosed**, and must be accurate on the date it is signed |
| `proposals/irb/*` in the repository | **never** — public on two GitHub remotes |
| the manuscript, README, student docs, grant text | **never** |

IRBs approve commercially-motivated research constantly. What they sanction is undisclosed
conversion after the fact. Disclosing now is cheaper than amending later, and an amendment
after a finding is worse than either.

---

## Edit 1 — Protocol 1 permitted uses

Add to the Confidentiality/HIPAA and Purpose sections, in the eProtocol only:

> Data collected under this protocol may be used for the development, training, testing and
> validation of computational methods and software, including software that may
> subsequently be commercialised or submitted for regulatory clearance. De-identified
> images and derived labels may be shared under a restricted data use agreement, and model
> weights may be released, each after a Wayne State University determination. Any transfer
> of data or derived artifacts to a commercial entity will be governed by a separate data
> use agreement executed with the covered entity, and is not authorised by this protocol
> alone.

The last sentence is the important one. It tells the IRB the commercial path exists, and
tells it the IRB is not the body authorising that path — which is both true and what keeps
the review simple.

## Edit 2 — the DUA is a parallel track

Not an IRB item at all; add to the week-one list:

- Ask Dr. Montie who at DMC/Tenet executes data use agreements for research data with
  downstream commercial rights, and open that conversation the same week the protocols go
  in. Expect legal, not research administration.
- What to ask for, in order of decreasing likelihood: an exclusive perpetual licence to
  de-identified derived data for commercial use; a non-exclusive perpetual licence; a
  licence limited to models trained on the data rather than the data itself.
- Title is not the goal. Functional control is.

## Edit 3 — a third protocol for intraoperative fluoroscopy

`COMMERCIALIZATION.md` §6 calls route 3 the differentiated asset, correctly: intraoperative
C-arm fluoroscopy during instrumentation largely never reaches PACS, so no vendor can sell
it. There is currently **no protocol for it**. Protocol 2 as drafted is silent evaluation
on incoming trauma imaging, which is Product A validation.

Submit a Protocol 3 with the other two:

- **Design.** Prospective capture, nested in existing care. Patients already undergoing
  instrumented spine surgery; images already being acquired for the operation.
- **Risk.** Zero incremental radiation — no additional exposures are ordered. Minimal risk.
  Expedited category 5 (existing data/records) if capture is from the device's own archive,
  or category 4/5 depending on how the export works.
- **Consent.** Waiver, on the same grounds as Protocol 1, if capture is passive and the
  images are de-identified. If the OR workflow requires anything of the patient, it is not
  passive and the waiver argument fails.
- **Ground truth is free.** The operative note and postoperative imaging state which level
  was instrumented. Radiologist adjudication is needed only for LSTV/Castellvi, where
  expert judgment is genuinely required.
- **Longest lead time of the three.** Surgeon buy-in, OR workflow, and getting images off
  the C-arm are all slower than the IRB. Start it first, not last.

## Edit 4 — sequence the provisional and the COI

Order matters, and the current plan has no order:

1. File the provisional **before or at** protocol submission. Micro-entity, ~$65–130. Its
   value is dated corroboration of conception, not a moat — `COMMERCIALIZATION.md` already
   ranks patents last and that ranking is right.
2. Disclose the financial interest in the COI at submission, so the disclosure is accurate
   on the day it is signed.
3. If an entity is formed while a protocol is pending, that is a COI amendment, not a
   silent change.

**The disclosure clock is the item with a real deadline.** Earliest enabling public
disclosure appears to be the AACA Tech Fair, June 2026. The US grace period therefore
expires around **June 2027**, and ex-US absolute novelty is likely already spent. Get the
exact date of the earliest enabling disclosure — the 12 CNS abstracts, the AACA Tech Fair,
NeurIPS #3474 OpenReview visibility — and put it at the top of the action list as a date.

## Edit 5 — what stays out, and why that is still right

`IRB_PLAN.md`'s "Kept out on purpose" section excludes anything shown to a treating
clinician, any change to care, and any patient contact. That is correct and should stay:
it is what keeps Protocols 1 and 2 exempt and expedited.

It is also the FDA evidence gap, and the gap needs its own plan. A 510(k) wants standalone
performance plus a multi-reader multi-case study. The readers are the subjects in an MRMC
study, not the patients, which is usually an easier review than people expect. That is a
fourth protocol, later, and it should not be folded into these.

---

## What I did not change and why

Nothing in `proposals/irb/`. Those files are already public on `origin` and `osc`, and the
commercial framing must not be added to them. Separately, they carry eight named DMC/WSU
staff with work email addresses and internal read-outs of the review process; that is worth
removing from the public repository on its own merits, independent of anything here.
