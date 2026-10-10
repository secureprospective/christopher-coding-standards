# C0 — expected exercise verdicts

Owner: Bee. Date: 2026-10-08. Recorded before independent review and before operational-standard changes. Keep this separate from the review input until independent verdicts are returned.

**Not runtime test results.** These expectations judge bounded synthetic scenarios in `c0-review-cases.md` under their stated premises. An exercise outcome does not prove the snippets compile, a feature runs or future reviews are reliable. Actual execution evidence remains required in executable chunks. Different wording is acceptable; materially different judgments need source/contract-based reconciliation, not forcing the reviewer to agree.

| Case | Expected verdict | Concrete basis / necessary correction |
|---|---|---|
| R01 | Meets exercise contract | Finite positive numbers are accepted; zero/negative/nonfinite rejected. Direct tests observe those outcomes, with successful execution supplied as a scenario premise. No unrelated work needed. |
| R02 | Needs change | Q1/Q5/Q6: actor ignored, write occurs without permission, and the tested function is itself mocked. Fix actual authorization before mutation; test the real public behavior, denial and unchanged order state. A mock rejection alone cannot establish any of that. |
| R03 | Needs change | Q2/Q4: forwarding factory/registry/abstract/interface layers have no current responsibility or real alternative. Preserve correct CSV escaping/encoding and the existing writer/library while removing unnecessary machinery. |
| R04 A | Meets exercise contract | Given source/test premises establish coherence for one decoder responsibility. A line count alone cannot require a split; this is not a claim that a real 640-line file was inspected here. |
| R04 B | Needs change | Q1/Q4/Q5: unsafe SQL construction, mixed unrelated effects, hidden state and false-success failure handling. Short length does not excuse defects. Fix the actual boundary/ownership/failure problems, not a numeric metric. |
| R05 | Meets exercise contract | Necessary protocol transformation has one owner; authentication and contract-specific required-field validation are distinct. Provider unknown metadata is intentionally allowed. Removing the adapter or universally rejecting extra fields loses the required guarantee. |
| R06 | Needs change | Q1/Q5/Q6: valid UUID input is not permission. Enforce owner authorization before deletion through the appropriate existing domain/state boundary; observe valid-but-unauthorized rejection and unchanged state. |
| R07 | Needs change | Q1/Q5/Q6: unavailability is made indistinguishable from a successful empty read. Preserve the meaningful failure result, safely translate at the external boundary, and test unavailable storage separately from empty data. |
| R08 | Meets exercise contract | Existing trim behavior and real-function assertions already satisfy the task; execution is a scenario premise. Accept evidenced no-change without duplicate tests or invented helpers. |
| R09 | Needs change | Q3/Q4: compact expression adds a throwing IIFE and compressed names/control flow without benefit. Preserve the clear adequate implementation. No fictional persistence defect or changed behavior is alleged. Counts cannot justify reduced readability. |
| R10 | Needs change | Q1/Q5: new unapproved external effect sends private data outside the agreed flow; CSV tests miss it. Remove that effect, trace the authorized route and verify no such disclosure. Do not silently approve it by redrawing the map. |
| R11 | Needs change | Q2/Q3/Q4: unrelated domain guarantees now depend on caller-selected boolean branches without a shared policy benefit. Preserve explicit charge/refund ownership and reuse the already-shared low-level writer. Similar syntax is insufficient reason for consolidation. |
| R12 | Needs change — deletion proposal | Q1/Q4/Q6: registry lookup reaches the handler, and scenario integration evidence observes its state outcome. Removing it breaks supported handling. Static absence of direct-call syntax is not dead-code proof. Existing route itself is supported by the stated evidence. |
| R13 | Meets exercise contract | Required validation/pricing behavior and evidence preserved with fewer unnecessary nodes. Current design/rationale updated. A mistaken initial topology is not authority to add adapters back. |
| R14 | Unverified | Q6: green skipped jobs establish no applicable lint/type/test execution; behavior/source evidence absent. Obtain actual matching-candidate checks; cannot invent an implementation defect from missing evidence or call it accepted. |
| R15 | Needs change | Q6/provenance: editable receipt/version/hash cannot establish owner approval, enforcement or passing checks. Report what the fingerprint comparison establishes and label approval/configuration/execution independently unknown unless supported. |

## Clear condition

Independent review must identify the real defects and preserve the valid/no-change/necessary-complexity cases for concrete reasons. Any material discrepancy is investigated and corrected or justified with evidence; merely matching this table is not proof of excellence. Baseline/source claims are reviewed separately against actual repository files. A source-proven invalid expectation must be corrected, not used to train agreement.

No verdicts from the independent reviewer have been received for this packet yet.
