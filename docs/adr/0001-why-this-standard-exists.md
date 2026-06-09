# ADR-0001: Why this standard exists

## Date
2026-06-07

## Status
Accepted

## Context

Christopher Campbell builds with multiple AI models. Claude Code in VSCode/ClaudeBox is the primary execution environment, with planned and active use of other frontier models and local LLMs (Qwen 2.5 Coder, GLM-4.7, Qwen3-30B) on dedicated hardware.

Different models produce code with different characteristics. All current LLMs produce code that is measurably less secure than human-written code. The 2025–2026 empirical record:

| Source | Finding |
|---|---|
| Veracode 2025 GenAI Code Security Report (100+ LLMs, 4 languages) | 2.74x more vulnerabilities in AI-generated code vs. human baseline. 45% of samples carry OWASP Top 10 issues. Java worst at 72% security failure rate. |
| Veracode XSS analysis | 86% of relevant AI-generated samples fail XSS defenses. 88% have log injection vulnerabilities. |
| AppSec Santa, 2026 | 1 in 4 AI-generated samples contain a confirmed OWASP vulnerability. |
| Apiiro Fortune-50 analysis | CVSS 7.0+ vulnerabilities appear 2.5x more often in AI-generated code. By June 2025, AI code was adding 10,000+ new security findings per month — 10x increase from December 2024. |
| arXiv 2510.26103 (GitHub-scale CWE study) | Most dangerous CWEs in AI code: SQL Injection (CWE-89), OS Command Injection (CWE-78), Code Injection (CWE-94), hard-coded credentials (CWE-259/798). Four appear in MITRE 2024 Top 25. |
| Pearce et al., 2022 | ~40% of GitHub Copilot generated programs contain vulnerabilities. |
| Perry et al., 2023 | Participants using AI assistants wrote "significantly less secure code" and exhibited a "false sense of security," often rating their insecure solutions as secure. |

Without a standard, AI-assisted development at speed produces inconsistent style, security gaps, structural drift, and code bloat across projects. Multiple LLMs amplify this — each has different style defaults, different security weak spots, and different failure modes.

## Decision

Adopt a **layered guardrail standard** that is:

1. **Model-agnostic.** Same gates apply whether code comes from Claude Code, frontier models, or local LLMs.
2. **Deterministic where possible.** Hooks and CI gates over prose instructions. Prose in `AGENTS.md` is advisory; pre-commit and CI are enforcement. (Per Anthropic's own published guidance: "If you want something to happen every time without exception, use hooks. For guidance that requires judgment, use CLAUDE.md. Hooks are deterministic; CLAUDE.md is advisory.")
3. **Free-tooling-first.** The standard works without paid SaaS. Recommended stack: Biome / Ruff / golangci-lint, Semgrep CE, Trivy, Gitleaks, pre-commit framework.
4. **Canonical.** This repo is the single source of truth. Other repos copy from here. Updates flow from here outward.
5. **Replicable.** Designed so TFM Vanguards can adopt the same standard with the same tooling on their own hardware.

## Architectural invariants

These follow from the decision and constrain future design:

- **`AGENTS.md` is the advisory file.** Multi-model. Vendor-specific filenames (`CLAUDE.md`, `GEMINI.md`) symlink to it. Source: AGENTS.md was donated to the Agentic AI Foundation under the Linux Foundation in December 2025 and is the emerging open standard (20,000+ repositories on GitHub).
- **`.claude/settings.json` deny rules are belt-and-suspenders.** Not the sole boundary for sensitive files. Reason: deny-rule enforcement bugs are documented in Claude Code (GitHub issues #6631, #18160, #27040, #31925). OS-level containment (container scope, LXC/microVM) is required.
- **Pre-commit hooks are the enforcement layer.** Prose in `AGENTS.md` is advisory. Documented behavior pattern: agents reading hook failures mid-session learn the project's standards through enforcement, not through instructions.
- **Spec Kit is conditional.** The agent asks at the start of a new feature or project. Default off.
- **Security tools pin to commit SHAs, not version tags.** Reason: `aquasecurity/trivy-action` supply chain compromise of March 19, 2026 — 75 of 76 version tags force-pushed with malicious payload that exfiltrated CI/CD secrets before running the legitimate scan. Pipelines pinned to SHAs were unaffected.
- **Architecture/overview sections are excluded from `AGENTS.md`.** Per ETH Zurich research (Gloaguen et al., 2026): LLM-generated context files consistently reduce agent performance and inflate cost. Generic architecture overviews increase token cost without changing agent behavior.

## Consequences

### Positive
- Every project starts with the same baseline.
- Standard evolves in one place; consumers re-pull.
- Vanguards can fork or copy the standard without rebuilding it.
- Model swap (Claude → frontier → local) does not require restandardizing.
- Audit trail: every layer is documented with rationale.

### Negative
- Setup cost per new repo (template copy).
- Standard must be kept current; stale standards drift faster than no standard at all.
- Tooling versions need periodic review (quarterly minimum).
- Free-only constraint means giving up some paid-tool capabilities (e.g., automated SAST remediation, Renovate cloud orchestration).

### Neutral
- Branch protection enforcement is GitHub-side; repos hosted elsewhere (self-hosted Gitea, GitLab) need equivalent configuration.
- AI-assisted commit metadata is convention, not enforced — depends on human or agent discipline.

## Alternatives considered

- **Per-project ad-hoc standards.** Rejected: multiplies maintenance, prevents replication for Vanguards.
- **CLAUDE.md as the canonical instruction file.** Rejected: locks the standard to one vendor. Switching to local models or Gemini would require re-tooling.
- **Paid SaaS stack (Snyk + CodeRabbit + Pixee).** Rejected: violates the free-tooling-first principle. Free stack covers the same gates with manual configuration.
- **No standard, rely on model self-policing.** Rejected: 2.74x baseline vulnerability rate makes this untenable.

## Sources

1. Veracode. *2025 GenAI Code Security Report.* https://www.veracode.com/blog/genai-code-security-report-2025/
2. AppSec Santa, summarized in NowSecure (2026-05-19), "What OWASP Vulnerabilities in AI-Generated Code Mean for Mobile App Security."
3. Apiiro AI-generated code analysis, summarized in SoftwareSeni (2026-02-17).
4. arXiv 2510.26103. *Security Vulnerabilities in AI-Generated Code: A Large-Scale Analysis of Public GitHub Repositories.*
5. Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B., Karri, R. (2022). *Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions.*
6. Perry, N., Srivastava, M., Kumar, D., Boneh, D. (2023). *Do Users Write More Insecure Code with AI Assistants?*
7. OWASP Top 10 for LLM Applications, 2025 edition. https://genai.owasp.org/
8. Snyk advisory: *Trivy GitHub Actions Supply Chain Compromise.* https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/
9. Anthropic. *Best practices for Claude Code.* https://code.claude.com/docs/en/best-practices
10. AGENTS.md specification. https://agents.md/
11. Gloaguen et al. (2026). LLM-generated context file performance analysis, ETH Zurich.
