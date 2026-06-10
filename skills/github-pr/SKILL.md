---
name: github-pr
description: GitHub PR and CI operations (open PR, check CI status, view branch protection) via REST API — for repos/environments where `gh` CLI isn't installed. Wraps token lookup from ~/.git-credentials and owner/repo detection from git remote.
---

# GitHub PR Helper

This environment doesn't have `gh`. This skill standardizes the read-side
REST API calls that replace it, using `scripts/gh.py`.

## Operations

| Command | What it does |
|---|---|
| `python3 scripts/gh.py pr-open --title T [--head BRANCH] [--base main] [--body-file F]` | Opens a PR, prints URL + number. `--head` defaults to current branch. |
| `python3 scripts/gh.py ci-status [--ref BRANCH]` | Prints each check run: name / status / conclusion. `--ref` defaults to current branch. |
| `python3 scripts/gh.py protection-get BRANCH` | Prints current branch protection settings as JSON |

## Out of scope — stays manual

Merging PRs and changing branch protection are hard-to-reverse / shared-state
actions per global CLAUDE.md. They are deliberately **not** in this skill —
confirm the exact action with the human owner and make the API call directly,
as before. This skill only covers calls that create review material or report
state.

## Safety notes

- Token is read from `~/.git-credentials` and never printed.
- If a call fails with 401/403, the error is shown without the Authorization
  header value.
