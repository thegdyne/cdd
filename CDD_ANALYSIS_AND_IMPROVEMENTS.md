# CDD Analysis and Improvement Proposal

**Date:** 2025-12-28  
**Based on:** CDD v1.1.3 codebase analysis  
**Problem Statement:** Contracts based on assumptions lead to iterative rework

---

## Part 1: Current State Analysis

### What CDD Does Well

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURRENT CDD PIPELINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   contracts/*.yaml  ──►  cdd lint  ──►  cdd test  ──►  report  │
│                              │              │                   │
│                              ▼              ▼                   │
│                      Schema valid?    Tests pass?               │
│                      Coverage OK?                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Implemented Features:**
- ✅ YAML schema validation (lint)
- ✅ Requirement coverage checking (every req needs ≥1 test)
- ✅ Multiple executors (python, shell, static, sclang)
- ✅ Assertion DSL (12 operators)
- ✅ JSONPath resolution
- ✅ Variable injection (`--var`)
- ✅ Static file scanning with regex assertions
- ✅ Spec version compatibility checking

**Code Quality:**
- Clean separation: cli.py → runner.py → executors → assertions
- Proper dataclasses (RunContext, StepResult, AssertionResult)
- Rich console output for human-readable reports
- JSON output for machine consumption

### The Gap: No Source Validation

The linter checks:
```python
# From lint/__init__.py
def _lint_component(...):
    required = ["contract", "version", "status", "description", 
                "runner", "requirements", "tests"]
    # ✅ Checks fields exist
    # ✅ Checks requirement coverage
    # ❌ Does NOT check if requirements are grounded in evidence
```

**What's missing:** There's no validation that requirements describe reality.

---

## Part 2: The Failure Mode (Pyro-Logger Case Study)

### What Happened

```
1. User: "Replicate this PDF form"
2. AI: *glances at PDF* → writes contract with "underlines for input fields"
3. Lint: ✅ PASS (schema valid, requirements covered)
4. Build: implements underlines
5. User: "Wrong! The original has boxes, not underlines"
6. Analysis: extract PDF images, discover actual layout
7. Fix contract, rebuild
```

**The lint passed because the contract was syntactically correct.**  
**The contract was semantically wrong because it wasn't validated against the source.**

### Root Cause

```yaml
# What was written (assumption)
- id: R010b
  description: Inline text fields have underlines
  acceptance_criteria:
    - Format is "LABEL:" followed by underline

# What should have been required
- id: R010b
  description: Input fields use rectangular boxes
  source_ref: analysis/page1_structure.json#element_E002  # ← MUST exist
  visual_ref: analysis/page1.png                          # ← MUST exist
  acceptance_criteria:
    - Rectangular bordered box at coordinates (95, 85, 295, 105)
```

---

## Part 3: Proposed Improvements

### 3.1 New Command: `cdd analyze`

Extract structured data from source artifacts before writing contracts.

```bash
# Analyze a PDF
cdd analyze sources/form.pdf --output analysis/

# Produces:
#   analysis/form_page1.png
#   analysis/form_page2.png  
#   analysis/form_structure.json
#   analysis/form_elements.yaml
```

**Implementation location:** `src/cdd/analyze/`

```python
# src/cdd/analyze/__init__.py
from pathlib import Path
from typing import Dict, Any

def analyze_source(source_path: Path, output_dir: Path) -> Dict[str, Any]:
    """
    Analyze a source artifact and produce structured output.
    
    Supported types:
    - PDF: extract images, detect rectangles/lines/text positions
    - Image: detect shapes, text regions
    - JSON/YAML: schema extraction
    - API: endpoint discovery (future)
    """
    suffix = source_path.suffix.lower()
    
    if suffix == '.pdf':
        from cdd.analyze.pdf import analyze_pdf
        return analyze_pdf(source_path, output_dir)
    elif suffix in ('.png', '.jpg', '.jpeg'):
        from cdd.analyze.image import analyze_image
        return analyze_image(source_path, output_dir)
    else:
        raise ValueError(f"Unsupported source type: {suffix}")
```

```python
# src/cdd/analyze/pdf.py
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, Any, List

def analyze_pdf(pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
    """Extract structure from PDF."""
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    
    result = {
        "source": str(pdf_path),
        "type": "pdf",
        "page_count": len(doc),
        "pages": []
    }
    
    for page_num, page in enumerate(doc):
        # Render page as image
        pix = page.get_pixmap(dpi=150)
        img_path = output_dir / f"page_{page_num + 1}.png"
        pix.save(str(img_path))
        
        # Extract elements
        page_data = {
            "page": page_num + 1,
            "image": str(img_path),
            "width": page.rect.width,
            "height": page.rect.height,
            "elements": []
        }
        
        # Extract drawings (rectangles, lines)
        for i, path in enumerate(page.get_drawings()):
            for item in path.get("items", []):
                if item[0] == "re":  # Rectangle
                    rect = item[1]
                    page_data["elements"].append({
                        "id": f"E{page_num+1}_{i}",
                        "type": "rectangle",
                        "bounds": {
                            "x": round(rect.x0, 1),
                            "y": round(rect.y0, 1),
                            "width": round(rect.width, 1),
                            "height": round(rect.height, 1)
                        }
                    })
        
        # Extract text with positions
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text:
                            page_data["elements"].append({
                                "id": f"T{page_num+1}_{len(page_data['elements'])}",
                                "type": "text",
                                "content": text,
                                "bounds": {
                                    "x": round(span["bbox"][0], 1),
                                    "y": round(span["bbox"][1], 1),
                                    "width": round(span["bbox"][2] - span["bbox"][0], 1),
                                    "height": round(span["bbox"][3] - span["bbox"][1], 1)
                                },
                                "font": span.get("font", ""),
                                "size": round(span.get("size", 0), 1)
                            })
        
        result["pages"].append(page_data)
    
    # Save structure
    import json
    structure_path = output_dir / "structure.json"
    with open(structure_path, "w") as f:
        json.dump(result, f, indent=2)
    
    doc.close()
    return result
```

---

### 3.2 New Contract Fields: `sources` and `source_ref`

**Schema additions:**

```yaml
# Project contract - new field
sources:
  - id: SRC001
    type: pdf
    file: sources/WeeklyPyrotechnicLog_4.pdf
    analysis: analysis/form/  # Output from cdd analyze
    description: Official form to replicate

# Component contract - requirements must cite sources
requirements:
  - id: R010b
    priority: must
    description: Input fields use rectangular boxes
    source_ref: SRC001#E1_5          # Required: element from analysis
    visual_ref: analysis/form/page_1.png  # Required for visual requirements
    acceptance_criteria:
      - Rectangular bordered box matching element E1_5 dimensions
```

**Lint additions:**

```python
# src/cdd/lint/__init__.py additions

def _lint_component(path, doc, errors, warnings, strict):
    # ... existing checks ...
    
    # NEW: Check source refs if sources defined
    sources = doc.get("sources", [])
    source_ids = {s["id"] for s in sources if isinstance(s, dict)}
    
    for r in doc.get("requirements", []):
        source_ref = r.get("source_ref")
        visual_ref = r.get("visual_ref")
        
        # If contract has sources, requirements should cite them
        if sources and not source_ref:
            warnings.append({
                "code": "missing_source_ref",
                "message": f"{path}: requirement {r.get('id')} has no source_ref"
            })
        
        # Validate source_ref format and existence
        if source_ref:
            ref_source = source_ref.split("#")[0]
            if ref_source not in source_ids:
                errors.append({
                    "code": "invalid_source_ref", 
                    "message": f"{path}: source_ref '{ref_source}' not in sources"
                })
        
        # Validate visual_ref file exists
        if visual_ref:
            visual_path = path.parent / visual_ref
            if not visual_path.exists():
                errors.append({
                    "code": "missing_visual_ref",
                    "message": f"{path}: visual_ref '{visual_ref}' not found"
                })
```

---

### 3.3 New Lint Rules: Assumption Detection

Detect vague language that indicates assumptions rather than evidence:

```python
# src/cdd/lint/assumption_detector.py

ASSUMPTION_PATTERNS = [
    (r'\bmatches?\s+(the\s+)?original\b', "Use source_ref instead of 'matches original'"),
    (r'\bsimilar\s+to\b', "Use source_ref with specific element"),
    (r'\blike\s+the\b', "Cite specific source element"),
    (r'\bappropriate\b', "Define specific criteria"),
    (r'\bcorrect\s+(position|layout|format)\b', "Specify coordinates or source_ref"),
    (r'\bstandard\b', "Define the standard explicitly"),
]

def check_assumption_language(text: str) -> List[Dict[str, str]]:
    """Detect vague language that suggests assumptions."""
    import re
    warnings = []
    for pattern, suggestion in ASSUMPTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            warnings.append({
                "code": "assumption_language",
                "message": f"Vague language detected: {suggestion}",
                "pattern": pattern
            })
    return warnings
```

---

### 3.4 New Command: `cdd validate`

Deep validation that requirements are grounded:

```bash
cdd validate contracts/

# Output:
# ✓ R001: source_ref SRC001#E1_5 exists in analysis/form/structure.json
# ✓ R001: visual_ref analysis/form/page_1.png exists
# ✓ R002: source_ref SRC001#E1_8 exists
# ⚠ R003: no source_ref (requirement may be based on assumption)
# ✗ R004: source_ref SRC001#E99 not found in structure.json
```

```python
# src/cdd/validate.py

def validate_source_refs(contracts_path: Path) -> Dict[str, Any]:
    """
    Validate that all source_refs point to existing analysis artifacts.
    """
    results = {
        "ok": True,
        "validated": [],
        "warnings": [],
        "errors": []
    }
    
    # Load all contracts
    for contract_path in contracts_path.rglob("*.yaml"):
        doc = yaml.safe_load(contract_path.read_text())
        if "contract" not in doc:
            continue
            
        sources = {s["id"]: s for s in doc.get("sources", [])}
        
        for req in doc.get("requirements", []):
            req_id = req.get("id")
            source_ref = req.get("source_ref")
            visual_ref = req.get("visual_ref")
            
            if source_ref:
                # Parse ref: SRC001#E1_5
                parts = source_ref.split("#")
                source_id = parts[0]
                element_id = parts[1] if len(parts) > 1 else None
                
                if source_id not in sources:
                    results["errors"].append({
                        "req": req_id,
                        "error": f"Source {source_id} not defined"
                    })
                    results["ok"] = False
                else:
                    # Check element exists in analysis
                    analysis_dir = sources[source_id].get("analysis")
                    if analysis_dir and element_id:
                        structure_file = contract_path.parent / analysis_dir / "structure.json"
                        if structure_file.exists():
                            structure = json.loads(structure_file.read_text())
                            all_elements = []
                            for page in structure.get("pages", []):
                                all_elements.extend(e["id"] for e in page.get("elements", []))
                            
                            if element_id not in all_elements:
                                results["errors"].append({
                                    "req": req_id,
                                    "error": f"Element {element_id} not in {structure_file}"
                                })
                                results["ok"] = False
                            else:
                                results["validated"].append({
                                    "req": req_id,
                                    "source_ref": source_ref,
                                    "status": "valid"
                                })
            else:
                results["warnings"].append({
                    "req": req_id,
                    "warning": "No source_ref - may be assumption-based"
                })
    
    return results
```

---

### 3.5 Updated CLI

```python
# src/cdd/cli.py additions

# cdd analyze
p_analyze = sub.add_parser("analyze", help="Analyze source artifacts")
p_analyze.add_argument("source", help="Source file (PDF, image, etc.)")
p_analyze.add_argument("--output", "-o", default="analysis/", help="Output directory")

# cdd validate  
p_validate = sub.add_parser("validate", help="Validate source references")
p_validate.add_argument("path", nargs="?", default="contracts", help="Contracts directory")
p_validate.add_argument("--json", action="store_true")
p_validate.add_argument("--strict", action="store_true", help="Fail on warnings")
```

---

## Part 4: Updated Workflow

### Before (Assumption-Based)

```
User Request → AI Writes Contract → Lint (schema only) → Build → Wrong → Fix → Repeat
```

### After (Source-First)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SOURCE-FIRST CDD WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. ACQUIRE                                                                 │
│     User provides source artifacts (PDFs, images, API specs, etc.)          │
│                                                                             │
│  2. ANALYZE                                                                 │
│     $ cdd analyze sources/form.pdf --output analysis/                       │
│     → Produces: structure.json, page images, element catalog                │
│                                                                             │
│  3. WRITE CONTRACT                                                          │
│     Requirements MUST cite source_ref from analysis                         │
│     Visual requirements MUST include visual_ref                             │
│                                                                             │
│  4. VALIDATE                                                                │
│     $ cdd validate contracts/                                               │
│     → Checks all source_refs exist in analysis artifacts                    │
│     → Warns on requirements without source_refs                             │
│                                                                             │
│  5. LINT                                                                    │
│     $ cdd lint contracts/                                                   │
│     → Schema validation + coverage + assumption language detection          │
│                                                                             │
│  6. BUILD                                                                   │
│     Implementation guided by source_refs and analysis artifacts             │
│                                                                             │
│  7. TEST                                                                    │
│     $ cdd test contracts/                                                   │
│     → Tests can reference same analysis for comparison                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 5: Implementation Roadmap

### Phase 0: Source-First Foundation (NEW)

| Item | Effort | Impact | Notes |
|------|--------|--------|-------|
| `cdd analyze` for PDFs | 2 days | High | Uses PyMuPDF, extracts images + structure |
| `source_ref` field | 1 day | High | Schema addition, optional initially |
| `visual_ref` validation | 0.5 day | High | File existence check in lint |
| `cdd validate` command | 1 day | High | Deep source_ref validation |
| Assumption language lint | 0.5 day | Medium | Regex patterns for vague words |

### Integration with Existing Phases

The new Phase 0 becomes a prerequisite. Existing phases remain:

- **Phase 1 (MVP):** Add source_ref support to lint
- **Phase 2 (Production):** `cdd analyze` supports images, APIs
- **Phase 3 (Polish):** Visual diff testing against analysis

---

## Part 6: Contract Schema Changes

### New Top-Level Field: `sources`

```yaml
# contracts/project.yaml
project: pyro-logger
cdd_spec: 1.2.0
version: 1.0.0
status: draft

sources:  # NEW
  - id: SRC001
    type: pdf
    file: sources/WeeklyPyrotechnicLog_4.pdf
    analysis: analysis/form/
    description: Official form to replicate
    
  - id: SRC002
    type: image
    file: sources/brothers_screenshot.png
    description: Reference for saved entries UI

# ... rest of contract
```

### New Requirement Fields

```yaml
requirements:
  - id: R010b
    priority: must
    description: Input fields use rectangular boxes
    source_ref: SRC001#E1_5      # NEW: Required for grounded requirements
    visual_ref: analysis/form/page_1.png  # NEW: Required for visual requirements
    region: {x: 95, y: 85, w: 200, h: 20}  # NEW: Optional specific coordinates
    acceptance_criteria:
      - Bordered rectangle matching source element E1_5
```

### Lint Behavior

| Contract Status | source_ref Missing | visual_ref Missing (visual req) |
|-----------------|-------------------|--------------------------------|
| draft | Warning | Warning |
| frozen | Warning (strict=Error) | Error |

---

## Part 7: Example - How This Prevents Our Failure

### Without Source-First (What Happened)

```yaml
# AI writes based on assumption
- id: R010b
  description: Inline text fields have underlines
  acceptance_criteria:
    - Format is "LABEL:" followed by underline
```

```bash
$ cdd lint contracts/
✅ PASS  # Schema valid, coverage OK

$ cdd test contracts/
# ... builds wrong thing
```

### With Source-First (What Should Happen)

```bash
# Step 1: Analyze source
$ cdd analyze sources/WeeklyPyrotechnicLog_4.pdf --output analysis/form/

Analyzing: sources/WeeklyPyrotechnicLog_4.pdf
  Page 1: 47 elements (23 rectangles, 24 text blocks)
  Page 2: 38 elements (15 rectangles, 23 text blocks)
Output: analysis/form/
  - page_1.png
  - page_2.png
  - structure.json
```

```yaml
# Step 2: Write contract citing analysis
sources:
  - id: SRC001
    type: pdf
    file: sources/WeeklyPyrotechnicLog_4.pdf
    analysis: analysis/form/

requirements:
  - id: R010b
    description: Input fields use rectangular boxes  # Correct!
    source_ref: SRC001#E1_5  # Points to actual rectangle in structure.json
    visual_ref: analysis/form/page_1.png
    acceptance_criteria:
      - Rectangular bordered box at element E1_5 position
```

```bash
# Step 3: Validate refs exist
$ cdd validate contracts/
✅ R010b: source_ref SRC001#E1_5 found in structure.json
✅ R010b: visual_ref analysis/form/page_1.png exists

# Step 4: Lint
$ cdd lint contracts/
✅ PASS

# Step 5: Build - now building the right thing
```

**The key difference:** Before writing "underlines," I would have run `cdd analyze` which would have shown rectangles in `structure.json`. The contract would have been correct from the start.

---

## Summary

| Problem | Solution |
|---------|----------|
| Contracts based on assumptions | `cdd analyze` extracts evidence first |
| No source validation | `source_ref` field links requirements to artifacts |
| Visual specs in prose | `visual_ref` + region coordinates |
| Vague language passes lint | Assumption language detection |
| Late discovery of errors | `cdd validate` catches missing refs early |

**The core principle:** You can't write a requirement until you've analyzed the source. The tooling enforces this by requiring source_refs that point to analysis artifacts.
