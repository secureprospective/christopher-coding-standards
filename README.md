<div align="center">

# christopher-coding-standards

### Stop the slop.

**Engineering standards that turn AI-generated code from "I hope this works"
into something a human — or a different model, in a different session — can
pick up cold and trust.**

[![Security](https://github.com/secureprospective/christopher-coding-standards/actions/workflows/security.yml/badge.svg)](https://github.com/secureprospective/christopher-coding-standards/actions/workflows/security.yml)
![Phase](https://img.shields.io/badge/Go%20overlay-live-success)
![Enforcement](https://img.shields.io/badge/enforcement-compile--time-blueviolet)
![Model Agnostic](https://img.shields.io/badge/models-Claude%20%7C%20Gemini%20%7C%20local-9cf)
![Zero Trust](https://img.shields.io/badge/AI%20output-zero%20trust-critical)
![License](https://img.shields.io/badge/license-MPL--2.0-blue)

**Starting a session here? → Read [`docs/INDEX.md`](docs/INDEX.md) first.**
It routes you to only the files your task needs, instead of this whole repo.

</div>

---

## Contents

- [The problem](#the-problem)
- [The core move: don't warn — *forbid*](#the-core-move-dont-warn--forbid)
- [Proof the gates actually bite](#proof-the-gates-actually-bite)
- [Two models, measured — not a theory](#two-models-measured--not-a-theory)
- [How it fits together](#how-it-fits-together)
- [What's actually in here](#whats-actually-in-here)
- [Design principles](#design-principles)
- [The eleven-layer guardrail stack](#the-eleven-layer-guardrail-stack)
- [How to adopt in a new or existing repo](#how-to-adopt-in-a-new-or-existing-repo)
- [Phase status](#phase-status)

---

## The problem

LLMs write fine code *inside* a single context window. They fall apart *across*
sessions and *across* agents — a new session, or a different model picking up
another's work, with nothing forcing it to stay coherent. The result is **AI
slop**: inconsistent patterns, duplicated logic, code that only made sense to
the model that wrote it, in the hour it wrote it.

So we don't ask models to behave. We build an environment where the wrong thing
**can't happen** — and where every AI output is treated as **unverified
third-party code** until it passes the layered gates below. No model — frontier
or local, Claude or Gemini — is trusted to self-police.

> Models bring **unlimited leverage** — scale, speed, throughput no human can
> match. Humans bring **revelation** — judgment, values, and the "should we"
> that no benchmark answers. This repo exists to marry the two: machine leverage
> applied inside a structure that always leaves room for human revelation to act.

### The numbers

- **Veracode 2025 GenAI Code Security Report** (100+ LLMs across Java,
  JavaScript, Python, C#): AI-generated code contains **2.74× more
  vulnerabilities** than human-written code. 45% of samples carry an OWASP Top
  10 issue.
- **AppSec Santa, 2026**: **1 in 4** AI-generated code samples contain a
  confirmed OWASP vulnerability.
- **Apiiro, Fortune 50 analysis**: CVSS 7.0+ vulnerabilities appear **2.5× more
  often** in AI-generated code.
- **GitHub-scale CWE study**: the top dangerous CWEs in AI-generated code are
  SQL Injection (CWE-89), OS Command Injection (CWE-78), Code Injection
  (CWE-94), and hard-coded credentials (CWE-259/798).

Full citations: [`docs/adr/0001-why-this-standard-exists.md`](docs/adr/0001-why-this-standard-exists.md).

## The core move: don't warn — *forbid*

A linter warning is a suggestion a tired model can ignore at 2 a.m. The
standard this repo holds itself to is stronger: **make the wrong program refuse
to exist.** Where the type system or the build can carry a rule, we put it
there — so the violation isn't a red squiggle, it's a compile error, and the
code never ships because it never builds.

The Go overlay is where this gets vivid. One invariant: a player ID must always
flow through its validating constructor (MFL IDs under 1000 need leading zeros —
`"0099"`, never `"99"`; skip that and records silently stop matching). A linter
*could* try to flag the bypass. Instead:

```go
type PlayerID struct{ id string }   // unexported field

playerid.New("99")        // ✅ validates, normalizes → "0099"
playerid.PlayerID("99")   // ❌ does not compile — you can't build a struct from a string
```

The bypass isn't discouraged. It's **impossible to compile.** That's the bar:
turn a social contract into a law of physics wherever the language lets you.

## Proof the gates actually bite

We don't *claim* enforcement — we **attack our own rules** with deliberate
violations and watch them fail the build. Every gate in the Go overlay, fired
on purpose:

| Deliberate violation | What stops it | Outcome |
|---|---|---|
| `playerid.PlayerID("99")` — skip validation | struct-wrap (unexported field) | **won't compile** |
| `interface{}` / `any` in an exported signature | **`ifaceguard`** — a `go/analysis` vettool we *wrote*, because no off-the-shelf linter catches this | `go vet` fails |
| `internal/ingestion` imports `internal/engine` (cross-layer) | `depguard` rules encoding the three-layer architecture law | **build error** |
| a 600-line source file | `filelen` gate | `make lint` fails |
| `fmt.Sprintf`-built SQL / hard-coded AWS key | `gosec` + `gitleaks` | blocked at commit |

And here's the part most "standards" skip: **we test the testers.** Two gates
that *looked* perfectly correct silently passed everything —

- a `depguard` file-glob missing a `**/` prefix matched **zero files**, so the
  entire three-layer architecture law was decorative — it threw no error and
  caught nothing;
- a `filelen` check built on `find -exec ... exit 1` printed the violation and
  then exited `0`, because `find` doesn't propagate an `-exec` exit code.

Both were invisible until we fired a real violation at them. So the rule is now
doctrine: **a gate is not real until a deliberate violation has been seen to
fail it.** Every overlay ships with that verification test baked in.

## Two models, measured — not a theory

The multi-agent design isn't an org chart on a slide. It's **Build → Review →
Triage**, run on real code, with numbers:

- A **Builder** (Claude Code) writes; a second, differently-trained **Recon/Audit**
  agent (the Antigravity CLI) reviews from its own vantage. On a real transport
  client, that review caught **two genuine logic bugs the linters had no way to
  see** — invisible to tooling, visible to a second model reading for what the
  code *does*.
- But a second model is not an oracle: a confident, line-specific,
  *"blocking"*-severity finding can still be a **hallucination** (measured rate:
  1 in 8). So every concrete finding is **checked against the actual source
  before it's acted on** — the triage step. With the protocol in place, the next
  review pass landed **zero** false findings.
- Neither model is trusted to self-police, and a **human owns every merge.**
  Builder holds sole git authority; the auditor never commits and never edits
  living docs; the human resolves the calls a benchmark can't.

That's the whole thesis in one loop: leverage from the machines, the final word
from the human, and a paper trail proving it works rather than asserting it.

## How it fits together

```
                       ┌─────────────────────────┐
                       │   docs/INDEX.md          │   ← every session starts here
                       │   "what do I need?"      │
                       └────────────┬─────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                             ▼                             ▼
┌───────────────┐           ┌─────────────────┐          ┌──────────────────┐
│  BUILDER agent │           │ RECON/AUDIT agent│          │   HUMAN OWNER     │
│  (Claude Code) │◄─────────►│ (Antigravity CLI)│          │  (the soul)       │
│                │  cross-    │                  │          │                  │
│ • writes code  │ pollinate  │ • repo recon     │          │ • approves merges│
│ • sole git     │  (relayed) │ • audits, drafts │          │ • resolves        │
│   authority    │           │ • never commits  │          │   disagreements   │
│ • living docs  │           │ • never edits    │          │ • sets direction  │
└───────┬────────┘           │   living docs    │          └──────────────────┘
        │                     └──────────────────┘
        ▼
┌─────────────────────────────────────────────────────────────┐
│  Eleven-layer guardrail stack (advisory → deterministic CI)   │
│  AGENTS.md → permissions → SYSTEM_MAP.md → schemas → lint →   │
│  pre-commit → SAST/SCA/secrets → tests → sandboxing → ADRs →  │
│  local-model gates                                            │
└─────────────────────────────────────────────────────────────┘
```

Full role split, escalation, and task routing: [`docs/multi-agent-roles.md`](docs/multi-agent-roles.md).

## What's actually in here

| | |
|---|---|
| **Eleven-layer guardrail stack** | From advisory `AGENTS.md` instructions down to CI-enforced SAST/SCA/secrets scanning — table below |
| **Compile-time enforcement** | Where the language allows, rules become build errors, not warnings — the struct-wrap idiom, the three-layer architecture law as `depguard` rules |
| **A custom analyzer we built** | `ifaceguard` (`templates/go/tools/ifaceguard/`) — a `go/analysis` vettool that catches `interface{}`/`any` escapes no stock linter flags; pinned, `analysistest`-covered, `//ifaceguard:allow` escape hatch |
| **Multi-agent governance** | A binding role split between a Builder agent (deep reasoning, sole git authority) and Recon/Audit agents (large context, throughput) — `docs/multi-agent-roles.md` |
| **Cross-pollination + triage** | Structured, logged second-opinion audits between agents, with a triage protocol because confident findings still need source-checking — `docs/cross-pollination-log.md` |
| **Task-routing index** | `docs/INDEX.md` — load only what your task needs, not the whole repo |
| **Skills** | `adopt-coding-standards` (one command to onboard a new repo), `github-pr` (read-side GitHub API helper for environments without `gh`) |
| **Language overlays** | `templates/typescript/` (Biome, Zod, Stryker, Vitest) · `templates/astro/` (Prettier + `prettier-plugin-astro`, `astro check`) · `templates/cloudflare-workers/` (Wrangler, workerd Vitest pool, typed bindings, secrets-not-in-vars rule) · `templates/go/` (golangci-lint v2, struct-wrap idiom, `ifaceguard`, `filelen`, pinned pre-commit) |

## Design principles

1. **Forbid over warn.** If the type system or the build can carry a rule, it goes there. A warning is optional; a compile error is not.
2. **Model-agnostic.** Same gates apply whether code comes from Claude Code, frontier models, or local LLMs.
3. **Deterministic where possible.** Hooks and CI gates over prose instructions.
4. **Prove it, don't assert it.** Every gate is verified by a deliberate violation that must fail. A silent gate is worse than no gate.
5. **Free-tooling-first.** Works without paid SaaS.
6. **Canonical & replicable.** This repo is the single source of truth; other repos copy from here, on any hardware.

## The eleven-layer guardrail stack

| Layer | Mechanism | Artifact in this repo |
|---|---|---|
| 1 | Agent instruction (advisory) | `AGENTS.md` |
| 2 | Claude Code permissions | `.claude/settings.json` |
| 3 | System map (anti-drift) | `SYSTEM_MAP.md` (template) |
| 4 | Schema-driven boundaries | language overlays (`templates/*`) |
| 5 | Formatter + linter | language overlays |
| 6 | Pre-commit hooks | language overlays (SHA-pinned) |
| 7 | Security scanning (SAST + SCA + secrets) | `.gitleaks.toml`, `.github/workflows/security.yml` |
| 8 | Test discipline | branch protection + language overlays |
| 9 | Execution sandboxing | OS-level (operator concern, documented separately) |
| 10 | Refactoring discipline | `AGENTS.md` + ADR pattern |
| 11 | Local model selection | quantization floor, dual-model architecture (Phase 3) |

## How to adopt in a new or existing repo

Run the `adopt-coding-standards` skill ([`skills/adopt-coding-standards/SKILL.md`](skills/adopt-coding-standards/SKILL.md))
from a Claude Code session in the target repo — it walks through all of the
following:

1. Copy `AGENTS.md` to repo root. Customize the per-project section (project name, languages, public exposure, stack-specific commands).
2. Copy `.claude/settings.json` to repo `.claude/` directory.
3. Copy `SYSTEM_MAP.md` template to repo root and fill in directory invariants and existing utilities.
4. Copy `.gitleaks.toml` to repo root.
5. Copy `.github/workflows/security.yml` to repo `.github/workflows/`.
6. Enable branch protection per `docs/branch-protection.md`.
7. Copy the overlay for your stack from `templates/` (`typescript/`, `astro/`, `cloudflare-workers/`, or `go/`) and follow its `README.md`. Then **run its deliberate-violation test** — confirm every gate fails before you trust it.
8. If more than one AI agent works this codebase, copy `docs/multi-agent-roles.md` and `docs/cross-pollination-log.md` (reset to just its format section).

## Phase status

- ✅ Phase 1A–1B — repo skeleton + language-agnostic templates
- ✅ Phase 1C — TypeScript overlay (`templates/typescript/`)
- ✅ Phase 1D — Astro overlay (`templates/astro/`)
- ✅ Cloudflare Workers overlay (`templates/cloudflare-workers/`) — extends the TS overlay: Wrangler config, workerd Vitest pool, `wrangler types` bindings, bindings-as-capability-grants + secrets-never-in-`vars` discipline
- ✅ Multi-agent governance — role allocation, cross-pollination + triage protocol, task-routing index
- ✅ **Go overlay** (`templates/go/`) — golangci-lint v2, the struct-wrap compile-time idiom, the custom `ifaceguard` vettool, the `filelen` gate, SHA-pinned pre-commit; **proven by deliberate-violation tests**
- ⏳ Phase 2 (cont.) — Python and Bash overlays
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc

## License

[MPL-2.0](LICENSE) — Mozilla Public License 2.0. Permissive enough to drop these
templates into any project (including proprietary ones), with a file-level
copyleft: if you modify one of these files and redistribute it, those changes
stay open under MPL-2.0 too. The goal is for improvements to flow back into the
standard, not to restrict who can use it.

## Sources

The empirical claims in this README and in
[`docs/adr/0001-why-this-standard-exists.md`](docs/adr/0001-why-this-standard-exists.md)
are sourced. See that ADR for full citations.
