# BIB-1 · Field and convention map

Derived comparison, not a copy of internal documents. G/T refer to the source
versions fingerprinted in sources.json and the headings cited in compatibility-33.md.

| Kit convention | Oficina source / mapping | Action and boundary |
|---|---|---|
| title/authors/year/doi/citekey | Same existing YAML keys (T YAML; G §Referencia) | Read only; no DOI/title/year completion from patterns. Identity with Zotero remains unverified. |
| venue | journal (T YAML; G §Implementación de la plantilla) | No rename, no field injection. Kit's deprecated-key rule is not run. |
| type | No equivalent key in T YAML | Folder scope identifies external notes in memory; no stored note type. |
| status (draft/final) | review_status + full_text_status (G §Propiedades) | Not equivalent: review and access are independent. No promotion or quality score. Blank import values are pending, not invalid controlled values. |
| evidence_level | study_type (G §study_type) | NOT a semantic mapping. Validate design labels only; no evidence hierarchy or SR ranking injected. |
| field | topic (G §topic) | One approved primary topic; no automatic selection, duplication or scientific classification. |
| subfield | subtopic (G §tags y subtopic) | Multiple controlled values, exact accents; [] allowed where unsupported. Literal pending suffix generates a decision item. No scalar coercion. |
| tags | Existing descriptive YAML tags (G §tags y subtopic) | Keep apart from imported Zotero labels and author keywords. No copying between them. |
| concepts_touched/related_concepts | Body glossary / related-article sections (G §§Conceptos, Artículos relacionados) | No automatic YAML mapping or mandatory reciprocal link. Canonical glossary format awaits approval. |
| source_verification/last_verified | Fuentes y alcance de la revisión + actual access state | Textual scope is not a seal and does not prove reading; no new fields/dates. |
| volume/pages and check18_exempt | Reference section and original source (G §Referencia) | Not added as mandatory YAML. Publication-type exceptions and APA need source inspection. |
| Useful Quotes | Citas textuales relevantes | Optional; no required quote per article. Annotation/import expressions stay intact. |
| English source/analysis assumption | Spanish analysis + original-language abstract/terms/quotes | No global language-radar finding on allowed imported content. |
| paper stem Surname_Year | Actual Zotero citekey (G §Incorporación por letras; T YAML) | Exact string preserved. Filename difference/duplicate key is review, not auto-rename/merge; aliases may be legitimate. |
| concept aliases → single canonical | Per-source definitions with original term, variants and attribution | Test-only sidecar proposal preserves record identity, year/location/context and differing definitions. Shared normalized terms are candidates, not synonymy. |
| _VOCABULARY.md in place | New external proposal directory | No changes to existing glossary, notes, classifications or aliases. |
| PDF inferred from citekey | Only explicit existing link (G §PDF; §Flujo 19/10) | Check local existence in synthetic vault only; identity/reading unverified. HTML full text without a PDF is allowed. |
| Global skill installation | Repository-local instruction adapters | No Claude installers, ChatGPT Skill changes, native activation or synchronization claimed. |

## Template preservation

No supplied template was copied, rendered, edited or used as a public test fixture.
The test builder writes a short invented snippet with generic Zotero/Jinja syntax
only. It tests that unresolved expressions are deferred and input bytes stay intact;
it does not validate Zotero Integration execution. Real original expressions,
annotations, abstracts, journal, headings and classification remain untouched.

## Additional metadata: none adopted

The synthetic glossary JSON has software-test record keys; it is NOT a new library
schema. Adopting machine-readable glossary records, additional provenance fields,
freshness dates, source seals, canonical synonym policies or scientific review gates
requires Manu's explicit decision. Existing fields are sufficient for the current
state/taxonomy/documentary diagnostics; source truth cannot be inferred from them.
