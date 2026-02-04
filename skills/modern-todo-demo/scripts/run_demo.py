#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_ROOT / "assets"
TODO_ASSETS_DIR = ASSETS_DIR / "todo-app"
REPO_ASSETS_DIR = ASSETS_DIR / "repo"

PR_URL_RE = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/pull/\d+")


class CmdError(RuntimeError):
    pass


def _strip_leading_warnings(text: str) -> str:
    start = text.find("{")
    if start == -1:
        return text.strip()
    return text[start:].strip()


def run(
    args: list[str],
    *,
    check: bool = True,
    capture: bool = True,
    input_text: str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        args,
        input=input_text,
        text=True,
        capture_output=capture,
        env=env,
    )
    if check and proc.returncode != 0:
        raise CmdError(
            "\n".join(
                [
                    f"command failed: {shlex.join(args)}",
                    f"exit code: {proc.returncode}",
                    f"stdout:\n{proc.stdout}",
                    f"stderr:\n{proc.stderr}",
                ]
            )
        )
    return proc


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_tools() -> None:
    missing = [tool for tool in ("coder", "gh") if shutil.which(tool) is None]
    if missing:
        raise CmdError(f"Missing required CLI tools: {', '.join(missing)}")


def gh_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(base or os.environ)
    env.setdefault("GH_PROMPT_DISABLED", "1")
    env.setdefault("GH_NO_UPDATE_NOTIFIER", "1")
    env.setdefault("GH_SPINNER_DISABLED", "1")
    return env


def preflight(template: str, org: str | None) -> None:
    run(["coder", "whoami"], check=True, capture=True)
    run(["gh", "auth", "status"], check=True, capture=True, env=gh_env())

    # Fail fast if the template doesn't exist.
    tpl_list = run(["coder", "templates", "list"], check=True, capture=True).stdout
    if template not in tpl_list:
        raise CmdError(f"Coder template not found: {template}")

    if org:
        # Validate org is accepted by coder CLI; this will error if invalid.
        run(["coder", "task", "create", "--help"], check=True, capture=True)


def get_github_login() -> str:
    proc = run(["gh", "api", "user", "--jq", ".login"], check=True, capture=True, env=gh_env())
    login = proc.stdout.strip()
    if not login:
        raise CmdError("Unable to determine GitHub login via `gh api user`.")
    return login


def create_repo(owner: str, repo_name: str, public: bool) -> tuple[str, str]:
    full = f"{owner}/{repo_name}"
    args = ["gh", "repo", "create", full, "--confirm", "--add-readme"]
    args.append("--public" if public else "--private")
    run(args, check=True, capture=True, env=gh_env())
    url = f"https://github.com/{full}"
    return full, url


def build_git_auth_note() -> str:
    return """Git auth note (important):
- The Task environment may override git askpass/external-auth.
- Workaround: create /tmp/git-askpass and ALWAYS override askpass in the same command:

  export GIT_TERMINAL_PROMPT=0
  cat >/tmp/git-askpass <<'SH'
  #!/bin/sh
  case "$1" in
    Username*) echo "x-access-token" ;;
    Password*) echo "$GITHUB_TOKEN" ;;
    *) echo "" ;;
  esac
  SH
  chmod +x /tmp/git-askpass

  Then prefix git commands with:
  GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git ...
"""


def build_prompt_ui(repo_url: str, repo_dir: str, branch: str) -> str:
    index_html = read_text(TODO_ASSETS_DIR / "index.html")
    app_js = read_text(TODO_ASSETS_DIR / "app.js")
    style_css = read_text(TODO_ASSETS_DIR / "style.css")
    repo_full = repo_url.split("https://github.com/", 1)[1]

    return f"""You are running inside a Coder Task with Claude Code.

Goal: Add a modern, dependency-free, single-user Todo web app (static HTML/CSS/JS + localStorage) to this repo on a feature branch and open a PR.

Repo:
- URL: {repo_url}.git
- Work directory: {repo_dir}
- Base branch: main
- Feature branch: {branch}

Constraints:
- Do NOT add GitHub Actions / workflows.
- Do NOT add package.json or dependencies.
- Only create/modify these files: index.html, app.js, style.css.

{build_git_auth_note()}

Steps:
1) Ensure the repo is cloned to the absolute path {repo_dir} (don’t rely on cwd):
   - `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git clone {repo_url}.git {repo_dir}`
2) `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git -C {repo_dir} fetch --prune origin`
3) `git -C {repo_dir} checkout main && git -C {repo_dir} reset --hard origin/main`
4) `git -C {repo_dir} checkout -B {branch}`
5) Write files with EXACT contents:

index.html:
```html
{index_html}
```

app.js:
```js
{app_js}
```

style.css:
```css
{style_css}
```

6) Quick self-check (serve the repo dir, then stop):
   - `(python3 -m http.server 8000 --bind 127.0.0.1 --directory {repo_dir} >/tmp/http.log 2>&1 & pid=$!; sleep 1; curl -fsS --max-time 3 http://127.0.0.1:8000/ >/dev/null; kill \"$pid\" || true)`

7) Commit + PR:
   - `git -C {repo_dir} add -A`
   - `git -C {repo_dir} commit -m "feat: add modern todo app"`
   - `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git -C {repo_dir} push -u origin {branch}`
   - `gh pr create --repo {repo_full} --base main --head {branch} --title "Add modern Todo app" --body "Adds a modern static Todo app (HTML/CSS/JS) with localStorage."`

Output:
- Print the PR URL.
"""


def build_prompt_meta(repo_url: str, repo_dir: str, branch: str) -> str:
    readme = read_text(REPO_ASSETS_DIR / "README.md")
    gitignore = read_text(REPO_ASSETS_DIR / "gitignore")
    repo_full = repo_url.split("https://github.com/", 1)[1]

    return f"""You are running inside a Coder Task with Claude Code.

Goal: Add repo metadata/docs on a feature branch and open a PR.

Repo:
- URL: {repo_url}.git
- Work directory: {repo_dir}
- Base branch: main
- Feature branch: {branch}

Constraints:
- Do NOT add GitHub Actions / workflows.
- Only create/modify: README.md, .gitignore.

{build_git_auth_note()}

Steps:
1) Ensure the repo is cloned to the absolute path {repo_dir}:
   - If `{repo_dir}/.git` does not exist, run:
     `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git clone {repo_url}.git {repo_dir}`
2) `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git -C {repo_dir} fetch --prune origin`
3) `git -C {repo_dir} checkout main && git -C {repo_dir} reset --hard origin/main`
4) `git -C {repo_dir} checkout -B {branch}`
5) Write files with EXACT contents:

README.md:
```md
{readme}
```

.gitignore:
```gitignore
{gitignore}
```

6) Commit + PR:
   - `git -C {repo_dir} add -A`
   - `git -C {repo_dir} commit -m "chore: add README and gitignore"`
   - `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git -C {repo_dir} push -u origin {branch}`
   - `gh pr create --repo {repo_full} --base main --head {branch} --title "Add repo docs" --body "Adds README and .gitignore for the Todo demo repo."`

Output:
- Print the PR URL.
"""


def coder_task_create(prompt: str, *, template: str, org: str | None, name: str) -> str:
    args = ["coder", "task", "create", "--template", template, "--name", name, "--quiet", "--stdin"]
    if org:
        args = ["coder", "task", "create", "--org", org, "--template", template, "--name", name, "--quiet", "--stdin"]
    out = run(args, check=True, capture=True, input_text=prompt).stdout.strip()
    task_id = out.splitlines()[-1].strip()
    if not task_id:
        raise CmdError("coder task create returned empty task id")
    return task_id


def coder_task_status(task_id: str) -> dict:
    raw = run(["coder", "task", "status", task_id, "-o", "json"], check=True, capture=True).stdout
    json_text = _strip_leading_warnings(raw)
    return json.loads(json_text)


def coder_task_logs(task_id: str) -> str:
    return run(["coder", "task", "logs", task_id], check=True, capture=True).stdout


def wait_for_pr_urls(task_ids: dict[str, str], timeout_s: int) -> dict[str, str]:
    start = time.time()
    pr_urls: dict[str, str] = {}
    last_line: dict[str, str] = {}

    while True:
        elapsed = int(time.time() - start)
        if elapsed > timeout_s:
            raise CmdError(f"Timed out waiting for tasks after {timeout_s}s")

        done = True
        for label, task_id in task_ids.items():
            if label in pr_urls:
                continue

            status = coder_task_status(task_id)
            task_status = status.get("status")
            current = status.get("current_state") or {}
            state = current.get("state")
            message = current.get("message") or ""
            uri = current.get("uri") or ""

            line = f"{label}: {state or '<no-state>'} {message}".strip()
            if last_line.get(label) != line:
                print(f"[+{elapsed:>3}s] {line}")
                last_line[label] = line

            if task_status == "error":
                workspace_name = status.get("workspace_name") or "<unknown>"
                workspace_status = status.get("workspace_status") or "<unknown>"
                raise CmdError(
                    "\n".join(
                        [
                            f"Task {label} is in status=error (workspace={workspace_name}, workspace_status={workspace_status}).",
                            f"Inspect via: coder ssh {workspace_name}",
                        ]
                    )
                )

            if state == "failure":
                logs_tail = "\n".join(coder_task_logs(task_id).splitlines()[-80:])
                raise CmdError(f"Task {label} entered failure state.\n\nLogs (tail):\n{logs_tail}")

            if state in ("idle", "complete"):
                if uri and PR_URL_RE.search(uri):
                    pr_urls[label] = uri
                    continue

                # Fallback: parse logs for PR URL.
                logs = coder_task_logs(task_id)
                matches = PR_URL_RE.findall(logs)
                if matches:
                    pr_urls[label] = matches[-1]
                    continue

                raise CmdError(f"Task {label} finished but no PR URL found (state={state}).")

            done = False

        if done:
            return pr_urls

        time.sleep(10)


def merge_prs(pr_urls: list[str], repo_full: str) -> None:
    for url in pr_urls:
        run(["gh", "pr", "merge", url, "--squash", "--delete-branch", "--repo", repo_full], check=True, capture=True, env=gh_env())


def verify_repo(repo_full: str) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="modern-todo-demo-"))
    repo_dir = temp_dir / "repo"
    run(["gh", "repo", "clone", repo_full, str(repo_dir)], check=True, capture=True, env=gh_env())

    required = ["index.html", "app.js", "style.css", "README.md", ".gitignore", "DEMO.md"]
    for filename in required:
        path = repo_dir / filename
        if not path.exists():
            raise CmdError(f"Verification failed: missing {filename}")

    # Serve + curl smoke check.
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8123", "--bind", "127.0.0.1"],
        cwd=repo_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1)
        run(["curl", "-fsS", "--max-time", "3", "http://127.0.0.1:8123/"], check=True, capture=True)
    finally:
        server.terminate()
        try:
            server.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server.kill()
    return repo_dir


def delete_tasks(task_ids: list[str]) -> None:
    for task_id in task_ids:
        run(["coder", "task", "delete", task_id, "--yes"], check=False, capture=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a modern Todo demo repo via parallel Coder Tasks.")
    parser.add_argument("--template", default="todo-parallel-claude-task", help="Coder Task template name")
    parser.add_argument("--org", default=None, help="Coder org name (optional)")
    parser.add_argument("--repo", default=None, help="Existing GitHub repo as OWNER/REPO (skip creation)")
    parser.add_argument("--owner", default=None, help="GitHub owner for new repo (default: gh user)")
    parser.add_argument("--name", default=None, help="Repo name for new repo (default: generated)")
    parser.add_argument("--public", action="store_true", help="Create repo as public (default: private)")
    parser.add_argument("--timeout", type=int, default=20 * 60, help="Timeout in seconds")
    parser.add_argument("--no-merge", action="store_true", help="Do not merge PRs")
    parser.add_argument("--skip-verify", action="store_true", help="Skip local clone + http smoke check")
    parser.add_argument("--keep-tasks", action="store_true", help="Do not delete tasks at the end")
    args = parser.parse_args()

    ensure_tools()
    preflight(args.template, args.org)

    if args.repo:
        repo_full = args.repo.strip()
        if "/" not in repo_full:
            raise CmdError("--repo must be OWNER/REPO")
        repo_url = f"https://github.com/{repo_full}"
    else:
        owner = args.owner or get_github_login()
        repo_name = args.name
        if not repo_name:
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            repo_name = f"modern-todo-demo-{stamp}"
        repo_full, repo_url = create_repo(owner, repo_name, public=args.public)

    repo_dir = f"/home/coder/projects/{repo_full.split('/', 1)[1]}"

    prompts = {
        "ui": build_prompt_ui(repo_url, repo_dir, branch="feat/modern-todo-ui"),
        "docs": build_prompt_meta(repo_url, repo_dir, branch="chore/repo-docs"),
        "demo": build_prompt_meta(repo_url, repo_dir, branch="docs/demo-checklist"),
    }

    # Make the third task minimal but distinct: DEMO.md only. Reuse prompt_meta but it will touch same files.
    # To avoid conflicts, override demo prompt to ONLY add DEMO.md.
    demo_md = read_text(REPO_ASSETS_DIR / "DEMO.md")
    repo_full = repo_url.split("https://github.com/", 1)[1]
    prompts["demo"] = f"""You are running inside a Coder Task with Claude Code.

Goal: Add a short DEMO checklist on a feature branch and open a PR.

Repo:
- URL: {repo_url}.git
- Work directory: {repo_dir}
- Base branch: main
- Feature branch: docs/demo-checklist

Constraints:
- Do NOT add GitHub Actions / workflows.
- Only create/modify: DEMO.md

{build_git_auth_note()}

Steps:
1) Ensure the repo is cloned to the absolute path {repo_dir}:
   - If `{repo_dir}/.git` does not exist, run:
     `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git clone {repo_url}.git {repo_dir}`
2) `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git -C {repo_dir} fetch --prune origin`
3) `git -C {repo_dir} checkout main && git -C {repo_dir} reset --hard origin/main`
4) `git -C {repo_dir} checkout -B docs/demo-checklist`
5) Write `DEMO.md` with EXACT contents:

```md
{demo_md}
```

6) Commit + PR:
   - `git -C {repo_dir} add -A`
   - `git -C {repo_dir} commit -m "docs: add demo checklist"`
   - `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/tmp/git-askpass git -C {repo_dir} push -u origin docs/demo-checklist`
   - `gh pr create --repo {repo_full} --base main --head docs/demo-checklist --title "Add demo checklist" --body "Adds DEMO.md with a short talk track and reset instructions."`

Output:
- Print the PR URL.
"""

    print(f"Repo: {repo_url}")
    print("Starting 3 parallel Coder Tasks...")

    task_ids: dict[str, str] = {}
    task_ids["ui"] = coder_task_create(prompts["ui"], template=args.template, org=args.org, name="todo-ui")
    task_ids["docs"] = coder_task_create(prompts["docs"], template=args.template, org=args.org, name="todo-docs")
    task_ids["demo"] = coder_task_create(prompts["demo"], template=args.template, org=args.org, name="todo-demo")

    print("Task IDs:")
    for k, v in task_ids.items():
        print(f"- {k}: {v}")

    pr_urls = wait_for_pr_urls(task_ids, timeout_s=args.timeout)
    print("PR URLs:")
    for k, v in pr_urls.items():
        print(f"- {k}: {v}")

    if not args.no_merge:
        # Merge in a safe order (non-overlapping, but deterministic).
        merge_prs([pr_urls["docs"], pr_urls["demo"], pr_urls["ui"]], repo_full=repo_full)
        print("Merged PRs into main.")

    verified_path: Path | None = None
    if not args.skip_verify and not args.no_merge:
        verified_path = verify_repo(repo_full)
        print(f"Verified repo output at: {verified_path}")

    if not args.keep_tasks:
        delete_tasks(list(task_ids.values()))
        print("Deleted Coder Tasks.")

    print(f"Done: {repo_url}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CmdError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
