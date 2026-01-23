# JJ Docs: Local-first index

Prefer local docs (in a `jj` checkout) and `jj help` over memory.

## Canonical sources

- CLI (authoritative): `jj help <command>` / `jj <command> -h`
- Web docs: https://docs.jj-vcs.dev/latest/
- Web docs (prerelease): https://docs.jj-vcs.dev/prerelease/
- Repo docs (in a `jj` checkout): `./docs/*.md`

## Fast navigation (repo `docs/`)

- Getting started: `docs/tutorial.md`, `docs/install-and-setup.md`
- Core concepts: `docs/glossary.md`, `docs/core_tenets.md`, `docs/working-copy.md`
- Revsets: `docs/revsets.md` (also see `cli/src/config/revsets.toml` in the repo)
- Filesets: `docs/filesets.md`
- Templates: `docs/templates.md`
- Bookmarks (branch-like names): `docs/bookmarks.md`
- Conflicts: `docs/conflicts.md`, `docs/working-copy.md`
- Undo/operations: `docs/operation-log.md`
- Config: `docs/config.md`, `docs/config-schema.json`
- Git interop: `docs/git-compatibility.md`, `docs/git-experts.md`, `docs/git-command-table.yml`, `docs/github.md`
- FAQ: `docs/FAQ.md`

## Search

Use `scripts/jj-doc-search.sh "<query>" [path-to-jj-checkout-or-docs-dir]` to locate relevant sections quickly (output is truncated).
