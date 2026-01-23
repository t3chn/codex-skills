# Partial encryption and MAC mismatch

## What this is

- By default SOPS encrypts **values** and keeps keys in plaintext.
- Even if some values remain plaintext, they may still be covered by the MAC, so manual edits often cause **MAC mismatch** on decrypt.

## How to keep some parts plaintext

Options (mutually exclusive; choose one):

- `_unencrypted` suffix (default): keys ending with `_unencrypted` stay plaintext.
- `--encrypted-regex` / `--unencrypted-regex` (or the same fields in `.sops.yaml`)
- `--encrypted-suffix` / `--unencrypted-suffix`
- `--encrypted-comment-regex` / `--unencrypted-comment-regex` (YAML comments)

## About `mac_only_encrypted`

- If you enable `mac_only_encrypted: true` (or the `--mac-only-encrypted` flag at creation time), the MAC is computed only over values SOPS actually encrypted.
- This reduces MAC mismatch for plaintext edits, but changes integrity guarantees: plaintext is no longer protected by the MAC.
