# C2 — pre-recorded exercise expectations

Owner: Bee. Date: 2026-10-08. Recorded before publishing the method and before independent review. Reviewer must not read this until its independent judgments are returned. These are expected judgments, not executed product results.

| Case | Expected classification | Concrete basis / preservation requirement |
|---|---|---|
| R03 | Needs change | Forwarding layers lack supplied responsibility/alternate implementation. Simplify to existing CSV library/writer; preserve encoding/escaping/output contract and relevant tests. Do not claim measured reduction without snapshots. |
| R05 | Meets exercise contract | Adapter owns real protocol conversion/validation. Preserve authenticated ingress, required-field checks, supported scale and forward-compatible metadata. Extra node alone is not bloat. |
| R09 | Needs change | More compressed, harder-to-read control flow without benefit. Retain clear pure calculation and the same behavior tests; do not invent a ledger-write defect. |
| R10 | Needs change | Omitted external analytics edge discloses private data outside the approved route. Remove it, trace actual effects/callers and verify the authorized-only flow; updating a map alone cannot approve the risk. |
| R11 | Needs change | Boolean branching combines distinct business/state guarantees without useful shared policy. Preserve separate charge/refund operations and their contract/state tests; reuse the existing low-level writer. |
| R12 | Needs change — deletion | Registry lookup reaches handler; direct-call grep cannot justify deletion. Preserve entry/handler and observe supported event/state behavior under real verification before any future change. |
| R13 | Meets exercise contract | Simpler actual validation/pricing route preserves requirement and supplied evidence. Update intended/current map and rationale; don't recreate forwarding scaffolding to match stale intent. |
| E01 | Unverified | Only intent is supplied. Relabel design arrows as intent; independently trace source and obtain candidate-bound authorization/failure/state tests. Missing proof is not an observed implementation defect. |
| E02 | Needs change — measurement claim | Both snapshots total12physical lines/300Unicode code points. Entrypoint-only two-thirds claim omits the replacement helper. No demonstrated reduction, clarity improvement or behavior proof; relocation may still be justified separately. |
| E03 | Needs change | Before:1physical line/5Unicode code points/6UTF-8bytes including LF. After:1line/5code points/5bytes. Byte reduction is not character reduction and changes the required accented string. Preserve exact semantics; no normalization or tests deleted to manufacture savings. |
| S01 | Source-traced with inherited boundary gap; runtime unverified | Script loads library (strict settings, IFS/ERR trap), main takes CLI value, require_positive_int calls require_arg then digit regex, echo writes stdout or helper exits on invalid shape/empty. Echo is not listener startup. Regex admits0, violating positivity; written Bats checks omit zero rejection. No real test execution observed. C4 must exercise positive/zero/negative/malformed/empty inputs and applicable success/rejection outputs without pretending source trace is runtime proof. |

Pass means material judgments are supported, useful complexity/architecture is preserved and evidence/counting claims are honest. Investigate material disagreements against source/contract; never alter expectations simply to manufacture agreement. Optional wording preferences are not blockers.
