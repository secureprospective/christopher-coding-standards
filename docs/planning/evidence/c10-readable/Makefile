# Active owner-selected project venv/tools; no implicit downloads or remote resolvers.
.PHONY: lint fmt format-check typecheck test test-coverage sca mutation-report

lint:
	ruff check .

fmt:
	ruff format .
	ruff check --fix .

format-check:
	ruff format --check .

typecheck:
	mypy src tests

test:
	pytest -v

COVERAGE_THRESHOLD ?= 80

test-coverage:
	pytest --cov --cov-report=term-missing --cov-fail-under=$(COVERAGE_THRESHOLD)

# Reference graph only; consumer supplies its actual reviewed full requirements lock.
sca:
	pip-audit --disable-pip --no-deps -r requirements-reference.lock

# Optional mutmut3 config-driven report; inspect survivors/untested/errors/timeouts.
# Successful tool execution is NOT an all-killed result or acceptance gate.
mutation-report:
	mutmut run --max-children 1
	mutmut results
