# CLI design checklist (Rust CLIs)

## Contract checklist

- Define the primary use-case in one sentence.
- Define inputs:
  - Files, directories, stdin, network, env vars, config files.
  - Encoding and line ending expectations (UTF-8? binary?).
- Define outputs:
  - Primary output on stdout.
  - Diagnostics, progress, logs on stderr.
  - Optional machine output (e.g., JSON) with a stable schema.
- Define behavior:
  - Ordering guarantees (stable sort? input order?).
  - Determinism and randomness (seed?).
  - Idempotency and overwrites (require `--force`?).
- Define exit codes:
  - `0` success.
  - Non-zero values for distinct failure classes (document them).

## UX checklist

- Provide helpful `--help` with examples and defaults.
- Use subcommands when it improves discoverability (e.g., `tool init`, `tool fmt`, `tool run`).
- Prefer explicit flags over implicit behavior switches.
- Validate early and fail fast with actionable messages.
- Provide `--quiet` and `--verbose` when there is meaningful diagnostic output.
- Provide `--no-color` (and avoid colors when not on a TTY).

## Composability (Unix-style)

- Read from stdin when input is omitted or `-` is passed (when it makes sense).
- Avoid writing anything other than the intended output to stdout (keep it scriptable).
- Make output line-oriented when possible.
- Stream data; avoid reading unbounded input into memory.

## Cross-platform notes

- Avoid Unix-only assumptions in paths and file permissions.
- Keep tests resilient to path separators and line endings.
- If you need signal handling, make it opt-in and guard platform-specific logic.

