# Code-quality acceptance contract — draft

Date: 2026-10-08. Owner: Christopher. Drafted by Bee.
**Planning proposal only.** Not adopted policy, new agent permissions, a superseding ADR, or a claim that these checks exist. Operational files and consumer projects remain unchanged.

## Purpose

Produce correct, elegant, human-readable code that remains understandable and safe to change after its original author/session is gone. Give agents freedom inside the approved task; constrain defective output, unnecessary complexity and unsafe behavior—not the number of procedural steps taken.

**No slop means:** no unnecessary machinery, misleading tests, hidden assumptions, unexplained behavior, unrelated churn or unsupported completion claims. This is an acceptance objective, not a guarantee a scanner can prove.

## The six acceptance rules

| ID | A change meets the contract when… | Reasons to request a change |
|---|---|---|
| Q1 — Behavior | It delivers the requested observable behavior, preserves relevant existing guarantees and handles material failure/edge cases. No-change is valid when the requested behavior already exists. | Wrong interpretation, partial implementation, accidental compatibility change, missing failure behavior. |
| Q2 — Simplicity | It uses the simplest sufficient design for today's requirement and the project's idioms/utilities. Abstractions, dependencies and optimizations solve identifiable needs. | Speculative framework, unnecessary indirection, duplicate business logic, dependency added for convenience without a useful tradeoff. |
| Q3 — Readability | Names express domain intent; control flow and state ownership are understandable; comments clarify non-obvious constraints. Public contracts are discoverable without the original prompt. | Clever compression, ambiguous flags, misleading names, unexplained side effects, ceremonial comments or review history embedded in code. |
| Q4 — Maintainability | Responsibilities, dependency directions, state ownership and data flows are coherent; shared behavior has an appropriate owner; relevant API/data/config changes and rationale are discoverable. | Splits made only for a size cap, unexplained flow/ownership changes, tangled responsibilities, changes requiring synchronized fixes in copies, brittle implementation-coupled tests. |
| Q5 — Safety | Trust boundaries enforce appropriate shape/domain/authorization rules; errors, resources and dependencies are handled deliberately. No secret leakage, unsafe external command/SQL construction or newly introduced unexplained risk. | Type-casting used as runtime validation, swallowed failures, unbounded work/retries, unsafe permissions, unreviewed dependency identity or failing applicable security checks. |
| Q6 — Evidence | Tests assert intended outcomes and material failure paths. Applicable checks actually ran on the candidate under review; skipped/unknown checks and residual limits are explicit. | Test theater, expectations weakened just to get green, green no-op jobs, results from different code, claims that compile success proves the feature. |

These apply to changed behavior and affected guarantees, not as a demand to repair every historic issue in every task. An inherited relevant failure is disclosed and assessed; it is not disguised, silently waived or used to excuse a newly introduced defect.

## Concrete good/bad examples

Examples are illustrative sketches, not production code or executed tests. They assume the behavior stated alongside them; established project APIs take precedence.

### 1. Tests verify the contract, not activity — Q1/Q6

Requirement: an unauthorized cancellation must fail and leave the order intact.

**Bad:**
```ts
await cancelOrder(orderId, anotherCustomer);
expect(true).toBe(true);
```

**Good:**
```ts
await expect(cancelOrder(orderId, anotherCustomer)).rejects.toThrow(Forbidden);
expect(await orders.getStatus(orderId)).toBe("confirmed");
```

The good test observes rejection AND preserved state. Add the authorized success case using the same public behavior. Do not mock cancellation itself to manufacture these results. Use the project's actual error representation, not a prescribed exception class.

### 2. Complete simple work without inventing a platform — Q2/Q4

Requirement: add CSV export using existing report data and file-writing facilities.

**Bad:** introduce ExportStrategyFactory, PluginRegistry, AbstractExporter and three interfaces for one export format with no actual extension requirement.

**Good:** add a focused CSV renderer, reuse the existing writer, and test escaping/encoding plus the export result. Use a mature CSV library if correct handling/maintenance warrants it; do not hand-roll a risky parser to avoid a dependency.

A stable plugin API or several real implementations could justify the abstraction later. Reject unsupported machinery, not useful architecture.

### 3. Split by responsibility, not a number — Q3/Q4

**Bad:** divide one coherent operation among ten tiny files solely to pass a line limit; the reader must navigate all ten to understand it.

**Good:** keep coherent behavior together; separate transport parsing, domain decisions or persistence when they have genuinely different responsibilities. A larger cohesive file may be acceptable; a short tangled one may not be.

Length/complexity/duplication reports can point reviewers toward problems. They do not define elegance or authorize automatic splitting. Enforced thresholds need project-specific calibration and an observed defect-prevention benefit.

### 4. Share the same rule, not merely similar syntax — Q2/Q4

**Bad:** copy the same eligibility calculation into an endpoint and a background job; a rule fix now needs two edits.

**Good:** both call the same eligibility function, with policy differences passed as explicit data when they truly share behavior.

**Also bad:** combine charging and refunding into one boolean-driven generic routine merely because their code looks alike. Different business guarantees may deserve separate operations. Prefer stable semantic ownership over blind DRY or automatic abstraction on the second similar block.

### 5. Boundary validation and authorization are distinct — Q1/Q5

**Bad:**
```ts
const command = request.body as AttackCommand;
executeAttack(command);
```

**Good:**
```ts
const command = attackSchema.parse(request.body);
authorizeAttack(currentPlayer, command);
executeAttack(command);
```

The schema implements the agreed input contract; authorization checks allowed behavior. Test valid input, malformed input and a structurally valid but unauthorized request. Type annotations/casts and valid UUIDs prove neither runtime safety nor ownership. Unknown-field behavior depends on the actual protocol; strict own-client schemas and forward-compatible provider schemas need not be identical.

### 6. Failure remains a failure — Q3/Q5

**Bad:** catch a failed report read and return an empty list; callers cannot distinguish no data from unavailable data.

**Good:** propagate the project's meaningful failure result with operational context; translate it into a safe external response at the appropriate boundary. Test the unavailable-data path. Recovery to an empty result is acceptable only when that is the explicitly intended contract.

Comments should explain constraints such as why a retry is unsafe—not narrate each assignment or name the model/reviewer who requested it. Real constants and immutable tables are fine; hidden mutable state and unexplained environmental assumptions are the problem.

## Architecture/data-flow review and suggestive debloat

For material architectural or cross-boundary work, capture a small intended data-flow slice in the initial coding session. Nodes represent real code components, responsibilities and state owners—not compulsory new classes/files. Record important input/output contracts, transformations, side effects and failure routes.

Review the actual source against that baseline, distinguishing design intent, source-traced routes and paths exercised by tests. Identify unexpected edges, ownership/contract mismatches and unnecessary layers/data movement. A better implementation may justify updating the map; a stale map is not authority.

Return prioritized debloat suggestions with concrete locations, the proposed simplification, guarantees to preserve, callers/risks and verification needed. Line/character reduction is supporting evidence, not a mandate to compress readable code or erase tests. No automatic refactor or mandatory separate review agent is implied.

Detailed method and examples: `architecture-dataflow-debloat-review-draft-2026-10-08.md`. A small fix can reuse its existing flow description; do not impose a new diagram/report ritual.

## Smallest useful enforcement

Choose an existing trusted check where it detects the actual failure. Do not add one tool per rule or pretend a machine can settle intent/readability.

| Mechanism | Use it for | Limit / focused review |
|---|---|---|
| Formatter + selected lint | Consistency and established defect-prone constructs | No subjective style battles or maximal rule sets; judge names/responsibility separately. |
| Compiler/type checker where applicable | Type/API mismatches and invariants the language can enforce | Does not validate external bytes or prove the requirement. Not every domain string requires a newtype. |
| Behavioral tests | Requested results, failure paths and affected regressions | Review the oracle and mocks. Existing adequate tests may suffice; do not add a duplicate test to satisfy a count. |
| Existing scoped security/dependency/secret checks | Relevant unsafe patterns, credentials and known supply-chain findings | Check applicability and exclusions; scanner findings need triage. No silent suppression; medium severity can still be consequential. |
| Focused diff review | Intent, simplicity, domain naming, shared ownership and maintainability | Findings cite concrete behavior/lines, explain the defect/cost and propose the smallest fix. AI findings are leads until verified. |
| Targeted stronger tests | Critical boundary/concurrency/math/data-loss risks or uncovered failure modes | Integration/property/fuzz/mutation/race/performance/accessibility checks only where relevant; not universal ceremony. |

When adopting or changing a mechanical gate, prove one clean case passes and the intended violating case fails with the expected diagnostic. A missing tool/config or arbitrary nonzero exit is not proof. This belongs to gate validation, not a repeated exercise in every coding task.

For existing canonical CI: required TypeScript contexts currently succeed while substantive steps skip; actual Python/Go/Bash fixture jobs are not required. The hosted audit documents this. This contract describes a target, not current enforcement.

## Acceptance and review without ritual

For an approved task, inspection, implementation, relevant test updates and ordinary in-scope feedback are normal work. Ask when a material ambiguity changes behavior, risk or scope—not for each permitted step. Current commit/push/merge authority and credential safeguards remain unchanged until separately adopted.

Review outcome:
- **Meets contract:** applicable behavior/checks observed and no material quality issue found.
- **Needs change:** concrete defect, unnecessary maintenance burden or safety issue identified.
- **Unverified:** a material check/behavior could not be established. Specify what is missing; do not relabel it passing.

A meaningful finding states the violated contract, evidence and expected failure/maintenance cost. Preferences unsupported by a project convention or material benefit are suggestions, not blockers. A reviewer need not propose a change merely to prove it reviewed the patch.

Test expectations may change to implement approved behavior. Weakening unrelated guarantees, skipping tests to conceal failures, disabling gates or changing acceptance/security policy needs explicit review outside routine fixes. No known-broken commit or hook bypass is authorized here.

Minimal completion evidence can be three lines, with links only when useful:
```text
Behavior: unauthorized cancellation rejected; order remains confirmed.
Verified: relevant behavior tests and applicable lint/typecheck passed on <candidate>.
Unverified: <specific material limit, or none within the stated checks>.
```

Support this with actual command/result or CI evidence bound to the tested candidate; 'none' never claims the absence of all possible bugs. Do not require bulky task reports or reproduce raw logs in prompts. Human acceptance and publication permissions are a separate authority seam—not proof of code quality.

## Explicit non-goals

No universal file-size cap, coverage score as proof, automatic abstraction on the second near-copy, fixed ~15-line dependency rule, 'everything must be configurable', total ban on globals/constants, universal test reruns/mutation, ADR for every small structural choice, or prohibition on all explanatory architecture context.

Document major compatibility/ownership/security decisions where future readers can find them. Add no new machinery solely to prove compliance with this document.

## Proposed validation before adoption

Use representative diffs rather than build a new service:
1. A small correct bug fix with meaningful regression evidence: accept without unrelated cleanup.
2. A green-test patch that mocks its own behavior or omits an assertion: request an oracle fix.
3. A functioning patch with an unnecessary framework/duplicated rule: request a simpler complete design.
4. A cohesive larger file and a short tangled one: judge responsibilities, not length.
5. A valid input with unauthorized action or swallowed failure: reject despite typecheck/coverage success.
6. Already-satisfied requested behavior: accept an evidenced no-change result.

Success: reviewer verdicts explain concrete quality differences, necessary complexity is not penalized, and routine work is not blocked by proxy metrics or additional approvals. These exercises have NOT been run. Use current/historical project diffs only with approved access; no consumer rewrites or large model evaluation is implied.

## Integration path

This candidate preserves useful existing Codex principles while narrowing absolute claims. Compare against actual stack enforcement and project idioms, resolve meaningful disagreements, and obtain Christopher's acceptance. Canonical instruction/ADR changes require a separate reviewed migration; this draft silently supersedes nothing.

After that: map the adopted contract to each overlay's smallest adequate gates, and make tracking record which rules/checks a consumer actually uses. Reconsider publication/registry infrastructure only when it earns its complexity and does not displace the quality goal.
