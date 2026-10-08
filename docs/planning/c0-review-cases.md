# C0 — representative review cases

Owner: Bee. Date: 2026-10-08. Scope: acceptance-method exercises, not production implementations.

These are synthetic, deliberately bounded scenarios. Code blocks and execution records below are **scenario inputs, not programs/tests run in this repository**. They do not prove runtime behavior or reliable future model performance. For an exercise verdict, take explicitly stated premises as given; independently inspect the supplied code, assertions and contracts for contradictions. Separately disclose real-world verification limits. Do not treat a scenario's asserted green result as authority over its visible broken oracle.

Review each case under the six quality dimensions and the architecture/data-flow draft. Return `meets exercise contract`, `needs change`, or `unverified`, with a concrete reason and smallest necessary correction/evidence. No preference-only rewrite or finding quota. Do not read `c0-review-oracle.md` until independent case verdicts have been returned; Bee recorded it before review, separately from this input.

## R01 — small complete fix

Requirement: `validQuantity` accepts finite positive numbers, rejects zero/negative/nonfinite numbers. No unrelated cleanup.

```ts
// Before
export const validQuantity = (n: number) => n >= 0;
// Candidate
export const validQuantity = (n: number) => Number.isFinite(n) && n > 0;
// Candidate tests call the real function, not a stub.
expect(validQuantity(2)).toBe(true);
expect(validQuantity(0.5)).toBe(true);
for (const n of [0, -1, NaN, Infinity, -Infinity]) {
  expect(validQuantity(n)).toBe(false);
}
```

Scenario evidence: these tests and applicable type/lint checks executed successfully on this candidate; unrelated existing tests remain successful. No public contract beyond the stated one changes.

## R02 — green oracle hiding broken behavior

Requirement: a denied cancellation rejects and leaves the order confirmed. Existing storage and identity APIs are unchanged.

```ts
// cancel.ts — production
export async function cancelOrder(orderId: string, actor: Actor) {
  await orders.setStatus(orderId, "cancelled"); // actor is ignored
}
```

```ts
// cancel.test.ts — imports are hoisted/mocked by the test runner
vi.mock("./cancel", () => ({ cancelOrder: vi.fn() }));
import { cancelOrder } from "./cancel";
it("rejects another customer's cancellation", async () => {
  vi.mocked(cancelOrder).mockRejectedValue(new Forbidden());
  await expect(cancelOrder("A", otherCustomer)).rejects.toThrow(Forbidden);
});
```

Scenario evidence: the test runner reports green because the test replaces the very behavior under judgment. No other authorization/state-preservation test exists. Judge the production body and oracle, not the reported test color.

## R03 — unnecessary export platform

Requirement: export one existing report to CSV. The project already has a correct CSV library and a file writer; no extension/plugin requirement exists.

Candidate introduces `ExportStrategyFactory → PluginRegistry → AbstractExporter → CsvExporter → CsvLibrary → ExistingWriter`, three forwarding interfaces and configuration for other formats. Only CsvExporter is implemented. Output escaping/encoding tests observe correct CSV bytes.

Supplied responsibility trace: factory selects the only exporter; registry only holds it; abstract class supplies no shared behavior; interfaces forward unchanged arguments. Neither transport isolation nor alternate implementations need those layers. Judge whether functional success settles acceptance, and suggest only a behavior-preserving correction.

## R04 — cohesive larger unit versus tangled short unit

Requirement: review responsibility and ownership, not enforce a source-line quota.

Scenario A: a 640-line generated-protocol-independent handwritten decoder owns one documented wire format. Its constant field table and named parsing helpers implement that one responsibility; parsing errors are explicit, it has no I/O/state mutation, and real round-trip/malformed-input tests cover the specified protocol. Source inspection in the scenario establishes those facts. The size is a supplied count, not a measured claim about a file in this kit.

Scenario B: a 45-line handler concatenates SQL from request bytes, updates shared mutable state, calls an unrelated notification API and suppresses all failures as successful empty results. No boundary/authorization/failure tests exist.

Must either be accepted/rejected solely for its length? Give separate outcomes and reasons. Do not demand a split or validate the decoder's whole real-world correctness from this exercise alone.

## R05 — necessary adapter

Requirement: accept a provider's forward-compatible webhook containing money in minor units; domain logic uses major units. Provider metadata fields must remain allowed. Authentication of the webhook is already enforced and exercised at ingress.

Candidate validates required provider fields, converts minor to major units in one named adapter, and passes a domain command to the existing domain function. Tests observe signature rejection, malformed required fields, allowed unknown metadata and exact conversion for the supported currency scale. Scenario evidence: all ran on the candidate. The protocol adapter is the only conversion owner.

Would deleting the adapter because it is an extra node improve this requirement? Judge the supplied guarantees rather than imposing universally strict unknown-field rejection.

## R06 — valid input without permission

Requirement: only the owner may delete a document. A UUID is not ownership. `trustedActor` comes from the authenticated session; storage deletion checks no permission itself.

```ts
const command = deleteSchema.parse(request.body);
await documents.remove(command.documentId);
```

Scenario tests cover valid/invalid UUIDs and successful deletion; all green. There is no actor/owner check or unauthorized state-preservation test. Explain the material failure and where evidence is missing.

## R07 — swallowed unavailable-data failure

Requirement: empty means a successfully read empty report. Storage unavailability must be a distinguishable failure, translated into a safe external error.

```ts
async function readReport() {
  try { return await storage.readReport(); }
  catch { return []; }
}
```

Scenario tests verify empty and nonempty successful reads only. Candidate claims robust graceful recovery. Would the claim satisfy the stated failure contract?

## R08 — evidenced no-change

Task: ensure `renderLabel` trims surrounding whitespace while preserving internal spaces. Current code:

```ts
export function renderLabel(value: string) { return value.trim(); }
```

Existing tests call this function and assert `"  alpha  beta  " → "alpha  beta"`, `" x " → "x"`, and `"   " → ""`. Scenario evidence: current tests actually ran successfully on the inspected candidate. Author proposes no production change and reports those results. No new feature, contract ambiguity or unmet guarantee exists.

Must a reviewer require a new helper, duplicate test or changed file to prove work happened?

## R09 — fewer lines, more hidden control flow

Requirement: debit only a positive safe-integer amount within the balance; rejection must leave the ledger unchanged. Balance is a trusted nonnegative safe integer from the validated ledger; the caller writes only after this pure calculation returns. The existing clear implementation is correct, tested and adequate. No measured performance need exists.

```ts
// Existing
function debit(balance: number, amount: number): number {
  if (!Number.isSafeInteger(amount) || amount <= 0 || amount > balance) {
    throw new RangeError("invalid debit");
  }
  return balance - amount;
}
// Candidate
const debit=(b:number,a:number)=>Number.isSafeInteger(a)&&a>0&&a<=b?b-a:(()=>{throw new RangeError("invalid debit")})();
```

Scenario evidence: same behavior tests remain green. Author calls it an optimization solely because lines/characters decrease. There is no ledger write in either function. Judge readability/maintenance benefit, not invented lost persistence behavior.

## R10 — unexpected data-flow effect

Approved flow: authenticate → validate report query → read authorized records → render CSV → return download. No network call outside the application and no new dependency are needed.

Candidate performs the same flow but adds `await publicAnalytics.send({ actorEmail, reportRows })` before returning. The source and caller trace confirms it sends complete private records to an external endpoint. Tests stub analytics and assert only correct CSV output. The author leaves analytics out of the map.

Identify the unexpected edge, privacy/authority consequence, and smallest scope-preserving correction. Do not update the diagram to bless an unapproved data disclosure.

## R11 — similar syntax, different guarantees

Requirement: retain two existing operations with different contracts. Charge requires a positive safe-integer amount and may create one new ledger entry; refund may only reference a prior settled charge and must not exceed its remaining refundable amount. Those contracts are already observed by direct success/rejection/state tests.

Candidate replaces the two public functions with `adjustBalance(id, amount, isRefund)` solely because both call a ledger writer. Public callers must now choose a boolean. Separate validations remain correct and tests pass; the new shared function owns unrelated authorization/state rules and must branch repeatedly on the boolean. No genuinely shared policy or demonstrated navigation/maintenance improvement exists.

Judge semantic ownership. Do not demand blind DRY on the second similar block; a shared low-level writer already exists.

## R12 — callback reached through a registry

Requirement: preserve supported `invoice.paid` event handling.

```ts
const handlers = new Map([["invoice.paid", handleInvoicePaid]]);
export async function dispatch(event: ProviderEvent) {
  const handler = handlers.get(event.type);
  if (!handler) throw new UnsupportedEvent(event.type);
  await handler(event);
}
```

No direct `handleInvoicePaid(...)` call is found by grep. An integration test dispatches `invoice.paid` through this exported path and observes the correct ledger state. Scenario evidence: it ran successfully on this candidate. A debloat proposal deletes the handler and its registry entry as dead code.

Is that removal justified? Identify the reachable route and preservation failure.

## R13 — improved implementation over initial map

Requirement: validate an amount and compute a pure quote without changing state. Initial map used three proposed forwarding adapters before an existing pricing function. During implementation the author found the pricing function already accepts the validated command and removed the proposed adapters.

Actual trace: schema parse → existing pricing function → safe response. No I/O/state change or missing authorization requirement exists. Scenario evidence: direct valid/invalid-input and quote-result tests ran successfully on the candidate. Author records why the current map differs and updates the design slice; initial intent remains discoverable in history.

Must code be forced back to the initial map merely to match it?

## R14 — green skipped check / unverified behavior

Requirement: verify an implemented TypeScript change before calling it accepted.

Evidence packet: job conclusion success. Checkout and an existence probe ran; dependency installation, lint, typecheck and tests were all skipped because the expected root configs were absent. The author supplies no other applicable test evidence. Code itself is not supplied in this case.

What verdict does this evidence support? State what is missing without inventing a code defect or claiming an unavailable tool test passed.

## R15 — receipt is not approval or enforcement

Requirement: report adopted-unit freshness separately from provenance, configured controls and actual execution evidence.

Candidate hashes agree with an editable local receipt's recorded source unit; source-owner approval and check execution have no supporting records. A status renderer labels the project `approved, fully enforced, all checks passed` based solely on the hash/version match.

Judge that claim and the smallest honest status correction. A matching fingerprint can be useful without authenticating approval or proving tests ran.

## Exercise boundary

No production tests were executed for this packet. Independent review evaluates the method and visible contradictions under explicitly stated scenario premises. C1 reuses these cases against actual revised instructions. C3 and overlay chunks must supply genuine executable positive/negative fixtures and candidate-bound runtime evidence; a clean result here cannot replace those gates.
