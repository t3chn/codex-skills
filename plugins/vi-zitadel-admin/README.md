# vi-zitadel-admin

Claude Code plugin for self-hosted ZITADEL administration and day-2 operations.

## Overview

This plugin provides knowledge and guidance for administering self-hosted ZITADEL deployments through configuration-only changes. It covers initial setup, hardening, upgrades, scaling, backups, observability, and common troubleshooting scenarios.

## Features

- Configuration discovery and management (runtime vs setup steps)
- Production hardening checklist
- Upgrade and scaling workflows (init/setup/start phases)
- Database operations (Postgres, CockroachDB migration)
- HTTP/2 and TLS configuration
- Observability setup (metrics, health endpoints, logging)
- Troubleshooting common issues (Instance not found, gRPC errors)

## Installation

Copy or symlink the plugin to your Claude Code plugins directory:

```bash
# Option 1: Symlink
ln -s /path/to/vi-zitadel-admin ~/.claude/plugins/vi-zitadel-admin

# Option 2: Copy
cp -r /path/to/vi-zitadel-admin ~/.claude/plugins/
```

## Configuration

### ZITADEL Repository Path

Create a settings file at `.claude/vi-zitadel-admin.local.md` in your project to configure the local ZITADEL repository path:

```yaml
---
zitadel_repo: ~/contrib/zitadel
---
```

If not configured, the skill defaults to `~/contrib/zitadel`.

The local ZITADEL repo is used as the authoritative source for:
- `cmd/defaults.yaml` - Runtime configuration defaults
- `cmd/setup/steps.yaml` - Setup steps defaults
- `docs/docs/self-hosting/manage/` - Offline documentation

## Usage

The skill activates automatically when you ask about ZITADEL administration tasks:

- "How do I configure ZITADEL for production?"
- "Fix Instance not found error"
- "Set up TLS for ZITADEL"
- "Upgrade ZITADEL to v3"
- "Migrate from CockroachDB to Postgres"

## Skill Structure

```
vi-zitadel-admin/
├── .claude-plugin/
│   └── plugin.json
├── README.md
└── skills/
    └── vi-zitadel-admin/
        ├── SKILL.md
        └── references/
            ├── config-discovery.md
            ├── production-hardening.md
            ├── upgrade-scaling.md
            ├── database.md
            ├── networking-http2-tls.md
            ├── observability.md
            └── migration-crdb-to-pg.md
```

## Reference Topics

| File | Description |
|------|-------------|
| config-discovery.md | Config key discovery, runtime vs setup separation |
| production-hardening.md | Security and reliability checklist |
| upgrade-scaling.md | Init/setup/start phases, zero-downtime upgrades |
| database.md | Postgres/CockroachDB operations, credential rotation |
| networking-http2-tls.md | HTTP/2, TLS modes, reverse proxy configuration |
| observability.md | Health endpoints, metrics, logging |
| migration-crdb-to-pg.md | CockroachDB to Postgres migration guide |
