# Advisor findings: autonomy and authority for the coding-standards rebuild

**Prepared:** 2026-10-08 — Bee, on-machine, at Christopher's request
**Input:** `docs/planning/ordinary-task-authority-advisor-prompt-2026-10-08.md` (canonical repo verified at commit `93ee82a` at answer time)
**Status:** A recommendation for Christopher to accept, amend, or reject. Nothing here is adopted policy, a live permission change, or a claim that any proposed gate exists, was tested, or was configured. No tools installed, no consumers touched, no agents contacted, nothing committed or pushed.

---

## 1. Direct recommendation

Adopt a **bounded-corridor default**. For an ordinary approved task, the approval is one task grant covering the entire mechanical chain up to a **draft PR**:

> branch/worktree → in-scope code/test edits → builds/tests/lints → stage authorized changes only → local commits → push to the grant's named remote and branch namespace → draft PR.

Two gates remain **human-only, always**: marking a PR ready for review, and merge/deploy/irreversible actions.

Why this shape:

- The ladder is not binary. A verified patch, local commit, push, and PR differ in reversibility and external surface; the default must be graduated, not all-or-nothing.
- **Local commit is default-included.** It is local and reversible. Commit-time hooks execute project-controlled code — but the agent already executes project-controlled code whenever it builds or tests, so a commit adds a small event surface, not a new trust class. Per-commit human approval adds latency without adding safety.
- **Push and draft PR are conditionally included.** They add real external surface: credentials, network, CI/workflow triggers, external artifacts. Containment does not come from trusting the agent; it comes from four conditions: (a) the grant names the exact remote and branch namespace, (b) the remote is on a Christopher-maintained allowlist, (c) the namespace is non-default and non-protected (`agents/<task-slug>`), and (d) remote-side branch protection and required checks are verified present. Pushing early is what lets CI and review machinery run *before* human attention is spent; the draft PR carries scope, evidence, and an explicit not-verified list instead of a readiness claim.
- **Human attention concentrates where it changes outcomes:** the readiness claim (what other humans will trust) and the merge (what the repo and production receive). Everything before those points is mechanical execution of already-approved scope.

Limits and conditions required for adoption:

1. Explicit adoption by Christopher, including a **reviewed superseding note** for current doctrine ("human owner approves pushes", "Builder is the sole git authority") — a policy update, never silent drift. The stale single-vendor/relay role topology gets the same reviewed update.
2. Corridor activation is **per-remote**, gated on verifying remote-side protections (branch protection on default branches, required status checks, no self-merge from agent namespaces). These are currently unverified on the canonical repo and both consumers. Until verified for a given remote, the default degrades to: stop at verified local commit for that remote.
3. The corridor is **opt-in per grant**, not ambient. If the task grant omits the push/PR fields, or the repo is not pre-cleared, agents stop at a verified local commit and report.
4. Standing rules are unchanged and non-waivable in ordinary grants: no force-push, no `--no-verify`, no email, no committing known-broken code (one opt-in diagnostic exception below).

## 2. Authority matrix

| # | Action | Actor / permission | Prerequisite evidence | Stop / escalate trigger |
|---|--------|--------------------|-----------------------|--------------------------|
| 1 | Create/select branch or isolated worktree | Task agent, ordinary grant | Repo + scope declared; live state inspected | Dirty tree, unexpected user changes, or collision with a live path → stop, report |
| 2 | Modify code and tests | Task agent | Scope contract within declared blast radius | Touches a protected path or outside declared radius → stop |
| 3 | Run builds/tests/hooks/lints | Task agent | Toolchain known to the grant | Missing toolchain, or work of the excluded class (dependency/build/hook-script changes) → escalate |
| 4 | Stage changes | Task agent | Staged set = task files only | Foreign changes present → unstage own files only, report |
| 5 | Local commit | Task agent | Gates green, or failures reported to operator | Any failing gate → no commit without explicit operator OK; never `--no-verify` |
| 6 | Push | Task agent | Grant names remote + namespace; commit evidence recorded | Remote/namespace not in grant, credential prompt, or unexpected remote state → stop |
| 7 | Open/update draft PR | Task agent | Push done; PR body carries scope + evidence + not-verified list | Repo not pre-cleared or its CI/workflows unverified → stop |
| 8 | Mark ready for review | **Christopher only** | Evidence summary presented by agent | Agents never self-mark; an agent reviewer is input, never acceptance |
| 9 | Address reviewer/CI feedback | Task agent | Same grant | Feedback expands scope or hits the excluded class → new grant |
| 10 | Change test expectations, scanner exceptions, receipts, gates, hooks, checks, policy | **Excluded from ordinary grants** | n/a | Attempt within an ordinary task → stop, escalate to elevated grant |
| 11 | Merge | **Christopher only** | Review evidence | Never delegated by default |
| 12 | Deploy / irreversible / external data migration | **Christopher only** | n/a | Never |

**Granted once per task:** steps 1–7. **Always a new human action:** steps 8, 11, 12. **Always a separate grant class:** step 10. Step 9 is covered while feedback stays within the approved scope.

**Grant lifetime:** void on completion, explicit revocation, or any change in scope, risk, actor, or state (discovered pre-existing user changes, missing remote protections, unrecoverable gate failure). A re-grant is cheap: restate scope plus the changed condition — no long-prompt rewrite, so token burn stays low.

## 3. Small task-authorization contract (illustrative future-policy draft)

```
id:          <slug>
approver:    Christopher
writer:      <agent identity>
repo:        <repo> @ <remote>
namespace:   agents/<slug>
contract:    <concrete behavior/acceptance criteria: what is true when done>
scope:       <files/modules/paths; declared blast radius>
risk_class:  ordinary | <escalation reason>
chain:       commit: yes | push: yes | draft_pr: yes | draft_pr_on_red: no (default)
lifetime:    task completion | explicit revocation | state/scope/risk/actor change
evidence:    ran | passed | failed-or-unavailable | not-verified
exclusions:  <reference to standing list; not restated>
```

Standing exclusions (inherited by every ordinary grant, never restated at length): row-10 items, merge/deploy/irreversible, new credentials or scopes, cross-repo actions, external writes, email, another owner's files without handoff, and any readiness claim. The contract stays 10–15 lines by referencing that list.

## 4. Enforcement sketch

**Advisory (explicitly not relied upon):** `AGENTS.md` doctrine; the grant file itself (auditable, but agent-readable); all local hooks. Per the supplied Claude hook docs, ordinary command-hook timeouts do not block the tool call and post-action hooks cannot prevent a completed action — and local hooks are bypassable in practice. Local hooks are UX, not enforcement.

**Mechanical (real enforcement, to verify or configure before relying on it):**

- **Remote:** branch protection on default branches, required status checks, and prevention of self-merge from agent namespaces. Unverified on the canonical repo and both consumers today. The corridor does not activate for a remote until this is inspected (read-only settings check, needs Christopher's authorization).
- **Path-based human review** for authority surfaces: a CODEOWNERS-style rule putting receipts, scanner allowlists, gates, checks, and workflow files under mandatory human review, so an ordinary-grant PR mechanically cannot merge those paths on its own. Unverified whether configured anywhere.
- **Receipts split into two fields:** agent-writable *evidence* (what, when, fingerprints) and human-only *acceptance* (a field only Christopher or a token he controls can write). Until mechanically split, acceptance is policy-labeled. An agent editing a SHA advances evidence, never approval.
- **Read-only checker** (per the agreed tracking-first order) verifies presence and shape of evidence — never authority, never approval.

**What remains unverified:** hosted protections on all repos; effective installed hook behavior versus documentation; actual Pi parent/child permission arbitration settings; OS/network/credential confinement; token scopes on this host; CI coverage beyond the selected Python/Go/Bash fixtures.

## 5. Prioritized additional decisions

**Blockers — settle before drafting the spec:**

1. **Pre-cleared remote/namespace allowlist.** Recommended default: canonical standards repo plus TheWarRoom and TFM Playbook, `agents/<task-slug>` namespaces, draft PRs only. Tighter option: canonical-only at first. Looser changes little mechanically but widens blast radius across owners.
2. **Confirm human-only ready-for-review and merge.** Recommended default: yes. If Christopher ever wants delegated merging, that is a fleet-level durable decision requiring ClaudeBox context and expert review — not part of this rebuild.
3. **Elevated-risk class definition** (row-10 items plus policy/tracker/updater changes). Default: separate grant type, Christopher's approval, independent review — where an agent reviewer is input and human acceptance is the event.
4. **Done-evidence format.** Default: ran / passed / failed-or-unavailable / not-verified. Cheap, honest, token-light; unknown is never success.

**Deferrable — settle conservatively during design, do not ask Christopher:**

- Multi-agent mechanics: one writer per seam/worktree; reviewers read and comment only; integration by forward-merge inside one's own namespace; collisions → stop, report, human arbitrates.
- Receipt schema fields (design step).
- Containment for untrusted execution (dependency/build/hook-script class): deferred; ordinary tasks already run project code under today's accepted trust model, but the elevated class needs a verified container/VM plan before any such grant exists.
- Evaluation cadence: risk-scaled; no universal five-run or full-mutation mandates for routine mechanical tasks.
- Recovery mechanics detail: inspect postconditions before retry (local log/status, remote refs, PR list), idempotent retries, rollback by forward-fix or deleting one's own namespace branch only — never force-push, never delete user work.

**Genuine operator ambiguity — Christopher's call, provisional defaults given:**

- **Personal latency at push/draft-PR on pre-cleared repos.** Default: corridor included. Alternative: stop-at-commit, which trades interruptions for tighter visibility. This materially changes his attention budget, so it is his to set.
- **Draft-PR-on-red as a diagnostic tool.** Default: opt-in grant flag, `no` by default — this keeps "never commit broken code" intact. If allowed: the push/PR title and body must carry the failing/unknown status and must never contain readiness language.

## 6. Exact first planning step and no-go conditions

**First step:** Christopher accepts or amends the corridor (one decision, one variable). Then produce, in the canonical repo under `docs/planning/`, a short `authority-model` draft capturing: risk classes, the §3 grant contract, standing exclusions, escalation triggers, the evidence format, and the §4 enforcement boundaries with their unverified list. A planning artifact only — no code, no consumer contact. Then proceed in the already-proposed order: schema/ownership → read-only synthetic-fixture checker → owner-reviewed enrollment proposals → safe update plans → separately approved managed-file application → coordinated rollout.

**No-go conditions:**

- Remote-side protections verified absent → corridor degrades to stop-at-commit for that remote until fixed.
- Consumer owners not consented → no enrollment or pilot on their repos.
- Any fleet-level effect → ClaudeBox and expert review required first (not contacted now).
- Any gate/expectation/scanner edit needed to make work pass → escalation, never performed in-task.
- No implementation before adoption; standing guardrails hold regardless of adoption.

## 7. Uncertainties and contradictions

- **Remote protections are the load-bearing unknown.** The corridor's containment premise rests on branch protection and required checks that have not been verified to exist. This is the single most important read-only verification before activation.
- **A draft PR is not side-effect-free:** `pull_request` workflows, notifications, and metadata exposure still occur; the draft state reduces signaling risk, not the event surface.
- **Commit hooks inherit the agent's environment.** Same trust class as test execution, but credential exposure through hook environments is unexamined — flagged here, not solved.
- **Doctrine contradiction is real:** current canonical prose says the human owner approves pushes and one Builder holds git authority. The corridor supersedes that by design; it must be a reviewed policy update, or the corpus says one thing while practice does another.
- **Receipt self-certification:** any SHA an agent records is evidence, not approval. Only the human-only acceptance field changes trust state.
- **Hook semantics** are taken from the supplied documentation (timeouts non-blocking for ordinary command hooks; post-action hooks cannot prevent completed actions); installed-version behavior is unverified, so local hooks stay advisory. The Pi child-permission arbitration described in the inspected docs (unknown tools defaulting to allow) is documented for that subsystem only — it is not evidence of fleet-wide confinement.
- **Sources are scoped:** the context study and verify-before-retry paper are controlled-setting findings used directionally here. No universal failure percentages, model-brand claims, or invented product features or deployed configurations appear in this recommendation.

---

**Provenance:** authored by Bee on 2026-10-08 from the self-contained advisor prompt only; repo verified at `93ee82a` (clean tree except pre-existing untracked `.project.yaml` and `docs/planning/`). Local research passes (`~/scratch/coding-standards-rebuild-research-pass.md`, `coding-standards-overlay-audit.md`, `coding-standards-update-mechanism-investigation.md`) were not re-read for this answer. This file lives in `~/scratch/`, is untracked, and commits to nothing.
