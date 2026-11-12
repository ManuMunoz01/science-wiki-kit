# T-38 · Provisional compatibility matrix

Documentation CC BY 4.0; based on science-wiki-kit by MinorBaek. Reviewed against
`bb639423771a60b430819f11f62c56e29c225324`, especially `wikikit/lint/checks_*.py`,
`context.py`, `defaults.json`, and `skills/wiki-lint/references/check-origins.md`.
This is NOT a comparison with the actual Oficina Manu guide/template: their full
contents were unavailable. No actual schema, status policy or taxonomy is inferred.

D = reusable detector; C = configurable adaptation; A = code adapter or code change
needed for the stated extension. Every row still needs confirmation of policy.
All 33 numbered rules (including 7b) are called by the adapter; a call is not proof
that its prerequisites exist. The original self-test tests the original contract,
not compatibility with the real library. The synthetic trial covers only a subset.

| Rule | Original behavior | Route / configuration first | Provisional validation and limits |
|---|---|---|---|
| 1 | Orphan concepts | C: folder roles; requires inline links, concepts_touched or related_concepts | Trial fires (2); no imposed real backlink policy |
| 2 | Orphan methods | C: methods/papers/books roles | Trial guard: method cites synthetic source, zero; no scientific inference |
| 3 | Empty concepts_touched in non-stub papers | C if real field agrees; A for a different key | Trial fires (1); actual required fields pending |
| 4 | Unsourced verb claims in concepts | C: bilingual verb_list, radius, threshold | Trial Spanish positive (1); nearby any wikilink may suppress a finding; no evidence verification |
| 5 | Broken/empty/placeholder wikilinks | D with C: scanned folders/recursion, ignore patterns | Trial one broken target; cross-folder project and accented target resolve; basenames are ambiguous on collisions (adapter refuses them) |
| 6 | Stale drafts / promotion candidates | C: statuses must match draft logic; age/source thresholds configurable; A for different hard-coded status | Trial 2 undated drafts; never auto-promote; source count not quality |
| 7 / 7b | Index presence / section placement | C: manual mode, index_sections/exemptions | Manual mode enabled, 5 missing; real index policy unknown; bases mode skips both |
| 8 | chapters_ingested vs numeric _ChNN notes | C: books folder; A for other chapter naming | No books in trial: not exercised; original fixture only |
| 9 | Chapter book field / parent resolution | C if original chapter contract applies; A for other fields | No chapters in trial; original fixture only |
| 10 | Quick Stats counters in index | C: quick_stats_labels; A to translate hard-coded Quick Stats heading | Trial has no such table: zero is no coverage |
| 11 | Coverage by Field/subfield table drift | C: field_titlecase_map and folder roles; A for translated hard-coded heading/format | Trial has no table: zero is no coverage; do not invent taxonomy |
| 12 | concepts_touched to source backlink symmetry | C if keys agree; A for different metadata conventions | Trial empty list is caught by 3; asymmetry not exercised here |
| 13 | Documented aliases used without links | D/C: alias stoplist | Trial zero; original fixture positive; excludes blockquotes, not a duplicate detector |
| 14 | Foreign-language radar | C: enabled, headings, stopwords and guards | Enabled with English radar for provisional Spanish notes; 3 controlled Results headings; bilingual quotes may false-flag |
| 15 | Missing/stale synthesis on eligible final notes | C: thresholds and synthesis_block_heading; A if other hard-coded synthesis format differs | Trial draft-only: not exercised; same-day staleness blind spot remains |
| 16 | type/status vocabulary and template leaks | C: status_by_type | Trial invalid status (1); actual template types/statuses pending |
| 17 | Missing or abstract-only provenance | C only if source_verification applies; A for actual different key | Trial fires (1); field presence is not full-text verification |
| 18 | Verified source lacking volume/pages / dated exemption | C: exemption age; A for different fields / additional venue-language cases | No verified sources in trial; original fixture only; no metadata invented |
| 19 | Paper evidence_level vocabulary | C: evidence_level_vocab; A for another key | Trial invented-invalid value fires (1); use actual classification only after guide review |
| 20 | Leaked ]] in Useful Quotes blockquotes | A for translated hard-coded Useful Quotes heading | No trial quote section; original fixture only; cannot validate quotation fidelity |
| 21 | Pre-fulltext cohort by cutoff | C: synthesis.prefulltext_cutoff | Explicitly inactive in provisional config: cutoff unknown; original fixture tests it |
| 22 | Stale pre-fulltext warning after verification | C/A: original seal/warning conventions required | Not exercised in trial; hard-coded warning patterns may need language adaptation |
| 23 | Unfilled claim markers | C: unfilled_claim_patterns | Three Spanish controlled placeholders detected |
| 24 | Deprecated frontmatter keys | C: deprecated_frontmatter_keys | Original mapping retained only as synthetic policy; not exercised here; never rename actual YAML without review |
| 25 | Uncited statistical values | C: numeric/citation patterns, radius, methods fields; A for reliable citekey attribution | Trial has no numbers; original fixture only; author-year classifier assumes Surname_Year-like stems and may misclassify actual Zotero citekeys; no renaming proposed |
| 26 | Markdown table column mismatch | D | Three controlled malformed rows detected; original escaped-pipe guards retained |
| 27 | Reversible UTF-8/cp1252 mojibake | D | Original positive/guard fixtures; trial accents remain intact; no automatic repairs |
| 28 | Seal without last_verified | C if actual keys agree; A otherwise | No trial seals; original fixture only; never invent dates |
| 29 | Out-of-vault memory slug links | C: memory_slug_prefixes/exemptions | Explicitly inactive: no actual slug policy known; original fixture tests it |
| 30 | Missing/ghost generated vocabulary entries | A: original ASCII canonical-row regex fails spaces/accents | Trial upstream missing=4 vs Unicode supplement missing=3, ghost=1; preserve raw counters; supplement reads link targets without renaming canonicals |
| 31 | Short seal without explanatory verification text | C/A: actual verification schema and channels | No seals in trial; original fixture only; cannot prove underlying reading |
| 32 | Synthesis (note,work) pair without named seal | A for alternate block/seal conventions; original State of Knowledge parser remains | No synthesis in trial; original fixture only; seal mentioning a name is not scientific validation |
| 33 | Paper lacks title or venue | D if actual keys agree; A for alternative key mapping | Trial fires (1); authors/year/citekey/DOI are NOT validated by this rule |

## Cross-cutting adaptation

The adapter refuses empty scopes, missing configured folders and canonical basename
collisions (casefold/NFC). It generates a separate Unicode-aware vocabulary comparison,
recurses through configured concept/method folders, and broadens duplicate proposals
to any normalized shared canonical term or alias across fields. This deliberately
increases review candidates; it never identifies semantic equivalence or merges notes.
Original generators still run unchanged. Folder roles under `4. Temas` are TEST
subfolders, not a claim about how the real vault separates concepts, methods or books.

## Actual-library comparison pending

| Available evidence | Known constraint | Pending full-text comparison |
|---|---|---|
| User-described Obsidian/Biblioteca layout | Preserve five top-level folders | Inventory exact scanned subfolders, archives and exclusions |
| User-described scientific template | Preserve YAML, Zotero expressions, analytical headings | Map each real field/heading to the rows above; do not use Articulo_modelo.md |
| Citekeys linked to Zotero | Preserve identity; no automatic renaming | Exact citekey storage, filename relation, links, DOI/PDF conventions |
| Guide and change-log URLs | Documents identified, not read | Status/evidence vocabularies, provenance, exemptions and approved history |

Required attachments: the complete current bibliographic guide and
`Articulo_cientifico.md` in original text/Markdown form. Also useful: bibliographic
change log and an anonymized completed source note plus one thematic/glossary note.
No private scientific content is needed in the test vault. The real-library matrix
must be completed after reading these documents, not reconstructed from URLs.
