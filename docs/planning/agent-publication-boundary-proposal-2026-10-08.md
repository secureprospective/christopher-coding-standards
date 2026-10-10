# Agent publication and human acceptance boundary — proposal

Date: 2026-10-08. Author: Bee. Status: planning only, not adopted policy or permission to register an App, mint tokens, configure rules, create a test repository, migrate credentials or activate a corridor.

## Recommended architecture

Use a repo-selected GitHub App installation identity, with App keys and installation tokens held by a small deterministic publisher outside agent execution. Christopher keeps his human identity/control-plane authority in a separate environment. A approved task grant permits the publisher to validate and publish an exact candidate only to a named agents/<slug> branch and open/update its draft PR. No merge, mark-ready, deploy, delete, force-push, policy change or arbitrary API/command interface exists in the ordinary publisher.

The agent workspace is isolated from Christopher's gh/git/SSH credentials, app keys/tokens and the publisher's configuration/state. A separate username is insufficient if the agent still has sudo, shared secret mounts, host shell tools or an exposed Docker/control socket. Baseline parent, child and external runners; processes/build/tests must share the intended boundary. Do not move/revoke existing fleet credentials casually or disrupt another agent.

Flow:

agent workspace -> exact task-approved candidate + evidence -> restricted publisher -> App-authenticated agents/<slug> branch + draft PR -> CI/review -> Christopher's separate human identity accepts and merges

This is one trusted non-LLM component, not another reasoning agent. Routine publication/checks require no model calls; implementation, secure operation and review are real costs and have not been benchmarked.

## App installation and permission candidate

Start with the canonical repo only, not both consumers. Register/install an independently acting GitHub App, not a token acting as Christopher. Exact registration/permissions require approval and verification.

Candidate permissions:
- Metadata read (normal App minimum).
- Contents read/write, for approved branch publication.
- Pull requests read/write, for draft PR creation/update.
- Actions read and/or checks read only if needed for observing CI.
- No administration, workflow write, checks/status write, secret/environment/deployment/package write or unrelated repositories.

Contents-write/PR-write can authorize more than the intended corridor; they do NOT alone enforce branch namespaces, draft-only behavior or human-only merge. Hence: token remains inside the restricted publisher, plus GitHub-side update/merge rules independently constrain the App. Do not claim a fine-grained permission flag makes PR-write draft-only.

App installation tokens expire after one hour and may be narrowed to selected repositories/permissions. The private App key remains outside the worker. Lifetime/scope limits reduce exposure but do not make a leaked token harmless.

## Deterministic publisher contract

Human-approved task grants live in a store the agent cannot edit. Repo/branch/scope/risk/actor/expiry are validated against it. An agent-generated grant/receipt cannot approve itself.

Allow only:
1. Observe current allowed repo/ref/CI state.
2. Publish the exact approved candidate to the task's existing/allowed namespace using ordinary non-forced updates.
3. Open/update a draft PR whose base/source/body are constructed from approved identifiers and observed evidence.

Refuse: wrong remote/base/namespace/actor, expired/revoked grant, missing/failed required pre-publication evidence, unexpected source state, foreign staged files, protected policy paths, workflow changes, destructive actions, arbitrary command/API payloads and authority expansion.

Candidate identity includes tested bytes/content/tree, source/base state and the commit being published; an untrusted message 'tests passed' is not sufficient evidence. Paths/config/Git helpers/hooks are untrusted: no command execution from candidate config, shell strings, external diff/filter helpers or publisher-owned code changes. Details need threat review and tests, not an assumed safe git wrapper.

On timeout/error: inspect remote ref and existing task PR before retry. Retry identity is the same logical operation; avoid duplicate PRs/side effects. A failed or unknown check is never rewritten as pass. Legitimate remote-only checks run after publication; report 'candidate awaiting CI', not fully verified. Do not publish known-broken code under an ordinary diagnostic exception; current standing rules remain.

## GitHub-side human acceptance

Layer controls rather than granting one blanket bypass:
- Retain/enhance a main quality ruleset/protection requiring PR integration, applicable meaningful checks, an independent approving review, stale-review dismissal/last-push review as appropriate and protected policy owners.
- Separately constrain who can update/merge main: Christopher's authorized human admin identity/role, not the App or ordinary write role. The App is not on the bypass list.
- Constrain branch creation/update/deletion outside agents/<single-slug> and tag/release operations as appropriate. Rules target patterns use GitHub fnmatch; agents/* does not match arbitrary nested slash names.
- Keep the human's narrowly needed bypass for an update-restriction rule distinct from bypass of test/review rules. Human admin can always change policy; that control-plane trust is explicitly retained, not eliminated.
- Protect .github/workflows/**, CODEOWNERS, standards policy/catalog/checker/updater, scanner exceptions and acceptance records with required human-owned review. CODEOWNERS alone is not enforcement.

GitHub docs support restrict-creation/update/deletion rules and role/App bypass selections. Exact personal-repository behavior, role mappings and merge interactions must be verified with a disposable pilot; do not assert the planned App/rules combination is proven on our repo.

At least one review is meaningful for App-authored PRs because Christopher is a distinct actor. Christopher cannot approve his own human-authored PR; define another authorized reviewer or separately governed break-glass maintenance rather than locking out human maintenance or silently weakening reviews. Existing open human-authored PRs need transition review before settings change.

Human-only 'ready' is enforced by the publisher lacking that operation and withholding the PR-write token, not by GitHub permission scopes alone. Actual human-only integration also needs server-side main update controls. Do not depend merely on agent obedience.

## Receipts/evidence

Agent observation records may be generated within scope and remain untrusted claims until independently checked. Accepted rule adoption is recorded through protected human-reviewed integration or a separately authenticated approval record binding exact source and candidate. Do not call a field human-only just because its name says so; Git cannot prevent edits to one field in an otherwise writable document. Freshness, provenance, configuration and executed evidence stay separate.

## CI changes needed from completed audit

Current canonical settings do not meet this design: approving review count0, owner admin credential available through current session, no mandatory policy owner, green-but-skipped required TS checks, actual Python/Go/Bash fixture jobs not required, mutable action references, broad security-events permission and scanner exclusions.

Replace required-context no-ops with actual applicable fixture/gate proof; prevent policy/check weakening from self-certifying. Restrict CI token/secret exposure, especially candidate source execution. Branch protection does not contain PR jobs; draft PRs still execute workflows/emit notifications. Rebuild/workflow/updater changes are elevated-risk work, NOT ordinary corridor work.

## Acceptance fixtures before activation (not run)

- Valid approved candidate -> only named branch and draft PR; no unexpected operation.
- App requests update/merge of main -> denied, even when checks are green.
- Agent calls mark-ready/merge/arbitrary API via publisher -> denied.
- Agent tries other branch/remote, tag, workflow/policy path, deletion or forced update -> denied.
- Worker attempts human credential/private key/token/control-state reads -> denied through actual subprocess paths; approved publisher endpoint still works.
- Agent changes receipt or grant locally -> no acceptance/authority advancement.
- Human reviews App PR with actual gates -> allowed approved merge; human bypass of update restriction does not bypass independent quality rules.
- Missing check, no-op check, failed check, unrelated tool error, changed candidate after testing -> not accepted as passing evidence.
- Ambiguous publication timeout -> state verified and no duplicate PR/nonforced loss.
- Token expiration/revocation and publisher unavailable -> stop safely; no fallback to owner credentials.

## First step / escalation

First prepare a reviewed canonical-only authority design: permission/operation matrix, protected surfaces, exact rule interaction, candidate/evidence binding, worker/broker boundary, transition/rollback and test plan. Christopher must approve deployment/actions; ClaudeBox context/expert review is required before durable fleet identity/registry architecture. Do not create a GitHub App or test repository without that authorization. Verify risky assumptions on an approved disposable repo before changing live main controls. Roll out one control at a time; no migration of existing human credentials or consumers in this proposal.

Sources checked October8:
- https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/deciding-when-to-build-a-github-app
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository

See `docs/planning/canonical-github-authority-audit-2026-10-08.md` for observed controls. This proposal contains no newly verified runtime protection.
