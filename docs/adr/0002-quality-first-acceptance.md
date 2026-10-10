# ADR-0002 — quality-first acceptance and scoped context

Date: 2026-10-08. Owner: Christopher. Implementation writer: Bee.
Status: **Core decision/content review cleared**, implementing Christopher's approved quality-first rebuild and chunk plan; [acceptance record](../planning/c1-acceptance-result.md). Final status verification precedes the local checkpoint. This is not consumer enrollment, a fleet role reassignment, a complete-kit release or new operational authority.

## Context

The original kit mixes copy/customize templates with maintainer instructions. Root project/map placeholders, mandatory full Codex loads, blanket size/DRY/dependency/architecture prescriptions and dated vendor-role mappings obscure the real acceptance objective. C0 source inspection also established that configured/green/skipped checks cannot be equated with behavior or effective containment.

Christopher's direction is settled: no slop; elegant, human-readable, maintainable code; freedom in implementation, rigor in acceptance. He approved the rebuild after compaction, then the per-chunk independent review plan: **“excellence is the standard, not the goal.”**

## Decision

1. Make `docs/quality-contract.md` the compact shared acceptance contract: behavior, simplicity, readability, maintainability, safety and evidence. Project/stack rules specialize real needs; do not weaken applicable configured gates silently.
2. Separate root kit-maintainer AGENTS/SYSTEM_MAP from consumer starting points under `templates/`. Adoption proposes selected source/revision/artifacts and preserves local rules; it never copies the kit's identity/map into an application or blindly installs legacy security/configuration.
3. Route only needed context through `docs/INDEX.md`. Historical Codex/model guides retain original bodies behind explicit historical banners, not routine instructions or current capability/permission claims. No universal full-document/model-specific bootstrap.
4. Retain canonical/model-agnostic/free-tooling-first/replicable aims. Machine checks are preferred for failures they actually detect; prove changed gates with clean/intended violating cases and correct diagnostics. Review settles intent, ownership, readability and needless complexity that machines cannot prove.
5. Permit concise useful design context and initial task flow slices, compared independently with actual source/evidence. No universal architecture/layer/DAG/newtype/size/mutation/unknown-field rules. Legitimate constants, adapters and necessary complexity remain valid.
6. Ordinary in-scope implementation/test/feedback does not need repeated approval. Material scope/behavior/risk/architecture/authority changes do. This is not an autonomous publication corridor, hook bypass or permission to rewrite other-agent workspaces.

## Relation to ADR-0001 and legacy guidance

ADR-0001 remains unedited as history. For the accepted core/routing slice, this decision supersedes its blanket architecture-context exclusion, mandatory Spec Kit question (tool use becomes project/operator-selected), universal hook/enforcement claims and vendor-file symlink expectation (runtime filenames/loading must be verified). Model-agnostic shared guidance, free-tooling-first distribution, narrow permissions and immutable third-party action/hook refs remain.

The superseding contract replaces conflicting universal prescriptions in the historical Codex/full-lite/model-role guides, including guaranteed purity/security/capability claims, always-on race/mutation/newtype requirements and fixed size/duplication/dependency heuristics. Their historical receipts/benchmarks are not current verified facts. Research cannot justify universal model-security or workflow rules from conditional studies; corrected research is retained in planning evidence, not every prompt.

## Consequences and limits

Default reads are smaller and source ownership/routing is explicit, but diagrams/receipts/prose still cannot authenticate approval or prove runtime behavior. C0 scenarios are calibration examples, not a model reliability benchmark. C1 validates document routing and review; full runtime overlay/CI acceptance belongs to later chunks. Remaining template conflicts are disclosed, not silently waived.

No consumer, hosted setting, runtime permissions, CI workflow, credential, dependency or language gate changes in C1. No publication/version/release claim. Fleet-wide governance and unapproved durable architecture decisions still need the operator's existing escalation process.

Evidence: [approved map](../planning/rebuild-at-a-glance-2026-10-08.md), [C0 acceptance](../planning/c0-acceptance-result.md), [approved chunk plan](../planning/rebuild-chunk-plan-2026-10-08.md). The decision's implementation must itself clear that plan's verification/review gates.
