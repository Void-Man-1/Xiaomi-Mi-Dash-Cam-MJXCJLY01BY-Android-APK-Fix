#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CHANGES = {
    "site/pl/index.html": [
        ("Oryginalna europejska aplikacja nie jest wspierana od lat.", "Oryginalna europejska aplikacja od lat nie jest już rozwijana."),
        ("Projekt jest przeznaczony dla europejskiej wersji Mi Dash Cam (EU) oraz starej aplikacji", "Projekt jest przeznaczony dla europejskiej wersji Mi Dash Cam (EU) i jej oryginalnej aplikacji"),
        ("Zaktualizowano zgodność ze starszym API i architekturami procesora, dzięki czemu plik APK znów instaluje się normalnie na Androidzie 15 i 16.", "Dostosowano aplikację do nowszych wersji Androida i współczesnych architektur procesora, dzięki czemu plik APK znów instaluje się normalnie na Androidzie 15 i 16."),
        ("Martwe strony internetowe zastąpiono wbudowaną pomocą i instrukcjami.", "Niedziałające strony pomocy zastąpiono wbudowaną pomocą i instrukcjami."),
        ("Ścieżka UI na nowym Androidzie", "Ekran dodawania kamery na nowym Androidzie"),
        ("Testy fizyczne lub emulowane są udokumentowane dla Androida 8.1, 9 oraz 12–16.", "Udokumentowano testy na urządzeniach fizycznych lub w emulatorach dla Androida 8.1, 9 oraz 12–16."),
    ],
    "site/ru/index.html": [
        ("<span>Документированное тестирование</span>", "<span>Задокументированные тесты</span>"),
        ("<span>Проверяемая целостность релиза</span>", "<span>Возможность проверить целостность файла</span>"),
        ("Совместимость с ним этим проектом не заявляется.", "Проект не заявляет совместимость с этой моделью."),
        ("<h3>Установка на новых Android</h3>", "<h3>Установка на новых версиях Android</h3>"),
        ("Опубликованный APK протестирован с настоящей камерой EU.", "Опубликованный APK протестирован с настоящей камерой в версии EU."),
        ("Добавьте камеру, проверьте живое видео и локально просматривайте или скачивайте записи.", "Добавьте камеру, проверьте предпросмотр в реальном времени, затем локально просматривайте или скачивайте записи."),
        ("Это независимый проект по сохранению работоспособности заброшенного ПО.", "Это независимый проект по сохранению работоспособности ПО, поддержка которого прекращена."),
        ("Физические или эмуляторные тесты задокументированы для Android 8.1, 9 и 12–16.", "Тесты на физических устройствах и в эмуляторах проведены и задокументированы для Android 8.1, 9 и 12–16."),
    ],
    "site/uk/index.html": [
        ("<span>Стабільний реліз</span>", "<span>Стабільна версія</span>"),
        ("<span>Перевірювана цілісність релізу</span>", "<span>Можна перевірити цілісність файлу</span>"),
        ("Проєкт призначений для європейської версії Mi Dash Cam (EU) і старого застосунку", "Проєкт призначений для європейської версії Mi Dash Cam (EU) та її оригінального застосунку"),
        ("Опублікований APK-файл протестовано з реальною камерою EU.", "Опублікований APK-файл протестовано з реальною камерою у версії EU."),
        ("<div class=\"kicker\">Установлення</div>", "<div class=\"kicker\">Встановлення</div>"),
        ("перевірте живе відео, потім переглядайте або завантажуйте записи локально.", "перевірте перегляд у реальному часі, потім переглядайте або завантажуйте записи локально."),
        ("<h2>Перед установленням</h2>", "<h2>Перед встановленням</h2>"),
        ("Фізичні або емуляторні тести задокументовано для Android 8.1, 9 та 12–16.", "Тести на фізичних пристроях або в емуляторах задокументовано для Android 8.1, 9 та 12–16."),
    ],
    "site/de/index.html": [
        ("Mit echter Kamera verifizierte Kompatibilität", "Kompatibilität mit echter Kamera geprüft"),
        ("— ohne erforderliches Mi-Konto.", "— ganz ohne Mi-Konto."),
        ("<span>Dokumentierte Testabdeckung</span>", "<span>Dokumentierter Testumfang</span>"),
        ("Dieses Projekt richtet sich an die europäische Version der Mi Dash Cam (EU) und die alte App", "Dieses Projekt richtet sich an die europäische Version der Mi Dash Cam (EU) und deren ursprüngliche App"),
        ("<h3>Installation auf aktuellem Android</h3>", "<h3>Installation auf aktuellen Android-Versionen</h3>"),
        ("<h3>Keine Mi-Konto-Abhängigkeit</h3>", "<h3>Kein Mi-Konto erforderlich</h3>"),
        ("Genau das veröffentlichte APK wurde mit einer echten EU-Kamera getestet.", "Die veröffentlichte APK-Datei wurde mit einer echten Kamera in der EU-Version getestet."),
        ("<strong>Release auf Poco F6</strong>", "<strong>Version 2.0.0 auf Poco F6</strong>"),
        ("<span>UI-Pfad auf modernem Android</span>", "<span>Kamera hinzufügen unter aktuellem Android</span>"),
        ("<h2>Getestetes Release herunterladen</h2>", "<h2>Getestete Version herunterladen</h2>"),
        ("aktuelle stabile Kompatibilitäts-Build", "aktuelle stabile Kompatibilitätsversion"),
        (">Release-Hinweise</a>", ">Versionshinweise</a>"),
        ("aufgegebene Begleitsoftware", "nicht mehr gepflegte Begleitsoftware"),
        ("diese Version ist mit dem Projektschlüssel signiert", "diese Version ist mit dem Projektschlüssel signiert"),
        ("Physische oder emulierte Tests sind für Android 8.1, 9 sowie 12–16 dokumentiert.", "Tests auf physischen Geräten oder in Emulatoren sind für Android 8.1, 9 sowie 12–16 dokumentiert."),
    ],
}

# One source sentence uses "dieser Build"; keep a separate exact replacement.
CHANGES["site/de/index.html"].append(("dieser Build ist mit dem Projektschlüssel signiert", "diese Version ist mit dem Projektschlüssel signiert"))

for rel, replacements in CHANGES.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old == new:
            continue
        if old not in text:
            raise SystemExit(f"{rel}: expected phrase missing: {old!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

# Editorial regression checks.
for rel in CHANGES:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for old, new in CHANGES[rel]:
        if old != new and old in text:
            raise SystemExit(f"{rel}: old phrase remains: {old!r}")
        if new not in text:
            raise SystemExit(f"{rel}: replacement missing: {new!r}")
    for block in re.findall(r'<script type="application/ld\\+json">(.*?)</script>', text, re.S):
        json.loads(block)

print("Final locale editorial checks passed.")
