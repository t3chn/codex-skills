#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class RepoInfo:
    raw: str
    https: str | None
    ssh: str | None


_NON_NAME_CHARS = re.compile(r"[^a-z0-9-]+")


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("_", "-").replace(".", "-").replace("/", "-")
    value = _NON_NAME_CHARS.sub("-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "task"


def _run_capture(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True)
    except FileNotFoundError:
        raise RuntimeError(f"missing command: {cmd[0]}")
    except subprocess.CalledProcessError as exc:
        msg = exc.output.strip() if exc.output else ""
        raise RuntimeError(f"command failed: {' '.join(cmd)}{(': ' + msg) if msg else ''}")


def _try_git_origin() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        return out or None
    except Exception:
        return None


def _normalize_repo(remote: str) -> RepoInfo:
    remote = remote.strip()

    if remote.startswith("git@") and ":" in remote:
        # git@host:owner/repo(.git)
        user_host, path = remote.split(":", 1)
        host = user_host.split("@", 1)[-1]
        path = path.lstrip("/")
        https = f"https://{host}/{path}"
        return RepoInfo(raw=remote, https=https.removesuffix(".git"), ssh=remote)

    parsed = urlparse(remote)
    if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.path:
        host = parsed.netloc
        path = parsed.path.lstrip("/")
        ssh = f"git@{host}:{path}"
        https = f"{parsed.scheme}://{host}/{path}"
        return RepoInfo(raw=remote, https=https.removesuffix(".git"), ssh=ssh)

    return RepoInfo(raw=remote, https=None, ssh=None)


def _load_bead(bead_id: str) -> dict[str, Any]:
    raw = _run_capture(["bd", "show", bead_id, "--json"])
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"bd show returned invalid JSON: {exc.msg}") from exc
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"bd show returned empty result for {bead_id}")
    issue = data[0]
    if not isinstance(issue, dict):
        raise RuntimeError(f"bd show returned non-object issue for {bead_id}")
    return issue


def _build_prompt(repo: RepoInfo | None, issue: dict[str, Any]) -> str:
    bead_id = str(issue.get("id", "") or "").strip()
    title = str(issue.get("title", "") or "").strip()
    description = str(issue.get("description", "") or "").strip()
    acceptance = str(issue.get("acceptance_criteria", "") or "").strip()

    if not bead_id:
        raise RuntimeError("bead id is missing")
    if not title:
        title = bead_id
    if not description:
        raise RuntimeError(f"{bead_id}: bead description is empty (cannot generate a safe prompt)")

    repo_lines: list[str] = []
    if repo is not None:
        if repo.https:
            repo_lines.append(f"Repo: {repo.https}")
        if repo.ssh:
            repo_lines.append(f"RepoSSH: {repo.ssh}")
        if not repo_lines and repo.raw:
            repo_lines.append(f"Repo: {repo.raw}")

    header = "\n".join(repo_lines + [f"Bead: {bead_id}", f"Title: {title}"]).strip()

    parts: list[str] = []
    parts.append("You are a coding agent running inside a Coder Task workspace.")
    if header:
        parts.append("")
        parts.append(header)

    parts.append(
        "\n\nRules:\n"
        "- Follow the Beads spec exactly. Do ONLY the Must-Haves.\n"
        "- Do not add extra improvements; if you discover more work, create a new Beads issue and stop.\n"
        "- Work only in this repo.\n"
        "- Do not edit `.beads/*`.\n"
        "- Run the Verification commands from the spec and report results.\n"
    )

    parts.append("Beads Description:\n" + description)
    if acceptance:
        parts.append("\nAcceptance Criteria:\n" + acceptance)

    return "\n\n".join(parts).rstrip() + "\n"


def _create_task(prompt: str, *, template: str, preset: str, owner: str, name: str) -> str:
    cmd = [
        "coder",
        "task",
        "create",
        "--quiet",
        "--template",
        template,
        "--preset",
        preset,
        "--name",
        name,
        "--owner",
        owner,
        "--stdin",
    ]
    try:
        out = subprocess.check_output(cmd, input=prompt, text=True)
        return out.strip()
    except FileNotFoundError:
        raise RuntimeError("missing command: coder")
    except subprocess.CalledProcessError as exc:
        msg = exc.output.strip() if exc.output else ""
        raise RuntimeError(
            f"coder task create failed for {name!r} (exit {exc.returncode}){(': ' + msg) if msg else ''}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Spawn one Coder Task per Beads issue (orx workflow helper)."
    )
    parser.add_argument("bead_ids", nargs="+", help="Beads issue ids")
    parser.add_argument("--template", required=True, help="Coder task template name")
    parser.add_argument("--preset", default="none", help="Coder task preset (default: none)")
    parser.add_argument("--owner", default="me", help="Coder task owner (default: me)")
    parser.add_argument(
        "--name-prefix",
        default="",
        help="Prefix for generated task names (default: empty)",
    )
    parser.add_argument(
        "--repo",
        dest="repo_url",
        help="Repo remote URL to include in prompts (defaults to git origin, if available)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts and exit (do not create tasks).",
    )
    parser.add_argument(
        "--json",
        dest="json_out",
        action="store_true",
        help="Output a JSON mapping {bead_id: task_id}.",
    )
    args = parser.parse_args()

    try:
        repo_raw = (args.repo_url or "").strip() or _try_git_origin()
        repo = _normalize_repo(repo_raw) if repo_raw else None
    except Exception as exc:
        print(f"[ERROR] failed to detect repo: {exc}", file=sys.stderr)
        return 2

    mapping: dict[str, str] = {}
    prompts: dict[str, str] = {}

    try:
        for bead_id in args.bead_ids:
            issue = _load_bead(bead_id)
            prompts[bead_id] = _build_prompt(repo, issue)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        for bead_id in args.bead_ids:
            sys.stdout.write(f"\n--- {bead_id} ---\n")
            sys.stdout.write(prompts[bead_id])
        return 0

    try:
        for bead_id in args.bead_ids:
            name = _slugify(f"{args.name_prefix}{bead_id}")
            task_id = _create_task(
                prompts[bead_id],
                template=args.template,
                preset=args.preset,
                owner=args.owner,
                name=name,
            )
            mapping[bead_id] = task_id
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if args.json_out:
        sys.stdout.write(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")
        return 0

    for bead_id, task_id in mapping.items():
        sys.stdout.write(f"{bead_id}\t{task_id}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

