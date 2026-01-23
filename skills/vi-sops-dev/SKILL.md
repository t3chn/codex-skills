---
name: vi-sops-dev
description: "Work effectively in the getsops/sops codebase (Go + Rust functional tests): trace CLI behavior (edit/encrypt/decrypt/rotate/updatekeys), debug encryption/decryption + metadata/MAC issues, add or modify key providers (KMS/GCP/Azure/Vault/age/PGP), add file-format stores (YAML/JSON/INI/ENV/binary), update config (.sops.yaml), and run the right test suites. Use when a task mentions SOPS, getsops/sops, sops CLI internals, master keys, keyservice, stores, or functional-tests."
---

# Vi Sops Dev

## Quick Start

- Start from the repo map in `references/repo-map.md` to pick the right entry point fast.
- Run the developer test loop from `references/testing.md` (`make test`, then `make functional-tests`).
- Use `--verbose` (or per-command `--verbose` where available) to enable debug logging in the CLI.

## Workflow

### 1) Triage the user request

- Identify whether the change is primarily:
  - CLI plumbing (`cmd/sops/...`)
  - crypto/tree/metadata (`sops.go`, `aes/`, `stores/`)
  - key provider (`kms/`, `gcpkms/`, `azkv/`, `hckms/`, `hcvault/`, `age/`, `pgp/`)
  - config parsing (`config/`)
  - keyservice / gRPC (`keyservice/`, `cmd/sops/subcommand/keyservice/`)
  - functional tests (`functional-tests/`)

### 2) Trace the execution path

- If the behavior is user-facing, start at `cmd/sops/main.go` and follow into the command implementation in `cmd/sops/*.go`.
- If the behavior is encryption/decryption:
  - CLI calls helpers in `cmd/sops/common/` (load/decrypt/encrypt).
  - Core logic lives in `sops.go` (Tree/Metadata, MAC, key groups, store interfaces).

### 3) Make a minimal reproduction

- Prefer a small fixture (YAML/JSON/ENV/INI) in `example.*` style, or use existing `example.yaml` / `example.json`.
- Prefer unit tests (`go test ./...`) for pure logic and functional tests (`functional-tests/`) for end-to-end CLI behavior.

### 4) Implement the change

- Match existing patterns in the nearest package (key providers, stores, CLI command wiring).
- Keep backwards compatibility in mind: encrypted-file schema + metadata fields are part of the ecosystem.

### 5) Validate

- Run `make test` and (when relevant) `make functional-tests`. See `references/testing.md`.

## Pointers

- Repo map: `references/repo-map.md`
- Testing: `references/testing.md`
- Key providers: `references/key-providers.md`
- Optional quick overview script: `scripts/sops-repo-map.sh`
