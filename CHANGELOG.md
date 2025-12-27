# Changelog

All notable changes to the CDD spec and tooling.

## [1.1.0] - 2025-12-27

### Added
- `cdd_spec` field in project contracts — required for `status: frozen`, optional for `draft`
- Version compatibility checking in tooling (major mismatch = error, else warn)
- `--require-exact-spec` flag for strict version enforcement

### Changed
- Spec version now explicitly declared in project contracts (canonical source of truth)
- `.cdd-version` file is now optional fallback

### Compatibility
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
