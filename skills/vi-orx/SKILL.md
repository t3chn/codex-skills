---
name: vi-orx
description: "Orchestrate parallel agent development with anti-drift constraints using Beads (`bd`) as the source of truth and Coder Tasks (`coder task`) as execution: define strict scope (Objective/Must-Haves/Non-Goals/Constraints/Verification), spawn tasks, land PRs, and close/sync issues. Triggers: orx, agent drift, feature creep, beads+coworker tasks, parallel tasks."
---

# ORX (Beads → Coder Tasks → PR)

## Goal

Run parallel work safely: strict scope, small PRs, explicit verification, and serialized Beads updates.

## Task contract (anti-drift)

For tasks labeled `orx`, the Beads **Description** must include these headings:

```md
## Objective
One short sentence describing the result.

## Must-Haves (≤3)
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Non-Goals
- None

## Constraints
- None

## Verification
- Command(s) you will actually run (tests/lint/build).
```

Rules:

- Do ONLY the Must-Haves; no “bonus” improvements.
- If you discover extra work, create a new Beads issue (new bead) and stop.

## Parallel workflow (recommended)

1) Create Beads issues (small scope, 1 PR each). Label them `orx` if you want strict contract enforcement.
2) Spawn Coder Tasks from beads (one task per bead): `python3 scripts/spawn_coder_tasks.py ...`
3) Each Task works on a branch named after the bead id and opens a PR.
4) Merge PRs once verification passes.
5) Orchestrator closes beads and runs `bd sync` once.

## Beads hygiene (critical)

- Workers must not edit `.beads/*` (avoids cross-task merge conflicts).
- Only the orchestrator updates/closes issues and commits `.beads/issues.jsonl`.

## Tooling

- Run prek/pre-commit early and re-run after auto-fixes.
- Prefer SSH deploy keys for Git operations from Tasks when HTTPS tokens are restricted.

## Scripts (load as needed)

- Spawn tasks from beads: `scripts/spawn_coder_tasks.py`

