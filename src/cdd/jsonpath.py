# src/cdd/jsonpath.py
"""Minimal JSONPath resolver per spec."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass(frozen=True)
class PathResolution:
    """Result of JSONPath resolution."""
    ok: bool
    value: Any = None
    error: str | None = None  # "path_not_found" | "type_mismatch" | "invalid_path"


def resolve_jsonpath(root: Any, path: str) -> PathResolution:
    """
    Minimal JSONPath resolver per spec.
    
    Supports: $.key.key2[0].key3
    Missing path resolves to null (ok=True, value=None).
    No type coercion.
    """
    if path is None:
        return PathResolution(ok=True, value=None)

    if not isinstance(path, str) or not path.startswith("$."):
        return PathResolution(ok=False, error="invalid_path")

    tokens = _tokenize(path)
    if tokens and tokens[0] == ("invalid", None):
        return PathResolution(ok=False, error="invalid_path")

    cur = root

    for tok_type, tok_val in tokens:
        if tok_type == "key":
            if isinstance(cur, dict):
                if tok_val in cur:
                    cur = cur[tok_val]
                else:
                    return PathResolution(ok=True, value=None)  # missing => null
            else:
                return PathResolution(ok=False, error="type_mismatch")
        elif tok_type == "idx":
            if isinstance(cur, list):
                idx = tok_val
                if 0 <= idx < len(cur):
                    cur = cur[idx]
                else:
                    return PathResolution(ok=True, value=None)  # missing => null
            else:
                return PathResolution(ok=False, error="type_mismatch")

    return PathResolution(ok=True, value=cur)


def _tokenize(path: str) -> List[Tuple[str, Any]]:
    """Parse $.a.b[0].c into tokens."""
    # path begins with "$."
    s = path[2:]
    out: List[Tuple[str, Any]] = []
    i = 0
    buf = ""
    
    while i < len(s):
        ch = s[i]
        if ch == ".":
            if buf:
                out.append(("key", buf))
                buf = ""
            i += 1
            continue
        if ch == "[":
            if buf:
                out.append(("key", buf))
                buf = ""
            j = s.find("]", i)
            if j == -1:
                return [("invalid", None)]
            idx_str = s[i + 1 : j].strip()
            if not idx_str.lstrip("-").isdigit():
                return [("invalid", None)]
            out.append(("idx", int(idx_str)))
            i = j + 1
            continue
        buf += ch
        i += 1
    
    if buf:
        out.append(("key", buf))
    
    return out
