"""Passive declared dev-lock vulnerability oracle; never install/execute the package."""

from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import urllib.request

assert platform.node() == "claudeos" and os.getuid() == 1000
root = Path.home() / "coding-standards-verification/bee-c12-2026-10-09"
work = root / "trivy-passive-cve-probe"
work.mkdir()
env = os.environ | json.loads((root / "installed-ready-trivy/environment.json").read_text())
cache = root / "checks-ready-trivy with spaces/cache"
db = cache / "db/trivy.db"
with db.open('rb') as stream:
    db_before = hashlib.file_digest(stream, 'sha256').hexdigest()
records = []
oracles = []
for url in ["https://api.github.com/advisories/GHSA-35jh-r3h4-6jhm", "https://registry.npmjs.org/lodash/4.17.20", "https://registry.npmjs.org/lodash/4.17.21"]:
    req = urllib.request.Request(url, headers={"User-Agent": "coding-standards-c12-source-oracle"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read();status = response.status
    value = json.loads(data)
    filename = 'advisory.json' if '/advisories/' in url else 'lodash-' + value['version'] + '-metadata.json'
    (work / filename).write_bytes(data)
    oracles.append({'url': url, 'http_status': status, 'path': str(work / filename), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
for label, version in [('vulnerable', '4.17.20'), ('fixed', '4.17.21')]:
    metadata = json.loads((work / ('lodash-' + version + '-metadata.json')).read_text())
    folder = work / label;folder.mkdir()
    package = {'private': True, 'name': 'own-passive-trivy-control', 'version': '0.0.0', 'devDependencies': {'lodash': version}}
    (folder / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
    lock = f"lockfileVersion: '9.0'\nsettings:\n  autoInstallPeers: true\n  excludeLinksFromLockfile: false\nimporters:\n  .:\n    devDependencies:\n      lodash:\n        specifier: {version}\n        version: {version}\npackages:\n  lodash@{version}:\n    resolution: {{integrity: {metadata['dist']['integrity']}}}\nsnapshots:\n  lodash@{version}: {{}}\n"
    (folder / 'pnpm-lock.yaml').write_text(lock)
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()}
    argv = ['trivy', 'fs', '--cache-dir', str(cache), '--skip-db-update', '--scanners', 'vuln', '--include-dev-deps', '--severity', 'HIGH,CRITICAL', '--exit-code', '1', '--list-all-pkgs', '--format', 'json', '.']
    p = subprocess.run(argv, cwd=folder, env=env, capture_output=True, text=True, timeout=180)
    record = {'label': label, 'argv': argv, 'cwd': str(folder), 'status': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr, 'inputs_before': before, 'inputs_after': {x.name: hashlib.sha256(x.read_bytes()).hexdigest() for x in folder.iterdir()}}
    records.append(record)
    (work / (label + '-report.json')).write_text(p.stdout)
    (root / 'results/trivy-passive-probe.json').write_text(json.dumps({'oracles': oracles, 'db_sha256_before': db_before, 'records': records, 'limits': 'Own passive declared-lock fixtures only; package archives not downloaded, installed or executed. Current selected cache DB reused; no universal security/approval claim.'}, indent=2) + '\n')
    report = json.loads(p.stdout)
    findings = [(v.get('VulnerabilityID'), v.get('PkgName'), v.get('InstalledVersion'), v.get('Severity')) for result in report.get('Results', []) for v in result.get('Vulnerabilities', [])]
    print(label, p.returncode, findings)
    assert record['inputs_before'] == record['inputs_after']
    if label == 'vulnerable':
        assert p.returncode == 1 and ('CVE-2021-23337', 'lodash', version, 'HIGH') in findings
    else:
        assert p.returncode == 0 and not findings
with db.open('rb') as stream:
    db_after = hashlib.file_digest(stream, 'sha256').hexdigest()
assert db_before == db_after
print('Passive lodash dev lock HIGH/CVE reject1, fixed clean0, inputs/DB unchanged')
