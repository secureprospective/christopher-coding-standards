# Python — validated shapes, typed callers and observed checks

Adopt the [core contract](../../docs/quality-contract.md), preserving consumer project/dependency/test rules. Current status is [HANDOFF](../../HANDOFF.md), not historical phases. Ruff checks selected style/bug/security rules; mypy checks types, not runtime validity. Pydantic validates selected shape/constraints, not permission or all possible states.

## Compose an owner-selected environment

Tested reference Python3.13.5/Linux x86_64, Ruff0.16.0/mypy2.3.0/Pydantic2.14.0/pytest9.1.1/cov7.1.0/pip-audit2.10.1/mutmut3.8.0. `requirements-reference.lock` is the complete **selected Linux/CPython3.13 wheel graph**, with publisher SHA256 for each selected distribution; it is not all platform/Python locks or a mandate to upgrade existing applications. Preserve existing manager/pins; choose compatible tools and create/review an actual consumer lock deliberately. Pinned/hash-verified resolution is integrity evidence, not authenticated approval/universal safety/containment.

For this reference only, confirm the selected interpreter/platform, then:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --only-binary=:all: --require-hashes -r requirements-reference.lock
python -m pip check
```

Do not disable hashes or silently bootstrap tools when the reference wheel/platform does not fit. Select compatible consumer versions/distributions, review the whole graph and actually repeat checks instead. Optional mutation/report tooling can be omitted from the consumer graph if unneeded; do not assert the reference lock verifies a different graph. Installer bootstrap pip and unrelated/global packages are outside the locked graph audit.

Merge pyproject tool tables, hook entries and Make targets; do not overwrite project metadata, local exclusions or build/test decisions. Copy `schema/example.py` to src/schema/example.py and tests/test_example.py to tests/. Adapt package names/layout consistently. `mypy src tests` uses the actual project environment and Pydantic plugin (`init_typed=true`); it does not establish runtime semantic constraints. Tests are both typed and executed. `mutants/` is explicitly excluded generated output, not a production/SAST bypass guarantee. Type/lint caches may be written; read-only refers to checked source, not a filesystem sandbox.

```sh
make lint
make format-check
make typecheck
make test
make test-coverage
make sca
```

`make fmt` deliberately writes source; hooks never fix it automatically. Coverage includes configured src, namespace packages and branches (include_namespace_packages=true), default reference80% may be adapted deliberately; it is not correctness. Missing test discovery must reject, not an empty green. Audit checks the supplied full reference lock's reported vulnerabilities, not all bootstrap/installed packages or complete future safety.

Install pre-commit in an owner-selected compatible environment, activate project venv and verify the native scanner before `pre-commit install`. Local read-only Ruff/format/mypy hooks use the active project dependencies, not duplicate remote resolvers or isolated typing environments missing Pydantic. Native Gitleaks-system uses the owner's verified binary and immutable hook source; staged-Git scope, not whole-directory/complete detection. Missing dependencies must fail, not silently install/skip. Pins/hooks/green commits are not authenticated approval or containment.

## Boundary behavior and limits

RawPlayerRecord ignores provider-added fields; owned InternalPlayerUpdate forbids unknown fields. Owned clients are still untrusted, not automatically authorized. Raw strings normalize whitespace and require unsigned ASCII-decimal IDs, nonblank name/position and finite salary when present; blank salary/zero numeric ID/negative finite salary remain allowed. Python ID shape does **not** impose Go's platform-int range; domain conversion/range/permission belongs to the consumer. Internal updates reject blank position/invalid ID and trim strings. Reader/body limits and error redaction are separate; do not blindly log raw validation exceptions.

Use validated construction/model_validate/model_validate_json before domain/effects. Assignment validation catches selected bad reassignment, but `model_construct`, `model_copy(update=...)`, direct object manipulation and unvalidated inputs can bypass it. An invalid Pydantic object can exist: neither mypy nor the plugin makes runtime invalid states impossible. Shipped tests explicitly exhibit documented bypasses and a synthetic caller's rejection-before-effect; not application persistence/authentication proof.

## Exercise actual diagnostics

On an authorized disposable consumer, introduce one violation at a time, require the intended diagnostic, then restore. Pydantic ctor `RawPlayerRecord(id=42, name="Chris", position="QB")` must reject statically via plugin arg-type. A wrong typed assignment/untyped definition should trigger its named mypy diagnostic. Selected eval/shell/query hazards must trigger the actual Ruff rule; a formatter-only edit must reject without rewriting bytes. An intentional assertion and no discovered tests must fail. Exercise actual installed hooks and an ordinary clean commit, not source-only configuration or a passing echo. No generic fake AWS string is guaranteed to be detected by every scanner configuration; use an owner-selected harmless known rule probe and distinguish wiring from completeness.

## Optional mutation report, not an acceptance gate

Selected mutmut3 reads `[tool.mutmut]` source_paths and pytest_add_cli_args_test_selection; legacy `--paths-to-mutate`/tests_dir recipes are not this interface. Execute from the configured project (even CLI startup/help may load source configuration):

```sh
make mutation-report   # mutmut run --max-children 1; mutmut results
```

The reference generated three numeric-helper mutants, not mutations of all decorated Pydantic model validators; those three were killed by strong tests. A separate deliberately weak control had survivors despite status0, so it was not a quality pass. This generates mutants/reports and runs selected tests; status0 is tool completion, **not** all mutants killed, assertion quality or acceptance. Inspect actual killed/surviving/untested/timeout/error evidence, test adequacy/equivalent mutations and selected scope; reject unverified claims. It is optional and not a universal mutation/purity framework, fixed score ritual or default check. Other platforms/fork/tool/source patterns may need separate verification. Generated/cache mutations are not original-source rewriting or isolation guarantees.

No hosted execution/enforcement, live consumer enrollment, publication/fleet rollout, push/main merge/deploy, system/GUI/config changes or other platforms follows from this reference.
