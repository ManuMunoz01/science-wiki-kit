"""Tests for the wiki-lint repair tools (index proposal, Check 12 backlinks, promotion)."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from wikikit.config import load_config  # noqa: E402
from wikikit.lint import checks_structure, fixes  # noqa: E402
from wikikit.lint.context import Context  # noqa: E402
from wikikit.textio import read_text, write_text  # noqa: E402

FX = ROOT / "tests" / "fixtures" / "lint" / "TheVault"


class FixtureCopy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name) / "TheVault"
        shutil.copytree(FX, self.vault)

    def tearDown(self):
        self.tmp.cleanup()

    def ctx(self, self_test=True):
        root, cfg = load_config(self.vault)
        return Context(root, cfg, self_test=self_test)


class Check12Fix(FixtureCopy):
    def test_dry_run_writes_nothing_then_apply_closes_the_asymmetries(self):
        before = {p: read_text(p) for p in self.vault.rglob("*.md")}
        r = fixes.fix_check12(self.ctx(), dry_run=True)
        self.assertEqual((r["touched"], r["added"]), (2, 3))
        self.assertEqual(before, {p: read_text(p) for p in self.vault.rglob("*.md")})

        fixes.fix_check12(self.ctx())
        res = checks_structure.check12(self.ctx())
        self.assertEqual(res.counters["check12"], 0)
        self.assertEqual(res.counters["check12_missing"], 1)  # missing targets are never touched

        again = fixes.fix_check12(self.ctx())  # idempotent
        self.assertEqual((again["touched"], again["added"]), (0, 0))

    def test_inserted_line_uses_the_configured_placeholder(self):
        fixes.fix_check12(self.ctx())
        text = read_text(self.vault / "09_Recursos" / "metodologia" / "Fixture_Draft_SingleSource.md")
        self.assertIn("- [[Smith_2024_FakePaper]] - [pendiente claim]", text)

    def test_line_endings_are_preserved(self):
        target = self.vault / "09_Recursos" / "metodologia" / "Fixture_Draft_SingleSource.md"
        write_text(target, read_text(target).replace("\r\n", "\n").replace("\n", "\r\n"))
        fixes.fix_check12(self.ctx())
        data = target.read_bytes()
        self.assertEqual(data.count(b"\n"), data.count(b"\r\n"))


class Promote(FixtureCopy):
    def test_flips_only_draft_status_and_keeps_crlf(self):
        wiki = self.vault / "09_Recursos"
        a = wiki / "metodologia" / "Fixture_Draft_MultiSource.md"
        write_text(a, read_text(a).replace("\r\n", "\n").replace("\n", "\r\n"))
        stub_before = read_text(wiki / "conceptos" / "Fixture_Stub.md")
        lst = Path(self.tmp.name) / "list.txt"
        # a path, a final note by name, a stub by name, and a name that does not exist
        write_text(lst, "# comment\n%s\nFixture_Concept_A\nFixture_Stub\nNope_Does_Not_Exist\n" % a)
        log = Path(self.tmp.name) / "log.md"
        r = fixes.promote(self.ctx(), lst, log_file=log)
        self.assertEqual((r["changed"], r["listed"]), (1, 4))
        data = a.read_bytes()
        self.assertIn(b"status: final", data)
        self.assertEqual(data.count(b"\n"), data.count(b"\r\n"))  # the `$`-in-CRLF bug cannot happen
        self.assertEqual(stub_before, read_text(wiki / "conceptos" / "Fixture_Stub.md"))  # reported, not touched
        txt = read_text(log)
        self.assertIn("draft -> final", txt)
        self.assertIn("NOT FOUND", txt)
        self.assertIn("already final (no-op)", txt)
        self.assertIn("manual review", txt)


class IndexProposal(FixtureCopy):
    def test_groups_missing_entries_by_title_case_field(self):
        ctx = self.ctx()  # self-test forces manual index mode, so Check 7 runs
        res = checks_structure.check7(ctx)
        text, (n_papers, n_books, n_concept_groups, n_method_groups) = fixes.index_proposal(
            ctx, res.files["wiki_check7_index_missing.txt"], today="2026-11-07")
        self.assertIn("# Wiki Index - Proposed Additions (2026-11-07)", text)
        self.assertEqual(sum(1 for ln in text.splitlines() if ln.startswith("- [[")),
                         res.counters["check7_missing"])
        self.assertGreaterEqual(n_concept_groups + n_method_groups + n_papers + n_books, 1)


class Check11NoCoverageSection(FixtureCopy):
    """A fresh wiki has no `## Coverage by Field` table: subfields must not read as MISSING-ROW."""

    def test_missing_row_needs_a_coverage_section(self):
        with_table = checks_structure.check11(self.ctx()).files["wiki_check11_coverage.txt"]
        self.assertTrue(any(r.startswith("MISSING-ROW") for r in with_table))  # positive control
        index = self.ctx().index_path
        lines = read_text(index).split("\n")
        keep, skipping = [], False
        for ln in lines:
            if ln.startswith("## "):
                skipping = ln.startswith("## Coverage by Field")
            if not skipping:
                keep.append(ln)
        write_text(index, "\n".join(keep))
        without = checks_structure.check11(self.ctx()).files["wiki_check11_coverage.txt"]
        self.assertEqual([r for r in without if r.startswith("MISSING-ROW")], [])


if __name__ == "__main__":
    unittest.main()
