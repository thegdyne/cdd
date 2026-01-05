# Changelog
All notable changes to the CDD spec and tooling.

## [1.1.6] - 2026-01-05

### Added
- `cdd isolate` command for testing single contracts in isolation (addresses directory-running bug)
- `cdd paths` command (G0.3 gate) for path verification before testing
- Documentation of `cdd test file.yaml` bug (runs all contracts in directory, not just file)

### Changed
- README.md: Updated CLI reference to recommend `cdd isolate` for single contracts
- README.md: Updated Practical Workflow to use `cdd isolate` instead of `cdd test`
- README.md: Updated Known Issues to recommend `cdd isolate` as workaround
- HOWTO.md: Updated all workflows to use `cdd isolate` for single contracts
- HOWTO.md: Added path verification step to all workflows
- HOWTO.md: Updated Quick Reference Card and Common Patterns
- SPEC.md: Added `contract-paths` and `contract-isolate` to CLI Tools section
- SPEC.md: Updated Tool Purposes table to include new commands
- SPEC.md: Updated Exit Codes table to include new commands

### Compatibility
- **No behavior change** -- documentation updates only, clarifies best practices

## [1.1.5] - 2025-12-29

### Added
- HTML analyzer (`cdd analyze <file.html>`) for web project contracts
- `analyze/html.py` extracts: element counts, CSS classes, images, required elements check
- `compare_html_analyses()` for comparing HTML baselines
- Process failure report template for post-mortems

### Changed
- `cdd analyze` now supports `.html` and `.htm` files

### Compatibility
- **Additive, backwards compatible**

## [1.1.5] - 2025-12-29

### Added
- Mandatory Gates section in SPEC.md (G0-G3 with sequence diagram)
- Process Checkpoints table in SPEC.md
- Anti-Patterns appendix in SPEC.md (AP1-AP6)
- HTML analyzer (`cdd analyze *.html`) in tooling
- Gates and Anti-Patterns summary in README.md

### Changed
- README updated with gates workflow and anti-patterns table
- Documentation section now references CDD_ANALYSIS_AND_IMPROVEMENTS.md

### Compatibility
- **No behavior change** â€” clarifies process enforcement without changing contract schema or tooling

## [1.1.4] - 2025-12-29

### Added
- "Analysis precedes contracts" as first principle in What section
- Reference, Analysis, Baseline terms added to Glossary
- Reference Analysis and Compare phases added to The Model diagram

### Changed
- README rewritten with Phase 0 hard gate methodology
- Development loop now starts with reference analysis

### Compatibility
- **No behavior change** â€” clarifies process without changing contract schema or tooling

## [1.1.3] - 2025-12-28

### Fixed
- Interpolate variables in shell command arguments

### Compatibility
- **No behavior change** â€” fixes variable expansion to work as documented

## [1.1.2] - 2025-12-28

### Fixed
- Fix repo_root detection when passing single contract file

### Compatibility
- **No behavior change** â€” bug fix only

## [1.1.1] - 2025-12-27

### Added
- Native static file scanning wired into runner
- Expanded README with full usage guide

### Compatibility
- **Additive, backwards compatible**

## [1.1.0] - 2025-12-27

### Added
- `cdd_spec` field in project contracts â€” required for `status: frozen`, optional for `draft`
- Version compatibility checking in tooling (major mismatch = error, else warn)
- `--require-exact-spec` flag for strict version enforcement
- **Native static file scanning** â€” `type: static` tests with `files:` glob support
- `not_matches` operator â€” inverse of `matches` for regex lint checks
- `pattern` field on assertions â€” alternative to `expected` for regex operators
- `message` field on assertions â€” user-provided context for failure reporting
- `{var}` interpolation in `files:` globs (in addition to `$.vars.X`)
- File/line/col/snippet details in static assertion failures

### Changed
- Spec version now explicitly declared in project contracts (canonical source of truth)
- `.cdd-version` file is now optional fallback
- Static executor now supports file scanning via `run_static_test()`

### Compatibility
- **Additive, backwards compatible** â€” existing contracts continue to work
- New static scanning features are opt-in via `type: static` + `files:`
- Frozen contracts without `cdd_spec` will trigger a warning

## [1.0.14] - 2025-12-27

### Added
- Normative Step Fields table (action, with, save_as, method, n, warmup, command, seconds, fixture)
- Clarified `contains` on arrays uses exact element equality

### Compatibility
- **No behavior change**

## [1.0.13] - 2025-12-27

### Fixed
- `Â±` encoding issue in spec
- Added `$.env.os_family` for clean platform skip logic

### Compatibility
- **No behavior change**

## [1.0.12] - 2025-12-27

### Added
- Compatibility Promise with table format
- Normative Core definition
- "Reference runner is arbiter" rule

### Compatibility
- **No behavior change**

## [1.0.0] - 2025-12-27

### Added
- Initial frozen release
- Complete schema with field tables
- Assertion DSL with 12 operators
- JSONPath resolution rules
- Step/action vocabulary with executor validity matrix
- Parameterisation via CLI and matrix
- Report format specification

---

See SPEC.md for complete changelog with implementation details.
