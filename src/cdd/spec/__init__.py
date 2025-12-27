# src/cdd/spec/__init__.py
"""Spec and version loading utilities."""
from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.parent.parent


def get_tool_version() -> str:
    """Read version from VERSION file."""
    version_file = _REPO_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    # Fallback: read from pyproject.toml or hardcode
    return "1.1.3"


def load_schema_version() -> str:
    """Return the report schema version (coupled to spec version for v1.x)."""
    v = get_tool_version()
    parts = v.split(".")
    # Schema version is major.minor (e.g., "1.1")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else "1.0"


def load_spec_text() -> str:
    """Load the full SPEC.md text."""
    spec_file = _REPO_ROOT / "SPEC.md"
    if spec_file.exists():
        return spec_file.read_text(encoding="utf-8")
    return "(SPEC.md not found)"
