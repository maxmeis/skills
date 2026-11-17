# Verification and recovery

Primary documentation checked 2026-11-17: [Homebrew command reference](https://docs.brew.sh/Manpage), [Cask Cookbook](https://docs.brew.sh/Cask-Cookbook), [Apple notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [Sparkle publishing](https://sparkle-project.org/documentation/publishing/), and [immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

## Pick evidence appropriate to the task

For a cask edit, validate the actual definition, download and checksum. For a new pipeline, test its publication boundaries as well as app packaging. Use disposable repositories/environments for negative cases; unit fixtures should not modify live releases, protections or credentials.

Useful failure cases include a mismatched digest, missing binary, wrong channel/source/check integration, stale candidate ref, extra changed file, symlink cask, default-branch advance, reordered releases and repeated identical publication. Test source-only pointer preservation if that mode exists. Distinguish mocked API behavior from a live server result.

For a real binary release, download the public final assets and compare their hashes to the release metadata. Inspect the extracted bundle and executable architectures, then use the appropriate checks:

```sh
shasum -a 256 Example-1.2.3.zip
codesign --verify --deep --strict Example.app
codesign --display --verbose=4 Example.app
xcrun stapler validate Example.app
spctl --assess --type execute --verbose=2 Example.app
```

These checks cover different things. Confirm the intended Developer ID/team, runtime/timestamp and notarization result; a successful ad-hoc signature is not distribution evidence. If Sparkle is present, verify the archive signature with the embedded public key and compare the live feed with the immutable release feed. Do not claim a quarantined first launch from a download that lacks quarantine metadata.

## Exercise Homebrew

Use the actual tap and token, not a different cached or API-resolved cask. In a disposable Mac test environment where installation changes are authorized:

```sh
brew tap owner/tap https://github.com/owner/app-repository
brew trust --cask owner/tap/example
brew style owner/tap/example
brew audit --cask --online owner/tap/example
brew fetch --cask owner/tap/example
brew install --cask owner/tap/example
brew uninstall --cask owner/tap/example
```

Check the exact installed app version/path and preserve user configuration during normal uninstall. App launch, permission prompts, updater execution and `--zap` cleanup need separate authorized test cases; don't launch a production input utility or change its TCC/configuration solely to smoke-test packaging. A dry-run/fetch is useful evidence, but does not establish successful installation.

For channel support, test that each token downloads its channel, automatic updates remain on that feed, and switching behaves as documented. Test an upgrade from a prior installed version and after an in-app self-update. Never remove quarantine or disable Gatekeeper to make the test pass.

## Recover without mutating history

- A finished identical retry is a no-op. An outdated run must not advance cask/feed/latest pointers.
- A public binary with failed cask publication is a partial release: retain valid existing pointers, fix the publication cause and rerun only the authorized metadata path.
- An old asset may be referenced again only if it still satisfies the project's compatibility and version policy; do not silently downgrade installed users.
- A published immutable source-only release cannot gain a binary later. Use a new version/tag; a draft release can remain unpublished while its required assets are prepared.
- To restore earlier app behavior, normally publish a new, higher-version build containing the fix/revert. Do not move a tag or replace an immutable ZIP. Changes to the public updater or a manual downgrade need an explicit migration plan.

Finish with separate evidence for release publication, default-branch cask publication, Homebrew installation and updater behavior. List untested parts rather than combining them into a blanket “shipped” claim.
