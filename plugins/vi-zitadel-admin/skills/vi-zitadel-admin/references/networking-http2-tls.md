# Networking, HTTP/2, and TLS

Use this when configuring external access, reverse proxies, or debugging console/API issues caused by HTTP/2 or Host header handling.

Upstream references:

- External access and "Instance not found": `{zitadel_repo}/docs/docs/self-hosting/manage/custom-domain.md`
- TLS modes: `{zitadel_repo}/docs/docs/self-hosting/manage/tls_modes.mdx`
- HTTP/2 requirement: `{zitadel_repo}/docs/docs/self-hosting/manage/http2.mdx`
- Reverse proxy examples: `{zitadel_repo}/docs/docs/self-hosting/manage/reverseproxy/`

## ExternalDomain, ExternalPort, ExternalSecure

ZITADEL serves requests only for the expected protocol/host/port.

- Set `ExternalDomain`, `ExternalPort`, `ExternalSecure` to match how end users reach ZITADEL.
- After changing any of these, rerun `zitadel setup` so the system picks up the changes.

## TLS Modes

ZITADEL supports three operational modes (often configured via `--tlsMode`):

- `disabled`: plain HTTP (test only)
- `external`: terminate TLS upstream (reverse proxy/WAF/service mesh) but instruct clients to use HTTPS
- `enabled`: ZITADEL terminates TLS itself (configure `TLS.*`)

Pick the mode that matches your network boundary and certificate management.

## HTTP/2 and h2c (Common Pitfall)

ZITADEL uses HTTP/2 for gRPC and the console (gRPC-Web). The reverse proxy must support HTTP/2 end-to-end.

- If TLS is terminated upstream and traffic to ZITADEL is plaintext, ensure the proxy supports **h2c** to ZITADEL.
- If the console shows gRPC errors or fails to load, suspect missing HTTP/2 or incorrect proxy config first.

## Reverse Proxy Header Handling

ZITADEL uses the request Host header (or forwarded host) to select the virtual instance.

When running behind a proxy:

- Preserve the original `Host` header, or
- Populate forwarded headers so ZITADEL can recover the public host.

If users see "Instance not found", validate:

- external config matches public domain/port
- proxy sends correct Host / forwarded host
- `zitadel setup` has been rerun after changing external settings

## Performance Notes

- Enable compression (gzip/brotli) for UI assets if the proxy supports it.
- Consider a CDN for static assets to reduce latency and offload traffic.
