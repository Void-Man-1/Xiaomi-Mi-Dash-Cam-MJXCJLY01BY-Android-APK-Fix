# Uniform Project Naming Migration Design

## Goal

Standardize the public project identity around the official product/model name while removing `EU` and Android-version-range clutter from branding and release filenames.

## Canonical naming

- Repository: `Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix`
- Display/project title: `Xiaomi Mi Dash Cam MJXCJLY01BY Android APK Fix`
- Product name: `Mi Dash Cam`
- Current release title: `Mi Dash Cam 2.0.0`
- Current release APK: `Mi-Dash-Cam-2.0.0.apk`
- Future release APK pattern: `Mi-Dash-Cam-<version>.apk`
- Future GitHub Pages root: `https://void-man-1.github.io/Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix/`

## Accuracy constraints

`EU` is removed from branding, filenames, release title, social copy, and generic project naming. It is retained only where it communicates a real compatibility boundary: the tested European app variant, the Android package `com.banyac.mijia.app.eu`, and warnings distinguishing supported `MJXCJLY01BY` from unsupported `MJXCJLY02BY`/other variants.

The APK binary is not rebuilt or resigned. Renaming the release asset must preserve its SHA-256 `2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887` and release signing lineage.

## Migration sequence

1. Add a repository-wide naming validator and prove the current tree fails it for expected legacy branding/filenames.
2. Update source-kit output naming, README, localized docs, release documentation, checksum filename reference, Pages EN/RU/PL pages, structured data, crawler files, and release-sync automation.
3. Rename the existing GitHub release asset in place to `Mi-Dash-Cam-2.0.0.apk` and update the `v2.0.0` release title/body without changing binary content.
4. Verify the new asset name, SHA-256 digest, release links, repository text, and site-language pages.
5. Rename the GitHub repository manually to `Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix` because the installed connector does not expose repository-administration mutations.
6. After the manual rename, update all GitHub Pages canonical/hreflang/Open Graph/sitemap/robots/repository URLs to the new path, redeploy Pages, and verify the live EN/RU/PL site.

## URL behavior

Normal GitHub repository/release URLs are expected to redirect after a GitHub repository rename. GitHub Pages project-site URLs do not receive the same automatic redirect, so Pages URL migration is an explicit post-rename task.

## Automation

The release-sync workflow must stop selecting an arbitrary first APK. It must identify the canonical current asset using the `Mi-Dash-Cam-<version>.apk` pattern and propagate that exact filename/URL/version to README, Russian and Polish docs, and all three Pages languages.

Contributor build outputs use the same project stem, with only build-state suffixes added when technically necessary, for example `Mi-Dash-Cam-2.0.0-unsigned.apk`, `Mi-Dash-Cam-2.0.0-local-signed.apk`, or `Mi-Dash-Cam-2.0.0-partial-development-unsigned.apk`.

## Success criteria

The migration is complete when the canonical release asset is `Mi-Dash-Cam-2.0.0.apk`, its digest is unchanged, no public branding still calls the release/project `EU`, future build/release automation emits the new naming pattern, EN/RU/PL pages are internally consistent, and after the manual repository rename the live Pages URLs and metadata use the new repository slug.