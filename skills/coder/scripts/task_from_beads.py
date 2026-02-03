#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
        raise RuntimeError("bd show returned empty result")
    issue = data[0]
    if not isinstance(issue, dict):
        raise RuntimeError("bd show returned non-object issue")
    return issue


def build_prompt(repo: RepoInfo | None, issue: dict[str, Any]) -> str:
    bead_id = str(issue.get("id", "") or "").strip()
    title = str(issue.get("title", "") or "").strip()
    description = str(issue.get("description", "") or "").strip()
    acceptance = str(issue.get("acceptance_criteria", "") or "").strip()

    if not bead_id:
        raise RuntimeError("bead id is missing")
    if not title:
        title = bead_id
    if not description:
        raise RuntimeError("bead description is empty (cannot generate a safe prompt)")

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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a Coder Task from a Beads issue (anti-drift wrapper prompt)."
    )
    parser.add_argument("bead_id", help="Beads issue id (e.g. repo-abc)")
    parser.add_argument("--template", required=True, help="Coder task template name")
    parser.add_argument("--preset", default="none", help="Coder task preset (default: none)")
    parser.add_argument("--name", help="Coder task name (default: bead id)")
    parser.add_argument("--owner", default="me", help="Coder task owner (default: me)")
    parser.add_argument(
        "--repo",
        dest="repo_url",
        help="Repo remote URL to include in prompt (defaults to git origin, if available)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated prompt and exit (do not create a task).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the created task's ID (passes --quiet to coder).",
    )
    args = parser.parse_args()

    try:
        issue = _load_bead(args.bead_id)
        repo_raw = (args.repo_url or "").strip() or _try_git_origin()
        repo = _normalize_repo(repo_raw) if repo_raw else None
        prompt = build_prompt(repo, issue)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        sys.stdout.write(prompt)
        return 0

    task_name = args.name or args.bead_id

    cmd = [
        "coder",
        "task",
        "create",
        "--template",
        args.template,
        "--preset",
        args.preset,
        "--name",
        task_name,
        "--owner",
        args.owner,
        "--stdin",
    ]
    if args.quiet:
        cmd.insert(cmd.index("create") + 1, "--quiet")

    try:
        subprocess.run(cmd, input=prompt, text=True, check=True)
        return 0
    except FileNotFoundError:
        print("[ERROR] missing command: coder", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"[ERROR] coder task create failed (exit {exc.returncode})", file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())

