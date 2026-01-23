# JJ Quick Reference (common workflows)

Always confirm exact flags/options with `jj help <command>` because they may change across versions.

## Inspect state

- Status: `jj status` (shorthand: `jj st`)
- Log: `jj log` (filter with revsets: `jj log -r '<revset>'`)
- Diff: `jj diff` (see also `jj diff --git` for Git-style output)

## Start / continue work

- Create a new change on top of the current commit: `jj new`
- Start a new change on top of a specific revision: `jj new <rev>`
- Edit an existing revision: `jj edit <rev>`
- Set/change description: `jj describe` (or `jj describe -m "msg"`)

## Rewrite history (everyday)

- Move current diff into parent: `jj squash`
- Split a change: `jj split`
- Rebase: `jj rebase` (common pattern: `jj rebase -s <source> -o <dest>`)
- Drop a revision: `jj abandon <rev>`

## Conflicts (typical flow)

When a rebase produces conflicts, `jj` usually recommends creating a new commit on top of the first conflicted commit, resolving, then squashing the resolution into the conflicted commit:

1. `jj new <conflicted-rev>`
2. Resolve conflicts: `jj resolve` (or edit conflict markers directly)
3. Inspect: `jj diff`
4. Move resolution into the conflicted commit: `jj squash`

See `references/doc-index.md` → `docs/conflicts.md` / `docs/working-copy.md` for details.

## Undo / safety net

- Undo last operation: `jj undo`
- Inspect operation history: `jj op log`
- Restore/revert specific operations: see `jj help op restore` / `jj help op revert`

## Bookmarks and Git remotes

`jj git push` pushes *bookmarks* (branch-like names), not arbitrary revisions. If nothing is bookmarked, pushing can appear to do nothing.

- List bookmarks: `jj bookmark list`
- Create a bookmark: `jj bookmark create NAME -r <rev>`
- Set/move a bookmark: `jj bookmark set NAME` / `jj bookmark move NAME -r <rev>`
- Track remote bookmark: `jj bookmark track NAME --remote origin`
- Fetch: `jj git fetch`
- Push a bookmark: `jj git push --bookmark NAME`
- Push a change (auto-creates a bookmark): `jj git push --change <rev>`
- Push all bookmarks: `jj git push --all`
