# Testing Rust CLIs

## What to test

- Pure logic: unit tests in the library (fast, deterministic).
- Parsing/formatting: unit tests with representative fixtures.
- End-to-end behavior: integration tests that run the binary.

## Integration testing with `assert_cmd`

- Use `assert_cmd::Command::cargo_bin(\"your-bin\")` to run the compiled binary.
- Use `predicates` to assert on stdout/stderr.
- Use `tempfile` to isolate filesystem tests.

## Golden files and portability

- Compare against fixture files when output is long.
- Normalize line endings if needed (`\\n` vs `\\r\\n`).
- Avoid embedding absolute paths in output; prefer relative or user-provided paths.

## Testability design rules

- Take `impl Read`/`impl BufRead` and `impl Write` in core functions.
- Pass configuration and dependencies in explicitly (avoid globals).
- Keep nondeterminism controllable (seed, clock injection, fixed temp dirs in tests).

