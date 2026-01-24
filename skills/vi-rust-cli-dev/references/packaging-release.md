# Packaging and release options

## Common distribution paths

- Crate install: publish to crates.io so users can `cargo install your-tool`.
- Binary releases: ship platform-specific binaries (e.g., GitHub Releases).
- Package managers: Homebrew, Scoop, apt/rpm, etc. (usually driven by your release artifacts).

## Cross-compilation

- Prefer reproducible builds and CI-based releases.
- Use `cross` or `cargo-zigbuild` when native toolchains are painful.

## Release checklist

- Confirm help output and exit codes are stable.
- Run `cargo fmt`, `cargo clippy`, `cargo test`.
- Build `--release` artifacts for supported targets.
- Generate completions and man pages (if supported).
- Attach checksums and notes (breaking changes, migration, known issues).

## Publishing hygiene

- Set `name`, `version`, `description`, `license`, `repository`, and `readme` in `Cargo.toml`.
- Add a short `README.md` with usage examples and installation instructions.

