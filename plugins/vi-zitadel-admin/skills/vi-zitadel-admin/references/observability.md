# Observability and Operational Signals

Use this when wiring monitoring/alerting or when diagnosing availability/performance issues.

## Health and Readiness

ZITADEL exposes:

- Readiness: `GET /debug/ready`
- Liveness: `GET /debug/healthz`

Upstream reference:

- Local: `{zitadel_repo}/docs/docs/apis/observability/health.md`
- Online: https://zitadel.com/docs/apis/observability/health

## Metrics

Metrics endpoint:

- `GET /debug/metrics` (Prometheus exposition format; implemented via OpenTelemetry)

Upstream reference:

- Local: `{zitadel_repo}/docs/docs/self-hosting/manage/metrics/overview.mdx`
- Online: https://zitadel.com/docs/self-hosting/manage/metrics

## Logging

Prefer shipping logs to stdout/stderr and collecting them via your platform (journald, Kubernetes logging, log forwarders).

To adjust log level, format, and exporters, consult:

- `{zitadel_repo}/cmd/defaults.yaml` (Instrumentation + legacy logging sections)
- `{zitadel_repo}/docs/docs/self-hosting/manage/production.md` (logging discussion)

## Minimal Alert Set (Practical)

- Readiness fails for N minutes (no traffic should be routed)
- Liveness fails (process crash loop)
- Elevated request latency and 5xx rate
- Database connection saturation / long query times
- TLS certificate expiry within X days

## Troubleshooting Shortcuts

- If readiness fails but liveness succeeds, suspect migrations/setup, database connectivity, or projections catching up.
- If console/API calls fail in-browser, validate HTTP/2 and proxy config (see `references/networking-http2-tls.md`).
