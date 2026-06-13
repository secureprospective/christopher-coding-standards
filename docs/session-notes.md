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
