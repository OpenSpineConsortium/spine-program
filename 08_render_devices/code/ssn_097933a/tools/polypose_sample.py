#!/usr/bin/env python
"""THE SAMPLER. Draws one whole sagittal profile for one source CT and turns it into per-segment rigid rotations
for the PolyPose polyrigid transform. Seeded, reproducible from its manifest row, and self-tested.

WHAT IS OURS AND WHAT IS NOT. The transform is published (Gopalakrishnan, Dey, Golland, *PolyPose*, NeurIPS 2025,
arXiv:2505.19256, MIT) and is used FORWARD here: per-bone rigid motions are sampled instead of estimated by
registration. Ours is this sampling model, the junction rules and the checks -- and the sampling model itself is
assembled from published normative series, not fitted here. Every number it uses names a source in
`SchwingNet/results/polypose/sampling_spec.json` (v2).

THE MODEL, in the order the draws happen (spec `seeding.draw_order`):

  1. PI is NOT drawn. It is the patient's, measured on the source CT by ostk, and invariant under the warp
     because the pelvis is the identity body. PI is posture-invariant, so the supine measurement is also the
     standing PI.
  2. (LL*, TK*, SS*) | PI, one multivariate-normal draw in the STANDING frame of the asymptomatic literature.
     PT* = PI - SS*. This is the global compensation model: lordosis is coupled to PI, kyphosis to lordosis,
     and the pelvis follows, so the sampler cannot add lumbar lordosis without the thoracic and pelvic terms
     moving with it.
  3. Rejection BEFORE anything is rendered: marginal bands, the 99 % conditional ellipsoid, the balance
     residual and Roussouly consistency. A rejected draw is redrawn with the next sub-seed and counted.
  4. Standing -> supine offsets, because every CT here is supine and the normative cohorts stand.
  5. Roussouly type from SS*, which sets the SHAPE: how the lordosis is distributed over the segments.
  6. dLL = LL_target_supine - LL_source_measured, spread over the mobile lumbar segments by the type's shares,
     each draw truncated at that segment's Panjabi-band cap times its junction multiplier.
  7. The thoracolumbar coupling: dTLK_T10L1 = 0.2 dLL + noise (pan2024), split over the in-field thoracic
     segments in proportion to their caps. This is the part that makes "you cannot add a bunch of lumbar
     lordosis without adding thoracic kyphosis" true of the output and not only of the drawn profile.
  8. Small lateral-bending and axial-rotation draws.

WHAT IS APPLIED AND WHAT IS ONLY RECORDED. The pelvis is fixed in image space, so SS and PT are invariant in the
image BY CONSTRUCTION and cannot be "applied". Their compensation appears as the trunk's orientation over the
sacrum, which is the sum of the segmental angles. The sampler therefore applies the segmental deltas and nothing
else, and records SS*, PT* and the out-of-field part of dTK as the standing profile the result corresponds to
(spec `image_space_realisation`). Rotating the column bodily on the sacrum as well would double-count it.

THE HARD RULES (Greg, 2026-09-23) this file carries:
  - a fused or sacralised junction is ONE rigid body: junction multiplier 0, share 0, delta exactly 0.0, and the
    upper body joins the pelvis group. `--self-test` injects a Castellvi IV source and fails if any motion appears.
  - every per-segment delta inside the published segmental ROM for that segment and direction.
  - PI invariant: the sampler never emits a pelvic transform.
  - every row reproducible from its seed; the seed is a hash of the source and the variant index.

OUTSIDE CHECKS, because internal consistency has never caught anything in this project:
  `--check-cohort` measures the sampler against things it did not compute --  the drawn marginals against the
  published means and SDs, the drawn PT against Lafage's published predictor, the realised per-segment shares
  against milele2022, and the acceptance rate against the real cohort's own ostk measurements.

Usage:
  python tools/polypose_sample.py self-test                     # phantom sources, injected faults, exits non-zero
  python tools/polypose_sample.py draw --case 0244 --variant 3  # one row's sampling block as JSON
  python tools/polypose_sample.py plan --out plan.jsonl         # the whole bank's draws, before any rendering
  python tools/polypose_sample.py check-cohort                  # the outside checks
  python tools/polypose_sample.py envelope-vs-cohort            # why the balance bound is not the Schwab grade
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import polypose_manifest as PM  # noqa: E402  (seed policy, junction rules, ROM table, envelope)

SPEC_DEFAULT = ROOT / "SchwingNet/results/polypose/sampling_spec.json"
COHORT_DEFAULT = ROOT / "SchwingNet/results/polypose/cohort_sagittal.json"
SAMPLER_VERSION = "polypose-sampler/1"

# The one place the sub-draw streams are named. Each gets its own SeedSequence child so that adding a draw
# later cannot shift the numbers of the draws before it.
STREAMS = ("profile", "supine", "lumbar", "thoracolumbar", "lateral", "axial")


class UnusableSource(Exception):
    """This CT cannot be a source, and no seed will change that -- as opposed to a draw that is rejected and
    redrawn. Raised so the planner records and counts the case instead of looping or crashing."""


# --------------------------------------------------------------------------------------------- spec access
def load_spec(path=SPEC_DEFAULT) -> dict:
    """The sampling spec, refused unless it is v2 and carries every section the sampler reads. A truncated or
    hand-edited spec must not pass as a permissive one."""
    p = Path(path)
    spec = json.loads(p.read_text(encoding="utf-8"))
    if str(spec.get("spec_version")) != "2":
        raise ValueError(f"{p}: sampler needs sampling_spec v2, found {spec.get('spec_version')!r}")
    need = ("rom_deg", "junction_rules", "joint_sagittal_model", "supine_conversion", "roussouly_shape_rule",
            "segment_share_of_LL", "thoracolumbar_coupling", "per_segment_draw", "rejection_envelope", "seeding")
    missing = [k for k in need if k not in spec]
    if missing:
        raise ValueError(f"{p}: sampling spec has no {', '.join(missing)}")
    spec["__sha256__"] = PM.hashlib.sha256(p.read_bytes()).hexdigest()
    spec["__path__"] = str(p)
    return spec


def _seg_caps(spec: dict, seg: str) -> dict:
    """{flex, ext, lb, ar} for a segment from the spec's rom_deg table, by name only."""
    r = spec["rom_deg"].get(seg)
    if not isinstance(r, dict) or "flex" not in r:
        raise KeyError(f"no ROM row for segment {seg!r}")
    return dict(flex=float(r["flex"]), ext=float(r["ext"]), lb=float(r["lb"]), ar=float(r["ar"]),
                source=r.get("source", ""))


def subtype_plan(spec: dict, subtype: str) -> dict:
    """{mobile: [...], cap_from: {seg: seg_whose_caps_it_borrows}, lumbar: [...], thoracolumbar: [...]}.

    The anchoring rules are the spec's, in words, made mechanical here: an L6 spine anchors its caps AT THE
    SACRUM and walks up (L6-S1 takes L5-S1's caps), because lumbosacral mechanics are set by the pelvis; a T13
    spine takes the thoracolumbar caps for its extra thoracic-type segment. Both are decisions, not measurements
    -- no segmental ROM has ever been published for a six-lumbar or thirteen-thoracic spine (spec
    `junction_rules.subtypes.*.evidence_gap`) -- and they are recorded per row as such."""
    sub = spec["junction_rules"]["subtypes"]
    if subtype not in sub or "mobile_segments" not in sub.get(subtype, {}):
        subtype = "ordinary"
    mobile = list(sub[subtype]["mobile_segments"])
    cap_from = {}
    if subtype == "L6":
        # caudally anchored: the bottom segment borrows the bottom ordinary segment's caps, and so on up
        anchor = ["L1-L2", "L1-L2", "L2-L3", "L3-L4", "L4-L5", "L5-S1"]      # for L1-L2 .. L6-S1
        lumb = [s for s in mobile if not s.startswith("T")]
        for s, a in zip(lumb, anchor[-len(lumb):] if len(lumb) <= len(anchor) else anchor):
            cap_from[s] = a
    elif subtype == "T13":
        cap_from.update({"T11-T12": "T10-T11", "T12-T13": "T11-T12", "T13-L1": "T12-L1"})
    elif subtype == "four_lumbar_count_without_fusion":
        cap_from["L4-S1"] = "L5-S1"
    for s in mobile:
        cap_from.setdefault(s, s)
    lumbar = [s for s in mobile if not s.split("-")[0].startswith("T")]
    thoracolumbar = [s for s in mobile if s.split("-")[0].startswith("T")]
    return dict(subtype=subtype, mobile=mobile, cap_from=cap_from, lumbar=lumbar, thoracolumbar=thoracolumbar,
                evidence_gap=sub[subtype].get("evidence_gap"))


def plan_from_levels(spec: dict, levels: list) -> dict:
    """The motion plan for the vertebrae a label ACTUALLY holds (non-debris, cranio-caudal, sacrum present).

    The chain's kind is read from the labels, never from a subtype string: an L6 label makes an L6 chain, a T13
    label a T13 chain, L5 as the last lumbar an ordinary chain, L4 as the last lumbar a four-lumbar chain (L4-S1 is
    then the lumbosacral segment, with L5-S1's caps per the spec's four_lumbar rule). Mobile segments whose two ends
    are not both in the field are dropped (a field that starts at T11 has no T10-T11 to move); a lumbar chain with a
    gap (L2-L4 because L3 is unlabelled) is not a usable source. Whether the lumbosacral segment is FUSED is not
    decided here: that is the Castellvi read's job (multipliers_for)."""
    lumbar = [l for l in levels if l.startswith("L")]
    if not lumbar:
        raise UnusableSource("no lumbar vertebra labelled")
    if "L6" in lumbar:
        kind = "L6"
    elif "T13" in levels:
        kind = "T13"
    elif lumbar[-1] == "L5":
        kind = "ordinary"
    elif lumbar[-1] == "L4":
        kind = "four_lumbar"
    else:
        raise UnusableSource(f"last lumbar vertebra {lumbar[-1]}: no plan for this count")
    want = [f"L{i}" for i in range(1, int(lumbar[-1][1:]) + 1)]
    if lumbar != want:
        raise UnusableSource(f"lumbar labels {lumbar} are not the contiguous chain {want}")
    if kind == "four_lumbar":
        base = dict(subtype="four_lumbar", mobile=["T10-T11", "T11-T12", "T12-L1", "L1-L2", "L2-L3", "L3-L4", "L4-S1"],
                    cap_from={"L4-S1": "L5-S1"}, evidence_gap=spec["junction_rules"]["subtypes"]
                    .get("four_lumbar_count_without_fusion", {}).get("rule", "no published ROM for four-lumbar spines"))
        for s in base["mobile"]:
            base["cap_from"].setdefault(s, s)
    else:
        base = subtype_plan(spec, kind)
    present = set(levels) | {"S1"}
    mobile = [s for s in base["mobile"] if all(x in present for x in s.split("-"))]
    lum = [s for s in mobile if not s.split("-")[0].startswith("T")]
    need = [f"{a}-{b}" for a, b in zip(want, want[1:] + ["S1"])]
    if lum != need:
        raise UnusableSource(f"lumbar segments {lum} != the chain {need}")
    tl = [s for s in mobile if s.split("-")[0].startswith("T")]
    return dict(subtype=base["subtype"], mobile=mobile, cap_from={s: base["cap_from"][s] for s in mobile},
                lumbar=lum, thoracolumbar=tl, evidence_gap=base.get("evidence_gap"),
                dropped_out_of_field=[s for s in base["mobile"] if s not in mobile])


def shares_for(spec: dict, plan: dict, roussouly_type: str, multipliers: dict) -> dict:
    """The share of dLL each mobile lumbar segment carries, for this Roussouly type and this subtype.

    Roussouly type sets the SHAPE: a type 1 puts 0.525 of its lordosis at L5-S1 and 0.012 at L1-L2, a type 4
    spreads it (0.387 / 0.028). That is the difference between a short hyperlordosis over the last disc and a
    long harmonious curve, and it is the reason the type is drawn at all rather than LL alone.

    Subtype anchoring: an L6 chain takes the ordinary shares anchored AT THE SACRUM and reuses the top share,
    exactly as `junction_rules.subtypes.L6.shares` spells out; a segment whose junction multiplier is 0 (fused)
    gets share 0 and the rest renormalise -- which is also what makes the sacralised row come out at the spec's
    published 0.040 / 0.204 / 0.316 / 0.440 without a second table."""
    table = spec["roussouly_shape_rule"]["resulting_shares_by_type"]
    base = table.get(str(roussouly_type)) or spec["segment_share_of_LL"]
    ordinary = ["L1-L2", "L2-L3", "L3-L4", "L4-L5", "L5-S1"]
    vals = [float(base[s]) for s in ordinary]
    lumb = plan["lumbar"]
    if plan["subtype"] == "L6" and len(lumb) == 6:
        # ONLY here do the names shift, so only here is the mapping positional: the L6 chain is anchored at the
        # sacrum (L6-S1 takes L5-S1's share) and the top share is reused, per junction_rules.subtypes.L6.shares.
        raw = dict(zip(lumb, [vals[0]] + vals))
    elif plan["subtype"] == "four_lumbar" and len(lumb) == 4:
        # A four-lumbar chain (L1-L2, L2-L3, L3-L4, L4-S1) is anchored at the sacrum the same way: L4-S1 takes
        # L5-S1's share, L3-L4 takes L4-L5's, and so on up; the top ordinary share (L1-L2) has no segment and the
        # rest renormalise. The mirror of the L6 decision, stated as a decision: no share series is published
        # for four-lumbar spines.
        raw = dict(zip(lumb, vals[1:]))
    else:
        # Every other subtype keeps the ordinary NAMES; a segment the subtype does not have (L5-S1 in a
        # sacralised spine) is simply absent and the rest renormalise below. Matching positionally here was a
        # bug: it slid L2-L3's share onto L1-L2 and gave a four-segment lumbar spine the wrong shape entirely.
        raw = {s: float(base[s]) for s in lumb if s in base}
        for s in lumb:
            raw.setdefault(s, 0.0)
    raw = {s: (0.0 if float(multipliers.get(s, 1.0)) == 0.0 else v) for s, v in raw.items()}
    tot = sum(raw.values())
    if tot <= 0:
        raise ValueError("every lumbar segment is fused: there is nothing to distribute lordosis over")
    return {s: v / tot for s, v in raw.items()}


def multipliers_for(spec: dict, plan: dict, castellvi) -> dict:
    """Junction multiplier per mobile segment. 1.0 everywhere except the lumbosacral junction, where the
    Castellvi grade sets it: I -> 1.0 (an enlarged transverse process is not an articulation), II -> 0.45
    (kuoppala2025 measured 3.3 deg against 7.3 in controls for pooled II-IV), III/IV -> 0.0, EXACTLY zero, the
    fused body joining the pelvis. `unknown` takes the II value, which is the conservative middle.

    The grade comes from the anomaly tables' own reads, never from label ids -- inferring a fusion from the fact
    that a case has five lumbar labels is how a wrong map produces a plausible answer.

    THE JUNCTION IS THE SEGMENT ENDING AT S1, NOT THE LAST MOBILE SEGMENT. In a sacralised spine the subtype has
    already taken L5 into the pelvis, so the caudal-most MOBILE segment is L4-L5 -- an ordinary, mobile,
    adjacent level (kuoppala2025 measured no excess motion there). Putting the fusion multiplier on the last
    mobile segment froze L4-L5 instead, which produces a spine that is rigid one level too high and looks
    entirely reasonable in every number. Returns (multipliers, junction_segment, fused_segments)."""
    tab = spec["junction_rules"]["castellvi_multiplier"]
    key = str(castellvi).strip() if castellvi not in (None, "", "nan") else "0"
    mult = tab.get(key)
    if mult is None:
        types = PM.parse_castellvi(key)
        mult = min((float(tab[t]) for t in types if t in tab), default=float(tab["unknown"]))
    mult = float(mult)
    out = {s: 1.0 for s in plan["mobile"]}
    junction = next((s for s in plan["mobile"] if s.endswith("-S1")), None)
    fused = []
    if junction is not None:
        out[junction] = mult
        if mult == 0.0:
            fused.append(junction)
    else:
        # the subtype removed the lumbosacral segment: it is fused by definition of the subtype (sacralised L5)
        junction = f"{plan['lumbar'][-1].split('-')[1]}-S1" if plan["lumbar"] else None
        if junction:
            fused.append(junction)
    return out, junction, fused


# ------------------------------------------------------------------------------------------- the joint model
def conditional_given_pi(spec: dict, PI: float) -> tuple:
    """(mean vector, covariance) of (LL, TK, SS) given PI, in the STANDING frame."""
    j = spec["joint_sagittal_model"]
    beta = j["conditional_given_PI"]["mean_i = mu_i + beta_i * (PI - 52.0)"]
    mu = j["means_sd_standing"]
    mean = np.array([float(mu["LL"][0]) + float(beta["LL"]) * (PI - 52.0),
                     float(mu["TK"][0]) + float(beta["TK"]) * (PI - 52.0),
                     float(mu["SS"][0]) + float(beta["SS"]) * (PI - 52.0)], dtype=float)
    cov = np.array(j["conditional_given_PI"]["residual_covariance_order_LL_TK_SS"], dtype=float)
    return mean, cov


def truncated_normal(rng, mean: float, sd: float, lo: float, hi: float, tries: int = 64) -> float:
    """A normal draw resampled into [lo, hi]; the clamp is the last resort so the call always terminates. sd <= 0
    returns the clamped mean."""
    if not (hi > lo):
        return float(min(max(mean, min(lo, hi)), max(lo, hi)))
    if sd <= 0:
        return float(min(max(mean, lo), hi))
    for _ in range(tries):
        v = float(rng.normal(mean, sd))
        if lo <= v <= hi:
            return v
    return float(min(max(float(rng.normal(mean, sd)), lo), hi))


def roussouly_from_ss(spec: dict, SS_star: float, TK_star: float, TK_cond_mean: float) -> str:
    """Type by standing SS (Roussouly 2005 cut-offs 35 / 45). Types 1 and 2 share the SS band and are NOT
    separable by SS: the spec resolves them by the drawn thoracolumbar kyphosis, and at this point in the draw
    order the only thoracic quantity drawn is TK*, so type 1 (the long thoracolumbar kyphosis) is assigned when
    TK* sits above its mean conditional on PI and LL*, type 2 otherwise. That is an interpretation of the spec's
    words, recorded per row as `type_1_2_rule`, not a published test."""
    r = spec["roussouly_shape_rule"]
    lo = float(str(r.get("ss_type12_max", 35.0)) if "ss_type12_max" in r else 35.0)
    hi = 45.0
    if SS_star > hi:
        return "4"
    if SS_star < lo:
        return "1" if TK_star > TK_cond_mean else "2"
    return "3"


def _tk_given_pi_ll(cov: np.ndarray, mean: np.ndarray, LL_star: float) -> float:
    """E[TK | PI, LL*] from the conditional covariance: mean_TK + (cov_LL,TK / var_LL) (LL* - mean_LL)."""
    return float(mean[1] + (cov[0, 1] / cov[0, 0]) * (LL_star - mean[0]))


# -------------------------------------------------------------------------------------------------- the draw
def ll_quantile(spec: dict, PI: float, LL: float) -> float:
    """Where a standing LL sits in the model's LL | PI conditional, as a probability (0..1)."""
    mean, cov = conditional_given_pi(spec, PI)
    return 0.5 * (1.0 + math.erf((LL - mean[0]) / (math.sqrt(cov[0, 0]) * math.sqrt(2.0))))


def draw_profile(spec: dict, PI: float, rng, ll_band=None) -> dict:
    """One accepted standing profile, with the rejections that preceded it. Rejection happens HERE, before any
    volume is touched: a profile outside the reference envelope never reaches a renderer.

    `ll_band` (lo, hi) restricts the draw to a STRATUM of the conditional LL | PI distribution (the fill-in rule's
    conditional-LL deciles, coarsened to terciles for validation): a draw outside the band is not a rejection by
    the envelope -- it is simply not this stratum -- and is counted separately as a stratum miss."""
    mean, cov = conditional_given_pi(spec, PI)
    rej = spec["rejection_envelope"]
    mb = rej["marginal_bounds_standing_deg"]
    jb = rej["joint_bounds"]
    chi2 = 11.34
    bal = spec["joint_sagittal_model"]["balance_identity"]["c = SS - LL + TK"]
    cmean, csd = float(bal["mean"]), float(bal["sd"])
    cinv = np.linalg.inv(cov)
    env = PM.load_envelope_table()
    sd_ll = math.sqrt(cov[0, 0])

    rejected, misses = [], 0
    for attempt in range(1000 if ll_band else 200):
        LL, TK, SS = (mean + rng.multivariate_normal(np.zeros(3), cov)).tolist()
        PT = PI - SS
        q = 0.5 * (1.0 + math.erf((LL - mean[0]) / (sd_ll * math.sqrt(2.0))))
        if ll_band is not None and not (float(ll_band[0]) <= q <= float(ll_band[1])):
            misses += 1
            continue
        why = []
        for name, v, key in (("LL", LL, "LL_star"), ("TK", TK, "TK_star"), ("SS", SS, "SS_star"), ("PT", PT, "PT_star")):
            lo, hi = float(mb[key][0]), float(mb[key][1])
            if not (lo <= v <= hi):
                why.append(f"marginal_{name} {v:.1f} outside [{lo}, {hi}]")
        lo, hi = float(mb["PI_minus_LL_star"][0]), float(mb["PI_minus_LL_star"][1])
        if not (lo <= PI - LL <= hi):
            why.append(f"PI-LL {PI - LL:.1f} outside [{lo}, {hi}]")
        d = np.array([LL, TK, SS]) - mean
        m2 = float(d @ cinv @ d)
        if m2 > chi2:
            why.append(f"mahalanobis {m2:.2f} > {chi2} (outside the 99 % conditional ellipsoid)")
        c = SS - LL + TK
        if abs(c - cmean) > 2.5 * csd:
            why.append(f"balance residual {c - cmean:+.1f} beyond 2.5 SD ({2.5 * csd:.1f})")
        TKm = _tk_given_pi_ll(cov, mean, LL)
        rtype = roussouly_from_ss(spec, SS, TK, TKm)
        if (SS < 35 and LL > 70) or (SS > 45 and LL < 40):
            why.append(f"roussouly shape inconsistent: SS {SS:.1f} with LL {LL:.1f}")
        drawn = dict(PI=PI, PT=PT, SS=SS, LL=LL, TK=TK, roussouly_type=rtype)
        ev = PM.evaluate_profile(drawn, env)
        if not ev["in_envelope"]:
            why.append("envelope table: " + ", ".join(k for k, v in ev["rules"].items() if v["status"] == "fail"))
        if why:
            rejected.append(dict(attempt=attempt, reasons=why))
            # PI is the patient's and the warp cannot change it, so a PI rule can never be satisfied by
            # redrawing: that is a source that must be excluded, not a draw that must be retried.
            if any("range_PI" in w for w in why):
                raise UnusableSource(f"the source's own PI {PI:.1f} is outside the published range: "
                                     f"no draw can move it, so this case is not a source")
            continue
        return dict(standing=drawn, mahalanobis=m2, balance_c=c, conditional_mean=dict(LL=mean[0], TK=mean[1], SS=mean[2]),
                    TK_conditional_mean_given_LL=TKm, type_1_2_rule="TK* above E[TK|PI,LL*] -> 1 else 2",
                    envelope=ev["rules"], in_envelope=True, envelope_sha256=ev["envelope_sha256"],
                    rejections=len(rejected), rejection_reasons=rejected[:8], accepted_on_attempt=attempt,
                    ll_quantile=q, ll_band=None if ll_band is None else list(ll_band), stratum_misses=misses)
    raise RuntimeError(f"no profile inside the envelope after {attempt + 1} draws at PI {PI:.1f} (band {ll_band}, "
                       f"{misses} stratum misses): last reasons {rejected[-1]['reasons'] if rejected else 'none'}")


def distribute_ll(spec: dict, plan: dict, shares: dict, caps: dict, mults: dict, dLL: float, rng) -> dict:
    """Spread dLL over the mobile lumbar segments, each draw truncated at its own cap, clipping once and
    redistributing the clipped remainder over the segments that still have room.

    A fused segment has share 0 and cap 0 and comes out EXACTLY 0.0 -- not 1e-17, not 'small': the checker tests
    it at 1e-6 and the figure has to show it rigid."""
    req, out = {}, {}
    for s in plan["lumbar"]:
        m = float(mults.get(s, 1.0))
        c = caps[s]
        lo, hi = -c["flex"] * m, c["ext"] * m
        mu = shares.get(s, 0.0) * dLL
        mu = min(max(mu, lo), hi)
        req[s] = mu
        if m == 0.0:
            out[s] = 0.0
            continue
        sd_cap = (c["ext"] if mu >= 0 else c["flex"]) * m
        sd = float(spec["per_segment_draw"].get("sd_fraction", 0.4)) * (sd_cap if sd_cap > 0 else min(c["flex"], c["ext"]) * m)
        out[s] = truncated_normal(rng, mu, sd, lo, hi)
    # one redistribution of whatever the caps refused, over the segments with room in the needed direction
    short = dLL - sum(out.values())
    if abs(short) > 1e-9:
        room = {}
        for s in plan["lumbar"]:
            m = float(mults.get(s, 1.0))
            if m == 0.0:
                continue
            lo, hi = -caps[s]["flex"] * m, caps[s]["ext"] * m
            room[s] = (hi - out[s]) if short > 0 else (out[s] - lo)
        tot = sum(v for v in room.values() if v > 0)
        if tot > 0:
            for s, r in room.items():
                if r > 0:
                    out[s] += short * (r / tot)
                    lo, hi = -caps[s]["flex"] * mults[s], caps[s]["ext"] * mults[s]
                    out[s] = min(max(out[s], lo), hi)
    return dict(requested=req, applied=out, shortfall=dLL - sum(out.values()))


TARGETS = ("lo", "mid", "hi")
# Strata of the conditional LL | PI distribution for a variant's target (validation terciles; the production
# fill-in rule uses deciles). Each band stops 2 % short of the tails so a stratum is never defined by the 2.5-SD
# rejection edge alone.
TARGET_BANDS = {"lo": (0.02, 0.25), "mid": (0.375, 0.625), "hi": (0.75, 0.98)}


class Unreachable(Exception):
    """No realisable profile for this (source, stratum): every draw either left a lumbar shortfall over the spec's
    3 deg or put the realised profile outside the envelope. Recorded as unreachable, never clipped into existence."""


def realised_profile(spec: dict, case_row: dict, st: dict, off: dict, segments: dict, plan: dict, tk_segments) -> dict:
    """The standing-equivalent profile the SEGMENTS realise, in the manifest's arithmetic.

    source_standing: PI measured; SS and LL = the source's supine measurement minus this output's drawn supine
    offset; PT = PI - SS; TK (T4-T12, out of an abdominopelvic field) imputed as E[TK | PI, LL] of the joint model.
    drawn: SS* and PT* as drawn (virtual: the pelvis is fixed in the image), LL = source + the lumbar deltas actually
    applied, TK = source + minus the thoracic deltas inside the measured TK span. So delta.LL == requested.delta_ll_deg
    and delta.TK == requested.delta_tk_deg by construction, and what the model drew but the segments could not carry
    is the shortfall, recorded beside it."""
    PI = float(case_row["PI"])
    mean, cov = conditional_given_pi(spec, PI)
    src = dict(PI=PI, SS=float(case_row["SS"]) - off["SS"], LL=float(case_row["LL"]) - off["LL"])
    src["PT"] = PI - src["SS"]
    src["TK"] = float(mean[1] + (cov[0, 1] / cov[0, 0]) * (src["LL"] - mean[0]))
    src["PT_method"] = ("PT = PI - SS; SS = the source's supine image SS (ostk pi-v1 core) minus this output's drawn "
                        "supine offset dSS (sampling_spec supine_conversion.draw)")
    src["TK_method"] = ("imputed: E[TK | PI, LL] of the joint model (T4-T12 lies outside an abdominopelvic field); "
                        "only the in-field thoracic deltas are applied and re-measured")
    dLL = sum(float(segments[s]["flex_ext_deg"]) for s in plan["lumbar"] if s in segments)
    dTK = -sum(float(segments[s]["flex_ext_deg"]) for s in (tk_segments or []) if s in segments)
    drawn = dict(PI=PI, SS=float(st["SS"]), PT=PI - float(st["SS"]), LL=src["LL"] + dLL, TK=src["TK"] + dTK,
                 roussouly_type=str(st["roussouly_type"]))
    ev = PM.evaluate_profile(drawn, PM.load_envelope_table())
    delta = dict(PT=drawn["PT"] - src["PT"], SS=drawn["SS"] - src["SS"], LL=dLL, TK=dTK)
    return dict(source_standing=src, drawn=drawn, delta=delta, envelope=ev["rules"], in_envelope=ev["in_envelope"],
                unverified_bounds=ev["unverified"],
                shortfall=dict(LL_deg=float(st["LL"]) - drawn["LL"], TK_deg=float(st["TK"]) - drawn["TK"]),
                delta_ll_deg=dLL, delta_tk_deg=dTK)


def draw_variant(spec: dict, case_row: dict, variant_index: int, collection: str = "ctsp", plan=None, target=None,
                 tk_segments=None, realise=False, max_tries=80) -> dict:
    """The whole sampling block of one manifest row. Deterministic in (collection, case, variant_index).

    With `realise=True` (the generator's call) a draw is accepted only when the segments can carry it: a lumbar
    shortfall over the spec's 3 deg (rejection_envelope.per_level) or a REALISED profile outside the envelope sends it
    back to be redrawn from the next numbers of the same streams, and every such rejection is counted. `plan`
    overrides the subtype plan (plan_from_levels: the vertebrae the label really holds); `target` picks a stratum of
    the conditional LL (TARGET_BANDS). The stream order is the one the self-test pins: profile, supine, lumbar,
    thoracolumbar, lateral, axial -- calls without the new arguments draw exactly the numbers they always drew."""
    case = str(case_row["case"])
    seed = PM.seed_for(collection, case, variant_index)
    ss_root = np.random.SeedSequence(seed)
    streams = dict(zip(STREAMS, (np.random.Generator(np.random.PCG64(s)) for s in ss_root.spawn(len(STREAMS)))))

    PI = float(case_row["PI"])
    subtype = str(case_row.get("subtype") or "ordinary")
    plan = plan if plan is not None else subtype_plan(spec, subtype)
    mults, junction_seg, fused = multipliers_for(spec, plan, case_row.get("castellvi"))
    caps = {s: _seg_caps(spec, plan["cap_from"][s]) for s in plan["mobile"]}
    band = TARGET_BANDS[target] if target else None
    sc = spec["supine_conversion"]["draw"]
    LL_src = float(case_row["LL"])
    realise_rejections = []
    for attempt in range(max_tries if realise else 1):
        prof = draw_profile(spec, PI, streams["profile"], ll_band=band)
        st = prof["standing"]

        # standing -> supine, one draw per output, recorded (the normative cohorts stand; every CT here is supine)
        off = {k: float(streams["supine"].normal(float(sc[f"d{k}"][1]), float(sc[f"d{k}"][2]))) for k in ("LL", "SS", "TK")}
        sup = dict(PI=PI, LL=st["LL"] + off["LL"], SS=st["SS"] + off["SS"], TK=st["TK"] + off["TK"])
        sup["PT"] = PI - sup["SS"]

        shares = shares_for(spec, plan, st["roussouly_type"], mults)
        dLL = sup["LL"] - LL_src
        lum = distribute_ll(spec, plan, shares, caps, mults, dLL, streams["lumbar"])

        # thoracolumbar coupling (pan2024): TLK is KYPHOTIC-positive, the segment deltas are LORDOTIC-positive, so
        # the segments carry -dTLK. Getting that sign backwards would make every added lordosis straighten the
        # thoracolumbar junction instead of bending it, which is the opposite of the compensation being modelled.
        dTLK = 0.2 * dLL + float(streams["thoracolumbar"].normal(0.0, 2.0))
        tl_segs = plan["thoracolumbar"]
        wts = np.array([(caps[s]["flex"] + caps[s]["ext"]) / 2.0 for s in tl_segs], dtype=float)
        wts = wts / wts.sum() if wts.sum() > 0 else wts
        tl_out = {}
        for s, w in zip(tl_segs, wts):
            m = float(mults.get(s, 1.0))
            lo, hi = -caps[s]["flex"] * m, caps[s]["ext"] * m
            tl_out[s] = min(max(-dTLK * float(w), lo), hi)

        segments = {}
        for s in plan["mobile"]:
            m = float(mults.get(s, 1.0))
            c = caps[s]
            fe = lum["applied"].get(s, tl_out.get(s, 0.0))
            lb = 0.0 if m == 0.0 else truncated_normal(streams["lateral"], 0.0, 1.0, -0.5 * c["lb"] * m, 0.5 * c["lb"] * m)
            ar = 0.0 if m == 0.0 else truncated_normal(streams["axial"], 0.0, 0.5, -0.5 * c["ar"] * m, 0.5 * c["ar"] * m)
            segments[s] = dict(flex_ext_deg=round(float(fe), 6), lat_bend_deg=round(float(lb), 6),
                               axial_rot_deg=round(float(ar), 6))
        realised = None
        if realise:
            realised = realised_profile(spec, case_row, st, off, segments, plan, tk_segments)
            why = []
            if abs(lum["shortfall"]) > 3.0:
                why.append(f"lumbar shortfall {lum['shortfall']:+.2f} deg beyond the spec's 3 deg: the segments cannot carry this draw")
            if not realised["in_envelope"]:
                why.append("realised profile outside the envelope: " + ", ".join(k for k, v in realised["envelope"].items() if v["status"] == "fail"))
            if why:
                realise_rejections.append(dict(attempt=attempt, reasons=why, LL_star=round(st["LL"], 2)))
                continue
        break
    else:
        raise Unreachable(f"{collection}/{case} v{variant_index} target {target}: no realisable draw in {max_tries} "
                          f"(last: {realise_rejections[-1]['reasons'] if realise_rejections else 'none'})")

    jr = PM.junction_rule_for(case_row.get("castellvi"), case_row.get("lstv_class"))
    return {
        "sampler": {"version": SAMPLER_VERSION, "spec": spec["__path__"], "spec_sha256": spec["__sha256__"],
                    "streams": list(STREAMS)},
        "source": {"collection": collection, "case": case, "subtype": subtype,
                   "castellvi": case_row.get("castellvi"), "lstv_class": case_row.get("lstv_class"),
                   "measured_supine": {k: case_row.get(k) for k in ("PI", "SS", "PT", "LL", "TLK_T10L2", "junction_disc")}},
        "variant_index": int(variant_index), "seed": seed, "seed_policy": PM.SEED_POLICY,
        "target": target, "ll_band": None if band is None else list(band),
        "profile": {"model": "global-sagittal-compensation/2", "posture": "supine",
                    "drawn_standing": st, "drawn_supine": sup, "supine_offsets": off,
                    "roussouly_type": st["roussouly_type"], "shares": shares,
                    "mahalanobis": prof["mahalanobis"], "balance_c": prof["balance_c"],
                    "envelope": prof["envelope"], "in_envelope": True, "envelope_sha256": prof["envelope_sha256"],
                    "rejections": prof["rejections"], "rejection_reasons": prof["rejection_reasons"],
                    "type_1_2_rule": prof["type_1_2_rule"], "ll_quantile": prof.get("ll_quantile"),
                    "stratum_misses": prof.get("stratum_misses", 0),
                    "realise_rejections": len(realise_rejections), "realise_rejection_reasons": realise_rejections[:8],
                    "realised": realised},
        "requested": {"segments": segments, "delta_ll_deg": round(dLL, 6),
                      "delta_tlk_t10l1_deg": round(dTLK, 6),
                      "delta_tk_star_deg": round(st["TK"], 6),
                      "shortfall": {"LL_deg": round(lum["shortfall"], 6)},
                      "per_segment_requested": {k: round(v, 6) for k, v in lum["requested"].items()},
                      "caps_used": {s: {k: caps[s][k] for k in ("flex", "ext", "lb", "ar", "source")} for s in plan["mobile"]},
                      "multipliers": mults},
        "junction": {"rule": jr["rule"], "reason": jr["reason"], "castellvi": jr["castellvi"],
                     "segment": junction_seg, "fused_segments": fused,
                     "multiplier": mults.get(junction_seg, 0.0) if junction_seg else None,
                     "fused_by_subtype": junction_seg not in plan["mobile"] if junction_seg else False},
        "subtype_plan": {k: plan.get(k) for k in ("subtype", "mobile", "lumbar", "thoracolumbar", "cap_from", "evidence_gap",
                                                   "dropped_out_of_field")},
    }


# ------------------------------------------------------------------------------------------------- cohort IO
def load_cohort(path=COHORT_DEFAULT) -> list:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return [r for r in d["per_case"] if not r.get("error")]


def plate_sane(spec: dict, r: dict) -> tuple:
    """The spec's own source gate (`rejection_envelope.source_plate_sanity`). Returns (ok, reasons).

    It matters: 64 of the 750 CTSP ordinary rows carry flags ['ok'] and still fail it, one of them with a
    measured standing-equivalent LL of -19.9 deg. A row flagged ok by the measurer is not a usable source."""
    bad = []
    num = (int, float)
    if not all(isinstance(r.get(k), num) for k in ("PI", "SS", "PT", "LL")):
        bad.append("PI/SS/PT/LL not all measured")
        return False, bad
    if not (10.0 <= float(r["LL"]) <= 85.0):
        bad.append(f"LL {r['LL']} outside [10, 85]")
    jd = r.get("junction_disc")
    if isinstance(jd, num) and abs(float(jd)) > 30.0:
        bad.append(f"junction disc {jd} beyond 30")
    tl = r.get("TLK_T10L2")
    if isinstance(tl, num) and abs(float(tl)) > 40.0:
        bad.append(f"TLK_T10L2 {tl} beyond 40")
    # A non-ordinary source needs a lumbosacral read to set its junction rule. lstv_class 0 IS a read -- the flag
    # table's readers looked and called the junction not transitional (a lumbar-rib spine, a four-lumbar count) --
    # so Castellvi '0' (full mobility) applies; only a source with neither a grade nor a class is refused.
    if (str(r.get("subtype") or "ordinary") != "ordinary" and r.get("castellvi") in (None, "", "nan")
            and str(r.get("lstv_class")).strip() not in ("0", "0.0")):
        bad.append("a non-ordinary source with no Castellvi read and no lstv_class: the junction rule cannot be set")
    # PI is invariant under the warp, so a source whose own PI is outside the published band can never produce
    # an in-envelope output. 5 of the 756 measured cases (0.7 %) fall here: 22.6, 23.2, 87.0, 89.5, 90.0 deg.
    env = PM.load_envelope_table()["range"]["PI"]
    if not (float(env["lo"]) <= float(r["PI"]) <= float(env["hi"])):
        bad.append(f"source PI {r['PI']} outside the published range [{env['lo']}, {env['hi']}] and the warp "
                   f"cannot change PI")
    return (not bad), bad


# ----------------------------------------------------------------------------------------------- self-test
def _phantom_row(case="9001", subtype="ordinary", castellvi=None, PI=52.0, LL=50.0):
    return dict(cohort="ctsp", case=case, subtype=subtype, castellvi=castellvi, PI=PI, SS=38.0, PT=PI - 38.0,
                LL=LL, TLK_T10L2=4.0, junction_disc=9.0, flags=["ok"])


def self_test(spec: dict) -> int:
    """Builds phantom sources, draws, and FAILS ON PURPOSE when a rule is violated. A checker that cannot fail is
    not a checker; this one is exercised against the three hard rules and the two sign traps."""
    fails, checks = [], 0

    def ck(name, cond, note=""):
        nonlocal checks
        checks += 1
        if not cond:
            fails.append(f"{name}: {note}")

    # 1. determinism
    a = draw_variant(spec, _phantom_row(), 3)
    b = draw_variant(spec, _phantom_row(), 3)
    ck("determinism", json.dumps(a["requested"], sort_keys=True) == json.dumps(b["requested"], sort_keys=True),
       "two draws with the same seed differ")
    c = draw_variant(spec, _phantom_row(), 4)
    ck("variant_index_moves_the_draw", json.dumps(a["requested"]) != json.dumps(c["requested"]),
       "variant 3 and variant 4 produced the same numbers")
    ck("seed_is_the_hash", a["seed"] == PM.seed_for("ctsp", "9001", 3), "seed does not match the manifest policy")

    # 2. HARD RULE: a fused junction has exactly zero motion, on every axis. Two routes reach it -- the subtype
    #    takes the fused body into the pelvis (sacralised_L5), or the Castellvi multiplier zeroes a segment that
    #    is still in the chain (an ordinary five-lumbar spine read III/IV) -- and BOTH are tested, because it was
    #    the interaction of the two that put the freeze on the wrong level.
    for subtype in ("sacralised_L5", "ordinary"):
        for grade in ("III", "IIIa", "IIIb", "IV"):
            r = draw_variant(spec, _phantom_row(case="9002", subtype=subtype, castellvi=grade), 0)
            segs, fused = r["requested"]["segments"], r["junction"]["fused_segments"]
            tag = f"fused_{subtype}_{grade}"
            ck(f"{tag}_declared", r["junction"]["rule"] == "fused_zero_motion", f"rule is {r['junction']['rule']}")
            ck(f"{tag}_junction_is_lumbosacral", str(r["junction"]["segment"]).endswith("-S1"),
               f"the junction was taken to be {r['junction']['segment']!r}, which does not end at S1")
            ck(f"{tag}_named", fused, "a III/IV read produced no fused segment at all")
            for s in fused:
                if s in segs:
                    v = segs[s]
                    ck(f"{tag}_zero_{s}", all(abs(float(v.get(k, 0.0))) < 1e-12 for k in
                                              ("flex_ext_deg", "lat_bend_deg", "axial_rot_deg")), f"{s} moved: {v}")
                ck(f"{tag}_share_zero_{s}", r["profile"]["shares"].get(s, 0.0) == 0.0,
                   "a fused segment kept a share of the lordosis")
            # and the ADJACENT level must still move: freezing L4-L5 in a sacralised spine is the bug this catches
            if subtype == "sacralised_L5":
                adj = r["subtype_plan"]["lumbar"][-1]
                ck(f"{tag}_adjacent_mobile", float(r["requested"]["multipliers"][adj]) == 1.0,
                   f"{adj} was frozen; kuoppala2025 measured no excess at the level above a sacralisation")

    # 3. HARD RULE: every delta inside its own cap x multiplier, both directions
    for case, sub, cas in (("9003", "ordinary", None), ("9004", "L6", None), ("9005", "T13", None),
                           ("9006", "ordinary", "II"), ("9007", "sacralised_L5", "IV")):
        for vi in range(6):
            r = draw_variant(spec, _phantom_row(case=case, subtype=sub, castellvi=cas), vi)
            caps, mult = r["requested"]["caps_used"], r["requested"]["multipliers"]
            for s, v in r["requested"]["segments"].items():
                m = float(mult[s])
                ck(f"rom_{case}_{vi}_{s}",
                   -caps[s]["flex"] * m - 1e-9 <= v["flex_ext_deg"] <= caps[s]["ext"] * m + 1e-9,
                   f"{v['flex_ext_deg']:.3f} outside [{-caps[s]['flex'] * m:.3f}, {caps[s]['ext'] * m:.3f}]")
                ck(f"lb_{case}_{vi}_{s}", abs(v["lat_bend_deg"]) <= 0.5 * caps[s]["lb"] * m + 1e-9, "lateral bend over cap")
                ck(f"ar_{case}_{vi}_{s}", abs(v["axial_rot_deg"]) <= 0.5 * caps[s]["ar"] * m + 1e-9, "axial rotation over cap")

    # 4. OUTSIDE CHECK on shares_for: fed the spec's population row, the renormalisation must reproduce the
    #    share numbers the spec publishes for a sacralised spine, which were computed independently of this code.
    plan = subtype_plan(spec, "sacralised_L5")
    m_s, _, _ = multipliers_for(spec, plan, "IV")
    sh = shares_for(spec, plan, "population", m_s)          # not a type key -> the segment_share_of_LL row
    want = {"L1-L2": 0.040, "L2-L3": 0.204, "L3-L4": 0.316, "L4-L5": 0.440}
    ck("sacralised_shares_match_spec", all(abs(sh[k] - v) < 0.002 for k, v in want.items()),
       f"computed {sh} against the spec's published {want}")
    # and the L6 row, likewise published in the spec (its values divided by 1.023)
    plan6_ = subtype_plan(spec, "L6")
    m6, _, _ = multipliers_for(spec, plan6_, None)
    sh6 = shares_for(spec, plan6_, "population", m6)
    want6 = {k: v / 1.023 for k, v in {"L1-L2": 0.023, "L2-L3": 0.023, "L3-L4": 0.117,
                                       "L4-L5": 0.181, "L5-L6": 0.252, "L6-S1": 0.427}.items()}
    ck("L6_shares_match_spec", all(abs(sh6[k] - v) < 0.002 for k, v in want6.items()),
       f"computed {sh6} against the spec's published {want6}")
    plan6 = subtype_plan(spec, "L6")
    ck("L6_chain", plan6["lumbar"][-1] == "L6-S1" and plan6["cap_from"]["L6-S1"] == "L5-S1",
       f"L6 caps not anchored at the sacrum: {plan6['cap_from']}")
    ck("T13_chain", subtype_plan(spec, "T13")["cap_from"].get("T12-T13") == "T11-T12", "T13 caps not anchored")

    # 5. SIGN TRAP: more lordosis must bend the thoracolumbar junction into kyphosis, not straighten it.
    #    dLL > 0 -> dTLK > 0 (kyphotic-positive) -> the TL segment deltas (lordotic-positive) go NEGATIVE.
    lo = draw_variant(spec, _phantom_row(case="9008", LL=25.0), 0)     # source far below target -> large +dLL
    hi = draw_variant(spec, _phantom_row(case="9008", LL=75.0), 0)     # source far above target -> large -dLL
    ck("sign_dLL", lo["requested"]["delta_ll_deg"] > 0 > hi["requested"]["delta_ll_deg"],
       f"dLL {lo['requested']['delta_ll_deg']:.1f} / {hi['requested']['delta_ll_deg']:.1f}")
    tl_lo = sum(lo["requested"]["segments"][s]["flex_ext_deg"] for s in lo["subtype_plan"]["thoracolumbar"])
    tl_hi = sum(hi["requested"]["segments"][s]["flex_ext_deg"] for s in hi["subtype_plan"]["thoracolumbar"])
    ck("sign_thoracolumbar_compensation", tl_lo < 0 < tl_hi,
       f"added lordosis gave TL sum {tl_lo:+.2f} and lost lordosis {tl_hi:+.2f}: the compensation sign is inverted")
    ck("lumbar_carries_dLL",
       sum(lo["requested"]["segments"][s]["flex_ext_deg"] for s in lo["subtype_plan"]["lumbar"]) > 0,
       "the lumbar segments did not carry the requested lordosis")

    # 6. the profile the row records is inside the envelope table on disk, recomputed not trusted
    env = PM.load_envelope_table()
    for vi in range(12):
        r = draw_variant(spec, _phantom_row(case="9009"), vi)
        ev = PM.evaluate_profile(r["profile"]["drawn_standing"], env)
        ck(f"envelope_{vi}", ev["in_envelope"], f"an accepted row is out of envelope: "
                                                f"{[k for k, v in ev['rules'].items() if v['status'] == 'fail']}")

    # 7. INJECTED FAULTS: each must be caught by the rule that carries it
    caught = []
    plan = subtype_plan(spec, "ordinary")
    m_bad, jseg, _ = multipliers_for(spec, plan, "IV")
    m_bad[jseg] = 1.0                                                 # a fused junction handed a multiplier of 1
    sh_bad = shares_for(spec, plan, "3", m_bad)
    caught.append(("fused_junction_given_motion", sh_bad.get(jseg, 0.0) > 0))
    caps = {s: _seg_caps(spec, plan["cap_from"][s]) for s in plan["mobile"]}
    over = distribute_ll(spec, plan, sh_bad, caps, m_bad, 400.0, np.random.Generator(np.random.PCG64(1)))
    caught.append(("impossible_dLL_leaves_a_shortfall", abs(over["shortfall"]) > 3.0))
    caught.append(("impossible_dLL_still_respects_caps",
                   all(-caps[s]["flex"] * m_bad[s] - 1e-6 <= v <= caps[s]["ext"] * m_bad[s] + 1e-6
                       for s, v in over["applied"].items())))
    try:
        draw_profile(spec, 200.0, np.random.Generator(np.random.PCG64(2)))     # PI no human has
        caught.append(("absurd_PI_rejected", False))
    except UnusableSource:
        caught.append(("absurd_PI_rejected", True))
    try:
        load_spec_bad = dict(spec)
        load_spec_bad.pop("rom_deg")
        json_p = Path(PM.tempfile.mkdtemp()) / "spec.json"
        json_p.write_text(json.dumps(load_spec_bad), encoding="utf-8")
        load_spec(json_p)
        caught.append(("truncated_spec_refused", False))
    except Exception:
        caught.append(("truncated_spec_refused", True))
    for name, ok in caught:
        checks += 1
        if not ok:
            fails.append(f"INJECTED FAULT NOT CAUGHT: {name}")

    print(f"self-test: {checks} checks over the sampler, {len(caught)} injected faults")
    if fails:
        print("SELF-TEST FAILED:")
        for f in fails[:40]:
            print("  " + f)
        return 1
    print("SELF-TEST OK: determinism, the fused-junction rule, every ROM cap, the compensation sign, the "
          "envelope, and every injected fault behaved as the spec says")
    return 0


# ------------------------------------------------------------------------------------------- outside checks
def check_cohort(spec: dict, n_draws=400) -> int:
    """Measure the sampler against things it did not compute."""
    allrows = [r for r in load_cohort() if r.get("cohort") == "ctsp"]
    rows = [r for r in allrows if plate_sane(spec, r)[0]]
    print(f"CTSP rows {len(allrows)} -> plate-sane sources {len(rows)} "
          f"(dropped {len(allrows) - len(rows)} by the source gate)")
    rng_rows = rows[:n_draws]
    LL, TK, SS, PT, rej, types, unusable = [], [], [], [], [], {}, []
    for i, r in enumerate(rng_rows):
        try:
            d = draw_variant(spec, r, 0)
        except UnusableSource as e:
            unusable.append((r["case"], str(e)))
            continue
        st = d["profile"]["drawn_standing"]
        LL.append(st["LL"]); TK.append(st["TK"]); SS.append(st["SS"]); PT.append(st["PT"])
        rej.append(d["profile"]["rejections"])
        types[st["roussouly_type"]] = types.get(st["roussouly_type"], 0) + 1
    if unusable:
        print(f"unusable sources that passed the gate anyway: {len(unusable)} -- {unusable[:3]}")
    pub = spec["joint_sagittal_model"]["means_sd_standing"]
    print(f"\n{'quantity':<10}{'drawn mean':>12}{'drawn sd':>10}{'published':>18}{'verdict':>10}")
    ok = True
    for name, vals in (("LL", LL), ("TK", TK), ("SS", SS), ("PT", PT)):
        m, s = float(np.mean(vals)), float(np.std(vals, ddof=1))
        pm, ps = float(pub[name][0]), float(pub[name][1])
        # the sampler conditions on THIS cohort's PI, so the mean may shift with the cohort's PI; the SD must not
        # exceed the published SD, and the mean must sit within one published SD
        good = abs(m - pm) <= ps and s <= ps * 1.15
        ok &= good
        print(f"{name:<10}{m:>12.1f}{s:>10.1f}{f'{pm} +/- {ps}':>18}{'ok' if good else 'OFF':>10}")
    print(f"\nrejections per accepted draw: mean {np.mean(rej):.2f}, max {max(rej)}")
    tot = sum(types.values())
    print("Roussouly types drawn: " + ", ".join(f"{k} {v / tot:.1%}" for k, v in sorted(types.items())))
    print("  cohort's own supine-derived shares (spec): type 1/2 60.6 %, type 3 26.1 %, type 4 13.4 %")
    return 0 if ok else 1


def envelope_vs_cohort(spec: dict) -> int:
    """The measurement behind the corrected balance bound: what each candidate rule refuses of REAL people."""
    env = PM.load_envelope_table()
    dLL = float(env["supine_to_standing"]["LL_deg"])
    rng = env["range"]
    rows = [r for r in load_cohort() if r.get("cohort") == "ctsp" and str(r.get("subtype") or "ordinary") == "ordinary"]
    sane = [r for r in rows if plate_sane(spec, r)[0]]
    n = len(sane)
    schwab = pop = 0
    for r in sane:
        PI, PT, SS = float(r["PI"]), float(r["PT"]), float(r["SS"])
        LL = float(r["LL"]) + dLL
        inr = all(float(rng[k]["lo"]) <= v <= float(rng[k]["hi"])
                  for k, v in (("PI", PI), ("PT", PT), ("SS", SS), ("LL", LL)))
        schwab += inr and abs(PI - LL) < 10.0 and PT < 20.0
        pop += inr and -30.0 <= PI - LL <= 20.0 and -8.0 <= PT <= 35.0
    print(f"CTSP ordinary rows {len(rows)} -> plate-sane sources {n}")
    print(f"  Schwab grade-0 as a rejection rule : accepts {schwab}/{n} ({schwab / n:.1%}), "
          f"REFUSES {n - schwab} real people ({(n - schwab) / n:.1%})")
    print(f"  2.5-SD population band (in use)    : accepts {pop}/{n} ({pop / n:.1%}), "
          f"refuses {n - pop} ({(n - pop) / n:.1%})")
    print("\nA balance GRADE is not a reference range. The envelope table gates on the population band and "
          "records the Schwab grade per row (docs/polypose_reference_envelope.json balance).")
    return 0


# ------------------------------------------------------------------------------------------------ the generator
# `generate` runs INSIDE the pinned PolyPose container (GPU): source in, one warped CT + label + body mask + field +
# DRR pair out, and a PENDING manifest row with everything but the invariant verdicts. `finalize` runs the invariant
# checker on that row in the environment the checker was self-tested in (spineps env, CPU) and files the row under
# manifest/ (all pass, validator clean) or manifest_failed/ (anything else), exiting non-zero on failure. The split is
# deliberate: the certifying measurement is made by a second environment, so measured_recorded is also a test that
# the ostk numbers reproduce across two numpy/scipy stacks.
PP_ROOT = "/rs/rs_grp_oschome/go2432/data/polypose"
ROM_FRACTION = 0.7        # largest per-direction cap / published two-direction total over every segment (L3-L4 flex 7.5/11.2)
MANIFEST_SUBTYPES = {"ordinary", "L6", "T13", "lumbar_rib", "four_lumbar", "sacralised_L5",
                     "castellvi_I", "castellvi_II", "castellvi_III", "castellvi_IV"}
POLYPOSE_DEPARTURES = [
    "chunked evaluation of PolyRigid.pose (identical arithmetic; verified per row against the PolyRigid class on a crop)",
    "gravity weights computed on each body's RIGIDLY MOVED mask (the pull-back's output frame), not the source frame",
    "sampling with the corrected voxel-centre convention (-0.5 <= c < n-0.5), cubic B-spline for the CT, nearest for masks",
]


def _vox_centroid_world(mask, affine):
    idx = np.array(np.nonzero(mask), float)
    A = np.asarray(affine, float)
    return (A[:3, :3] @ idx.mean(axis=1) + A[:3, 3]) if idx.shape[1] else None


def rekey_body_mask(body, label, LMAP, min_frac=0.9):
    """The SPINEPS body mask re-keyed to the RELEASE label ids by overlap, restricted to its vertebra's label.

    Why: tools/body_masks.py writes SPINEPS/VERIDAH's own vertebra numbering, which on transitional spines is not the
    release's (0376: the body mask names T10-T13 and L1-L4 where the labels hold T9-T12 and L1-L6). Bridging by id
    or by name then pairs a body with the wrong vertebra -- a finite, plausible, wrong box. Each body component takes
    the vertebra label holding >= min_frac of its voxels; a body straddling two labels is dropped and said so."""
    from ostk.labels import labels_for  # noqa: F401  (import error surfaces here)
    inv = {v: k for k, v in LMAP.items()}
    vert_ids = {i for i, n in inv.items() if PM.VERTEBRA_RE.match(str(n))}
    out = np.zeros(label.shape, dtype=np.asarray(body).dtype)
    table = []
    for b in [int(x) for x in np.unique(body) if x != 0]:
        m = body == b
        vals, cnt = np.unique(label[m], return_counts=True)
        tot = int(m.sum())
        cand = [(int(c), int(v)) for v, c in zip(vals, cnt) if int(v) in vert_ids]
        best = max(cand) if cand else (0, 0)
        frac = best[0] / max(1, tot)
        rec = dict(spineps_id=b, voxels=tot, release_id=best[1] if frac >= min_frac else None,
                   release_name=inv.get(best[1]) if frac >= min_frac else None, overlap=round(frac, 4))
        if frac >= min_frac:
            out[m & (label == best[1])] = best[1]
            rec["renamed"] = b != best[1]
        table.append(rec)
    return out, table


def centroid_S1_slab(label, affine, LMAP, depth_mm=30.0, radius_mm=35.0):
    """Centroid of the top of the sacrum (its S1 segment): sacrum voxels within depth_mm below the S1 superior plate
    and within radius_mm of the plate centre. The whole sacrum's centroid sits near S2-S3, so a hinge built from it
    would put the lumbosacral rotation centre ~25 mm inside the sacrum and shear the last disc."""
    from ostk.geometry import WORLD_SUPERIOR
    from ostk.spine import endplate_from_label
    es = endplate_from_label(label, affine, "S1", "superior", normal_axis=WORLD_SUPERIOR, min_points=30, labels=LMAP)
    if es is None:
        raise UnusableSource("S1 superior plate unavailable: no lumbosacral hinge")
    c, n = np.asarray(es[0], float), np.asarray(es[1], float) / np.linalg.norm(es[1])
    sac = LMAP["S1"] if (label == LMAP["S1"]).any() else LMAP["sacrum"]
    idx = np.array(np.nonzero(label == sac), float)
    A = np.asarray(affine, float)
    P = (A[:3, :3] @ idx + A[:3, 3:4]).T - c
    h = P @ n
    r = np.linalg.norm(P - np.outer(h, n), axis=1)
    sel = (h <= 1.0) & (h >= -depth_mm) & (r <= radius_mm)
    if sel.sum() < 100:
        raise UnusableSource(f"S1 slab has {int(sel.sum())} voxels")
    return (P[sel] + c).mean(axis=0), dict(plate_centre=c.round(3).tolist(), plate_normal=n.round(5).tolist(),
                                           slab_voxels=int(sel.sum()))


def build_transforms(label, affine, LMAP, chain, segments, fused_names, debris_ids):
    """Every label id -> its 4x4 source -> output world motion (FILE world mm), and the rigid bodies for the weights.

    The chain is built from the fixed pelvis upward (T_upper = T_lower @ S_segment), each segment a single rotation
    whose rotation vector is (flex_ext, lat_bend, axial_rot) about world +x, +y, +z through the segment's hinge: the
    midpoint of the two vertebrae's centroids (for X-S1, the S1 slab's). A single rotation vector -- not three
    sequential rotations -- so the relative rotation the checker recovers (rom_bound's rotvec components) is the
    requested triple exactly, not up to a BCH cross term (0.17 deg for a 10 x 2 deg pair, three times the tolerance).
    Ribs move with their vertebra (rib n with T_n), lumbar ribs with L1, debris with the nearest structure, the
    pelvis and every fused vertebra not at all."""
    from scipy.spatial.transform import Rotation
    inv = {v: k for k, v in LMAP.items()}
    ids = [int(i) for i in np.unique(label) if i != 0]
    T = {}
    pelvis = {LMAP[n] for n in PM.PELVIS_NAMES if n in LMAP}
    for i in ids:
        if i in pelvis:
            T[i] = np.eye(4)
    cent = {n: _vox_centroid_world(label == LMAP[n], affine) for n in chain}
    s1c, s1facts = centroid_S1_slab(label, affine, LMAP)
    lower, T_lower = "S1", np.eye(4)
    hinges = {}
    for name in reversed(chain):
        seg = f"{name}-{lower}"
        d = segments.get(seg, {})
        c_lo = s1c if lower == "S1" else cent[lower]
        centre = 0.5 * (cent[name] + c_lo)
        rv = np.radians([float(d.get("flex_ext_deg", 0.0)), float(d.get("lat_bend_deg", 0.0)), float(d.get("axial_rot_deg", 0.0))])
        S = np.eye(4)
        if not (lower == "S1" and name in fused_names) and np.any(rv != 0.0):
            R = Rotation.from_rotvec(rv).as_matrix()
            S[:3, :3] = R
            S[:3, 3] = centre - R @ centre
        T[LMAP[name]] = T_lower @ S
        hinges[seg] = np.round(centre, 3).tolist()
        lower, T_lower = name, T[LMAP[name]]
    owner = {}                                           # label id -> the chain name / 'sacrum' whose body it joins
    thor = [n for n in chain if n.startswith("T")]
    for i in ids:
        n = inv.get(i, "")
        if i in T:
            continue
        if n.startswith("rib_left_") or n.startswith("rib_right_"):
            k = n.rsplit("_", 1)[1]
            if k == "lumbar":
                tgt = "L1" if "L1" in chain else None
            else:
                v = "T13" if k == "13" else f"T{k}"
                tgt = v if v in chain else (min(thor, key=lambda t: abs(PM.LEVEL_ORDER.index(t) - PM.LEVEL_ORDER.index(v))) if thor and v in PM.LEVEL_ORDER else None)
            if tgt is None:
                raise UnusableSource(f"{n}: no vertebra to carry it")
            T[i] = T[LMAP[tgt]]; owner[i] = tgt
        elif i in debris_ids:
            cd = _vox_centroid_world(label == i, affine)
            best, bd = None, math.inf
            for cand in list(chain) + ["sacrum"]:
                cid = LMAP[cand]
                idx = np.array(np.nonzero(label == cid), float)[:, ::17]
                A = np.asarray(affine, float)
                dd = float(np.min(np.linalg.norm((A[:3, :3] @ idx + A[:3, 3:4]).T - cd, axis=1)))
                if dd < bd:
                    best, bd = cand, dd
            T[i] = T[LMAP[best]] if best != "sacrum" else np.eye(4)
            owner[i] = best
        else:
            raise UnusableSource(f"label {i} ({n or 'unnamed'}) has no motion rule (hardware or an unknown id)")
    bodies = []
    for name in chain:
        if name in fused_names:
            continue
        mem = [LMAP[name]] + [i for i, o in owner.items() if o == name]
        bodies.append((sorted(mem), T[LMAP[name]], name))
    sac = [LMAP["sacrum"]] + [LMAP[n] for n in fused_names] + [i for i, o in owner.items() if o == "sacrum"]
    if LMAP.get("coccyx") in ids:
        sac.append(LMAP["coccyx"])
    bodies.append((sorted(set(sac)), np.eye(4), "sacrum" + ("+" + "+".join(fused_names) if fused_names else "")))
    for n in ("left_hip", "right_hip", "femur_left", "femur_right"):
        if LMAP.get(n) in ids:
            bodies.append(([LMAP[n]], np.eye(4), n))
    covered = sorted(i for b in bodies for i in b[0])
    if covered != sorted(ids) or len(covered) != len(set(covered)):
        raise RuntimeError(f"bodies do not partition the labels: missing {sorted(set(ids) - set(covered))}, "
                           f"doubled {sorted(i for i in set(covered) if covered.count(i) > 1)}")
    return T, bodies, dict(hinges_world_mm=hinges, s1=s1facts, owner={str(k): v for k, v in owner.items()})


def noise_ratio(src_ct, out_ct, src_label, out_label, disp, box):
    """High-pass noise SD in soft tissue (-50..120 HU, 2 voxels from any label) of the output over the source, split
    by where the field displaces by > 1 voxel. Trilinear resampling at a random sub-voxel phase lowers white-noise SD
    by up to ~3x; a warped CT that is visibly smoother than a real one is a synthetic tell a network can learn."""
    from scipy import ndimage as ndi
    a = np.asarray(src_ct[box], np.float32)
    b = np.asarray(out_ct[box], np.float32)
    ha = a - ndi.uniform_filter(a, 3)
    hb = b - ndi.uniform_filter(b, 3)
    sa = ndi.binary_erosion((a > -50) & (a < 120) & (src_label[box] == 0), iterations=2)
    sb = ndi.binary_erosion((b > -50) & (b < 120) & (out_label[box] == 0), iterations=2)
    mv = np.linalg.norm(disp[(slice(None),) + box], axis=0) > 1.0
    res = dict(sd_source=float(ha[sa].std()) if sa.any() else None,
               sd_output_moved=float(hb[sb & mv].std()) if (sb & mv).any() else None,
               sd_output_still=float(hb[sb & ~mv].std()) if (sb & ~mv).any() else None,
               n_moved=int((sb & mv).sum()), n_still=int((sb & ~mv).sum()))
    if res["sd_source"] and res["sd_output_moved"]:
        res["ratio_moved"] = round(res["sd_output_moved"] / res["sd_source"], 4)
    if res["sd_source"] and res["sd_output_still"]:
        res["ratio_still"] = round(res["sd_output_still"] / res["sd_source"], 4)
    return res


def _setup_status():
    p = Path(PP_ROOT) / "env" / "export" / "SETUP_STATUS.json"
    return json.loads(p.read_text()) if p.exists() else {}


def environment_block(polypose_commit):
    st = _setup_status()
    fp = PM.environment_fingerprint(polypose_commit)
    lock = str(Path(PP_ROOT) / "env" / "export" / "polypose.requirements.lock.txt")
    inside = os.path.exists("/.singularity.d") or bool(os.environ.get("APPTAINER_CONTAINER") or os.environ.get("SINGULARITY_CONTAINER"))
    return dict(fingerprint=fp["fingerprint"], python=fp["python"], torch=fp["torch"], cuda=fp["cuda"], lock=lock,
                env_hash=st.get("env_hash"),
                container=dict(image=st.get("sif") if inside else None, sha256=st.get("sif_sha256") if inside else None,
                               reason=("ran inside the pinned image (apptainer exec); the image was pulled, not built: "
                                       "build --fakeroot needs an /etc/subuid entry the grid has not granted") if inside
                               else "not run inside the container"))


def cmd_generate(a) -> int:
    """One output: see the section header. Exit 0 = a pending row was written; exit 3 = the source or the stratum is
    unusable/unreachable (recorded under <bank>/refused/, no volume written)."""
    import platform
    import time as _t
    import nibabel as nib
    import torch
    t_start = _t.time()
    sys.path.insert(0, str(HERE))
    import polypose_invariants as INV
    import polypose_warp as PW
    INV.find_ostk()
    from ostk.labels import detect_scheme, labels_for

    torch.manual_seed(0)
    spec = load_spec(a.spec)
    rom, env = PM.load_rom_table(), PM.load_envelope_table()
    coll, case, vi = a.collection, a.case, int(a.variant)
    rid = PM.row_id_for(coll, case, vi)
    seed = PM.seed_for(coll, case, vi)
    target = a.target if a.target != "auto" else TARGETS[(vi // 3) % 3]
    bank = Path(a.bank)
    for d in ("volumes", "fields", "drr", "sources", "pending", "refused", "manifest", "manifest_failed", "ann"):
        (bank / d).mkdir(parents=True, exist_ok=True)

    def refuse(why, kind="unusable"):
        rec = dict(row_id=rid, case=case, variant_index=vi, target=target, kind=kind, reason=str(why),
                   created_utc=_t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()), node=platform.node())
        (bank / "refused" / f"{rid}.json").write_text(json.dumps(rec, indent=1))
        print(f"REFUSED {rid}: {kind}: {why}")
        return 3

    # ---- 1. the source, read, checked on one grid, hashed
    ct_p, lab_p, body_p = (os.path.expanduser(x) for x in (a.ct, a.label, a.body))
    ci, li, bi = nib.load(ct_p), nib.load(lab_p), nib.load(body_p)
    for nm, im in (("ct", ci), ("body", bi)):
        if tuple(im.shape) != tuple(li.shape) or not np.allclose(im.affine, li.affine, atol=1e-3):
            return refuse(f"{nm} grid differs from the label's")
    affine = np.asarray(li.affine, float)
    lab = np.asarray(li.dataobj).astype(np.int16)
    scheme = detect_scheme(lab)
    if scheme != "v10" or (lab == 29).any():
        return refuse(f"label scheme {scheme} (id 29 present: {bool((lab == 29).any())}); v11 required")
    LMAP = labels_for(lab)
    ids = sorted(int(i) for i in np.unique(lab) if i != 0)
    hw = [i for i in ids if 62 <= i <= 68]
    if hw:
        return refuse(f"hardware labels {hw}: no motion rule for implants yet")
    inv = {v: k for k, v in LMAP.items()}
    vcount = {inv[i]: int(np.count_nonzero(lab == i)) for i in ids if PM.VERTEBRA_RE.match(str(inv.get(i, "")))}
    debris_names = [n for n, c in vcount.items() if c < INV.MIN_VERTEBRA_VOXELS]
    chain = [n for n in PM.LEVEL_ORDER if n in vcount and n not in debris_names and n != "S1"]
    sha_in = dict(ct=PM.sha256_file(ct_p), label=PM.sha256_file(lab_p), body=PM.sha256_file(body_p))

    # ---- 2. the flag table's read of this case (never label ids for a fusion)
    flag = None
    if a.flag_table and os.path.exists(os.path.expanduser(a.flag_table)):
        import csv
        for r in csv.DictReader(open(os.path.expanduser(a.flag_table), encoding="utf-8")):
            if r.get("cohort") == "ctsp" and str(r.get("volume_id", "")).zfill(4) == case:
                flag = r
                break
    castellvi = (flag or {}).get("castellvi_type") or None
    lstv_class = (flag or {}).get("lstv_class")
    subtype = a.subtype
    if subtype not in MANIFEST_SUBTYPES:
        return refuse(f"subtype {subtype!r} not one of {sorted(MANIFEST_SUBTYPES)}")

    # ---- 3. measure the source (ostk), span endpoints excluding FOV-cut and fragment vertebrae
    excl0 = set(INV.truncated_levels(lab, LMAP)) | set(INV.fragment_levels(lab, LMAP))
    m0 = INV.measure(lab, affine, labels=LMAP, exclude=excl0)
    if any(m0.get(k) is None for k in ("PI", "SS", "LL")):
        return refuse(f"source PI/SS/LL unmeasured: {m0['flags']}")
    case_row = dict(case=case, PI=m0["PI"], SS=m0["SS"], PT=m0["PT"], LL=m0["LL"], subtype=subtype, castellvi=castellvi,
                    lstv_class=lstv_class, junction_disc=None, TLK_T10L2=None)
    ok, why = plate_sane(spec, dict(case_row, subtype="ordinary" if subtype == "ordinary" else subtype,
                                    PT=m0["PT"]))
    if not ok:
        return refuse("; ".join(why))
    try:
        plan = plan_from_levels(spec, chain)
    except UnusableSource as e:
        return refuse(e)
    # the plan's chain kind must agree with the declared subtype
    kind_ok = {"L6": plan["subtype"] == "L6", "T13": plan["subtype"] == "T13", "four_lumbar": plan["subtype"] == "four_lumbar"}
    if subtype in kind_ok and not kind_ok[subtype]:
        return refuse(f"declared subtype {subtype} but the labels make a {plan['subtype']} chain")
    if subtype not in kind_ok and plan["subtype"] != "ordinary":
        return refuse(f"declared subtype {subtype} but the labels make a {plan['subtype']} chain")
    if subtype == "lumbar_rib" and not any(inv.get(i, "").endswith("_lumbar") for i in ids):
        return refuse("declared lumbar_rib but no lumbar rib label")
    # the TK span the source measurement actually used (measure_sagittal fits T9 down only), so delta_tk_deg is summed
    # over exactly the segments between the two plates it reads
    tk_segs = PM.segments_between(*m0["TK_span"].split("-"), chain) if m0.get("TK_span") else []

    # ---- 4. draw the whole profile; rejected and redrawn until the segments can carry it
    try:
        draw = draw_variant(spec, case_row, vi, coll, plan=plan, target=target, tk_segments=tk_segs, realise=True)
    except Unreachable as e:
        return refuse(e, kind="unreachable")
    except (UnusableSource, RuntimeError) as e:
        return refuse(e)
    segs = draw["requested"]["segments"]
    fused_names = [s.split("-")[0] for s in draw["junction"]["fused_segments"] if s.split("-")[0] in chain]
    jr = PM.junction_rule_for(castellvi, lstv_class, subtype)
    if jr["rule"] == "fused_zero_motion" and not fused_names:
        return refuse("the read says fused but the fused vertebra has no label of its own (it sits inside the sacrum "
                      "label): the frame cannot express that fusion without freezing the mobile level above it")

    # ---- 5. transforms and bodies
    debris_ids = {LMAP[n] for n in debris_names}
    try:
        T, bodies, tf_facts = build_transforms(lab, affine, LMAP, chain, segs, set(fused_names), debris_ids)
    except UnusableSource as e:
        return refuse(e)

    # ---- 6. the re-keyed body mask (release ids), written once per source
    body_raw = np.asarray(bi.dataobj)
    body_rk, rk_table = rekey_body_mask(body_raw, lab, LMAP)
    rk_path = bank / "sources" / f"CTSP_{case}_body_msk_rekeyed.nii.gz"
    if not rk_path.exists():
        hdr = bi.header.copy()
        tmp = rk_path.with_name(rk_path.name + f".tmp{os.getpid()}.nii.gz")
        nib.save(nib.Nifti1Image(body_rk.astype(body_raw.dtype), bi.affine, header=hdr), str(tmp))
        os.replace(tmp, rk_path)
    body_rk = np.asarray(nib.load(str(rk_path)).dataobj)

    # ---- 7. PolyPose: the equivalence check against the class, then the full field and the three volumes
    A_c, iso = PW.centred_affine(ct_p)
    bodies_T = [(b[0], b[1]) for b in bodies]
    ref_name = next((n for n in ("L3", "L2", "L4") if n in chain), chain[-1])
    cvox = np.round(np.linalg.inv(affine) @ np.append(_vox_centroid_world(lab == LMAP[ref_name], affine), 1.0))[:3]
    dev = a.device if a.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
    if dev == "cpu":
        torch.set_num_threads(max(1, int(os.environ.get("SLURM_CPUS_PER_TASK", "4"))))
    eq = PW.verify_equivalence(ct_p, lab_p, bodies_T, affine, cvox, size=64, tmpdir=str(bank / "sources"), kernel=a.kernel,
                               device=dev)
    if not eq["ok"]:
        return refuse(f"chunked field disagrees with the PolyRigid class: {eq}", kind="equivalence_failed")
    ct = np.asarray(ci.dataobj, np.float32)
    zooms = tuple(float(z) for z in li.header.get_zooms()[:3])
    res = PW.warp_volumes(ct, lab, body_rk, affine, A_c, zooms, bodies_T, frame=a.weights_frame, kernel=a.kernel, device=dev)

    # ---- 8. write, on the source grids, never reoriented
    tag = a.tag or ("" if a.weights_frame == "moved" else "srcframe")
    stem = f"{rid}_{tag}" if tag else rid
    outp = dict(ct=bank / "volumes" / f"{stem}_ct.nii.gz", label=bank / "volumes" / f"{stem}_label.nii.gz",
                body=bank / "volumes" / f"{stem}_body_msk.nii.gz", field=bank / "fields" / f"{stem}_field.npz",
                ap=bank / "drr" / f"{stem}_ap.png", lat=bank / "drr" / f"{stem}_lat.png")
    # The released CTs are integer HU stored as float32; the cubic spline returns non-integer HU, which doubles the
    # gzipped size (494 vs 265 MB on 0874) and gives the warped CT a value set no real CT here has. When the source
    # is integer-valued the output is rounded to integer HU: the source's own quantisation, recorded per row.
    samp = ct[::7, ::7, ::7]
    int_src = bool(np.all(samp == np.rint(samp)))
    if int_src:
        res["ct"] = np.rint(res["ct"])
    h = ci.header.copy(); h.set_data_dtype(np.float32)
    nib.save(nib.Nifti1Image(res["ct"].astype(np.float32), ci.affine, header=h), str(outp["ct"]))
    nib.save(nib.Nifti1Image(res["label"].astype(np.asarray(li.dataobj).dtype), li.affine, header=li.header.copy()), str(outp["label"]))
    nib.save(nib.Nifti1Image(res["body"].astype(body_raw.dtype), bi.affine, header=bi.header.copy()), str(outp["body"]))
    np.savez(str(outp["field"]), disp=res["disp"], units=INV.FIELD_UNITS, convention=INV.FIELD_CONVENTION, affine=affine)
    drr = INV.drr_contrast(res["ct"], res["label"], affine, LMAP, png_ap=str(outp["ap"]), png_lat=str(outp["lat"]))

    # ---- 9. measured exactly as the checker will re-measure
    ms, mo = INV.measure_pair(lab, res["label"], affine, LMAP)
    lum_names = [n for n in chain if n.startswith("L")]
    lo_n = next((n for n in lum_names), None)
    box = None
    if lo_n:
        lm = np.isin(lab, [LMAP[n] for n in lum_names])
        bb = INV.bbox_of(lm, pad=40)
        box = bb
    nz = noise_ratio(ct, res["ct"], lab, res["label"], res["disp"], box) if box else None
    rl = draw["profile"]["realised"]

    # ---- 10. the row
    out_files = {k: PM.sha256_file(str(v)) for k, v in outp.items() if k in ("ct", "label", "body", "field")}
    fused_groups = [sorted([LMAP[n], LMAP["sacrum"]]) for n in fused_names]
    row = {
        "schema": PM.SCHEMA, "row_id": rid, "created_utc": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()),
        "node": platform.node(), "wall_seconds": 0.0, "argv": sys.argv,
        "source": {"collection": coll, "case": case, "series": None, "patient_key": f"ctsp_release/{case}",
                   "label_scheme": "v11", "subtype": subtype, "castellvi_type": castellvi,
                   "lstv_class": lstv_class, "truth": "lstv_flag_labels_v2.csv (castellvi_type, lstv_class, lstv_label) + the "
                   "release label's own vertebrae (plan_from_levels)",
                   "flag_table_sha256": PM.sha256_file(os.path.expanduser(a.flag_table)) if flag else None,
                   "flag_row": {k: flag.get(k) for k in ("lstv_label", "lstv_class", "castellvi_type", "castellvi_agreement",
                                                         "has_L6", "n_lumbar_labelled", "has_lumbar_rib", "LSTV_flag", "TLTV_flag",
                                                         "vertebrae_present", "config")} if flag else None,
                   "ct": {"path": ct_p, "sha256": sha_in["ct"]}, "label": {"path": lab_p, "sha256": sha_in["label"]},
                   "body_mask": {"path": str(rk_path), "sha256": PM.sha256_file(str(rk_path))},
                   "body_mask_spineps": {"path": body_p, "sha256": sha_in["body"], "rekey": rk_table,
                                         "renamed": sum(1 for r in rk_table if r.get("renamed")),
                                         "dropped": [r["spineps_id"] for r in rk_table if r["release_id"] is None]},
                   "debris_ids": sorted(debris_ids), "debris": {n: vcount[n] for n in debris_names},
                   "levels": chain, "span_endpoint_excluded": sorted(excl0)},
        "variant_index": vi, "seed": seed, "seed_policy": PM.SEED_POLICY,
        "requested": {"segments": segs, "delta_ll_deg": round(rl["delta_ll_deg"], 6), "delta_tk_deg": round(rl["delta_tk_deg"], 6),
                      "rom_fraction": ROM_FRACTION, "tk_span_segments": tk_segs,
                      "target": target, "ll_band": draw["ll_band"], "ll_quantile": draw["profile"]["ll_quantile"],
                      "delta_ll_model_supine_deg": draw["requested"]["delta_ll_deg"],
                      "delta_tlk_t10l1_deg": draw["requested"]["delta_tlk_t10l1_deg"],
                      "caps_used": draw["requested"]["caps_used"], "multipliers": draw["requested"]["multipliers"],
                      "per_segment_requested": draw["requested"]["per_segment_requested"]},
        "profile": {"model": draw["profile"]["model"], "posture": "supine",
                    "supine_to_standing": {"LL_deg": -draw["profile"]["supine_offsets"]["LL"],
                                           "SS_deg": -draw["profile"]["supine_offsets"]["SS"],
                                           "TK_deg": -draw["profile"]["supine_offsets"]["TK"],
                                           "source": "sampling_spec.json supine_conversion.draw, one draw per output"},
                    "source_standing": rl["source_standing"], "drawn": rl["drawn"], "delta": rl["delta"],
                    "realisation": "implicit_trunk_over_pelvis",
                    "realisation_note": spec["image_space_realisation"]["PT_star_is_not_an_image_quantity"],
                    "envelope": rl["envelope"], "in_envelope": rl["in_envelope"], "unverified_bounds": rl["unverified_bounds"],
                    "shortfall": rl["shortfall"], "model_draw_standing": draw["profile"]["drawn_standing"],
                    "roussouly_type": draw["profile"]["roussouly_type"], "shares": draw["profile"]["shares"],
                    "rejections": draw["profile"]["rejections"], "stratum_misses": draw["profile"]["stratum_misses"],
                    "realise_rejections": draw["profile"]["realise_rejections"],
                    "realise_rejection_reasons": draw["profile"]["realise_rejection_reasons"]},
        "junction": {"rule": jr["rule"], "reason": jr["reason"], "fused_groups": fused_groups,
                     "last_presacral": chain[-1], "segment": draw["junction"]["segment"],
                     "multiplier": draw["junction"]["multiplier"]},
        "applied_transforms": {str(k): np.asarray(v, float).tolist() for k, v in sorted(T.items())},
        "bodies": [{"name": b[2], "ids": b[0]} for b in bodies],
        "polypose": {"repo": PM.POLYPOSE_REPO, "commit": _setup_status().get("polypose_sha", a.polypose_commit),
                     "licence": "MIT", "departures": POLYPOSE_DEPARTURES, "weights_frame": a.weights_frame,
                     "kernel": a.kernel, "kernel_source": "polypose.weights.weights." + ("gravity" if a.kernel == "gravity" else "inverse_distance"),
                     "tag": tag or None, "equivalence": eq,
                     "warp": res["facts"], "centred_affine_isocenter": iso.round(4).tolist()},
        "sampler": {"version": SAMPLER_VERSION, "commit": a.sampler_commit,
                    "files_sha256": {Path(f).name: PM.sha256_file(str(HERE / f)) for f in
                                     ("polypose_sample.py", "polypose_warp.py", "polypose_invariants.py", "polypose_manifest.py")},
                    "spec": {"path": spec["__path__"], "sha256": spec["__sha256__"]},
                    "rom_table": {"path": rom["__path__"], "sha256": rom["__sha256__"]},
                    "envelope": {"path": env["__path__"], "sha256": env["__sha256__"]},
                    "hinges": tf_facts},
        "environment": environment_block(_setup_status().get("polypose_sha", a.polypose_commit)),
        "outputs": {"ct": {"path": str(outp["ct"]), "sha256": out_files["ct"]},
                    "label": {"path": str(outp["label"]), "sha256": out_files["label"]},
                    "body_mask": {"path": str(outp["body"]), "sha256": out_files["body"]},
                    "field": {"path": str(outp["field"]), "sha256": out_files["field"]},
                    "drr_ap": {"path": str(outp["ap"])}, "drr_lat": {"path": str(outp["lat"])}},
        "measured": {"method": "tools/polypose_invariants.py measure_pair (ostk pi-v1 core; signed Cobb from ostk end plates; "
                               "span endpoints exclude FOV-cut and fragment vertebrae in either volume)",
                     "source": {k: v for k, v in ms.items() if k != "lr_axis"},
                     "output": {k: v for k, v in mo.items() if k != "lr_axis"},
                     "source_pre_draw": {k: m0[k] for k in ("PI", "SS", "PT", "LL", "TK", "TK_span", "flags")}},
        "quality": {"noise": nz, "fov_out_voxels": res["facts"]["fov_out_voxels"], "ct_rounded_to_integer_hu": int_src,
                    "fov_out_body_voxels": int(np.count_nonzero(res["fov_out"] & (ct > -500))) if res.get("fov_out") is not None else None,
                    "drr_contrast": {k: v for k, v in drr.items() if k != "finite"}},
        "tolerances": dict(PM.TOLERANCE_DEFAULTS),
        "invariants": {}, "all_pass": False,
    }
    row["wall_seconds"] = round(_t.time() - t_start, 1)
    pend = bank / "pending" / f"{stem}.json"
    pend.write_text(json.dumps(row, indent=1, default=float))
    print(f"PENDING {stem} {row['wall_seconds']} s  dLL {row['requested']['delta_ll_deg']:+.2f}  target {target}  "
          f"folds? see finalize  eq {eq['max_coord_diff_vox']:.2e} vox  -> {pend}")
    return 0


def cmd_finalize(a) -> int:
    """Run every invariant on a pending row in THIS environment, fill the verdicts, validate, file the row."""
    import platform
    import time as _t
    sys.path.insert(0, str(HERE))
    import polypose_invariants as INV
    INV.find_ostk()
    row = json.loads(Path(a.row).read_text())
    rom, env = PM.load_rom_table(), PM.load_envelope_table()
    t0 = _t.time()
    chk = INV.RowCheck(row, rom, env, render_dir=None, verbose=True)
    res = chk.run()
    INV.finish_row(row, res)
    probs = PM.validate_row(row, rom, env)
    row["check"] = dict(checker=INV.CHECKER_VERSION, node=platform.node(), python=sys.version.split()[0],
                        seconds=round(_t.time() - t0, 1), validator_problems=probs,
                        at=_t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()))
    bank = Path(a.bank)
    good = row["all_pass"] and not probs
    diag = row.get("polypose", {}).get("weights_frame", "moved") != "moved" or bool(row.get("polypose", {}).get("tag"))
    # a source-frame DIAGNOSTIC row shares its row_id with the bank row it shadows: it is filed apart, never in the
    # manifest, so the bank cannot hold two rows with one id
    dest_dir = bank / ("diagnostics" if diag else ("manifest" if good else "manifest_failed"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{Path(a.row).stem}.jsonl"
    dest.write_text(json.dumps(row, default=float) + "\n")
    if good and not diag:
        for role, rec in row["outputs"].items():
            p = rec.get("path")
            if p:
                json.dump(dict(PM.ledger_sidecar(row), role=role), open(bank / "ann" / f"{PM._output_stem(p)}.json", "w"), indent=1)
    failed = sorted(k for k, v in res.items() if v["status"] == "fail")
    for p in probs:
        print("VALIDATOR", p)
    print(("ROW_OK " if good else "ROW_FAIL ") + row["row_id"] + (f" failed={failed}" if failed else "") + f" -> {dest}")
    return 0 if good else 1


def cmd_head(a) -> int:
    rom, env = PM.load_rom_table(), PM.load_envelope_table()
    commit = _setup_status().get("polypose_sha", a.polypose_commit)
    head = dict(schema=PM.SCHEMA, created_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                polypose=dict(repo=PM.POLYPOSE_REPO, commit=commit), sampler=dict(version=SAMPLER_VERSION, commit=a.sampler_commit),
                rom_table=dict(path=rom["__path__"], sha256=rom["__sha256__"]),
                envelope=dict(path=env["__path__"], sha256=env["__sha256__"]),
                environment=environment_block(commit))
    Path(a.bank).mkdir(parents=True, exist_ok=True)
    (Path(a.bank) / "BANK_HEAD.json").write_text(json.dumps(head, indent=1))
    print(json.dumps(head, indent=1))
    return 0


# --------------------------------------------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", default=str(SPEC_DEFAULT))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("self-test")
    sub.add_parser("check-cohort")
    sub.add_parser("envelope-vs-cohort")
    d = sub.add_parser("draw")
    d.add_argument("--case", required=True)
    d.add_argument("--variant", type=int, default=0)
    d.add_argument("--collection", default="ctsp")
    p = sub.add_parser("plan")
    p.add_argument("--out", required=True)
    p.add_argument("--variants", type=int, default=4)
    g = sub.add_parser("generate", help="one warped output + a pending manifest row (inside the PolyPose container, GPU)")
    g.add_argument("--collection", default="ctsp")
    g.add_argument("--case", required=True)
    g.add_argument("--variant", type=int, required=True)
    g.add_argument("--target", default="auto", choices=("auto",) + TARGETS,
                   help="conditional-LL stratum; auto = TARGETS[(variant // 3) mod 3]")
    g.add_argument("--subtype", required=True, help="manifest subtype: " + ", ".join(sorted(MANIFEST_SUBTYPES)))
    g.add_argument("--ct", required=True)
    g.add_argument("--label", required=True)
    g.add_argument("--body", required=True, help="SPINEPS body mask (tools/body_masks.py); re-keyed to release ids here")
    g.add_argument("--bank", required=True)
    g.add_argument("--flag-table", default=str(ROOT / "SchwingNet/results/polypose/inputs/lstv_flag_labels_v2.csv"))
    g.add_argument("--weights-frame", default="moved", choices=("moved", "source"))
    g.add_argument("--kernel", default=os.environ.get("PP_KERNEL", "gravity"),
                   help="PolyPose weight kernel: gravity (the paper's) or invdf:<eps> (mm^-2)")
    g.add_argument("--tag", default="", help="diagnostic suffix: the row is filed under diagnostics/, never the manifest")
    g.add_argument("--device", default=os.environ.get("PP_DEVICE", "auto"), choices=("auto", "cuda", "cpu"))
    g.add_argument("--sampler-commit", default="0000000")
    g.add_argument("--polypose-commit", default="909a9bb2eeccf05065c7bc1d3703fb99f87b35b9")
    f = sub.add_parser("finalize", help="run every invariant on a pending row and file it (checker environment, CPU)")
    f.add_argument("--row", required=True)
    f.add_argument("--bank", required=True)
    h = sub.add_parser("head", help="write <bank>/BANK_HEAD.json from this environment")
    h.add_argument("--bank", required=True)
    h.add_argument("--sampler-commit", default="0000000")
    h.add_argument("--polypose-commit", default="909a9bb2eeccf05065c7bc1d3703fb99f87b35b9")
    a = ap.parse_args()
    if a.cmd == "generate":
        return cmd_generate(a)
    if a.cmd == "finalize":
        return cmd_finalize(a)
    if a.cmd == "head":
        return cmd_head(a)
    spec = load_spec(a.spec)

    if a.cmd == "self-test":
        return self_test(spec)
    if a.cmd == "check-cohort":
        return check_cohort(spec)
    if a.cmd == "envelope-vs-cohort":
        return envelope_vs_cohort(spec)
    if a.cmd == "draw":
        rows = {str(r["case"]): r for r in load_cohort() if r.get("cohort") == a.collection}
        r = rows.get(str(a.case))
        if r is None:
            print(f"no measured row for {a.collection} case {a.case}", file=sys.stderr)
            return 2
        ok, why = plate_sane(spec, r)
        if not ok:
            print(f"case {a.case} is not a usable source: {'; '.join(why)}", file=sys.stderr)
            return 3
        print(json.dumps(draw_variant(spec, r, a.variant, a.collection), indent=1))
        return 0
    if a.cmd == "plan":
        rows = [r for r in load_cohort() if plate_sane(spec, r)[0]]
        n = 0
        with open(a.out, "w", encoding="utf-8") as fh:
            for r in rows:
                for vi in range(a.variants):
                    fh.write(json.dumps(draw_variant(spec, r, vi, r.get("cohort", "ctsp"))) + "\n")
                    n += 1
        print(f"{n} draws over {len(rows)} sources -> {a.out}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
