---
name: coder
description: "Work with Coder using the `coder` CLI and API, especially Coder Tasks (AI agents in Coder workspaces): create/list/monitor tasks (`coder task create|list|status|logs|send|delete`), pick task templates/presets, and troubleshoot task-template requirements (`coder_ai_task` and `coder_task`). Triggers: Coder, Coder Tasks, coder task, coder_ai_task, AgentAPI, AI Bridge, templates push."
---

# Coder (Tasks-first)

## Goal

Use Coder Tasks as the primary unit of work (a task runs an agent inside an isolated Coder workspace), and manage tasks from the terminal reliably.

## Key concept: Task ≈ Workspace + prompt

- A Coder **Task** provisions a **backing workspace** and runs an agent with the task prompt.
- Use **Tasks** for parallel, one-shot agent jobs; use **Workspaces** for interactive development.
- Cleanup is two layers: deleting a **Task** may not remove the backing **Workspace** (stop/delete it explicitly when needed).

## Quick start (CLI)

1) Ensure `coder` CLI is installed and authenticated

- Login: `coder login <url>`
- Print current session token (useful for API calls): `coder login token`

2) Create a task

- Direct input: `coder task create "<prompt>"`
- From stdin: `echo "<prompt>" | coder task create`
- Non-interactive: pass `--template`, optional `--preset`, optional `--name`
- Automation: add `--quiet` to print only the task ID
- From Beads (recommended for strict scope): `python3 scripts/task_from_beads.py <bead_id> --template <tpl> --preset <preset>`

3) Monitor + iterate

- Watch status: `coder task status <task> --watch`
- Send follow-ups: `coder task send <task> "<more instructions>"`
- Inspect logs: `coder task logs <task> -o json`

4) Find the backing workspace (when you need a shell)

- `coder task status <task> -o json` → read `workspace_name`
- Use normal workspace commands after that: `coder ssh <workspace>`, `coder stop <workspace>`, `coder delete <workspace>`

5) Cleanup

- Delete (no prompt): `coder task delete <task> --yes`

## Git operations from Tasks (important)

HTTPS pushes from Tasks can fail (external auth wrappers, missing scopes, workflow restrictions). Prefer SSH deploy keys for repo write access.

Steps + troubleshooting: `references/git-from-tasks.md`.

## Task templates (required)

If `coder task create` fails with something like “no task templates configured”, the deployment has no templates that are Tasks-capable.

A template becomes Tasks-capable when it defines:

- `resource "coder_ai_task" ...` (links a workspace app to the Task UI)
- `data "coder_task" "me" {}` (gives access to the task prompt and metadata)
- An agent module (Codex CLI, Claude Code, etc.) that runs in the workspace and consumes `data.coder_task.me.prompt`

Minimal Terraform snippet + notes: `references/task-template-snippet.md`.

## Subscription auth (Codex + Claude)

- **Codex CLI (ChatGPT subscription)**: login is interactive by default; for headless Tasks, pre-seed `~/.codex/auth.json` in the workspace (e.g., via a sensitive template variable written at startup). If you see an “unsupported model” error, use a ChatGPT-supported Codex model (typically `gpt-5.2-codex`).
- **Claude Code (subscription)**: generate an OAuth token via `claude setup-token` and pass it to the workspace (e.g., as a sensitive template variable). Avoid storing plaintext tokens in git. If you use OAuth, do not also set `CLAUDE_API_KEY` (pick one auth mode).
- Set/update template variables non-interactively with `coder templates push <template> --variables-file <yaml> --yes`.

## API (automation)

If you need to create tasks from CI/GitHub automation (or without the `coder` CLI), use the Tasks API (`/api/v2/tasks/...`) with a Coder session token.

Quick reference: `references/api.md`.

## Safety defaults

- Prefer a dedicated, locked-down Task template (least privilege, no prod secrets).
- Treat agents as untrusted: restrict permissions in the agent module when supported.
- Keep prompts explicit: inputs, repo, constraints, and “done when” criteria.

## Troubleshooting

- Need the backing workspace: `coder task status <task> -o json` (look for `workspace_name`/IDs), then use normal workspace commands.
- Task is `error`/unhealthy: start with `coder task logs <task>`.
- GitHub Actions is stuck in `queued`: check whether Actions is enabled and runners/minutes exist; see `references/git-from-tasks.md`.

## References (load as needed)

- Task template snippet + design notes: `references/task-template-snippet.md`
- Tasks API quick reference: `references/api.md`
- Git auth + deploy keys from Tasks: `references/git-from-tasks.md`
- Beads → Task prompt generator: `scripts/task_from_beads.py`
