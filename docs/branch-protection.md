# Branch protection

Branch protection is GitHub-side enforcement of the standard. Configure once per repo. Without it, the CI checks in `.github/workflows/security.yml` are advisory only — anyone or any agent can push directly to `main` and bypass them.

## Required settings on `main`

Navigate: **Repo → Settings → Branches → Branch protection rules → Add rule**

**Branch name pattern:** `main`

### Pull request requirements
- [x] Require a pull request before merging
- [x] Require approvals — minimum **1**
- [x] Dismiss stale pull request approvals when new commits are pushed
- [ ] Require review from Code Owners (optional, useful for shared repos)

### Status check requirements
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging

**Status checks that must pass** (these are the CI job names from `.github/workflows/security.yml`):

- `secrets — gitleaks`
- `sast — semgrep`
- `sca — trivy`

When Phase 1C lands, add the language overlay checks (e.g., `lint — biome`, `test — vitest`).

### History and integrity
- [x] Require signed commits *(recommended — requires GPG or SSH commit signing setup)*
- [x] Require linear history
- [x] Do not allow bypassing the above settings
- [ ] Allow force pushes — **leave unchecked**
- [ ] Allow deletions — **leave unchecked**

### Optional, for shared repos
- [ ] Restrict who can push to matching branches

## Same for `develop` if used

Apply identical rules to any long-lived branch.

## Why each setting

- **Required PR + status checks** — closes the path where an agent or human pushes directly to `main` and bypasses all gates. The CI checks are only meaningful if they cannot be skipped.
- **Linear history** — makes `git log` readable and `git bisect` reliable. Merge commits scatter the trail and make AI-generated mistakes harder to isolate.
- **Signed commits** — ties commits to a verified identity. Combined with the `[AI-assisted]` commit convention in `AGENTS.md`, provides an audit trail showing which commits an AI agent generated.
- **No force pushes, no deletions** — protects history. Force-push erases the audit record.
- **Up-to-date before merge** — prevents the "PR was green when opened, broken after a sibling PR landed" failure.
- **Dismiss stale approvals** — if new commits arrive after a review, the review is no longer valid. Particularly important for AI-assisted work where the agent may push significant changes after initial approval.

## Verification

After configuring:

1. Open a PR that introduces a deliberate violation — for example, a file containing `AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"` *(use the AWS-docs example key, not a real one)*.
2. Confirm the `secrets — gitleaks` check fails on the PR.
3. Confirm the **Merge pull request** button is greyed out or blocked.
4. Confirm an admin override is required to merge. **Do not use it** — close the PR and verify the gate held.

If any of the four steps fail, branch protection is misconfigured. Stop, fix the configuration, repeat the test.

## For self-hosted Gitea or GitLab

The same principles apply with different UI paths:

- **Gitea:** Repo → Settings → Branches → Branch Protection Rules. Equivalent options exist for required PR, required status checks, no force push, no deletion.
- **GitLab:** Settings → Repository → Protected branches, plus Settings → Merge requests → Merge checks.

Status check job names may differ depending on CI configuration. The list of checks-that-must-pass should match the jobs defined in your CI workflow file.
