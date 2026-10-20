# Filing checklist

**Not legal advice.** Counsel decides all of this; the list exists so nothing is forgotten and so the order
is deliberate.

---

## Before anything leaves this repository

- [ ] **Export the GitHub audit log** for `Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` and extract the
      visibility-change timestamp. `../DISCLOSURE_MEMO.md` §5.1 establishes this by third-party inference —
      the account's own public event stream carries pushes to five other repositories in the window and none
      to this one — and the audit log converts that inference into a first-party record. This is the single
      most useful remaining fact.
- [ ] Counsel reads `../DISCLOSURE_MEMO.md` **before** `SPECIFICATION.md`, because it bears on timing.
- [ ] Counsel sees the manuscript's conflict-of-interest declaration, which is required by the journal and
      is also a public statement made before filing.

## Required by 37 CFR 1.51(c)

- [ ] **Specification** — `SPECIFICATION.md`, reformatted. No claims required.
- [ ] **Drawings** where necessary to understand (35 U.S.C. §113). Informal drawings are acceptable. See
      `README.md`; six figures carry limitations and should not be omitted.
- [ ] **Cover sheet** — form SB/16, data in `COVER_SHEET.md`.
- [ ] **Fee.** Verify the current micro- or small-entity fee; a university assignee is ordinarily a small
      entity, and micro-entity status has its own conditions counsel must confirm.
- [ ] **Application Data Sheet** if counsel prefers it to the cover sheet.

## Sequence

| when | step |
|---|---|
| now | invention disclosure to WSU technology transfer; engage counsel |
| before anything public | **file the provisional** |
| then | release the manuscript for submission |
| ≤ 12 months | non-provisional + PCT |
| 30 months from priority | national phase |

**The manuscript is held until the provisional is on file.** It is the one unambiguously enabling disclosure
in existence and it is not yet public. In the United States §102(b)(1) gives a twelve-month grace period for
the inventor's own disclosure; EP, JP and CN give none, so those rights turn on filing first.

## Things that must not happen before filing

- [ ] No preprint, no conference abstract, no poster, no talk describing the method.
- [ ] No repository made public. Every surface was closed on 2026-09-18 and verified anonymously; keep it so.
- [ ] No demonstration to anyone outside a confidentiality obligation.
- [ ] No weights served from anywhere.

## Within the twelve months

- [ ] **Commission the INPADOC family sweep** for continuations and divisionals of the four patents in
      `../INVENTION_DISCLOSURE.md` §6. A continuation with broader claims is where a blocking claim would
      live, and this search has never been run.
- [ ] Finish the measurements the specification marks as not made: the render-corpus run of the acquisition
      loop and the marker; and the timing of the linking, composition and registration stages. Anything
      measured before the non-provisional can be added there; a provisional cannot be amended.
- [ ] Decide on foreign filing, which is a cost decision and not a technical one.

## Questions for counsel, from `../INVENTION_DISCLOSURE.md` §10

1. The INPADOC sweep above.
2. Whether Family A's commanded-displacement step survives *Dental Monitoring*. The distinction offered is
   that the act changes the **geometry** of the next acquisition rather than its quality, is computed from a
   run-time confidence, and is emitted as a physical quantity that moves a machine. That is an argument, not
   a settled answer.
3. Divided infringement on Family E, and whether drafting the marking and propagation as system-performed
   avoids it.
4. University ownership: the disclosure process, the timing, and what happens if the university declines.
5. Whether a signal claim (Family A claim 12) is available, and if not how to capture that scope.

## A note on the claims

`CLAIMS.md` is **not** for filing. It exists so that the specification can be checked against what will be
claimed in twelve months, limitation by limitation. If counsel finds a limitation there without adequate
support in `SPECIFICATION.md`, that is a defect to fix **before** filing — a provisional cannot be amended,
and support that is added later gets the later date.
