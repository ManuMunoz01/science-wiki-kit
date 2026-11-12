"""Build a NEW synthetic BIB-1 vault; no internal documents copied (MIT)."""
import json
from pathlib import Path
import sys

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from wikikit.textio import write_text


def pdf_fixture():
    """A blank, valid synthetic PDF; presence must never be reported as identity/reading."""
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>']
    data = b'%PDF-1.4\n% Synthetic fixture only\n'
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += str(i).encode() + b' 0 obj\n' + obj + b'\nendobj\n'
    start = len(data)
    data += b'xref\n0 4\n0000000000 65535 f \n'
    data += b''.join(('%010d 00000 n \n' % offset).encode() for offset in offsets[1:])
    return data + b'trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n' + str(start).encode() + b'\n%%EOF\n'


def make(target):
    target = Path(target)
    target.mkdir(parents=True, exist_ok=False)
    write_text(target / '.t38-synthetic', 'Invented test data only. No real library documents.\n')
    write_text(target / 'wiki.config.json', read_profile())
    for folder in ('1. Mis_articulos', '2. Papers', '3. Assets/PDFs', '4. Temas', '5. Templates'):
        (target / folder).mkdir(parents=True, exist_ok=True)
    def note(path, metadata, body):
        fm = '\n'.join(key + ': ' + json.dumps(value, ensure_ascii=False) for key, value in metadata.items())
        write_text(target / path, '---\n' + fm + '\n---\n\n' + body + '\n')
    base = dict(title='Invented software fixture', authors='Example, X.', year='2026', journal='Synthetic Journal',
                doi='', citekey='Fixture2026a', topic='hombro', subtopic=['anatomia', 'deportistas'],
                study_type='validation-study', tags=['ensayo-sintetico'], full_text_status='full-text', review_status='reviewed')
    note('2. Papers/Fixture2026a.md', base,
         '# Synthetic fixture A\n\n## Resumen\nAn invented English abstract, not scientific evidence.\n\n'
         '## Artículos relacionados\n[[Fixture2026b|otra ficha]]\n[Zotero](zotero://select/library/items/TEST0001)\n'
         '## PDF\nSin PDF asociado: ensayo de acceso HTML declarado, no verificado.\n'
         '## Fuentes y alcance de la revisión\nEscenario inventado de HTML completo; no se ha leído ninguna publicación real.\n'
         '## Palabras clave originales\nPendientes, no inferidas de etiquetas.')
    other = dict(base, citekey='Fixture2026b', full_text_status='abstract-only', review_status='partial',
                 topic='imus', subtopic=['sensores-materiales', 'validez-fiabilidad'])
    note('2. Papers/Fixture2026b.md', other,
         '# Synthetic fixture B\n\n## PDF\n[[3. Assets/PDFs/archivo de ensayo.pdf]]\n'
         '## Fuentes y alcance de la revisión\nEscenario sintético: lectura parcial declarada. El archivo no acredita lectura.\n'
         '## Palabras clave originales\nNo verificadas.')
    bad = dict(base, citekey='Fixture2026bad', full_text_status='downloaded', review_status='final',
               topic='hombro', subtopic=['review'], study_type='textbook')
    note('2. Papers/Fixture2026bad.md', bad,
         '# Controlled errors, not a real study\n[[Missing_Controlled]]\n'
         '## PDF\n[[3. Assets/PDFs/ausente.pdf]]\n'
         '## Resultados principales\n| A | B |\n|---|---|\n| a | b | c |\n'
         '## Palabras clave originales\nNo verificadas.\n## Fuentes y alcance de la revisión\nEnsayo inventado.')
    pending = dict(base, citekey='Fixture2026pending', topic='', subtopic=[], study_type='', full_text_status='', review_status='')
    note('2. Papers/Fixture2026pending.md', pending, '# Imported synthetic fixture, awaiting review')
    # Small original test snippet, NOT a copy of the confidential scientific template.
    write_text(target / '5. Templates/Example.synthetic.md',
               '---\ntitle: "{{title}}"\ncitekey: "{{citekey}}"\njournal: "{{publicationTitle}}"\n---\n'
               '{% for annotation in annotations %}\n{{annotation.comment}}\n{% endfor %}\n')
    write_text(target / '2. Papers/Fixture2026template.md',
               '---\ntitle: "{{title}}"\ncitekey: "{{citekey}}"\n---\n{{bibliography}}\n'
               '[[{{citekey}}]]\n')
    note('4. Temas/Término sintético.md', {'aliases':['synthetic load', 'carga de ensayo']},
         '# Invented thematic note\n[[2. Papers/Fixture2026a]]\n[[Fixture2026b]]')
    note('1. Mis_articulos/Example_Project.md', {}, '# Invented project, outside the scientific audit scope')
    (target / '3. Assets/PDFs/archivo de ensayo.pdf').write_bytes(pdf_fixture())
    records = [
        dict(id='example-a', canonical='Carga de ensayo', aliases=['synthetic load'], source_note='2. Papers/Fixture2026a.md',
             citekey='Fixture2026a', year='2026', location='synthetic section A',
             definition='Invented definition A for software testing only.', definition_kind='synthetic-paraphrase', context='invented scenario A'),
        dict(id='example-b', canonical='Carga de ensayo', aliases=['Synthetic Load'], source_note='2. Papers/Fixture2026b.md',
             citekey='Fixture2026b', year='2026', location='synthetic section B',
             definition='Invented DIFFERENT definition B, not merged with A.', definition_kind='synthetic-paraphrase', context='invented scenario B'),
        dict(id='example-c', canonical='Variable de ensayo', aliases=['trial variable'], source_note='2. Papers/Fixture2026a.md',
             citekey='Fixture2026a', year='2026', location='synthetic section C',
             definition='Used without an explicit definition in this invented scenario.', definition_kind='synthetic-no-explicit-definition', context='invented scenario C')]
    write_text(target / 'glossary.synthetic.json', json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    return target


def read_profile():
    return (Path(__file__).with_name('profile.json')).read_text(encoding='utf-8')


if __name__ == '__main__':
    make(sys.argv[1])
