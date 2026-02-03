# Git from Coder Tasks (SSH-first)

## Why SSH (vs HTTPS)

Git pushes from Tasks can fail over HTTPS due to:

- external-auth wrappers in the workspace image
- missing token scopes (especially when changing `.github/workflows/*`)
- CI/app tokens that are read-only or restricted

SSH deploy keys avoid most of these issues.

## GitHub: deploy key (recommended for a single repo)

1) Get the Coder SSH public key (safe to share):

```bash
coder publickey
```

2) Add it to the repo as a **Deploy key** with **Write access**.

- UI: Repo → Settings → Deploy keys → Add deploy key
- CLI (requires `gh` auth with repo admin access):

```bash
OWNER="t3chn"
REPO="todo-parallel-sandbox"
gh api -X POST "/repos/$OWNER/$REPO/keys" \
  -f title="coder-task-write" \
  -f key="$(coder publickey)" \
  -F read_only=false
```

3) Use an SSH remote in the Task:

```bash
git remote set-url origin "git@github.com:$OWNER/$REPO.git"
git push -u origin <branch>
```

Note: GitHub deploy keys are repo-scoped. If you need write access across many repos, prefer a dedicated “machine user” SSH key or a GitHub App instead of reusing deploy keys.

## Workflow files: “workflow scope” failures

If a Task can push normal code but fails when adding/updating `.github/workflows/*`, it’s usually a token restriction.

- SSH deploy key with write access generally works.
- Otherwise use a PAT that includes `workflow` scope (less preferred; higher blast radius).

## Actions runs stuck in `queued`

Common causes:

- GitHub Actions disabled for the repo
- no available runners (self-hosted only, but none online)
- minutes/billing limits (personal/org policy)

Quick checks:

```bash
OWNER="t3chn"
REPO="todo-parallel-sandbox"
gh api "/repos/$OWNER/$REPO/actions/permissions"
gh api "/repos/$OWNER/$REPO/actions/runners" --jq ".total_count"
```

If `total_count` is `0`, you’re relying on GitHub-hosted runners. If jobs still queue forever, check Actions/billing/rate limits in the UI.

## GitLab: deploy key

GitLab also supports deploy keys. Add the public key, enable write access, and use:

```bash
git remote set-url origin "git@gitlab.com:<group>/<repo>.git"
```

