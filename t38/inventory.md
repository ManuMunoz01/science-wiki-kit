# T-38 · File inventory and difference from baseline

All paths below are new, local and uncommitted relative to the exact base commit.
No previously tracked repository file was modified. No commit/PR was created.
The only Git configuration additions are local branch t-38 and the upstream reference remote.

| File | Purpose |
|---|---|
| `.agents/skills/oficina-vocabulary-update/SKILL.md` | Local Codex instruction adapter; native discovery unverified |
| `.agents/skills/oficina-wiki-lint/SKILL.md` | Local Codex instruction adapter; native discovery unverified |
| `t38/README.md` | Review documentation (CC BY 4.0) |
| `t38/compatibility-33.md` | Review documentation (CC BY 4.0) |
| `t38/diagnostics.py` | Reproducible adapter, fixture builder, probe or validation/test code (MIT) |
| `t38/inventory.md` | Review documentation (CC BY 4.0) |
| `t38/make_trial.py` | Reproducible adapter, fixture builder, probe or validation/test code (MIT) |
| `t38/probe_codex_skills.py` | Reproducible adapter, fixture builder, probe or validation/test code (MIT) |
| `t38/provisional.config.json` | Explicitly provisional configuration |
| `t38/report.md` | Review documentation (CC BY 4.0) |
| `t38/task-update.md` | Review documentation (CC BY 4.0) |
| `t38/trial-vault/1. Mis_articulos/Fixture_Project.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/2. Papers/Fixture2026a.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/4. Temas/Conceptos/Fuerza máxima.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/4. Temas/Conceptos/Maximal_Strength.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/4. Temas/Conceptos/Potencia.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/4. Temas/Metodos/Dinamometría.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/_VOCABULARY.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/index.md` | Synthetic fixture/config; invented data only |
| `t38/trial-vault/wiki.config.json` | Synthetic fixture/config; invented data only |
| `t38/validate.py` | Reproducible adapter, fixture builder, probe or validation/test code (MIT) |
| `tests/test_t38.py` | Reproducible adapter, fixture builder, probe or validation/test code (MIT) |

Runtime evidence: /tmp/t38-validation-reviewed (logs, original/adapted outputs,
hash/repeatability summary). These caches are deliberately not added to Git.
An external ZIP at /workspace/T-38-entregables.zip packages these new files and
the dated synthetic evidence for review; it contains no Git metadata or credentials.

Empty test directories (3. Assets/PDFs, 5. Templates, 4. Temas/Libros) are
restored by make_trial.py. Ignored Python bytecode is not part of the deliverable.

Original relation is checked against the requested base commit already present locally;
the current remote upstream tip has not been fetched or claimed identical.
