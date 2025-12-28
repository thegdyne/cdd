# Contract Runner Roadmap

Future additions to the Contract-Driven Development spec and tooling.

**Applies to spec version:** 1.1.3  
**Last updated:** 2025-12-28

---

## Phase 1: MVP (must-have for initial release)

| Item | Status | Notes |
|------|--------|-------|
| `approx` operator | ✅ Done (v1.0.6) | Float/timing comparisons with tolerance |
| `skip_if` grammar lock-down | ✅ Done (v1.0.6) | Restricted safe expression subset |
| Numeric version fields | ✅ Done (v1.0.7) | `_major`, `_minor` for safe version comparisons |
| Requirement coverage rules | ✅ Done (v1.0.7) | Only linked tests count toward coverage |
| Matrix report shapes | ✅ Done (v1.0.7) | Per-target report + matrix summary report |
| Shell executor semantics | ✅ Done (v1.0.8) | cwd, artifacts_dir, env, timeout defined |
| Report file outputs | ✅ Done (v1.0.9) | File naming convention for matrix runs |
| Report invariants | ✅ Done (v1.0.10) | Status values, assertions array, required fields |
| AST stability note | ✅ Done (v1.0.10) | Only calls/bus_reads stable in v1.0 |
| `contract-lint` | 🔲 TODO | Schema validation + requirement coverage |
| Python executor | 🔲 TODO | `call`, `call_n`, step envelope |
| `sclang` executor | 🔲 TODO | `render_nrt` + metrics JSON output |
| Static executor | 🔲 TODO | `sclang_ast` parser (MVP); `python_ast` later |
| Report writer | 🔲 TODO | JSON output per schema_version 1.0 (core MVP) |

**Goal:** Run `contract-test` against a single Python contract and get a valid single-target `report.json` (no matrix required for MVP).

---

## Phase 2: Production Ready

| Item | Status | Notes |
|------|--------|-------|
| `contract-scaffold` | 🔲 TODO | Generate implementation stubs from contract |
| `schema` operator | 🔲 TODO | Validate object shape against schema |
| `all_lt` / `all_gt` quantifiers | 🔲 TODO | Assert condition over all array elements |
| `any` quantifier | 🔲 TODO | Assert condition over any array element |
| Report diff tooling | 🔲 TODO | Compare two reports, show regressions |
| Node executor | 🔲 TODO | JavaScript/TypeScript support |
| `--must-only` flag | 🔲 TODO | Run only tests linked to `must` requirements |

**Goal:** Full Noise Engine migration to contract-based validation.

---

## Phase 3: Polish

| Item | Status | Notes |
|------|--------|-------|
| AST schema versioning | 🔲 TODO | `$.ast.schema_version` field |
| `tolerance_pct` for approx | 🔲 TODO | Percentage-based tolerance option |
| Audio metrics expansion | 🔲 TODO | Clipping count, NaN/Inf detection, spectral centroid |
| Stereo correlation metric | 🔲 TODO | Left/right channel correlation check |
| CI integration guide | 🔲 TODO | GitHub Actions workflow examples |

**Goal:** Production-grade tooling with extended diagnostics.

---

## Deferred / Maybe

| Item | Notes |
|------|-------|
| Universal executor adapters | Risk of bypassing consistency via shell escape hatch |
| Regex parser for static | Explicitly excluded to prevent false positives |
| `eval` in skip_if | Security risk, grammar is intentionally restricted |
| Stricter requirement links | Current: SHOULD + warn on unlinked tests in frozen. May tighten to MUST in future major version. |

---

## Design Decisions Log

### Why numeric version fields instead of version string semantics?
- Lexicographic string compare is wrong (`"3.9" > "3.10"`)
- Implementing semver parsing adds complexity to every executor
- Numeric fields (`_major`, `_minor`) are simple and unambiguous
- Full version string still available for display/logging

### Why `approx` instead of `within`?
- `approx` is more intuitive for "approximately equal"
- `within` could be confused with `in_range`
- Semantics: `abs(actual - expected) <= tolerance`

### Why restricted `skip_if` grammar?
- Prevents eval injection
- Ensures portable expressions across executor implementations
- Frozen contracts fail lint on invalid expressions (catches errors early)

### Why AST stability note?
- Parser implementations may vary in what optional fields they emit
- Only calls and bus_reads are required for Noise Engine contracts
- Other fields (imports, definitions) are useful but not guaranteed
- Prevents contracts from depending on parser-specific behavior

### Why report invariants?
- Different executor implementations must produce identical report shapes
- Status values locked to 4 options prevents ad-hoc additions
- Assertions array always present simplifies consumer code
- Implicit expected values rendered explicitly ensures report is self-documenting

### Why report file output convention?
- CI/diff tooling needs predictable file locations
- Per-target reports allow caching and parallel processing
- `report_path` in matrix summary enables tool traversal
- Sanitized target names prevent filesystem issues

### Why shell executor cwd is contract directory?
- Relative paths in shell commands resolve predictably
- Scripts can reference sibling files without absolute paths
- Consistent across all platforms
- artifacts_dir is created before first step and exposed as $ARTIFACTS_DIR

### Why two matrix report shapes?
- Per-target reports allow caching and diffing individual targets
- Matrix summary provides quick pass/fail overview without loading all data
- `runs[]` in summary contains summaries only (not full results) to keep size manageable
- Clear separation prevents confusion about what data lives where

### Why coverage only counts linked tests?
- Unlinked tests are ambiguous for coverage calculation
- Tests without `requirement` are typically utility/meta tests
- Frozen contracts should have explicit requirement links
- Keeps `contract-lint` coverage logic simple and deterministic

### Why priority is advisory-only?
- If you don't want a test to fail the build, use `skip: true`
- Priority helps humans triage, not machines ignore failures
- Future `--must-only` provides opt-in filtering

### Why AST source is optional?
- Reduces report size significantly
- Available with `--verbose` when needed for debugging
- Required fields are `calls` and `bus_reads`

---

## Contributing

To propose additions:
1. Check if item exists in this roadmap
2. If new, add to appropriate phase with rationale
3. For spec changes, require dual-AI review before merge
4. Spec version bump required for any normative changes

---

*Roadmap for CONTRACT_DRIVEN_DEV.md spec*
