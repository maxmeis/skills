# Build and release

Primary documentation checked 2026-11-17: [Apple notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [bundle marketing version](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundleshortversionstring), [bundle build version](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundleversion), [Sparkle publishing](https://sparkle-project.org/documentation/publishing/), and [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

## Establish source and build inputs

Follow the project's chosen trigger. For a requested two-channel model, Stable can be a deliberate versioned owner dispatch and Canary an automatic build for app-related default-branch changes. Preserve other explicitly chosen policies. Exclude unrelated docs/site/cask commits from automatic app releases when the dependency map supports it.

Record the full authorized source SHA, channel, public tag/version, bundle short/build versions, artifact names, supported OS/architectures and updater configuration. Make the build and metadata renderer share these inputs. A checked-in configuration or versioned release manifest is useful when separate scripts otherwise repeat them; do not introduce another source of truth for a small cask fix.

Check out the authorized SHA and verify the resulting checkout before testing, tagging and building. Distinguish a Git tag from a branch name and verify annotated tags through their peeled commit. Tests on a different commit do not authorize publication. Do not allocate a Stable version or dispatch a live release merely to demonstrate a pipeline.

## Signing modes

Ordinary local and PR builds can use explicit ad-hoc signing (`codesign --sign -`) without an Apple account. Keep release credentials out of untrusted PR jobs. Some provisioned capabilities require Apple-issued identities even in development; inspect the app rather than making ad-hoc signing universal.

For outside-store binary distribution, use the authorized Developer ID identity, hardened runtime and timestamp, with entitlements appropriate to the app. Sign nested frameworks/XPC helpers inside-out and preserve their entitlements. Do not use `codesign --deep` as a substitute for correct signing; deep verification is a separate check.

Keep certificates, passwords, notary credentials and updater private keys in protected CI secrets. Use a temporary keychain with cleanup and the project's required production approval. Invocation of this skill is not permission to import a new certificate, replace secrets, or approve a deployment on another person's behalf.

## Finalize bytes before publication

1. Build/test the selected source and inspect the actual bundle version, channel, architecture, minimum OS and updater metadata.
2. Sign, create a supported notary submission archive (ZIP, DMG or PKG), submit it with `notarytool` and wait for an accepted result. Staple the supported app/installer target and validate the ticket. A raw `.app` is not a submission archive, and a ZIP itself is not a stapling target.
3. Package the finalized app with a tool that preserves framework symlinks and permissions. For example, `ditto -c -k --sequesterRsrc --keepParent Example.app Example-1.2.3.zip`.
4. Hash that final archive, and generate any Sparkle signature against those same bytes. Verify the signature using the public key embedded in the distributed app. Feed build/short versions, URL and length must agree with the artifact.
5. Prepare the GitHub release as a draft, attach all required assets, verify their identities and then publish it. Preserve immutable tags and assets after publication.

A compiled release should expose its binary, checksum, cask metadata and optional appcast. A release manifest can additionally bind them to a source SHA and renderer/schema version. Machine decisions should use validated metadata, not an arbitrary substring of editable release notes.

If the project supports source-only publication, choose that mode explicitly before publishing. Publish source and local build instructions without binary assets, cask/feed changes, signing claims or promotion as the latest installable app. A later binary needs a new version when the earlier release is immutable. Do not silently turn missing signing credentials into source-only mode.

Publication and installation are separate gates: after release publication, verify downloaded public assets before advancing a Homebrew or update pointer. If that check fails, leave the previous install pointers intact and report the published-release/metadata split clearly.
