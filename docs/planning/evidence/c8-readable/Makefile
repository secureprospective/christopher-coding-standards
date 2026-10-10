# Merge into the consumer Makefile. Optional profile checks are not default gates.
PM ?= bun

.PHONY: lint lint-fix format format-check typecheck test check-all check-deps check-file-length check-components
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

check-all:
	$(PM) run check:all

# Enable only after owner selects/tests the corresponding project-specific profile.
check-deps:
	$(PM) run check:deps

check-file-length:
	$(PM) run check:file-length

check-components:
	$(PM) run check:components
