# Architecture, data-flow and debloat review — draft

Date: 2026-10-08. Drafted by Bee for Christopher.
**Planning only:** not adopted policy, a new workflow service, implementation authority or a requirement to map every function. Christopher clarified that nodes mean **code components and data flows**, not agent orchestration stages.

## Purpose

Review whether the design makes the requested behavior understandable, verifiable and economical to maintain. Identify bloat and suggest a smaller implementation doing the same job, without code-golf, lost guarantees or extra procedural machinery.

This extends Q4/Q5/Q6 in `code-quality-acceptance-contract-draft-2026-10-08.md`. It does not replace behavioral acceptance or authorize refactors.

## 1. Begin with a small design map during the initial coding session

For new modules, material architectural changes or behavior crossing components/trust/state boundaries, capture the relevant intended flow before implementation. Map only the task slice and the dependencies necessary to understand it—not the whole repository. For a small fix in an existing mapped flow, reference/update that slice; no fresh architecture document or diagram ritual is necessary.

The initial map records:
- Requested behavior and relevant invariants.
- Existing components to reuse and new responsibilities genuinely required.
- Inputs, transformations, state reads/writes, outputs and material failure routes.
- Trust/authorization boundaries and ownership of state.
- Unresolved assumptions and applicable verification.

This is a design baseline, not proof. Discoveries during coding may improve it. Preserve why a material route/ownership change was made; update ordinary details without repeated permission requests. Material changes to approved behavior/risk/architecture still need clarification under current rules.

## 2. Wise node structure: responsibility and ownership, not more objects

A node describes a real component with a coherent job: function/module, existing service, store, external system or significant boundary. Use the project's natural granularity. Do not add a class, interface, file or adapter merely to satisfy the map.

For each meaningful node, record concisely:

| Field | What it establishes |
|---|---|
| ID / responsibility | What job this component actually does; real source location when available. |
| Input -> output | Shape/meaning and important invariants, not an exhaustive field dump. |
| State / effects | What it reads/writes/calls and who owns mutations; say 'none' for pure logic. |
| Boundary / failure | Where untrusted data becomes accepted; authorization and failure handling as applicable. |
| Evidence | Design-only, traced in source, exercised by named test/runtime evidence, or unknown. |

An edge says which node passes which data/control to which other node, under what important condition. Label crossings such as HTTP input, event/queue, store access or external API when that changes guarantees. Include ordering, cancellation/retry/lifetime or transaction assumptions only when they affect correctness. Feedback loops/events may be legitimate; do not force every system into a DAG or universal layer scheme.

Prefer explicit domain contracts and state ownership. Avoid raw untrusted payloads silently circulating, multiple competing versions of the same rule, unexplained globals and hidden side effects. Similar shapes do not necessarily mean the same contract; necessary adapters and transformations are not bloat by default.

## 3. Example: cancellation flow

Illustrative design, NOT the architecture of either consumer:

```text
request + trusted actor identity
    -> parse cancellation command
    -> check actor permission and current order state
    -> perform permitted cancellation
    -> persist outcome
    -> return safe result

invalid input / denied permission / invalid state
    -> safe rejection, no cancellation write

persistence failure
    -> explicit failure, no false success
```

Review questions:
- Where does trusted actor identity come from? Can a client supply it instead?
- Is permission checked for the actual target/state, including relevant concurrent changes?
- Which component owns the state transition and persistence? Is atomicity needed for this contract?
- Do rejection/failure paths preserve the right state and report an honest outcome?
- Which tests observe those outcomes rather than merely confirming functions were called?

Pure quote/formatting behavior may need no store or transaction at all. Do not copy this flow into unrelated tasks as a skeleton requirement.

## 4. Review the implementation against the baseline

The reviewer independently traces the affected code, callers and side effects; the author's map is a lead, not authority. Use real symbols/paths and available test/runtime evidence. Classify a route as source-traced versus actually exercised; a diagram or typecheck is not runtime proof.

Compare intended versus implemented flows:
1. **Topology:** required routes exist; unexpected dependencies/side effects are explained; failure/recovery routes are not omitted.
2. **Contracts:** values retain the intended meaning across edges; conversions/defaults/validation are visible; caller assumptions match callee guarantees.
3. **Ownership:** state writes, mutation ordering and resource lifetime are clear; competing writers/cycles are safe or justified.
4. **Boundaries:** parsing, authorization, escaping/SQL/command/path handling occur where needed; validation is not mistaken for permission.
5. **Economy:** does each node/transformation contribute a real guarantee or job? Are we passing through redundant representations or layers?
6. **Proof:** behavior tests cover relevant paths and preserved invariants; unknown or unexercised paths remain labeled.

A mismatch may expose a defect OR a better design. Do not force code back to a mistaken initial diagram. Explain the difference, verify the intended behavior and update the accepted map when appropriate.

For dynamic dispatch, event systems or generated integrations, static search may be insufficient. Record unknown reachability and use targeted evidence where warranted. 'No grep matches' does not prove dead code.

## 5. Debloat: smaller implementation, same or better guarantees

Inspect for:
- Repeated business calculations/validation/serialization that should have one semantic owner.
- Wrappers, factories, interfaces or forwarding layers without an actual boundary, alternate implementation or useful contract.
- Unused branches/helpers/config knobs/dependencies—after checking dynamic/external callers and compatibility.
- Repeated conversions, copied state and unnecessary data movement.
- Oversized mixed responsibilities, excessive tiny-file fragmentation and indirection that makes one job harder to follow.
- Dead comments, obsolete scaffolding and history embedded in source.
- Tests duplicated without added behavior coverage; mocks concealing the behavior being tested.

Do not confuse necessary protocol adapters, clear domain types, error context, observability or valuable tests with bloat. Inline/remove only where the result stays easier to reason about. Keep shared behavior shared; keep genuinely different business guarantees separate.

Each suggestion includes:
```text
Finding: concrete node/edge/source location and unnecessary cost.
Proposal: smallest removal/consolidation/restructure; no unrelated cleanup.
Preserve: behavior/API/state/security/error guarantees that must not change.
Evidence: callers/uses inspected and uncertainty; tests/checks needed before acceptance.
Impact: expected source-line/character and complexity/navigation change; unmeasured if not calculated.
Risk: compatibility/dynamic callers/state/timing concerns; why this is worth doing.
```

Prioritize correctness/unsafe flow first, then high-confidence maintenance reduction, then optional polish. Suggestions are not automatic edits. Apply an approved coherent change/hypothesis at a time; verify preservation before proceeding.

## 6. Measure reduction without rewarding obfuscation

For a proposed/applied debloat, compare the full affected file set, including added replacement helpers. Use the same formatting/count convention on both sides. Report production source lines/characters separately from test/documentation counts; moving code into another file or deleting tests is not a demonstrated improvement.

Counts can be simple physical lines and Unicode character totals, with the convention stated. Exclude generated/vendor/lock output from the hand-written source comparison without deleting or ignoring its compatibility/security obligations. No quota, weighted 'slop score' or custom measurement service is required.

Expected estimates must be labeled; actual reductions require measured before/after snapshots. Consider fewer responsibilities/representations/navigation hops and better ownership alongside counts. Reducing lines while increasing mental complexity fails the contract. Sometimes clearer, safer code grows; show the benefit rather than squeezing it to meet a target.

## 7. Minimal review output

One compact finding list for the relevant slice:
- Architecture/data-flow defects and design mismatches, with source/behavior evidence.
- Debloat candidates ordered by expected value and preservation risk.
- Material unknowns and the smallest additional verification needed.
- No-change verdict when the current design is already sufficient.

A tiny existing fix may need only a short flow statement and one finding or no finding. A cross-boundary change may need the node/edge table plus tests. No separate mandatory agent, approval gate, huge report or whole-repo audit is implied. Focused independent review uses the project's adopted review process; this draft does not alter delegation/merge authority.

Keep a reviewed current slice with project design docs when it will help future work; retain significant prior rationale in history. Do not put a duplicated whole-system map into every prompt or pretend manually maintained maps cannot drift. Initial intent, current source-traced flow and test evidence remain distinguishable.

## 8. Acceptance exercise before adoption

Not run yet. Review representative diffs/maps containing:
- A coherent direct flow: accept without inventing extra layers.
- An unexpected store/network effect: identify the edge and its behavior/security consequence.
- A forwarding framework with no actual purpose: propose a smaller implementation and preserving tests.
- Two similar routines with different guarantees: avoid unsafe consolidation.
- A 'dead' callback referenced dynamically: preserve it or disclose unresolved reachability.
- A line-reducing but unreadable rewrite: reject the optimization.
- A better implementation than the initial map: update the design, not enforce the stale diagram.

Passing means concrete flow/ownership defects are found, useful architecture is preserved, debloat suggestions have verifiable preservation plans and routine work gains little overhead. No implementation, diagram engine, runtime tracing system or special node framework is authorized here.
