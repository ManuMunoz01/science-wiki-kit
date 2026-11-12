---
name: wiki-lint
description: "Run the Oficina synthetic wiki diagnostic through the existing BIB-1 adapter; read-only, never repair."
---

# Synthetic wiki diagnostic

Read [shared policy](../../../t38/bib9/POLICY.md) first.
Original full package: [wiki-lint](../../../skills/wiki-lint/SKILL.md), including
its scripts/references and shared kit modules. Preserve it; do not run fix.py.
Read [BIB-1 scope/matrix](../../../t38/bib1/README.md).

From the checkout root:
1. Choose a NEW external synthetic vault path and output directory.
2. Run `python t38/bib1/make_trial.py <NEW_SYNTHETIC_VAULT>`.
3. Run `python t38/bib1/audit.py lint --vault-root <NEW_SYNTHETIC_VAULT> --out-dir <NEW_EXTERNAL_OUTPUT>`.
4. Read lint.proposed.json. Report scope, original checks 26/27, pending/deferred
   findings and documentary errors separately. Do not repair or claim source truth.

Use only generated synthetic data; a real-library request is outside this entrypoint.
