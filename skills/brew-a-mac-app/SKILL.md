---
name: brew-a-mac-app
description: Package compiled macOS apps as Homebrew casks and build verified GitHub release automation. Use for app tap setup, Stable/Canary distribution, signed release assets, or porting automatic cask publication to another repository.
---

# Brew a Mac App

Make the chosen macOS app installable from its actual published bytes. Match the project's existing build system, release policy and authorized scope. A cask correction needs only the relevant checks; porting a release pipeline needs its source, artifact and publication boundaries verified together. For research-only work, return a proposal without provisioning credentials or publishing.

Start by identifying the app bundle/token, source and release repositories, default branch, supported macOS/architectures, version/build scheme, updater and authenticated publisher. Inspect existing workflows and protections before proposing a publication path. Keep these values configurable; do not transplant another app's account IDs, paths, keys or version rules.

Read the reference for the current task:

| Task | Reference |
| --- | --- |
| Choose the tap layout, write a cask, or isolate Stable/Canary | [Casks and channels](references/casks-and-channels.md) |
| Build, sign, notarize, package, or publish immutable/source-only releases | [Build and release](references/build-and-release.md) |
| Automate publication after CI, including without a release PR | [GitHub publication](references/github-publication.md) |
| Test installation, inspect release evidence, or recover from a partial run | [Verification and recovery](references/verification-and-recovery.md) |

The core invariant is one traceable chain: approved source commit → tested app → final signed archive → immutable release → verified cask/update feed. Advance an install pointer only when its referenced binary exists and passes the required checks. Preserve channel separation and reject stale publication attempts.

Use current primary documentation linked in the references when platform behavior is uncertain. Keep optional Codex UI metadata independent of the portable instructions; the same skill folder and relative references must work in Claude Code and Codex.

Complete already authorized work without repeatedly seeking permission. Creating packaging files does not itself authorize a release, a new token, changes to protection/environment rules, or a wider publisher exception. If the chosen no-PR route is blocked, finish the reviewable files and report the exact missing permission rather than silently changing the repository policy.

Report what is installable, the source/tag and asset identity, the cask/feed publication state, checks actually run, and remaining limits. Local or mocked checks do not prove a live notarized release, an installed update, or physical Mac behavior.
