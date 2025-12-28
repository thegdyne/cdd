# Contract-Driven Development (CDD)

A methodology where you write the spec and tests first, then build the implementation to pass them.

## What is CDD?

CDD inverts the typical development flow:

1. **Write a contract** "” Define requirements and tests in YAML before writing code
2. **Implement against it** "” Build code that makes the tests pass
3. **Iterate with feedback** "” Run tests, see failures with full context, fix, repeat
4. **Freeze when stable** "” Lock the contract, changes require version bumps

The contract is the source of truth. The code exists to fulfill it.

## Installation

```bash
# Via pipx (recommended for CLI)
pipx install git+https://github.com/thegdyne/cdd.git@v1.1.3

# Via pip
pip install git+https://github.com/thegdyne/cdd.git@v1.1.3
```

Verify:

```bash
cdd spec --version
# 1.1.3
```

## Using CDD in Your Project

### 1. Create a project contract

```yaml
# my-project/contracts/project.yaml
project: my-project
cdd_spec: 1.1.3          # Locks to this CDD spec version
version: 1.0.0
status: draft            # draft | frozen | deprecated

goal: |
  What you're building and why.

success_criteria:
  - Criterion 1
  - Criterion 2

components:
  - component_a
  - component_b
```

### 2. Write component contracts

```yaml
# my-project/contracts/component_a.yaml
contract: component_a
version: 1.0.0
status: draft
description: |
  What this component does.

runner:
  executor: python
  entry: src/component_a.py
  symbol: main_function

requirements:
  - id: R001
    priority: must
    description: Does the thing
    acceptance_criteria:
      - Returns expected output

tests:
  - id: T001
    name: does_the_thing
    requirement: R001
    type: unit
    steps:
      - action: call
        with: { input: "test" }
        save_as: result
    assert:
      - op: eq
        actual: $.result.value
        expected: "expected_output"
```

### 3. Run the tools

```bash
# Validate contracts (schema + requirement coverage)
cdd lint contracts/

# Run tests
cdd test contracts/

# Check requirement coverage
cdd coverage contracts/
```

### 4. Implement until green

Write code in `src/component_a.py` that makes `cdd test` pass. The test output shows exactly what failed and why.

### 5. Freeze when stable

Change `status: draft` â†’ `status: frozen` in your contracts. Now any changes require a version bump.

## Version Compatibility

The `cdd_spec` field in your project contract declares which CDD spec version you're targeting.

| Scenario | Behavior |
|----------|----------|
| Major mismatch (project: 2.x, tool: 1.x) | **Error** "” incompatible |
| Minor/patch mismatch | **Warning** "” should be compatible |
| Exact match required | Use `--require-exact-spec` flag |

When CDD releases a new version:

1. Review the [CHANGELOG](CHANGELOG.md)
2. Update your tooling: `pipx upgrade cdd` or reinstall with new tag
3. Update `cdd_spec` in your project contract
4. Run tests to verify compatibility

## CLI Reference

```bash
# Show spec/tool version
cdd spec --version

# Print full spec text
cdd spec --print

# Lint contracts (exits 1 if errors)
cdd lint contracts/
cdd lint contracts/component_a.yaml
cdd lint contracts/ --strict        # Treat warnings as errors
cdd lint contracts/ --json          # Machine-readable output

# Run tests (exits 1 if failures)
cdd test contracts/
cdd test contracts/ --var target=foo        # Inject variable
cdd test contracts/ --only T001 --only T002 # Run specific tests
cdd test contracts/ --require-exact-spec    # Strict version check
cdd test contracts/ --json                  # Machine-readable report

# Coverage report (exits 0 unless --strict)
cdd coverage contracts/
cdd coverage contracts/ --strict    # Exit 1 if uncovered requirements
cdd coverage contracts/ --json
```

## Project Structure

Recommended layout for a CDD-based project:

```
my-project/
â”œâ”€â”€ contracts/
â”‚   â”œâ”€â”€ project.yaml        # Project contract (required)
â”‚   â”œâ”€â”€ component_a.yaml    # Component contracts
â”‚   â””â”€â”€ component_b.yaml
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ component_a.py      # Implementation
â”‚   â””â”€â”€ component_b.py
â””â”€â”€ .cdd-version            # Optional fallback (if no cdd_spec in project.yaml)
```

## Documentation

- [SPEC.md](SPEC.md) "” The normative specification (what contracts look like, assertion operators, report format)
- [ROADMAP.md](ROADMAP.md) "” Implementation status and future plans
- [CHANGELOG.md](CHANGELOG.md) "” Version history and compatibility notes

## Executors

CDD supports multiple executors for different languages/environments:

| Executor | Actions | Use Case |
|----------|---------|----------|
| `python` | `call`, `call_n` | Python functions |
| `shell` | `shell` | CLI tools, scripts |
| `static` | (assertions only) | AST analysis |
| `sclang` | `render_nrt` | SuperCollider audio |

## License

MIT
