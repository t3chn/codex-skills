# Key providers (MasterKey implementations)

## What “key provider” means in SOPS

- SOPS encrypts values with a per-file *data key*.
- “Master keys” (providers like KMS/age/PGP/Vault) encrypt that data key.
- Providers implement `keys.MasterKey` (`keys/keys.go`) and are serialized into the `sops` metadata block.

## Where provider code usually lives

- Each provider has its own package (e.g. `kms/`, `gcpkms/`, `azkv/`, `hcvault/`, `age/`, `pgp/`).
- Providers typically expose:
  - `KeyTypeIdentifier` (string used in decryption order + metadata)
  - `MasterKey` struct storing identifier + encrypted data key + creation timestamp/params
  - Parse helpers for environment/config/flag strings

## Integration touch points (high level)

1) Implement the `keys.MasterKey` interface in a provider package.
2) Ensure the provider can be:
   - constructed from CLI flags/env/config (look for existing parsing patterns in `cmd/sops/main.go` and `config/`)
   - converted to/from the metadata map representation (`ToMap()` / `TypeToIdentifier()`)
3) Ensure keyservice interop still works:
   - keyservice converts to/from `MasterKey` via helpers in `keyservice/`
4) Add tests:
   - unit tests near the provider package
   - functional tests when CLI wiring or behavior changes

## Debugging tips

- Use `--verbose` in the CLI to enable debug logging (many commands gate this to `logrus.DebugLevel`).
- If decryption fails for a specific provider, confirm:
  - decryption order includes the provider’s `KeyTypeIdentifier` when needed
  - metadata contains the expected provider block and encrypted data key
  - the provider’s `Decrypt()` path returns the raw data key bytes expected by SOPS

