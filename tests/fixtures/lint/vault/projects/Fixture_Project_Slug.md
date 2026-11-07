---
tags: [project, fixture]
date: 2026-08-14
status: active
type: proyecto
project: fixture
---

# Fixture Project Note (memory-slug sweep)

Exercises Check 29's VAULT-WIDE scope: this note lives outside wiki, where no other
check looks. If the check's scope regresses to the wiki folders, the hit below disappears
and check29 falls to 0, which fails the self-test. One real hit, two guards.

- Real defect (must count): see [[project_fixture_memory]] for the durable decision.
- Inline-code guard (must NOT count): the slug `[[reference_fixture_memory]]` is quoted code, not a link.

```
[[feedback_fixture_memory]] inside a fenced block must NOT count either.
```
