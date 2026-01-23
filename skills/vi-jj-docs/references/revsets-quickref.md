# JJ Revsets (minimal, example-driven)

Revsets are expressions used by many commands (for example `jj log -r '<revset>'`).

## Symbols you will use constantly

- `@` = the working-copy commit
- `@-` = parent(s) of the working-copy commit (built-in alias: `HEAD = @-`)

## Common patterns (copy/paste)

- Parent(s) of working copy: `jj log -r @-`
- All ancestors of working copy: `jj log -r ::@`
- All commits: `jj log -r ::` (or `jj log -r 'all()'`)
- Show tags + bookmarks: `jj log -r 'tags() | bookmarks()'`
- Commits not on any remote bookmark: `jj log -r 'remote_bookmarks()..'`

## Tips

- Quote revsets in the shell: `jj log -r '... | ...'`
- When in doubt, open the canonical doc: `references/doc-index.md` → `docs/revsets.md`
