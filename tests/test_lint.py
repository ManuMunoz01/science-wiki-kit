"""wiki-lint regression: the fixtures' expected counters, for every check that is ported."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from wikikit.lint import engine  # noqa: E402

FX = ROOT / "tests" / "fixtures" / "lint"


class FixtureCounters(unittest.TestCase):
    def test_counters_match_expected(self):
        with tempfile.TemporaryDirectory() as out:
            failures, pending = engine.self_test(FX / "TheVault", FX / "expected_counters.txt", out, quiet=True)
        self.assertEqual(failures, [])
        ported = len(engine.load_expected(FX / "expected_counters.txt")) - len(pending)
        self.assertGreater(ported, 0)


if __name__ == "__main__":
    unittest.main()
