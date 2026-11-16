# T3 runtime and delegation

Read this before a T3 `delegate_task` or top-level thread launch. Tool names and fields can vary by connection; discover the available namespace and schema. Use T3 tools directly rather than an invented CLI.

## Child selection and dispatch

- For a same-provider child on a model offered by the native agent tool and no settings beyond yours, use Claude `Agent` with `run_in_background:false`, or Codex `spawn_agent` and wait for completion.
- Use `delegate_task` for another provider, a user-named model or settings, background work, an isolated checkout or PR, or an explicit request for `delegate_task`. Call `orchestrator_capabilities` once per thread before the first delegation. Call it again only after an error or a user-named provider change. Put supported settings in `target.options`. If a requested provider or model is unavailable, report that; await user direction rather than silently substituting a model, native agent, workflow, or CLI.
- A delegated child receives only `task`, not parent history. Include the outcome, committed base SHA, context needed to find the code, owned files, dependencies, constraints, checks, and return format. Tell workers they share the codebase, must preserve others' edits, and may delegate further only when their task explicitly allows it.
- Use `isolation:'worktree'` for a child that needs a separate checkout or PR. T3 creates that checkout from the parent's committed HEAD; dirty edits are absent and `delegate_task` has no base selector. Integrate a child's prerequisite commits into the parent's HEAD before dispatching its dependent layer. Let independent nodes run concurrently. Leave child checkout creation to T3, including for delegated reviews.
- A T3 review or recheck is a new `delegate_task` with its own brief. Fix small findings locally. Stop a replaced or unneeded delegate with `task_cancel`; use it instead of interrupting the child thread.
- Follow the response's `next`. When it says completion wakes this thread, end your turn. Read the result after the wake; use `task_status` then if needed. Waiting means no polling, sleep loop, or watcher. A completed child turn with live delegated work is not a completed task.

## Top-level threads

`t3_thread_launch` and `create_threads` create top-level threads, only when the user asks for new threads. For a thread worktree, set `workspaceStrategy` on `t3_thread_launch`. Honor a requested base. Otherwise use the default branch as `remote/branch` with `startFromOrigin:true` for independent work when a remote exists; use the local default without a remote. Dependent work and required unpublished commits use the appropriate local `baseRef` with `startFromOrigin:false`. Without `workspaceStrategy`, the launch uses the project root rather than your current worktree. Let T3 prepare the checkout; do not create one in the shell or task text.

Before answering about a thread identified by ID, read it with `t3_thread_read`. Mention it by the returned `link` verbatim, including in a handoff.
