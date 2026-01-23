# Rotation and `updatekeys`

## `sops rotate`

- Re-encrypts the file with a **new data key**.
- Use for routine rotation.
- Example: `sops rotate -i secrets.enc.yaml`

## `sops updatekeys`

- Re-applies keys/settings from `.sops.yaml` (creation rules) to an existing encrypted file.
- Use when:
  - recipients / fingerprints / KMS keys changed
  - you want existing secrets to follow new config
- Example: `sops updatekeys secrets.enc.yaml`
