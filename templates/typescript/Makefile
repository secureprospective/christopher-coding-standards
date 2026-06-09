# Makefile — thin wrapper for standard project commands.
# Provides a consistent interface regardless of package manager (pnpm, npm, yarn).
# All targets map directly to package.json scripts.

.PHONY: lint lint-fix format typecheck test test-watch test-coverage mutation-test mutation-test-full

lint:
	pnpm lint

lint-fix:
	pnpm lint:fix

format:
	pnpm format

typecheck:
	pnpm typecheck

test:
	pnpm test

test-watch:
	pnpm test:watch

test-coverage:
	pnpm test:coverage

mutation-test:
	pnpm mutation-test

# Full mutation scan — no incremental filter. Use for the weekly cron.
mutation-test-full:
	pnpm mutation-test:full
