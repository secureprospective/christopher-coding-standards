# Fixture check support (kit maintainers)

Use existing `scratch/fixtures/` inputs before adding cases. Run product/tool tests only in the owner-approved suitable environment on copied candidate files—not on an unapproved host or live consumer. These tools are not a default consumer payload.

`verify_fixture.py` is a Python3.10+ stdlib CLI. It runs one **trusted caller-selected argv**, without a shell and with closed stdin, and records declared workspace-relative files before/after. A matched expectation requires:

- **pass:** tool exit0 and unchanged input fingerprints;
- **reject:** tool exit1, unchanged inputs and a required nonblank literal tool diagnostic in captured stdout/stderr.

Use the tool's documented violation status/diagnostic. Exit2, missing executables/config/inputs, wrong markers, unexpected green and timeout cannot stand in for intended rejection. This narrow checker supports tools whose clean/violation statuses are0/1; others need explicit assessment, not an invented mapping.

## Representative commands

In the approved fixture copy, with the selected ShellCheck version on PATH:

```sh
python3 -m unittest discover -s tools/tests -v
python3 tools/verify_fixture.py --expect pass \
  --input tools/verify_fixture.py --input scratch/fixtures/bash/clean.sh \
  -- env -u SHELLCHECK_OPTS shellcheck --norc scratch/fixtures/bash/clean.sh
python3 tools/verify_fixture.py --expect reject --diagnostic 'SC2086 (info):' \
  --input tools/verify_fixture.py --input scratch/fixtures/bash/violating.sh \
  -- env -u SHELLCHECK_OPTS shellcheck --norc scratch/fixtures/bash/violating.sh
```

These Linux examples disable ambient ShellCheck options/config; assess explicit project config separately. Tool identity/version and all relevant copied inputs belong in the independent copy manifest.

Checker exit0 means the stated expectation matched, **not** that the negative fixture is valid production code or the whole overlay passed. Exit1 means a completed command did not match; exit2 means usage/setup/execution trouble. Usage errors use argparse stderr; executed/setup attempts emit JSON. Do not catch arbitrary checker failure as an intended negative pass.

JSON retains command, timeout, expected/observed status, declared-input SHA256 snapshots, decoded stdout/stderr, error and match result. Output decodes UTF-8 with replacement for invalid bytes; it is not a byte-perfect log. Keep it with environment/tool versions, copy manifest and candidate identity. Avoid credentials/private input/output. A matching editable record authenticates neither approval nor tool identity.

## Limits and ownership

Select all relevant source/config/lock/test inputs and verify copied bytes independently. Input paths must be relative regular files resolving inside the workspace; hashes establish only declared snapshots, not every file the tool read or absence of transient mutation. Tools can still read/write undeclared files or create caches. Caller owns trusted commands, dependency provenance/installation and fixture isolation; this is not a sandbox, updater or automatic assembler.

`--timeout` is finite positive seconds (default120); it limits the direct command, not arbitrary descendant processes. Use appropriate tool-native/process controls for commands that spawn work. No automatic system install, GUI launch, service change, global configuration or repo relocation. Test trees/tool binaries belong in an approved isolated workspace. Preserve computer-use and other agents' files.

Unit tests simulate tool outputs to exercise the checker contract; they are not ShellCheck evidence. The representative real-tool pair uses existing Bash fixtures and a verified official ShellCheckv0.11.0 archive, matching the legacy pinned overlay version. C4 must independently verify actual Bash helpers/Bats/lint behavior. Python/Go/other overlays, Gitleaks/shfmt, tool compatibility and workflow wiring need their own gates. No existing workflow is fixed merely because this CLI exists.
