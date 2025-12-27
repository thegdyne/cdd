# src/cdd/spec/__init__.py
"""Spec and version loading utilities."""
from __future__ import annotations
from importlib import metadata
from pathlib import Path


def get_tool_version() -> str:
    """Get version from installed package metadata."""
    try:
        return metadata.version("cdd")
    except metadata.PackageNotFoundError:
        # Development mode - try VERSION file
        version_file = Path(__file__).parent.parent.parent.parent / "VERSION"
        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()
        return "0.0.0"


def load_schema_version() -> str:
    """Return the report schema version (coupled to spec version for v1.x)."""
    v = get_tool_version()
    parts = v.split(".")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else "1.0"


def load_spec_text() -> str:
    """Load the full SPEC.md text."""
    # Try installed package data first
    try:
        from importlib.resources import files
        return files("cdd.spec").joinpath("SPEC.md").read_text(encoding="utf-8")
    except (ImportError, FileNotFoundError, TypeError):
        pass
    # Fallback to repo root
    spec_file = Path(__file__).parent.parent.parent.parent / "SPEC.md"
    if spec_file.exists():
        return spec_file.read_text(encoding="utf-8")
    return "(SPEC.md not found)"
