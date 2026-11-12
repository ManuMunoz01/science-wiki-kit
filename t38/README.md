# T-38 · Isolated Oficina Manu trial

Provisional development on the user's fork only. Base:
`bb639423771a60b430819f11f62c56e29c225324`; branch `t-38`.
Original code, tests, defaults, templates and skills remain unchanged. Code added
here is MIT; documentation and synthetic examples CC BY 4.0, preserving the kit's
attribution to MinorBaek and the root licences.

This is software validation with invented notes, not scientific validation or a
migration of the real library. None of the provisional metadata is prescribed for
Oficina Manu. Actual YAML, Zotero template expressions, citekeys and taxonomy must
be retained when the full guide/template become accessible.

From the kit checkout, Python >=3.9 (tested: 3.12.14), standard library only:

```bash
python t38/validate.py /tmp/t38-evidence-NEW
python t38/diagnostics.py lint --vault-root t38/trial-vault --out-dir /tmp/t38-lint-NEW
python t38/diagnostics.py vocabulary --vault-root t38/trial-vault --out-dir /tmp/t38-vocabulary-NEW
python -I -m unittest discover -s tests
```

Replace NEW with a unique identifier. Commands refuse an existing output directory;
no deletion, repair, merge, overwrite or commit step is part of the workflow.
`validate.py` generates a separate fresh vault, checks the original five test
modules and self-test separately, runs both original CLIs with external output
paths, tests the adapter and checks byte hashes/repeatability. It leaves detailed
logs and reports in the selected output directory. These are runtime caches,
not authoritative current measurements to version. A dated report is in
`report.md`. Recreate the checked-in synthetic fixture, ONLY at a new path, with:
`python t38/make_trial.py /tmp/t38-vault-NEW`.

The on-disk trial has six invented notes, controlled broken link,
invalid status/evidence level, absent metadata, unsourced Spanish claims,
English headings, claim placeholders, malformed tables, bilingual overlapping
aliases and a stale vocabulary. `3. Assets/PDFs` and `5. Templates` are empty test
directories (created by the generator, not restored by Git alone). No PDF,
Zotero expression, real template or real scientific result is fabricated.
The trial generator is the authoritative way to restore empty directories.

## Local Codex skills

`.agents/skills/oficina-wiki-lint/SKILL.md` and
`.agents/skills/oficina-vocabulary-update/SKILL.md` are local instruction adapters.
They point to the retained original scripts/references and use safe external
proposals. They are not ChatGPT Skills and are not globally installed.

Current-agent explicit file-based invocation: ask Codex to follow the corresponding
SKILL.md; read it and execute its procedure. This has been exercised in this task.
Native discovery is a separate capability: `python t38/probe_codex_skills.py`
uses local Codex `skills/list` without an inference/model turn. In this Cloud
sandbox it failed during app-server startup due to read-only Codex state storage.
Therefore automatic discovery and native `$skill-name` invocation are UNVERIFIED.
Do not equate the successful Python commands with native skill activation.

## Limits

Read `compatibility-33.md` before interpreting zero counters. Rules 21 and 29
are explicitly inactive, 7 is manual and 14 enabled. Several other rules have
no applicable books, seals, synthesis or index tables in this small trial.
No actual guide/template was read; Drive CONNECT returned 403 and no Drive
connector is available. Request attachments, do not guess field mappings.

The adapter leaves upstream Check 30 counters visible and adds Unicode entry
coverage separately. The vocabulary proposal preserves accents and canonical
names, supports configured recursion, and lists even single-alias collisions
across fields for human review. It does not translate or infer synonyms. It
is not an audit of Zotero identity, PDF existence, DOI validity or source fidelity.
