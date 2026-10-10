# Thin package.json wrappers. Merge targets; don't replace a project's Makefile.
# npm/Bun consumers must also compose their own manifest/guard/lock contract.
PM ?= pnpm

.PHONY: lint lint-fix format format-check typecheck test test-watch test-coverage mutation-test mutation-test-full

lint:
	$(PM) run lint

lint-fix:
	$(PM) run lint:fix

format:
	$(PM) run format

format-check:
	$(PM) run format:check

typecheck:
	$(PM) run typecheck

test:
	$(PM) run test

test-watch:
	$(PM) run test:watch

test-coverage:
	$(PM) run test:coverage

mutation-test:
	$(PM) run mutation-test

mutation-test-full:
	$(PM) run mutation-test:full

# Merge with the base Makefile; preserve the project's package-manager contract.
PM ?= pnpm

.PHONY: format-astro lint-astro typecheck-astro
format-astro:
	$(PM) run format:astro

lint-astro:
	$(PM) run lint:astro

typecheck-astro:
	$(PM) run typecheck:astro
