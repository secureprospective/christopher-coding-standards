# C1 — core contract and routing slice

Owner: Bee. Base: C0 checkpoint `1ea1a0e`; branch `rebuild/quality-core-2026-10-08`.

## Result and preserved guarantees

One compact shared quality contract; distinct kit-maintenance versus copied consumer instructions/maps; scoped routing; explicit migration rationale. Keep safety, useful tests, model-agnostic operation, free-tooling-first portability and existing publication/ownership constraints. No promise that configuration proves enforcement.

Initial responsibility flow:

```text
kit maintainer → root AGENTS + docs/INDEX → shared quality contract + named source slice
consumer adoption proposal → templates/AGENTS + templates/SYSTEM_MAP + shared contract
    → customized project instructions/map → actual project checks and review evidence
historical Codex/model profiles → marked historical, not routine instructions or permission
```

The shared contract owns acceptance principles. Project guidance owns actual commands, local constraints and state/flow knowledge. Selected overlays own language/config particulars; they remain unchanged and unverified in this chunk. Adoption instructions identify a source/revision and propose exact replacements, rather than copying the maintainer's profile or overwriting consumers.

Allowed source changes: root AGENTS/SYSTEM_MAP/README; docs/INDEX; new quality contract, portable review-role guidance and ADR-0002; status banners only on five historical Codex/model guides; new consumer instruction/map templates; adoption skill documentation. Planning/result metadata is separate. All are this shared kit's project artifacts; no other-agent workspace/identity/config file is touched.

Protected: ADR-0001 body, existing language/runtime templates, fixtures, workflows, secret/vendor permission configuration, global skill installation, live consumers, hosted settings, credentials and unrelated `.project.yaml`. No files/repos moved; no new top-level directory.

## Gates

1. Verify allowed diff, Markdown structure and local links; preserved legacy bodies byte-identical after status banner.
2. Assemble a disposable **Markdown-only** consumer document set; customize its profile/map; verify required routing resolves without kit-only or phantom paths. No application/tool/runtime test is claimed.
3. Reconcile active-read-set bytes/words against C0; report measured counts, not actual token savings or quotas.
4. Freeze source files/diff and baseline identity. Fresh read-only reviewer checks actual maintained entrypoints, migration/authority boundaries and all16 C0 scenario judgments under the new contract, without reading the oracle or previous case verdicts.
5. Resolve concrete defects; rerun affected checks/review. No C1 acceptance until both verification and independent review clear.

Status: implementation candidate in progress. Consumer enrollment and execution remain unauthorized; runtime overlays/CI belong to later chunks.
