# BIB-7 · Limited format compatibility review

2026-11-12, Europe/Madrid. Branch t-38, user fork.
Baseline: 0777fe03301b61caf9887788fecedee6fa3a4dc7.
No commit, push, PR, installation, remote connection or real-data reading.
New examples are invented, not copies of scientific definitions or private glossaries.

## Demonstrated incompatibilities and minimal corrections

Five new tests were written before implementation changes. Against the baseline
they did not pass (3 assertion failures, 2 errors for missing extraction metadata).
The pre-change log is /tmp/t38-bib7-compatibility-before.log. This is an expected
regression demonstration, not an unexplained remaining failure.

| User-described case | Baseline finding | Final limited correction / evidence |
|---|---|---|
| Long bold definition/context/provenance labels | Raw fields survived but structured definitions/context were empty | Add the three explicit label mappings; retain all original labels/values/raw spans. No broad fuzzy label matching. |
| Editorial H3 with a middle dot | Resumen was incorrectly treated as an entry ID | Recognize H-prefixed, numeric-ending IDs only. Non-entry H3 sections delimit records without creating observations; malformed H-like headers remain diagnostic. Prior H-Á-03 fixture still passes. |
| Frontmatter type/topic/task/updated/status | Inputs were left unchanged, but metadata was not exposed | Preserve the parsed flat frontmatter in document metadata, without treating status/updated as scientific review or creating glossary_id. |
| Narrative location / mixed table cell | Empty locations array lacked an explicit extraction-state distinction | Add extraction_status and proposal pending_status. A labelled narrative location is retained literally; unlabelled narrative is not-structured; table location/context remains combined-cell-unparsed. No page extraction or attribution guessed. |
| Explicit no informado / unknown values | Missing structured values and declared absence were conflated in the queue | Explicit no informado/no consta yields declared-not-reported-unverified. Pending/empty/unstructured values are distinct; none establishes absence in the source. |
| Source URL and citekey wikilink | Raw source text survived; URLs were not exposed separately | Preserve source_urls tokens without fetching or checking them. Invented Drive-shaped URLs use drive.example.invalid, never real document IDs. |

The wording paráfrasis verificada in a label remains a source declaration, not a
verification performed by the adapter. All observations remain declared-unverified;
scientific_validity stays not-assessed and action stays none.

## Format and relation checks

The compatibility A fixture has the five stated frontmatter keys, H2 concepts,
five H-xxx entries, the exact long bold labels, narrative source locations,
citekey wikilinks and a non-resolving example URL. Editorial H3 controls are not
scientific entries. The B fixture has the exact three columns and one row with
two publications and ambiguous clause-to-source correspondence. It stays one
ID-less observation; raw usage/location and both references survive unchanged.

Bold explicit bibliographic-alias statements and possible shared-data statements
remain different proposal kinds, both not-verified. Two distinct publication
references remain distinct; no bibliographic duplicate is inferred from them.
No entry/definition is merged and no permanent identifier is generated.

## Execution record

| Run | Actual result |
|---|---|
| New tests against unchanged baseline | 5 not passed: 3 assertion failures, 2 missing-field errors; confirms the regressions |
| New tests after correction | 5 passed |
| Full suite after corrections | 70 passed: all 65 previous tests + 5 new tests |
| Original lint self-test | PASS, 43 expected counters |
| Original BIB-7 fixtures | Still 8 observations and previous proposal-kind counts |
| New compatibility CLI fixture | 6 observations (5 H records + 1 table row), 0 parse diagnostics; 1 alias statement and 1 possible shared-data statement |
| Preservation/repeatability | Raw inputs unchanged and two external proposals byte-identical; previous no-overwrite/synthetic-only guards remain tested |

Reproduce combined tests, the original self-test and original BIB-7 proposal
checks using the unchanged runner, with a NEW directory:

```bash
python t38/bib7/validate.py /tmp/t38-bib7-compatibility-validation-NEW
python -I -m unittest discover -s tests -p test_t38_bib7_compatibility.py
python t38/bib7/adapter.py --synthetic-root t38/bib7/fixtures --a t38/bib7/fixtures/shoulder.compatibility.synthetic.md --b t38/bib7/fixtures/force.compatibility.synthetic.md --out-dir /tmp/t38-bib7-compatibility-proposals-NEW
```

Final execution logs: /tmp/t38-bib7-compatibility-validation/unittest-all.log and
original-selftest.log. The new format CLI output is in that directory under
format-proposals/suggestions.proposed.json. The pre-change failure log is kept
separately; logs contain only invented fixture content, not internal documents.
Tests are software evidence, not source-reading or scientific validation.

## Remaining limits

- Only the user-described syntax has been reproduced with invented examples.
  No real/anonymized glossary file or private export was read in this intervention.
- Explicit mappings are intentionally limited; unknown labels remain raw, not
  silently interpreted. The reader is still a flat-YAML/Markdown subset, not a
  general parser. Other entry prefixes, plugin layouts and complex YAML need
  explicit examples before support can be asserted.
- A non-entry editorial heading is distinguished syntactically, not by scientific
  content. An H-ID-shaped heading is only a declared record, not validated science.
- Narrative locations are preserved, not independently verified or converted into
  exact page/section coordinates. Table cells are not split into source-specific
  definitions without an authoritative binding. Unknown information is not filled.
- URL extraction is tokenization, not validation/access; unusual punctuation or
  Markdown URL syntax may require manual review of the retained source text.
- Bibliographic identity, documented-alias truth and shared-data relationships
  are not independently checked. Only explicit supported declarations are surfaced.
- The later bibliographic register remains unavailable and unread; its exceptions
  have not been reconciled. Original Skills and real-library permissions remain
  separate from parser compatibility.

## Verdict for a private read-only pilot

**Favorable synthetic compatibility result, conditional readiness for PREPARING a
small private pilot; real execution is not enabled or validated.** The actual CLI
still requires synthetic-marked inputs and rejects writes to input/repository
paths. No real-input switch, library writes, Skill installation or Drive/Zotero
connection was added.

Before a real pilot is executed, separately authorize one private snapshot/export,
review the relevant registry exceptions/label variants, select a private external
output location and retain human review of ambiguous bindings. Any controlled
real-export entrypoint must be reviewed separately; do not bypass the current
synthetic guard by adding its marker to real-library folders. The pilot should
read a bounded copy, preserve IDs/rows/raw content and produce proposals only,
without syncing or writing back to the Library.

BIB-7 format compatibility has advanced; BIB-4 gains clearer diagnostic semantics
without changing the lint engine. Neither subtask nor T-38 is declared approved
or closed. These local changes are presented for Manu's review.
