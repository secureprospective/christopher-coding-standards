# Session notes

Append-only retrospective log — what worked, what didn't, for sessions
working in this repo (or repos that have adopted this standard). Distinct
from `docs/cross-pollination-log.md`, which is an audit trail of individual
Recon/Audit rounds; this file is process- and standard-level: the kind of
lesson that should eventually change `AGENTS.md`, a template, or this
repo's own routing in `docs/INDEX.md`.

**Not read during normal sessions** — see `docs/INDEX.md`. It's read during
a periodic standards review: mining entries for recurring patterns, then
promoting them into actual changes and marking them actioned below.

## When and how to write an entry

At session close, the Builder (Claude) appends one entry covering the
session just finished:

- **What worked** — approaches, prompts, file structures, or workflow steps
  that held up. Specific enough to repeat on purpose, not "good
  communication."
- **What didn't** — friction, rework, ambiguity, or anything that cost more
  tokens/time than it should have. Root cause, not just the symptom.
- **Cross-agent perspective** — if a Recon/Audit agent (Antigravity or
  otherwise) did substantive work this session, ask it directly — via the
  cross-pollination relay in `docs/multi-agent-roles.md` — what worked and
  didn't from its side before closing. Two agents looking at the same
  session often disagree about where the friction was; both views are the
  point. Omit this section if no other agent did real work.
- **Standard impact** — concrete, actionable items only. Each item is
  either marked actioned (with where) in the same entry, or left open for a
  future standards review to pick up.

Keep entries short — a few bullets per section, not a transcript.

## Format

```
## YYYY-MM-DD — <session focus / branch / PR>

**Agents involved:** Claude (Builder) [+ Antigravity (Recon/Audit), if applicable]

**What worked:**
- ...

**What didn't:**
- ...

**Cross-agent perspective:** (omit if N/A)
- Antigravity reported: ...

**Standard impact:**
- [ ] <open — proposed change, not yet made>
- [x] <actioned — what changed and where>
```

---

## 2026-06-10 — PR #1 + PR #2 (multi-agent governance, repo compaction)

**Agents involved:** Claude (Builder) only — no Recon/Audit agent did
substantive work this session.

**What worked:**
- Iterative single-step confirmation (sketch → confirm → commit → push →
  PR → CI check, one decision at a time) kept both PRs small, reviewable,
  and easy to back out of if a step landed wrong.
- `docs/INDEX.md` as a task-routing table, plus turning the adoption
  checklist and read-side GitHub calls into skills, directly cuts what a
  future session has to load — the compaction goal was achieved by
  *deleting reasons to read things*, not by shrinking the docs themselves.
- Splitting `gh.py` into read-only (skill-ified) vs. write/destructive
  (stays manual) mapped cleanly onto the global CLAUDE.md rule about
  hard-to-reverse, shared-state actions — the existing rule was sufficient,
  no new policy needed.
- `Monitor` with an until-loop for CI polling replaced a blocked
  `sleep && check` chain cleanly once discovered.

**What didn't:**
- First version of `gh.py` tripped the `dynamic-urllib-use-detected`
  semgrep rule on push — found and fixed reactively via job logs. The
  scheme/host-validation pattern (validate `urllib.parse.urlparse(url)`
  before `urlopen`, with a documented `# nosemgrep:` comment) should be
  baked into any future script template that calls external APIs, so it's
  written correctly the first time.
- The README "make it cool" request needed two passes because the first
  edit landed on the session branch while Christopher was viewing `main` on
  GitHub — read as "nothing changed." When asking Christopher to view
  something on GitHub mid-session before merge, say explicitly that it's on
  the session branch, not `main` yet.

**Standard impact:**
- [ ] Open: add the urllib scheme/host-validation pattern to a shared
  reference (e.g. a short note in `AGENTS.md` or a snippet in
  `templates/`) for any future Python script hitting external APIs.
- [ ] Open: when pointing Christopher at a GitHub URL for a pre-merge
  review, state it's on the session branch, not `main`.
- [x] Actioned: `docs/INDEX.md` created with a routing table (PR #2).
- [x] Actioned: `skills/adopt-coding-standards/` and `skills/github-pr/`
  created (PR #2).

## 2026-06-10 — PR #3 + PR #4 (session-notes log, Astro overlay / Phase 1D)

**Agents involved:** Claude (Builder) only.

**What worked:**
- Checking TFM's actual Astro setup and Astro's official tsconfig presets
  before drafting the overlay grounded it in what a live project needs,
  rather than guessing versions/structure.
- Mirroring Phase 1C's exact file shape (README structure, the
  package.json.snippet/Makefile/.pre-commit-config.yaml.snippet split) made
  Phase 1D fast to draft and easy to cross-reference.
- The `astro — check` CI job's conditional no-op pattern (mirroring
  `ts-lint`/`ts-test`) passed first try, confirmed on this repo (which has
  no `astro.config.*`).

**What didn't:**
- No `pyyaml`/`js-yaml` available locally to fully parse-validate
  `security.yml` — fell back to a tab-character check plus structural
  comparison against existing jobs. Low risk for a doc/template-only repo,
  but worth a real parse check if a future overlay needs more complex YAML
  (e.g. matrix builds).
- A throwaway JSONC-comment-stripping regex (`//.*`) ate the `https://`
  inside a URL inside a comment-stripped string, producing a false
  validation failure — cost a few minutes of confusion before realizing the
  file itself was fine. Lesson: anchor comment-stripping regexes to
  line-start (`^\s*//`), not bare `//`.

**Standard impact:**
- [ ] Open: Phase 2 — consider whether the dev environment should have
  `pyyaml`/`js-yaml` available for real YAML validation.
- [x] Actioned: `docs/session-notes.md` created (PR #3).
- [x] Actioned: `templates/astro/` (Phase 1D) merged (PR #4); `astro —
  check` CI job added.

## 2026-06-10 — PR #6 (MPL-2.0 license)

**Agents involved:** Claude (Builder) only.

**What worked:**
- Fetching the license text from `mozilla.org/media/MPL/2.0/index.txt`
  (plain-text source) rather than scraping the HTML page or relying on
  memory gave an exact, verifiable copy in one step.
- Closing a long-open `CLAUDE.md` item (License) was a small, fast,
  low-risk PR — good shape for a quick end-of-session task.

**What didn't:**
- Nothing notable — straightforward doc/license addition, all CI checks
  passed first try.

**Standard impact:**
- [x] Actioned: `LICENSE` (MPL-2.0) added, README badge/section updated,
  "License" open item removed from `CLAUDE.md` (PR #6).

## 2026-06-13 — Go overlay completion: Gates 1/2 + filelen (`session/go-overlay-g0`)

**Agents involved:** Claude (Builder) + Antigravity (Recon/Audit, T4 review)

**What worked:**
- Decision-gates-up-front: laying out each enforcement choice (struct-wrap vs.
  analyzer vs. checklist) with plain-language *risk-if-unfixed* let a
  non-Go-expert owner make the right calls fast, then engineer against locked
  decisions instead of guessing.
- Building the `interface{}` guard as a `go/analysis` vettool (unitchecker,
  `go vet -vettool`) in its own pinned module with an `analysistest` suite +
  `//ifaceguard:allow` hatch — clean `make lint`/pre-commit integration, no
  dependency added to the consuming project's `go.mod`.
- Struct-wrap (unexported field) turns AD-06 into a *compile* error — stronger
  than any linter and free, since no `playerid` code existed yet.
- Verifying every new gate with a deliberate violation *before* trusting it
  caught two would-be silent gates (see below). Non-negotiable.

**What didn't:**
- Custom-gate authoring keeps reproducing the Friction-#8 trap — a gate that
  *looks* right but silently no-ops. Hit twice: an early `playerid` draft
  imported `database/sql/driver` (depguard's `sql-confined` rule correctly
  rejected it — the rule working), and the first `filelen` used
  `find -exec awk 'exit 1'`, which doesn't propagate exit status (printed the
  violation, exited 0). Both caught only by running a real violation. Lesson is
  now baked into the README's 3-part verification test.
- agy is NOT usable for quick Q&A: two introspection attempts produced zero
  output (10-min hang on the default model; 150s `timeout` on Flash-Low). It
  reliably does heavy, file-producing tasks only. ~12 min spent before the rip
  cord.

**Cross-agent perspective:**
- Antigravity (T4 re-review of `internal/mfl` via SSH-relay): **0 hallucinations**
  this pass (vs. 1-in-8 in T3); independently re-found 2 known-valid items
  (timer leak, missing `rps>0` guard) consistent with T3 — stable calibration;
  flagged one context-overstated item (backoff jitter, irrelevant for a
  single-client desktop app); correctly self-dismissed a non-issue.
- A *live* agy retrospective relay was **not** run this close: the same session
  established agy cannot return a quick answer (two timeouts), so a retrospective
  prompt would risk another long hang. Its perspective is captured from the T4
  output instead. This deviation is itself a standard-impact item.

**Standard impact:**
- [x] Actioned: Go overlay completed — `playerid` struct-wrap, `ifaceguard`
  vettool, `filelen` gate; README converted gaps→resolved with a 3-part
  verification test (this branch).
- [ ] Open: `docs/multi-agent-roles.md` should state agy is a *heavy-task*
  collaborator, not a fetch/Q&A tool — dispatch substantial tasks that write a
  file artifact, wrap every `agy -p` in a `timeout`, never expect quick stdout.
- [ ] Open: Layer-11 (local-model selection) + Phase-3 (dual-model) are now
  **moot** — Christopher cut the local-AI idea (2026-06-13). Needs a wind-down
  pass at a standards review.
- [ ] Open: a Claude-side "fetch-delegation discipline" (Haiku fetchers; when
  to delegate vs. read inline) — drafted in concept, parked until a real build
  session creates the context pressure it relieves.

## 2026-06-13 — Showpiece README (#9) + the Agent Codex (#10) + agy capability probe

**Agents involved:** Claude (Builder) + Antigravity (Recon — deep web research for the Codex)

**What worked:**
- The GitHub **API merge flow** under branch protection (no `gh`): open PR → poll
  `commits/{sha}/check-runs` until none pending → `PUT /pulls/N/merge` (squash).
  Reliable across three PRs; token read from `~/.git-credentials` without echoing.
- Gating the **public README** on the owner's taste (CI green → present → merge on
  his nod) was the right call for creative/front-facing copy, vs. auto-merging.
- Dispatching agy a **deep-research task that writes a file artifact** played
  exactly to its strength — ~30 sourced items returned, dense and usable. The
  right shape for agy: heavy task + file output + generous `timeout`.
- **Triaging agy's research citations** (M13 applied to web recon, not just code):
  verified the canon against first-hand knowledge, flagged one shaky attribution
  `[unverified]` rather than launder it. Caught exactly the failure mode the
  Codex itself warns about.

**What didn't:**
- agy **cannot return a quick answer.** A 4-line capability-introspection probe
  produced zero output twice (10-min hang on the default model; 150s `timeout` on
  Flash-Low). Root cause likely: asked to "list tools," it tried to *use* tools to
  introspect, and spiralled. Confirms agy is heavy-task-only — costed ~12 min
  before the rip cord. (Mitigation now doctrine: wrap every `agy -p` in a
  `timeout`; ask for a file artifact; never expect fast stdout.)

**Cross-agent perspective:**
- Antigravity's research output *was* its contribution this round; it's folded
  into `docs/agent-codex.md` §F and credited there. No separate retrospective
  relay — same quick-answer limitation as above.

**Standard impact:**
- [x] Actioned: README showpiece (PR #9) — "forbid don't warn", "proof the gates
  bite", measured multi-agent loop.
- [x] Actioned: **`docs/agent-codex.md`** (PR #10) — agent-facing build doctrine,
  17 motifs + slop catalog + canon→motif map + triaged field intelligence; routed
  in `docs/INDEX.md`; adopted into TheWarRoom so agy's clone gets it on pull.
- [ ] Open (Codex-flagged adoptions for a future overlay/standards pass):
  dependency-existence/**slopsquatting** check; a **`dupl`** duplication gate;
  **license scanning** in CI; **SBOM + signed provenance** for shipped binaries.
- [ ] Open: fold "agy is heavy-task-only, wrap in `timeout`, expect a file not
  stdout" into `docs/multi-agent-roles.md` (re-confirmed this session).

## 2026-06-15 — Cloudflare Workers overlay (extends the TS overlay)

**Agents involved:** Claude (Builder), solo. No Recon/Audit round — agy is benched for the social-media-automation track that drives this work (and by the 2026-06-13 local-AI pivot).

**What worked:**
- **Verifying a stale premise before building.** The task arrived as "author the TS
  overlay" (carried in a project memory). One disk check showed the TS overlay
  already existed and was strong — so the session produced the *actually-missing*
  piece (the Workers extension), not a duplicate. Lesson: when a memory asserts a
  gap, confirm the gap on disk before filling it.
- **Treating my own Cloudflare knowledge as untrusted, then checking it.** Three
  shapes I "remembered" were wrong/stale: the vitest pool uses the `cloudflareTest()`
  plugin (not `defineWorkersConfig`/`poolOptions.workers`, now deprecated), requires
  Vitest 4.1+, and `env` now imports from `cloudflare:workers` (not `cloudflare:test`).
  All pinned against live June-2026 docs before a line was written. For a canonical
  template others copy, model-memory is third-party code too — verify it.
- **Reusing the base overlay instead of duplicating it.** The Workers overlay keeps
  the TS overlay's Biome/pre-commit/Gitleaks untouched and only replaces what
  workerd actually forces (tsconfig, vitest, toolchain). Mirrors the Astro overlay's
  relationship — kept the diff small and the layering legible.

**What didn't / honest limits:**
- **Stryker can't drive the workerd pool.** Rather than paper over it, the README
  documents the split: mutation-test pure logic via the base config; use the Workers
  pool for binding-dependent integration tests. A gate that can't run shouldn't be
  implied to run.
- **No deliberate-violation test shipped** (unlike the Go overlay). The Workers gates
  are config/type-level and need a real Worker entrypoint to fire, so verification is
  a README procedure, matching the TS/Astro overlays. Honest, but weaker than Go's
  "proven by a failing build" bar.

**Standard impact:**
- [x] Actioned: `templates/cloudflare-workers/` — Wrangler config, workerd Vitest
  pool, `wrangler types` bindings, npm toolchain; codifies bindings-as-capability-
  grants + secrets-never-in-`vars`. Routed in `docs/INDEX.md`; README/CLAUDE.md/TS-
  README cross-references added.
- [ ] Open: consider a real deliberate-violation harness for the Workers overlay
  (a minimal Worker that proves the typed-`Env` and secret-discipline gates fail) to
  reach the Go overlay's "proven, not asserted" bar.
- [ ] Open: a generic "verify SDK/runtime API shapes against live docs before writing
  a canonical template" line belongs in `AGENTS.md` — this session is the second time
  stale model-memory of a fast-moving API would have shipped wrong config.

---

## 2026-06-20 — GLM large-context auditor + front-end QA doctrine (Layer 10.5)

**Agents involved:** Claude (Builder), solo authoring. The session's *subject* was standing up GLM (Z.ai Coding Plan via OpenCode on the "bird" worker node) as a third agent; this entry covers the doctrine layered back into the standard.

**What worked:**
- **A live test killed a planning assumption before it shipped.** The plan assumed "GLM sees the front end and QAs it visually." First real run proved GLM-5.2 is **text-only** — it captured a screenshot and openly said it couldn't view it, then did excellent *structural* QA (contrast math, ARIA gaps, a step→chart binding bug) off the DOM instead. The doctrine now reflects reality: two-lane QA (structural + deterministic pixel-diff), never "the model sees the page."
- **Triaging a recon agent's output as leads, not findings.** A GLM web-recon returned a tidy table at uniform HIGH confidence; triage found most of it fabricated — invented repo owners, and a pricing claim that contradicted a live API test from minutes earlier. The one verified gem (deterministic visual-regression: `toHaveScreenshot`/pixelmatch) became the actual design. Logged as the M18 receipt.

**What didn't / honest limits:**
- **Semantic visual QA is deferred, not solved.** "Does it look good / on-brand" needs a real vision model; the Lite plan denies Z.ai vision models. Documented as an explicit deferral with a revisit condition, not papered over.
- **No deliberate-violation gate for the doctrine itself** — it's process doctrine (M18 + dispatch/triage rules), enforced by the existing human-owner merge gate and `cross-pollination-log.md`, not a CI check.

**Standard impact:**
- [x] Actioned: `docs/glm-auditor-discipline.md` (Layer 10.5); `agent-codex.md` §M18 + two slop-catalog rows; `multi-agent-roles.md` mapping (GLM as second recon-class agent, same exclusions); routed in `docs/INDEX.md`; `CLAUDE.md` layer table + key files + motif count (17→18).
- [ ] Open: **agy reliability is a tracked problem** — its fabrication rate this session (and prior) warrants a dedicated session to build a focus/triage process around it. How much is prompt-side vs model-side is part of that diagnosis.
- [ ] Open: first real GLM whole-repo de-slop audit + cross-pollination-log entry, to move the doctrine from authored to proven.

---

## 2026-07-24 — Backport pass: TS biome.json + Go .golangci.yml (both defects found by adopters, fixed here)

**Agents involved:** Claude (Builder), solo authoring. Pure backport — both fixes were already proven correct in adopter repos (social-media-automation for TS, TheWarRoom for Go); this session ported them into canonical and verified with the real tools rather than re-deriving.

**What worked:**
- **Verify against the real tool, not just visual diff.** `npx @biomejs/biome check --config-path` and `golangci-lint config verify` both ran clean against the fixed configs before commit — the exact check whose *absence* caused both defects to ship in the first place (see the 2026-06-15/06-17 entries this repo's memory already flagged). Closing the loop meant running the check, not just trusting the adopter fix looked right.
- **Deliberately narrowed the Go backport.** TheWarRoom's `.golangci.yml` also adds project-specific depguard paths (`internal/normalize`, `internal/output`) that only make sense for TheWarRoom's actual package tree — the canonical template's own header comment says adopters find/replace the depguard rules for their tree, so those stayed out. Only the generically-applicable fixes crossed: the two schema-invalid empty `{}` settings blocks, three new linters (`nolintlint`/`exhaustive`/`nilerr`), `run.concurrency: 1` (documented as removable on bigger hardware), and denying `net/http`/`net`/`os` in the pure-engine rule (a generic "pure means no I/O by any path" hardening, not TheWarRoom-specific).

**What didn't / honest limits:**
- **Still no automated config-verify CI job in this repo** for the shipped template configs — the fix here is manual verification at backport time, not a standing guard. Considered adding one; deferred as scope creep on a "small backport" session (Task_list.md explicitly scoped this as the small item before Python/Bash overlays). Flagged below as the natural next hardening.

**Standard impact:**
- [x] Actioned: `templates/typescript/biome.json` (`files.ignore`→`files.includes` with `!`-negation; `noConsole` moved `style`→`suspicious`); `templates/go/.golangci.yml` (empty settings blocks removed, `nolintlint`/`exhaustive`/`nilerr` added, `run.concurrency: 1`, pure-engine I/O denial extended to `net/http`/`net`/`os`). Both configs verified clean against the real tool (Biome 2.4.15 `check`, golangci-lint 2.12.2 `config verify`).
- [ ] Open: add a CI job that runs `golangci-lint config verify` + `biome check` directly against `templates/go/.golangci.yml` and `templates/typescript/biome.json` on every PR to this repo — closes the root cause (a shipped config was never verified against its own schema) permanently instead of relying on the next adopter to catch it.

---

## 2026-07-24 — Python overlay (`templates/python/`), Phase 2 continuation

**Agents involved:** Claude (Builder), solo authoring. Task_list.md scoped this as "GLM drafts, Claude reviews," but no bird/GLM session was available this pass — built directly, following the Go/TS overlay pattern as the template per this repo's own Session Start Instruction.

**What worked:**
- **No tools installed locally, so installed the real toolchain rather than authoring blind.** `python3-venv`/`pip` weren't present on this box; `sudo apt-get install python3-venv python3-pip` plus a scratch venv got ruff 0.16.0, mypy 2.3.0, pytest 9.1.1, pydantic 2.13.4 running for real. Every config in this overlay was checked against the actual binary, not assumed correct by inspection — same discipline the 2026-07-24 backport session applied, extended to a from-scratch build.
- **Ran the full deliberate-violation test live**, including through `pre-commit run` (not just the standalone tools) — confirmed all four gates fire: ruff (`S608` SQL injection, `S602` shell=True, `F401`/`F841`), mypy (`no-untyped-def`, `assignment`), and gitleaks (AWS key pattern). Also verified the *clean* case passes with zero findings, and exercised the Pydantic strict/lenient boundary policy at runtime (external model tolerates an unknown field, internal model rejects one, a non-numeric id is rejected) — not just read as plausible.
- **Caught a wrong example en route:** the first-draft deliberate-violation test used AWS's own documented example key `AKIAIOSFODNN7EXAMPLE`, which gitleaks allowlists by design as a known false-positive — it silently did NOT fire. Found only because the test was actually run, not because it looked wrong on inspection. Fixed to a non-allowlisted `AKIA...` string and re-verified it fires. This is itself the exact class of defect the 2026-07-24 backport session was closing (an unverified claim in a template/doc that looks right but silently doesn't work) — evidence for actioning the open CI-verification item above, generalized: templates need to be run, not just written.
- **Tool choice: ruff over flake8+isort+black+bandit.** One tool, one config — mirrors the TS overlay choosing Biome over ESLint+Prettier and the Go overlay's "avoid surprise linters a weaker model can't reason about." ruff's `S` (flake8-bandit) rule family covers SAST directly, so Layer 7 for this overlay is ruff (SAST) + gitleaks (secrets) + pip-audit (SCA) — three legs, same split as the Go overlay's gosec/depguard/gitleaks.
- **Pydantic v2 over a hand-written `Validate()`** (unlike the Go overlay, which deliberately avoids struct-tag reflection). Documented why explicitly in `schema/example.py`'s docstring: the risk Go avoids (an LLM hallucinating struct tags) doesn't transfer the same way to Pydantic's field/method validators, which are type-checked by mypy and are the idiomatic, battle-tested choice in Python. The strict/lenient unknown-field policy (external=`extra="ignore"`, internal=`extra="forbid"`) is identical doctrine to the Go/TS schema templates.

**What didn't / honest limits:**
- No GLM/bird draft pass this session — Task_list.md's suggested workflow (GLM drafts against Go/TS overlays, Claude reviews) wasn't followed; built and self-verified directly instead. Not a regression on quality (every gate was proven live), but worth naming since it deviates from the stated plan.
- mutmut and pip-audit were installed and version-checked but not run against a real violation case in this session (no representative source tree to mutate/audit) — their wiring (`Makefile.snippet` targets) is asserted correct by tool documentation, not proven live, unlike ruff/mypy/gitleaks/pytest above.

**Standard impact:**
- [x] Actioned: `templates/python/` — `pyproject.toml.snippet` (ruff/mypy/pytest/coverage config), `.pre-commit-config.yaml` (ruff-check+ruff-format, mypy, gitleaks; SHA-pinned to ruff v0.16.0, mypy v2.3.0, gitleaks v8.30.1), `Makefile.snippet` (lint/fmt/typecheck/test/test-coverage/sca/mutation-test), `schema/example.py` (Pydantic v2 boundary pattern), `README.md` (adoption guide + verified deliberate-violation test). `CLAUDE.md` phase status, Key Files table, and header updated.
- [ ] Open: the CI-config-verification item from the 2026-07-24 backport entry above now also covers Python — a future CI job verifying shipped templates against their real tools should include `ruff check`/`mypy` on this overlay's own `schema/example.py`, not just Go/TS.
- [ ] Open: Bash overlay is the last Phase 2 item.

---

## 2026-07-24 — Bash overlay (`templates/bash/`), Phase 2 complete

**Agents involved:** Claude (Builder), solo authoring, same as the Python overlay session earlier today.

**What worked:**
- **Installed the real toolchain again rather than authoring blind** — shellcheck, shfmt, and bats weren't on this box; `sudo apt-get install shellcheck shfmt bats` (Debian bookworm: shellcheck 0.9.0, shfmt 3.6.0, bats 1.8.2) got real binaries running. Every file in this overlay was checked against them, including a full 9-assertion bats suite (unit tests on `lib/strict-mode.sh`'s `require_arg`/`require_positive_int`, integration tests running `scripts/example.sh` end to end) — all passing live, not asserted.
- **`lib/strict-mode.sh` as the Bash overlay's boundary-validation layer** — `require_arg`/`require_positive_int` fail loud on an empty/malformed script input before it reaches business logic, the same role Pydantic/Zod/hand-written `Validate()` play in the Python/TS/Go overlays. Documented as such in the file's own header comment so the pattern reads as intentional, not incidental.
- **Curated `.shellcheckrc` optional-check set** (5 specific checks, not `enable=all`) — same "avoid surprise linters a weaker model can't reason about" reasoning as the Go overlay's `linters: default: none` and this morning's Python overlay's curated ruff `select` list. Each enabled check has a one-line rationale in the file.

**What didn't / two real defects caught only by running the deliberate-violation test, not by reading the config:**
- **SC1091 false positive on the dynamic `source` path.** `scripts/example.sh` computes its own directory at runtime (`$(dirname "${BASH_SOURCE[0]}")`) and sources `lib/strict-mode.sh` relative to that — shellcheck can't statically follow a dynamic path and needs the `# shellcheck source=` comment, but by default resolves that comment's path relative to the *shellcheck invocation's cwd*, not the linted file's own directory. Linting from the repo root reported a false "does not exist." Fixed by adding `source-path=SCRIPTDIR` to `.shellcheckrc`.
- **The shfmt pre-commit hook silently no-op'd.** Its default `args:` is `[--write]`; this overlay's `.pre-commit-config.yaml` supplies a custom `args:` list to set `-i 2 -ci -sr` (indent/style flags) — and pre-commit's custom `args:` **replaces** the hook's default rather than merging with it. The first draft's custom list omitted `-w`, which silently dropped `--write` entirely: `pre-commit run` reported the shfmt hook as `Passed` on a file with an unindented `if/then/fi` block that plainly needed reformatting — no diff shown, no failure, no fix applied. Caught only because the deliberate-violation test was run through the actual `pre-commit run`, not `shfmt -d` standalone (which did correctly flag it, masking the hook-level bug during earlier spot-checks). Fixed by adding `-w` to the custom args list, with a comment in `.pre-commit-config.yaml` naming the trap. **Same root-cause shape as the AWS-example-key catch in this morning's Python session: a plausible-looking config that silently doesn't do its job, only surfaced by actually exercising it end to end.**
- No GLM/bird drafting pass this session either — consistent with the Python overlay session, built and self-verified directly.

**Standard impact:**
- [x] Actioned: `templates/bash/` — `.shellcheckrc` (curated 5-check set + `source-path=SCRIPTDIR`), `.pre-commit-config.yaml` (shellcheck-py v0.11.0.1, scop/pre-commit-shfmt v3.13.1-1 with the `-w` fix documented inline, gitleaks v8.30.1; `.bats` files excluded from both lint hooks), `Makefile.snippet` (lint/fmt/test), `lib/strict-mode.sh` + `scripts/example.sh` (boundary-validation pattern), `tests/example.bats` (9 passing assertions), `README.md` (adoption guide + verified deliberate-violation test, including both defects found above). `CLAUDE.md` phase status, Key Files table, header, and Open Items updated — **Phase 2 is now complete.**
- [ ] Open (carried forward, now covers three overlays): the CI-config-verification item from the 2026-07-24 backport/Python entries — a future CI job should also run `shellcheck`/`shfmt -d` against `templates/bash/`'s own shipped files on every PR to this repo.
- [ ] Open: Phase 3 (local-model selection guidance, dual-model architecture doc) and the deferred cross-pollination pilot (Antigravity audit of `templates/astro/`) are the two candidates for the next substantive session here.

---

## 2026-07-24 — Phase 3: local-model selection guidance (`docs/local-model-guidance.md`, PR #22, squash `6e50109`)

**Agents involved:** Claude (Builder), solo authoring.

**What worked:**
- **Caught a stale premise before building against it.** The project's own memory (`project_christopher_coding_standards`) flagged Phase 3's original scope — a dual-model architecture doc written against the local-ai-stack project — as MOOT after that project wound down 2026-06-13, but `CLAUDE.md`/`Task_list.md` still listed it as the next open item unchanged. Rather than build the stale version, surfaced the contradiction and asked Christopher what Phase 3 should actually cover now that Beelink is a real local-model deployment.
- **Portability constraint set by Christopher mid-session, before any writing started:** local models "will change over time" and hardware will get upgraded — so the doc had to separate durable principles (selection checklist: context window/tool-calling/quant floor/task fit, verified against primary source not folklore; dual-model architecture pattern; weight-agnostic teammate doctrine) from the current fleet (Ornith/Gemma on Beelink), which is included only as an explicitly dated, non-authoritative snapshot with a "re-run the checklist on any hardware/model change" instruction. This is the same discipline the repo already applies to code (don't hardcode what will drift) applied to a planning doc.
- Brought README.md's phase status current in the same PR — it had drifted (still showing Python/Bash overlays as pending after both had merged) and would have misled the next session reading it cold.

**What didn't / honest limits:**
- No live "test" of this doc the way code overlays get a deliberate-violation test — it's guidance prose, not an enforceable gate, so verification here means internal consistency + cross-references to real existing artifacts (`agent-codex-lite.md`, `feedback_beelink_boot_gating`, `lesson_small_model_floor_claims_expire`) rather than a pass/fail run.
- No GLM/bird drafting pass — consistent with the Python/Bash overlay sessions.

**Standard impact:**
- [x] Actioned: `docs/local-model-guidance.md` (new — Layer 11 doctrine), `docs/INDEX.md` routing row, `CLAUDE.md` Layer 11 table row/Phase Status/Key Files/Open Items, `README.md` Layer 11 row + phase-status catch-up (Python/Bash/Phase 3 all marked complete).
- [ ] Open: still no CI job verifying shipped template configs against their real tools (carried forward from the backport/Python/Bash entries — now the longest-standing open item in this log).
- [ ] Open: the deferred cross-pollination pilot (Antigravity/second-vantage audit of `templates/astro/`) is now the only unscoped item left from the original Phase 2/3 list.

---

## 2026-07-24 — Cross-pollination pilot: `templates/astro/` pre-commit hook (PR #24, squash `06064b1`)

**Agents involved:** Claude (Builder), GLM 5.2 via OpenCode on bird (Recon/Audit — the current mapping post-Antigravity retirement).

**What worked:**
- **First real cross-pollination round under the current GLM 5.2 mapping.** The `docs/multi-agent-roles.md` workflow (self-contained scoped prompt → human relay → agent runs it → Builder triage against source → integrate) held unchanged from the Antigravity-era pilot — only the agent identity changed, exactly as the doc's own framing ("roles are what matter, not vendor names") predicted.
- **Scoping the request around this repo's known failure class paid off immediately.** Rather than "audit templates/astro/" (an explicitly banned vague request per the workflow), the prompt asked 4 closed-ended questions targeting exactly the "config looks right but silently no-ops" pattern already caught 3 times this month (AWS-example-key allowlist, shellcheck SCRIPTDIR, shfmt `args:` replace-not-merge). It found a 4th instance on the first try.
- **Triage against primary source caught something GLM's own session didn't finish.** GLM's run correctly identified the `rev: "v3.4.2"` tag doesn't exist but got cut off mid-diagnosis before reaching a verdict. Claude verified independently (`git ls-remote --tags` on the real repo — confirmed newest tag is `v3.1.0`), then went a layer deeper than the cut-off session reached: repinning to a real tag still doesn't fix it, because Prettier 3's ESM plugin resolution can't cross the hook's isolated `additional_dependencies` environment. This is the textbook shape of the doctrine's "second vantage is real but not an oracle" rule (Codex M13) — the agent's lead was correct as far as it went, and the Builder still had to do the deeper source-verification work to land a real fix.

**What didn't / honest limits:**
- GLM's OpenCode session ended before delivering the final closed-ended answer summary — it stopped mid-reasoning after diagnosing the mechanism but before running its own planned diagnostic. Not a wasted round (the critical finding was real and actionable), but a reminder that headless GLM 5.2 runs over SSH are not guaranteed to reach a clean stop; budget for the Builder to finish verification independently rather than assuming a complete handoff.
- Q1–Q3 (Prettier reformatting, tsconfig extends resolution, astro check pass/fail) were accepted on the strength of GLM's specific, internally consistent evidence (real error codes like `ts6133`/`ts2322`, a correctly-reasoned Node-resolver-vs-tsc-resolver distinction for Q2) rather than independently re-run by Claude — a judgment call to spend verification effort where the stakes were highest (the pre-commit hook, the actual shipped enforcement mechanism), not evenly across all 4 questions.

**Standard impact:**
- [x] Actioned: `templates/astro/.pre-commit-config.yaml.snippet` (mirrors-prettier remote hook → `repo: local` hook), `templates/astro/README.md` (new "Why a local hook, not mirrors-prettier" section, corrected verification-test expectations, corrected stale Phase 2/3 status footer), `docs/cross-pollination-log.md` (new dated entry). Fix verified end-to-end through `pre-commit run` itself with the exact shipped snippet content, not just standalone CLI or direct binary invocation.
- [ ] Open: this closes the last item from the original Phase 2/3 list. The one item still carried forward across four sessions now is the CI job that verifies shipped template configs against their real tools on every PR — this cross-pollination round is itself evidence of exactly why that job would pay for itself (a config sat broken, unnoticed, since 2026-06-10).

---

## 2026-07-26 — Bun + ECS overlay (`templates/bun-ecs/`)

**Agents involved:** Claude (Builder), solo authoring.

**What worked:**
- **Net-new overlay outside the phase roadmap, requested by a downstream project (Shadowbane Rebuild) rather than this repo's own planning.** Read the requesting project's `ECS_RULES.md`/`SYSTEM_ORDER.md`/`BLUEPRINT.md` first instead of designing an ECS pattern generically — the overlay's enforcement rules (import layering, component purity, file-length cap) are a direct port of that project's already-locked architecture-panel decisions, not an independent invention.
- **Installed the real toolchain again, same discipline as every prior overlay.** Bun wasn't present on this box — installed it live, then hit `dependency-cruiser@18.1.0`'s Node `^22||^24||>=26` engine floor failing under Bun's Node-20-compat surface on first install. Didn't just downgrade blindly: checked `npm view <pkg> engines` across the last three majors and pinned to `17.4.3` (floor `^20.12`) with the reasoning documented in the overlay's README, not just the pin itself.
- **Wrote the two custom pre-commit hooks (file-length, component-purity) as small Bun scripts rather than reaching for a heavier tool.** `check-component-purity.ts` uses the real TypeScript compiler API (not regex) to catch `class` declarations, method signatures, and function-typed component fields — deliberately mirroring the Go overlay's `ifaceguard` vettool pattern (a custom AST-based check for a project-specific invariant no stock linter covers) rather than under-building it as a grep.
- **Every gate proven live through actual `pre-commit run`, both directions, before anything was copied into the real repo.** Built the whole overlay in a scratch dir first (not directly in the repo), ran `tsc`, Biome, `dependency-cruiser` (four layering rules + circular-import detection + the broadcast-phase carveout), both custom scripts, and gitleaks against a clean example tree (all passed) and then against one deliberate violation per gate (a component with a method + a function-typed field, a 311-line file, a simulate-phase system importing `db/`, a two-file circular import, a planted AWS-shaped secret) — all five failed correctly. Diffed the scratch files against the final copied-in files before committing to confirm byte-for-byte parity between what was tested and what shipped.
- Smoke-ran the example tree under real Bun (`bun run`) — confirmed `World.exportSnapshot()` produces plain `JSON.stringify`-able output at runtime, not just type-checks clean. This closes the same class of gap the astro pilot found (a config/pattern that looks right until actually executed).

**What didn't / honest limits:**
- No GLM/bird cross-pollination round on this overlay — built and self-verified directly, same as the Python/Bash overlay sessions. A natural pilot candidate for a future session (the layering-rule regex paths in `.dependency-cruiser.cjs` are exactly the kind of "looks right, did anyone actually break it" surface GLM has caught elsewhere).
- The `examples/server/src/` reference tree is intentionally minimal (12 files covering one component per pattern, one simulate-phase system, one broadcast-phase system) — it is not a scaffold to build a real game server from, just enough to prove every enforcement rule fires against representative code. The requesting project's actual `rebuild/` scaffold is separate and unaffected by this PR.
- Same standing gap as every prior overlay: this repo has no CI job that re-verifies shipped template configs against real tools on every future PR to this repo — the verification above is a point-in-time guarantee, not a regression gate.

**Standard impact:**
- [x] Actioned: `templates/bun-ecs/` (README.md, package.json.snippet, Makefile.snippet, tsconfig.json, biome.json, `.dependency-cruiser.cjs`, `.pre-commit-config.yaml`, `scripts/check-file-length.ts`, `scripts/check-component-purity.ts`, `examples/server/src/`), `docs/INDEX.md` routing row, `CLAUDE.md` header/Phase Status/Key Files.
- [ ] Open: same CI-config-verification item as above, now spanning five overlays with pre-commit hooks instead of four.
