#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PAGES = {
    "en": SITE / "index.html",
    "pl": SITE / "pl" / "index.html",
    "uk": SITE / "uk" / "index.html",
    "de": SITE / "de" / "index.html",
    "ru": SITE / "ru" / "index.html",
}
ORDER = ("en", "pl", "uk", "de", "ru")
FLAG_LANGS = {"en", "pl", "uk", "de"}

class Parser(HTMLParser):
    pass

def required_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: expected text not found: {old!r}")
    return text.replace(old, new)

def normalize_language_nav(path: Path, text: str) -> str:
    match = re.search(r'(<nav class="langs"[^>]*>)(.*?)(</nav>)', text, re.S)
    if not match:
        raise RuntimeError(f"{path}: language nav not found")
    inner = match.group(2)
    link_re = re.compile(
        r'<a\b(?=[^>]*\bclass="[^"]*\blang\b[^"]*")(?=[^>]*\bhreflang="(en|pl|uk|de|ru)")[^>]*>.*?</a>',
        re.S,
    )
    links = {}
    for m in link_re.finditer(inner):
        lang = m.group(1)
        link = m.group(0)
        link = re.sub(r'<span class="flag"[^>]*>.*?</span>', '', link, flags=re.S)
        link = re.sub(r'<img class="flag-img"[^>]*>', '', link)
        label_m = re.search(r'<span class="label">(.*?)</span>', link, re.S)
        if not label_m:
            raise RuntimeError(f"{path}: missing label for {lang}")
        if lang in FLAG_LANGS:
            prefix = "" if path == SITE / "index.html" else "../"
            flag = (
                f'<img class="flag-img" src="{prefix}flags/{lang}.svg" '
                f'width="18" height="12" alt="" aria-hidden="true">'
            )
            link = link.replace("</a>", flag + "</a>")
        links[lang] = link
    missing = [lang for lang in ORDER if lang not in links]
    if missing:
        raise RuntimeError(f"{path}: missing language links {missing}")
    rebuilt = "".join(links[lang] for lang in ORDER)
    return text[:match.start(2)] + rebuilt + text[match.end(2):]

COPY_REPLACEMENTS = {
    "pl": [
        ("Xiaomi Mi Dash Cam MJXCJLY01BY — poprawiony APK dla Android 15/16 i HyperOS",
         "Xiaomi Mi Dash Cam MJXCJLY01BY — poprawiony plik APK dla Androida 15/16 i HyperOS"),
        ("Działający APK Xiaomi Mi Dash Cam MJXCJLY01BY EU dla nowych wersji Androida i HyperOS. Wi-Fi, podgląd, nagrania, pobieranie i odtwarzanie sprawdzone z prawdziwą kamerą.",
         "Działający plik APK dla Xiaomi Mi Dash Cam MJXCJLY01BY w wersji EU, przeznaczony dla nowych wersji Androida i HyperOS. Wi-Fi, podgląd na żywo, nagrania, pobieranie i odtwarzanie sprawdzono z prawdziwą kamerą."),
        ("Xiaomi Mi Dash Cam MJXCJLY01BY European/EU model",
         "Xiaomi Mi Dash Cam MJXCJLY01BY — europejska wersja (EU)"),
        ("Tak w przetestowanej konfiguracji. Dokładny APK 2.0.0 przeszedł pełny test z fizyczną kamerą na Poco F6 z Androidem 16 / HyperOS 3.",
         "Tak, w przetestowanej konfiguracji. Wersja 2.0.0 przeszła pełny test z fizyczną kamerą na Poco F6 z Androidem 16 i HyperOS 3."),
        ("Android 10–11 nie są obecnie oznaczone jako przetestowane.",
         "Android 10 i 11 nie są obecnie deklarowane jako przetestowane."),
        ("Oryginalna europejska aplikacja została porzucona lata temu. Ten naprawiony APK ponownie obsługuje Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> na współczesnym Androidzie — bez wymaganego konta Mi.",
         "Oryginalna europejska aplikacja nie jest wspierana od lat. Ten poprawiony plik APK pozwala ponownie używać Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> z nowymi wersjami Androida — bez konieczności logowania się na konto Mi."),
        ("Kod źródłowy na GitHub</a>", "Kod źródłowy na GitHubie</a>"),
        ("Test z fizyczną kamerą zaliczony", "Przetestowano z fizyczną kamerą"),
        ("HyperOS 3 · prawdziwa MJXCJLY01BY", "HyperOS 3 · fizyczna kamera MJXCJLY01BY"),
        ("<strong>SHA-256 opublikowany</strong><span>Weryfikowalna integralność wydania</span>",
         "<strong>Suma SHA-256 opublikowana</strong><span>Możliwość weryfikacji pliku</span>"),
        ("europejskiej/EU Mi Dash Cam", "europejskiej wersji Mi Dash Cam (EU)"),
        ("Naprawiona zgodność starego API i architektur pozwala ponownie instalować APK normalnie na Androidzie 15 i 16.",
         "Zaktualizowano zgodność ze starszym API i architekturami procesora, dzięki czemu plik APK znów instaluje się normalnie na Androidzie 15 i 16."),
        ("Naprawiono starszą ścieżkę streamingu i użyto RTSP przez TCP. Obraz sprawdzono z fizyczną kamerą.",
         "Naprawiono obsługę strumienia wideo i użyto RTSP przez TCP. Podgląd na żywo sprawdzono z fizyczną kamerą."),
        ("Aplikacja uruchamia się z kontem Offline i działa lokalnie bez starego mechanizmu logowania Xiaomi.",
         "Aplikacja uruchamia się z kontem „Offline” i działa lokalnie, bez zależności od przestarzałego logowania Xiaomi."),
        ("Dodano ARM64 i zgodność z 16 KiB page size, zachowując starsze ARMv7.",
         "Dodano obsługę ARM64 i stron pamięci o rozmiarze 16 KiB, zachowując wsparcie dla starszego ARMv7."),
        ("Dowody zamiast deklaracji z emulatora.", "Dowody zamiast deklaracji opartych wyłącznie na emulatorze."),
        ("Dokładnie ten wydany APK przetestowano z prawdziwą kamerą EU. Testy innych wersji Androida i ich ograniczenia są opisane w repozytorium.",
         "Ten sam plik APK z wydania przetestowano z prawdziwą kamerą w wersji EU. Testy innych wersji Androida i ich ograniczenia opisano w repozytorium."),
        ("Użyj kanonicznego przycisku GitHub Release na tej stronie.",
         "Użyj przycisku pobierania z wydania na GitHubie."),
        ("Kod źródłowy, dowody testów i dane integralności są publiczne na GitHub.",
         "Kod źródłowy, wyniki testów i sumy kontrolne są publiczne na GitHubie."),
        ('aria-label="Mi Dash Cam app verification screenshots"',
         'aria-label="Zrzuty ekranu potwierdzające działanie aplikacji Mi Dash Cam"'),
        ('alt="Mi Dash Cam 2.0.0 running on Poco F6"', 'alt="Mi Dash Cam 2.0.0 działająca na Poco F6"'),
        ('alt="Mi Dash Cam release app on Poco F6"', 'alt="Mi Dash Cam 2.0.0 na Poco F6"'),
        ('alt="Offline account screen"', 'alt="Ekran konta Offline"'),
        ('alt="Add camera screen"', 'alt="Ekran dodawania kamery"'),
    ],
    "ru": [
        ("Рабочий APK Xiaomi Mi Dash Cam MJXCJLY01BY EU для современных Android и HyperOS. Проверены Wi-Fi, превью, записи, загрузка и воспроизведение на реальной камере.",
         "Рабочий APK для европейской Xiaomi Mi Dash Cam MJXCJLY01BY (EU) на современных версиях Android и HyperOS. На реальной камере проверены Wi-Fi, предпросмотр в реальном времени, записи, скачивание и воспроизведение."),
        ("Xiaomi Mi Dash Cam MJXCJLY01BY European/EU model",
         "Xiaomi Mi Dash Cam MJXCJLY01BY — европейская версия (EU)"),
        ("Да для проверенной конфигурации. Точный релиз 2.0.0 прошёл полный тест с реальной камерой на Poco F6 с Android 16 / HyperOS 3.",
         "Да, для проверенной конфигурации. Именно версия 2.0.0 прошла полный тест с реальной камерой на Poco F6 с Android 16 и HyperOS 3."),
        ("Оригинальное европейское приложение давно заброшено. Этот исправленный APK снова делает Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> пригодной для современных Android — без обязательного Mi-аккаунта.",
         "Оригинальное европейское приложение давно не поддерживается. Этот исправленный APK снова позволяет использовать Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> с современными версиями Android — без обязательного входа в Mi-аккаунт."),
        ("Тест с реальной камерой пройден", "Проверено с реальной камерой"),
        ("HyperOS 3 · реальная MJXCJLY01BY", "HyperOS 3 · физическая камера MJXCJLY01BY"),
        ("<strong>ARM64 + ARMv7</strong><span>Современные и старые CPU</span>",
         "<strong>ARM64 + ARMv7</strong><span>Современные и старые процессоры</span>"),
        ("европейской/EU Mi Dash Cam", "европейской версии Mi Dash Cam (EU)"),
        ("Исправлена совместимость старого API и архитектур, поэтому APK снова устанавливается обычным способом на Android 15 и 16.",
         "Обновлена совместимость со старыми Android API и архитектурами процессора, поэтому APK снова нормально устанавливается на Android 15 и 16."),
        ("<h3>Рабочее живое видео</h3>", "<h3>Предпросмотр в реальном времени</h3>"),
        ("Исправлен старый путь видеопотока и включён RTSP через TCP. Превью подтверждено на физической камере.",
         "Исправлена работа видеопотока и включён RTSP через TCP. Предпросмотр подтверждён на физической камере."),
        ("<h3>Без зависимости от Mi Account</h3>", "<h3>Без зависимости от Mi-аккаунта</h3>"),
        ("Приложение запускается с Offline account и работает локально, не полагаясь на устаревший вход Xiaomi.",
         "Приложение запускается с профилем «Offline» и работает локально, не завися от устаревшей авторизации Xiaomi."),
        ("Добавлена совместимость ARM64 и 16 KiB page size, при этом сохранена поддержка старого ARMv7.",
         "Добавлена поддержка ARM64 и страниц памяти размером 16 КиБ, при этом сохранена поддержка старого ARMv7."),
        ("Не просто обещание на основе эмулятора.", "Реальные доказательства, а не выводы только по эмулятору."),
        ("Именно релизный APK проверен с настоящей EU-камерой. Для других версий Android отдельно задокументированы физические и эмуляторные тесты.",
         "Опубликованный APK протестирован с настоящей камерой EU. Физические и эмуляторные тесты для других версий Android отдельно задокументированы в репозитории."),
        ("<strong>Offline account</strong><span>Локально, без Mi-логина</span>",
         "<strong>Профиль Offline</strong><span>Локально, без входа в Mi-аккаунт</span>"),
        ("<strong>Добавление камеры</strong><span>Путь интерфейса на новом Android</span>",
         "<strong>Добавление камеры</strong><span>Экран добавления камеры на современном Android</span>"),
        ("Открыть доказательства →", "Открыть материалы теста →"),
        ("Четыре шага до живого изображения.", "Четыре шага до просмотра в реальном времени."),
        ("Используйте каноническую ссылку GitHub Release на этой странице.",
         "Скачайте APK по ссылке из раздела GitHub Releases на этой странице."),
        ("Неофициальный проект совместимости для сохранения рабочей техники. Исходный код, тесты и данные целостности опубликованы на GitHub.",
         "Неофициальный проект совместимости, позволяющий продолжать использовать исправное оборудование. Исходный код, результаты тестов и контрольные суммы опубликованы на GitHub."),
        ('aria-label="Mi Dash Cam app verification screenshots"',
         'aria-label="Скриншоты, подтверждающие работу приложения Mi Dash Cam"'),
        ('alt="Mi Dash Cam 2.0.0 running on Poco F6"', 'alt="Mi Dash Cam 2.0.0 на Poco F6"'),
        ('alt="Mi Dash Cam release app on Poco F6"', 'alt="Релиз Mi Dash Cam 2.0.0 на Poco F6"'),
        ('alt="Offline account screen"', 'alt="Экран профиля Offline"'),
        ('alt="Add camera screen"', 'alt="Экран добавления камеры"'),
    ],
    "uk": [
        ("Xiaomi Mi Dash Cam MJXCJLY01BY — виправлений APK для Android 15/16 та HyperOS",
         "Xiaomi Mi Dash Cam MJXCJLY01BY — виправлений APK-файл для Android 15/16 і HyperOS"),
        ("Робочий APK Xiaomi Mi Dash Cam MJXCJLY01BY EU для сучасного Android і HyperOS. Wi-Fi, відео, записи, завантаження та відтворення перевірені з реальною камерою.",
         "Робочий APK-файл для європейської Xiaomi Mi Dash Cam MJXCJLY01BY (EU) на сучасних версіях Android і HyperOS. На реальній камері перевірено Wi-Fi, перегляд у реальному часі, записи, завантаження та відтворення."),
        ("Xiaomi Mi Dash Cam MJXCJLY01BY European/EU model",
         "Xiaomi Mi Dash Cam MJXCJLY01BY — європейська версія (EU)"),
        ("Так у перевіреній конфігурації. Точний реліз 2.0.0 пройшов повний тест із фізичною камерою на Poco F6 з Android 16 / HyperOS 3.",
         "Так, у перевіреній конфігурації. Саме версія 2.0.0 пройшла повний тест із фізичною камерою на Poco F6 з Android 16 і HyperOS 3."),
        ("Оригінальний європейський застосунок покинули багато років тому. Цей виправлений APK знову робить Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> придатною для сучасного Android — без обов’язкового Mi-акаунта.",
         "Підтримку оригінального європейського застосунку припинили багато років тому. Цей виправлений APK-файл знову дає змогу використовувати Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> із сучасними версіями Android — без обов’язкового облікового запису Mi."),
        ("Тест із фізичною камерою пройдено", "Перевірено з фізичною камерою"),
        ("HyperOS 3 · реальна MJXCJLY01BY", "HyperOS 3 · фізична камера MJXCJLY01BY"),
        ("<strong>ARM64 + ARMv7</strong><span>Сучасні та старі CPU</span>",
         "<strong>ARM64 + ARMv7</strong><span>Сучасні та старі процесори</span>"),
        ("європейської/EU Mi Dash Cam", "європейської версії Mi Dash Cam (EU)"),
        ("<h3>Установлення на нових Android</h3>", "<h3>Встановлення на нових версіях Android</h3>"),
        ("Оновлено сумісність старого API та архітектур, тому APK знову нормально встановлюється на Android 15 і 16.",
         "Оновлено сумісність зі старими Android API та архітектурами процесора, тому APK-файл знову нормально встановлюється на Android 15 і 16."),
        ("<h3>Відновлене живе відео</h3>", "<h3>Перегляд у реальному часі відновлено</h3>"),
        ("Виправлено старий шлях відеопотоку та використано RTSP через TCP. Видиме прев’ю перевірене з фізичною камерою.",
         "Виправлено роботу відеопотоку та використано RTSP через TCP. Перегляд у реальному часі перевірено з фізичною камерою."),
        ("<h3>Без залежності від Mi Account</h3>", "<h3>Без залежності від облікового запису Mi</h3>"),
        ("Застосунок стартує з Offline account і працює локально без застарілого входу Xiaomi.",
         "Застосунок запускається з профілем «Offline» і працює локально без застарілої авторизації Xiaomi."),
        ("Додано ARM64 та сумісність із 16 KiB page size зі збереженням ARMv7.",
         "Додано підтримку ARM64 і сторінок пам’яті розміром 16 КіБ, збережено підтримку ARMv7."),
        ("Не просто заява на основі емулятора.", "Реальні докази, а не висновки лише з емулятора."),
        ("Саме релізний APK перевірено з реальною EU-камерою. Межі тестування інших версій Android описані в репозиторії.",
         "Опублікований APK-файл протестовано з реальною камерою EU. Результати й обмеження тестування інших версій Android описано в репозиторії."),
        ("<strong>Offline account</strong><span>Локально, без Mi-логіна</span>",
         "<strong>Профіль Offline</strong><span>Локально, без входу в обліковий запис Mi</span>"),
        ("<strong>Додавання камери</strong><span>Сучасний шлях інтерфейсу</span>",
         "<strong>Додавання камери</strong><span>Екран додавання камери на сучасному Android</span>"),
        ("Чотири кроки до живого відео.", "Чотири кроки до перегляду в реальному часі."),
        ("Скористайтеся канонічною кнопкою GitHub Release на цій сторінці.",
         "Скористайтеся кнопкою завантаження з GitHub Releases на цій сторінці."),
        ("Неофіційний проєкт сумісності для збереження робочого обладнання. Вихідний код, докази тестів і дані цілісності відкриті на GitHub.",
         "Неофіційний проєкт сумісності, що дає змогу й надалі використовувати справне обладнання. Вихідний код, результати тестів і контрольні суми опубліковані на GitHub."),
        ("покинутого програмного забезпечення", "програмного забезпечення, підтримку якого припинено"),
        ('aria-label="Mi Dash Cam app verification screenshots"',
         'aria-label="Знімки екрана, що підтверджують роботу застосунку Mi Dash Cam"'),
        ('alt="Mi Dash Cam 2.0.0 running on Poco F6"', 'alt="Mi Dash Cam 2.0.0 на Poco F6"'),
        ('alt="Mi Dash Cam release app on Poco F6"', 'alt="Реліз Mi Dash Cam 2.0.0 на Poco F6"'),
        ('alt="Offline account screen"', 'alt="Екран профілю Offline"'),
        ('alt="Add camera screen"', 'alt="Екран додавання камери"'),
    ],
    "de": [
        ("Funktionierendes Xiaomi Mi Dash Cam MJXCJLY01BY EU APK für modernes Android und HyperOS. WLAN, Livebild, Aufnahmen, Downloads und Wiedergabe mit echter Kamera getestet.",
         "Funktionierende APK für die europäische Xiaomi Mi Dash Cam MJXCJLY01BY (EU) auf aktuellen Android-Versionen und HyperOS. WLAN, Livebild, Aufnahmen, Downloads und Wiedergabe wurden mit einer echten Kamera getestet."),
        ("Xiaomi Mi Dash Cam MJXCJLY01BY European/EU model",
         "Xiaomi Mi Dash Cam MJXCJLY01BY — europäische Version (EU)"),
        ("Ja, für die getestete Konfiguration. Das exakte Release 2.0.0 hat einen vollständigen Test mit echter Kamera auf einem Poco F6 mit Android 16 / HyperOS 3 bestanden.",
         "Ja, für die getestete Konfiguration. Version 2.0.0 wurde vollständig mit einer echten Kamera auf einem Poco F6 mit Android 16 und HyperOS 3 getestet."),
        ("Mach deine <span class=\"accent\">Mi Dash Cam</span> wieder nutzbar.",
         "Bring deine <span class=\"accent\">Mi Dash Cam</span> wieder zum Laufen."),
        ("Die ursprüngliche europäische App wurde vor Jahren aufgegeben. Dieses reparierte APK bringt die Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> auf modernem Android zurück — ohne erforderliches Mi-Konto.",
         "Die ursprüngliche europäische App wird seit Jahren nicht mehr unterstützt. Diese reparierte APK macht die Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> wieder mit aktuellen Android-Versionen nutzbar — ohne erforderliches Mi-Konto."),
        (">Herunterladen Mi-Dash-Cam-2.0.0.apk</a>", ">Mi-Dash-Cam-2.0.0.apk herunterladen</a>"),
        ("Test mit echter Kamera bestanden", "Mit echter Kamera getestet"),
        ("HyperOS 3 · echte MJXCJLY01BY", "HyperOS 3 · physische Kamera MJXCJLY01BY"),
        ("<strong>v2.0.0</strong><span>Stabiles Release</span>",
         "<strong>v2.0.0</strong><span>Stabile Version</span>"),
        ("<strong>ARM64 + ARMv7</strong><span>Moderne + ältere CPUs</span>",
         "<strong>ARM64 + ARMv7</strong><span>Moderne und ältere CPUs</span>"),
        ("<strong>SHA-256 veröffentlicht</strong><span>Prüfbare Release-Integrität</span>",
         "<strong>SHA-256 veröffentlicht</strong><span>Prüfbare Dateiintegrität</span>"),
        ("europäische/EU Mi Dash Cam", "europäische Version der Mi Dash Cam (EU)"),
        ("Die alte API- und Architekturkompatibilität wurde aktualisiert, damit das APK auf Android 15 und 16 wieder normal installiert werden kann.",
         "Die Kompatibilität mit älteren Android-APIs und CPU-Architekturen wurde aktualisiert, sodass sich die APK unter Android 15 und 16 wieder normal installieren lässt."),
        ("Der alte Streaming-Pfad wurde repariert und RTSP über TCP verwendet. Das sichtbare Livebild wurde mit der echten Kamera geprüft.",
         "Der Videostream wurde repariert und RTSP über TCP aktiviert. Das Livebild wurde mit der echten Kamera überprüft."),
        ("Tote Webseiten wurden durch integrierte Hilfe und Handbücher ersetzt.",
         "Nicht mehr erreichbare Hilfeseiten wurden durch integrierte Hilfe und Handbücher ersetzt."),
        ("Nachweise statt Emulator-Versprechen.", "Nachweise aus echter Hardware statt nur aus dem Emulator."),
        ("Eine datenschutzbereinigte vollständige Aufzeichnung des Tests mit echter Kamera liegt im Repository.",
         "Eine vollständige, um persönliche Daten bereinigte Aufzeichnung des Tests mit der echten Kamera liegt im Repository."),
        ("Verwende den offiziellen GitHub-Release-Button auf dieser Seite.",
         "Verwende den Download-Button des GitHub-Releases auf dieser Seite."),
        ("Inoffizielles Kompatibilitätsprojekt zur Weiternutzung funktionierender Hardware. Quellcode, Testnachweise und Integritätsdaten sind öffentlich auf GitHub.",
         "Inoffizielles Kompatibilitätsprojekt zur weiteren Nutzung funktionsfähiger Hardware. Quellcode, Testergebnisse und Prüfsummen sind öffentlich auf GitHub verfügbar."),
        ('aria-label="Mi Dash Cam app verification screenshots"',
         'aria-label="Screenshots zum Nachweis der funktionierenden Mi-Dash-Cam-App"'),
        ('alt="Mi Dash Cam 2.0.0 running on Poco F6"', 'alt="Mi Dash Cam 2.0.0 auf einem Poco F6"'),
        ('alt="Mi Dash Cam release app on Poco F6"', 'alt="Mi Dash Cam 2.0.0 auf einem Poco F6"'),
        ('alt="Offline account screen"', 'alt="Bildschirm des Offline-Kontos"'),
        ('alt="Add camera screen"', 'alt="Bildschirm zum Hinzufügen einer Kamera"'),
    ],
}

def apply_copy(path: Path, lang: str, text: str) -> str:
    for old, new in COPY_REPLACEMENTS.get(lang, []):
        text = required_replace(text, old, new, f"{path}:{lang}")
    return text

def apply_css() -> None:
    path = SITE / "styles.css"
    text = path.read_text(encoding="utf-8")
    text = required_replace(
        text,
        ".langs{display:flex;align-items:center;gap:6px;overflow-x:auto;scrollbar-width:none}",
        ".langs{display:flex;align-items:center;gap:6px;min-width:0;overflow-x:auto;scrollbar-width:none}",
        str(path),
    )
    text = required_replace(
        text,
        ".flag{font-size:1.05em;line-height:1}",
        ".flag{display:none}.flag-img{width:18px;height:12px;flex:0 0 auto;object-fit:cover;border-radius:2px;box-shadow:0 0 0 1px rgba(20,20,20,.12)}",
        str(path),
    )
    tablet = (
        '@media(max-width:820px){.nav{flex-wrap:wrap;padding:10px 0}.brand small{display:none}'
        '.langs{order:3;width:100%;max-width:none;flex-wrap:wrap;justify-content:flex-start;padding:3px 0 2px}'
        '.lang{padding:6px 9px;flex:0 0 auto}}\n'
    )
    marker = "@media(max-width:680px)"
    if tablet not in text:
        if marker not in text:
            raise RuntimeError("mobile media marker missing")
        text = text.replace(marker, tablet + marker, 1)
    if ".wrap{width:min(calc(100% - 34px),var(--max));margin-inline:auto}" not in text:
        raise RuntimeError("desktop centered wrap invariant missing")
    if ".trust-strip{margin:4px auto 34px}" not in text:
        raise RuntimeError("trust strip centering invariant missing")
    path.write_text(text, encoding="utf-8")

def apply_js() -> None:
    path = SITE / "app.js"
    path.write_text('''(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      }
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
  }

  document.querySelectorAll('[data-copy-hash]').forEach((button) => {
    button.addEventListener('click', async () => {
      const hash = button.getAttribute('data-copy-hash');
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(hash);
        button.textContent = button.dataset.copied || 'Copied';
      } catch {
        button.textContent = hash;
      }
      setTimeout(() => { button.textContent = original; }, 1800);
    });
  });
})();
''', encoding="utf-8")

def apply_validator() -> None:
    path = ROOT / "tools" / "verify_public_naming.py"
    text = path.read_text(encoding="utf-8")
    old_languages = '''SITE_LANGUAGES = (
    ("", "🇬🇧", "English"),
    ("ru/", "🇷🇺", "Русский"),
    ("pl/", "🇵🇱", "Polski"),
    ("uk/", "🇺🇦", "Українська"),
    ("de/", "🇩🇪", "Deutsch"),
)'''
    new_languages = '''SITE_LANGUAGES = (
    ("", "en", "English"),
    ("pl/", "pl", "Polski"),
    ("uk/", "uk", "Українська"),
    ("de/", "de", "Deutsch"),
    ("ru/", None, "Русский"),
)'''
    text = required_replace(text, old_languages, new_languages, str(path))
    old_loop = '''        for route, flag, native_name in SITE_LANGUAGES:
            expected_href = f'href="{site_base}{route}"'
            if expected_href not in nav:
                errors.append(f"{rel}: missing language navigation {expected_href}")
            if flag not in nav:
                errors.append(f"{rel}: missing language flag {flag}")
            if native_name not in nav:
                errors.append(f"{rel}: missing native language label {native_name!r}")'''
    new_loop = '''        positions = []
        for route, flag_code, native_name in SITE_LANGUAGES:
            expected_href = f'href="{site_base}{route}"'
            if expected_href not in nav:
                errors.append(f"{rel}: missing language navigation {expected_href}")
                continue
            positions.append(nav.index(expected_href))
            if native_name not in nav:
                errors.append(f"{rel}: missing native language label {native_name!r}")

            lang_code = flag_code or "ru"
            link_match = re.search(
                rf'<a\\b(?=[^>]*hreflang="{lang_code}")[^>]*>.*?</a>',
                nav,
                re.DOTALL,
            )
            if not link_match:
                errors.append(f"{rel}: missing language link for {lang_code}")
                continue
            link_html = link_match.group(0)
            if flag_code:
                prefix = "" if rel == "site/index.html" else "../"
                expected_flag = f'src="{prefix}flags/{flag_code}.svg"'
                if expected_flag not in link_html:
                    errors.append(f"{rel}: missing static SVG flag {expected_flag}")
            elif "flag" in link_html or "<img" in link_html or "🇷🇺" in link_html:
                errors.append(f"{rel}: Russian selector must be text-only")

        if positions != sorted(positions):
            errors.append(f"{rel}: language order must be English, Polski, Українська, Deutsch, Русский")
        if "🇷🇺" in nav:
            errors.append(f"{rel}: Russian flag must not be present")'''
    text = required_replace(text, old_loop, new_loop, str(path))
    path.write_text(text, encoding="utf-8")

def check() -> None:
    css = (SITE / "styles.css").read_text(encoding="utf-8")
    assert ".wrap{width:min(calc(100% - 34px),var(--max));margin-inline:auto}" in css
    assert ".trust-strip{margin:4px auto 34px}" in css
    assert "@media(max-width:820px)" in css
    assert ".flag-img{" in css

    forbidden_literals = {
        "pl": ["16 KiB page size", "kanonicznego przycisku GitHub Release", "prawdziwa MJXCJLY01BY"],
        "ru": ["для современных Android", "16 KiB page size", "Путь интерфейса на новом Android", "Offline account"],
        "uk": ["16 KiB page size", "Сучасний шлях інтерфейсу", "Offline account", "Оригінальний європейський застосунок покинули"],
        "de": ["Herunterladen Mi-Dash-Cam", "Dieses reparierte APK", "Tote Webseiten", "datenschutzbereinigte vollständige"],
    }
    for lang, path in PAGES.items():
        text = path.read_text(encoding="utf-8")
        Parser().feed(text)
        nav_m = re.search(r'<nav class="langs"[^>]*>(.*?)</nav>', text, re.S)
        assert nav_m, f"{path}: nav missing"
        nav = nav_m.group(1)
        positions = []
        for code in ORDER:
            m = re.search(rf'<a\b(?=[^>]*hreflang="{code}")[^>]*>.*?</a>', nav, re.S)
            assert m, f"{path}: {code} link missing"
            positions.append(m.start())
            if code in FLAG_LANGS:
                prefix = "" if path == SITE / "index.html" else "../"
                assert f'src="{prefix}flags/{code}.svg"' in m.group(0)
            else:
                assert "flag" not in m.group(0) and "<img" not in m.group(0) and "🇷🇺" not in m.group(0)
        assert positions == sorted(positions), f"{path}: wrong language order"
        if lang != "en":
            assert 'aria-label="Mi Dash Cam app verification screenshots"' not in text
            assert 'alt="Mi Dash Cam 2.0.0 running on Poco F6"' not in text
            assert 'alt="Offline account screen"' not in text
            assert 'alt="Add camera screen"' not in text
        for bad in forbidden_literals.get(lang, []):
            assert bad not in text, f"{path}: literal/awkward phrase remains: {bad}"

        for block in re.findall(r'<script type="application/ld\\+json">(.*?)</script>', text, re.S):
            json.loads(block)

def apply() -> None:
    for lang, path in PAGES.items():
        text = path.read_text(encoding="utf-8")
        text = normalize_language_nav(path, text)
        text = apply_copy(path, lang, text)
        path.write_text(text, encoding="utf-8")
    apply_css()
    apply_js()
    apply_validator()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.apply:
        apply()
    if args.check:
        check()
