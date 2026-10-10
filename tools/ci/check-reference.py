"""Exercise shipped reference inputs; records are observations, not hosted approval."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / source, target)


def prepare(stack, work):
    work.mkdir(parents=True, exist_ok=False)
    if stack == "typescript":
        for name in ["biome.json", "tsconfig.json", "vitest.config.ts", "stryker.config.mjs"]:
            copy("templates/typescript/" + name, work / name)
        copy("templates/typescript/package.json.snippet", work / "package.json")
        copy(
            "templates/typescript/scripts/check-package-manager.mjs",
            work / "scripts/check-package-manager.mjs",
        )
        for name in ["example.ts", "example.test.ts"]:
            copy("templates/typescript/schemas/" + name, work / "src/schemas" / name)
        copy("scratch/fixtures/typescript/pnpm-lock.yaml", work / "pnpm-lock.yaml")
    elif stack == "python":
        copy("templates/python/pyproject.toml.snippet", work / "pyproject.toml")
        copy("templates/python/schema/example.py", work / "src/schema/example.py")
        copy("templates/python/tests/test_example.py", work / "tests/test_example.py")
        copy("templates/python/requirements-reference.lock", work / "requirements-reference.lock")
        copy("templates/python/Makefile.snippet", work / "Makefile")
    elif stack == "go":
        for name in ["playerid", "schema", "tools/ifaceguard"]:
            shutil.copytree(ROOT / "templates/go" / name, work / name)
        copy("templates/go/.golangci.yml", work / ".golangci.yml")
        copy("templates/go/Makefile.snippet", work / "Makefile")
        (work / "go.mod").write_text("module reference\n\ngo 1.27.2\n")
    elif stack == "bash":
        for name in ["lib", "scripts", "tests"]:
            shutil.copytree(ROOT / "templates/bash" / name, work / name)
        copy("templates/bash/.shellcheckrc", work / ".shellcheckrc")
        copy("templates/bash/Makefile.snippet", work / "Makefile")
    else:
        raise ValueError("unknown reference stack")


def check(work, argv, diagnostic=None):
    excluded = {
        "node_modules",
        ".git",
        ".mypy_cache",
        ".ruff_cache",
        "coverage",
        "dist",
        "mutants",
        ".stryker-tmp",
    }
    # Fingerprint source/config/reference-lock/checker inputs, not tool caches or reports.
    inputs = sorted(
        str(p.relative_to(work))
        for p in work.rglob("*")
        if p.is_file()
        and not excluded.intersection(p.relative_to(work).parts)
        and (
            p.suffix
            in {
                ".py",
                ".ts",
                ".mjs",
                ".json",
                ".yml",
                ".yaml",
                ".toml",
                ".mod",
                ".sum",
                ".go",
                ".sh",
                ".bats",
                ".lock",
            }
            or p.name in {"Makefile", ".shellcheckrc"}
        )
    )
    command = [
        sys.executable,
        str(ROOT / "tools/verify_fixture.py"),
        "--timeout",
        "600",
        "--expect",
        "reject" if diagnostic else "pass",
    ]
    for name in inputs:
        command += ["--input", name]
    if diagnostic:
        command += ["--diagnostic", diagnostic]
    result = subprocess.run(command + ["--", *argv], cwd=work, capture_output=True, text=True)
    print(result.stdout, end="", flush=True)
    print(result.stderr, end="", file=sys.stderr, flush=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"fixture expectation failed: {argv!r}; checker exit {result.returncode}"
        )


def typescript_type_rejection(work):
    # tsc's observed diagnostic status is2, outside C3's deliberately narrow0/1
    # contract. Assess this named command directly; never normalize arbitrary errors.
    inputs = sorted(
        p
        for p in work.rglob("*")
        if p.is_file()
        and "node_modules" not in p.relative_to(work).parts
        and p.suffix in {".ts", ".json", ".yaml", ".mjs", ".py"}
    )

    def snapshot():
        return {
            str(p.relative_to(work)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs
        }

    before = snapshot()
    argv = ["pnpm", "run", "typecheck"]
    result = subprocess.run(
        argv, cwd=work, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600
    )
    after = snapshot()
    matched = (
        result.returncode == 2
        and "TS2322" in result.stdout + "\n" + result.stderr
        and before == after
    )
    print(
        json.dumps(
            {
                "command": argv,
                "expected_status": 2,
                "diagnostic": "TS2322",
                "exit_code": result.returncode,
                "inputs_before": before,
                "inputs_after": after,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "matched": matched,
            }
        ),
        flush=True,
    )
    if not matched:
        raise RuntimeError("named TypeScript diagnostic/status/input expectation failed")


def controls(stack, work):
    fixture = work / ".controls"
    fixture.mkdir()
    if stack == "python":
        for name in ["clean.py", "violating.py"]:
            copy("scratch/fixtures/" + name, fixture / name)
        check(work, ["ruff", "check", "--config", "pyproject.toml", ".controls/clean.py"])
        check(work, ["mypy", "--config-file", "pyproject.toml", ".controls/clean.py"])
        check(
            work, ["ruff", "check", "--config", "pyproject.toml", ".controls/violating.py"], "S608"
        )
        check(
            work,
            ["mypy", "--config-file", "pyproject.toml", ".controls/violating.py"],
            "[no-untyped-def]",
        )
    elif stack == "bash":
        for name in ["clean.sh", "violating.sh"]:
            copy("scratch/fixtures/bash/" + name, fixture / name)
        check(work, ["shellcheck", ".controls/clean.sh"])
        check(work, ["shfmt", "-d", "-i", "2", "-ci", "-sr", ".controls/clean.sh"])
        check(work, ["shellcheck", ".controls/violating.sh"], "SC2086")
        check(
            work,
            ["shfmt", "-d", "-i", "2", "-ci", "-sr", ".controls/violating.sh"],
            "violating.sh.orig",
        )
    elif stack == "go":
        for name in ["clean.go", "violating.go"]:
            copy("scratch/fixtures/go/" + name, fixture / name)
        with tempfile.TemporaryDirectory(prefix="ifaceguard.", dir="/tmp") as binary_dir:
            binary = str(Path(binary_dir) / "ifaceguard")
            check(
                work / "tools/ifaceguard",
                ["go", "build", "-mod=readonly", "-o", binary, "./cmd/ifaceguard"],
            )
            for name, diagnostic in [("clean.go", None), ("violating.go", "errcheck")]:
                check(
                    work,
                    ["golangci-lint", "run", "--config", ".golangci.yml", ".controls/" + name],
                    diagnostic,
                )
            check(work, ["go", "vet", "-vettool=" + binary, ".controls/clean.go"])
            check(
                work,
                ["go", "vet", "-vettool=" + binary, ".controls/violating.go"],
                "exported func BadSignature: result uses the empty interface",
            )
    else:
        raise ValueError("unknown control stack")
    for p in sorted(fixture.iterdir()):
        check(work, ["gitleaks", "dir", "--no-banner", "--redact", str(p.relative_to(work))])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode", choices=["ts-lint", "ts-test", "python", "go", "bash", "sca-prepare"]
    )
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    stack = "typescript" if args.mode.startswith("ts-") else args.mode
    if args.mode == "sca-prepare":
        work.mkdir(parents=True, exist_ok=False)
        prepare("typescript", work / "typescript")
        check(work / "typescript", ["pnpm", "install", "--frozen-lockfile"])
        copy("templates/python/requirements-reference.lock", work / "python/requirements.txt")
        copy("tools/ci/requirements-semgrep.lock", work / "semgrep-tool/requirements.txt")
        for name in ["go.mod", "go.sum"]:
            copy("templates/go/tools/ifaceguard/" + name, work / "go" / name)
        return
    prepare(stack, work)
    if stack == "typescript":
        check(work, ["pnpm", "install", "--frozen-lockfile"])
        if args.mode == "ts-lint":
            check(work, ["pnpm", "run", "lint"])
            check(work, ["pnpm", "run", "typecheck"])
            probe = work / "src/probe.ts"
            try:
                probe.write_text("export const value: string = 42;\n")
                typescript_type_rejection(work)
            finally:
                probe.unlink(missing_ok=True)
            check(work, ["pnpm", "run", "typecheck"])
        else:
            check(work, ["pnpm", "run", "test:coverage"])
            probe = work / "src/probe.test.ts"
            try:
                probe.write_text(
                    'import { expect, test } from "vitest";\ntest("intended CI assertion probe", () => { expect(1).toBe(2); });\n'
                )
                check(work, ["pnpm", "run", "test"], "AssertionError: expected 1 to be 2")
            finally:
                probe.unlink(missing_ok=True)
            check(work, ["pnpm", "run", "test"])
    elif stack == "python":
        for command in [["make", "lint", "format-check", "typecheck"], ["make", "test-coverage"]]:
            check(work, command)
        controls(stack, work)
    elif stack == "bash":
        check(work, ["make", "lint", "test"])
        controls(stack, work)
    elif stack == "go":
        check(work, ["make", "lint", "format-check", "vet", "build", "test-coverage"])
        check(work / "tools/ifaceguard", ["go", "mod", "verify"])
        check(work / "tools/ifaceguard", ["go", "test", "./..."])
        controls(stack, work)
    print(
        json.dumps(
            {
                "completed_mode": args.mode,
                "work": str(work),
                "limits": "Actual trusted copied reference commands; not hosted execution, sandbox, live consumer or approval.",
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
