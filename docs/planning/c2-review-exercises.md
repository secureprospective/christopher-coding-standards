# C2 — architecture/data-flow/debloat review exercises

Owner: Bee. Date: 2026-10-08. Documentation-method calibration, not executable application tests or a model reliability benchmark.

Read the actual new method and shared quality contract, then evaluate these cases independently. Do not read `c2-review-oracle.md`, C0/C1 oracles or previous case verdicts. Synthetic cases take expressly stated premises as inputs; source tracing or a scenario's supplied test result is not an actual new runtime result. Findings must explain a real contract/maintenance cost and the smallest correction/preservation evidence.

## Existing synthetic slices

Use only the named case bodies in `c0-review-cases.md`. For each, return the relevant route/owner issue or useful architecture, a bounded debloat disposition and evidence/preservation limits—not merely a score.

| Case | Focus |
|---|---|
| R03 | Do forwarding factory/registry/interfaces contribute a current guarantee? Specify the smallest preserving simplification. |
| R05 | Does a protocol conversion/validation adapter have a real boundary job? Avoid deleting necessary transformations. |
| R09 | Can shorter expressions with harder control flow count as improvement? Do not invent persistence defects in pure code. |
| R10 | Independently expose the omitted external effect/trust crossing, rather than redraw intent to bless it. |
| R11 | Similar syntax versus different charge/refund state/authorization contracts. |
| R12 | Actual registry dispatch versus no direct-call grep; preserve dynamic reachability. |
| R13 | A better actual route than initial forwarding-map intent; preserve behavior and update rationale. |

Return `meets exercise contract`, `needs change`, or `unverified` and one concise concrete reason/preservation plan for each. No full-program/runtime assurance from bounded premises.

## E01 — map presented as runtime proof

Author supplies only an initial diagram: input → schema → permission → store → success, with three failure arrows. No actual source trace, calls/tests or runtime result is supplied. Every arrow is labelled `exercised`, and the author claims the authorization/failure behavior is verified.

Does that evidence support the labels/claim? Distinguish the useful intent from the missing implementation/runtime evidence; name the smallest needed verification without inventing an observed defect.

## E02 — reduction measured on the entrypoint alone

A proposal moves a pure helper from one file into another without changing its logic. Supplied like-for-like formatted counts are:

| Snapshot | Production file | Physical lines | Unicode code points including LF |
|---|---|---:|---:|
| Before | entry.ts | 12 | 300 |
| After | entry.ts | 4 | 100 |
| After | helper.ts (new) | 8 | 200 |

The author claims a two-thirds production-source reduction using only entry.ts. Tests/docs are unchanged. Supplied counts are scenario premises, not a measurement of actual kit files. No responsibility benefit or loss has been established beyond relocating the helper.

Evaluate the reduction claim using the complete affected production set. Do not conclude either that moving a helper is inherently bad or that unchanged counts establish behavioral preservation/clarity.

## E03 — smaller bytes, different job

Requirement: preserve the exact output string `café\n` (é is U+00E9). Before sample text is `café` followed by LF; after sample text is `cafe` followed by LF. Author counts UTF-8 bytes and calls the change fewer source characters with the same behavior. These are text-count samples, not executed programs.

State before/after physical line, Unicode-code-point and UTF-8-byte counts with the convention explicit. Does the claimed preserving optimization meet the requirement? Do not reward removed semantics as debloat.

## S01 — actual source trace, not a scenario execution record

Independently inspect these unchanged repository files:
- `templates/bash/scripts/example.sh`
- `templates/bash/lib/strict-mode.sh`
- `templates/bash/tests/example.bats`

Trace CLI input through loaded strict-mode/helper code to output/rejection, including process settings/trap changes relevant to the trace. Give actual symbols/paths, state/effects, shape/domain boundary and available evidence classification. Does the output wording prove a network listener starts? Does digit-only validation establish the helper's positive-integer contract? What relevant tests are written and what isn't observed?

Do not run Bash/Bats or fix anything. Identify any source-proven inherited gap and the smallest required C4 runtime verification. Runtime behavior and written-test execution remain unverified here; do not label them exercised because the files exist.

## Boundary

A clear exercise identifies unsafe/unnecessary routes, preserves meaningful adapters/ownership/dynamic callers, distinguishes intent/source/runtime evidence, and measures the whole affected source set without losing readability or guarantees. No automatic rewrites, source version-as-approval, fabricated callers, quota, DAG rule or forced project architecture.
