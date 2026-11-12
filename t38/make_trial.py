"""Create an exclusively synthetic T-38 vault in a NEW folder (stdlib, MIT)."""
import json
from pathlib import Path
import sys

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))
from wikikit.textio import write_text


def make(target):
    target = Path(target)
    target.mkdir(parents=True, exist_ok=False)
    cfg = json.loads((KIT / 't38/provisional.config.json').read_text(encoding='utf-8'))
    write_text(target / 'wiki.config.json', json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    for folder in cfg['folders'] + ['3. Assets/PDFs', '5. Templates']:
        (target / folder).mkdir(parents=True, exist_ok=True)
    def note(path, fm, body):
        write_text(target / path, '---\n' + fm + '\n---\n\n' + body + '\n')
    note('2. Papers/Fixture2026a.md', 'type: paper\nstatus: invented-invalid\nevidence_level: invented-invalid\nconcepts_touched: []',
         '# Synthetic source, not a real study\n[[Missing_Controlled_Target]]\n[[1. Mis_articulos/Fixture_Project]]\n[[4. Temas/Conceptos/Fuerza máxima]]\n')
    for name, aliases in [('Fuerza máxima', '[fuerza máxima, maximal strength]'),
                          ('Maximal_Strength', '[Fuerza maxima, maximal strength]'),
                          ('Potencia', '[potencia, power]')]:
        note('4. Temas/Conceptos/' + name + '.md',
             'type: concept\nstatus: draft\ndate: 2026-11-12\nfield: synthetic\naliases: ' + aliases,
             '# Synthetic concept\n## Results\n[pendiente claim]\n' +
             ('mejora un resultado ficticio.\n' * 3 if name == 'Fuerza máxima' else 'Descripción ficticia, sin resultado científico.') +
             '\n| A | B |\n|---|---|\n| uno | dos | tres |\n')
    note('4. Temas/Metodos/Dinamometría.md', 'type: method\nstatus: draft\nfield: synthetic\naliases: [dinamometría, dynamometry]',
         '# Synthetic method\n[[Fixture2026a]]')
    note('1. Mis_articulos/Fixture_Project.md', 'type: project\nstatus: draft', '# Synthetic project')
    write_text(target / 'index.md', '# Synthetic index\n\n## Papers\n[[Fixture2026a]]\n')
    write_text(target / '_VOCABULARY.md', '| Canonical | Aliases | Note |\n|---|---|---|\n| Fuerza máxima | fuerza máxima | [[Fuerza máxima]] |\n| Ghost_Controlled | ghost | [[Ghost_Controlled]] |\n')
    return target


if __name__ == '__main__':
    make(sys.argv[1])
