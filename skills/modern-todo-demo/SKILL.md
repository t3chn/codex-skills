---
name: modern-todo-demo
description: "End-to-end demo workflow to create a modern, single-user Todo web app (static HTML/CSS/JS + localStorage) in a new GitHub repo using 3+ parallel Coder Tasks (Claude Code): open PRs, merge, verify, cleanup. Use when asked to 'создать todo/to-do', 'todo app for demo', 'современный дизайн todo', or to demonstrate parallel Coder Tasks producing a ready-to-run app."
---

# Modern Todo Demo

## What you get

- A brand-new GitHub repo with a ready-to-run static Todo app (`index.html`, `style.css`, `app.js`).
- 3 parallel Coder Tasks (Claude Code) that each open a PR:
  - UI app
  - Repo meta (`README.md`, `.gitignore`)
  - Demo checklist (`DEMO.md`)
- PRs merged into `main`, output verified, Tasks cleaned up.

## Run (recommended)

From this skill folder:

```bash
python3 scripts/run_demo.py
```

Useful flags:

- `--public` (default is private)
- `--repo OWNER/REPO` (skip repo creation, reuse existing)
- `--template todo-parallel-claude-task` (default)
- `--org coder` (Coder org name)
- `--keep-tasks` (don’t delete Tasks at the end)
- `--no-merge` / `--skip-verify`

## Notes (reliability)

- Claude Code subscription auth must be configured in the Coder template via `claude_code_oauth_token` (and keep `claude_api_key` empty; don’t set both).
- Git from Tasks may be intercepted by Coder external-auth wrappers; always override `GIT_ASKPASS` inside the same shell invocation as `git clone/push` (the runner prompts already do this).
