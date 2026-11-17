# Casks and channels

Primary documentation checked 2026-11-17: [tap authoring](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap), [Cask Cookbook](https://docs.brew.sh/Cask-Cookbook), [Tap Trust](https://docs.brew.sh/Tap-Trust), [Acceptable Casks](https://docs.brew.sh/Acceptable-Casks), and [Homebrew FAQ](https://docs.brew.sh/FAQ). Recheck changing syntax against the installed Homebrew release.

## Choose the package and repository

A compiled `.app` is normally distributed as a cask. CLI-only source builds belong in formula/bottle workflows; do not turn a requested CLI into an app merely to use this skill.

The app repository can itself be the tap. Put `Casks/<token>.rb` at the root of its default branch. A dedicated tap is another valid choice when the project needs it. Preserve the chosen layout instead of requiring a repository rename or a second repository.

The short `brew tap owner/name` normally resolves a GitHub repository named `owner/homebrew-name`. For an app repository without that prefix, document the explicit URL:

```sh
brew tap owner/tap https://github.com/owner/app-repository
brew install --cask owner/tap/example
```

`owner/tap` is the local tap name; the URL determines its actual Git remote. Inspect both when debugging. Users receive casks from the tap's default branch, not from internal staging branches. A fully qualified install grants trust to that item. For inspection commands needing prior trust, use `brew trust --cask owner/tap/example`; avoid trusting an entire tap by default.

For public installation, both the tap and binary endpoint must be accessible to the intended users. Private repository Git access and private asset-download authentication are separate problems. Never embed a token in a public cask URL.

## Render from a real release

Configure the exact app name, bundle ID, token, repository, source tag, asset filename, version/build mapping and supported OS/architectures once. Generate the cask from the final artifact URL and downloaded ZIP/DMG checksum. Example structure, with project-specific values to replace:

```ruby
cask "example" do
  version "1.2.3"
  sha256 "FINAL_ZIP_SHA256"

  url "https://github.com/OWNER/REPO/releases/download/v#{version}/Example-#{version}.zip"
  name "Example"
  desc "Short factual description"
  homepage "https://github.com/OWNER/REPO"

  depends_on macos: :sonoma
  depends_on arch: :arm64

  app "Example.app"
end
```

The Sonoma/ARM64 constraints are examples, not defaults for every app. Inspect the artifact's declared minimum and executable architectures. Use a literal versioned URL with a pinned checksum for immutable releases. Never calculate the cask checksum before the final signing/stapling/archive step.

Set `auto_updates true` only if the installed app actually self-updates. Homebrew and the app's updater have separate state; test upgrades after an in-app update rather than assuming their recorded versions match. Use `livecheck` when detection needs explicit control, or a documented skip when the project's publisher deliberately owns updates. A source-only or wrong-channel release must never become the detected binary version.

Add uninstall handling for actual helpers/installers. Derive optional `zap` paths from the app's real storage and review them; ordinary uninstall should preserve user configuration. Own-tap distribution does not inherit the official `homebrew/cask` admission thresholds or contribution/AI-disclosure workflow. Read those requirements when the task is specifically an upstream submission.

## Stable and Canary, when requested

Use an unversioned token for the normal channel and an explicit token such as `example@canary` for the opt-in channel. Keep their asset URLs and install/update pointers separate. If both replace the same `.app` or share one bundle identity, declare the conflict and document uninstall/install switching; do not claim side-by-side support.

Map public prerelease tags to numeric Apple bundle versions rather than writing a suffix such as `-canary` into `CFBundleShortVersionString`. Keep the cask display version consistent with the actual bundle. Preserve the project's ordering scheme within each feed.

For strict Sparkle isolation, separate feed selection prevents the Canary feed from affecting Stable users. Sparkle's allowed-channel set always includes its default channel, so merely adding a named channel does not exclude default-channel updates. Key separation is an optional design decision with migration implications; inspect the existing app before changing it. See [Sparkle publishing](https://sparkle-project.org/documentation/publishing/) and [updater delegation](https://sparkle-project.org/documentation/api-reference/Protocols/SPUUpdaterDelegate.html). Changing channels may require manual installation if the target build sorts lower or uses another signing key.
