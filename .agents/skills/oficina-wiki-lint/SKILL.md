---
name: oficina-wiki-lint
description: Audit the T-38 synthetic Oficina Manu trial with read-only wiki-lint diagnostics. Use for T-38 wiki health checks; never repair or operate on the real library.
---

# T-38 wiki diagnostic

Provisional local Codex skill; not an installed ChatGPT skill. Documentation CC BY 4.0,
derived from science-wiki-kit (MinorBaek); retain the repository licences.

1. Find the kit checkout containing `t38/diagnostics.py`. Read `t38/README.md`,
   `docs/GOTCHAS.md`, `skills/wiki-lint/references/cli-reference.md` and
   `skills/wiki-lint/references/check-origins.md`. These remain the rule references.
2. Confirm the requested target is the synthetic trial and has `wiki.config.json`.
   Never infer actual library fields from the provisional configuration.
3. From the kit root run:
   `python t38/diagnostics.py lint --vault-root t38/trial-vault --out-dir /tmp/t38-lint-NEW`
   Replace NEW with a unique run identifier; output must not exist or be inside the vault.
4. Read `scope.json` and relevant per-check lists. Report loaded notes, checks called,
   conditional/inactive checks, upstream counters and the separate Unicode vocabulary audit.
   Zero findings and exit code 0 do not certify coverage or scientific validity.
5. Show findings and limitations; never call fix.py, promote notes, edit the vault,
   commit, push, synchronize or open a PR. Request current guides before any real-library adaptation.
