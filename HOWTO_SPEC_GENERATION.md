# CDD HOWTO: Spec Generation

How to create feature specifications before CDD contracts.

Spec generation is a **pre-gate** activity. The frozen spec becomes the reference artifact that CDD contracts are written against.

```
┌─────────────────────────────────────────┐
│  SPEC GENERATION (this document)        │
│  Pre-CDD: Define what success looks like│
└─────────────────────────────────────────┘
                    │
                    ▼ frozen spec
┌─────────────────────────────────────────┐
│  CDD GATES                              │
│  G0 → G1 → G2 → G3                      │
│  Contracts reference the frozen spec    │
└─────────────────────────────────────────┘
```

---

## When You Need a Spec

**Use spec generation for:**
- Multi-component features (3+ files touched)
- Features requiring coordination between systems
- Anything with edge cases that need explicit handling
- Features where "done" isn't obvious

**Skip to contracts directly for:**
- Bug fixes with clear reproduction steps
- Single-file changes with obvious success criteria
- Refactors where tests already exist

---

## The Spec Document

Create `docs/FEATURE_SPEC.md` with this structure:

```markdown
---
status: draft
created: YYYY-MM-DD
author: AI1
reviewers: []
---

# Feature: [Name]

## Summary

One paragraph describing what this feature does and why.

## Requirements

| ID | Description | Priority |
|----|-------------|----------|
| R1 | [Functional requirement] | must |
| R2 | [Functional requirement] | must |
| R3 | [Nice-to-have] | should |

## Edge Cases

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| E1 | [Edge case description] | [What should happen] |
| E2 | [Edge case description] | [What should happen] |

## Constraints

- [Technical constraint]
- [Performance constraint]
- [Compatibility requirement]

## Not In Scope

- [Explicitly excluded feature]
- [Future work deferred]

## Success Criteria

How do we know this is done?

- [ ] [Measurable criterion]
- [ ] [Measurable criterion]

## Architecture Notes

Reference existing decisions:
- See DECISIONS.md#section for [relevant context]
- See BLUEPRINT.md for system overview
```

---

## R# and E# Format

Requirements and edge cases get IDs that flow through to contracts.

### Requirements (R#)

```markdown
| ID | Description | Priority |
|----|-------------|----------|
| R1 | CC messages route to correct parameter | must |
| R2 | Multiple MIDI devices supported simultaneously | must |
| R3 | Visual feedback shows CC activity | should |
```

**Priority values:**
- `must` — Feature incomplete without this
- `should` — Important but can ship without
- `could` — Nice to have if time permits

### Edge Cases (E#)

```markdown
| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| E1 | CC value 0 received | Parameter set to minimum |
| E2 | Device disconnected mid-session | Graceful degradation, no crash |
| E3 | Two devices send same CC simultaneously | Last-write-wins, no race |
```

---

## The Review Cycle

Specs require agreement between two AI sessions before freeze.

### Step 1: Draft (AI1)

Create the spec in your primary session:

```
1. Start conversation with project context
2. Request: "Create a feature spec for [description]"
3. Claude produces FEATURE_SPEC.md
4. Download and save to docs/
```

### Step 2: Review (AI2)

Open a fresh session for review:

```bash
# Zip project for handoff
zip -r project-for-review.zip . -x "*.git*" -x "node_modules/*" -x "__pycache__/*"
```

Upload to new session with prompt:

```
Review docs/FEATURE_SPEC.md. Check for:
- Missing requirements
- Unhandled edge cases  
- Contradictions
- Ambiguities
```

AI2 returns one of:
- **Accept** — Spec is complete
- **Accept with changes** — Minor additions needed
- **Reject** — Significant gaps, return to AI1

### Step 3: Iterate

If rejected or changes requested:

```
Back to AI1 with AI2's feedback:
"AI2 review identified: [issues]. Update spec."
```

Repeat Steps 2-3 until both sessions agree.

### Step 4: Freeze

When both sessions approve, update the spec header:

```markdown
---
status: frozen
created: YYYY-MM-DD
frozen: YYYY-MM-DD
author: AI1
reviewers: [AI2]
approvals: AI1 ✓ AI2 ✓
---
```

**Frozen means frozen.** Changes require the change control process.

---

## Change Control (Post-Freeze)

After freeze, changes require explicit approval:

```markdown
## Change Request CR001

**Date:** YYYY-MM-DD
**Reason:** [Why change is needed]

**Spec Impact:**
- R2: [Modified description]
- E4: [New edge case added]

**Test Impact:**
- T002 needs update
- T007 new test required

**Docs Impact:**
- README section 3.2 needs update

**Approvals:**
- AI1: ✓
- AI2: ✓

**Resolution:** Approved / Rejected
```

Append change requests to the spec document. Don't modify frozen content inline.

---

## From Spec to Contracts

The frozen spec becomes your reference for CDD contracts.

### Traceability

Each contract requirement references the spec:

```yaml
requirements:
  - id: R001
    description: CC messages route to correct parameter
    source_ref: FEATURE_SPEC#R1

  - id: R002
    description: Graceful handling when device disconnects
    source_ref: FEATURE_SPEC#E2
```

**source_ref format:** `SPEC_NAME#ID` where:
- `SPEC_NAME` is the spec filename without extension
- `#R1`, `#E2` etc. reference the requirement/edge case ID

### Coverage Matrix

Track which spec items have contract coverage:

| Spec ID | Contract | Test IDs | Status |
|---------|----------|----------|--------|
| R1 | midi_cc.yaml | T001, T002 | ✓ |
| R2 | midi_cc.yaml | T003 | ✓ |
| E1 | midi_cc.yaml | T004 | ✓ |
| E2 | midi_cc.yaml | T005 | ✓ |
| R3 | — | — | Deferred |

Fill this out during contract creation. It becomes the traceability matrix.

### Handoff to CDD

```
FEATURE_SPEC.md (frozen)
        │
        │  Spec is the reference artifact
        ▼
    Write contracts
    source_ref: FEATURE_SPEC#R1, #E2, etc.
        │
        ▼
    G0 → G1 → G2 → G3
    Normal CDD flow
```

The spec doesn't go through `cdd analyze` — it's human-readable and already structured. CDD gates start when you write contracts against it.

---

## Phased Rollout Plan

For complex features, break implementation into phases:

```markdown
## Rollout Plan

### Phase 1: Core Routing
**Implements:** R1, E1
**Verify:** `cdd test contracts/midi_cc.yaml --only T001,T002,T004`

### Phase 2: Multi-Device
**Implements:** R2, E2, E3  
**Verify:** `cdd test contracts/midi_cc.yaml --only T003,T005,T006`

### Phase 3: Visual Feedback
**Implements:** R3
**Verify:** `cdd test contracts/midi_cc.yaml --only T007`
```

Each phase:
- Maps to specific R#/E# items
- Has an explicit verification command
- Can be reviewed independently by AI2

---

## Session Handoff

### Minimal Handoff (quick question)

Copy/paste the relevant section of the spec.

### Standard Handoff (full review)

```bash
# Create zip excluding noise
zip -r project-for-review.zip . \
    -x "*.git*" \
    -x "node_modules/*" \
    -x "__pycache__/*" \
    -x "*.pyc" \
    -x "venv/*"
```

Upload to new session with specific review request.

### Full Context Handoff (complex iteration)

Include in your prompt:
- Current spec status (draft/frozen)
- What's been reviewed already
- Specific concerns or areas to focus on

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  SPEC GENERATION WORKFLOW                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Draft spec (AI1)                                        │
│     - R1..Rn requirements with priority                     │
│     - E1..En edge cases with expected behavior              │
│     - Constraints, success criteria                         │
│                                                             │
│  2. Review (AI2)                                            │
│     - Fresh session, zip handoff                            │
│     - Check gaps, contradictions, ambiguities               │
│                                                             │
│  3. Iterate until agreement                                 │
│     AI1 ↔ AI2 until both approve                            │
│                                                             │
│  4. Freeze                                                  │
│     status: frozen + approvals: AI1 ✓ AI2 ✓                 │
│                                                             │
│  5. Handoff to CDD                                          │
│     Write contracts with source_ref: SPEC#R1                │
│                                                             │
│  POST-FREEZE CHANGES:                                       │
│     Change Request → Both approve → Append to spec          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### Vague Requirements

**Wrong:**
```markdown
| R1 | System should be fast | must |
```

**Right:**
```markdown
| R1 | Response time < 100ms for CC routing | must |
```

Measurable beats subjective.

### Missing Edge Cases

**Wrong:**
```markdown
## Edge Cases
(none listed)
```

**Right:**
Think through:
- What if input is empty? Maximum? Invalid?
- What if external system fails?
- What about concurrent access?
- What happens at boundaries?

### Scope Creep After Freeze

**Wrong:**
> "While we're at it, let's also add feature X"

**Right:**
> File a change request. If approved, update spec formally. If not, create separate spec for feature X.

### Skipping AI2 Review

**Wrong:**
> "I'm confident in this spec, let's just freeze it"

**Right:**
> Fresh eyes catch blind spots. Always do the review cycle.

### Starting CDD Before Freeze

**Wrong:**
> "I'll write the contracts while we're still refining the spec"

**Right:**
> Freeze first. Contracts written against draft specs cause rework when the spec changes.

---

## When to Switch Sessions

**Switch from AI1 to AI2 when:**
- Draft is complete and ready for review
- Stuck on how to structure requirements
- Need validation of edge case coverage
- Spec feels circular or self-referential

**Switch from AI2 back to AI1 when:**
- Review complete with actionable feedback
- Agreement reached, ready to freeze
- Need to continue primary development

---

*Based on DUAL_AI_WORKFLOW.md v1.2*
*Pre-gate workflow for CDD SPEC.md v1.1.5*
