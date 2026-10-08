# Maintaining christopher-coding-standards

This is the public copy-and-customize standards **kit**, not an application or a consumer profile. Its artifacts are documentation and TypeScript/Go/Python/Bash/config templates. Christopher owns direction and acceptance; the assigned writer owns the approved slice.

## Read only the task slice

- [Quality contract](docs/quality-contract.md): shared acceptance standard for writing/reviewing changes.
- [Routing index](docs/INDEX.md): relevant overlays, adoption, review and decisions.
- [Actual kit map](SYSTEM_MAP.md): existing paths and ownership. Do not invent utilities/services.
- [Migration rationale](docs/adr/0002-quality-first-acceptance.md): new core versus historical guidance.

Historical Codex/model-role pages are not current instructions. Research/planning archives are evidence inputs, not policies or permissions. Operator/system instructions and existing safety/ownership/publication constraints remain controlling.

## Work and verification

Declare a coherent scope and preserved guarantees; work on a branch for experimental changes. Implement the simplest complete result and resolve normal in-scope feedback without another approval ritual. Escalate material behavior/scope/risk/architecture/authority changes. Preserve others' work; never stage unrelated metadata or edit another agent's workspace/identity files.

There is currently **no root Makefile, package manifest or installed repository pre-commit configuration**. Do not invent root lint/test commands. Documentation changes use structure/link/scope checks and relevant review exercises. Template runtime changes need the designated suitable test environment, real assembled fixtures and the selected overlay's actual commands; missing tools/environment leave the result unverified. Do not install/run product tooling on an unapproved host.

Changed enforcement must reject its intended violation for the correct reason as well as accept clean input. Record candidate-bound results; a green skipped job, configuration file or diagram is not proof. Do not bypass hooks, suppress failures or commit known-broken operational code. Never force-push.

Conventional commits include `[AI-assisted]` when applicable; describe affected artifacts and actual verification. A clean review grants no push/merge/deploy authority. Do not email without explicit permission.

## Distribution boundary

Consumers start from [templates/AGENTS.md](templates/AGENTS.md), [templates/SYSTEM_MAP.md](templates/SYSTEM_MAP.md) and the shared contract—not these maintainer files. Follow the [adoption proposal skill](skills/adopt-coding-standards/SKILL.md); do not overwrite customized projects, install global skills, alter hosted controls or enroll consumers without the relevant authority.

C1 core/routing cleared content review on the rebuild branch; see the [acceptance record](docs/planning/c1-acceptance-result.md). This is not a complete-kit release. Runtime overlays/CI remain legacy until their own gates clear; conflicting configured gates are assessed/migrated explicitly, never silently bypassed.
