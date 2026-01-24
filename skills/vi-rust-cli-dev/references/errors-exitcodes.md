# Errors + exit codes

## Error strategy (practical default)

- In library code:
  - Prefer typed errors via `thiserror`.
  - Return `Result<T, Error>` and keep printing out of the library.
- In binary code:
  - Use `anyhow::Result<()>` (or `Result<(), anyhow::Error>`) for wiring.
  - Add context to failures so the user can act (file path, operation, hint).

## Exit code strategy

- Use a small, documented set of exit codes.
- Map error types to exit codes in one place (typically `main.rs`).
- Keep exit codes stable across versions.

## User-facing error output

- Print one concise error line by default.
- Print more detail behind `--verbose` (or when `RUST_BACKTRACE=1` is set).
- Consider “pretty errors” (e.g., `miette` or `color-eyre`) for complex tools, but keep output stable if scripts depend on it.

## Avoid foot-guns

- Avoid `unwrap()`/`expect()` on user input and IO paths.
- Avoid panicking on expected failures (missing files, invalid flags, parse errors).

