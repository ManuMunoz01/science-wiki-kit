#!/usr/bin/env python3
"""wiki-lint: health checks for a scientific markdown wiki. Standard library only.

  python lint.py                       # run every check; per-check lists go to _temp/
  python lint.py --only 1,5            # only these checks
  python lint.py --out-dir lint_out    # where the per-check .txt lists are written
  python lint.py --self-test           # run against the kit's fixtures and compare the counters

Run from the vault (or pass --vault-root): the config is the nearest wiki.config.json upwards.
The tool is read-only against the wiki; it only writes the per-check lists into --out-dir.
Exit code: 0 clean run (or self-test passed), 1 self-test failure, 2 usage error.
"""
import argparse
import sys
from pathlib import Path

try:
    import wikikit  # noqa: F401
except ImportError:  # running from a checkout without `pip install -e .`
    for _p in Path(__file__).resolve().parents:
        if (_p / "wikikit" / "__init__.py").is_file():
            sys.path.insert(0, str(_p))
            break
    else:
        sys.exit("wikikit not found: run `pip install -e <kit>` or keep the skills inside the kit checkout")

from wikikit.config import load_config  # noqa: E402
from wikikit.lint import engine  # noqa: E402
from wikikit.lint.context import Context  # noqa: E402


def kit_fixtures():
    for p in Path(__file__).resolve().parents:
        f = p / "tests" / "fixtures" / "lint"
        if (f / "expected_counters.txt").is_file():
            return f
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault-root", default=".")
    ap.add_argument("--only", help="comma-separated check numbers, e.g. 1,5,12")
    ap.add_argument("--out-dir", default="_temp")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    only = {int(x) for x in a.only.split(",")} if a.only else None

    if a.self_test:
        fx = kit_fixtures()
        if fx is None:
            sys.exit("fixtures not found (they ship in tests/fixtures/lint of the kit checkout)")
        failures, pending = engine.self_test(fx / "TheVault", fx / "expected_counters.txt", a.out_dir, only=only)
        for f in failures:
            print("FAIL " + f)
        if pending:
            print("pending (not selected or not ported): %d" % len(pending))
        print("SELF-TEST: %s" % ("FAIL (%d)" % len(failures) if failures else "PASS"))
        return 1 if failures else 0

    root, cfg = load_config(a.vault_root)
    ctx = Context(root, cfg)
    print("Loaded wiki notes: %d" % len(ctx.notes))
    engine.run(ctx, only=only, out_dir=a.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
