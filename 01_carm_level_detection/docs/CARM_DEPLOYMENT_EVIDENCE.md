# Can this ship as a software update to a C-arm?

Researched 2026-09-20 with a multi-source sweep and three-vote adversarial verification. Every claim below
survived verification; the claims that did **not** survive are recorded at the bottom, because one of them
is the kind of plausible detail that would otherwise get written into a paper.

The question asked was narrow: is there a C-arm with the processing power, or one that permits a firmware
or software update, such that a level-confirmation algorithm could be licensed to the manufacturer and
installed on fielded units with no new hardware?

---

## Short answer

**One platform, and the blocker is not the one expected.** Regulation has a route and commerce has a
route. What nobody publishes is the compute.

---

## 1. There is exactly one vendor-sanctioned on-device route (high confidence)

The **Siemens Cios family — Alpha, Flow, Spin — via "Cios OpenApps"**. Siemens' partner documentation names
the Cios C-arm as one of only two permitted hosts for locally installed partner software, the other being
its enterprise imaging platform. The wording on the partner page is the operative sentence: an application
that must be installed locally *is required to* run on one of those two.

The capability is not an aftermarket add-on. It was cleared as a software feature of the C-arm itself:

| clearance | year | device |
|---|---|---|
| K181560 | 2018 | Cios Alpha mobile C-arm |
| K203504 | 2020 | Cios Flow mobile C-arm |

So the manufacturer has already told the FDA that third-party applications run on this device. That is a
materially different starting position from arguing the case cold with any other OEM.

## 2. It is a curated marketplace, not a developer platform (high confidence)

No published software development kit. No application programming interface specification. No developer
portal. Distribution happens only through the Siemens Digital Marketplace after a partner-programme
review, and availability is gated by country. Access is a business-development conversation, not a
download.

## 3. Real third-party imaging software already ships this way (high confidence, 3-0)

Radlink launched orthopaedic applications on Cios through this route, and Siemens' own press material
advertises the absence of added hardware as the selling point. The distribution precedent is established.
The *compute* precedent is not — see section 6.

## 4. The partner carries the regulatory burden (medium confidence, 2-1)

Siemens states it is "neither the provider nor reseller nor legal manufacturer" of marketplace
applications. The algorithm vendor is therefore the legal manufacturer and needs its own clearance or CE
mark. Siemens' C-arm 510(k) does not cover partner software riding on it.

This cuts both ways. The platform clearance does not shelter the application, but the application also
does not have to wait on the OEM's submission cycle.

## 5. No other mobile C-arm has a documented on-device route (low confidence — absence of evidence)

Nothing surfaced for GE OEC (Elite, One, 3D), Ziehm (Vision RFD, Solo), Philips Zenition, Shimadzu,
Hologic Fluoroscan, Orthoscan, Whale or Turner. This is absence of published evidence, not evidence of
refusal; a bilateral agreement with any of them would not necessarily be public. Treat it as "no route you
can plan around", not "no route exists".

## 6. The real blocker: nobody publishes the compute envelope (medium confidence)

This gap was flagged independently while verifying five separate claims, which is why it is stated as a
finding rather than a caveat. **No CPU, GPU or RAM figure surfaced for any C-arm examined, from any
manufacturer.** The only operating-system datapoint that survived verification is that the Cios Flow VA30
software release involved an "Upgrade to Windows 10 Operating System".

Two things follow that matter for planning:

- Whether a Cios OpenApp is given an accelerator, or only a general-purpose core, is unknown.
- Whether the sandbox is served **live fluoroscopic frames** or only stored images after acquisition is
  unknown, and a level-confirmation loop that runs between exposures needs the former.

Neither regulation nor commercial willingness is what is unresolved here. The specification is.

## 7. The alternative architecture is cleared, shipping and vendor-agnostic (high confidence, 3-0)

An external unit that passively ingests the C-arm's video or DICOM output and drives its own display,
without modifying the C-arm. The precedent is **NuVasive/Globus Pulse with LessRay, K180038**, verified
against the FDA primary document rather than the press release, with sub-frame latency documented.

This is the route that does not depend on any OEM saying yes. It costs the "no new hardware" claim.

## 8. The licensing question returned nothing (low confidence — no surviving evidence)

Not one claim about OEM algorithm-licensing structures, royalty terms or edge-appliance economics
survived verification. Public sources do not carry this. It is answerable only by asking the OEMs or by
finding someone who has signed such a deal.

---

## Refuted — do not write these

Both were plausible, sourced, and wrong. Recorded so they are not rediscovered as facts.

- **"The OEC 3D's compute is two general-purpose computers, one for imaging and one for 3D reconstruction
  in the storage bay."** Refuted 0-3 against K203346. Every OEC 3D compute and regulatory claim drawn from
  that document failed verification and none of it is usable.
- **"Adding an image-processing or reconstruction function to a cleared mobile C-arm required a Traditional
  510(k) with the manufacturer's own prior model as predicate, not a letter to file."** Refuted.

---

## What to do with this

For the paper, sections 1, 4, 6 and 7 are written into the deployment paragraph of `paper/focused/main.tex`
with citations `k181560`, `k203504`, `ciosopenapps`, `k180038`.

For the product, the two live questions are both directed at Siemens and neither is answerable from
public documents: what compute does an OpenApp get, and does it see live frames. Until those are answered
the external-box architecture is the one that can be planned; the on-device route is the one worth asking
about.
