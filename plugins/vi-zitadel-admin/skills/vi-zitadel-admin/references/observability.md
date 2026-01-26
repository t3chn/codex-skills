# Observability and operational signals

Use this when wiring monitoring/alerting or when diagnosing availability/performance issues.

## Health and readiness

ZITADEL exposes:

- Readiness: `GET /debug/ready`
- Liveness: `GET /debug/healthz`

Upstream reference:

- Online: https://zitadel.com/docs/apis/observability/health
- Repo path (optional): `docs/docs/apis/observability/health.md`

## Metrics

Metrics endpoint:

- `GET /debug/metrics` (Prometheus exposition format; implemented via OpenTelemetry)

Upstream reference:

- Online: https://zitadel.com/docs/self-hosting/manage/metrics
- Repo path (optional): `docs/docs/self-hosting/manage/metrics/overview.mdx`

## Logging

Prefer shipping logs to stdout/stderr and collecting them via your platform (journald, Kubernetes logging, log forwarders).

To adjust log level, format, and exporters, consult:

- `cmd/defaults.yaml` (Instrumentation + legacy logging sections) or https://github.com/zitadel/zitadel/blob/main/cmd/defaults.yaml
- https://zitadel.com/docs/self-hosting/manage/production (logging discussion)

## Minimal alert set (practical)

- Readiness fails for N minutes (no traffic should be routed)
- Liveness fails (process crash loop)
- Elevated request latency and 5xx rate
- Database connection saturation / long query times
- TLS certificate expiry within X days

## Troubleshooting shortcuts

- If readiness fails but liveness succeeds, suspect migrations/setup, database connectivity, or projections catching up.
- If console/API calls fail in-browser, validate HTTP/2 and proxy config (see `references/networking-http2-tls.md`).
