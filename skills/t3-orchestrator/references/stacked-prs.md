# Stacked PRs

Read this when publishing, taking over, pushing, restacking, or monitoring a stack. Use the repository's stack tool when it has one; otherwise use verified Git and PR tooling. Keep the stack's base branches, head SHAs, and incremental diffs explicit.

## Build and update

1. The bottom PR targets the repository base branch. Each higher PR targets the preceding layer's branch. Verify the actual branch base and diff before creating or updating a PR, so each diff contains only that layer's change. Serialize dependent layers until their prerequisite commit exists; independent work can run concurrently.
2. After a lower layer changes or merges, inspect successors from bottom to top. Restack or retarget using the actual merge history. A squash merge may leave old ancestor commits in an upper diff. Recheck each incremental diff, PR base and description, then rerun affected checks on the resulting heads. Use evidence from each current head and base to assess readiness.
3. After creating, taking over, or pushing PRs, make the **next tool call** `link_pull_request` for one PR or `link_pull_requests` for multiple PRs, with full URLs for every stack layer. A child that publishes a PR should link it immediately. If linking fails, report it. The child reports its PR on the last line: `PR <full URL>, head <SHA>, checks and reviews <state>`.

### Two-layer example

In an illustrative notes app, the parent's integration branch `session/search` starts at `main`. `API search` and `search documentation` are initially independent frontier nodes; `UI search` is blocked by the API response shape. Dispatch API and documentation concurrently, but keep unrelated documentation commits out of the API/UI stack base. When the API child returns, inspect its tests and integrate its commit into the parent checkout on `session/search`. Only then dispatch the UI child with `isolation:'worktree'`, so its prepared checkout contains the API commit.

Publish `feature/search-api` against `main`, then `feature/search-ui` against `feature/search-api`. The first PR's diff contains the endpoint and tests; the second contains the UI and its tests. Verify each diff against its actual PR base. If the API PR is squash-merged, inspect and restack the UI branch so its PR against `main` still contains only the UI change. Recheck the new head's checks and reviews before assessing readiness.

### API review changes after the UI branch exists

Suppose review asks the API PR to rename `{id,title}` to `{id,label}` after `feature/search-ui` already uses the old field. Update and validate `feature/search-api`, then bring that new API commit into the parent `session/search` checkout. The old UI branch still has the old API history: restack it onto the revised API branch, change the UI to read `label`, and verify the UI PR's diff against `feature/search-api` contains only UI work. If a new isolated UI delegate must make that repair, first make the revised API and current UI code available in the parent's committed HEAD; otherwise its worktree starts without the UI code. An existing UI owner's checkout can instead be updated from the revised API base.

Treat checks and reviews on the old API and UI heads as stale. Run affected tests on the new commits, verify both PR bases and incremental diffs, and update the PR descriptions. Push according to the repository's permitted update or force-push policy; make PR linking the next tool call after each push. If required checks or reviews remain pending, let the root watch and resume on T3's wake rather than polling.

## Checks, reviews, and handback

When the user asks for monitoring, or authorized work such as a merge still awaits checks or review, finish needed branch updates and pushes and address existing comments. The root then calls `watch_pull_request` and ends the turn. Use T3's wake instead of polling, sleep loops, `gh --watch`, Monitor, or ScheduleWakeup. T3 wakes the thread for new failures, required checks passing, reviews, comments, or conflicts. The watch persists across pushes and wakes, so assess the current head, required checks, reviews, comments, and conflicts on each wake without registering it again. A wake is not merge authorization. Delegated children do not watch PRs.

Before final handback, call `unwatch_pull_request` for each PR this thread watches. Link every PR created, taken over, or pushed; report a failed link. Only merge or force-push within the user's authorized scope and the repository's established process.
