---
name: vi-jj-docs
description: "Accurate, low-token guidance for the Jujutsu (jj) version control system: CLI commands/flags, revsets, bookmarks, conflicts, config, and Git interop. Use when a request mentions Jujutsu, `jj`, revsets, bookmarks, `jj git`, `jj rebase`, `jj undo`, or interpreting `jj` output."
---

# Vi JJ Docs

Use local, authoritative sources (prefer `jj help` and upstream docs) to answer questions about `jj` without guessing command syntax.

## Workflow (token-efficient, accuracy-first)

1. Confirm context: repo/workspace root (`jj root`) and current state (`jj status`).
2. For command syntax/flags: run `jj help <command>` (or `jj <command> -h`) and quote only the relevant lines.
3. For concepts: search docs in a `jj` checkout (typically `./docs/`) using `scripts/jj-doc-search.sh "<query>"`, then open only the needed section.
4. Respond with the minimal command sequence and call out side effects (history rewriting, pushing bookmarks).

## Quick start (common tasks)

- Inspect: `jj status`, `jj log`, `jj diff`
- Start/continue work: `jj new`, `jj edit <rev>`, `jj describe`
- Rewrite history: `jj squash`, `jj split`, `jj rebase`
- Undo: `jj undo` or `jj op log` + `jj op restore`
- Bookmarks (branch-like names): `jj bookmark list|set|create|move|track|untrack`
- Git remotes: `jj git fetch`, `jj git push` (remember: pushes bookmarks, not revisions)

Examples: `references/quickref.md`. Revsets: `references/revsets-quickref.md`. Doc map: `references/doc-index.md`.

## Accuracy rules

- Do not invent flags, subcommands, or revset syntax; confirm via `jj help` or the matching doc page.
- Prefer stable revision selectors (`@`, `@-`, bookmarks) over copying short IDs unless the user already has them.
- When recommending `jj git push`, state exactly what will be pushed (e.g., `--bookmark X`, `--change Y`, or `--all`).
