#!/usr/bin/env bash
set -euo pipefail

target="${1:-.sops.yaml}"

if [[ -e "${target}" ]]; then
  echo "Refusing to overwrite existing file: ${target}" >&2
  exit 2
fi

cat > "${target}" <<'YAML'
# creation_rules are evaluated sequentially (first match wins)
creation_rules:
  # Example: encrypt all YAML files with age
  - path_regex: \\.ya?ml$
    age: age1REPLACE_ME_WITH_RECIPIENT

  # Example dev/prod split (uncomment and edit)
  # - path_regex: \\.dev\\.ya?ml$
  #   age: age1DEV_RECIPIENT
  # - path_regex: \\.prod\\.ya?ml$
  #   age: age1PROD_RECIPIENT

# Optional store formatting (uncomment as needed)
# stores:
#   yaml:
#     indent: 4
#   json:
#     indent: 2
YAML

echo "Wrote ${target}"

