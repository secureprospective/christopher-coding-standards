"""Actual bounded setup/matcher negatives on owned copies; not product approvals."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess

assert platform.node() == "claudeos" and os.getuid() == 1000
root = Path.home() / "coding-standards-verification/bee-c12-2026-10-09"
kit = root / "kit with spaces"
records = []
base_env = os.environ | json.loads((root / "installed-final-bash/environment.json").read_text())
node_env = os.environ | json.loads((root / "installed-final-ts-lint/environment.json").read_text())
sem_env = os.environ | json.loads((root / "installed-semgrep-private-rule-map/environment.json").read_text())


def run(label, argv, expected, marker=None, cwd=kit, env=base_env):
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=180)
    record = {"label": label, "argv": argv, "cwd": str(cwd), "status": p.returncode, "expected_status": expected, "required_marker": marker, "stdout": p.stdout, "stderr": p.stderr, "matched": p.returncode == expected and (marker is None or marker in p.stdout + "\n" + p.stderr)}
    records.append(record)
    (root / "results/guard-checks.json").write_text(json.dumps(records, indent=2) + "\n")
    assert record["matched"], label
    return p


checker = ["python3", "tools/verify_fixture.py", "--expect", "reject", "--diagnostic"]
for label, marker, fixture in [("unexpected clean is not rejection", "SC2086", "clean.sh"), ("wrong marker is not rejection", "BEE_WRONG_MARKER", "violating.sh")]:
    run(label, checker + [marker, "--input", "scratch/fixtures/bash/" + fixture, "--", "shellcheck", "scratch/fixtures/bash/" + fixture], 1, '"matched": false')
run("missing tool is not rejection", checker + ["SC2086", "--input", "scratch/fixtures/bash/clean.sh", "--", "bee_missing_ci_binary_123"], 2, "No such file or directory")
run("missing input is not rejection", checker + ["SC2086", "--input", "scratch/fixtures/bash/missing-input.sh", "--", "shellcheck", "scratch/fixtures/bash/clean.sh"], 2, "input must resolve to a file")

spec = importlib.util.spec_from_file_location("own_reference", kit / "tools/ci/check-reference.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
work = root / "guard-reference-repeat with spaces"
module.prepare("typescript", work)
(work / "pnpm-lock.yaml").unlink()  # Owned new reference only; deliberately absent binding.
run("absent lock with selected overrides fails frozen config validation", ["pnpm", "install", "--frozen-lockfile"], 1, "ERR_PNPM_LOCKFILE_CONFIG_MISMATCH", cwd=work, env=node_env)
run("npm does not bypass shipped manager guard", ["npm", "run", "preinstall"], 1, "pnpm@10.34.3", cwd=work, env=node_env)

private = root / "guard-own-rule-data"
private.mkdir()
for name in ["semgrep-security-audit.yml", "semgrep-secrets.yml", "semgrep-owasp-top-ten.yml"]:
    (private / name).write_text('{"rules":[{"id":"own-canary","pattern":"own-value","languages":["python"],"message":"own","severity":"WARNING"}]}\n')
run("changed complete rule map fails", ["python3", "tools/ci/check-security.py", "semgrep", "--work", str(root / "guard-rule-mismatch-work")], 1, "vendor complete rule map differs", env=sem_env | {"CODING_STANDARDS_SEMGREP_RULES_DIR": str(private)})
without = sem_env.copy()
without.pop("CODING_STANDARDS_SEMGREP_RULES_DIR", None)
run("missing private rule binding fails", ["python3", "tools/ci/check-security.py", "semgrep", "--work", str(root / "guard-rule-missing-work")], 1, "missing installed private Semgrep rule directory", env=without)
run("private rules cannot be in publication checkout", ["python3", "tools/ci/check-security.py", "semgrep", "--work", str(root / "guard-rule-public-work")], 1, "licensed rules must remain outside", env=sem_env | {"CODING_STANDARDS_SEMGREP_RULES_DIR": str(kit / "tools/ci/rules")})

code = "import importlib.util,sys;from pathlib import Path;s=importlib.util.spec_from_file_location('own_install',Path('tools/ci/install-tools.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);v=m.TOOLS['gitleaks'];m.TOOLS['gitleaks']=(v[0],'0'*64,v[2]);sys.argv=['install-tools.py','gitleaks','--directory',sys.argv[1]];m.main()"
run("bad native archive checksum blocks installation", ["python3", "-c", code, str(root / "guard-checksum-prefix")], 1, "gitleaks: archive checksum mismatch")
print("10 bounded actual guard observations matched; intended setup/matcher failures are not tool-quality passes")
