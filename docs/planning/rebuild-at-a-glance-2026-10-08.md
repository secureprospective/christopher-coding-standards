# New coding standards — proposed map

**Goal:** no slop · elegant · readable · maintainable
**Principle:** freedom in implementation; rigor in acceptance.
**Status:** planning drafts—not implemented/adopted. Existing guardrails remain live.

## What applies to your projects

```text
CANONICAL STANDARDS
│
├── QUALITY CONTRACT
│   Behavior · Simplicity · Readability · Maintainability · Safety · Evidence
│
├── STACK OVERLAYS — select what the project needs
│   TypeScript ── Astro / Cloudflare Workers / Bun-ECS
│   Go · Python · Bash
│
├── REVIEW METHOD
│   Architecture + data flows + preserving debloat suggestions
│
└── TRACKING [proposed, not built]
    Source mappings + per-unit revisions/fingerprints + read-only status
                          │
                          ▼
                    YOUR PROJECT
    Short instructions · relevant configs · project-specific rules
    Task-relevant flow maps · actual test/check evidence
```

## Coding and review loop

```text
APPROVED TASK
 behavior + scope + acceptance
          ↓
INITIAL DESIGN SLICE
 real components → data contracts → transformations → outputs
 state owners + trust boundaries + failure routes
          ↓
IMPLEMENT ↔ TEST
 existing idioms; simplest sufficient design
          ↓
REVIEW
 ├── requested behavior ↔ actual behavior
 ├── initial map ↔ source-traced / test-exercised flows
 ├── responsibility / dependency / state ownership
 └── bloat → bounded suggestions, not automatic rewrites
          ↓
VERIFY / RESOLVE
 same job + preserved guarantees + readable result
          ↓
EVIDENCE → HUMAN ACCEPTANCE → INTEGRATION
```

Logical checkpoints—not extra agent roles or repeated approvals. Small fixes reuse existing flow descriptions. Already-correct behavior permits **no change**.

## Review outputs

| Architecture/data flow | Debloat |
|---|---|
| Real node / edge / source location | Concrete unnecessary cost |
| Contract / ownership mismatch | Smallest simplification |
| Intended vs implemented route | Guarantees + risks + preserving tests |
| Source-traced / exercised / unknown | Before/after lines and characters, when measured |

**Smaller is useful; harder to read is not.** No size quotas, test deletion, blind abstraction or code-golf.

## Enforcement

| Machines, where applicable | Focused judgment |
|---|---|
| Format · lint · types · behavior tests · scoped security | Intent · architecture · readability · test quality · safe simplification |

Green checks do not prove elegance. Missing/skipped verification stays visible.

## Keeping projects current [proposed]

```text
Approved rule change → relevant comparison → update proposal
    → preserve customizations → verify → accepted per-unit baseline
```

Keep **freshness / provenance / configured controls / executed evidence** separate. A version stamp is not approval or proof. No blind overwrites.

## What this session has completed

| Completed | Still draft / unbuilt |
|---|---|
| Repo/consumer mapping | Six-rule quality contract + examples |
| Seven-overlay investigation | Architecture/data-flow/debloat method |
| Research accuracy audit | Tracking / update mechanism |
| Canonical GitHub control audit | Separated agent/publication authority |

**Audit blockers:** admin credential · zero required approvals · required TS checks skip real gates. No external-autonomy corridor activated.

## Before implementation

```text
Review contract/map → validate representative diffs
    → settle material ownership/authority → map rules to real stack gates
    → approve first bounded implementation
```

Proposed infrastructure starts read-only. No new service required to validate this review method. Durable fleet decisions need ClaudeBox/expert input.

**Details only when needed:**
- `code-quality-acceptance-contract-draft-2026-10-08.md`
- `architecture-dataflow-debloat-review-draft-2026-10-08.md`
- `canonical-github-authority-audit-2026-10-08.md`
- `rebuild-considerations-2026-10-08.md` — decision/evidence log
