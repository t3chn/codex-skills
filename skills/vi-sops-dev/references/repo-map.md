# SOPS repo map (getsops/sops)

## Entry points

- CLI app: `cmd/sops/main.go` (urfave/cli; wires flags + commands)
- Core types + crypto/tree/metadata: `sops.go`
- CLI shared helpers: `cmd/sops/common/` (load/decrypt/encrypt, keygroup diffs, etc.)

## CLI commands (common starting points)

- Edit flow (tmp file → editor → re-encrypt): `cmd/sops/edit.go`
- Encrypt flow (new file): `cmd/sops/encrypt.go`
- Decrypt flow: `cmd/sops/decrypt.go`
- Rotate keys / update metadata: `cmd/sops/rotate.go`, `cmd/sops/subcommand/updatekeys/`
- Config file lookup: `config/config.go` (`.sops.yaml`, `.sops.yml` is ignored with warnings)

## File formats (“stores”)

- Store interface: `sops.Store` in `sops.go`
- Store implementations: `stores/` and subpackages:
  - YAML: `stores/yaml/`
  - JSON: `stores/json/` (also supports “binary store” semantics)
  - dotenv: `stores/dotenv/`
  - INI: `stores/ini/`
- CLI store selection helpers: `cmd/sops/formats/`, plus helpers in `cmd/sops/common/`

## Key providers (“master keys”)

- MasterKey interface: `keys/MasterKey` in `keys/keys.go`
- Built-in provider packages (each typically defines `KeyTypeIdentifier` and a `MasterKey` struct):
  - AWS KMS: `kms/`
  - GCP KMS: `gcpkms/`
  - Azure Key Vault: `azkv/`
  - HuaweiCloud KMS: `hckms/`
  - HashiCorp Vault transit: `hcvault/`
  - age: `age/`
  - PGP: `pgp/`

## Keyservice (gRPC)

- Keyservice protocol + helpers: `keyservice/` (incl. proto + generated code)
- CLI keyservice subcommand: `cmd/sops/subcommand/keyservice/`

## Tests

- Go unit tests: package tests throughout the repo (`go test ./...`, or `make test`)
- Rust functional tests: `functional-tests/` (drives the built `sops` binary)

