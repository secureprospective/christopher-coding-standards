# Christopher Coding Standards

**Stop the slop. Excellence is the standard, not the goal.**

A portable, copy-and-customize kit for correct, elegant, human-readable and maintainable code. Freedom in implementation; rigor in acceptance. No scanner, model or green badge guarantees quality.

## Start here

- Maintaining this kit: [AGENTS.md](AGENTS.md) → [task index](docs/INDEX.md) and [actual kit map](SYSTEM_MAP.md).
- Writing/reviewing code: [six-dimensional quality contract](docs/quality-contract.md) plus relevant project/stack context.
- Adopting elsewhere: [adoption proposal skill](skills/adopt-coding-standards/SKILL.md). Use consumer templates, not this kit's maintainer identity/map. Preserve customizations; do not copy every file or blindly enable workflows.

## What applies

```text
Shared quality contract
    + chosen language/runtime overlay
    + actual project rules, components and data flows
    → implementation + meaningful checks + focused review
    → evidence-based acceptance under existing owner authority
```

Behavior, simplicity, readability, maintainability, safety and evidence all matter. Real domain contracts and state/trust ownership determine structure. Useful adapters and cohesive larger code are valid; speculative platforms, proxy size quotas, blind DRY, code-golf and misleading tests are not.

Use trusted deterministic checks for actual failure modes. Independently assess things they cannot prove. A changed gate must accept clean input and reject its intended violation with the correct diagnostic. Green skipped checks, a version receipt or a diagram establish neither behavior nor approval.

## Kit contents

| Surface | Purpose |
|---|---|
| [Core contract](docs/quality-contract.md) | Compact acceptance rules, concrete safety/evidence constraints and review verdicts. |
| [Architecture/data-flow/debloat method](docs/architecture-review.md) | Optional focused review of actual code responsibilities, contracts, ownership, effects and preserving simplifications. |
| [Consumer instructions](templates/AGENTS.md), [map](templates/SYSTEM_MAP.md) | Project-customized starting points; required facts/checks are filled from the actual project. |
| `templates/typescript/` | Base TypeScript tooling/configs. |
| `templates/astro/`, `templates/cloudflare-workers/`, `templates/bun-ecs/` | Selected TS-related/runtime overlays. |
| `templates/go/`, `templates/python/`, `templates/bash/` | Language tooling, examples and command contracts. |
| [Scoped review roles](docs/review-roles.md) | Writer/reviewer/owner boundaries; no fixed model mandate or new privileges. |
| `.github/workflows/`, `scratch/fixtures/`, `.gitleaks.toml` | Existing security and selected deliberate-violation checks; coverage/diagnostic limitations remain visible. |
| [Decisions](docs/adr/0002-quality-first-acceptance.md), [rebuild state](HANDOFF.md) | Migration rationale, reviewed progress and actual remaining work. |

## Adoption boundary

Select an owner-approved source revision and relevant units. Propose how `templates/AGENTS.md`, `templates/SYSTEM_MAP.md` and `docs/quality-contract.md` fit the target's existing instructions. Merge a chosen overlay only after applicable compatibility/security verification; project commands must actually exist. Never overwrite local rules, secret settings, workflows or package-manager contracts blindly. Record adopted source facts separately from approval and execution evidence.

Global skill installation, hosted protection, publication and live consumer enrollment require their existing authority. The kit itself grants none. It works free-tooling-first without asserting all free and paid tools have identical capabilities.

## Current verification status

The rebuild clears units independently; see [current handoff](HANDOFF.md) and its candidate-bound acceptance records for accepted units and remaining gates. A reviewed core or one overlay does not establish compatibility/enforcement for the rest. No complete-kit release, automatic updater, tracker registry or publisher is claimed.

Existing required TS contexts historically succeeded while substantive steps skipped; Python/Go/Bash fixture successes do not prove every advertised gate or complete project behavior. Known inherited fixture and npm/pnpm mismatches are assigned to later gates. See [C0 baseline](docs/planning/c0-gate-baseline.md) and [current handoff](HANDOFF.md), not old phase badges, for evidence and limits.

The historical Codex/model-specific guides retain earlier receipts behind explicit historical notices; they are not routine bootstrap or current policies. [ADR-0002](docs/adr/0002-quality-first-acceptance.md) records what the approved migration supersedes; ADR-0001 is unchanged history.

## License

[MPL-2.0](LICENSE), with file-level copyleft obligations when covered files are modified and redistributed. Preserve applicable notices; do not replace a consumer's existing license wholesale.
