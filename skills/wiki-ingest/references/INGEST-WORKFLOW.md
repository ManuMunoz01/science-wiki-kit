# Ingest Workflow: Detailed Procedure

## Step 1: Resolve the paper from the reference manager (Zotero MCP)

```
1. zotero_search_items(query="{title or author or citekey}", limit=5)
   -> pick the matching item; keep zotero_key and item_id
2. zotero_item_metadata(item_id={item_id})
   -> title, authors, year, venue, doi, citekey, abstract, tags, collections
3. zotero_item_fulltext(item_id={item_id})
   -> full text if available (use for concept and method extraction)
```

**Search semantics** (verified against zotero-mcp 0.3.x with the local API enabled; re-check after major upgrades):

- **Look a known paper up with `qmode="titleCreatorYear"`** (the default). Against the *local* API it also matches Better BibTeX citation keys; the Zotero Web API does not index them.
- **A hyphen in the query is read as OR, not as a literal.** `smithJonesValidity2023` is fine, but `smith-jonesValidity2023` searches `smith` OR `jonesValidity2023` and drags in unrelated work. **Write the hyphen as a space** to require both halves. This bites on every compound surname.
- **Never use `qmode="everything"` for known-item lookup.** It searches attachment full text and returns the matching *child* item, so the key belongs to a PDF, not to the article, and `zotero_item_metadata` then yields attachment metadata. Reserve `everything` for topic search.
- `zotero_item_metadata` returns a `Citation Key:` line. **That is the only valid source for the note's `citekey` field.** Never construct one.

If `zotero_item_fulltext` returns empty or fails (HTTP 404 means Zotero's fulltext index is not built for that attachment; "No suitable attachment found" means a metadata-only item), the PDF usually still exists locally. Try it before degrading to abstract-only:

1. **Locate the PDF** in your library's storage folder. Search with `find "<dir>" -iname "*.pdf" | grep -i <author>`, not `find -iname "*<author>*"`, which has documented false negatives on some filesystems (network or cloud-synced drives).
2. **Extract with a fidelity-first extractor.** Recommended: `docling` (layout-aware, tables as Markdown, keeps ±). Fallback: `pdftotext -layout -enc UTF-8`. **Always pass `-enc UTF-8`**: on Windows the default is Latin-1, accents break and a search for a term with an accent returns a false zero. Watch for fused numbers, dropped tables and corrupt glyphs: open the page image whenever a number matters.
3. **Scanned PDFs** (image only, under about 800 characters of text): OCR them, or find a text-layer copy elsewhere. A numeric anomaly may be the source's own typo; verify against the rendered page before "correcting" it.
4. **Citekey ambiguity**: a Better BibTeX year-suffix citekey (`...2019a`) does NOT reliably map to Part 1 versus Part 2 of a same-author, same-year series. Verify the real title via `zotero_item_metadata` before editing the note.

Only if no local PDF is recoverable:
- Use the abstract from metadata for concept extraction.
- Add to the paper note: `> [!note] Full text not available. Extraction from abstract only.`

> **Reading oversized fulltext.** When a tool result exceeds the inline limit the harness persists it to a file: `Read` that path directly instead of re-fetching. If you write extracted text to a file in order to `Read` it, put it in the project's temp directory, not an OS-specific `/tmp` that the Read tool cannot open (Git Bash on Windows maps `/tmp` somewhere Windows tools cannot see).

## Step 1.5: PubMed fallback (paper not in the library)

Use when Step 1 fails because the paper is not in the user's library (confirmed by the user).

```
1. article_searcher(keywords="{title or author}")  -> pick the match, note the PMID
2. article_getter(pmid={pmid})
   -> one call returns title, abstract, source AND full text when a PMC copy exists
```

Store the PMID in the paper note as `notes: "PMID: {pmid}"`. PubMed covers biomedical literature well but does not replace the library as canonical source: if the user later adds the paper to it, update the note with the real citekey.

## Fallback: reference manager unavailable

1. Try PubMed (Step 1.5) for biomedical papers.
2. Ask the user for the DOI, the citekey, or a pasted abstract.
3. DOI provided: note it, do not fabricate metadata.
4. Abstract pasted: use it for extraction, fill what is known, flag the rest.
5. URL to an open-access paper or blog post: convert to clean markdown first (web-to-markdown tool), then treat it as abstract and body.

## Step 2: Paper note filename

- `FirstAuthor_Year_Keyword.md`
- FirstAuthor: last name of the first author, ASCII only, no spaces
- Year: 4 digits
- Keyword: 1 to 3 words on the topic, no spaces, no special characters
- Examples: `Smith_2021_Isokinetic_Reliability.md`, `Garcia_2024_Machine_Learning_Review.md`

Check before writing: `Read "<wiki_root>/papers/{filename}.md"`. If the file exists, update it.

## Step 2.5: Source-fidelity gate (mandatory before writing the note)

Apply `WIKI_SCHEMA.md` → **Source-Fidelity Rules**. Quick checklist (examples in `INGEST-PITFALLS.md`):

1. **Do I have the fulltext in front of me?** If NO: `status: draft`, no quotes, no numbers, flag inline. STOP: do not populate Useful Quotes or statistics. (P1)
2. **Quotes** are copy-pasted verbatim from the fulltext, never from memory and never misattributed. (P3)
3. **Numbers** come from the TABLES, not the abstract; abstract-versus-table discrepancies are documented inline. (P2) If the paper has a PMCID, cross-check cells against the Europe PMC JATS before the page image; on a mismatch the printed PDF wins and the discrepancy is noted.
4. **`evidence_level`** follows the decision table (closed vocabulary; Step 5.5). (P4)
5. **`source_verification`** (library key + date + what was verified) and volume, issue and pages are filled. (P5)
6. **Every value is labelled with its group or side** (A vs B, dominant vs non-dominant, left vs right). (P6)
7. If this **corrects a previous value**: search the wrong value across `papers/`, `concepts/` and `methods/`. (P7)

## Step 3: Fill the paper note

Follow `templates/paper.md`.

**Frontmatter from the library:**
- `title`: exact title
- `authors`: last names, or "Last A, Last B"
- `year`: integer, not string
- `venue`: journal or conference
- `doi`: full DOI string
- `citekey`: the library's citekey, if available
- `research_lines`: slugs from `WIKI_SCHEMA.md`

**Sections:**
- **Research Question**: 1 to 2 sentences
- **Key Claims**: 3 to 5 bullets
- **Method**: design, sample, key instruments, statistical approach
- **Evidence & Key Results**: key quantitative results with effect sizes if available
- **Strengths**: 2 to 3 methodological strengths
- **Limitations**: 2 to 3, from the paper's own discussion where possible
- **Relevance to My Research**: direct link to the user's research lines

## Step 4: Concept extraction heuristic

Read abstract, results and discussion. Identify:

**Good concept candidates:**
- Named constructs the paper measures or manipulates
- Interventions, training methods or protocols
- Outcome or performance variables
- Clinical or injury constructs

**Not concept candidates (use `methods/`):**
- Statistical tools (ICC, ANOVA, mixed models, Cohen's d)
- Study designs (RCT, cross-sectional, scoping review)
- Instruments (unless the paper is specifically about the instrument)

Aim for 3 to 8 concepts per paper. More than that usually means noise.

## Step 5: Method extraction heuristic

Identify the PRIMARY methods: the main statistical analysis, the main measurement instrument or protocol, and the study design if it is the paper's key methodological contribution. Limit to 2 to 4. Generic methods (t-test) get a method note only if the paper makes a methodological contribution about them.

## Step 5.5: Evidence level classification

Assign one `evidence_level` from the controlled vocabulary (full table in `WIKI_SCHEMA.md` → Evidence Level Vocabulary). This is the **design axis**; it feeds the living-synthesis layer's confidence rating.

Decision shortcuts:
- **`SR-MA` vs `SR`**: does the paper pool effect sizes quantitatively (forest plot, pooled SMD/OR)? Yes: `SR-MA`. Systematic search with narrative synthesis only: `SR`. A scoping review is `SR`.
- **`RCT` vs `RCT-crossover` vs `CT`**: randomized parallel groups: `RCT`. Randomized within-subject order: `RCT-crossover`. Intervention with a control but no randomization: `CT`.
- **`cohort` vs `cross-sectional`**: follow-up over time: `cohort`. Single time point or correlational: `cross-sectional`. A single-arm pre/post study is `cohort`.
- **`pilot`**: explicitly a pilot or feasibility study, or n too small to be powered for efficacy, even if nominally randomized.
- **`case-series`**: descriptive, no control group, small N.
- **`narrative`**: non-systematic review, commentary, consensus or expert opinion.
- **`animal`**: non-human, in-vitro or preclinical (flag the transfer caveat in the body).
- **`textbook`**: book or chapter overview (default for `wiki-ingest-book` notes, unless the chapter is itself a standalone SR/MA).

Pick the **strongest** applicable design when a study mixes them, and note the nuance in the body.

**Measurement quality is NOT recorded here.** It is per outcome (one paper can use MRI for one variable and anthropometry for another), so it stays **inline in the finding** as a parenthetical. The synthesis skill harvests design from frontmatter and measurement quality from finding text.

## Step 6: Routing disambiguations

Wikis accumulate near-duplicate constructs that must not be merged. Keep a short list of confirmed routing rulings in your own `WIKI_SCHEMA.md` (or a `ROUTING.md` next to it) and consult it here. General principle: **route by the function measured, not by surface name similarity.** A worked set of rulings from a sport-science wiki is in `examples/sport-science/routing-disambiguations.md`.
