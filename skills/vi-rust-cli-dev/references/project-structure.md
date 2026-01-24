# Project structure patterns

## Default layout (single crate, lib + bin)

Prefer a single crate that has both a library and a binary:

- `src/lib.rs`: core logic (testable, reusable)
- `src/main.rs`: CLI wiring (args parsing, IO glue, exit codes)
- `src/cli.rs`: `clap` types (optional)
- `tests/`: integration tests that run the compiled binary

Benefits:

- Keep pure logic unit-testable without spawning processes.
- Keep `clap` and terminal dependencies out of the core library when appropriate.

## Suggested module split

- `cli`: parse args into a strongly-typed plan (subcommand + options)
- `config`: load/merge config sources (env, config file, args)
- `io`: readers/writers and streaming helpers
- `domain`: business logic (no printing, no global IO)
- `output`: formatting (text/JSON) and stable schemas

## Dependency boundaries

- Keep `clap`, terminal styling, and progress libraries close to the binary.
- Keep the library “boring”: `std` + small, focused crates.
- Avoid putting “process exit” logic in the library; return typed errors instead.

## When to use a workspace

Use a workspace when you have:

- Multiple binaries sharing a library (`crates/core`, `crates/cli`).
- A plugin system or multiple deliverables.
- Benchmarks/tools that should not ship with the main crate.

