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

Illustrative filled brief for the API node in the notes-app example; replace the sample commit and paths with verified values from the real repository:

```text
Objective: Add GET /api/search?query= to the notes app.
Base: Parent's committed HEAD 0123456789abcdef0123456789abcdef01234567
  on session/search, created from main.
Own: src/server/search.ts and tests/search.test.ts only.
Context: Notes are stored through src/server/notes.ts; the UI worker is blocked
  until this endpoint's response shape is committed and integrated into the
  parent checkout.
Acceptance: Return matching notes as {id,title} in stable title order; an empty
  query returns HTTP 400. Cover both cases in tests.
Coordination: Other workers own docs and UI. Preserve their edits. Do this work
  yourself; no recursive agents. Do not publish a PR in this assignment.
Check: Run `pnpm exec vitest run tests/search.test.ts` and `pnpm run typecheck`
  in this example project; report their outcomes and any uncovered gap.
Return: Changed files, commit SHA, response shape, test evidence, and blockers.
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

### Example: turn ends while the API delegate runs

Replace bracketed values with exact tool and Git results; these are fields, not live T3 links or PRs.

```text
Objective/scope: Notes search API then UI as two PRs; publishing authorized.
Parent: session/search @ [paste full HEAD SHA], based on main.
Dirty user file: notes/ideas.md, untouched and excluded from delegate base.
Frontier: API delegate running; docs independent; UI blocked by API response.
Delegate: taskId [paste delegate_task.taskId]; thread [paste its link verbatim].
PR stack: none yet; bases/heads/checks: not applicable. Active watch: none.
Next: end this turn per delegate_task.next. On wake read its result, inspect
  tests and commit, integrate API into session/search, then unlock UI.
Status: waiting on delegate, not a completed stack.
```

### Example: turn ends with the UI PR watched

Replace bracketed values with current tool results; record observation time alongside check results.

```text
Objective/scope: Finish authorized notes search stack after API squash merge.
Parent: session/search @ [paste actual HEAD]; dirty user file notes/ideas.md
  remains untouched.
Delegate record: API taskId [paste taskId], thread [paste returned link verbatim];
  completed and integrated. UI has no running child; children watch no PRs.
Stack: API [paste PR URL], base main, last head [paste API SHA], merged as
  squash [paste merge SHA]; its final-head checks passed at [paste timestamp].
  UI [paste PR URL], base main, head [paste current UI SHA]; incremental UI
  diff verified after restack. Old UI head checks/reviews are stale.
Checks/reviews at [paste timestamp]: required UI checks pending on current head;
  review state [paste observed state]. Blocker: UI checks/review.
Active watch: root watching UI PR.
Next: end this turn. On T3 wake inspect exact UI head, checks, reviews and
  conflicts; act on findings or hand back. Unwatch at final handback.
Status: waiting on watched PR, not a completed task or merge approval.
```
