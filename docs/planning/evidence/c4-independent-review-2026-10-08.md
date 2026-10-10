# C4 independent review — CLEAR

Candidate: `docs/planning/c4-candidate.json`  
Supplied SHA256: `c8999c338a34f1d14bd8c9bac5d00541ada0aa9356a35fa3c5ec4c00aa83a8e2`  
Base: `5761c151442bb213e2953ccc021f0164461a29bb`

## Review

- **Correct — Q1/Q5:** `templates/bash/lib/strict-mode.sh:26–46` preserves required-helper termination and uses string validation rather than arithmetic. Zero/all-zero strings fail; leading-zero and large positives remain valid. Quoted arguments keep values inert. The unchanged caller validates before printing (`templates/bash/scripts/example.sh:12–18`); caller-specific ranges/authorization remain deliberately separate.
- **Correct — Q2/Q3/Q4:** Existing interfaces remain intact, without new abstractions or dependencies. Strict options, IFS and trap ownership are explicit. The inline diagnostic preserves useful location/status in eligible contexts (`lib/strict-mode.sh:15–21`); adoption documentation explains process-wide effects and Bash suppression limits (`templates/bash/README.md:15,45–49`).
- **Correct — lint/format:** `templates/bash/Makefile.snippet:3–23` uses Bash pipefail, NUL-delimited regular-file discovery and option delimiters. Discovery/tool failures remain failures; empty source sets do not pass. Formatting and tests remain distinct. GNU requirements, symlink exclusions and customization-preserving merging are documented.
- **Correct — hooks/adoption:** Immutable hook-source pins and curated ShellCheck settings remain. `templates/bash/.pre-commit-config.yaml:19–24` selects the equivalent native-system scanner with `pass_filenames: false`. Installation/version responsibility and staged-diff versus whole-directory scanning are accurately distinguished (`templates/bash/README.md:43,56`).
- **Correct — scope:** Actual working-tree changes are bounded to Bash and the permitted status/progress routes. Shared core/consumer templates, other overlays, workflows and root security configuration have no delta. README/index status edits route readers to HANDOFF without declaring C4 accepted.
- **Merge verdict: OK for this bounded C4 gate.** No commit, push, merge, deployment or publication permission is granted.

No issues found.

## Test oracle and evidence

The 17 Bats tests invoke the real library in child Bash, not mocks or the Bats driver. Assertions observe diagnostic content, rejection status, absent continuation/success, exact successful output, inert metacharacters, eligible ERR locations/status and handled-condition suppression (`templates/bash/tests/example.bats:10–152`).

The authoritative current-source records bind the same seven fingerprints as `c4-source-copy.json`:

- `evidence/c4-final-candidate-checks.json:13–129`: recorded clean Make lint/test/fmt, 17 tests, standalone tools and separate directory scan.
- `:131–301,357–521`: path probes, intended SC2086/formatting failures, setup/traversal failures, installed hooks and ordinary clean commit.
- `evidence/c4-final-additional-checks.json:26–125`: actual staged sentinel rejection, missing-binary setup failure and space-containing project-root checks.

I inspected the manifest’s 14 artifacts, relevant package-resolution/install identities and lock, provenance/installer source, and five listed session helpers. The binding/integrity helper checks source bytes, evidence hashes, protected files and links; `c4-checks.json:35–49` records those results. Fingerprint entries agree across the candidate/copy/current-result records.

**Review method:** read-only source/diff and recorded-evidence inspection only. I did not rerun runtime tests, SSH, installation, link-check or hashing commands, independently recompute digests, or authenticate remote downloads. Package reports were inspected for relevant provenance/identity fields, not every descriptive metadata field.

## Prior failures and remaining limits

- Positivity baseline failures 4/8/10 became 12 passes. ERR failures 13/14/15 narrowed to 14 after the location repair, then all 17 passed after errtrace. These historical snapshots are not substituted for current evidence.
- The initial system-hook CLI failure is preserved and correctly repaired by disabling filename passing; final affected/full checks were rerun.
- The initial checksum-unverified Go bootstrap and unconfined default caches remain historical limitations—not retroactively verified or pristine-VM claims. Final configuration uses the verified native scanner without a Go compiler.
- Evidence is limited to selected Linux/tool versions. Symlink targets require project-owned coverage adaptation; Make shell settings require deliberate merging.
- ERR is not universal exception handling. Large-positive testing demonstrates absence of machine-integer conversion, not unlimited resources.
- The harmless custom rule proves scanner wiring, not default secret-policy completeness. Hook `--all-files` is not whole-tree secret scanning. Transitive hook environments are not covered by the separate bootstrap lock.
- No all-overlay, hosted-enforcement, containment, live-consumer or publication conclusion follows.