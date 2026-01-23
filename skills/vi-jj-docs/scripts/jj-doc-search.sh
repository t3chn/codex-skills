#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  jj-doc-search.sh "<query>" [path-to-jj-checkout-or-docs-dir]

Search JJ markdown docs and print a truncated list of matches (to keep output small).

Resolution order:
  1) JJ_DOCS_DIR env var (docs dir or jj repo root)
  2) Optional path arg (docs dir or jj repo root)
  3) Walk up from CWD looking for docs/revsets.md

Examples:
  jj-doc-search.sh "bookmark track"
  jj-doc-search.sh "immutable_heads" ~/src/jj
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

query="$1"
path_arg="${2:-}"

docs_dir=""

resolve_docs_dir_from_path() {
  local path="$1"
  if [[ -z "${path}" ]]; then
    return 0
  fi
  if [[ -f "${path}/revsets.md" ]]; then
    docs_dir="${path}"
    return 0
  fi
  if [[ -f "${path}/docs/revsets.md" ]]; then
    docs_dir="${path}/docs"
    return 0
  fi
  return 0
}

resolve_docs_dir_from_path "${JJ_DOCS_DIR:-}"
resolve_docs_dir_from_path "${path_arg}"

if [[ -z "${docs_dir}" ]]; then
  dir="$(pwd)"
  while true; do
    if [[ -f "${dir}/docs/revsets.md" ]]; then
      docs_dir="${dir}/docs"
      break
    fi
    if [[ "${dir}" == "/" ]]; then
      break
    fi
    dir="$(dirname "${dir}")"
  done
fi

if [[ -z "${docs_dir}" || ! -d "${docs_dir}" ]]; then
  echo "Could not find JJ docs directory." >&2
  echo "Set JJ_DOCS_DIR to a jj checkout (or its docs dir), or pass a path arg." >&2
  exit 2
fi

if command -v rg >/dev/null 2>&1; then
  rg --color=never -n -S --glob '*.md' "${query}" "${docs_dir}" | head -n 200
else
  grep -RIn --include='*.md' -- "${query}" "${docs_dir}" | head -n 200
fi
