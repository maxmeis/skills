# T3 session template

Use only the sections relevant to the task. Keep this in a planning note, issue, or conversation; the skill does not require a new file in the repository.

## Kickoff

```text
Outcome:
Authorized scope and external actions:
Repository / remote / default branch:
Current branch / HEAD / dirty changes:
Existing threads, PRs, and stack tooling:
Validation gates:
Integration owner:
```

## Work map

| Task | Owner / tool | Owned files | Depends on | Deliverable and validation | State / task ID / thread link |
| --- | --- | --- | --- | --- | --- |
| A |  |  |  |  |  |

For a `delegate_task`, supply a complete brief. The child does not inherit this session:

```text
Objective and acceptance criteria:
Repository, branch, committed base SHA, relevant context:
Owned files or modules and interfaces with other tasks:
Dependencies already available; work that must wait:
Constraints, including existing dirty changes and other workers:
Permission to delegate further, if any:
Required checks and review scope:
Return: files changed, tests and results, blockers, PR URL and head SHA if created.
```

## PR stack

| Layer | Branch / head SHA | PR URL | PR base branch | Depends on | Checks / reviews / conflicts | T3 linked / watched |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |

## Checkpoint or resume handoff

```text
As of (time):
Objective and current outcome:
Repo / worktree / branch / exact HEAD; dirty files:
Completed and validated work (commands and outcomes):
Delegates (task ID, thread link, state, expected result):
Stack (bottom to top: URL, base branch, head SHA, linked status):
Checks, reviews, conflicts, and their observation time:
Active PR watches:
Unknowns or decisions requiring user input:
Next safe action and its prerequisite:
```

On resume, recheck live state before relying on a saved head SHA, check result, review, or branch base.
