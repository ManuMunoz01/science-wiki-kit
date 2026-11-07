"""tools/pmc_tables.py: the body keeps the XML's section titles (offline, on a small JATS sample)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import pmc_tables  # noqa: E402

SAMPLE = b"""<?xml version="1.0"?>
<article><front><article-meta><abstract><p>Abstract text.</p></abstract></article-meta></front>
<body>
  <p>Untitled lead paragraph.</p>
  <sec id="s1"><title>Introduction</title><p>Intro paragraph.</p></sec>
  <sec id="s2"><title>Methods</title>
    <sec id="s2a"><title>Participants</title><p>Thirty men took part.</p></sec>
    <sec id="s2b"><title>Statistical analysis</title><p>Wilcoxon test.</p></sec>
  </sec>
  <sec id="s3"><title>Results</title>
    <p>See Table 1.</p>
    <table-wrap id="t1"><label>Table 1</label><caption><p>Outcomes.</p></caption>
      <table><tr><th>Var</th><th>Mean</th></tr><tr><td>PT</td><td>1.5</td></tr></table>
      <table-wrap-foot><p>Note: PT is peak torque.</p></table-wrap-foot></table-wrap>
  </sec>
  <sec id="s4"><p>Section without a title.</p></sec>
</body></article>"""


class BodyHeadings(unittest.TestCase):
    def setUp(self):
        self.doc = pmc_tables.parse_jats(SAMPLE)

    def test_headings_and_levels_in_document_order(self):
        heads = [(b["level"], b["title"]) for b in self.doc["blocks"] if b["type"] == "heading"]
        self.assertEqual(heads, [(1, "Introduction"), (1, "Methods"), (2, "Participants"),
                                 (2, "Statistical analysis"), (1, "Results")])

    def test_paragraph_follows_its_heading(self):
        seq = [b.get("title") or b["text"] for b in self.doc["blocks"]]
        self.assertLess(seq.index("Participants"), seq.index("Thirty men took part."))
        self.assertLess(seq.index("Thirty men took part."), seq.index("Statistical analysis"))

    def test_paragraph_list_is_what_iter_p_gave(self):
        # abstract excluded (it is in <front>), table caption and foot paragraphs kept, as before
        self.assertEqual(self.doc["paragraphs"], [
            "Untitled lead paragraph.", "Intro paragraph.", "Thirty men took part.", "Wilcoxon test.",
            "See Table 1.", "Outcomes.", "Note: PT is peak torque.", "Section without a title."])

    def test_markdown_body_carries_the_headings(self):
        md = pmc_tables.to_markdown(self.doc, {"title": "T"}, body=True)
        self.assertIn("### Introduction", md)
        self.assertIn("#### Participants", md)
        self.assertLess(md.index("### Methods"), md.index("#### Participants"))
        self.assertNotIn("### Section without", md)

    def test_without_body_flag_no_headings(self):
        md = pmc_tables.to_markdown(self.doc, {"title": "T"}, body=False)
        self.assertNotIn("Introduction", md)


class Metadata(unittest.TestCase):
    CORE = {"pmid": "1", "pmcid": "PMC1", "doi": "10.1/x", "title": "T", "pubYear": "2022",
            "authorString": "Doe J, Roe R.", "journalInfo": {"volume": "19", "issue": "15", "journal": {"title": "Journal of X"}}, "pageInfo": "9296"}

    def test_core_record_gives_bibliographic_fields(self):
        m = pmc_tables.meta_from_core(self.CORE)
        self.assertEqual((m["authors"], m["volume"], m["issue"], m["pages"], m["journalTitle"]),
                         ("Doe J, Roe R", "19", "15", "9296", "Journal of X"))

    def test_missing_fields_do_not_crash_and_are_not_printed(self):
        m = pmc_tables.meta_from_core({"pmcid": "PMC2", "title": "T"})
        md = pmc_tables.to_markdown({"tables": [], "paragraphs": [], "blocks": []}, m, body=False)
        self.assertNotIn("Bibliographic data", md)

    def test_header_prints_authors_and_biblio(self):
        md = pmc_tables.to_markdown({"tables": [], "paragraphs": [], "blocks": []},
                                    pmc_tables.meta_from_core(self.CORE), body=False)
        self.assertIn("Authors: Doe J, Roe R", md)
        self.assertIn("Bibliographic data (Europe PMC): volume 19, issue 15, pages 9296", md)


if __name__ == "__main__":
    unittest.main()
