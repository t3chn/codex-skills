# IO + output conventions

## Std streams

- Write the “answer” to stdout.
- Write errors, logs, and progress to stderr.
- Avoid mixing logs/progress with machine output.

## Files and stdin

- Accept `-` as stdin when it fits the domain.
- Prefer streaming (`BufRead`) over `read_to_end` for unbounded input.
- Use `stdin().lock()` / `stdout().lock()` for performance when output is large.

## Human vs machine output

- If supporting machine output, make it explicit (`--json`).
- Keep machine output stable; version fields/schemas if needed.
- Prefer newline-delimited output for streams (e.g., JSON Lines) when appropriate.

## Colors and TTY detection

- Default to `--color=auto` behavior (color only when writing to a TTY).
- Use `std::io::stdout().is_terminal()` / `stderr().is_terminal()` to detect TTY.

## Progress and logging

- Use `indicatif` for progress bars; route them to stderr.
- Use `tracing` or `log` for structured logs; route logs to stderr.

