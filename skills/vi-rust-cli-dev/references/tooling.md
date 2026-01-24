# Tooling and quality gates

## Core commands

- Format: `cargo fmt`
- Lint: `cargo clippy --all-targets --all-features -D warnings`
- Test: `cargo test`
- Build release: `cargo build --release`

## Debugging and inspection

- Faster iteration: `cargo check`
- Backtraces: `RUST_BACKTRACE=1`
- Expand macros: `cargo expand` (requires `cargo-expand`)

## Optional “production” gates

- Audit dependencies: `cargo audit` (or `cargo deny`)
- Faster test runner: `cargo nextest`
- Fuzzing: `cargo fuzz`
- Profiling: `cargo flamegraph`

