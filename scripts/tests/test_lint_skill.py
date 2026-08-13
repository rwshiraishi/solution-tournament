"""Tests for lint_skill.py.

Regression cases are seeded from real defects found and fixed during the
2026-08-13 wiring audit: the full-mode header timing contradiction and
the stale script line-count claim in the README.
"""

import pathlib
import shutil
import sys
import tempfile
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import lint_skill  # noqa: E402

SKILL_ROOT = SCRIPTS_DIR.parent
REPO_README = pathlib.Path.home() / "dev/solution-tournament/README.md"


def run_lint(root: pathlib.Path, readme: pathlib.Path) -> list:
    return lint_skill.lint(root, readme)


class FixtureCase(unittest.TestCase):
    """Copies the live skill into a temp dir so defects can be injected."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / "skill"
        shutil.copytree(SKILL_ROOT, self.root, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        self.readme = pathlib.Path(self.tmp.name) / "README.md"
        shutil.copy(REPO_README, self.readme)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def mutate(self, rel_path: str, old: str, new: str) -> None:
        p = self.root / rel_path if rel_path != "README.md" else self.readme
        text = p.read_text()
        assert old in text, f"fixture mutation target not found: {old[:60]}"
        p.write_text(text.replace(old, new))


class TestCurrentSkillClean(unittest.TestCase):
    def test_live_skill_passes(self) -> None:
        findings = run_lint(SKILL_ROOT, REPO_README)
        self.assertEqual(findings, [], f"live skill should lint clean, got: {findings}")


class TestRegressions(FixtureCase):
    def test_detects_mode_file_timing_regression(self) -> None:
        # Real defect, fixed 2026-08-13: header said "before Phase 1".
        self.mutate(
            "references/full-mode.md",
            "before Phase 0 (SKILL.md's Calibration owns this timing rule; this line matches it)",
            "before Phase 1",
        )
        findings = run_lint(self.root, self.readme)
        self.assertTrue(any("timing" in f.lower() for f in findings), findings)

    def test_detects_stale_line_count_claim(self) -> None:
        # Real defect, fixed 2026-08-13: README said ~100-line for a 120-line script.
        self.mutate("README.md", "~120-line", "~50-line")
        findings = run_lint(self.root, self.readme)
        self.assertTrue(any("line" in f.lower() and "readme" in f.lower() for f in findings), findings)

    def test_detects_missing_lightweight_box(self) -> None:
        self.mutate(
            "references/lightweight-mode.md",
            "11a. severity-gate determination",
            "REMOVED-BOX severity-gate determination",
        )
        findings = run_lint(self.root, self.readme)
        self.assertTrue(any("15" in f for f in findings), findings)

    def test_detects_broken_call_sum(self) -> None:
        self.mutate("references/full-mode.md", "1+1+2+1+6+2+2+2+1 = 18", "1+1+2+1+6+2+2+2+2 = 18")
        findings = run_lint(self.root, self.readme)
        self.assertTrue(any("18" in f for f in findings), findings)

    def test_detects_missing_referenced_file(self) -> None:
        (self.root / "templates/red-team.md").unlink()
        findings = run_lint(self.root, self.readme)
        self.assertTrue(any("red-team" in f for f in findings), findings)

    def test_detects_size_claim_drift(self) -> None:
        import re
        p = self.root / "SKILL.md"
        text = p.read_text()
        mutated = re.sub(
            r"this file \(~[\d.]+k words / [\d.]+k chars\)",
            "this file (~4.0k words / 20k chars)",
            text,
            count=1,
        )
        self.assertNotEqual(text, mutated, "size-claim pattern not found to mutate")
        p.write_text(mutated)
        findings = run_lint(self.root, self.readme)
        self.assertTrue(any("size claim" in f.lower() for f in findings), findings)


if __name__ == "__main__":
    unittest.main()
