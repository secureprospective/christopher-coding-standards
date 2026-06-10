---
name: adopt-coding-standards
description: Adopt christopher-coding-standards into a new or existing repo — copies AGENTS.md, SYSTEM_MAP.md template, security configs, branch protection guide, and language overlays from the canonical source repo, then customizes per-project sections.
---

# Adopt Christopher Coding Standards

Source of truth: `/mnt/storage/claudebox/projects/christopher-coding-standards/`
(see `docs/INDEX.md` there for what each file is for).

## Step 0 — one-time install (per machine)

This skill lives in the standards repo so it stays versioned with everything
else it references. To make it invocable from *other* project sessions, copy
or symlink it into the global skills directory:

```bash
ln -s /mnt/storage/claudebox/projects/christopher-coding-standards/skills/adopt-coding-standards \
      ~/.claude/skills/adopt-coding-standards
```

If this symlink doesn't exist yet when the skill is invoked, create it first
(after confirming with the human owner), then continue.

## Steps — apply to the current repo (the one this skill was invoked in)

1. **AGENTS.md** — copy from source root. Edit the per-project section: project
   name, languages, public exposure, stack-specific commands. Do not copy the
   rest verbatim without reading it — confirm each rule actually applies here.
2. **`.claude/settings.json`** — copy from source `.claude/`.
3. **SYSTEM_MAP.md** — copy the template from source root. Fill in this repo's
   directory invariants and existing utilities — no placeholders left behind.
4. **`.gitleaks.toml`** — copy from source root, unmodified.
5. **`.github/workflows/security.yml`** — copy from source `.github/workflows/`.
   Confirm the trivy-action SHA pin matches the source's current pin.
6. **Branch protection** — follow `docs/branch-protection.md` from source
   (read it; don't copy it into this repo).
7. **Language overlay** — TypeScript: copy `templates/typescript/` from source,
   follow its README. Other languages: not yet available (Phase 2) — flag to
   the human owner instead of improvising.
8. **Multi-agent** — if more than one AI agent works this codebase, copy
   `docs/multi-agent-roles.md` and `docs/cross-pollination-log.md` (reset to
   just its format section) from source `docs/`.

Report what was copied/customized and what was skipped (with why). Do not
commit without the human owner's confirmation.
