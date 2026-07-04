# Cross-pollination log

Append-only record of Recon/Audit cross-pollination rounds — see `docs/multi-agent-roles.md`. Each entry is a short record of one relay round, not a transcript. Purpose: evidence that the workflow described there is actually being followed, and precedent for future sessions to pattern-match against.

Adopting projects: copy this file (reset to just the format below) into your own `docs/` directory.

## Format

```
## YYYY-MM-DD — <branch/PR>
- **Asked:** <what was requested, and how it was scoped>
- **Returned:** <finding, "no issues found", or a question>
- **Resolved:** <integrated as-is / integrated with changes / escalated to human owner / dismissed as false positive — with why>
```

---

## 2026-07-04 — TheWarRoom `session/glm-audit-fixes-2026-06-28` (PR #1)
- **Asked:** Not a fresh dispatch — this is the formalizing pass for TheWarRoom's 2026-06-28 GLM 5.2 whole-repo de-slop audit (three passes: engine/rubrics/composition/harness, stores/DB/primitives, ingestion pipeline; ~30 findings, verdict at `TheWarRoom/docs/build-handoffs/audit-glm-2026-06-28.md`), which ran and shipped its B6-watch-list items at the time but was never logged here and left its 2 MAJOR findings untriaged against current source. This round re-verified both MAJORs against `main` (`8f57874`, 6 days and 4 build sessions later).
- **Returned:** Both MAJORs still live, unchanged: (1) `playerid.New` accepts signed numeric strings (`"+99"`, `"-5"`) — `strconv.Atoi` allows a leading sign, `strings.TrimLeft` only strips `'0'` runes, so a signed id survives into the canonical form (`"+99"` → `"0+99"`) and silently fails to cross-reference against the same player's unsigned id (AD-06/RISK-003). (2) `madden.fillRatings`' string-rating skip guard (`val[0] == '"'`) doesn't catch a JSON `null`, which unmarshal-succeeds to `0` with no error — a silent zero on K's 0.60-majority Madden signal.
- **Resolved:** Both fixed on TheWarRoom `session/glm-audit-fixes-2026-06-28` (PR #1) with planted tests confirmed to fail pre-fix (`git stash` round-trip) and pass post-fix; `make lint` 0 / `go test -race ./...` green. The ~25 remaining MINOR/IMPROVEMENT/NOTE items were reviewed but not individually re-triaged this round — none are BLOCKER-class, several (duplicated helpers, doc drift) are logged as future M17 candidates in TheWarRoom's own `docs/cross-pollination-log.md`, which this round also adopted into that repo. This satisfies the standing cross-pollination pilot: stayed in scope (verified against source, didn't act on unconfirmed leads), flagged the still-open MAJORs to Christopher before fixing rather than silently patching, both findings were real (not noise), and the relay (audit → dormant → this triage pass) still surfaced a live data-integrity bug 6 days later — the overhead was worth it.
