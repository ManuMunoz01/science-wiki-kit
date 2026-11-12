# BIB-1 · Document-grounded compatibility of the 33 kit rules

Review baseline: `22f1b2d81795a9071ddd3c32c06e71b94217804b`.
This replaces the *conclusions* of the provisional matrix for this new profile;
the old matrix/trial remain as historical artifacts. This is the complete
comparison for the two supplied documents, not human approval of BIB-1/4/7.
The separate update register was NOT supplied; later exceptions remain to reconcile.

G = internal guide, updated 2026-11-04; T = original scientific template.
Evidence references below identify headings/line ranges in the supplied versions,
without including their full text or internal research details. Fingerprints in
`sources.json` establish the exact versions. Attached documents are not repository
files. Classification: **D** directly compatible, **C** configuration,
**A** code adaptation, **N** not applicable to the documented Biblioteca contract,
**M** Manu decision needed. A is a compatibility judgment, not a claim that every
possible adapted detector is implemented. N never means "test passed".
No row is C-only: current folder names/lists are configurable, but the affected
original detectors also assume different field keys or semantic contracts. The
new adapter keeps those names, lists, headings and taxonomy in configuration; it
does not change the kit core or pretend configuration alone changes semantics.

| Rule | Classification | Document-grounded reason and evidence | New profile behavior |
|---|---|---|---|
| 1 Orphan concepts | M | Shared glossary and thematic organization are pending; no mandatory canonical concept-note graph exists. G §Conceptos para el glosario L510–526; §Glosario por temáticas L617–625; T §Conceptos L88–90. | Not run; do not report thematic notes as orphans. Agree glossary representation first. |
| 2 Orphan methods | N | No separate methods-note role or backlink obligation in the documented five-folder layout. G §Ubicación L52–63; T §Variables e instrumentos L46–48. | Not run. Scientific methods remain content, not inferred kit note types. |
| 3 concepts_touched | N | Not a template field. Concepts are collected in a body section without forced note creation. T YAML L1–14, §Conceptos L88–90; G §Conceptos L510–526. | No added field or empty-field finding. |
| 4 Unsourced claims | A | Attribution must distinguish results/calculations/interpretation and primary/secondary access, not mere proximity to any wikilink. G §Principios L65–79; §Resultados L382–392; §Procedencia L627–634. | Semantic source checking remains manual; original concept-only verb detector is not scheduled. |
| 5 Broken links | A | Preserve real citekey connections and explicit PDF links; no invented paths or links. G §Artículos relacionados L532–548; §PDF L550–552; T L96–102. | Path-aware note/PDF checks, ambiguous basenames reported, template/code/comment exclusion; Zotero URLs remain unverified, never dereferenced. |
| 6 Draft/promotion | N | full_text_status/review_status describe access and review, not kit final status or source-count promotion. G §full_text_status L169–175; §review_status L177–179; T YAML. | No age threshold, automatic task or promotion. reviewed is not quality certification. |
| 7 / 7b Index coverage | M | Guide specifies layout and future thematic work, but no mandatory index.md list/section-placement contract. G §Ubicación L52–63; §Pendientes L573–596. | No coverage assertion or forced index generation. |
| 8 Book/chapter sync | N | No chapters_ingested/_ChNN contract in guide/template. G §Ubicación; T YAML and analytical sections. | Not run; no claim that books cannot be added later. |
| 9 Chapter parent | N | No book field/chapter parent schema in the article template. T YAML L1–14; G §Plantilla L601–603. | Not run; no new book metadata imposed. |
| 10 Quick Stats | N | No Quick Stats table is required. G §Finalidad L9–13 and §Ubicación; T sections. | Not run; absent table is not zero drift. |
| 11 Coverage table | N | Classification is single topic, multiple controlled subtopic and descriptive tags, not the kit field/subfield count table. G §topic L83–98; §tags y subtopic L100–161. | Actual taxonomy is checked separately, without inventing an index table. |
| 12 Backlink symmetry | N | Related links are justified and reciprocal only when useful and verified, not mandatory concepts_touched reciprocity. G §Artículos relacionados L532–548; T L96–98. | No automatic reciprocal links or repairs. |
| 13 Alias without link | M | Glossary preserves per-source terminology; no approved canonical-only synonym bridge/compulsory links. G §Conceptos L510–526; §Glosario L617–625. | No alias-link backlog; vocabulary proposes review candidates without treating aliases as synonyms. |
| 14 Language radar | A | Analysis is Spanish but original abstracts, imported annotations, terms and quotations retain their languages. G §Resumen L189–191; §Anotaciones L487–489; §Conceptos L510–526; §Citas L528–530; T L24–28, L62–78. | English abstracts are valid guards. No global English-word radar. Section-aware language review remains manual. |
| 15 Synthesis eligibility | M | Thematic synthesis/glossary are future work; guide has no final/min_sources/State of Knowledge eligibility. G §Pendientes L573–596; §Glosario L617–625. | No kit synthesis quota or same-day freshness claim. |
| 16 Status/type vocabulary | A | Actual states are two independent fields and can be empty on import; type/status are absent. G §full_text_status/review_status L169–179; §Implementación L665–680; T YAML. | Validates allowed nonempty values separately; empty = pending review, unrendered template = deferred. |
| 17 Provenance missing | A | Provenance lives in Fuentes y alcance, not source_verification; abstract-only is a legitimate limited-access state. G §Principios L65–79; §Fuentes L554–556; T L104–106. | Empty source-scope section is pending scientific documentation, never a missing seal error. No proof of reading from text presence. |
| 18 Verified metadata | A | Reference verification is in APA/content and journal, not required volume/pages frontmatter plus seals. G §Referencia L183–187; T YAML and L18–22. | Metadata incompleteness is review; full APA/volume/page verification is manual and not implemented as kit Check18. |
| 19 Evidence level | A | study_type is design, not evidence hierarchy. Its empty state is allowed with uncertainty; no evidence_level field. G §study_type L163–167; T YAML, §Diseño L34–36. | Validates design vocabulary only. Does not map reviewed/design to strength of evidence. |
| 20 Quote artifacts | A | Actual optional quotation section differs from Useful Quotes; imported annotation expressions must be preserved. G §Citas L528–530; §Anotaciones L487–489; T L62–78, L92–94. | No per-article quotation requirement. Quote fidelity/artifact detector deferred; template entries not rendered or altered. |
| 21 Historical cutoff | N | Access state records actual consultation; no cutoff-based legacy cohort policy. G §full_text_status L169–175; §Principios. | No synthetic cutoff or rereading task. |
| 22 Stale warning/seal | N | No kit warning/seal grammar. Access limitations are explicit content and states. G §Principios; §Fuentes L554–556; T L104–106. | No stale-warning finding or seal conversion. |
| 23 Claim placeholders | M | Template expressions and incomplete scientific sections are legitimate pending work, not kit [pending claim] failures. G §Implementación L665–680; §Validación L682–688; T expressions/comments. | No kit placeholder pattern imposed; any rendered-note marker policy needs agreement. |
| 24 Deprecated keys | N | journal is the original field and must remain. T YAML L1–14; G §Implementación L665–680. | Check24 is not scheduled; never journal→venue. An empty override object alone would not clear the kit's recursive-merge default mapping. |
| 25 Uncited numbers | A | Own-paper numbers require verified scope and primary/secondary provenance; Zotero citekeys need not match Surname_Year. G §Resultados L382–392; §Procedencia L627–634; §Artículos relacionados L532–548. | No automatic numeric source/causal validity assertion. Scientific verification and adapted citation-span detector pending. |
| 26 Table structure | D | Optional tables must preserve their cells/meaning, and Markdown validation is required. G §Resultados L382–392; §Lectura de PDF/tablas L636–642; §Flujo L562–571; T L50–52. | Original code reused unchanged on rendered/supported source and theme notes. Malformed positive and valid/no-table guards. |
| 27 Mojibake | D | Preserve source names, accents, expressions and Markdown integrity. G §Ubicación L52–63; §Flujo L562–571; T YAML/expressions. | Original strict reversible-encoding detector reused; diagnosis only, no repair. |
| 28 Seal without date | N | Neither source_verification nor last_verified is required by template. T YAML; G §Fuentes L554–556. | No invented dates, fields or missing-seal report. |
| 29 Memory slug | M | No out-of-vault agent-memory slug policy is established by these sources. G §Ubicación; T §Artículos relacionados/PDF. | Not run. Real broken links still use adapted Rule5; no extra prefix prohibition. |
| 30 Vocabulary sync | A | Glossary retains distinct definitions/context by source and topic; its common storage is undecided. G §Conceptos L510–526; §Glosario L617–625; T L88–90. | Test-only records preserve canonicals/aliases, source, year, location and definitions; JSON proposal with per-topic grouping, no overwriting or false equivalence. Real glossary sync remains undecided. |
| 31 Seal description | N | Source limitations are in the actual scope section, not short kit seals. G §Fuentes L554–556; T L104–106. | Not run; missing scope is pending work under adapted 17. |
| 32 Pair seals | N | Guide requires justified source/relationship checking but no named pair-seal protocol. G §Artículos relacionados L532–548; §Principios; T L96–98. | No pair-seal fields/debt queue introduced. Scientific attribution stays human-reviewed. |
| 33 Title/venue | A | title and journal exist, venue does not; blank imports/unresolved expressions are not complete scientific notes. T YAML; G §Referencia L183–187; §Implementación L665–680. | Checks actual metadata types/completeness as review; retains journal and citekey; never rewrites. |

The new audit runs original checks **26 and 27 only**, supplemented by documented
Oficina-specific diagnostics. Every other rule is explicitly classified above,
not silently replaced by a passing zero. `notes_loaded`, `template_deferred`,
`kit_checks_run`, findings by category and `scientific_validity=not-assessed`
accompany every report. The legacy 33-rule runner remains unchanged and remains
available solely for its original synthetic contract.
