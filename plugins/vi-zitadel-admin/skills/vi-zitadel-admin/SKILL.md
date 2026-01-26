---
name: vi-zitadel-admin
description: This skill should be used when the user asks to "configure ZITADEL", "deploy ZITADEL", "troubleshoot ZITADEL", "debug ZITADEL", "upgrade ZITADEL", "harden ZITADEL for production", "fix Instance not found error", "configure TLS for ZITADEL", "set up ZITADEL database", "migrate from CockroachDB to Postgres", "configure ZITADEL masterkey", "check ZITADEL health", or works with ZITADEL deployment config (Helm, Docker Compose, Linux service), ZITADEL config/steps YAML, or self-hosted ZITADEL runtime issues. Provides reliable self-hosted ZITADEL administration and day-2 operations guidance with configuration-only changes.
---

# ZITADEL Administration

Administer self-hosted ZITADEL via configuration and operational workflows. Avoid patching ZITADEL source unless explicitly requested.

## Quick Intake (Ask First)

Before proceeding with ZITADEL tasks, gather context:

- **Deployment**: Kubernetes (Helm), Docker Compose, or Linux/service
- **Version/DB**: ZITADEL major version (v2 vs v3), Postgres vs CockroachDB (v2 only)
- **External access**: `ExternalDomain`, TLS termination (`--tlsMode`), reverse proxy/WAF/CDN, HTTP/2/h2c
- **Config delivery**: where `--config` and `--steps` files live; how `--masterkey*` is provided

## Source of Truth (Upstream)

Use the upstream ZITADEL repo + docs as the authoritative config catalog:

- Runtime defaults + env var mapping: https://github.com/zitadel/zitadel/blob/main/cmd/defaults.yaml
- Setup steps defaults + env var mapping: https://github.com/zitadel/zitadel/blob/main/cmd/setup/steps.yaml
- Self-hosting docs: https://zitadel.com/docs/self-hosting

If there is a local clone, prefer grepping local files for speed/offline work (any path; example: `~/contrib/zitadel`).

## Recommended Workflow

1. Locate current runtime config (`--config`) and setup steps (`--steps`).
2. Compare against the production checklist and close gaps (TLS/HTTP/2, non-default credentials, SMTP, backups, observability).
3. Apply changes as configuration-only:
   - Use multiple `--config` / `--steps` files to separate public config from secrets.
   - Keep secrets out of git (masterkey, DB creds, SMTP creds, TLS private key).
4. For installs/upgrades, follow the phase separation:
   - First install: `zitadel init` (once) → `zitadel setup` → `zitadel start`
   - Upgrade: run `zitadel setup` with the new version, then roll out `zitadel start`
5. Verify with health endpoints and logs:
   - Ready: `/debug/ready`
   - Health: `/debug/healthz`
   - Metrics: `/debug/metrics`

## Common Tasks (Short Recipes)

### Find Config Keys

Search `cmd/defaults.yaml` and `cmd/setup/steps.yaml` in the ZITADEL repo (look for `# ZITADEL_...` comments).

### Fix "Instance not found"

1. Validate `ExternalDomain`, `ExternalPort`, `ExternalSecure` match public access
2. Check reverse proxy host headers
3. Rerun `zitadel setup`

### Prepare for Production

Follow `references/production-hardening.md` and cross-check the upstream production checklist.

### Plan Upgrades and Scaling

Use `references/upgrade-scaling.md` for init/setup/start separation, probes, zero downtime.

### Validate Database Posture

Use `references/database.md` for supported versions, credential rotation, v2→v3 CRDB migration notes.

### Verify HTTP/2 + TLS

Use `references/networking-http2-tls.md` for TLS modes, reverse proxy configuration.

## Reference Files

For detailed guidance on specific topics, consult:

- **`references/config-discovery.md`** - Config discovery and file layout, runtime vs setup separation
- **`references/production-hardening.md`** - Production hardening checklist
- **`references/upgrade-scaling.md`** - Init/setup/start phases, upgrades, scaling
- **`references/database.md`** - Database operations, Postgres vs CockroachDB, credential rotation
- **`references/networking-http2-tls.md`** - HTTP/2, h2c, TLS modes, reverse proxies
- **`references/observability.md`** - Readiness/liveness/metrics/logging
- **`references/migration-crdb-to-pg.md`** - Migration from CockroachDB to Postgres (v2 to v3)
