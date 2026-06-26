# GLM large-context auditor & front-end QA discipline

**Layer 10.5** — sits between *Refactoring discipline* (10) and *Local model selection* (11) in the eleven-layer stack. This is the doctrine for the **Recon/Audit agent**: a large-context model (GLM-class, ~1M-token window) that runs the code-review gate, whole-repo audits, de-slop / efficiency passes, troubleshooting review, and automated front-end QA.

> **As of 2026-06-26 GLM 5.2 is the sole Recon/Audit agent** — Antigravity/agy (Gemini) is RETIRED as reviewer (blind-review false-positive rate too high). Where this doc still reads "a *second*/third agent alongside agy," read GLM as *the* recon-class agent; agy references are historical.

It extends the second-vantage pattern (`agent-codex.md` §M13, now §M18) to *whole-tree scale* and to *running UIs*. Read `docs/multi-agent-roles.md` first — the role matrix, exclusions, and human-owner gate are binding here too.

## The agent and its one hard constraint

- **Class:** Recon/Audit (per `multi-agent-roles.md`) — large context, high throughput, weaker multi-step reasoning, **never commits**. A *second* recon-class agent alongside Antigravity/agy, specialized for breadth.
- **Current mapping:** GLM-5.2 via the Z.ai Coding Plan, driven by OpenCode on a dedicated worker node (CT-class laptop), itself driven by the Builder (Claude/CT105).
- **HARD CONSTRAINT — it is text-only.** GLM-5.2 cannot see images. It can *capture* a screenshot but cannot interpret it (proven live 2026-06-20; the Lite plan also denies Z.ai vision models). Any doctrine that assumes "the model looks at the page" is wrong. Front-end QA is therefore structural + deterministic, not perceptual (see below).

## The three jobs

1. **Whole-repo audit / de-slop / efficiency.** Hold the whole tree; hunt cross-cutting rot a diff-level review never sees because no single PR introduced it: duplicated logic, drifted patterns, dead boundaries, the §4 slop-catalog smells at scale.
2. **Troubleshooting review-gate.** Same procedure as the existing cross-pollination gate — a different machine, not a new ritual. Build → Review → Triage (§M13).
3. **Automated front-end QA** on a running UI (see two-lane model).

## Dispatch rules — which agent for which question

| Situation | Send to |
|---|---|
| Multi-step reasoning, security boundary, architecture, the fix itself | **Builder** (Claude) — never delegated |
| Narrow, well-specified recon on a code subtree | **GLM** (OpenCode/bird) — throughput on scoped recon |
| Whole-repo de-slop / efficiency / drift audit (breadth > depth) | **GLM** large-context auditor |
| Front-end QA of a running UI (structural + visual regression) | **GLM** + the QA harness |

When unsure, it goes to the Builder. No recon-class agent picks its own scope.

## Two-lane front-end QA (the only correct model on a text LLM)

- **Lane A — structural.** GLM drives a headless browser (Playwright MCP) and inspects the **DOM, computed styles, and accessibility tree**: semantics, ARIA, contrast math, heading outline, focus order, content/label mismatches. This is GLM's strength and is often *more* rigorous than eyeballing.
- **Lane B — deterministic visual regression.** Playwright captures a screenshot; **pixelmatch** (or `toHaveScreenshot`) diffs it against a stored baseline and emits a mismatch count. **No vision model.** GLM then *reasons over the diff metric* ("0.46% of pixels changed in the header region — confirm intended"), it does not *see* the image.
- **Semantic "does it look good / on-brand" judgment** needs a real vision model, which the Lite plan lacks. It is **explicitly deferred**, not silently skipped. Revisit only with a budgeted vision model.

## Triage protocol — scale multiplies hallucination, not just coverage

A large-context auditor returns *more* findings, not *more reliable* ones. Treat output as **leads, not findings** (the standing rule for agy applies identically to GLM):

- Every concrete `file:line` / URL / dependency / pricing claim is **verified against source** before it is acted on (§M13). Survivors are fixed; the rest are logged, not escalated.
- **Uniform HIGH confidence across a long list is itself a red flag.** A model that is equally sure of everything is sure of nothing.
- **Receipt (2026-06-20):** a GLM recon returned a tidy table of repos/URLs all marked HIGH; triage found most fabricated — invented repo owners, and a pricing claim that **contradicted a live API test we had just run**. The verified residue (deterministic visual-regression tooling) was the real value. This is §M13's failure rate, at scale.

## Audit verdict format (what GLM returns)

Each finding on its own line, triage-ready:

```
[SEVERITY hi/med/lo] AREA — finding — exact location (file:line or DOM selector/URL) — what the Builder must verify
```

Plus a one-line self-assessment of coverage. No prose essays; closed, checkable claims (§M17 self-contained relay). For front-end QA, Lane B appends the JSON diff record (`{mismatchedPixels, ratio, diffImage}`).

## De-slop pass — what it hunts

The §4 slop catalog, swept across the whole tree: `interface{}`/`any` at boundaries, stringly-typed IDs, swallowed errors, package-level mutable state, string-built SQL, hardcoded hosts/secrets, giant util files, comment-restating-code, "tests later", un-reviewed cloned patterns, and duplication (`dupl`-class). Output is a verdict list per the format above — **the Builder makes every change.**

## Authority & exclusions (binding, from `multi-agent-roles.md`)

- GLM **never** commits, pushes, merges, or edits living docs (`AGENTS.md`, `SYSTEM_MAP.md`, ADRs, project instruction files, memory).
- GLM **never** has final say on auth/crypto/secrets/external-input code.
- GLM **never** sets direction or expands scope. It returns leads through the Builder; the human owner owns the merge.
- The Builder re-verifies (lint/test/build) regardless of what GLM reports green.

## Verification

- A dispatched audit is not trusted until the Builder has triaged each finding against source and recorded the outcome (extend `docs/cross-pollination-log.md` with the auditor verdict).
- A front-end QA run is not trusted until Lane B's baseline diff and Lane A's structural log are both reviewed; a green visual diff ≠ a correct feature (§M3, functional verification).
