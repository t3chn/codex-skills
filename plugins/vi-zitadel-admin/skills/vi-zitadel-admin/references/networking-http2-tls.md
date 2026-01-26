# Networking, HTTP/2, and TLS

Use this when configuring external access, reverse proxies, or debugging console/API issues caused by HTTP/2 or Host header handling.

Upstream references:

- External access and "Instance not found": https://zitadel.com/docs/self-hosting/manage/custom-domain
- TLS modes: https://zitadel.com/docs/self-hosting/manage/tls_modes
- HTTP/2 requirement: https://zitadel.com/docs/self-hosting/manage/http2
- Reverse proxy examples: https://zitadel.com/docs/self-hosting/manage/reverseproxy/reverse_proxy

Repo path (optional): `docs/docs/self-hosting/manage/` (files: `custom-domain.md`, `tls_modes.mdx`, `http2.mdx`, reverse proxy examples under `reverseproxy/`).

## ExternalDomain, ExternalPort, ExternalSecure

ZITADEL serves requests only for the expected protocol/host/port.

- Set `ExternalDomain`, `ExternalPort`, `ExternalSecure` to match how end users reach ZITADEL.
- After changing any of these, rerun `zitadel setup` so the system picks up the changes.

## TLS modes

ZITADEL supports three operational modes (often configured via `--tlsMode`):

- `disabled`: plain HTTP (test only)
- `external`: terminate TLS upstream (reverse proxy/WAF/service mesh) but instruct clients to use HTTPS
- `enabled`: ZITADEL terminates TLS itself (configure `TLS.*`)

Pick the mode that matches your network boundary and certificate management.

## HTTP/2 and h2c (common pitfall)

ZITADEL uses HTTP/2 for gRPC and the console (gRPC-Web). Your reverse proxy must support HTTP/2 end-to-end.

- If TLS is terminated upstream and traffic to ZITADEL is plaintext, ensure the proxy supports **h2c** to ZITADEL.
- If the console shows gRPC errors or fails to load, suspect missing HTTP/2 or incorrect proxy config first.

## Reverse proxy header handling

ZITADEL uses the request Host header (or forwarded host) to select the virtual instance.

When running behind a proxy:

- Preserve the original `Host` header, or
- Populate forwarded headers so ZITADEL can recover the public host.

If users see "Instance not found", validate:

- external config matches public domain/port
- proxy sends correct Host / forwarded host
- `zitadel setup` has been rerun after changing external settings

## Performance notes

- Enable compression (gzip/brotli) for UI assets if your proxy supports it.
- Consider a CDN for static assets to reduce latency and offload traffic.
