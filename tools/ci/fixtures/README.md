# Passive Trivy controls — do not install these graphs

These hand-authored pnpm lockfileVersion9 dev-dependency locks/package manifests are scanner data only. `check-security.py trivy` copies them into owned control directories and reads them with Trivy; it never runs a package manager, downloads package archives, imports lodash or executes an application for these controls. They are not consumer payloads or approved dependency graphs.

- `trivy-vulnerable`: lodash4.17.20 must produce status1 with `CVE-2021-23337` / package `lodash` / installed4.17.20 / HIGH in the actual JSON report. The current DB also reports HIGH `CVE-2026-4800`; this additional finding is retained, not suppressed.
- `trivy-fixed`: lodash4.18.0 must be recognized as a package-bearing pnpm graph and return0/no selected findings. The first attempted4.17.21 fixed control actually failed for HIGH `CVE-2026-4800`; that original failure remains evidence. Its documented first patch is4.18.0. This is a specific observed control repair, not an upgrade to the consumer graph.

Both use the same CLI/scanner/dev/severity/exit flags and the root clean scan's cache. Controls freeze DB updates, bind actual DB file SHA before/after and leave declared package/lock inputs unchanged. Any skipped graph, missing advisory, wrong package/version/severity, unexpected green, fixed finding or changed DB stops the helper. DB/hash observations are not authenticated approval or a promise all vulnerabilities are detected.

Oracles: [reviewed 2021 advisory](https://github.com/advisories/GHSA-35jh-r3h4-6jhm), [reviewed 2026 advisory](https://github.com/advisories/GHSA-r5fr-rjxr-66jc). Publisher version metadata supplied resolution integrity strings; no package archive was fetched/hashed or executed, so these strings are not asserted package-byte verification. Exact selected metadata/probe/current-source results are separate C12 evidence. No Semgrep licensed policy bytes belong in this directory.
