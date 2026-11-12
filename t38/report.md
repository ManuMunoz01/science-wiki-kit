# T-38 · Codex Cloud reproducibility and adaptation report

Dated 2026-11-12 (Europe/Madrid). Documentation CC BY 4.0. All new code MIT.

## Repository and boundaries

Development checkout: `/workspace/science-wiki-kit`, `origin` =
`https://github.com/ManuMunoz01/science-wiki-kit.git`. Local branch `t-38`.
HEAD is exactly `bb639423771a60b430819f11f62c56e29c225324`, the requested original
baseline. `upstream` = `https://github.com/MinorBaek/science-wiki-kit.git`, recorded
as reference only. No upstream fetch/update, source edits, commits, pushes or PRs
were made in this intervention. Branch originally called `work`, not main;
`t-38` was created locally. Existing tracked files remain byte-for-byte unchanged.
All development changes are additive and uncommitted. Licences retained.

The user reports an earlier Windows / Codex Desktop evaluation on Python 3.12.14,
labelled v0.1.2. Its technical report/evidence folder were not supplied. This task
does not assume access to Windows files or claim to have reproduced that OS.
The exact commit, rather than an independently verified tag, identifies the baseline.

## Independently executed in Cloud

Linux, Python 3.12.14, standard library only; no pip dependencies, installers,
global skill registration, external scientific data or credentials introduced.
`pdftotext` 25.03.0 is available, but no PDF ingestion/reading was tested here.

Final reproducible evidence: `/tmp/t38-validation-reviewed/`.
Command: `python t38/validate.py /tmp/t38-validation-reviewed` (use a NEW directory
for a future run). Separate logs preserve each subprocess's return code.

| Evidence | Outcome | What it establishes |
|---|---|---|
| Original unittest modules | 39 passed: wikikit 21, pmc_tables 9, example 2, fixes 6, lint 1 | Original tests run on Cloud independently of new adaptation tests |
| Original lint self-test | PASS, 33 numbered rules including 7b; 43 expected counters matched | Original synthetic contract and frozen-clock regressions |
| Combined original + adaptation suite | 44 passed | Original 39 plus 5 new tests |
| Original lint CLI on new synthetic vault | Completed, exit 0, findings intentionally present | CLI runs; exit 0 is NOT a clean-library signal |
| Original vocabulary CLI | 4 entries, 1 candidate pair; external outputs | Original bilingual generation on top-level test notes |
| Adapted lint | 6 notes, all 33 rule numbers called | Controlled diagnoses; applicability differs by rule |
| Adapted vocabulary | 4 entries, 1 candidate pair | Canonical names and Spanish/English aliases preserved |
| Repeat runs | Two byte-identical proposal/report pairs on same date | Same-day repeatability; date header changes across days expected |
| Input invariance | All synthetic vault file hashes identical before/after original/adapted CLI runs | No notes/config/vocabulary overwritten |
| Safeguards | Tests reject existing output, output inside vault, empty scope and ambiguous basenames | Failure cases are intentional expected rejections |
| Nested/bilingual variation | Nested concept collected; alias change adds candidates and changes output | Adapter extends original nonrecursive collection and two-term/same-field candidate rule |

## Controlled findings

The six-note vault has intentionally invalid source status/evidence level, a broken
link, missing title/venue and concepts_touched, Spanish unsourced claims, English
Results headings, three placeholders and three malformed tables. Assertions cover
rules 3, 4, 5, 14, 16, 19, 23, 26 and 33. A paired guard replaces ONLY the broken
link and proves Check 5 decreases by one. Links to a project in another top-level
folder and to an accented canonical concept do NOT count as broken.

Representative counters: 3=1, 4=1, 5=1, 14=3, 16=1, 19=1, 23=3, 26=3, 33=1.
Other outputs include orphan concepts (2), undated drafts (2), index omissions
(5), missing provenance (1). These are test findings, not real-library defects.

The original Check 30 reports 4 missing vocabulary entries and 1 ghost because its
canonical-row regex excludes spaces/accents. The separate Unicode-aware supplement
correctly treats `Fuerza máxima` as listed: 3 missing and 1 ghost. Original counters
are not rewritten to manufacture agreement.

Vocabulary candidate: `Fuerza máxima` / `Maximal_Strength`, sharing normalized
`fuerza maxima` and `maximal strength`. `Potencia` and `Dinamometría` remain
independent canonicals. A separate test proves single shared accented/uppercase
aliases across fields become review candidates; unrelated aliases are guards.
Candidates are not semantic-equivalence findings and are never merged.

Rules 7/7b use manual mode and 14 is enabled. Rules 21 and 29 are explicitly
inactive because the real cutoff/prefix policy is unknown. Rules depending on
books, chapter metadata, index count tables, synthesis, seals or citations may
return zero without applicable test data. They are NOT declared validated by this
trial; consult the full 33-row matrix and original regression fixture separately.

## Local Skills: tested vs unavailable

Two local skill definitions exist under `.agents/skills/`, without changing the
original `skills/` tree or globally installing anything. Their file-based
procedures were explicitly read and invoked by this Codex agent. Lint produced
6-note diagnostic output; vocabulary produced the four-entry proposal. Both
retain references to original scripts/documentation and prohibit mutation.

Native `skills/list` was attempted through local Codex app-server, with no model
turn. Startup failed opening `/home/agent/.codex/state_5.sqlite` in read-only
storage. Retrying with task-specific sqlite/log locations and no-daemon still
returned read-only filesystem. No credential/state relocation or sandbox bypass
was attempted. The probe script is retained for a writable runtime. Therefore
native discovery and `$oficina-...` activation remain UNVERIFIED; successful CLI
execution is not reported as native invocation. Nothing was installed or changed
in ChatGPT Skills.

## Actual-library documents and compatibility

User supplied links identifying the bibliographic guide, Articulo_cientifico.md,
5. Templates and bibliographic change log. There is no callable Drive connector.
A read-only request for the guide failed with `CONNECT tunnel failed, response
403` (HTTP 000); no document body was obtained. This is an observed access failure,
not evidence about whether the documents exist or their permissions outside Cloud.
No network-policy change was made. No real scientific library was accessed.

Attach the COMPLETE current guide and `Articulo_cientifico.md` (original Markdown
preferred), plus the change log if possible. Do not substitute Articulo_modelo.md.
A later comparison must preserve real YAML, Zotero expressions, headings,
citekeys and taxonomy. Current config maps only the known top-level layout and
INVENTS clearly labelled test subfolders/metadata, never a definitive schema.

## Incidents and outstanding checks

- Original Check 30 Unicode limitation reproduced and supplemented separately.
- Original vocabulary nonrecursive collection and two-shared-term/same-field
  threshold examined; new adapter and tests add recursion/single-term review.
- Native Codex skill discovery is blocked by read-only runtime state.
- Drive guide/template inaccessible from this runtime; definitive matrix pending.
- Earlier reported Python 3.9 installer risk is consistent with
  `tools/set_kit_dir.py` using `Path.write_text(..., newline=...)` (newer Python API).
  Python 3.9 and the installer were NOT run; no installer fix claimed.
- Earlier reported chapter-helper incident lacks the original reproducer/report.
  Helpers inspected, but that incident has NOT been reproduced, diagnosed or fixed.
- Vocabulary source hints still use the upstream top-level paper/book lookup;
  nested source-hint attribution is not extended or verified.
- No Windows/macOS compatibility run, scientific source validation, Zotero citekey
  resolution, DOI verification, PDF integrity or full YAML/Jinja parser validation.
- No automatic synchronization, repairs, status promotion or vocabulary adoption.

## Recommendation

Next: use Chat to supply and settle the authoritative guide/template rules, then
Codex to map fields through configuration first and add anonymized positive/guard
fixtures. Diagnose native local Skill discovery in a runtime permitting its state
DB. Use Work only to update T-38 from `task-update.md` after human review. No task
or subtask is marked complete; commits, publication and PRs still require Manu's
explicit authorization. Scientific approval remains a separate human decision.
