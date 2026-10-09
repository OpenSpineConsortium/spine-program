# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/level_flags.py [tracked at 097933a]
"""Frame-level flags computed from a decoded run: the conditions under which a level call should not be trusted.

WHY THESE EXIST, AND WHY THEY ARE RULES. The scoping review's sharpest finding is that countermeasures aimed at
the imaging step are named constantly and, in 15 of 15 sources, never evaluated against an outcome; organisational
countermeasures are evaluated in 7 of 18. So a countermeasure aimed at the imaging step is only worth adding if it
comes with a measured operating point. Rules can be measured against the render ground truth today, on thousands
of cases, without waiting for a training run or a new label set. Every flag below is therefore a deterministic
function of the decoded run, with its threshold written down here and its behaviour reported by
tools/eval_level_flags.py.

WHAT A FLAG IS AND IS NOT. A flag never renames a vertebra and never changes a level. It says "the condition this
call depends on is not met here": count the whole spine, get another view, or check the cross-sectional study. It
abstains when the frame cannot carry the call at all, which is a different output from "quiet" and is reported
separately -- a flag that silently reads "negative" on a frame that could never have shown the finding is the
failure this project keeps meeting in other forms.

THE MECHANISMS EACH ONE TARGETS, from the review's charted data:

  no_reference_landmark    "count from a fixed landmark" is the most frequently named countermeasure in the
                           corpus. It cannot be executed at all when no landmark is in the field, and a frame
                           with no sacrum and no C2 is exactly that. This flag makes the precondition explicit
                           instead of letting the decoder count from an assumed start.

  lumbar_count_anomaly     transitional anatomy is implicated in 20.7% of sources reporting a wrong-level event,
                           and 39.0% of lumbosacral ones. Six lumbar-type bodies above the sacrum is the
                           numerical phenotype. Needs the sacrum and a thoracolumbar junction in the run.

  count_vs_morphology      the project's own thesis, as a flag. The anchored decode uses the sequence; the
                           single-crop call uses only what the bone looks like. When a run's two readings
                           disagree on many vertebrae, the sequence and the morphology are telling different
                           stories, which is what a transitional or miscounted spine does.

  direction_unknown        a count is a direction plus a start. When the orientation net cannot say which way is
                           cranial, the count is ambiguous no matter how good the classifier is.

  hardware_in_field        previous instrumentation is a named mechanism: it changes the reference the surgeon
                           counts from, and a level already operated is the level most likely to be re-entered.

  low_confidence_run       out-of-domain frames are where a classifier collapses to its majority class, and the
                           collapse looks like a confident answer unless the run's own confidence is read.

THRESHOLDS. Each is a named constant with the reasoning next to it. They are defaults, not findings; anything
that claims an operating point has to come from eval_level_flags.py on held-out data.
"""
from __future__ import annotations

from collections import Counter

# A run shorter than this cannot support a disagreement rate: one disagreement in two vertebrae is 50%.
MIN_RUN_FOR_DISAGREEMENT = 4
# Fraction of the run where the counted name and the morphology name differ. The decode and the single-crop call
# agree almost everywhere on an ordinary spine, so a quarter of the run disagreeing is a loud signal rather than
# the usual one-off at a run's cut end.
DISAGREEMENT_FIRE = 0.25
# Median decoded probability below which the run is treated as unreliable rather than merely uncertain. The
# per-vertebra abstain already uses 0.5; this is the whole-frame version and is deliberately lower, so it fires
# on runs that are bad throughout rather than on runs with two weak members.
LOW_CONF_MEDIAN = 0.35

LUMBAR = [f"L{i}" for i in range(1, 7)]
CERVICAL = [f"C{i}" for i in range(1, 8)]


def _median(xs):
    xs = sorted(xs)
    if not xs:
        return 0.0
    n = len(xs)
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


# WHAT A FLAG CLAIMS TO DETECT, AND WHY THE DISTINCTION IS LOAD-BEARING.
#   "transitional"  the flag asserts something about the ANATOMY. A sensitivity and specificity against known
#                   transitional cases is the right way to report it, and is meaningful.
#   "precondition"  the flag asserts something about the IMAGE or the PIPELINE: no landmark in the field, unknown
#                   direction, hardware present, a run the classifier cannot read. Scoring one of these against
#                   transitional anatomy produces a number that looks like a detector's and is not. Measured on
#                   held-out renders, `no_reference_landmark` fires on 83% of six-lumbar cases and 23% of normal
#                   ones, which reads as 71% sensitivity -- but it is detecting how those cases were framed, not
#                   their anatomy. Reporting it as an LSTV detector would be a finite, plausible, wrong number.
# Evaluators must read this field and report the two kinds differently.
DETECTS = {
    "no_reference_landmark": "precondition",
    "lumbar_count_anomaly": "transitional",
    "count_vs_morphology": "transitional",
    "direction_unknown": "precondition",
    "hardware_in_field": "precondition",
    "low_confidence_run": "precondition",
}


def _entry(target, fired, abstain, reason, needs=None, missing=None, **evidence):
    return {"target": target, "kind": "rule", "detects": DETECTS.get(target, "precondition"),
            "flag": bool(fired), "abstain": bool(abstain),
            "needs": needs or [], "missing_in_frame": missing or [], "reason": reason,
            "evidence": {k: v for k, v in evidence.items()}}


def rule_flags(vert, direction_known=True, hw_boxes=None, thresholds=None):
    """Every rule flag for one frame.

    `vert` is the prototype's per-vertebra list: each item carries `level` (the decoded, counted name),
    `single_crop` (the morphology-only name), `level_prob` and `abstain`. Nothing else is read, so this runs
    identically inside the prototype and inside an offline evaluator over stored runs.
    """
    t = {"disagreement": DISAGREEMENT_FIRE, "low_conf": LOW_CONF_MEDIAN, **(thresholds or {})}
    out = []
    named = [v["level"] for v in vert]
    named_set = set(named)
    n = len(vert)

    # --- 1. is there anything in the field to count from
    has_sacrum = "sacrum" in named_set
    has_c2 = "C2" in named_set
    out.append(_entry(
        # An empty run ABSTAINS and does not fire: "no landmark was detected" and "no vertebra was detected at
        # all" are different statements, and reporting the second as the first would blame the field of view for
        # a detector failure.
        "no_reference_landmark", fired=(n > 0 and not (has_sacrum or has_c2)), abstain=(n == 0),
        reason=("no vertebra was detected, so whether a landmark is in the field cannot be said" if n == 0 else
                "no fixed landmark in the field: neither the sacrum nor C2 is among the named vertebrae, so a "
                "count has no anchor and the level names rest on the classifier alone"
                if not (has_sacrum or has_c2) else
                "a countable landmark is in the field"),
        n_vertebrae=n, sacrum_in_frame=has_sacrum, c2_in_frame=has_c2))

    # --- 2. six lumbar-type bodies above the sacrum
    # Needs BOTH ends: without the sacrum there is no bottom to count to, and without a thoracic name above the
    # lumbar run the top of the lumbar column is merely the top of the frame. Abstaining here is the common case
    # on a collimated intra-operative frame, and saying so is the point.
    lumbar_named = [x for x in named if x in LUMBAR]
    has_thoracic_above = any(x.startswith("T") for x in named)
    missing = []
    if not has_sacrum:
        missing.append("sacrum")
    if not has_thoracic_above:
        missing.append("a thoracic level above the lumbar run")
    n_lumbar = len(set(lumbar_named))
    out.append(_entry(
        "lumbar_count_anomaly", fired=(not missing and n_lumbar >= 6), abstain=bool(missing),
        needs=["sacrum", "thoracic level"], missing=missing,
        reason=("six or more distinct lumbar-type bodies are named between the thoracic spine and the sacrum, "
                "which is the numerical phenotype of a transitional lumbosacral segment: count the whole spine "
                "or check the cross-sectional study" if (not missing and n_lumbar >= 6) else
                ("the frame does not show both ends of the lumbar column, so the count cannot be made"
                 if missing else "the lumbar count between the thoracic spine and the sacrum is not anomalous")),
        distinct_lumbar_named=n_lumbar, lumbar_names=sorted(set(lumbar_named))))

    # --- 3. the counted name and the morphology name disagree across the run
    pairs = [(v["level"], v.get("single_crop")) for v in vert if v.get("single_crop")]
    ndis = sum(1 for a, b in pairs if a != b)
    frac = (ndis / len(pairs)) if pairs else 0.0
    short = len(pairs) < MIN_RUN_FOR_DISAGREEMENT
    out.append(_entry(
        "count_vs_morphology", fired=(not short and frac >= t["disagreement"]), abstain=short,
        needs=[f"at least {MIN_RUN_FOR_DISAGREEMENT} vertebrae"],
        missing=([f"only {len(pairs)} vertebrae in the run"] if short else []),
        reason=(f"the counted names and the shape-only names disagree on {ndis} of {len(pairs)} vertebrae "
                f"({100 * frac:.0f}%): the sequence and the bone are telling different stories, which is what a "
                f"transitional or miscounted column does" if (not short and frac >= t["disagreement"]) else
                ("the run is too short for a disagreement rate to mean anything" if short else
                 f"counted and shape-only names agree on {len(pairs) - ndis} of {len(pairs)} vertebrae")),
        n_disagreements=ndis, n_compared=len(pairs), disagreement_fraction=round(frac, 3)))

    # --- 4. direction
    out.append(_entry(
        "direction_unknown", fired=(not direction_known), abstain=False,
        reason=("the orientation step could not establish which way is cranial, so the direction of any count is "
                "unknown and the names could be the run read backwards"
                if not direction_known else "cranial-caudal direction was established"),
        direction_known=bool(direction_known)))

    # --- 5. hardware
    hw = list(hw_boxes or [])
    out.append(_entry(
        "hardware_in_field", fired=bool(hw), abstain=False,
        reason=(f"{len(hw)} hardware object(s) in the field: previous instrumentation changes the landmark the "
                f"count runs from, and an already-operated level is the one most likely to be re-entered"
                if hw else "no hardware detected in the field"),
        n_hardware=len(hw)))

    # --- 6. whole-run confidence
    probs = [float(v.get("level_prob") or 0.0) for v in vert]
    med = _median(probs)
    n_abstain = sum(1 for v in vert if v.get("abstain"))
    out.append(_entry(
        "low_confidence_run", fired=(n > 0 and med < t["low_conf"]), abstain=(n == 0),
        reason=(f"the run's median decoded probability is {med:.2f}, below {t['low_conf']:.2f}: this frame is "
                f"outside what the classifier can read, and a confident-looking name here is the majority class "
                f"rather than a reading" if (n > 0 and med < t["low_conf"]) else
                ("no vertebra was detected" if n == 0 else
                 f"the run's median decoded probability is {med:.2f}")),
        median_level_prob=round(med, 3), n_vertebrae=n, n_vertebrae_abstained=n_abstain))

    return out


def summarise(flags):
    """One line per frame: which flags fired, which abstained. For a log or a report table."""
    fired = [f["target"] for f in flags if f.get("flag")]
    abst = [f["target"] for f in flags if f.get("abstain")]
    return {"fired": fired, "abstained": abst, "n_fired": len(fired),
            "counts": Counter([f["target"] for f in flags if f.get("flag")])}
