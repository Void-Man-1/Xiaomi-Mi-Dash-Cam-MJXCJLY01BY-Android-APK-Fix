from _language_edit_helpers import apply

apply(".github/ISSUE_TEMPLATE/bug_report.yml", [
    ("description: Report a problem with the MJXCJLY01BY EU patch on a specific Android device", "description: Report a problem with version 2.0.0 on a specific Android device"),
    ("label: Camera confirmation", "label: Confirm the camera model"),
    ("label: Steps to reproduce from a cold start", "label: Steps to reproduce"),
    ("description: Include the exact navigation sequence and whether the phone was joined to camera Wi-Fi.", "description: Start from a fresh app launch. Include the exact steps and say whether the phone was connected to the camera's Wi-Fi."),
    ("label: Function results", "label: What did you test?"),
    ("label: Redacted screenshots or logs", "label: Screenshots or logs (redacted)"),
    ("description: Never post credentials, access tokens, Wi-Fi passwords, signing keys, or unredacted packet captures.", "description: Remove credentials, access tokens, Wi-Fi passwords, signing keys, device identifiers, and other private data before posting."),
])

apply("docs/GITHUB_LISTING.md", [
    ("Mi Dash cam Android 8.1-16 fix for Xiaomi MJXCJLY01BY EU: Poco F6/HyperOS 3, live preview, downloads, offline account, ARM64/16K, and manuals.", "Android compatibility fix for Xiaomi Mi Dash Cam MJXCJLY01BY EU. Tested on Android 8.1, 9 and 12–16; restores live preview, downloads and local use without a Mi account."),
    ("Keep the Xiaomi Mi Dash Cam MJXCJLY01BY working on modern Android. Version 2.0.0 provides accountless startup, ARM64/16 KiB support, repaired help/manuals, RTSP/TCP live preview, and reconnect hardening. Full physical-camera operation passed on a Poco F6 running Android 16 / HyperOS 3.", "Use the Xiaomi Mi Dash Cam MJXCJLY01BY on current Android versions. Version 2.0.0 restores local use without a Mi account, live preview, downloads and playback, adds ARM64/16 KiB support, and improves reconnection. The full physical-camera test used a Poco F6 running Android 16 / HyperOS 3."),
    ("The exact release-signed 2.0.0 APK passed the publishing acceptance checks with the EU `MJXCJLY01BY` on a Poco F6. Its full physical test covered connection and reconnection, live preview, the recording grid and thumbnails, completed downloads, and recording replay.", "The published 2.0.0 APK passed the release checks and the physical-camera test with an EU `MJXCJLY01BY` on a Poco F6. The test covered connection and reconnection, live preview, the recording grid and thumbnails, completed downloads, and recording playback."),
])

apply("docs/RELEASE_NOTES_2.0.0.md", [
    ("Release status: final, exact release-signed APK verified and physically hardware accepted.", "Release status: final. The published APK passed static verification and the documented physical-camera acceptance test."),
    ("Compatibility work restored operation on modern Android, but version 2.0.0 is a larger generational change: the old cloud-account-gated application now starts as a local accountless tool, its executable Mi-account implementation is removed, and the camera reconnection path is hardened.", "Compatibility work restored operation on current Android versions, but 2.0.0 also changes how the app starts and reconnects: it now opens in a local accountless mode, the executable Mi-account implementation is removed, and camera reconnection is more robust."),
    ("Version 2.0.0 addresses that recurrent-connection path by:", "Version 2.0.0 addresses that reconnection path by:"),
    ("These changes bound failed control requests and prevent stale work from overlapping a new connection attempt.", "These changes limit how long failed control requests can linger and prevent stale work from overlapping a new connection attempt."),
    ("The final 2.0.0 APK passed:", "The published 2.0.0 APK passed:"),
])

apply("docs/TROUBLESHOOTING.md", [
    ("when the original Mi Dash Cam Android app no longer installs, connects incorrectly, shows a black preview, freezes, or cannot be used normally on a modern phone.", "when the original Mi Dash Cam Android app no longer installs, fails to connect, shows a black preview, freezes, or otherwise no longer works correctly on a current phone."),
    ("Production 2.0.0 uses an accountless local profile", "Version 2.0.0 uses an accountless local profile"),
    ("Use the canonical signed APK from this repository's [latest release]", "Use the signed APK published in this repository's [latest release]"),
    ("The final signed 2.0.0 APK was tested with a real European `MJXCJLY01BY` on a Poco F6 running Android 16 / HyperOS 3, including a visible live preview.", "The published 2.0.0 APK was tested with a physical European `MJXCJLY01BY` on a Poco F6 running Android 16 / HyperOS 3, including a visible live preview."),
    ("Yes for the exact tested configuration documented by this project. The final release-signed 2.0.0 APK passed full physical-camera acceptance with a European `MJXCJLY01BY` on a **Poco F6 running Android 16 / HyperOS 3**.", "Yes, for the documented test setup. The published 2.0.0 APK completed the full physical-camera test with a European `MJXCJLY01BY` on a **Poco F6 running Android 16 / HyperOS 3**."),
    ("See the main [README](../README.md) for the complete Android compatibility table and the evidence boundaries for Android 8.1 through 16.", "See the main [README](../README.md) for the compatibility table and the evidence boundaries for Android 8.1, 9 and 12–16."),
    ("Download the current canonical release from the [GitHub Releases page]", "Download the current release from the [GitHub Releases page]"),
])

apply("docs/AUDIT_2026-09-11.md", [
    ("Status: complete. Audit remediation, production deployment verification, release-integrity re-check, GitHub Actions runtime maintenance, and stale-branch cleanup all finished successfully.", "Status: complete. The fixes, production deployment checks, release-integrity re-check, GitHub Actions maintenance, and stale-branch cleanup are finished."),
    ("No defect was found in the immutable release artifact itself. The audit identified repository, automation, documentation, and presentation maintenance defects; those confirmed findings were corrected and then re-verified from merged `main` and the deployed GitHub Pages site.", "No defect was found in the immutable release artifact itself. The audit found maintenance issues in the repository, automation, documentation and public presentation. Those confirmed issues were fixed and then re-verified from merged `main` and the deployed GitHub Pages site."),
])

apply("CONTRIBUTING.md", [
    ("The goal is to keep compatibility fixes reviewable, reproducible, and safe without turning the repository into a redistribution point for proprietary Xiaomi/70mai code or user/device data.", "The goal is to keep compatibility fixes reviewable, reproducible and safe without using the repository to redistribute proprietary Xiaomi/70mai code or private user/device data."),
])

apply("source-kit/docs/BUILD_FROM_ORIGINAL.md", [
    ("Preparation is intentionally fail-closed. If the input checksum, package identity, or expected patch anchors do not match, stop and investigate rather than forcing the patch onto a different application.", "Preparation is deliberately fail-closed. If the input checksum, package identity or expected patch anchors do not match, stop and investigate instead of forcing the patch onto a different application."),
])
