# Python Overlay — Adoption Guide

Part of `christopher-coding-standards`, Phase 2 (cont.). Companion to the
TypeScript (Phase 1C) and Go (Phase 2) overlays — same role, Python-specific
tooling. Model-agnostic and reusable by any Python project adopting the
standard (Hermes' Python-side tooling, Knowledge Vault scripts, etc.).

---

## What this overlay adds

| Layer | Tool | What it enforces |
|---|---|---|
| Formatter + linter | ruff 0.16 | Style, import sorting, modern syntax, bug patterns, and (via the `S` rule family) SAST — eval, SQL string-building, `shell=True`, weak crypto |
| Type safety | mypy `strict = true` | No untyped defs, no implicit `Any` escapes, `warn_return_any` |
| Pre-commit hooks | pre-commit + ruff + mypy + gitleaks | Blocks commits with lint/type failures or secrets |
| Boundary validation | Pydantic v2 (`schema/example.py`) | Schema-validated external input at every entry point; strict/lenient unknown-field policy matches the Go/TS overlays exactly |
| Testing | pytest + pytest-cov | Test runner + coverage gate |
| Dependency scanning (SCA) | pip-audit | Installed dependencies checked against OSV/PyPI advisories |
| Mutation testing | mutmut | Proves tests assert, not just execute — Python analogue of the TS overlay's Stryker / Go overlay's gremlins |

**Why ruff instead of flake8 + isort + black + bandit:** one tool, one
config, one process — no drift between a formatter and a linter disagreeing
(the same reasoning as the TS overlay choosing Biome over
ESLint+Prettier). ruff's `S` rule family (flake8-bandit) covers the SAST
layer directly, so no separate bandit dependency.

---

## Adoption steps

### 1. Install the toolchain

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install ruff mypy pytest pytest-cov pydantic pip-audit mutmut pre-commit
ruff --version    # verified against 0.16.0
mypy --version    # verified against 2.3.0 (mypy 2.x)
```

### 2. Copy files into your repo root

```
pyproject.toml.snippet  →  merge into pyproject.toml (see step 3)
.pre-commit-config.yaml
Makefile.snippet         →  merge targets into your project Makefile
schema/example.py       →  src/schema/example.py   (boundary-validation pattern)
```

### 3. Merge the pyproject.toml snippet

Open `pyproject.toml.snippet`. Merge the `[tool.ruff]`, `[tool.ruff.lint]`,
`[tool.ruff.format]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, and
`[tool.coverage.*]` tables into your project's `pyproject.toml`. Do not
overwrite an existing `[project]` table.

### 4. Activate pre-commit hooks

```bash
pre-commit install
```

### 5. Re-pin hook SHAs if you bump versions

```bash
git ls-remote https://github.com/astral-sh/ruff-pre-commit v0.16.0
git ls-remote https://github.com/pre-commit/mirrors-mypy v2.3.0
git ls-remote https://github.com/gitleaks/gitleaks v8.30.1
```

Replace the `rev:` values in `.pre-commit-config.yaml` with the full
40-character SHA. Never use a mutable tag (`@v1`, `@latest`) — the
trivy-action lesson (AGENTS.md hard rule).

**mypy's pre-commit hook runs in an isolated environment** and will not see
your project's venv — list any typed third-party package you import (e.g.
`pydantic`) in the hook's `additional_dependencies:`, or mypy will report
false `import-untyped` errors that don't reproduce with `make lint`.

---

## Verification test — deliberate violations

Run this after adoption to confirm every gate fires. Verified live against
the real tools during this overlay's build (ruff 0.16.0, mypy 2.3.0,
gitleaks — pre-commit run, not just `--help` output).

**Step 1:** Create `src/scratch_bad.py` with one violation per gate:

```python
import os               # F401 — unused import
import subprocess


def run(user_input):                                            # mypy: no-untyped-def
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"  # S608 — SQL injection
    subprocess.call(query, shell=True)                           # S602 — shell=True
    x: int = "not an int"                                        # mypy: assignment
    aws_key = "AKIAABCDEFGHIJKLMNOP"                              # gitleaks
    return x
```

(Do not use AWS's own documented example key `AKIAIOSFODNN7EXAMPLE` here —
gitleaks allowlists it by design as a known false-positive, so it will not
trigger the hook. Any other `AKIA`-prefixed 20-char string will.)

**Step 2:** Try to commit it:

```bash
git add src/scratch_bad.py
git commit -m "test: verify gates"
```

**Expected — all four must fire:**
- ruff flags the unused import (`F401`) and both security findings
  (`S608`, `S602`) → pre-commit blocks the commit
- mypy flags the missing type annotation and the `str`/`int` mismatch →
  pre-commit blocks the commit
- gitleaks flags the AWS key → pre-commit blocks the commit
- `make lint` exits non-zero standalone (not just inside pre-commit)

If any gate stays silent, stop and fix the overlay before trusting it in
production — a silent gate means that class of bug ships undetected.

**Step 3:** Delete `src/scratch_bad.py` and proceed.

---

## Unknown-field policy — matches the Go/TS overlays

`schema/example.py` documents and demonstrates the same strict/lenient
split as `templates/go/schema/example.go` and the TS overlay's Zod schemas:

- **External** (3rd-party API/feed you don't own) → `ConfigDict(extra="ignore")`.
  Providers add fields without versioning; rejecting them turns a benign
  upstream addition into an outage.
- **Internal** (your own client/frontend/service) → `ConfigDict(extra="forbid")`.
  An unknown field there is a bug on your side and should fail loudly — the
  Python equivalent of Go's `dec.DisallowUnknownFields()` and Zod's
  `.strict()`.

---

## Mutation testing — `mutmut`

```bash
make mutation-test   # mutmut run --paths-to-mutate=src/ ; mutmut results
```

Not run in CI by default (slow, same as the TS overlay's `mutation-test`
target) — run before a release or when test coverage feels high but
suspiciously easy to reach.

---

## Dependency scanning — `pip-audit`

```bash
make sca   # pip-audit
```

Checks installed dependencies against the OSV and PyPI advisory databases.
This is Layer 7 (security scanning) alongside gitleaks (secrets) and ruff's
`S` rules (SAST) — the same three-legged split the Go overlay documents via
gosec + depguard + gitleaks.

---

## Phase status

- ✅ Phase 1A — repo skeleton
- ✅ Phase 1B — language-agnostic templates
- ✅ Phase 1C — TypeScript overlay
- ✅ Phase 1D — Astro overlay
- ✅ Phase 2 — Go overlay
- ✅ Phase 2 (cont.) — Python overlay (this directory)
- ⏳ Phase 2 (cont.) — Bash overlay
- ⏳ Phase 3 — local-model selection guidance, dual-model architecture doc
