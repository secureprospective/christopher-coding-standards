#!/usr/bin/env python3
"""GitHub PR/CI helper for environments without the `gh` CLI.

Read-side subset only: open a PR, check CI status, view branch protection.
Merging and changing branch protection stay manual (see SKILL.md).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


def get_token() -> str:
    path = os.path.expanduser("~/.git-credentials")
    try:
        with open(path) as f:
            content = f.read()
    except OSError as e:
        sys.exit(f"Could not read {path}: {e}")
    match = re.search(r"://[^:]+:([^@]+)@", content)
    if not match:
        sys.exit(f"No token found in {path}")
    return match.group(1)


def get_owner_repo() -> tuple[str, str]:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True, text=True, check=True,
    )
    url = result.stdout.strip()
    match = re.search(r"github\.com[:/]([^/]+)/([^/.]+?)(\.git)?$", url)
    if not match:
        sys.exit(f"Could not parse owner/repo from remote URL: {url}")
    return match.group(1), match.group(2)


def get_current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def api_request(token: str, method: str, path: str, data: dict | None = None) -> dict:
    url = f"https://api.github.com{path}"
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "api.github.com":
        sys.exit(f"Refusing to request non-GitHub URL: {url}")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        # Scheme/host validated above: always https://api.github.com. path
        # segments come from git-derived strings and argparse choices, never
        # raw external input.
        with urllib.request.urlopen(req) as resp:  # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"GitHub API error {e.code}: {e.read().decode()}")


def cmd_pr_open(args, token, owner, repo):
    body_text = ""
    if args.body_file:
        with open(args.body_file) as f:
            body_text = f.read()
    data = {
        "title": args.title,
        "head": args.head or get_current_branch(),
        "base": args.base,
        "body": body_text,
    }
    result = api_request(token, "POST", f"/repos/{owner}/{repo}/pulls", data)
    print(f"PR URL: {result['html_url']}")
    print(f"PR number: {result['number']}")


def cmd_ci_status(args, token, owner, repo):
    ref = args.ref or get_current_branch()
    result = api_request(token, "GET", f"/repos/{owner}/{repo}/commits/{ref}/check-runs")
    for run in result.get("check_runs", []):
        print(f"{run['name']}: {run['status']} / {run['conclusion']}")


def cmd_protection_get(args, token, owner, repo):
    result = api_request(token, "GET", f"/repos/{owner}/{repo}/branches/{args.branch}/protection")
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_open = sub.add_parser("pr-open", help="Open a pull request")
    p_open.add_argument("--title", required=True)
    p_open.add_argument("--head", help="Source branch (default: current branch)")
    p_open.add_argument("--base", default="main")
    p_open.add_argument("--body-file", help="Path to file containing PR body markdown")

    p_status = sub.add_parser("ci-status", help="Check CI status for a ref")
    p_status.add_argument("--ref", help="Branch or SHA (default: current branch)")

    p_prot = sub.add_parser("protection-get", help="Print branch protection settings")
    p_prot.add_argument("branch")

    args = parser.parse_args()
    token = get_token()
    owner, repo = get_owner_repo()

    if args.command == "pr-open":
        cmd_pr_open(args, token, owner, repo)
    elif args.command == "ci-status":
        cmd_ci_status(args, token, owner, repo)
    elif args.command == "protection-get":
        cmd_protection_get(args, token, owner, repo)


if __name__ == "__main__":
    main()
