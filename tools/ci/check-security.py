"""Run selected actual security commands; do not confuse scope with complete safety."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def observe(cwd, argv, inputs, diagnostic=None, *, private_record=None):
    if private_record is not None:
        private_record = private_record.resolve()
        if private_record.is_relative_to(ROOT):
            raise ValueError("private security diagnostics must remain outside the checkout")
    command = [
        sys.executable,
        str(ROOT / "tools/verify_fixture.py"),
        "--timeout",
        "900",
        "--expect",
        "reject" if diagnostic else "pass",
    ]
    for name in inputs:
        command += ["--input", name]
    if diagnostic:
        command += ["--diagnostic", diagnostic]
    result = subprocess.run(command + ["--", *argv], cwd=cwd, capture_output=True, text=True)
    if private_record is None:
        print(result.stdout, end="", flush=True)
        print(result.stderr, end="", file=sys.stderr, flush=True)
    else:
        captured = json.dumps(
            {"checker_exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr},
            indent=2,
        ) + "\n"
        with private_record.open("x") as stream:
            stream.write(captured)
        print(
            json.dumps(
                {
                    "private_observation": str(private_record),
                    "sha256": hashlib.sha256(private_record.read_bytes()).hexdigest(),
                    "checker_exit": result.returncode,
                }
            ),
            flush=True,
        )
    if result.returncode != 0:
        raise RuntimeError(
            f"security expectation failed: {argv!r}; checker exit {result.returncode}"
        )
    return json.loads(result.stdout)


def rule_configs():
    from rules_identity import identity  # Selected Semgrep environment supplies safe YAML.

    configured = os.environ.get("CODING_STANDARDS_SEMGREP_RULES_DIR")
    if not configured:
        raise ValueError("missing installed private Semgrep rule directory")
    folder = Path(configured).resolve()
    if folder.is_relative_to(ROOT):
        raise ValueError("licensed rules must remain outside the publication checkout")
    manifest = json.loads((ROOT / "tools/ci/rules/MANIFEST.json").read_text())
    selected = {"semgrep-security-audit.yml", "semgrep-secrets.yml", "semgrep-owasp-top-ten.yml"}
    if {r["path"] for r in manifest["files"]} != selected or len(manifest["files"]) != 3:
        raise ValueError("expected exact three selected vendor policy inputs")
    result = []
    for record in manifest["files"]:
        path = (folder / record["path"]).resolve()
        if not path.is_relative_to(folder) or path.is_relative_to(ROOT):
            raise ValueError(
                "private vendor policy file must stay within its outside-checkout directory"
            )
        observed = identity(path)
        if (
            observed["rule_map_sha256"] != record["rule_map_sha256"]
            or observed["rules"] != record["rules"]
        ):
            raise ValueError(
                "vendor complete rule map differs from reviewed reference: " + path.name
            )
        result.append(path)
    return sorted(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["gitleaks", "semgrep", "trivy"])
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    if args.mode == "semgrep" and work.is_relative_to(ROOT):
        raise ValueError("Semgrep work directory must remain outside the publication checkout")
    work.mkdir(parents=True, exist_ok=False)
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")[:-1]
    if not tracked:
        raise ValueError("missing tracked source inventory; scan not verified")
    if args.mode == "gitleaks":
        shallow = subprocess.check_output(
            ["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, text=True
        ).strip()
        if shallow != "false":
            raise ValueError(
                "Git history scan requires non-shallow checkout; configure fetch-depth: 0"
            )
        observe(
            ROOT,
            [
                "gitleaks",
                "git",
                "--redact",
                "--no-banner",
                "--config",
                ".gitleaks.toml",
                "--log-opts=--all",
                ".",
            ],
            tracked,
        )
        observe(
            ROOT,
            ["gitleaks", "dir", "--redact", "--no-banner", "--config", ".gitleaks.toml", "."],
            tracked,
        )
        (work / "gitleaks.toml").write_text(
            '[extend]\nuseDefault=true\n[[rules]]\nid="bee-ci-harmless-canary"\ndescription="Harmless staged/directory rule-wiring control, not a credential"\nregex="BEE_CI_HARMLESS_CANARY"\nkeywords=["BEE_CI_HARMLESS_CANARY"]\n'
        )
        (work / "probe.txt").write_text("ordinary harmless fixture\n")
        command = [
            "gitleaks",
            "dir",
            "--redact",
            "--no-banner",
            "--verbose",
            "--config",
            "gitleaks.toml",
            "probe.txt",
        ]
        observe(work, command, ["gitleaks.toml", "probe.txt"])
        (work / "probe.txt").write_text("BEE_CI_HARMLESS_CANARY\n")
        observe(work, command, ["gitleaks.toml", "probe.txt"], "bee-ci-harmless-canary")
    elif args.mode == "semgrep":
        configs = rule_configs()
        command = [
            "semgrep",
            "scan",
            "--strict",
            "--error",
            "--metrics=off",
            "--disable-version-check",
            "--no-rewrite-rule-ids",
        ]
        for config in configs:
            command += ["--config", str(config)]
        # Deliberately invalid controls and immutable research/SDK payloads are data,
        # not active production source. Everything else remains in scope.
        exclusions = [
            "--exclude",
            "docs/planning/evidence/**",
            "--exclude",
            "scratch/fixtures/**",
            "--exclude",
            "_ci/**",
        ]
        # Licensed policy bytes remain in the private tool prefix, outside this
        # checkout; source targets require no vendor-file exemption.
        observe(
            ROOT,
            command + exclusions + ["."],
            tracked,
            private_record=work / "semgrep-root-private.json",
        )
        (work / "probe.py").write_text("def calculate(payload: str):\n    return eval(payload)\n")
        inputs = ["probe.py"]
        # Bind exact policy bytes within the control workspace too.
        for config in configs:
            shutil.copyfile(config, work / config.name)
            inputs.append(config.name)
        control = [
            "semgrep",
            "scan",
            "--strict",
            "--error",
            "--metrics=off",
            "--disable-version-check",
            "--no-rewrite-rule-ids",
        ]
        for config in configs:
            control += ["--config", config.name]
        observe(
            work,
            control + ["probe.py"],
            inputs,
            "python.lang.security.audit.eval-detected.eval-detected",
            private_record=work / "semgrep-rejection-private.json",
        )
        (work / "probe.py").write_text("def calculate(payload: str):\n    return int(payload)\n")
        observe(
            work,
            control + ["probe.py"],
            inputs,
            private_record=work / "semgrep-safe-private.json",
        )
    else:
        references = work / "references"
        # Fixed trusted kit executable/argv; resolved absolute output path is a
        # literal argument, not a command/option/shell. Caller owns the workspace.
        subprocess.run(
            # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
            [
                sys.executable,
                str(ROOT / "tools/ci/check-reference.py"),
                "sca-prepare",
                "--work",
                str(references),
            ],
            check=True,
        )
        report = work / "trivy-results.json"
        inputs = [
            str(p.relative_to(references))
            for p in references.rglob("*")
            if p.is_file()
            and "node_modules" not in p.relative_to(references).parts
            and p.suffix in {".json", ".yaml", ".txt", ".mod", ".sum"}
        ]
        command = [
            "trivy",
            "fs",
            "--cache-dir",
            str(work / "cache"),
            "--scanners",
            "vuln",
            "--include-dev-deps",
            "--severity",
            "HIGH,CRITICAL",
            "--exit-code",
            "1",
            "--list-all-pkgs",
            "--format",
            "json",
            "--skip-dirs",
            "typescript/node_modules",
        ]
        observe(references, command + ["--output", str(report), "."], inputs)
        data = json.loads(report.read_text())
        results = data.get("Results", [])
        types = {result.get("Type") for result in results if result.get("Packages")}
        expected = {
            "go/go.mod": "gomod",
            "python/requirements.txt": "pip",
            "semgrep-tool/requirements.txt": "pip",
            "typescript/pnpm-lock.yaml": "pnpm",
        }
        recognized = {r.get("Target"): r.get("Type") for r in results if r.get("Packages")}
        if any(recognized.get(path) != kind for path, kind in expected.items()):
            raise ValueError(
                f"required four lock graphs not recognized with actual packages: {recognized}"
            )
        # Passive dev-dependency lock data only: no package install or execution.
        # Reuse precisely the root scan's DB; current HIGH/CRITICAL policy stays on.
        db = work / "cache/db/trivy.db"
        with db.open("rb") as stream:
            db_before = hashlib.file_digest(stream, "sha256").hexdigest()
        controls = []
        for label, version, diagnostic in [
            ("vulnerable", "4.17.20", "CVE-2021-23337"),
            ("fixed", "4.18.0", None),
        ]:
            control = work / ("trivy-" + label)
            control.mkdir()
            for name in ["package.json", "pnpm-lock.yaml"]:
                shutil.copyfile(
                    ROOT / "tools/ci/fixtures" / ("trivy-" + label) / name, control / name
                )
            record = observe(
                control,
                command + ["--skip-db-update", "."],
                ["package.json", "pnpm-lock.yaml"],
                diagnostic,
            )
            payload = json.loads(record["stdout"])
            graph = [
                r
                for r in payload.get("Results", [])
                if r.get("Target") == "pnpm-lock.yaml" and r.get("Type") == "pnpm"
            ]
            if len(graph) != 1 or not any(
                p.get("Name") == "lodash" and p.get("Version") == version
                for p in graph[0].get("Packages", [])
            ):
                raise ValueError("passive Trivy control package/version graph was not recognized")
            findings = graph[0].get("Vulnerabilities", [])
            if diagnostic and not any(
                v.get("VulnerabilityID") == diagnostic
                and v.get("PkgName") == "lodash"
                and v.get("InstalledVersion") == version
                and v.get("Severity") == "HIGH"
                for v in findings
            ):
                raise ValueError(
                    "Trivy rejection lacks the expected advisory/package/version/HIGH finding"
                )
            if not diagnostic and findings:
                raise ValueError("fixed Trivy control still reports selected vulnerabilities")
            controls.append(
                {
                    "label": label,
                    "version": version,
                    "expected_advisory": diagnostic,
                    "exit_code": record["exit_code"],
                    "matched": record["matched"],
                }
            )
        with db.open("rb") as stream:
            db_after = hashlib.file_digest(stream, "sha256").hexdigest()
        if db_before != db_after:
            raise ValueError("Trivy database changed between root and passive controls")
        print(
            json.dumps(
                {
                    "passive_controls": controls,
                    "db_sha256_before_controls": db_before,
                    "db_sha256_after_controls": db_after,
                    "recognized_types": sorted(types),
                    "packages": sum(len(r.get("Packages", [])) for r in results),
                    "report": str(report),
                    "limits": "Selected recognized graphs/HIGH+CRITICAL current DB only; not all dependencies/platforms/advisories/security.",
                }
            ),
            flush=True,
        )
    print(
        json.dumps(
            {
                "completed_security_mode": args.mode,
                "limits": "Actual CLI scope and narrow controls; not hosted run, authenticated approval or complete safety.",
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
