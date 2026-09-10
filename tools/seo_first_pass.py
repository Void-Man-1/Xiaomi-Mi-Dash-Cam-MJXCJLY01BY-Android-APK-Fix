from pathlib import Path

readme = Path("README.md")
text = readme.read_text(encoding="utf-8")

old_intro = """<p align=\"center\">\n  Restores the European Mi Dash Cam app on modern Android, including Poco F6 with Android 16 / HyperOS 3.\n</p>"""
new_intro = """<p align=\"center\">\n  Compatibility-fixed Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> EU APK for Android 8.1–16 and HyperOS.<br>\n  Restores installation, camera Wi-Fi connection, live preview, recordings, downloads, playback, and accountless local use on modern phones.\n</p>"""
if old_intro in text:
    text = text.replace(old_intro, new_intro, 1)

lang_marker = "<!-- discovery-language-links -->"
if lang_marker not in text:
    needle = new_intro + "\n"
    if needle in text:
        lang_block = """\n<!-- discovery-language-links -->
<p align="center">
  <a href="docs/README.ru.md">Русский</a> · <a href="docs/README.pl.md">Polski</a>
</p>
"""
        text = text.replace(needle, needle + lang_block, 1)

toc_needle = "- [Technical details](#technical-details) — exact changes, account behavior, native compatibility, verification, and release identity."
toc_add = "- [Common problems and FAQ](#common-problems-and-faq) — installation, Android 15/16, black preview, Wi-Fi, Poco F6, Mi account, and model compatibility.\n" + toc_needle
if toc_needle in text and "[Common problems and FAQ](#common-problems-and-faq)" not in text:
    text = text.replace(toc_needle, toc_add, 1)

common_marker = "## Common problems this fixes"
why_marker = "## Why I made it"
if common_marker not in text and why_marker in text:
    common = """## Common problems this fixes

This project is intended for owners of the **Xiaomi Mi Dash Cam `MJXCJLY01BY` European/EU model** whose original Mi Dash Cam app no longer works correctly on a newer Android phone. It addresses the common symptoms people encounter when trying to keep this camera usable:

- **Mi Dash Cam APK will not install on Android 15 or Android 16** because the original app targets an obsolete Android API level;
- **Mi Dash Cam connects to Wi-Fi but the app does not connect correctly** to the camera;
- **black or missing live preview** after connecting to the dashcam;
- crashes or freezes when opening camera, profile, help, manual, or settings screens;
- recordings or thumbnails not loading correctly, or downloaded recordings not replaying as expected;
- obsolete **Mi account / Xiaomi login** dependencies blocking normal local use;
- compatibility problems on modern **ARM64**, **16 KiB page-size**, **HyperOS**, and Android devices.

The final 2.0.0 release was hardware-tested with the European `MJXCJLY01BY` on a **Poco F6 running Android 16 / HyperOS 3**, including connection and reconnection, live preview, recording thumbnails, download, and playback. It is not a compatibility claim for the similarly named Mi Dash Cam 1S (`MJXCJLY02BY`).

"""
    text = text.replace(why_marker, common + why_marker, 1)

faq_marker = "## Common problems and FAQ"
tech_marker = "# Technical details"
if faq_marker not in text and tech_marker in text:
    faq = """## Common problems and FAQ

### Does Xiaomi Mi Dash Cam MJXCJLY01BY work on Android 16?

Yes, with this compatibility release. The exact release-signed 2.0.0 APK was fully tested with a European `MJXCJLY01BY` camera on a Poco F6 running Android 16 / HyperOS 3. Camera connection and reconnection, live preview, recording thumbnails, downloads, and playback passed the physical acceptance test.

### Where can I download a working Mi Dash Cam APK?

Use the **Download Latest APK** button at the top of this README. It links directly to the canonical signed APK attached to the latest supported GitHub release. For release identity and integrity information, verify the SHA-256 listed in `checksums/SHA256SUMS.txt`.

### Why will the original Mi Dash Cam APK not install on Android 15 or Android 16?

The final original European Mi Dash Cam app targets Android API 23. Android 15 introduced a minimum installable target SDK requirement that rejects apps targeting below API 24 during normal installation. This project raises the target while preserving the legacy camera functionality needed by `MJXCJLY01BY`.

### Why does Mi Dash Cam show a black live preview?

The legacy application and modern Android/network stacks do not always negotiate the camera's old RTSP/RTP-JPEG stream correctly. This release repairs the live-preview path and uses RTSP over TCP, which was verified during the physical camera test.

### Does the patched app require a Mi account or Xiaomi login?

No. Version 2.0.0 starts with an `Offline account` and is designed for local phone-to-camera use. The obsolete executable Mi-account login implementation was removed from the production build.

### Does this work on Poco F6 and HyperOS?

Yes. The final signed 2.0.0 release passed the complete physical-camera acceptance test on a Poco F6 running Android 16 / HyperOS 3. Other tested Android versions and the exact scope of each test are listed in the compatibility table above.

### Is MJXCJLY01BY the same camera as Mi Dash Cam 1S / MJXCJLY02BY?

No. `MJXCJLY01BY` is the supported European Mi Dash Cam model for this project. `MJXCJLY02BY` is the similarly named Mi Dash Cam 1S and is not claimed compatible.

### Will this fix every Xiaomi or 70mai dashcam?

No. This project deliberately targets the European Xiaomi Mi Dash Cam `MJXCJLY01BY`. It should not be treated as a universal Xiaomi, Mijia, or 70mai camera application.

"""
    text = text.replace(tech_marker, faq + tech_marker, 1)

readme.write_text(text, encoding="utf-8")

docs = Path("docs")
docs.mkdir(exist_ok=True)

ru = """# Xiaomi Mi Dash Cam MJXCJLY01BY — APK для Android 8.1–16

Это неофициальная версия приложения **Mi Dash Cam для европейской камеры Xiaomi `MJXCJLY01BY`**, исправленная для современных версий Android и HyperOS.

Проект предназначен для случаев, когда старое приложение Mi Dash Cam не устанавливается на Android 15/16, не подключается к камере по Wi-Fi, показывает чёрный экран вместо live preview, зависает, не загружает записи или требует устаревший Mi Account.

Версия 2.0.0 работает локально без Mi Account. Финальный подписанный APK был полностью проверен с реальной камерой `MJXCJLY01BY` на **Poco F6 с Android 16 / HyperOS 3**: подключение и повторное подключение, live preview, список и миниатюры записей, скачивание и воспроизведение прошли проверку.

## Скачать

Актуальный APK находится в основном README репозитория: **[перейти к загрузке](../README.md)**.

Поддерживаемая модель: **Xiaomi Mi Dash Cam `MJXCJLY01BY`, EU / European region**.

**Mi Dash Cam 1S `MJXCJLY02BY` — другая камера и этим проектом не поддерживается.**

Полная информация о совместимости, SHA-256, тестировании, технических исправлениях и ограничениях находится в [основном README](../README.md).
"""

pl = """# Xiaomi Mi Dash Cam MJXCJLY01BY — APK dla Android 8.1–16

To nieoficjalna, poprawiona wersja aplikacji **Mi Dash Cam dla europejskiej kamery Xiaomi `MJXCJLY01BY`**, przystosowana do współczesnych wersji Androida i HyperOS.

Projekt jest przeznaczony dla sytuacji, w których stara aplikacja Mi Dash Cam nie instaluje się na Androidzie 15/16, nie łączy się prawidłowo z kamerą przez Wi-Fi, pokazuje czarny ekran zamiast podglądu na żywo, zawiesza się, nie pobiera nagrań albo wymaga przestarzałego konta Mi.

Wersja 2.0.0 działa lokalnie bez konta Mi. Finalny podpisany APK został w pełni sprawdzony z fizyczną kamerą `MJXCJLY01BY` na **Poco F6 z Androidem 16 / HyperOS 3**: połączenie i ponowne połączenie, podgląd na żywo, lista i miniatury nagrań, pobieranie oraz odtwarzanie przeszły testy.

## Pobieranie

Aktualny APK znajduje się w głównym README repozytorium: **[przejdź do pobierania](../README.md)**.

Obsługiwany model: **Xiaomi Mi Dash Cam `MJXCJLY01BY`, EU / region europejski**.

**Mi Dash Cam 1S `MJXCJLY02BY` to inna kamera i nie jest obsługiwana przez ten projekt.**

Pełne informacje o kompatybilności, SHA-256, testach, poprawkach technicznych i ograniczeniach znajdują się w [głównym README](../README.md).
"""

(docs / "README.ru.md").write_text(ru, encoding="utf-8")
(docs / "README.pl.md").write_text(pl, encoding="utf-8")
