# Contract-Driven Development (CDD)

A methodology where you write the spec and tests first, then build the implementation to pass them.

## Installation

```bash
# Via pipx (recommended for CLI)
pipx install git+https://github.com/yourname/cdd.git@v1.1.0

# Via pip (for embedding in projects)
pip install git+https://github.com/yourname/cdd.git@v1.1.0
```

## Quick Start

```bash
# Check spec/tool version
cdd spec --version

# Lint contracts (schema + coverage)
cdd lint contracts/

# Run contract tests
cdd test contracts/

# Requirement coverage report
cdd coverage contracts/
```

## Consumer Project Setup

1. Add `cdd_spec` to your project contract:

```yaml
# contracts/project.yaml
project: my-project
cdd_spec: 1.1.0
version: 1.0.0
status: draft
goal: Build something amazing
success_criteria:
  - Thing works
components:
  - component_a
```

2. Write component contracts with requirements and tests
3. Run `cdd test contracts/` — iterate until green

## Spec Version Checking

- **Major mismatch** → Error (project targets 2.x, you have 1.x)
- **Minor/patch mismatch** → Warning (should be compatible)
- **Exact match required** → Use `--require-exact-spec`

## Documentation

- [SPEC.md](SPEC.md) — The normative specification
- [ROADMAP.md](ROADMAP.md) — Implementation plan and future work
- [CHANGELOG.md](CHANGELOG.md) — Version history

## License

MIT
