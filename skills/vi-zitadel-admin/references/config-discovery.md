# Config discovery (runtime vs setup)

Use this when you need to find the right configuration key, decide whether it belongs to runtime config (`--config`) or setup steps (`--steps`), and apply changes without touching ZITADEL source code.

## Source of truth

Canonical sources:

- Runtime defaults: https://github.com/zitadel/zitadel/blob/main/cmd/defaults.yaml
- Setup steps defaults: https://github.com/zitadel/zitadel/blob/main/cmd/setup/steps.yaml
- Configuration guide (runtime vs steps, merge behavior, masterkey): https://zitadel.com/docs/self-hosting/manage/configure/configure

Both files also show the corresponding environment variable names in `# ZITADEL_...` comments.

If you have a local clone, use it for fast/offline search (any path). Example:

```bash
export ZITADEL_REPO=~/contrib/zitadel
```

## Fast search recipes

- List all runtime env vars: `rg -n \"#\\s*ZITADEL_[A-Z0-9_]+\" \"$ZITADEL_REPO/cmd/defaults.yaml\"`
- List all setup-step env vars: `rg -n \"#\\s*ZITADEL_[A-Z0-9_]+\" \"$ZITADEL_REPO/cmd/setup/steps.yaml\"`
- Jump to external access keys: `rg -n \"^External(Domain|Port|Secure):\" \"$ZITADEL_REPO/cmd/defaults.yaml\"`
- Jump to database keys: `rg -n \"^Database:\" \"$ZITADEL_REPO/cmd/defaults.yaml\"`
- Jump to first admin user defaults: `rg -n \"^FirstInstance:\" \"$ZITADEL_REPO/cmd/setup/steps.yaml\"`

## Runtime vs steps: what goes where

- **Runtime config (`--config`)**: networking (`ExternalDomain/...`), TLS, database connection (ZITADEL DB user), logging/metrics/tracing, quotas/limits defaults, etc.
- **Setup steps (`--steps`)**: first-instance bootstrap (initial org/admin, machine users, PAT outputs), data initialization steps and migrations.

Rule of thumb: if it affects "how the server runs", it is runtime; if it affects "what to create during bootstrap/migrations", it is steps.

## Config layering (recommended)

ZITADEL merges multiple `--config` and `--steps` files. Use this to keep secrets out of git.

- Put public, non-secret values in `config.public.yaml`
- Put secrets in `config.secrets.yaml` from a secret manager (mounted file) or generated at deploy time
- Pass both: `zitadel start --config config.public.yaml --config config.secrets.yaml ...`

Do the same for setup steps:

- `zitadel setup --steps steps.public.yaml --steps steps.secrets.yaml ...`

## Masterkey handling (critical)

The masterkey is the root secret used to encrypt other keys. It must be exactly 32 bytes.

Prefer one of:

- `--masterkeyFile /path/to/masterkey` (best for ops)
- `--masterkeyFromEnv` with `ZITADEL_MASTERKEY` (acceptable if your platform secures env vars)

Avoid committing or logging the masterkey. Treat it like a database encryption root key.

## Local docs (optional)

If you have a local clone, the self-hosting docs include examples and explanations:

- `$ZITADEL_REPO/docs/docs/self-hosting/manage/configure/`
- `$ZITADEL_REPO/docs/docs/self-hosting/manage/updating_scaling.md`
- `$ZITADEL_REPO/docs/docs/self-hosting/manage/productionchecklist.md`

If you do not have a local clone, use the online docs: https://zitadel.com/docs/self-hosting
