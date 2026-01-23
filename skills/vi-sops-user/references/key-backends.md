# Key backends (end user)

## age (often the simplest)

**Encryption**: provide recipient(s):

- CLI: `sops encrypt --age <recipient> file.yaml > file.enc.yaml`
- Env: `SOPS_AGE_RECIPIENTS`
- `.sops.yaml`: `age: ...`

**Decryption**: you need a private key:

- `SOPS_AGE_KEY_FILE` (path to a key file)
- `SOPS_AGE_KEY` (key(s) in env)
- `SOPS_AGE_KEY_CMD` (a command that prints keys)
- For SSH keys: `SOPS_AGE_SSH_PRIVATE_KEY_FILE`

## PGP/GPG

- Select public keys via `--pgp` or `SOPS_PGP_FP` or `.sops.yaml` (`pgp: ...`)
- Use a custom gpg binary/wrapper via `SOPS_GPG_EXEC`

## AWS KMS

- For new files: `--kms` or `SOPS_KMS_ARN` or `.sops.yaml` (`kms: ...`)
- Credentials are usually read from `~/.aws/credentials` or env (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)

## GCP KMS

- `--gcp-kms` / `SOPS_GCP_KMS_IDS` / `.sops.yaml` `gcp_kms: ...`
- Switch client type via `SOPS_GCP_KMS_CLIENT_TYPE=grpc|rest`

## Azure Key Vault

- `--azure-kv` / `SOPS_AZURE_KEYVAULT_URLS` / `.sops.yaml` `azure_keyvault: ...`

## HashiCorp Vault Transit

- `--hc-vault-transit` / `SOPS_VAULT_URIS` / `.sops.yaml` `hc_vault_transit_uri: ...`
