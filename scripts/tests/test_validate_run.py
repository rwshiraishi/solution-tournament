"""Tests for validate_run.py — the tournament-output validator."""

import pathlib
import sys
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import validate_run  # noqa: E402

# A minimal lightweight transcript that must PASS. Block formats are
# defined by templates/run-skeleton.md.
PASSING_LIGHTWEIGHT = """\
# tournament output

```st:meta
mode: lightweight
run_shape: attended-lightweight
```

pack-v1 sha256 4f2ad9c1b7e8f6a2c3d4e5f60718293a4b5c6d7e8f9012345678901234567890

```st:weights
root-cause 0.35
robustness 0.25
maintainability 0.20
risk 0.20
```

```st:matrix
A | root-cause=7 robustness=6 maintainability=8 risk=7 | total=6.95
B | root-cause=5 robustness=7 maintainability=6 risk=6 | total=5.90
C | root-cause=4 robustness=5 maintainability=7 risk=8 | total=5.65
```

near-miss sweep: 8 of 8 thresholds evaluated — decisive margin, 5.0 floor, 0.3 tiebreak band, majority-OPINION weight stop, recompute discrepancy, pre-commitment width rule, cap-magnitude-vs-margin, each active counter — none within band

disclosure: self-administered EXCEPT the user's checks

counters: reopen 0 of 1 · re-entry 0 of 1 · re-scores 0 of 2 · post-freeze mutation 0 of 1 · scoring rounds 1 of 1 · subagent-only counters n/a (no subagents)

checklist: 15 of 15
"""


def strikes(text: str, mode: str = "lightweight") -> list:
    return validate_run.validate(text, mode)


class TestPassing(unittest.TestCase):
    def test_minimal_lightweight_passes(self) -> None:
        self.assertEqual(strikes(PASSING_LIGHTWEIGHT), [])


class TestStrikes(unittest.TestCase):
    def test_bad_total_recomputation(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("total=6.95", "total=7.40")
        self.assertTrue(any("total" in s for s in strikes(bad)))

    def test_incomplete_checklist(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("checklist: 15 of 15", "checklist: 14 of 15")
        self.assertTrue(any("checklist" in s for s in strikes(bad)))

    def test_missing_disclosure(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("disclosure: self-administered EXCEPT the user's checks\n", "")
        self.assertTrue(any("disclosure" in s for s in strikes(bad)))

    def test_missing_pack_hash(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("pack-v1 sha256 4f2ad9c1b7e8f6a2c3d4e5f60718293a4b5c6d7e8f9012345678901234567890", "")
        self.assertTrue(any("hash" in s for s in strikes(bad)))

    def test_sweep_count_mismatch(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("8 of 8 thresholds", "7 of 8 thresholds")
        self.assertTrue(any("sweep" in s for s in strikes(bad)))

    def test_missing_sweep_threshold_name(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("recompute discrepancy, ", "")
        self.assertTrue(any("recompute discrepancy" in s for s in strikes(bad)))

    def test_missing_counters_line(self) -> None:
        bad = "\n".join(l for l in PASSING_LIGHTWEIGHT.splitlines() if not l.startswith("counters:"))
        self.assertTrue(any("counters" in s for s in strikes(bad)))

    def test_weights_not_normalized(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("risk 0.20", "risk 0.30")
        self.assertTrue(any("weights" in s for s in strikes(bad)))

    def test_no_execution_hash_fallback_accepted(self) -> None:
        ok = PASSING_LIGHTWEIGHT.replace(
            "pack-v1 sha256 4f2ad9c1b7e8f6a2c3d4e5f60718293a4b5c6d7e8f9012345678901234567890",
            "pack hash unavailable — no execution tool",
        )
        self.assertEqual(strikes(ok), [])


class TestReviewerRegressions(unittest.TestCase):
    """Cases from the 2026-08-13 python-review findings."""

    def test_sweep_as_last_line_without_trailing_newline(self) -> None:
        # HIGH: text.find("\n") == -1 used to truncate the final char,
        # producing a false "missing threshold name" strike.
        reordered = PASSING_LIGHTWEIGHT.splitlines()
        sweep = next(l for l in reordered if l.startswith("near-miss sweep"))
        rest = [l for l in reordered if not l.startswith("near-miss sweep")]
        text = "\n".join(rest + [sweep])  # sweep last, no trailing newline
        self.assertEqual(strikes(text), [])

    def test_malformed_weight_value_strikes_instead_of_crashing(self) -> None:
        # HIGH: "0.3.5" used to crash float() with an uncaught ValueError.
        bad = PASSING_LIGHTWEIGHT.replace("robustness 0.25", "robustness 0.2.5")
        found = strikes(bad)  # must not raise
        self.assertTrue(any("malformed weights line" in s for s in found), found)

    def test_malformed_matrix_score_strikes_instead_of_crashing(self) -> None:
        bad = PASSING_LIGHTWEIGHT.replace("root-cause=7 ", "root-cause=7.0.1 ")
        found = strikes(bad)  # must not raise
        self.assertTrue(any("missing dimensions" in s for s in found), found)


class TestFullMode(unittest.TestCase):
    def test_full_requires_gate_order_diff(self) -> None:
        full = PASSING_LIGHTWEIGHT.replace("mode: lightweight", "mode: full").replace(
            "run_shape: attended-lightweight", "run_shape: attended-full"
        ).replace("disclosure: self-administered EXCEPT the user's checks", "").replace(
            "checklist: 15 of 15",
            "checklist: 9 of 9 · 4 of 4 · 6 of 6 · 6 of 6 · 7 of 7 · 9 of 9 · 7 of 7",
        )
        found = validate_run.validate(full, "full")
        self.assertTrue(any("gate-order" in s for s in found))
        with_ledger = full + "\ngate-order diff: 9 ticks / 9 artifact IDs matched\n"
        found2 = validate_run.validate(with_ledger, "full")
        self.assertFalse(any("gate-order" in s for s in found2), found2)

    def test_full_checklist_below_denominator(self) -> None:
        full = PASSING_LIGHTWEIGHT.replace("mode: lightweight", "mode: full").replace(
            "run_shape: attended-lightweight", "run_shape: attended-full"
        ).replace("disclosure: self-administered EXCEPT the user's checks", "").replace(
            "checklist: 15 of 15",
            "checklist: 9 of 9 · 4 of 4 · 5 of 6 · 6 of 6 · 7 of 7 · 9 of 9 · 7 of 7",
        ) + "\ngate-order diff: 9 ticks / 9 artifact IDs matched\n"
        self.assertTrue(any("checklist" in s for s in validate_run.validate(full, "full")))


if __name__ == "__main__":
    unittest.main()
