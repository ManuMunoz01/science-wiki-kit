# BIB-7 · Minimal read-only glossary adapter

Additive work after `594ea89a1ff71a971b6c52c1ffeafb713e402108` on t-38.
Code MIT; authored documentation/synthetic examples CC BY 4.0, retaining the
original science-wiki-kit attribution to MinorBaek. No internal documents or
scientific definitions are included. Existing BIB-1/conciliation files remain
unchanged; the existing five Skills are not installed or activated.

## Run with synthetic inputs

Python 3.12.14 tested; standard library only. From the fork checkout:

```bash
python t38/bib7/adapter.py --synthetic-root t38/bib7/fixtures --a t38/bib7/fixtures/shoulder.synthetic.md --b t38/bib7/fixtures/force.synthetic.md --out-dir /tmp/bib7-proposals-NEW
python t38/bib7/validate.py /tmp/bib7-evidence-NEW
```

Use NEW directories: existing destinations are refused. Adapter output must be
outside BOTH the input root and this development checkout. The output directory
is created with mode 0700 and suggestions.proposed.json with 0600 on POSIX.
Only count/type metadata goes to stdout. No source passage is logged by the CLI.
Export may contain full definitions and raw record spans: never put real exports
or populated review queues in a public repository. Filesystem permissions do not
replace access policy for a future cloud/sync destination.

The CLI currently REQUIRES a `.t38-synthetic` input-root marker. It does not scan
recursively or fetch anything: each A/B file must be named explicitly inside
that root. Symlinked files/paths, duplicate inputs, empty recognized scope, input
changes during reading, existing output and output inside the checkout/input
root are rejected. The marker is an operational guard, not proof of data origin;
only the invented fixtures are authorized in this iteration. Real export support
must be separately reviewed and authorized, not enabled by marking real folders.

## Supported formats and preservation

**A:** H2 concept sections; H3 entries shaped `### H-001 · Author (year)`.
Only H-prefixed, numeric-ending IDs are recognized (the prior synthetic H-Á-03
variant remains supported). Other H3 headings delimit editorial sections, not entries.
IDs are copied literally (including accents/punctuation), never normalized.
Recognized labelled fields may be plain, bullets or bold labels: term, translation,
alias, definition/use, context, provenance, citekey, source and location. Repeated
and unknown fields remain in the fields array. The entire raw Markdown entry
span and snapshot/line locator are retained, including comments and line endings.
Optional existing glossary_id in flat frontmatter is read using the BIB-1 parser;
missing glossary IDs are valid, and the document reference is sufficient.

**B:** three-column Markdown with the supplied Term/Usage-and-location/Source
headers (Spanish labels). Optional outer pipes and escaped pipes are supported.
Every physical data row remains ONE observation, with entry_id=null. Mixed
usage/location/definitions remain one cell; multiple source references stay on
that row. The adapter does not assign fragments to individual studies or guess
years from citekeys. All row locators carry the document SHA-256 and line number;
they are temporary snapshot references, never new persistent IDs. Moving a row
or editing the document requires rereading/rebinding the locator.

An optional glossary_id and existing entry IDs are preserved when present. No
uniform source schema, migration, taxonomy, new YAML field or ID assignment is
introduced. No note, alias, glossary or source file is written.

## External proposal contract

The output follows the intent of t38/conciliation/integration.md: proposal ID,
kind, unchanged target IDs or null+temporary locator, complete observations,
reason, pending-review status and action=none. Observations are also retained in
a top-level list. IDs starting proposal- or containing snapshot/line references
are external report identifiers only. The envelope is not a real-library schema.

- term_candidate: an observed entry/row for review, not an automatic new entry.
- terminology_overlap: exact normalized label/explicit-alias overlap, using BIB-1
  normalization; no translation, semantic synonym claim or concept merge.
- glossary_inconsistency: missing/explicitly pending structured provenance,
  conflicting declared years, repeated entry ID or ambiguous relation syntax.
  This is a review item, not proof of a scientific error. Lack of row IDs is valid.
- bibliographic_alias_statement: an explicit alias statement in the document,
  not a terminology alias and not independently verified bibliographic identity.
- bibliographic_identity_candidate: an explicitly labelled possible duplicate,
  never inferred from repeated citekeys or term coincidence.
- dataset_relationship_review: an explicitly labelled possible data reuse,
  preserving distinct publications; no independence/dependence finding inferred.

The last three kinds are produced only from these explicit labelled statements
in A: Alias bibliográfico / Posible duplicado bibliográfico / Posible reutilización
de datos, each containing exactly two linked source references and `->`. These
are supported synthetic declaration syntax, NOT newly required library fields.
Other prose remains raw; malformed declarations are pending, not reconstructed.
The alias-statement kind extends the proposed enum so it cannot be confused with
possible duplication. Source relationship assertions remain unverified.

Sources are recognized conservatively as explicit Citekey fields, wikilinks or
`[@citekey]` references. All raw source text is retained. A shared source across
entries is normal reuse of a reference and does not mean duplicate bibliography.
Documented aliases, duplicate records and separate publications using one dataset
remain distinct review problems; this adapter does not solve record-level
bibliographic deduplication or count independent studies.

## Reused components

- t38/bib1/audit.py: existing normalization and strict flat YAML reader.
- wikikit/textio.py: byte-safe input; wikikit/lint/text.py: table shape guard.
- t38/bib1/validate.py: input snapshot hashing for tests/evidence.
- t38/conciliation: preserved proposal design, priorities and source/ID rules.

The original vocabulary generator is not rerun in place or reimplemented; its
canonical-note contract is retained unchanged. This adds only format readers,
conservative review proposals and safe external export. See report.md for actual
results, limitations and the bounded next integration step.

## Limited compatibility validation after 0777fe0

See compatibility-review.md for the invented user-described format tests and
remaining private-pilot conditions. The five known frontmatter keys (type, topic,
task, updated, status) are retained as document metadata only; none is interpreted
as proof of scientific review or imposed on source notes. Absence of glossary_id
is valid. The long bold labels below now map explicitly, while originals remain
unchanged in fields/raw_markdown:

- Definición o uso — paráfrasis verificada → definitions_or_uses.
- Contexto y criterios operativos → contexts.
- Procedencia y atribución → source_text.

The word verificada in a label does NOT establish verification. Source URLs are
retained as source_urls tokens without connecting to Drive/any network. The new
fixtures use drive.example.invalid (reserved non-resolving example domain), not
private Drive IDs. Original source text remains authoritative if URL punctuation
or Markdown syntax is outside this tokenizer's subset.

extraction_status distinguishes structured-declared-unverified, declared-pending,
declared-empty, declared-not-reported-unverified, not-structured,
source-text-not-structured and combined-cell-unparsed. A table cell with narrative
locations remains combined-cell-unparsed: [] in locations never proves the source
has no location. Explicit no informado text is only a declaration of absence,
not its verification. pending retains its prior role as a work queue;
pending_status on review suggestions explains these distinctions. No new data is
filled, no per-study attribution is inferred and no input/write capability is enabled.
