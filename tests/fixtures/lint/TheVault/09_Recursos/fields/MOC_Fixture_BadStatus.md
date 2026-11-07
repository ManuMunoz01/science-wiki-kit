---
tags: [MOC, fixture]
date: 2026-08-14
status: empty
type: MOC
field: "fixture"
---

# Fixture Bad Status MOC

Exercises Check 16 with the MOC status vocabulary (added 2026-08-14, auditoria A4/C3):
`status: empty` is outside config.status_by_type["MOC"] and must flag. This is the exact
defect class found live (two field MOCs carried scaffold `status: empty` while their own
body said "Status: Active"). MOC_Wiki (active) and MOC_Fixture_Sub (active) are the
negative guards: if the MOC vocab entry is removed from config, the type is skipped
again and check16 falls back to 0, which fails the self-test.
