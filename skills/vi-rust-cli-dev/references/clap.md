# `clap` recipes

## Recommended style

- Prefer derive (`#[derive(clap::Parser)]`) for most CLIs.
- Model subcommands with `enum` + `#[derive(clap::Subcommand)]`.
- Use `ValueEnum` for enums that should be validated and shown in help.
- Use `value_parser` for numeric ranges, paths, and custom validation.

## Minimal pattern

```rust
use clap::{Parser, Subcommand};

#[derive(Debug, Parser)]
#[command(author, version, about)]
struct Cli {
    #[command(subcommand)]
    cmd: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Run { #[arg(long)] dry_run: bool },
}
```

## Validation patterns

- Validate at parse time when possible:
  - `#[arg(value_parser = clap::value_parser!(u16).range(1..))]`
  - `#[arg(value_parser = ["json", "text"])]` (or `ValueEnum`)
- Validate after parse when rules depend on multiple flags.

## Output and UX flags

- Add `--json` when you need machine-readable output.
- Add `--quiet` to suppress non-essential output.
- Add `--no-color` and/or `--color=auto|always|never`.

## Completions and man pages

- Generate shell completions with `clap_complete`.
- Generate a man page with `clap_mangen` from the same `Command` model.

Keep generation out of the hot path (e.g., behind a `tool completions` subcommand or a build/release step).

