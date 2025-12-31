# CDD HOWTO: Real-World Workflow

How the CDD tools work together in practice.

## The Tools

| Tool | Command | Purpose |
|------|---------|---------|
| cdd-tooling | `cdd` | Contracts: analyze, lint, test, compare |
| cdd-context | `cdd-context` | Generate project context for AI |
| cdd-flow | `cdd-flow` | Orchestrate artifact handoff with AI |
| cdd-utils | `cdd-utils` | Utilities (encoding hygiene) |

## Install

```bash
pipx install cdd-tooling cdd-context cdd-flow cdd-utils
```

## Recommended Aliases

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Context
alias ctx='cdd-context build --clip'
alias ctxd='cdd-context build --changes --clip'

# Flow
alias fc='cdd-flow ctx'
alias fl='cdd-flow land'
alias flv='cdd-flow land --verify'
alias fu='cdd-flow undo'
alias fcp='cdd-flow checkpoint'
alias fs='cdd-flow status'

# Utils
alias cu='cdd-utils'
```

---

## Workflow 1: AI-Assisted Feature Development

The typical loop when building features with Claude.

### 1. Start a session

```bash
cd ~/repos/my-project
ctx                          # Generate context, copy to clipboard
```

Paste into Claude. Describe what you want to build.

### 2. Claude provides an artifact

Claude gives you code/files. Download to `~/Downloads/`.

### 3. Land the artifact

```bash
fl                           # Land from Downloads into project
```

This copies the artifact into your project and stages for git.

### 4. Check for AI quirks

AI-generated code sometimes has encoding issues:

```bash
cdd-utils utf8 --report src/
```

If corruption found:

```bash
cdd-utils utf8 --dry-run --smart src/   # See what's legitimate vs suspicious
cdd-utils utf8 --smart-fix src/          # Fix only corruption
```

### 5. Verify

```bash
cdd lint contracts/          # Schema valid?
cdd test contracts/          # Tests pass?
```

Or combined:

```bash
flv                          # Land + verify in one step
```

### 6. Iterate or checkpoint

If tests fail, go back to Claude with the error output. Use `ctxd` to send just the changes.

If tests pass:

```bash
fcp "Added feature X"        # Checkpoint (commits verified state)
```

### 7. Continue or finish

Repeat 1-6 until feature complete. Then freeze contracts:

```yaml
# In contracts/feature.yaml
status: frozen               # Was: draft
```

Commit and push.

---

## Workflow 2: Contract-First Development

When you want the contract to exist before implementation.

### 1. Analyze the reference

What are you building toward? A PDF form, an API spec, existing code?

```bash
# PDF/HTML reference
cdd analyze reference/mockup.pdf -o analysis/baseline/

# Existing code reference
cdd analyze src/existing_module.py -o analysis/baseline/
```

Review `analysis/baseline/elements.md`. Does it capture what matters?

### 2. Write the contract

```yaml
# contracts/feature.yaml
contract: feature
version: 1.0.0
status: draft
cdd_spec: 1.1.5

requirements:
  - id: R001
    description: Must have X from baseline
    source_ref: analysis/baseline/elements.md#E1

tests:
  - id: T001
    name: has_x
    requirement: R001
    steps:
      - action: shell
        command: ["grep", "pattern", "../src/feature.py"]
        save_as: result
    assert:
      - op: eq
        actual: $.result.ok
        expected: true
```

### 3. Verify contract is valid

```bash
cdd paths contracts/feature.yaml   # Paths resolve?
cdd lint contracts/feature.yaml    # Schema valid?
```

### 4. Implement

Now build the code. Test frequently:

```bash
cdd test contracts/feature.yaml
```

### 5. Compare output to baseline

If your output is comparable to the reference:

```bash
cdd analyze output/result.pdf -o analysis/output/
cdd compare analysis/baseline/ analysis/output/
```

This shows exact deviations. Fix and re-run until acceptable.

### 6. Freeze

```yaml
status: frozen
```

---

## Workflow 3: Fixing Encoding Issues

AI-generated code often has UTF-8 corruption (smart quotes, mojibake).

### Scan for issues

```bash
cdd-utils utf8 --report src/
```

Output shows files with non-ASCII and what characters were found.

### Preview fixes

```bash
cdd-utils utf8 --dry-run src/file.py
```

Shows line-by-line what would change.

### Smart mode

Distinguishes between:
- **Legitimate**: Isolated Unicode (intentional symbols like arrows in UI)
- **Suspicious**: Clustered Unicode (likely corruption)

```bash
cdd-utils utf8 --dry-run --smart src/file.py
```

### Fix

```bash
# Fix only corruption (keep intentional Unicode)
cdd-utils utf8 --smart-fix src/file.py

# Fix ALL non-ASCII (normalize everything to ASCII)
cdd-utils utf8 --fix src/file.py
```

Both create backups before modifying.

---

## Workflow 4: Recovery

When things go wrong.

### Undo last landing

```bash
fu                           # Reverts last fl/flv
```

### Check session history

```bash
cdd-flow history
```

### Abandon session entirely

```bash
cdd-flow abandon             # Reverts to baseline before session started
```

### Start fresh

```bash
git status                   # What's changed?
git diff                     # Review changes
git checkout -- .            # Nuclear option: discard all changes
```

---

## Quick Reference Card

```bash
# === CONTEXT ===
ctx                          # Full context to clipboard
ctxd                         # Delta (changes only) to clipboard

# === FLOW ===
fl                           # Land artifact from Downloads
flv                          # Land + verify
fu                           # Undo last landing
fcp "message"                # Checkpoint (commit verified state)
fs                           # Show status

# === CONTRACTS ===
cdd paths contracts/         # Verify paths resolve
cdd lint contracts/          # Validate schema
cdd test contracts/          # Run tests
cdd test contracts/ --only T001  # Single test
cdd analyze ref.pdf -o dir/  # Analyze reference
cdd compare dir1/ dir2/      # Compare analyses

# === UTILS ===
cdd-utils utf8 --report src/           # Scan for non-ASCII
cdd-utils utf8 --dry-run --smart file  # Preview with categorization
cdd-utils utf8 --smart-fix src/        # Fix corruption only
```

---

## Common Patterns

### "Claude gave me code with weird characters"

```bash
cdd-utils utf8 --report src/
cdd-utils utf8 --smart-fix src/
```

### "Tests fail but I don't know why"

```bash
cdd test contracts/feature.yaml --only T001
# Read the actual vs expected in output
```

### "I want to see what changed since last checkpoint"

```bash
ctxd                         # Delta context
git diff                     # Raw diff
```

### "I need to test one contract in isolation"

```bash
cdd isolate contracts/feature.yaml
cdd isolate contracts/feature.yaml --keep  # Keep temp dir for debugging
```

### "Contract paths aren't resolving"

```bash
cdd paths contracts/feature.yaml
# Paths are relative to contracts/ directory
# Use ../src/ not src/
```

---

## The Mental Model

```
You (human)                    Claude (AI)
    |                              |
    |  1. ctx - send context       |
    |----------------------------->|
    |                              |
    |  2. describe what you want   |
    |----------------------------->|
    |                              |
    |  3. artifact (code/files)    |
    |<-----------------------------|
    |                              |
    |  4. fl - land artifact       |
    |  5. cdd-utils - check encoding
    |  6. cdd test - verify        |
    |                              |
    |  7a. PASS: fcp checkpoint    |
    |  7b. FAIL: ctxd + errors     |
    |----------------------------->|
    |                              |
    |  repeat until done           |
```

The tools handle the mechanics. You focus on what to build.
