"""Install only selected Linux-x86_64 CI tools into a new caller-owned directory."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
TOOLS = {
    "shellcheck": (
        "https://github.com/koalaman/shellcheck/releases/download/v0.11.0/shellcheck-v0.11.0.linux.x86_64.tar.xz",
        "8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198",
        "shellcheck-v0.11.0/shellcheck",
    ),
    "shfmt": (
        "https://github.com/mvdan/sh/releases/download/v3.13.1/shfmt_v3.13.1_linux_amd64",
        "fb096c5d1ac6beabbdbaa2874d025badb03ee07929f0c9ff67563ce8c75398b1",
        None,
    ),
    "gitleaks": (
        "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz",
        "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb",
        "gitleaks",
    ),
    "golangci-lint": (
        "https://github.com/golangci/golangci-lint/releases/download/v2.14.0/golangci-lint-2.14.0-linux-amd64.tar.gz",
        "ab90aeb7b066f92a33415b638a50fe5344bbb75a0d32ad30cc248d88f81032ab",
        "golangci-lint-2.14.0-linux-amd64/golangci-lint",
    ),
    "go": (
        "https://go.dev/dl/go1.27.2.linux-amd64.tar.gz",
        "ecbadb99091a3f46e31f5f934b068b1864eafa7995211b39eaddf76996045fe5",
        "*",
    ),
    "bats": (
        "https://github.com/bats-core/bats-core/archive/eb7f42f8d608ac693d7a4b67474f6714ea68cfc5.tar.gz",
        "845574549f4c9777bf02fcdf307f1bf347d40c66920fb6b47dcc8fdfa065ac39",
        "*",
    ),
    "pnpm": (
        "https://registry.npmjs.org/pnpm/-/pnpm-10.34.3.tgz",
        "1c40544020a2e633068ed43a98eb5c0fed7d64a1c6d6f2382e43df91419dad62",
        "*",
    ),
    "trivy": (
        "https://github.com/aquasecurity/trivy/releases/download/v0.75.0/trivy_0.75.0_Linux-64bit.tar.gz",
        "c6e65abddb348e25f10549df887045629cf28cc72453cd1c63acb717316b3f3f",
        "trivy",
    ),
}
GROUPS = {
    "bash": ["shellcheck", "shfmt", "gitleaks", "bats"],
    "go": ["go", "golangci-lint", "gitleaks"],
    "python": ["gitleaks"],
    "typescript": ["pnpm"],
    "gitleaks": ["gitleaks"],
    "semgrep": [],
    "trivy": ["trivy", "pnpm"],
}


def github_environment(environment):
    if "GITHUB_PATH" in os.environ:
        # The runner prepends each line; emit reverse order to preserve PATH priority.
        with open(os.environ["GITHUB_PATH"], "a") as stream:
            stream.write("\n".join(reversed(environment["PATH"].split(os.pathsep))) + "\n")
        with open(os.environ["GITHUB_ENV"], "a") as stream:
            stream.write("".join(k + "=" + v + "\n" for k, v in environment.items() if k != "PATH"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=GROUPS)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    if (
        platform.system() != "Linux"
        or platform.machine() != "x86_64"
        or sys.version_info[:2] != (3, 13)
    ):
        parser.error("selected installation reference requires Linux x86_64 CPython3.13")
    dest = args.directory.resolve()
    if args.group == "semgrep" and dest.is_relative_to(ROOT):
        raise ValueError("licensed rule prefix must remain outside the publication checkout")
    dest.mkdir(parents=True, exist_ok=False)  # No overwrites of existing trees.
    bin_dir = dest / "bin"
    bin_dir.mkdir()
    environment = {
        "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
        "PIP_CACHE_DIR": str(dest / "cache/pip"),
        "npm_config_store_dir": str(dest / "cache/pnpm"),
        "TMPDIR": str(dest / "tmp"),
        "XDG_CACHE_HOME": str(dest / "cache"),
        "GOENV": "off",
        "GOTOOLCHAIN": "local",
        "GOPATH": str(dest / "gopath"),
        "GOMODCACHE": str(dest / "cache/go-mod"),
        "GOCACHE": str(dest / "cache/go-build"),
    }
    (dest / "tmp").mkdir()
    records = []
    for name in GROUPS[args.group]:
        url, digest, member = TOOLS[name]
        request = urllib.request.Request(url, headers={"User-Agent": "coding-standards-ci"})
        # Trusted maintainer-selected constant HTTPS URLs above, never a user URL.
        # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"{name}: archive checksum mismatch")
        archive = dest / (name + ".download")
        archive.write_bytes(data)
        if member is None:
            (bin_dir / name).write_bytes(data)
        else:
            with tarfile.open(archive) as tf:
                if member == "*":
                    tf.extractall(dest / name, filter="data")
                else:
                    stream = tf.extractfile(member)
                    if stream is None:
                        raise ValueError(f"{name}: missing regular archive member")
                    (bin_dir / name).write_bytes(stream.read())
        if member != "*":
            (bin_dir / name).chmod(0o755)
        elif name == "go":
            environment["PATH"] = str(dest / "go/go/bin") + os.pathsep + environment["PATH"]
            environment["GOROOT"] = str(dest / "go/go")
        elif name == "bats":
            environment["PATH"] = (
                str(dest / "bats/bats-core-eb7f42f8d608ac693d7a4b67474f6714ea68cfc5/bin")
                + os.pathsep
                + environment["PATH"]
            )
        elif name == "pnpm":
            wrapper = (
                '#!/usr/bin/env python3\nimport os,sys\nos.execvp("node", ["node", '
                + repr(str(dest / "pnpm/package/bin/pnpm.cjs"))
                + ", *sys.argv[1:]])\n"
            )
            (bin_dir / "pnpm").write_text(wrapper)
            (bin_dir / "pnpm").chmod(0o755)
        records.append({"tool": name, "url": url, "archive_sha256": digest})
    if args.group in {"python", "semgrep"}:
        venv = dest / "venv"
        # Fixed argv; caller-owned resolved absolute output path is one literal argument,
        # not a shell/program/option. This CLI is not an untrusted network service.
        # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        lock = ROOT / (
            "templates/python/requirements-reference.lock"
            if args.group == "python"
            else "tools/ci/requirements-semgrep.lock"
        )
        # Fixed selected executable/flags and source-owned complete hashed lock;
        # all paths are absolute literals, no shell or dynamic command selection.
        subprocess.run(
            # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
            [
                str(venv / "bin/python"),
                "-m",
                "pip",
                "install",
                "--require-hashes",
                "--only-binary=:all:",
                "-r",
                str(lock),
            ],
            env=os.environ | environment,
            check=True,
        )
        environment["PATH"] = str(venv / "bin") + os.pathsep + environment["PATH"]
    if args.group == "semgrep":
        # License permits internal use, not rule redistribution: keep exact bytes
        # in the private tool prefix, never in the checkout or published artifacts.
        rules_dir = dest / "rules"
        rules_dir.mkdir()
        manifest = json.loads((ROOT / "tools/ci/rules/MANIFEST.json").read_text())
        selected = {
            "semgrep-security-audit.yml",
            "semgrep-secrets.yml",
            "semgrep-owasp-top-ten.yml",
        }
        if {r["path"] for r in manifest["files"]} != selected or len(manifest["files"]) != 3:
            raise ValueError("expected exact three selected private vendor policy inputs")
        for record in manifest["files"]:
            url = "https://semgrep.dev/c/p/" + record["path"][8:-4]
            if record["source"] != url:
                raise ValueError("unexpected vendor policy locator")
            # Only these three fixed HTTPS locators, never a caller-selected URL.
            # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
            with urllib.request.urlopen(url, timeout=120) as response:
                data = response.read()
            policy = rules_dir / record["path"]
            policy.write_bytes(data)  # Preserve actual raw bytes, including failed observations.
            # Fixed selected interpreter/helper and one private absolute data path; no shell.
            observed = json.loads(
                subprocess.check_output(
                    # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
                    [
                        str(venv / "bin/python"),
                        str(ROOT / "tools/ci/rules_identity.py"),
                        str(policy),
                    ],
                    text=True,
                )
            )
            if (
                observed["rule_map_sha256"] != record["rule_map_sha256"]
                or observed["rules"] != record["rules"]
            ):
                raise ValueError("vendor complete-rule-map checksum mismatch: " + record["path"])
            records.append(
                {
                    "private_policy": record["path"],
                    "url": url,
                    "original_reference_raw_sha256": record["sha256"],
                    **observed,
                }
            )
        environment["CODING_STANDARDS_SEMGREP_RULES_DIR"] = str(rules_dir)
    (dest / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    (dest / "downloads.json").write_text(json.dumps(records, indent=2) + "\n")
    github_environment(environment)
    print(
        json.dumps(
            {"directory": str(dest), "environment": environment, "downloads": records}, indent=2
        )
    )


if __name__ == "__main__":
    main()
