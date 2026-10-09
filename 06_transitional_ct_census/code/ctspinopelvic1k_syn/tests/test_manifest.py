# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K-Syn (local git, no remote) tests/test_manifest.py; commit 7098eb1 of 2026-06-11; this folder is the only copy. The banned word, where it occurred, is rewritten as origin.
"""Tests for the synthetic-case tagging + split-leak guard (the correctness
-critical piece). These run without the heavy deps."""
from ctspino_syn import castellvi
from ctspino_syn.manifest import (
    make_case_id, is_synthetic, SynthManifest, SynthOrigin,
    audit_splits_no_synth_leak, SYNTH_PREFIX,
)


def test_caseid_is_tagged_and_detected():
    cid = make_case_id("IIb", "B", "COLONOG_0123", 7)
    assert cid.startswith(SYNTH_PREFIX)
    assert is_synthetic(cid)
    assert not is_synthetic("COLONOG_0123")          # a real case


def test_manifest_rejects_untagged_record():
    m = SynthManifest(label_scheme="merged-v6")
    bad = SynthOrigin(
        case_id="COLONOG_0123",  # not SYNTH_-prefixed
        class_code="IIb", type_roman="II", method="procedural",
        realized_side="bilateral", recipient_token="COLONOG_0123",
        donor_token=None, seed=0, blend="poisson", refined=False,
        label_scheme="merged-v6")
    try:
        m.add(bad)
    except ValueError:
        return
    raise AssertionError("manifest should reject a non-SYNTH_ caseID")


def test_audit_catches_synth_in_val_and_test():
    splits = [
        {"train": ["COLONOG_1", make_case_id("IIb", "B", "COLONOG_1", 0)],
         "val":   ["COLONOG_2", make_case_id("IIIa", "U", "COLONOG_3", 0)]},
        {"train": ["COLONOG_2"],
         "test":  [make_case_id("Ia", "U", "COLONOG_4", 0)]},
    ]
    violations = audit_splits_no_synth_leak(splits)
    assert len(violations) == 2          # one in val, one in test
    # a clean split passes
    assert audit_splits_no_synth_leak(
        [{"train": [make_case_id("IIb", "B", "COLONOG_1", 0)], "val": ["COLONOG_2"]}]
    ) == []


def test_castellvi_matrix_complete():
    codes = castellvi.all_codes()
    assert codes == ["Ia", "Ib", "IIa", "IIb", "IIIa", "IIIb", "IV"]
    assert castellvi.CLASS_BY_CODE["IV"].is_mixed
    assert castellvi.CLASS_BY_CODE["Ia"].unilateral
