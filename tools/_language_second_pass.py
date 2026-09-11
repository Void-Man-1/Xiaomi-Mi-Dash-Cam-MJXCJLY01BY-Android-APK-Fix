from pathlib import Path


def replace(path: str, pairs: list[tuple[str, str]]) -> None:
    p = Path(path)
    if p.name == "README.md" or p.name.startswith("README."):
        raise SystemExit(f"README edit refused: {path}")
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"Expected text not found in {path}: {old!r}")
        text = text.replace(old, new)
    if text == original:
        raise SystemExit(f"No changes produced for {path}")
    p.write_text(text, encoding="utf-8")
    print(f"edited {path}")


replace("site/index.html", [
    ("Compatibility APK for the European Xiaomi Mi Dash Cam MJXCJLY01BY on current Android versions and HyperOS.", "Updated APK for the European Xiaomi Mi Dash Cam MJXCJLY01BY on current Android versions and HyperOS."),
    ("The recording list, thumbnails, downloads and playback were tested during physical-camera acceptance.", "The recording list, thumbnails, downloads and playback were tested with the camera."),
    ("Physical-camera acceptance test", "Full camera test"),
])

replace("site/pl/index.html", [
    ("Sprawdzono z fizyczną kamerą", "Przetestowano z prawdziwą kamerą"),
    ("Testy z fizyczną kamerą", "Test z prawdziwą kamerą"),
    ("fizyczną kamerą", "prawdziwą kamerą"),
    ("fizyczna kamera MJXCJLY01BY", "kamera MJXCJLY01BY"),
    ("Nie. To niezależny projekt zgodności dla aplikacji, której producent już nie rozwija.", "Nie. To niezależny projekt, który przywraca działanie aplikacji niewspieranej już przez producenta."),
    ("Nieoficjalny projekt zgodności dla modelu MJXCJLY01BY.", "Nieoficjalny projekt dla modelu MJXCJLY01BY."),
])

replace("site/uk/index.html", [
    ("фізичною камерою", "реальною камерою"),
    ("фізична камера MJXCJLY01BY", "камера MJXCJLY01BY"),
    ("фізичною камерою у версії EU", "реальною камерою версії EU"),
    ("Неофіційний проєкт сумісності, що дає змогу й надалі використовувати справне обладнання.", "Неофіційний проєкт для MJXCJLY01BY."),
])

replace("site/de/index.html", [
    ("Die Kompatibilität mit älteren Android-APIs und CPU-Architekturen wurde aktualisiert, sodass sich die APK unter Android 15 und 16 wieder normal installieren lässt.", "Die App wurde an aktuelle Android-Versionen und CPU-Architekturen angepasst. Dadurch lässt sich die APK unter Android 15 und 16 wieder normal installieren."),
    ("ARM64 und 16-KiB-Seitengröße werden unterstützt, älteres ARMv7 bleibt erhalten.", "Die App unterstützt ARM64 und 16-KiB-Speicherseiten; ARMv7 bleibt ebenfalls unterstützt."),
    ("Die Mi Dash Cam 1S ist ein anderes Gerät. Für sie wird keine Kompatibilität zugesichert.", "Die Mi Dash Cam 1S ist ein anderes Gerät. Dieses Projekt ist nicht für dieses Modell bestimmt."),
    ("Inoffizielles Kompatibilitätsprojekt für die MJXCJLY01BY.", "Inoffizielles Projekt für die MJXCJLY01BY."),
])

replace("site/ru/index.html", [
    ("физической камерой", "реальной камерой"),
    ("физическая камера MJXCJLY01BY", "камера MJXCJLY01BY"),
    ("Сетка записей, миниатюры, загрузка и воспроизведение прошли приёмочное тестирование.", "Список записей, миниатюры, загрузка и воспроизведение проверены с камерой."),
    ("Неофициальный проект совместимости для MJXCJLY01BY.", "Неофициальный проект для MJXCJLY01BY."),
])

replace("docs/GITHUB_LISTING.md", [
    ("Android compatibility fix for Xiaomi Mi Dash Cam MJXCJLY01BY EU. Tested on Android 8.1, 9 and 12–16; restores live preview, downloads and local use without a Mi account.", "Updated Android app for Xiaomi Mi Dash Cam MJXCJLY01BY EU. Restores live preview, downloads and local use without Mi login; tested on Android 8.1, 9 and 12–16."),
    ("Use the Xiaomi Mi Dash Cam MJXCJLY01BY on current Android versions.", "Use the Xiaomi Mi Dash Cam MJXCJLY01BY with current Android versions."),
])

print("LANGUAGE_SECOND_PASS_OK")
