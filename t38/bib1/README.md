# BIB-1 · Guide-grounded synthetic Biblioteca profile

This is an additive profile after commit `22f1b2d81795a9071ddd3c32c06e71b94217804b`.
It keeps the historical `t38/diagnostics.py`, tests, trial and reports unchanged.
Code is MIT; newly authored documentation/synthetic examples follow CC BY 4.0,
retaining science-wiki-kit attribution to MinorBaek. Internal source documents
remain private and retain their original rights; they are NOT included here.

Read `compatibility-33.md` and `field-map.md` before interpreting any finding.
Both attached Markdown sources were read in full. `sources.json` records versions
by fingerprint, without copying content. No update register was supplied.
Neither internal-document instructions to operate on a library nor historical
permission to push a commit authorize external actions in this intervention.

## Reproduce

From the fork checkout, Python 3.12.14 tested, standard library only:

```bash
python t38/bib1/validate.py /tmp/t38-bib1-evidence-NEW
python -I -m unittest discover -s tests
```

The validator retains the historical validation as a separate run, runs the nine
new tests, creates a new invented vault, audits it, generates two vocabulary
proposals and verifies byte hashes and repeatability. Use a NEW output directory.
The marker and synthetic-only profile prevent accidental use of this entrypoint
on unmarked real library files. There is no network, sync, repair or mutation mode.

For separate procedural use through the repository-local Skills:

```bash
python t38/bib1/make_trial.py /tmp/t38-bib1-vault-NEW
python t38/bib1/audit.py lint --vault-root /tmp/t38-bib1-vault-NEW --out-dir /tmp/t38-bib1-lint-NEW
python t38/bib1/audit.py vocabulary --vault-root /tmp/t38-bib1-vault-NEW --out-dir /tmp/t38-bib1-vocabulary-NEW
```

No existing path is overwritten. Output directories must be outside the vault.
The fixture contains invented notes and a generated blank PDF, not a publication,
plus a short invented template snippet; no original guide/template or real paper.

## Interpretation

- `documentary`: malformed link/table or invalid nonempty controlled value.
- `pending-scientific-review`: access/design/classification/scope not yet recorded;
  not a task to automatically reread, and not an adverse scientific judgment.
- `review`: source/identity or metadata needs inspection (e.g. Zotero URL, existing
  PDF, duplicate citekey that may be a legitimate alias, missing journal).
- `decision`: proposed subtopic with the approved literal pending suffix.
- `deferred`: unrendered template or unsupported/unparsed YAML. Never call such a
  note validated or treat deferred work as zero errors.

Exit 0 means diagnostic execution completed, not "all notes correct". No check
verifies source truth, APA accuracy, causal inference or evidence quality.

## Intentional differences

Configuration holds actual field names, status/design lists, controlled taxonomy,
folder roles and relevant headings. There is no journal→venue conversion and no
kit type/status/evidence/concepts/seal field injection. Only original structural
checks 26/27 are reused; hard-coded semantic kit checks are not made compatible by
inventing extra fields. A strict flat YAML subset defers unsupported constructs
instead of silently parsing them; it is NOT a full YAML validator.

Vocabulary uses a TEST-ONLY sidecar of explicit source-specific records. It does
not extract definitions automatically from prose or equate aliases with synonyms.
Definitions/context/year/location stay separate even for identical canonical
terms; per-topic grouping refers to source topic, not scientific equivalence.
Missing records return pending extraction rather than an invented vocabulary.
The format/location of a real shared glossary remains a Manu decision.

Template imports are excluded/deferred without rendering. Allowed abstract,
quotation and annotation languages are not flagged by a global language radar.
PDF existence never establishes identity/reading; no path is inferred from citekey.
Only the supplied explicit local path is checked; Zotero/HTTP references stay
unverified. Symlinked notes and complex YAML are unsupported. Link syntax supports
ordinary wikilinks and inline Markdown, not every Obsidian plugin/reference format.
