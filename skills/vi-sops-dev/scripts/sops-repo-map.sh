#!/usr/bin/env bash
set -euo pipefail

root="${1:-.}"

if [[ ! -f "${root}/go.mod" ]]; then
  echo "No go.mod found at: ${root}" >&2
  exit 2
fi

if command -v rg >/dev/null 2>&1; then
  has_module="$(rg -q '^module github.com/getsops/sops/v3$' "${root}/go.mod" && echo yes || echo no)"
else
  has_module="$(grep -q '^module github.com/getsops/sops/v3$' "${root}/go.mod" && echo yes || echo no)"
fi

if [[ "${has_module}" != "yes" ]]; then
  echo "go.mod does not look like getsops/sops (module github.com/getsops/sops/v3)." >&2
  exit 3
fi

cat <<'EOF'
SOPS quick dev map

Key entry points:
  - cmd/sops/main.go                  (CLI wiring; flags + commands)
  - cmd/sops/edit.go                  (editor flow)
  - cmd/sops/encrypt.go               (encrypt new file)
  - cmd/sops/decrypt.go               (decrypt)
  - cmd/sops/common/                  (shared CLI helpers)
  - sops.go                           (Tree/Metadata/store interfaces, MAC, key groups)
  - config/config.go                  (.sops.yaml lookup + parsing)
  - stores/                           (format implementations)
  - keys/keys.go                      (MasterKey interface)
  - keyservice/                       (gRPC keyservice protocol + helpers)
  - functional-tests/                 (Rust e2e tests)

Common commands:
  - make test
  - make functional-tests
  - make staticcheck
  - make checkdocs

Common ripgrep searches:
  - rg -n "Name:\\s+\\\"edit\\\"" cmd/sops/main.go
  - rg -n "func (edit|encrypt|decrypt)\\(" cmd/sops
  - rg -n "type MasterKey interface" keys
  - rg -n "KeyTypeIdentifier" (kms|gcpkms|azkv|hckms|hcvault|age|pgp)
EOF
