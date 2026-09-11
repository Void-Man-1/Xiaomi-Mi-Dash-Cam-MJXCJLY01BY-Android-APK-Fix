from pathlib import Path


def apply(path: str, replacements: list[tuple[str, str]]) -> None:
    p = Path(path)
    if p.name == "README.md" or p.name.startswith("README."):
        raise SystemExit(f"README edit refused: {path}")
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        count = text.count(old)
        if count == 0:
            raise SystemExit(f"Expected text not found in {path}: {old[:120]!r}")
        text = text.replace(old, new)
    if text == original:
        raise SystemExit(f"No changes produced for {path}")
    p.write_text(text, encoding="utf-8")
    print(f"edited {path}")


apply("site/index.html", [
    ("Xiaomi Mi Dash Cam MJXCJLY01BY Android APK Fix — Android 15/16 &amp; HyperOS", "Xiaomi Mi Dash Cam MJXCJLY01BY — APK for Android 15/16 and HyperOS"),
    ("Working Xiaomi Mi Dash Cam MJXCJLY01BY EU APK for modern Android and HyperOS. Hardware-tested live preview, Wi-Fi, recordings, downloads and playback.", "Compatibility APK for the European Xiaomi Mi Dash Cam MJXCJLY01BY on current Android versions and HyperOS. Wi-Fi, live preview, recordings, downloads and playback were tested with a physical camera."),
    ("No. This is an independent preservation/compatibility project for abandoned companion software. Xiaomi, Mi, Mijia and 70mai names belong to their respective owners.", "No. This is an independent compatibility project for companion software that is no longer maintained. Xiaomi, Mi, Mijia and 70mai names belong to their respective owners."),
    ("Yes for the tested target. The exact 2.0.0 release completed a full physical-camera test on a Poco F6 running Android 16 / HyperOS 3.", "Yes, on the tested setup. Version 2.0.0 completed a full physical-camera test on a Poco F6 running Android 16 / HyperOS 3."),
    ("A SHA-256 checksum lets you confirm the APK you downloaded is exactly the artifact published by this repository. Android also requires APKs to be signed; this compatibility build is release-signed by the project, not by Xiaomi’s original key.", "A SHA-256 checksum lets you confirm that the APK you downloaded matches the file published by this project. Android also requires APKs to be signed; this build uses the project’s release key, not Xiaomi’s original key."),
    ("Hardware-tested compatibility release", "Tested with a physical MJXCJLY01BY camera"),
    ("Keep your <span class=\"accent\">Mi Dash Cam</span> working.", "Use your <span class=\"accent\">Mi Dash Cam</span> on current Android versions."),
    ("The original European app was abandoned years ago. This repaired APK brings the Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> back to modern Android — without requiring a Mi account.", "Xiaomi no longer maintains the original European app. This compatibility build restores local use of the Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> on current Android versions without requiring a Mi account."),
    ("Physical camera test passed", "Tested with the actual camera"),
    ("Local Wi-Fi · no cloud required", "Local Wi-Fi · no cloud service required"),
    ("Mi Dash Cam app verification screenshots", "Screenshots from Mi Dash Cam compatibility testing"),
    ("HyperOS 3 · real MJXCJLY01BY", "HyperOS 3 · physical MJXCJLY01BY camera"),
    ("Documented test coverage", "Tested versions documented"),
    ("Modern + legacy CPU support", "ARM64 and ARMv7 supported"),
    ("Verifiable release integrity", "Verify the downloaded file"),
    ("Check your camera first", "Check the model number"),
    ("One model. No guesswork.", "Confirm your camera before installing."),
    ("Xiaomi reused very similar product names. Match the model code printed on your camera before installing.", "Xiaomi used very similar names for different dashcams. Check the model code printed on the camera before installing."),
    ("This project targets the European/EU Mi Dash Cam and its old <code>com.banyac.mijia.app.eu</code> companion app.", "This project is for the European Mi Dash Cam <code>MJXCJLY01BY</code> and its original <code>com.banyac.mijia.app.eu</code> companion app."),
    ("What changed", "What this build fixes"),
    ("The old hardware is fine. The app was the problem.", "Compatibility fixes for current Android versions."),
    ("The repair focuses on the paths that actually broke on current phones instead of redesigning how the camera itself works.", "The changes are limited to functions that stopped working correctly on newer phones; they do not redesign the camera itself."),
    ("Installs on current Android", "Installs on Android 15 and 16"),
    ("Updates the abandoned API/architecture compatibility so normal installation works again on Android 15 and 16.", "Updates the app’s Android and CPU compatibility so it installs normally on Android 15 and 16."),
    ("Repairs the legacy stream path and uses RTSP over TCP. Visible live video was verified with the physical camera.", "Repairs the legacy streaming path and uses RTSP over TCP. Live video was verified with the physical camera."),
    ("No Mi account dependency", "Local use without a Mi account"),
    ("Starts with an Offline account for local phone-to-camera use instead of relying on the obsolete Xiaomi login flow.", "The app starts with an Offline account and works directly with the camera without the obsolete Xiaomi sign-in flow."),
    ("Recordings work again", "Recordings and downloads"),
    ("Recording grid, thumbnails, downloads and replay were exercised during acceptance testing.", "The recording list, thumbnails, downloads and playback were tested during physical-camera acceptance."),
    ("Modern CPU compatibility", "ARM64 and 16 KiB support"),
    ("Includes ARM64 and 16 KiB page-size compatibility while retaining older ARMv7 support.", "Adds ARM64 and 16 KiB page-size compatibility while retaining ARMv7 support for older devices."),
    ("Dead web help pages were replaced with bundled guidance and manuals so setup information stays available.", "Unavailable web help pages were replaced with bundled guidance and manuals that remain available offline."),
    ("Proof, not a compatibility claim made from an emulator.", "Tested with the actual camera."),
    ("The exact release APK was tested with the actual EU camera. Additional physical and emulator testing covers older Android versions with evidence boundaries documented in the repository.", "The published 2.0.0 APK was tested with the actual European camera. Other Android versions were tested separately, with the limits of that evidence documented in the repository."),
    ("Full physical-camera acceptance test video", "Physical-camera test video"),
    ("Full physical-camera acceptance test", "Physical-camera acceptance test"),
    ("Four steps from download to live view.", "Install in four steps."),
    ("The app talks directly to the dashcam over its Wi-Fi network. Mobile data is not used for camera transfer.", "The app communicates directly with the dashcam over its Wi-Fi network. Camera transfers do not use mobile data."),
    ("Use the canonical GitHub Release button on this page.", "Use the GitHub Release download button on this page."),
    ("Download the tested release", "Download version 2.0.0"),
    ("Version 2.0.0 is the current stable compatibility build. The SHA-256 below lets you verify that your downloaded file is byte-for-byte the published artifact.", "Version 2.0.0 is the current stable compatibility release. Use the SHA-256 below to verify that your download matches the published file."),
    ("Unofficial compatibility project for preserved hardware. Source, test evidence and integrity information are public in the GitHub repository.", "Unofficial compatibility project for the MJXCJLY01BY. Source code, test evidence and checksums are available in the GitHub repository."),
])

apply("site/pl/index.html", [
    ("Xiaomi Mi Dash Cam MJXCJLY01BY — poprawiony plik APK dla Androida 15/16 i HyperOS", "Xiaomi Mi Dash Cam MJXCJLY01BY — APK dla Androida 15/16 i HyperOS"),
    ("Działający plik APK dla Xiaomi Mi Dash Cam MJXCJLY01BY w wersji EU, przeznaczony dla nowych wersji Androida i HyperOS. Wi-Fi, podgląd na żywo, nagrania, pobieranie i odtwarzanie sprawdzono z prawdziwą kamerą.", "Zmodyfikowany APK dla europejskiej Xiaomi Mi Dash Cam MJXCJLY01BY (EU), przeznaczony do współczesnych wersji Androida i HyperOS. Połączenie Wi-Fi, podgląd na żywo, nagrania, pobieranie i odtwarzanie sprawdzono z fizyczną kamerą."),
    ("Nie. To niezależny projekt utrzymujący użyteczność porzuconego oprogramowania. Nazwy Xiaomi, Mi, Mijia i 70mai należą do ich właścicieli.", "Nie. To niezależny projekt zgodności dla aplikacji, której producent już nie rozwija. Nazwy Xiaomi, Mi, Mijia i 70mai należą do ich właścicieli."),
    ("Tak, w przetestowanej konfiguracji. Wersja 2.0.0 przeszła pełny test z fizyczną kamerą na Poco F6 z Androidem 16 i HyperOS 3.", "Tak, na przetestowanej konfiguracji. Wersja 2.0.0 przeszła pełny test z fizyczną kamerą na Poco F6 z Androidem 16 i HyperOS 3."),
    ("SHA-256 pozwala potwierdzić, że pobrany APK jest dokładnie plikiem opublikowanym w repozytorium. Android wymaga też podpisu APK; ta wersja jest podpisana kluczem projektu, a nie oryginalnym kluczem Xiaomi.", "SHA-256 pozwala sprawdzić, czy pobrany APK jest identyczny z plikiem opublikowanym przez projekt. Android wymaga również podpisu APK; ta wersja jest podpisana kluczem projektu, a nie oryginalnym kluczem Xiaomi."),
    ("Zgodność sprawdzona na prawdziwej kamerze", "Sprawdzono z fizyczną kamerą"),
    ("Przywróć <span class=\"accent\">Mi Dash Cam</span> do działania.", "Używaj <span class=\"accent\">Mi Dash Cam</span> na współczesnym Androidzie."),
    ("Oryginalna europejska aplikacja od lat nie jest już rozwijana. Ten poprawiony plik APK pozwala ponownie używać Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> z nowymi wersjami Androida — bez konieczności logowania się na konto Mi.", "Xiaomi nie rozwija już oryginalnej europejskiej aplikacji. Ta wersja przywraca lokalną obsługę Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> na współczesnych wersjach Androida bez logowania do konta Mi."),
    ("Przetestowano z fizyczną kamerą", "Testy z fizyczną kamerą"),
    ("Lokalne Wi-Fi · bez chmury", "Lokalne Wi-Fi · bez usług chmurowych"),
    ("Udokumentowany zakres testów", "Udokumentowane testy"),
    ("Nowe i starsze procesory", "Obsługa ARM64 i ARMv7"),
    ("Suma SHA-256 opublikowana", "SHA-256 opublikowany"),
    ("Możliwość weryfikacji pliku", "Sprawdź pobrany plik"),
    ("Najpierw sprawdź kamerę", "Sprawdź numer modelu"),
    ("Jeden model. Bez zgadywania.", "Przed instalacją upewnij się, że to właściwa kamera."),
    ("Xiaomi używało bardzo podobnych nazw dla różnych rejestratorów. Przed instalacją porównaj kod modelu z etykietą urządzenia.", "Xiaomi stosowało bardzo podobne nazwy dla różnych rejestratorów. Przed instalacją sprawdź kod modelu na obudowie kamery."),
    ("Co naprawiono", "Co naprawia ta wersja"),
    ("Sprzęt działa. Problemem była aplikacja.", "Poprawki dla współczesnych wersji Androida."),
    ("Zmiany skupiają się na funkcjach, które faktycznie przestały działać na nowych telefonach.", "Zmiany dotyczą funkcji, które przestały działać prawidłowo na nowszych telefonach."),
    ("Dostosowano aplikację do nowszych wersji Androida i współczesnych architektur procesora, dzięki czemu plik APK znów instaluje się normalnie na Androidzie 15 i 16.", "Dostosowano aplikację do nowszych wersji Androida i współczesnych architektur procesora, dzięki czemu APK instaluje się normalnie na Androidzie 15 i 16."),
    ("Bez zależności od konta Mi", "Lokalnie, bez konta Mi"),
    ("Aplikacja uruchamia się z kontem „Offline” i działa lokalnie, bez korzystania z przestarzałego mechanizmu logowania Xiaomi.", "Aplikacja uruchamia się z profilem „Offline” i działa lokalnie, bez przestarzałego mechanizmu logowania Xiaomi."),
    ("Nagr... (go/truncated-by-rlsnow)...