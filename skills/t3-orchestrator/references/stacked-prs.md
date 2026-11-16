# Stacked PRs

Read this when publishing, taking over, pushing, restacking, or monitoring a stack. Use the repository's stack tool when it has one; otherwise use verified Git and PR tooling. Keep the stack's base branches, head SHAs, and incremental diffs explicit.

## Build and update

1. The bottom PR targets the repository base branch. Each higher PR targets the preceding layer's branch. Verify the actual branch base and diff before creating or updating a PR, so each diff contains only that layer's change. Serialize dependent layers until their prerequisite commit exists; independent work can run concurrently.
2. After a lower layer changes or merges, inspect successors from bottom to top. Restack or retarget using the actual merge history. A squash merge may leave old ancestor commits in an upper diff. Recheck each incremental diff, PR base and description, then rerun affected checks on the resulting heads. Use evidence from each current head and base to assess readiness.
3. After creating, taking over, or pushing PRs, make the **next tool call** `link_pull_request` for one PR or `link_pull_requests` for multiple PRs, with full URLs for every stack layer. A child that publishes a PR should link it immediately. If linking fails, report it. The child reports its PR on the last line: `PR <full URL>, head <SHA>, checks and reviews <state>`.

## Checks, reviews, and handback

When the user asks for monitoring, or authorized work such as a merge still awaits checks or review, finish needed branch updates and pushes and address existing comments. The root then calls `watch_pull_request` and ends the turn. Use T3's wake instead of polling, sleep loops, `gh --watch`, Monitor, or ScheduleWakeup. T3 wakes the thread for new failures, required checks passing, reviews, comments, or conflicts. The watch persists across pushes and wakes, so assess the current head, required checks, reviews, comments, and conflicts on each wake without registering it again. A wake is not merge authorization. Delegated children do not watch PRs.

Before final handback, call `unwatch_pull_request` for each PR this thread watches. Link every PR created, taken over, or pushed; report a failed link. Only merge or force-push within the user's authorized scope and the repository's established process.
