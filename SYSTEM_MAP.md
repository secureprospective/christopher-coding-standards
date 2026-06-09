# System Map

This file tells AI agents what already exists in this project so they do not reinvent utilities or violate directory boundaries.

> Hand-maintained. Update when new directories, utilities, or external services are added. **Out-of-date system maps degrade agent performance more than missing ones.** If you cannot keep a section current, mark it `STALE` and the agent will skip it.

---

## Directory invariants

Describe each top-level directory and what belongs there. Example format:

- `/cmd` — entrypoints only. No business logic.
- `/internal/lib` — shared utilities. Check here before writing any helper.
- `/internal/db` — all database access. Nothing else imports the database driver.
- `/scripts` — operational scripts. Bash only. Each runnable standalone.
- `/docs/adr` — architectural decision records. Do not modify without proposing a new ADR.

## Existing utilities

List functions, classes, modules that agents should reuse instead of duplicating. Example format:

- `internal/lib/format.FormatCurrency(amount int64) string` — currency formatting
- `internal/lib/hash.SHA256(payload []byte) string` — SHA-256 hashing
- `internal/db.WithTx(ctx, fn) error` — standard transaction wrapper with retry
- `internal/http.WriteJSON(w, status, body)` — JSON response helper with consistent error envelope

## External services

List external services this project talks to. Agents should use the existing client, not write a new one. Example format:

- **Postgres** (primary store) — client in `internal/db/postgres.go`
- **Redis** (cache) — client in `internal/cache/redis.go`
- **S3-compatible object storage** — client in `internal/storage/s3.go`

## Configuration sources

Where configuration comes from. Agents should not invent new config sources. Example format:

- **Environment variables** — loaded in `cmd/server/main.go`. Listed in `.env.example`.
- **Feature flags** — `internal/config/flags.go`. Add new flags there.

## What does not exist (intentionally)

List things agents might assume exist but do not. This prevents wasted exploration. Example format:

- No ORM. Raw SQL with `sqlc`-generated query bindings.
- No logger framework. Standard library only (`log/slog` for Go, `structlog` for Python).
- No DI framework. Constructor injection only.
- No singletons. All dependencies passed explicitly.

## Public-facing surfaces

For security review — list every entrypoint that accepts external input. Example format:

- HTTP API: routes in `internal/http/router.go`, request schemas in `internal/http/schemas/`
- gRPC: defined in `proto/`, server in `internal/grpc/`
- CLI: `cmd/cli/main.go`

Agents must validate input through the schema layer before any business logic runs.
