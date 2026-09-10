# Xiaomi Mi Dash Cam MJXCJLY01BY troubleshooting

This page is for the **Xiaomi Mi Dash Cam `MJXCJLY01BY` European / EU model** when the original Mi Dash Cam Android app no longer installs, connects incorrectly, shows a black preview, freezes, or cannot be used normally on a modern phone.

> This project does **not** claim compatibility with the similarly named Mi Dash Cam 1S (`MJXCJLY02BY`) or every Xiaomi / 70mai dashcam.

## Quick diagnosis

| Symptom | What is usually happening | Status in this project |
|---|---|---|
| Original Mi Dash Cam APK will not install on Android 15 or 16 | The old EU app targets Android API 23; normal Android 15+ installation rejects apps targeting below API 24 | Addressed in the compatibility release |
| Phone joins the dashcam Wi-Fi but the app does not connect correctly | The legacy camera-control flow can leave stale requests or long retries active | Reconnection path hardened in 2.0.0 |
| Live preview is black or never starts | The old RTSP/RTP-JPEG path does not behave reliably on modern Android/network stacks | Live-preview path repaired; RTSP over TCP used |
| App freezes or becomes unresponsive while connecting or reconnecting | Legacy media teardown and retry behavior could block or overlap work | Blocking restart loop removed and VLC stop handling hardened |
| Mi account / Xiaomi login blocks use | The original application depended on obsolete account services | Production 2.0.0 uses an accountless local profile |
| Help, FAQ, installation or manual pages fail | Original online help endpoints are no longer dependable | Replaced with bundled offline help/manual content |
| Recordings, thumbnails, downloads or replay fail | Legacy media and storage behavior needed compatibility work | These paths were repaired and included in physical-camera acceptance testing |
| Modern ARM64 / 16 KiB page-size device compatibility is a problem | Original native libraries were built for much older Android/CPU assumptions | ARM64 and 16 KiB compatibility were added while retaining ARMv7 |

## Mi Dash Cam APK will not install on Android 15 or Android 16

The final original European Mi Dash Cam app targets Android API 23. Android 15 introduced a minimum installable target-SDK requirement that rejects apps targeting below API 24 during normal installation. The compatibility release raises the target while preserving the legacy local camera functionality required by `MJXCJLY01BY`.

Use the canonical signed APK from this repository's [latest release](https://github.com/Void-Man-1/Mi-Dash-cam-Android-8.1-16-fix-MJXCJLY01BY/releases/latest), not a debug or differently signed copy.

## Mi Dash Cam connects to Wi-Fi but the app does not connect

The camera uses a direct local Wi-Fi connection. Android may warn that the dashcam network has no internet and may try to switch back to mobile data or another Wi-Fi network. Keep the phone connected to the camera network while using the app.

Version 2.0.0 also hardens repeated connection attempts by cancelling stale camera-screen requests and removing long hidden retries from the fast control requests used while connecting.

## Mi Dash Cam black screen / black live preview

A black live-preview area was one of the reproduced failures in the abandoned app. The compatibility release repairs the live-preview path and uses RTSP over TCP for the camera's RTP/JPEG stream.

The final signed 2.0.0 APK was tested with a real European `MJXCJLY01BY` on a Poco F6 running Android 16 / HyperOS 3, including a visible live preview.

## Mi Dash Cam freezes when connecting again

The old application could leave work running while a new connection sequence started, and media teardown could block Android's main thread. Version 2.0.0 cancels stale tagged camera requests, bounds the fast control requests, removes the repeated blocking preview restart loop, and includes the asynchronous VLC stop fix used to prevent teardown hangs.

Physical testing included camera connection and reconnection on the Poco F6 / Android 16 setup.

## Mi Dash Cam Mi Account or Xiaomi login no longer works

The patched application does not require a Mi account for normal local camera use. Version 2.0.0 starts with an `Offline account` and removes the obsolete executable Mi-account login implementation from the production APK.

The camera itself still communicates with the phone over its local Wi-Fi network.

## Mi Dash Cam recordings or downloads do not work

The compatibility release preserves and repairs the local recording-list, thumbnail, download and playback paths. The final physical-camera acceptance test covered the recording grid and thumbnails, completed downloads, and replay.

## Does it work on Poco F6 / HyperOS 3 / Android 16?

Yes for the exact tested configuration documented by this project. The final release-signed 2.0.0 APK passed full physical-camera acceptance with a European `MJXCJLY01BY` on a **Poco F6 running Android 16 / HyperOS 3**.

See the main [README](../README.md) for the complete Android compatibility table and the evidence boundaries for Android 8.1 through 16.

## Is MJXCJLY01BY the same as Mi Dash Cam 1S / MJXCJLY02BY?

No. `MJXCJLY01BY` is the Xiaomi Mi Dash Cam model supported by this repository. Xiaomi identifies `MJXCJLY02BY` as the Mi Dash Cam 1S; it is a different model.

Xiaomi's original specification page identifies `MJXCJLY01BY` and its Wi-Fi / 1080p hardware details: https://www.mi.com/mj-carcorder/specs

## Download and verification

Download the current canonical release from the [GitHub Releases page](https://github.com/Void-Man-1/Mi-Dash-cam-Android-8.1-16-fix-MJXCJLY01BY/releases/latest). Verify the release SHA-256 against [`checksums/SHA256SUMS.txt`](../checksums/SHA256SUMS.txt) before installing if you want to confirm file integrity.

For the full technical explanation, compatibility matrix, test evidence and patch details, return to the [main README](../README.md).
