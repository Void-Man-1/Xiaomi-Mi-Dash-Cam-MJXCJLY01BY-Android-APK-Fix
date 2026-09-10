#!/usr/bin/env python3
"""One-time text/build naming migration. Safe to rerun; does not rename the repository."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OLD_APK = "Mi-Dash-Cam-EU-2.0.0-android12-16-arm64.apk"
NEW_APK = "Mi-Dash-Cam-2.0.0.apk"
OLD_RELEASE_TITLE = "Mi Dash Cam MJXCJLY01BY EU Android 8.1-16 fix 2.0.0"
CANONICAL_TITLE = "Xiaomi Mi Dash Cam MJXCJLY01BY Android APK Fix"

TEXT_SUFFIXES = {".md", ".txt", ".html", ".yml", ".yaml", ".ps1", ".py", ".xml"}
SKIP_PREFIXES = (
    "docs/superpowers/",
    "source-kit/patches/",
    "source-kit/reference-source/",
)
SKIP_FILES = {
    "tools/apply_uniform_naming_migration.py",
    "tools/verify_public_naming.py",
}


def text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES or rel.startswith(SKIP_PREFIXES):
            continue
        yield rel, path


def replace_all_public_text() -> None:
    replacements = (
        (OLD_APK, NEW_APK),
        ("Mi-Dash-Cam-EU-", "Mi-Dash-Cam-"),
        (OLD_RELEASE_TITLE, "Mi Dash Cam 2.0.0"),
        ("Mi Dash Cam EU 2.0.0", "Mi Dash Cam 2.0.0"),
        ("2.0.0 EU compatibility release", "2.0.0 compatibility release"),
    )
    for rel, path in text_files():
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"updated {rel}")


def patch_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<h1 align="center">Mi Dash cam Android 8.1-16 fix<br><code>MJXCJLY01BY</code></h1>',
        f'<h1 align="center">{CANONICAL_TITLE}</h1>',
    )
    text = text.replace(
        'Compatibility-fixed Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> EU APK for Android 8.1–16 and HyperOS.',
        'Compatibility-fixed Xiaomi Mi Dash Cam <code>MJXCJLY01BY</code> APK for Android 8.1–16 and HyperOS.',
    )
    path.write_text(text, encoding="utf-8")


def patch_listing() -> None:
    path = ROOT / "docs/GITHUB_LISTING.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"(?ms)(## Repository name\n\n)`[^`]+`",
        r"\1`Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix`",
        text,
        count=1,
    )
    text = re.sub(
        r"(?ms)(## About description\n\n).*?(?=\n\n## Suggested topics)",
        r"\1Android compatibility APK for Xiaomi Mi Dash Cam MJXCJLY01BY. Restores installation, Wi-Fi, live preview, downloads and playback on modern Android / HyperOS; tested on Poco F6.",
        text,
        count=1,
    )
    text = re.sub(
        r"(?ms)(## Suggested social preview text\n\n).*?(?=\n\n## First release)",
        r"\1Keep the Xiaomi Mi Dash Cam MJXCJLY01BY working on modern Android. Version 2.0.0 provides accountless startup, ARM64/16 KiB support, repaired help/manuals, RTSP/TCP live preview, and reconnect hardening. Full physical-camera operation passed on a Poco F6 running Android 16 / HyperOS 3.",
        text,
        count=1,
    )
    text = text.replace("- Title: `Mi Dash Cam MJXCJLY01BY EU Android 8.1-16 fix 2.0.0`", "- Title: `Mi Dash Cam 2.0.0`")
    path.write_text(text, encoding="utf-8")


def patch_release_notes() -> None:
    path = ROOT / "docs/RELEASE_NOTES_2.0.0.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^# .*2\.0\.0 release notes$", "# Mi Dash Cam 2.0.0 release notes", text, count=1, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8")


def patch_site(path: Path, language: str) -> None:
    text = path.read_text(encoding="utf-8")
    if language == "en":
        text = re.sub(r"<title>.*?</title>", f"<title>{CANONICAL_TITLE} | Android 8.1–16 / HyperOS</title>", text, count=1)
        text = re.sub(r'<meta name="description" content="[^"]+">', '<meta name="description" content="Xiaomi Mi Dash Cam MJXCJLY01BY Android APK fix for Android 8.1–16 and HyperOS. Restores installation, Wi-Fi, live preview, downloads and playback; hardware-tested on Poco F6.">', text, count=1)
        text = re.sub(r'<meta property="og:site_name" content="[^"]+">', f'<meta property="og:site_name" content="{CANONICAL_TITLE}">', text, count=1)
        text = re.sub(r'<meta property="og:title" content="[^"]+">', f'<meta property="og:title" content="{CANONICAL_TITLE}">', text, count=1)
        text = re.sub(r'<meta property="og:description" content="[^"]+">', '<meta property="og:description" content="Mi Dash Cam compatibility fix for modern Android and HyperOS: installation, camera Wi-Fi, live preview, recordings, downloads and playback.">', text, count=1)
        text = re.sub(r'<meta name="twitter:title" content="[^"]+">', f'<meta name="twitter:title" content="{CANONICAL_TITLE}">', text, count=1)
        text = re.sub(r'<meta name="twitter:description" content="[^"]+">', '<meta name="twitter:description" content="Mi Dash Cam MJXCJLY01BY Android APK fix for modern Android and HyperOS; physically tested on Poco F6 / Android 16.">', text, count=1)
        text = text.replace('"name": "Mi Dash Cam MJXCJLY01BY Android compatibility fix"', f'"name": "{CANONICAL_TITLE}"')
        text = text.replace('"alternateName": "Mi Dash Cam 2.0.0"', '"alternateName": "Mi Dash Cam 2.0.0"')
        text = re.sub(r'<div class="eyebrow">.*?</div>\s*<h1>.*?</h1>', '<div class="eyebrow">Android 8.1–16 · HyperOS compatibility release</div>\n      <h1>Xiaomi Mi Dash Cam MJXCJLY01BY<br>Android APK Fix</h1>', text, count=1, flags=re.DOTALL)
    elif language == "ru":
        text = re.sub(r"<title>.*?</title>", f"<title>{CANONICAL_TITLE} | Android 8.1–16 / HyperOS</title>", text, count=1)
        text = re.sub(r'<meta name="description" content="[^"]+">', '<meta name="description" content="Исправление APK Xiaomi Mi Dash Cam MJXCJLY01BY для Android 8.1–16 и HyperOS: установка, Wi‑Fi, live preview, скачивание и воспроизведение; проверено на Poco F6.">', text, count=1)
        text = re.sub(r'<meta property="og:title" content="[^"]+">', f'<meta property="og:title" content="{CANONICAL_TITLE}">', text, count=1)
        text = re.sub(r'<meta property="og:description" content="[^"]+">', '<meta property="og:description" content="Исправление Mi Dash Cam для современных Android и HyperOS: Wi‑Fi, live preview, записи, скачивание и воспроизведение.">', text, count=1)
        text = text.replace('"name":"Mi Dash Cam MJXCJLY01BY Android compatibility fix"', f'"name":"{CANONICAL_TITLE}"')
        text = re.sub(r'<div class="eyebrow">.*?</div><h1>.*?</h1>', '<div class="eyebrow">Android 8.1–16 · HyperOS</div><h1>Xiaomi Mi Dash Cam MJXCJLY01BY<br>Исправление APK для Android</h1>', text, count=1, flags=re.DOTALL)
    elif language == "pl":
        text = re.sub(r"<title>.*?</title>", f"<title>{CANONICAL_TITLE} | Android 8.1–16 / HyperOS</title>", text, count=1)
        text = re.sub(r'<meta name="description" content="[^"]+">', '<meta name="description" content="Poprawka APK Xiaomi Mi Dash Cam MJXCJLY01BY dla Androida 8.1–16 i HyperOS: instalacja, Wi‑Fi, podgląd, pobieranie i odtwarzanie; sprawdzone na Poco F6.">', text, count=1)
        text = re.sub(r'<meta property="og:title" content="[^"]+">', f'<meta property="og:title" content="{CANONICAL_TITLE}">', text, count=1)
        text = re.sub(r'<meta property="og:description" content="[^"]+">', '<meta property="og:description" content="Poprawka Mi Dash Cam dla współczesnego Androida i HyperOS: Wi‑Fi, podgląd na żywo, nagrania, pobieranie i odtwarzanie.">', text, count=1)
        text = text.replace('"name":"Mi Dash Cam MJXCJLY01BY Android compatibility fix"', f'"name":"{CANONICAL_TITLE}"')
        text = re.sub(r'<div class="eyebrow">.*?</div><h1>.*?</h1>', '<div class="eyebrow">Android 8.1–16 · HyperOS</div><h1>Xiaomi Mi Dash Cam MJXCJLY01BY<br>Poprawka APK dla Androida</h1>', text, count=1, flags=re.DOTALL)
    path.write_text(text, encoding="utf-8")


def patch_release_sync_workflow() -> None:
    path = ROOT / ".github/workflows/update-readme-download.yml"
    text = path.read_text(encoding="utf-8")

    old_block = re.compile(
        r'''          tag="\$\(jq -r '\.tag_name' <<<"\$release_json"\)"\n'''
        r'''          apk_name=.*?\n'''
        r'''          apk_url=.*?\n'''
        r'''          alias_id=.*?\n\n'''
        r'''          if \[\[ -z "\$apk_name" \|\| -z "\$apk_url" \]\]; then\n'''
        r'''            echo "No canonical APK found in latest release: \$tag" >&2\n'''
        r'''            exit 1\n'''
        r'''          fi\n\n'''
        r'''          echo "tag=\$tag" >> "\$GITHUB_OUTPUT"\n'''
        r'''          echo "apk_name=\$apk_name" >> "\$GITHUB_OUTPUT"\n'''
        r'''          echo "apk_url=\$apk_url" >> "\$GITHUB_OUTPUT"\n'''
        r'''          echo "alias_id=\$alias_id" >> "\$GITHUB_OUTPUT"\n\n'''
        r'''      - name: Remove obsolete latest-name alias\n'''
        r'''        if: steps\.release\.outputs\.alias_id != ''\n'''
        r'''        env:\n'''
        r'''          GH_TOKEN: \$\{\{ github\.token \}\}\n'''
        r'''          ALIAS_ID: \$\{\{ steps\.release\.outputs\.alias_id \}\}\n'''
        r'''        shell: bash\n'''
        r'''        run: \|\n'''
        r'''          set -euo pipefail\n'''
        r'''          gh api --method DELETE "repos/\$\{GITHUB_REPOSITORY\}/releases/assets/\$\{ALIAS_ID\}"\n''',
        re.DOTALL,
    )
    new_block = '''          tag="$(jq -r '.tag_name' <<<"$release_json")"
          version="${tag#v}"
          expected_name="Mi-Dash-Cam-${version}.apk"
          apk_name="$(jq -r --arg expected "$expected_name" '[.assets[] | select(.name == $expected)][0].name // empty' <<<"$release_json")"
          apk_url="$(jq -r --arg expected "$expected_name" '[.assets[] | select(.name == $expected)][0].browser_download_url // empty' <<<"$release_json")"

          if [[ -z "$apk_name" || -z "$apk_url" ]]; then
            echo "Canonical APK $expected_name not found in latest release: $tag" >&2
            exit 1
          fi

          echo "tag=$tag" >> "$GITHUB_OUTPUT"
          echo "apk_name=$apk_name" >> "$GITHUB_OUTPUT"
          echo "apk_url=$apk_url" >> "$GITHUB_OUTPUT"
'''
    text, count = old_block.subn(new_block, text, count=1)
    if count != 1:
        raise SystemExit("Could not rewrite canonical APK selection block")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    replace_all_public_text()
    patch_readme()
    patch_listing()
    patch_release_notes()
    patch_site(ROOT / "site/index.html", "en")
    patch_site(ROOT / "site/ru/index.html", "ru")
    patch_site(ROOT / "site/pl/index.html", "pl")
    patch_release_sync_workflow()


if __name__ == "__main__":
    main()
