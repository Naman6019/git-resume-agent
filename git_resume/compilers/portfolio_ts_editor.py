"""
Safe, field-level editing of the portfolio site's `portfolioProjects` array
(src/content/portfolio.ts). Never does a blind string overwrite of a project
entry -- it locates the object literal for a given `slug` by brace-matching,
then replaces only the specific fields it was asked to change, preserving
everything else (formatting included) byte-for-byte.
"""
import json
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

TEXT_FIELDS = ["summary", "problem", "build", "outcome", "limitations"]


class ProjectBlockNotFound(Exception):
    pass


def _find_block(source: str, slug: str) -> Tuple[int, int]:
    """Returns (start, end) indices (inclusive) of the `{ ... }` object literal
    for the entry whose `slug` field matches, by brace-matching from that
    entry's own opening brace (the nearest `{` before the `slug:` line -- safe
    given every entry in portfolioProjects opens with `{` immediately before
    its `slug` field, with no other object literal in between)."""
    slug_match = re.search(r'slug:\s*"' + re.escape(slug) + r'"', source)
    if not slug_match:
        raise ProjectBlockNotFound(f"No project with slug '{slug}' found")

    start = source.rfind("{", 0, slug_match.start())
    if start == -1:
        raise ProjectBlockNotFound(f"Could not locate opening brace for slug '{slug}'")

    depth = 0
    for i in range(start, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return start, i

    raise ProjectBlockNotFound(f"Unbalanced braces while scanning entry for slug '{slug}'")


def extract_current_fields(source: str, slug: str) -> Dict[str, Any]:
    """Reads the current field values for a project entry without modifying anything."""
    start, end = _find_block(source, slug)
    block = source[start : end + 1]

    fields: Dict[str, Any] = {}
    for field in TEXT_FIELDS:
        m = re.search(rf'{field}:\s*\n?\s*"((?:[^"\\]|\\.)*)"', block)
        if m:
            fields[field] = m.group(1)

    stack_m = re.search(r"stack:\s*\[([^\]]*)\]", block)
    if stack_m:
        fields["stack"] = [s.strip().strip('"') for s in stack_m.group(1).split(",") if s.strip()]

    return fields


def apply_field_updates(source: str, slug: str, updates: Dict[str, Any]) -> str:
    """Returns a new copy of `source` with only the given fields updated inside
    the entry matching `slug`. `updates` keys are a subset of TEXT_FIELDS plus
    optionally "stack" (a list of strings). Unknown keys are ignored."""
    start, end = _find_block(source, slug)
    block = source[start : end + 1]

    for field in TEXT_FIELDS:
        if field not in updates:
            continue
        new_literal = json.dumps(updates[field])
        pattern = re.compile(rf'({field}:\s*\n?\s*)"(?:[^"\\]|\\.)*"')
        block, n = pattern.subn(lambda m: m.group(1) + new_literal, block, count=1)
        if n == 0:
            raise ProjectBlockNotFound(f"Field '{field}' not found in entry for slug '{slug}'")

    if "stack" in updates:
        new_stack_literal = "stack: [" + ", ".join(json.dumps(s) for s in updates["stack"]) + "]"
        pattern = re.compile(r"stack:\s*\[[^\]]*\]")
        block, n = pattern.subn(new_stack_literal, block, count=1)
        if n == 0:
            raise ProjectBlockNotFound(f"'stack' field not found in entry for slug '{slug}'")

    return source[:start] + block + source[end + 1 :]


def validate_typescript(repo_path: str, timeout: int = 120) -> Tuple[bool, str]:
    """Runs `npx tsc --noEmit` in repo_path. Returns (ok, message). This is the
    final safety gate before any edited portfolio.ts is committed -- a syntax
    or type error here means the edit is rejected outright, never pushed."""
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=repo_path,
            text=True,
            capture_output=True,
            timeout=timeout,
            shell=True,
        )
        if result.returncode == 0:
            return True, "tsc --noEmit passed"
        return False, (result.stdout + result.stderr).strip()[-2000:]
    except subprocess.TimeoutExpired:
        return False, f"tsc --noEmit timed out after {timeout}s"
    except Exception as e:
        return False, str(e)
