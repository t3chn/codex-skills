#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import sys


CYRILLIC_RE = re.compile(r"[\u0400-\u052F\u2DE0-\u2DFF\uA640-\uA69F]")


def iter_markdown_files(skills_dir: pathlib.Path) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for skill_dir in skills_dir.glob("vi-*"):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            files.append(skill_md)
        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            files.extend([p for p in refs_dir.rglob("*.md") if p.is_file()])
    return sorted(set(files))


def check_file(path: pathlib.Path) -> list[tuple[int, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[tuple[int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if CYRILLIC_RE.search(line):
            issues.append((idx, line.strip()))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail if skill instructions contain Cyrillic characters (enforce English-only docs)."
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

    md_files = iter_markdown_files(skills_dir)
    if not md_files:
        print(f"[WARN] no skill markdown files found under: {skills_dir}", file=sys.stderr)
        return 0

    failed = False
    for md in md_files:
        issues = check_file(md)
        if not issues:
            continue
        failed = True
        rel = md.relative_to(skills_dir.parent)
        print(f"[FAIL] Non-English (Cyrillic) text detected in: {rel}", file=sys.stderr)
        for lineno, line in issues[:20]:
            print(f"  L{lineno}: {line}", file=sys.stderr)
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more lines", file=sys.stderr)

    if failed:
        print(
            "\nFix: translate skill docs to English (SKILL.md + references/*.md), then re-run.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

