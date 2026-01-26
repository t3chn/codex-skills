# Migrating CockroachDB -> Postgres (Mirror Command)

Use this when moving a ZITADEL v2 deployment off CockroachDB (for example to prepare for ZITADEL v3, where CockroachDB support is removed).

Upstream reference (recommended):

- Local: `{zitadel_repo}/docs/docs/self-hosting/manage/cli/mirror.mdx`
- Online: https://zitadel.com/docs/self-hosting/manage/cli/mirror

## High-Level Flow

1. Prepare the destination Postgres database (network, HA, backups).
2. Initialize an empty destination schema:
   ```bash
   zitadel init --config /path/to/new-config.yaml
   zitadel setup --for-mirror --config /path/to/new-config.yaml
   ```
3. Mirror data:
   ```bash
   zitadel mirror --system --config /path/to/mirror-config.yaml
   ```
4. Verify:
   ```bash
   zitadel mirror verify --system --config /path/to/mirror-config.yaml
   ```
5. Plan cutover:
   - stop writes to the old system (maintenance window) or repeat mirror with a final sync strategy
   - switch runtimes to the new Postgres-backed deployment

## Critical Constraints

- Keep the same masterkey and TLS mode assumptions across source/destination.
- Do not assume you can change the external domain as part of the migration.
- Read the limitations section in the upstream doc before executing in production.
