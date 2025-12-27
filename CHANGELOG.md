# Changelog
All notable changes to the CDD spec and tooling.

## [1.1.0] - 2025-12-27

### Added
- `cdd_spec` field in project contracts — required for `status: frozen`, optional for `draft`
- Version compatibility checking in tooling (major mismatch = error, else warn)
- `--require-exact-spec` flag for strict version enforcement
- **Native static file scanning** — `type: static` tests with `files:` glob support
- `not_matches` operator — inverse of `matches` for regex lint checks
- `pattern` field on assertions — alternative to `expected` for regex operators
- `message` field on assertions — user-provided context for failure reporting
- `{var}` interpolation in `files:` globs (in addition to `$.vars.X`)
- File/line/col/snippet details in static assertion failures

### Changed
- Spec version now explicitly declared in project contracts (canonical source of truth)
- `.cdd-version` file is now optional fallback
- Static executor now supports file scanning via `run_static_test()`

### Compatibility
- **Additive, backwards compatible** — existing contracts continue to work
- New static scanning features are opt-in via `type: static` + `files:`

- **Additive, backwards compatible** — existing draft contracts continue to work
- Frozen contracts without `cdd_spec` will trigger a warning

## [1.0.14] - 2025-12-27

### Added
- Normative Step Fields table (action, with, save_as, method, n, warmup, command, seconds, fixture)
- Clarified `contains` on arrays uses exact element equality

### Compatibility
- **No behavior change**

## [1.0.13] - 2025-12-27

### Fixed
- `±` encoding issue in spec
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
