# GitHub publication without a release PR

Primary documentation checked 2026-11-17: [workflow triggering and token behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [workflow_run](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run), [secure workflow use](https://docs.github.com/en/actions/reference/security/secure-use), [ruleset layering](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

This is a design for an explicitly requested automatic metadata path. A cask PR remains valid when the project requires one. Do not impose direct publication, remove review gates, or create an owner exception merely because another repository uses this pattern.

## Establish authority first

Separate commit attribution from authentication. `git user.name`/email label a commit; the push/API token determines its actual authority. A GitHub App is optional. An approved user token can publish as the configured account; verify its actual login and numeric ID through the API before writing.

Prefer credentials scoped to the destination repository and required operations. Determine Contents, Actions, Checks and any Workflow permissions from the actual endpoints and Git pushes; do not copy another repository's scopes. Changing workflow files may require additional permission. Keep tokens out of remotes, arguments and logs; use process-local credential configuration or a supported credential mechanism.

An ordinary `GITHUB_TOKEN` push generally does not start another push workflow. An authorized user token can, or an explicit workflow dispatch can supply a deliberate trigger. Pick one mechanism and verify it: sending push and dispatch for the same candidate can race concurrency cancellation and leave a required check canceled.

Inspect effective classic protection and rulesets before designing a direct default-branch write. If publication requires an exception to PR/review rules, it must already be authorized and narrowly assigned. Keep strict required CI and non-fast-forward/deletion protection in rules the publisher cannot bypass. A ruleset's actor exception is not restricted to a cask path or to PRs authored by that actor; the publisher must enforce its path boundary itself. If the existing controls do not permit this route, stop at prepared files and report the policy decision needed. Do not use an admin merge or fabricate review approval as a workaround.

## Stage metadata and run normal CI

After a binary release is public and verified, create a commit based on current default-branch history changing only `Casks/<channel-token>.rb`. An internal branch such as `release-casks/<channel>` holds this candidate; it is not the user-facing tap branch.

Use one configured channel-to-path mapping, not a path supplied by an untrusted event. Serialize publication where concurrent releases can race. Reuse identical candidates; refuse a stale version over a newer one. Updating a managed staging branch can use an exact force-with-lease if the project permits it. Never force-push the default branch.

Run required CI on the exact candidate. Keep the required check context stable and emitted even when change selection fails. Linux may run metadata/content checks when the full changed-path set is known not to affect the app; preserve release/schema/automation checks, test both sides of renames, and use native checks for unknown ranges or changes affecting app/build/workflow behavior. Do not optimize by marking a required job successful without its required validation.

## Finalize using trusted code

A `workflow_run` finalizer can access elevated credentials. Filter it to successful expected CI events, same-repository candidates and managed branches, but also recheck everything through the API. Execute publisher scripts from trusted default-branch code. Never run scripts, local actions, Ruby casks or executable artifacts from the candidate/fork in that privileged job.

Before writing, verify:

- Repository, workflow identity/path, event type, completed-success status and full head SHA match the accepted run.
- The exact required check came from the expected GitHub Actions integration, succeeded on that SHA and belongs to that run. A check name alone is insufficient.
- The staging ref still points at the checked SHA. Its single parent is approved default-branch history, and its diff changes exactly one allowed regular cask file.
- The channel/tag resolves to the approved source; the release is published with the expected mode/channel and immutable status when required.
- The final binary and cask assets exist. The downloaded cask hash and binary hash match trusted release digests; its URL, version and content match validated metadata. Do not execute Ruby to inspect candidate content.
- The current default-branch cask is not newer. If its content already matches, return success without a write.

Fast-forward only that checked candidate when its parent is still the current default-branch tip. If the branch advanced, rebuild the candidate on its new tip and require fresh CI; do not transplant old CI onto a new SHA. A concurrent push rejection is retryable only when verified branch advancement explains it. Authentication, policy or validation failures must stay visible.

Bound network retries and rebase/CI requeues with a configured attempt or time budget. On exhaustion, stop with the exact release/candidate state and leave valid install pointers intact; do not keep generating candidates indefinitely or broaden permissions to make a retry succeed.

Keep renderer compatibility across old immutable releases. If finalization compares a published cask to generated text, preserve the generator version that produced it or introduce an explicit validated migration. A template cleanup must not make legitimate old retries fail or authorize arbitrary modified metadata.

After finalization, verify the cask from the actual default branch and its downloadable binary. Publish clear source/tag/artifact links and leave ordinary application changes on the repository's normal PR/review path.
