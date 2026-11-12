---
name: oficina-vocabulary-update
description: Generate new review-only vocabulary and duplicate proposals for the T-38 synthetic Oficina Manu trial. Preserve canonical names and original notes; never merge or overwrite.
---

# T-38 vocabulary proposal

## BIB-1 profile routing (after baseline 22f1b2d)

For the guide-grounded synthetic Biblioteca profile, read `t38/bib1/README.md`,
`compatibility-33.md` and `field-map.md` there. Use `t38/bib1/audit.py vocabulary`
with an explicit `--vault-root` carrying `.t38-synthetic` and a NEW external
`--out-dir`. Generate a new fixture with `t38/bib1/make_trial.py` if needed.
Do not run the historical recipe below on this profile or on real library files.
Do not add kit type/status/seal/evidence fields, rename journal, render templates,
infer scientific review or merge definitions. Report deferred checks and decisions.
For vocabulary, test-only per-source glossary records are proposals, not approved
library schema. Preserve canonicals, aliases, source citekeys and differing definitions.
No commit, push, PR or external-library action is part of either diagnostic procedure.
Native skill discovery remains separate and unverified in this intervention.

## Historical profile only

Provisional local Codex skill; not an installed ChatGPT skill. Documentation CC BY 4.0,
derived from science-wiki-kit (MinorBaek); retain the repository licences.

1. Find the kit checkout containing `t38/diagnostics.py`. Read `t38/README.md` and
   `skills/vocabulary-update/SKILL.md` for the original generator and its references.
   This adapter replaces its write-in-place and commit steps with proposals only.
2. Confirm the target is a synthetic trial with the provisional configuration.
3. From the kit root run:
   `python t38/diagnostics.py vocabulary --vault-root t38/trial-vault --out-dir /tmp/t38-vocabulary-NEW`
   Use a new unique output directory outside the vault.
4. Read `_VOCABULARY.proposed.md` and `duplicates.proposed.json`. Present canonical
   terms, preserved Spanish/English aliases and review candidates. A shared normalized
   term is a collision candidate, not proof of equivalence. No translation or semantic inference.
5. Repeat into a second fresh directory and compare contents for repeatability on the
   same date. Generated date changes across days are expected. Compare note hashes before/after.
6. Never overwrite an existing vocabulary, merge terms, modify aliases, commit, push,
   synchronize or open a PR. User review is required before any later adoption.
