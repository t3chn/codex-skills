---
name: vi-sops-user
description: "Help a user use Mozilla SOPS (getsops/sops) safely and effectively: encrypt/decrypt/edit secrets files (YAML/JSON/ENV/INI/binary), set up and troubleshoot `.sops.yaml`, choose key backends (age/PGP/AWS KMS/GCP KMS/Azure Key Vault/Vault), rotate keys, use `sops set/unset/extract/exec-env`, and fix common workflow issues. Use when a request mentions SOPS, `sops`, `.sops.yaml`, secret encryption, age recipients/keys, PGP fingerprints, KMS/Key Vault/Vault, or Git diff with SOPS."
---

# Vi Sops User

Use SOPS as an end user (not SOPS development).

## Quick start (most common commands)

- **Create/edit an encrypted file**: `sops edit path/to/secrets.yaml`
- **Encrypt to stdout**: `sops encrypt secrets.yaml > secrets.enc.yaml`
- **Encrypt in place**: `sops encrypt -i secrets.yaml`
- **Decrypt to stdout**: `sops decrypt secrets.enc.yaml > secrets.yaml`
- **Decrypt in place**: `sops decrypt -i secrets.enc.yaml`
- **Rotate the data key** (re-encrypt with a new data key): `sops rotate -i secrets.enc.yaml`

Config/keys: see `references/config-sops-yaml.md` and `references/key-backends.md`.

## Recommended workflow (Git repo with secrets)

1) Put `.sops.yaml` at the repo root (or the directory you typically run `sops` from).
2) Define `creation_rules` per environment/path (dev/prod) and pick a backend (often `age`).
3) Create new secrets via `sops edit <file>` so SOPS auto-selects keys using `creation_rules`.
4) Make Git diffs readable using `textconv` (see `references/git-diff.md`).
5) When needed, run `sops updatekeys` or `sops rotate` (see `references/rotation-and-updatekeys.md`).

## `.sops.yaml` (key facts)

- Auto-discovery works only for a file named **`.sops.yaml`** (not `.sops.yml`).
- For new files, `creation_rules` are evaluated **in order** (“first match wins”).
- If you provide keys via CLI flags or env vars (`SOPS_KMS_ARN`, `SOPS_PGP_FP`, `SOPS_AGE_RECIPIENTS`, etc.), key selection from `.sops.yaml` is typically bypassed for new-file creation.

Details and templates: `references/config-sops-yaml.md`.

## Common tasks

### Extract a single value

- `sops decrypt --extract '["path"]["to"]["key"]' file.yaml`

### Modify a single field without an editor

- `sops set file.yaml '["path"]["to"]["key"]' '"newValue"'`
- `sops unset file.yaml '["path"]["to"]["key"]'`

### Run a command with secrets injected into env

- `sops exec-env file.yaml 'command_here'`

## Troubleshooting (quick checks)

- **“config file not found”**: run `sops` from a directory that has `.sops.yaml` in it (or a parent), or pass `--config`, or set `SOPS_CONFIG`.
- **Editor does not open**: check `SOPS_EDITOR`/`EDITOR`.
- **age cannot decrypt**: check `SOPS_AGE_KEY_FILE` / `SOPS_AGE_KEY` / `SOPS_AGE_KEY_CMD` and verify recipients match.
- **PGP cannot decrypt**: ensure the private key is in your keyring; use `SOPS_GPG_EXEC` if needed.
- **MAC mismatch**: the file was edited outside `sops` (or integrity settings differ). See `references/mac-and-partial-encryption.md`.

## Resources

- `.sops.yaml` setup: `references/config-sops-yaml.md`
- Key backends + env vars: `references/key-backends.md`
- Partial encryption + MAC: `references/mac-and-partial-encryption.md`
- Rotation + `updatekeys`: `references/rotation-and-updatekeys.md`
- Git diff decryption: `references/git-diff.md`
- Template generator: `scripts/sops-write-config-template.sh`
