# Project map

Fill in verified project facts, not the standards kit's directory listing. Keep only context useful to current/future work; update relevant slices when they change. Mark stale/unknown sections explicitly. Do not invent utilities or infer behavior from a diagram.

## Components and reuse

| Actual path/symbol | Responsibility / callers | State or effects / owner |
|---|---|---|
| `[existing component]` | `[actual job and relevant reusable API]` | `[reads/writes/calls, or none]` |

## Relevant flows and boundaries

For material cross-component work, record the task slice: input/identity → parsing/domain/authorization → transformations/state effects → output; include meaningful failure routes. Use real component/source names, not new classes/layers invented for the diagram. Capture necessary protocol, ordering, lifetime or compatibility guarantees.

Label evidence as **intent**, **source-traced**, **exercised by named test/runtime evidence**, or **unknown**. Independently trace actual callers and dynamic/event routes where relevant. A better implementation may update initial intent; no grep caller is not dead-code proof.

## Configuration, integrations and verification

- Actual configuration source/owner: `[verified source; do not copy secret values]`
- External integration/approved trust boundary: `[existing client/path; or none/unknown]`
- Applicable checks and evidence location: `[real project commands/results; or missing/unverified]`
- Deliberate absences / uncertain reachability: `[facts that prevent mistaken reinvention]`

Small fixes reuse existing slices; no whole-system map or duplicated field inventory required. Keep rationale where readers can find it without loading every prior session.
