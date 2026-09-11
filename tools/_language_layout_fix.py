from pathlib import Path

path = Path("site/de/index.html")
text = path.read_text(encoding="utf-8")
old = "Kompatibilitätskorrekturen für aktuelle Android-Versionen."
new = "Korrekturen für aktuelle Android-Versionen."
if old not in text:
    raise SystemExit("Expected German heading not found")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("GERMAN_MOBILE_OVERFLOW_FIX_OK")
