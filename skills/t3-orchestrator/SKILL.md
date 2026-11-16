---
name: t3-orchestrator
description: Coordinates T3 Code engineering sessions across Claude and Codex, including delegated agents, separate checkouts, stacked pull requests, and resumable handoffs. Use when a user asks to orchestrate T3 work with agents or threads, build or maintain a PR stack, or resume a paused T3 session.
---

# T3 orchestration

Use T3's connected orchestration tools under their actual namespace and schema. Compose with the repository's existing build, review, and stack workflows. The user's request defines which external actions are authorized; planning a stack does not itself authorize publishing or merging it.

## Quick start

Claude Code: `/t3-orchestrator Coordinate the search API and UI as two stacked PRs; delegate ready work and checkpoint waits.`

Codex: `$t3-orchestrator Resume this T3 session, verify the current PR heads and checks, then continue the stack.`

## Workflow

1. **Establish the base.** Inspect the repository, current branch and HEAD, dirty changes, existing PRs, and any stack tooling. State the requested outcome and validation gates. Preserve uncommitted work; when a prerequisite needs a commit, stage only its paths or hunks. This step is complete when the starting commit and protected edits are known.

2. **Draw the task graph.** Give each node an owner, files or module boundary, deliverable, acceptance evidence, and blocking predecessors. Mark the **frontier**: nodes whose prerequisite outputs are accessible; isolated code tasks also need their prerequisite commits in the checkout base. A PR stack adds a dependency edge from each upper layer to the one below. Use [the session template](references/session-template.md) when the graph, a delegate brief, or a later handoff needs a durable record. Every node must be ready or have a named blocker.

3. **Dispatch the frontier.** Launch independent ready nodes concurrently when useful; keep blocked nodes out of separate checkouts until their base exists. Choose a native Claude or Codex child for work on your current setup; use T3 delegation when the task requires another provider, requested settings, background execution, or a separate checkout or PR. Read [T3 runtime and delegation](references/t3-runtime.md) before dispatching a T3 child or opening a top-level thread. Give each child a self-contained brief with ownership, committed base, acceptance criteria, checks, and expected return. Record each dispatched task or thread ID for the checkpoint.

4. **Integrate and advance.** Read completed child results, inspect their changes, check acceptance evidence, integrate required commits into the parent base, and run relevant checks. Only then mark a node complete and recompute the frontier; a child checkout's HEAD does not update the parent's HEAD. Route an independent review through the same child-selection rules; each T3 review or recheck needs a fresh delegate. Resolve significant findings and verify the affected node again. Repeat until every requested node is integrated and validated, or a concrete blocker remains.

5. **Publish the stack when authorized.** For each PR layer, establish the exact preceding base and verify its incremental diff. Read [stacked PRs](references/stacked-prs.md) before creating, taking over, pushing, restacking, or monitoring a stack. This step is complete when every published layer has the intended base, current head SHA, link, and check/review state.

6. **Finish or park.** If required work is complete, report the result, validation, PR links, and any unresolved limits. Unwatch this thread's PRs before final handback. If a T3 delegate says completion will wake the thread, or a watched PR is waiting on checks or review, end this turn and let T3 resume it; keep a checkpoint with the next action. A parked session is complete for this turn only when its pending task or watch and its resume condition are explicit. On resume, verify live Git and PR state before acting on saved details.
