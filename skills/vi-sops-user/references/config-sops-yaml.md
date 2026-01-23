# `.sops.yaml` (user configuration)

## Key points

- Auto-discovery works only for **`.sops.yaml`**.
- `creation_rules` are evaluated **in order** (first match wins).
- `path_regex` matches paths **relative** to the `.sops.yaml` location.
- If you provide keys via CLI or env vars (e.g. `SOPS_KMS_ARN`, `SOPS_PGP_FP`, `SOPS_AGE_RECIPIENTS`), key selection from `.sops.yaml` is typically bypassed for new-file creation.

## Minimal example (age)

```yaml
creation_rules:
  - path_regex: \\.ya?ml$
    age: age1yourrecipienthere
```

## Common dev/prod split

```yaml
creation_rules:
  - path_regex: \\.dev\\.ya?ml$
    age: age1devrecipient
  - path_regex: \\.prod\\.ya?ml$
    age: age1prodrecipient
```

## `creation_rules` keys (summary)

- `kms`: AWS KMS ARNs (comma-separated string or list)
- `aws_profile`: AWS profile for AWS KMS keys
- `age`: age recipients (comma-separated string or list)
- `pgp`: fingerprints (often with `!` to force subkeys)
- `gcp_kms`: GCP KMS resource IDs
- `azure_keyvault`: Azure Key Vault key URLs
- `hc_vault_transit_uri`: Vault transit URIs
- `hckms`: HuaweiCloud KMS key IDs (format `<region>:<uuid>`)

## Partial encryption (per rule)

In a creation rule you can set (mutually exclusive; choose at most one):

- `unencrypted_suffix`
- `encrypted_suffix`
- `unencrypted_regex`
- `encrypted_regex`
- `unencrypted_comment_regex`
- `encrypted_comment_regex`

And also:

- `mac_only_encrypted: true|false`
