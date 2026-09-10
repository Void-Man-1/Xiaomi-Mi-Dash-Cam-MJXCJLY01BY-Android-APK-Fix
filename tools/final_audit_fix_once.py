#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

changes = {
    "site/de/index.html": [
        ("Diese reparierte APK macht die Xiaomi Mi Dash Cam", "Diese angepasste APK-Datei macht die Xiaomi Mi Dash Cam"),
        ("Version 2.0.0 ist der aktuelle stabile Kompatibilitätsversion.", "Version 2.0.0 ist die aktuelle stabile Kompatibilitätsversion."),
    ],
    "site/pl/index.html": [
        ("<h3>Instalacja na nowych Androidach</h3>", "<h3>Instalacja na nowych wersjach Androida</h3>"),
        ("Aplikacja uruchamia się z kontem „Offline” i działa lokalnie, bez zależności od przestarzałego logowania Xiaomi.", "Aplikacja uruchamia się z kontem „Offline” i działa lokalnie, bez korzystania z przestarzałego mechanizmu logowania Xiaomi."),
    ],
    "site/uk/index.html": [
        ("Перед установленням звірте код моделі на корпусі.", "Перед встановленням звірте код моделі на корпусі."),
        ("<div class=\"kicker\" style=\"color:#ffe4d1\">v2.0.0 · Стабільний</div>", "<div class=\"kicker\" style=\"color:#ffe4d1\">v2.0.0 · Стабільна версія</div>"),
    ],
}

for rel, replacements in changes.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"{rel}: expected phrase missing: {old!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

css_path = ROOT / "site/styles.css"
css = css_path.read_text(encoding="utf-8")
needle = "@media(max-width:980px){.nav-links{display:none}"
if needle not in css:
    raise SystemExit("Expected 980px navigation breakpoint not found")
nav_breakpoint = "@media(max-width:1100px){.nav-links{display:none}}\n"
if nav_breakpoint not in css:
    css = css.replace(needle, nav_breakpoint + needle, 1)
css_path.write_text(css, encoding="utf-8")

# Assertions for the exact regressions addressed in this pass.
assert "Version 2.0.0 ist die aktuelle stabile Kompatibilitätsversion." in (ROOT / "site/de/index.html").read_text(encoding="utf-8")
assert "Instalacja na nowych wersjach Androida" in (ROOT / "site/pl/index.html").read_text(encoding="utf-8")
uk = (ROOT / "site/uk/index.html").read_text(encoding="utf-8")
assert "Перед встановленням" in uk and "v2.0.0 · Стабільна версія" in uk
assert nav_breakpoint in css
print("Final audit fixes applied and asserted.")
