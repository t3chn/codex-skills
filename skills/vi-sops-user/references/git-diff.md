# Git diff with decryption

Use `textconv` so `git diff` shows decrypted content.

## Minimal setup (YAML)

`.gitattributes`:

```text
*.yaml diff=sopsdiffer
```

In the repo:

```sh
git config diff.sopsdiffer.textconv "sops decrypt"
```

After that, `git diff` will decrypt both sides before displaying the diff.
