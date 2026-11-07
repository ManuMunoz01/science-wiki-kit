"""The worked example under examples/ must stay lint-clean: it is what a new user is shown first."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from wikikit.config import load_config  # noqa: E402
from wikikit.lint import engine  # noqa: E402
from wikikit.lint.context import Context  # noqa: E402

EXAMPLE = ROOT / "examples" / "worked-example"


class WorkedExample(unittest.TestCase):
    def test_lints_clean_and_is_not_empty(self):
        root, cfg = load_config(EXAMPLE)
        ctx = Context(root, cfg)
        self.assertEqual(len(ctx.notes), 4)  # 1 paper, 2 concepts, 1 method
        with tempfile.TemporaryDirectory() as out:
            counters = engine.run(ctx, out_dir=out, quiet=True)
        findings = {k: v for k, v in counters.items() if v}
        self.assertEqual(findings, {})

    def test_config_carries_no_local_path(self):
        text = (EXAMPLE / "wiki.config.json").read_text(encoding="utf-8")
        self.assertNotIn("kit_dir", text)
        self.assertNotIn("Users", text)


if __name__ == "__main__":
    unittest.main()
