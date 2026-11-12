"""Invoke existing Oficina adapters on invented inputs, no original write workflows (MIT)."""
import json
from pathlib import Path
import subprocess
import sys

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from t38.bib1.make_trial import make
from t38.bib1.validate import snapshot


def run(destination):
    out = Path(destination).resolve()
    if out == KIT or KIT in out.parents:
        raise ValueError('Synthetic smoke output must be outside the checkout')
    out.mkdir(parents=True,mode=0o700,exist_ok=False)
    vault = make(out/'synthetic-vault')
    glossary = KIT/'t38/bib7/fixtures'
    before = snapshot(vault),snapshot(glossary)
    commands = {
        'wiki-lint':['t38/bib1/audit.py','lint','--vault-root',str(vault),'--out-dir',str(out/'lint')],
        'vocabulary-update':['t38/bib7/adapter.py','--synthetic-root',str(glossary),
           '--a',str(glossary/'shoulder.compatibility.synthetic.md'),
           '--b',str(glossary/'force.compatibility.synthetic.md'),'--out-dir',str(out/'vocabulary')]
    }
    results = {}
    for name,args in commands.items():
        proc = subprocess.run([sys.executable,*args],cwd=KIT,capture_output=True,text=True)
        (out/(name+'.log')).write_text(proc.stdout+proc.stderr,encoding='utf-8')
        results[name] = {'exit_code':proc.returncode, 'invocation':'procedure/CLI, not native model activation'}
        if proc.returncode:
            raise RuntimeError('Existing adapter failed: '+name)
    lint = json.loads((out/'lint/lint.proposed.json').read_text())
    vocab = json.loads((out/'vocabulary/suggestions.proposed.json').read_text())
    if lint['notes_loaded'] != 6 or vocab['summary']['observations'] != 6:
        raise RuntimeError('Unexpected/empty synthetic scope')
    if before != (snapshot(vault),snapshot(glossary)):
        raise RuntimeError('Synthetic inputs changed')
    results['invariants'] = {'wiki_notes_loaded':6,'glossary_observations':6,'inputs_unchanged':True,
                            'planning_only_scripts_executed':False,'real_data_accessed':False}
    (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results


if __name__ == '__main__':
    run(sys.argv[1])
