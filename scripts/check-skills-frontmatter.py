#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import sys


DOUBLE_QUOTED_RE = re.compile(r'^"([^"\\\\]|\\\\.)*"$')
SINGLE_QUOTED_RE = re.compile(r"^'([^']|'')*'$")
BLOCK_SCALAR_HEADER_RE = re.compile(r"^[>|]([+-]?\\d?)$")
KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")


def iter_skill_dirs(skills_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted([p for p in skills_dir.glob("vi-*") if p.is_dir()])


def _unquote_scalar(value: str) -> str:
    value = value.strip()
    if DOUBLE_QUOTED_RE.match(value):
        inner = value[1:-1]
        # Minimal unescape for our use-cases (name comparisons).
        inner = inner.replace(r"\\", "\\").replace(r"\"", '"')
        return inner
    if SINGLE_QUOTED_RE.match(value):
        inner = value[1:-1]
        return inner.replace("''", "'")
    return value


def _extract_front_matter_lines(
    text: str,
) -> tuple[list[str] | None, int | None, str | None]:
    lines = text.splitlines()
    if not lines:
        return None, None, "empty file"

    first = lines[0].lstrip("\ufeff").strip()
    if first != "---":
        return None, None, "missing opening '---' YAML front matter delimiter"

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            # YAML front matter is lines[1:idx]; content starts at idx+1.
            # YAML content starts at 1-based line 2.
            return lines[1:idx], 2, None

    return None, None, "missing closing '---' YAML front matter delimiter"


def validate_skill_file(skill_dir: pathlib.Path) -> list[tuple[int, str]]:
    issues: list[tuple[int, str]] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [(1, "missing SKILL.md")]

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    yaml_lines, start_lineno, err = _extract_front_matter_lines(text)
    if err is not None or yaml_lines is None or start_lineno is None:
        return [(1, err or "invalid YAML front matter")]

    fields: dict[str, str] = {}
    i = 0
    while i < len(yaml_lines):
        line = yaml_lines[i]
        lineno = start_lineno + i

        if "\t" in line:
            issues.append((lineno, "tabs are not allowed in YAML front matter"))
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        match = KEY_VALUE_RE.match(line)
        if not match:
            issues.append((lineno, "invalid YAML front matter line (expected 'key: value')"))
            i += 1
            continue

        key = match.group(1)
        value = match.group(2).strip()

        if value and BLOCK_SCALAR_HEADER_RE.match(value):
            # Consume indented block scalar content until next top-level key.
            i += 1
            while i < len(yaml_lines):
                next_line = yaml_lines[i]
                if next_line.strip() == "":
                    i += 1
                    continue
                if KEY_VALUE_RE.match(next_line) and not next_line.startswith((" ", "\t")):
                    break
                if not next_line.startswith((" ", "\t")):
                    issues.append(
                        (start_lineno + i, f"block scalar content for '{key}' must be indented")
                    )
                    break
                i += 1
            fields[key] = "<block>"
            continue

        if key == "description":
            if not (DOUBLE_QUOTED_RE.match(value) or SINGLE_QUOTED_RE.match(value)):
                issues.append(
                    (
                        lineno,
                        "description must be quoted (e.g. description: \"...\") or use a |/> block scalar",
                    )
                )

        is_quoted = bool(DOUBLE_QUOTED_RE.match(value) or SINGLE_QUOTED_RE.match(value))
        if value and not is_quoted and ": " in value:
            issues.append(
                (
                    lineno,
                    f"unquoted value for '{key}' contains ': ' (quote it to keep YAML valid)",
                )
            )

        if key in fields:
            issues.append((lineno, f"duplicate key '{key}' in YAML front matter"))
        fields[key] = value
        i += 1

    for required in ("name", "description"):
        if not fields.get(required):
            issues.append((start_lineno, f"missing required '{required}' in YAML front matter"))

    name_value = _unquote_scalar(fields.get("name", ""))
    if name_value and name_value != skill_dir.name:
        issues.append(
            (
                start_lineno,
                f"front matter name '{name_value}' does not match directory '{skill_dir.name}'",
            )
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate SKILL.md YAML front matter for each skill directory."
    )
    parser.add_argument(
        "--skills-dir",
        default=str(pathlib.Path(__file__).resolve().parent.parent / "skills"),
        help="Path to the skills directory (default: repo_root/skills).",
    )
    args = parser.parse_args()

    skills_dir = pathlib.Path(args.skills_dir).expanduser().resolve()
    if not skills_dir.is_dir():
        print(f"[ERROR] skills dir not found: {skills_dir}", file=sys.stderr)
        return 2

    skill_dirs = iter_skill_dirs(skills_dir)
    if not skill_dirs:
        print(f"[WARN] no skill directories found under: {skills_dir}", file=sys.stderr)
        return 0

    failed = False
    for skill_dir in skill_dirs:
        issues = validate_skill_file(skill_dir)
        if not issues:
            continue
        failed = True
        rel = (skill_dir / "SKILL.md").relative_to(skills_dir.parent)
        print(f"[FAIL] Invalid SKILL.md YAML front matter: {rel}", file=sys.stderr)
        for lineno, msg in issues[:20]:
            print(f"  L{lineno}: {msg}", file=sys.stderr)
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more issue(s)", file=sys.stderr)

    if failed:
        print("\nFix: ensure SKILL.md has valid YAML front matter and re-run.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
