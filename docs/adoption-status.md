# Adoption status — manual facts, not enrollment

Use the [adoption skill](../skills/adopt-coding-standards/SKILL.md) for an owner-authorized proposal or bounded merge. Current [handoff](../HANDOFF.md) gives accepted unit status; copying a whole branch does not release the complete kit.

**Tracking implementation is deferred.** No catalog, receipt schema, checker, registry or updater was selected/implemented in C11. Historical [tracking research](planning/evidence/tracking-investigation.md) is a proposal, not a deployment decision. See the [decision and missing inputs](planning/c11-tracking-decision.md). No live consumers were enrolled or inspected by this decision.

## A useful manual report

For an already authorized source/target, keep the adoption/update proposal short:

- Actual owner-selected source clone/revision and selected source artifacts; their known acceptance state. No assumed canonical machine path or latest-branch trust.
- Actual target/branch/ref and selected units; current local rules/manager/locks and preserved customizations. Unknown ownership stops proposed writes, not read-only status.
- Genuine recorded old source and actual customized baseline, if available. Missing history means **unknown**, not a guessed adoption date/version.
- Observed source changes/local edits and the smallest review-needed update proposal. A changed shared rule may affect several selected units; a history-only commit need not change any unit. Inspect exact relevant source sets, not branch age or a blind whole-repo fingerprint.
- Configured checks, candidate-bound actual execution, missing/skipped/failed operations, review and owner approval **separately**. A hash/editable record describes bytes, not provenance/authenticated permission or passed behavior.

This report can live with the owner's ordinary review evidence. It creates no new required receipt format, storage service or automatic task/enrollment API. Do not claim fleet coverage or complete adoption from a list of files. Logical projects/refs/worktrees can differ; do not flatten divergent states into one alleged version.

## Conservative update classification

| Observation | Honest status/action |
|---|---|
| Selected current source bytes equal the observed target artifact | Exact match **for those bytes**; not approval, behavior or complete adoption proof. |
| Known accepted old baseline/source differs from selected new source; target unchanged | Upstream change / review needed. Owner-authorized bounded proposal, not automatic overwrite. |
| Target has local edits or is a merged snippet/shared file | Customized / review needed. Preserve local rules; compare the actual old/new source and customization, not assume whole-target upstream ownership. |
| Some units have different genuine source baselines | Mixed bindings. Report each affected unit/ref; do not forge one uniform version. |
| Receipt/baseline/unit binding missing, source unavailable or history uncertain | Unknown/missing, not stale/compliant/approved by guess. No destructive update. |
| Source only changed session/history outside selected unit inputs | No observed unit-content change; other approval/verification/freshness may still be unknown. |
| Requested path/ownership/ref is ambiguous or unsafe | Stop that comparison/write and ask. Never execute commands loaded from a record or follow arbitrary destinations. |

These are manual reporting examples, not executed checker fixtures. No checker/path-containment/automatic merge safety is promised. A conflict-free text merge or exact match still needs real behavior/configuration review and actual applicable checks before acceptance.

## To authorize a future read-only checker

Christopher must select the source/approval identity, canonical unit-to-consumer mapping and its owner, managed versus shared/adapted boundaries, and how genuine per-unit/customized baselines are established. Scope offline observation and failure behavior before implementation; specify paths/symlink/ref/input constraints, preservation and real fixture evidence. Mutable records cannot approve themselves. Fleet/catalog/identity/registry authority decisions need the existing coordinator/expert review; a narrow local report grants no such authority.

Until then use bounded manual proposals and preserve custom rules. Deferral does not block otherwise-ready core/overlays or their actual tests; it also does not waive unknown tracking status. Push/merge/install/deploy/enrollment/global/hosted/fleet changes remain separate existing authority.
