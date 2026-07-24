# Local Model Guidance (Layer 11)

**Purpose:** Layer 11 of the guardrail stack governs how a *local* model earns a role in the pipeline — what it's trusted to do, what it's never trusted to do, and how that assignment gets re-checked. This doc is written to survive a hardware upgrade or a model swap without a rewrite: the **principles are permanent, the current fleet is a dated example**, not the spec. Never let a specific model name calcify into the rule.

**Why this is its own layer:** small local models fail differently than frontier models. They don't just get things wrong — they hallucinate specs about *themselves* (context window, parameter count, tool-calling support) as readily as they hallucinate application code. Layer 11 exists so a session doesn't inherit last year's floor numbers as gospel, and doesn't quietly let a small model self-certify work only a frontier model should merge.

---

## 1. The weight-agnostic teammate principle

A local model is a teammate, not a lesser Claude. Assign role by what each tier is actually good at, not by a vibe of "small = worse":

- **Small/local model** → high-recall first pass: draft scaffolds, flag candidate issues, surface signal + explicit uncertainty ("I'm not sure X is right, check it"). Optimize for *not missing things*, not for polish.
- **Frontier model (Claude/GLM 5.2)** → judgment: triage the small model's leads against source, decide what's real, own the merge. Teaches specificity back rather than just grading pass/fail.

Full doctrine: `local-model-teammate-doctrine` (memory + `plans/local-model-teammate-doctrine.md` on the ClaudeBox side). The rule that matters here: **a small model's output is a lead, never a finding, and never self-certified.** Same shape as the Codex's M13 (second vantage, not an oracle) and M18 (audits return leads, never write) — Layer 11 is that discipline applied specifically to the small-model tier.

## 2. The selection checklist — run this before trusting a model, not once

Before assigning any local model a role in the pipeline (or re-confirming an existing one after a hardware/model change), verify these against the model's **primary-source spec sheet**, not folklore, not a prior session's memory, not what "everyone knows" about that model family:

1. **Context window** — the actual documented figure for the exact quantization/build in use, not the base model's marketing number.
2. **Tool-calling / structured-output support** — does it reliably call tools or emit valid structured output at the quant level actually deployed, or only at full precision?
3. **Quantization floor** — the point past which quality degrades below usable for the task class assigned. Test it, don't assume it from a smaller/larger sibling model.
4. **Task-class fit** — chat/draft-shaped work tolerates more slop than structured code generation; code generation tolerates less than a first-pass audit lead. Match the role to the model's actual reliability at that class, not its reliability in general.

**Why re-verify instead of trust the last answer:** a real floor claim ("this model breaks past 8k context") was carried in memory and later found to be flatly false against the model's actual published spec (`lesson_small_model_floor_claims_expire`) — small-model capability claims expire the same way application specs do, and the fix is the same discipline this whole repo already applies to code: verify against the primary source before trusting the config.

## 3. Delivery mechanism — the Lite Codex, model-agnostic by design

`docs/agent-codex-lite.md` is Layer 11's existing delivery vehicle: the full 18-motif Codex compressed to one-line laws + slop-catalog headlines for a context budget too small to hold the full doc. It's already written model-agnostically — swap which model receives it without touching the doc. Any new local model that earns a coding role gets the Lite Codex, not a shrunk-down improvisation; if a future model's context can hold the full Codex, load that instead (see the Codex's own guidance: template-setting work always gets the full version regardless of model size).

## 4. Dual-model architecture pattern

The durable shape, independent of which models fill the roles:

```
Small/local model(s)  →  high-recall pass, flags candidates, states uncertainty
                       →  (never merges, never self-certifies)
Frontier model         →  triage against source, judgment call, owns the merge
```

This is the same Build → Review → Triage shape as Codex M13, applied specifically to local-vs-frontier pairing. It holds whether the small tier is one model or several, and whether "frontier" is Claude or GLM 5.2 acting as reviewer.

---

## Today's snapshot — dated, not the spec

**As of 2026-07-24**, on the Beelink EQR6 AI Command Center (`project_beelink_ai_build`):

| Model | Role | Notes |
|---|---|---|
| Ornith (9B) | Local coding fallback for Hermes; first-pass review drafting | Gets the Lite Codex |
| Gemma E4B | Lighter local tier | Boot-gating: NONE of the foundation docs load for Gemma E4B sessions (too small a budget even for the Lite Codex header) — see `feedback_beelink_boot_gating` |

This table is a snapshot, not a commitment. **Re-run the Section 2 checklist whenever:**
- the Beelink (or any node) gets new/upgraded hardware,
- a model in the fleet is swapped or requantized,
- a new local node joins the fleet.

Do not carry this table's numbers forward into a new hardware generation without re-verifying them — that's exactly the failure mode Section 2 exists to prevent.

---

*Layer 11 in the 11-layer stack (`CLAUDE.md`). Routed in `docs/INDEX.md`. Companion docs: `docs/agent-codex-lite.md` (delivery), `docs/agent-codex.md` (the full Codex M13/M18 this pattern extends).*
