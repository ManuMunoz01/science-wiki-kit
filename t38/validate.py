"""Reproduce T-38 software evidence in a NEW directory; no library access (MIT)."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 't38'))
from make_trial import make


def hashes(vault):
    return {str(p.relative_to(vault)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in vault.rglob('*') if p.is_file()}


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=False)
    results = {}
    def run(name, *args):
        p = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
        (out / (name + '.log')).write_text(p.stdout + p.stderr, encoding='utf-8')
        results[name] = {'exit_code':p.returncode}
        if p.returncode:
            raise RuntimeError(name + ' failed: see ' + str(out))
    # Run the five original modules separately from adaptation tests.
    for module in ['wikikit', 'pmc_tables', 'example', 'fixes', 'lint']:
        run('original_' + module, '-I', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_' + module + '.py')
    run('selftest', '-I', 'skills/wiki-lint/scripts/lint.py', '--self-test', '--out-dir', str(out / 'selftest'))
    run('adaptation', '-I', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_t38.py')
    vault = make(out / 'trial-vault')
    before = hashes(vault)
    run('original_lint_cli', '-I', 'skills/wiki-lint/scripts/lint.py', '--vault-root', str(vault), '--out-dir', str(out / 'original-lint'))
    run('original_vocabulary', '-I', 'skills/vocabulary-update/scripts/build_vocabulary.py', '--vault-root', str(vault),
        '--out', str(out / 'original-vocabulary.md'), '--dupes', str(out / 'original-dupes.txt'))
    run('adapter_lint', 't38/diagnostics.py', 'lint', '--vault-root', str(vault), '--out-dir', str(out / 'lint'))
    for suffix in ['a', 'b']:
        run('vocabulary_' + suffix, 't38/diagnostics.py', 'vocabulary', '--vault-root', str(vault), '--out-dir', str(out / ('vocabulary-' + suffix)))
    for name in ['_VOCABULARY.proposed.md', 'duplicates.proposed.json']:
        if (out / 'vocabulary-a' / name).read_bytes() != (out / 'vocabulary-b' / name).read_bytes():
            raise RuntimeError('Nonrepeatable proposal: ' + name)
    if before != hashes(vault):
        raise RuntimeError('Vault changed')
    results['invariants'] = {'vault_hashes_unchanged':True,'same_day_repeatability':True,'notes':6}
    (out / 'summary.json').write_text(json.dumps(results,indent=2) + '\n',encoding='utf-8')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
