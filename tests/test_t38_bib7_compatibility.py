"""Compatibility regressions on invented stated A/B formats only (MIT)."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from t38.bib7.adapter import build, export
from t38.bib1.validate import snapshot


class Compatibility(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base/'inputs'
        shutil.copytree(ROOT/'t38/bib7/fixtures', self.root)
        self.a = self.root/'shoulder.compatibility.synthetic.md'
        self.b = self.root/'force.compatibility.synthetic.md'
        self.inputs = [('a',self.a),('b',self.b)]

    def row(self, result, identifier):
        return next(r for r in result['observations'] if r['target']['entry_id']==identifier)

    def test_long_bold_fields_frontmatter_and_source_urls_are_not_lost(self):
        result = build(self.root,self.inputs)
        row = self.row(result,'H-101')
        self.assertEqual(row['definitions_or_uses'],['Definición inventada Alfa. La etiqueta no acredita verificación.'])
        self.assertEqual(row['contexts'],['Escenario ficticio Alfa, sin datos de investigación.'])
        self.assertIn('Paráfrasis de ensayo',row['source_text'][1])
        self.assertEqual(row['source_references'],['ExampleAlpha2026'])
        self.assertEqual(row['source_urls'],['https://drive.example.invalid/file/d/EXAMPLE-NOT-REAL/view'])
        self.assertEqual(row['verification'],'declared-unverified')
        doc = next(d for d in result['documents'] if d['document_reference']==self.a.name)
        self.assertEqual(set(doc['frontmatter']),{'type','topic','task','updated','status'})
        self.assertIsNone(row['target']['glossary_id'])
        self.assertEqual(row['declared_years'],['2026'])

    def test_editorial_h3_is_not_a_scientific_entry_or_part_of_previous_definition(self):
        result = build(self.root,self.inputs)
        self.assertEqual([r['target']['entry_id'] for r in result['observations'] if r['target']['entry_id']],
                         ['H-101','H-102','H-103','H-104','H-105'])
        self.assertNotIn('Control editorial',self.row(result,'H-101')['raw_markdown'])
        self.assertEqual(result['summary']['parse_diagnostics'],0)

    def test_narrative_locations_and_nonextraction_are_not_declared_absence(self):
        result = build(self.root,self.inputs)
        labelled = self.row(result,'H-101')
        self.assertIn('párrafo Alfa',labelled['locations'][0])
        self.assertEqual(labelled['extraction_status']['location'],'structured-declared-unverified')
        narrative = self.row(result,'H-102')
        self.assertIn('Narrativa no estructurada',narrative['raw_markdown'])
        self.assertEqual(narrative['locations'],[])
        self.assertEqual(narrative['extraction_status']['location'],'not-structured')
        absence = self.row(result,'H-103')
        self.assertEqual(absence['locations'],['no informado'])
        self.assertEqual(absence['extraction_status']['location'],'declared-not-reported-unverified')
        self.assertEqual(absence['extraction_status']['definition-or-use'],'declared-not-reported-unverified')
        self.assertIn('location',absence['pending'])

    def test_multisource_cell_is_preserved_with_binding_pending_not_absence(self):
        result = build(self.root,self.inputs)
        row = next(r for r in result['observations'] if r['target']['entry_id'] is None)
        self.assertEqual(row['source_references'],['ExampleReportOne2025','ExampleReportTwo2026'])
        self.assertEqual(len(row['definitions_or_uses']),1)
        self.assertIn('párrafo inventado Dos',row['definitions_or_uses'][0])
        self.assertIsNone(row['target']['entry_id'])
        self.assertEqual(row['source_binding'],'row-level-unresolved')
        self.assertIn('row-definition-source-binding',row['pending'])
        self.assertEqual(row['extraction_status']['location'],'combined-cell-unparsed')

    def test_bold_alias_and_distinct_publications_remain_unverified_and_inputs_intact(self):
        before = snapshot(self.root)
        one = export(self.root,self.inputs,self.base/'one')
        export(self.root,list(reversed(self.inputs)),self.base/'two')
        self.assertEqual((self.base/'one/suggestions.proposed.json').read_bytes(),(self.base/'two/suggestions.proposed.json').read_bytes())
        self.assertEqual(before,snapshot(self.root))
        aliases = [s for s in one['suggestions'] if s['kind']=='bibliographic_alias_statement']
        datasets = [s for s in one['suggestions'] if s['kind']=='dataset_relationship_review']
        self.assertEqual(len(aliases),1)
        self.assertEqual(len(datasets),1)
        self.assertEqual(datasets[0]['related_source_references'],['ExampleReportOne2025','ExampleReportTwo2026'])
        self.assertEqual(datasets[0]['verification'],'not-verified')
        self.assertFalse(any(s['kind']=='bibliographic_identity_candidate' for s in one['suggestions']))
        self.assertTrue(all(s['action']=='none' for s in one['suggestions']))
        for s in one['suggestions']:
            if s['kind']=='glossary_inconsistency':
                self.assertIn('pending_status',s)


if __name__ == '__main__':
    unittest.main()
