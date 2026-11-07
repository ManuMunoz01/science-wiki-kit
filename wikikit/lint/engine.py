"""Run the checks, write their output files, and the --self-test against the fixtures."""
import re
from pathlib import Path

from ..config import load_config
from ..textio import write_text
from . import checks_basic, checks_content, checks_integrity, checks_structure
from .context import Context

ALL_CHECKS = (list(checks_basic.CHECKS) + list(checks_structure.CHECKS)
              + list(checks_content.CHECKS) + list(checks_integrity.CHECKS))
_EXPECTED = re.compile(r"^([a-z0-9_]+)\s*=\s*(-?\d+)", re.M)


def origin_anchor(num):
    """Where `references/check-origins.md` explains why check `num` exists."""
    if num == 7:
        return "check-origins.md#check-7--check-7b"
    if 17 <= num <= 21:
        return "check-origins.md#check-17--check-18--check-19--check-20--check-21"
    return "check-origins.md#check-%d" % num


def run(ctx, only=None, out_dir="_temp", quiet=False):
    """Run the selected checks (a set of numbers, or None for all). Returns {counter: value}."""
    counters, fired = {}, []
    out_dir = Path(out_dir)
    for num, fn in ALL_CHECKS:
        if only and num not in only:
            continue
        res = fn(ctx)
        counters.update(res.counters)
        if res.fired and num not in fired:
            fired.append(num)
        for fname, lines in res.files.items():
            write_text(out_dir / fname, "\n".join(lines) + ("\n" if lines else ""))
        if not quiet:
            vals = ", ".join("%s=%d" % (k.replace("check", "", 1), v) for k, v in res.counters.items())
            print("Check %d (%s): %s" % (num, res.label, vals))
    # The motive must arrive when you decide whether a hit is real or noise, not months later.
    if fired and not quiet and not ctx.self_test:
        print("\nWhy these checks exist (read before dismissing a finding as a false positive):")
        for num in fired:
            print("  Check %d -> references/%s" % (num, origin_anchor(num)))
    return counters


def load_expected(path):
    text = Path(path).read_bytes().decode("utf-8")
    return {k: int(v) for k, v in _EXPECTED.findall(text)}


def self_test(fixture_vault, expected_file, out_dir, only=None, quiet=False):
    """Run against the fixtures and compare each counter with expected_counters.txt.

    Counters whose check is not selected are reported as `pending`, not as failures.
    Returns (failures, pending)."""
    root, cfg = load_config(fixture_vault)
    ctx = Context(root, cfg, self_test=True)
    actual = run(ctx, only=only, out_dir=out_dir, quiet=quiet)
    expected = load_expected(expected_file)
    failures, pending = [], []
    for key, want in expected.items():
        if key not in actual:
            pending.append(key)
        elif actual[key] != want:
            failures.append("%s expected=%d actual=%d" % (key, want, actual[key]))
    return failures, pending
