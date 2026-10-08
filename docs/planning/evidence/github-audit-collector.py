"""One-shot authorized canonical-repo audit: GitHub GET only; no token reads/output."""
import datetime
import json
import re
import subprocess
from pathlib import Path

ROOT = 'repos/secureprospective/christopher-coding-standards'
OUT = Path('/home/chris/scratch/coding-standards-github-audit-2026-10-08.json')
results = {'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'repo': ROOT, 'method': 'GET only', 'requests': {}}

def get(suffix):
    path = ROOT + suffix
    assert path.startswith(ROOT + '/') or path == ROOT
    proc = subprocess.run(['gh', 'api', '--hostname', 'github.com', '--method', 'GET', '--include', path], capture_output=True, text=True, timeout=45)
    raw = proc.stdout.replace('\r\n', '\n')
    header, sep, body = raw.partition('\n\n')
    status_match = re.search(r'^HTTP/\S+\s+(\d+)', header)
    status = int(status_match.group(1)) if status_match else None
    try:
        data = json.loads(body if sep else raw)
    except json.JSONDecodeError:
        data = None
    selected_headers = {}
    for line in header.splitlines():
        key, colon, value = line.partition(':')
        if colon and key.lower() in ['x-oauth-scopes', 'x-accepted-oauth-scopes', 'x-accepted-github-permissions']:
            selected_headers[key.lower()] = value.strip()
    item = {'http_status': status, 'command_exit': proc.returncode, 'permission_headers': selected_headers, 'data': data}
    if proc.returncode:
        item['error_message'] = data.get('message') if isinstance(data, dict) else 'API/CLI request failed; no raw output retained'
    results['requests'][suffix or '/metadata'] = item
    OUT.write_text(json.dumps(results, indent=2) + '\n')
    summary = {'endpoint': suffix or '/metadata', 'http_status': status, 'exit': proc.returncode}
    if proc.returncode:
        summary['error'] = item['error_message']
    elif isinstance(data, list):
        summary['items'] = len(data)
    elif isinstance(data, dict):
        summary['keys'] = list(data.keys())
    print(json.dumps(summary), flush=True)
    return data if proc.returncode == 0 else None

metadata = get('')
if isinstance(metadata, dict):
    # Exclude unrelated account/repository metadata from this audit artifact.
    results['requests']['/metadata']['data'] = {k: metadata.get(k) for k in ['full_name', 'visibility', 'private', 'default_branch', 'archived', 'disabled', 'permissions', 'allow_auto_merge', 'allow_merge_commit', 'allow_squash_merge', 'allow_rebase_merge', 'delete_branch_on_merge']}
    results['requests']['/metadata']['data']['owner_type'] = metadata.get('owner', {}).get('type')
    OUT.write_text(json.dumps(results, indent=2) + '\n')
branches = get('/branches?per_page=100')
get('/branches/main/protection')
rulesets = get('/rulesets?includes_parents=true&per_page=100')
if isinstance(rulesets, list):
    for row in rulesets:
        if isinstance(row.get('id'), int):
            get('/rulesets/' + str(row['id']))
get('/rules/branches/main')
get('/rules/branches/agents%2Faudit-scope-probe')  # Read-only hypothetical name; no branch is created.
get('/actions/permissions')
get('/actions/permissions/workflow')
get('/actions/permissions/selected-actions')
get('/actions/permissions/fork-pr-contributor-approval')
get('/actions/workflows?per_page=100')
get('/actions/runs?per_page=20')
get('/commits/93ee82a346289f7fdf77a696a20a999ffcc61dc6/check-runs?per_page=100')
get('/commits/93ee82a346289f7fdf77a696a20a999ffcc61dc6/status')
get('/pulls?state=open&per_page=100')
OUT.write_text(json.dumps(results, indent=2) + '\n')
print('Evidence artifact: ' + str(OUT))
