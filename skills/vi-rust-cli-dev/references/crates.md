# Crate index (by concern)

This is a pragmatic starting list, not a mandate. Prefer fewer dependencies.

## CLI args

- `clap`: full-featured argument parsing (derive + builder)
- `bpaf`, `argh`: smaller alternatives for some tools

## Errors and diagnostics

- `anyhow`: application-level error handling + context
- `thiserror`: typed library errors
- `eyre`, `color-eyre`: ergonomic error reports
- `miette`: rich diagnostics

## Logging and tracing

- `tracing`, `tracing-subscriber`: structured logs/spans
- `log`, `env_logger`: classic logging facade + simple backend

## Config and directories

- `config`, `figment`: layered config loading/merging
- `directories`: platform-correct config/data/cache dirs
- `serde`, `toml`, `serde_json`: parsing config formats

## Output and terminal UX

- `serde_json`, `csv`: machine-readable formats
- `indicatif`: progress bars
- `console`, `owo-colors`, `termcolor`: styling and colors
- `dialoguer`: interactive prompts
- `ratatui`, `crossterm`: TUIs

## Testing

- `assert_cmd`: integration tests for CLIs
- `predicates`: assertions for process output
- `tempfile`: temp dirs/files
- `insta`: snapshot testing
- `trycmd`: “CLI test cases” driven by files

## Distribution

- `cargo-dist`: CI-driven release artifacts
- `cargo-release`: version/tag/publish automation
- `cross`: cross-compilation helper
- `cargo-binstall`: binary installation for end users (ecosystem tool)

