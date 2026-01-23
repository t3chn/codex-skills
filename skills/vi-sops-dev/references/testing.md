# Testing and validation (SOPS)

## Fast local loop

- Unit tests: `make test`
  - Runs `go test` with race + coverage flags.
  - Imports the repo’s functional test PGP key first (`pgp/sops_functional_tests_key.asc`) so PGP-backed tests can run.
- Lint/static analysis: `make vet` and `make staticcheck`
- Docs lint (RST + MD): `make checkdocs`

## End-to-end behavior

- Functional tests (Rust): `make functional-tests`
  - Builds `functional-tests/sops` from `cmd/sops`.
  - Runs `cargo test` in `functional-tests/`.
- Full functional test suite: `make functional-tests-all`
  - Includes ignored tests (often require external services like AWS KMS).

## When to add which test

- Add/adjust Go unit tests when changing pure logic (tree traversal, metadata, parsing, store emit/load, etc.).
- Add/adjust Rust functional tests when changing CLI UX, flags, output formatting, or end-to-end encryption/decryption flows.

