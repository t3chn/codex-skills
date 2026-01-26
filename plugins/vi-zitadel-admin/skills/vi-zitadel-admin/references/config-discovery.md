# Config Discovery (Runtime vs Setup)

Use this when finding the right configuration key, deciding whether it belongs to runtime config (`--config`) or setup steps (`--steps`), and applying changes without touching ZITADEL source code.

## Source of Truth

Prefer these files from the ZITADEL repo:

- Runtime defaults: `{zitadel_repo}/cmd/defaults.yaml`
- Setup steps defaults: `{zitadel_repo}/cmd/setup/steps.yaml`

Both files show the corresponding environment variable names in `# ZITADEL_...` comments.

If repo not available locally, use upstream equivalents:

- https://github.com/zitadel/zitadel/blob/main/cmd/defaults.yaml
- https://github.com/zitadel/zitadel/blob/main/cmd/setup/steps.yaml

## Fast Search Recipes

List all runtime env vars:
```bash
rg -n "#\s*ZITADEL_[A-Z0-9_]+" {zitadel_repo}/cmd/defaults.yaml
```

List all setup-step env vars:
```bash
rg -n "#\s*ZITADEL_[A-Z0-9_]+" {zitadel_repo}/cmd/setup/steps.yaml
```

Jump to external access keys:
```bash
rg -n "^External(Domain|Port|Secure):" {zitadel_repo}/cmd/defaults.yaml
```

Jump to database keys:
```bash
rg -n "^Database:" {zitadel_repo}/cmd/defaults.yaml
```

Jump to first admin user defaults:
```bash
rg -n "^FirstInstance:" {zitadel_repo}/cmd/setup/steps.yaml
```

## Runtime vs Steps: What Goes Where

**Runtime config (`--config`)**: networking (`ExternalDomain/...`), TLS, database connection (ZITADEL DB user), logging/metrics/tracing, quotas/limits defaults, etc.

**Setup steps (`--steps`)**: first-instance bootstrap (initial org/admin, machine users, PAT outputs), data initialization steps and migrations.

Rule of thumb: if it affects "how the server runs", it is runtime; if it affects "what to create during bootstrap/migrations", it is steps.

## Config Layering (Recommended)

ZITADEL merges multiple `--config` and `--steps` files. Use this to keep secrets out of git.

- Put public, non-secret values in `config.public.yaml`
- Put secrets in `config.secrets.yaml` from a secret manager (mounted file) or generated at deploy time
- Pass both: `zitadel start --config config.public.yaml --config config.secrets.yaml ...`

Do the same for setup steps:
```bash
zitadel setup --steps steps.public.yaml --steps steps.secrets.yaml ...
```

## Masterkey Handling (Critical)

The masterkey is the root secret used to encrypt other keys. It must be exactly 32 bytes.

Prefer one of:

- `--masterkeyFile /path/to/masterkey` (best for ops)
- `--masterkeyFromEnv` with `ZITADEL_MASTERKEY` (acceptable if platform secures env vars)

Avoid committing or logging the masterkey. Treat it like a database encryption root key.

## Useful Offline Docs in the Repo

If the ZITADEL repo exists, the self-hosting docs include examples and explanations:

- `{zitadel_repo}/docs/docs/self-hosting/manage/configure/`
- `{zitadel_repo}/docs/docs/self-hosting/manage/updating_scaling.md`
- `{zitadel_repo}/docs/docs/self-hosting/manage/productionchecklist.md`
