#!/usr/bin/env python3
"""Validate the public naming contract for the Mi Dash Cam project."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_TITLE = "Xiaomi Mi Dash Cam MJXCJLY01BY Android APK Fix"
CANONICAL_APK = "Mi-Dash-Cam-2.0.0.apk"
OLD_REPO = "Mi-Dash-cam-Android-8.1-16-fix-MJXCJLY01BY"
NEW_REPO = "Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix"

TEXT_SUFFIXES = {".md", ".txt", ".html", ".yml", ".yaml", ".ps1", ".py", ".json", ".xml"}
SKIP_PREFIXES = (
    ".git/",
    "docs/superpowers/specs/",
    "docs/superpowers/plans/",
)
SKIP_FILES = {
    "tools/verify_public_naming.py",
    "tools/apply_uniform_naming_migration.py",
}
BANNED_PUBLIC_PATTERNS = (
    "Mi-Dash-Cam-EU-",
    "Mi Dash Cam EU 2.0.0",
    "Mi Dash Cam MJXCJLY01BY EU Android",
)

REQUIRED_APK_FILES = (
    "README.md",
    "docs/README.ru.md",
    "docs/README.pl.md",
    "docs/RELEASE_NOTES_2.0.0.md",
    "docs/PUBLISHING_CHECKLIST.md",
    "release-assets/README.md",
    "checksums/SHA256SUMS.txt",
    "site/index.html",
    "site/ru/index.html",
    "site/pl/index.html",
    "site/uk/index.html",
    "site/de/index.html",
)

SITE_PAGES = (
    "site/index.html",
    "site/ru/index.html",
    "site/pl/index.html",
    "site/uk/index.html",
    "site/de/index.html",
)
SITE_LANGUAGES = (
    ("", "🇬🇧", "English"),
    ("ru/", "🇷🇺", "Русский"),
    ("pl/", "🇵🇱", "Polski"),
    ("uk/", "🇺🇦", "Українська"),
    ("de/", "🇩🇪", "Deutsch"),
)


def iter_public_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES or rel.startswith(SKIP_PREFIXES):
            continue
        yield rel, path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-rename", action="store_true", help="also reject the old repository slug")
    args = parser.parse_args()

    errors: list[str] = []
    contents: dict[str, str] = {}
    for rel, path in iter_public_text_files():
        try:
            contents[rel] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

    for rel, text in contents.items():
        for pattern in BANNED_PUBLIC_PATTERNS:
            if pattern in text:
                errors.append(f"{rel}: legacy public naming remains: {pattern!r}")
        if args.post_rename and OLD_REPO in text:
            errors.append(f"{rel}: old repository slug remains after rename")

    readme = contents.get("README.md", "")
    if CANONICAL_TITLE not in readme:
        errors.append(f"README.md: missing canonical title {CANONICAL_TITLE!r}")

    for rel in REQUIRED_APK_FILES:
        text = contents.get(rel)
        if text is None:
            errors.append(f"{rel}: required public file is missing or unreadable")
        elif CANONICAL_APK not in text:
            errors.append(f"{rel}: missing canonical APK filename {CANONICAL_APK!r}")

    build = contents.get("source-kit/scripts/build.ps1", "")
    if '$releaseName = "Mi-Dash-Cam-$($manifest.releaseVersion)"' not in build:
        errors.append("source-kit/scripts/build.ps1: contributor build stem is not canonical")

    sync = contents.get(".github/workflows/update-readme-download.yml", "")
    if "Mi-Dash-Cam-${version}.apk" not in sync and "Mi-Dash-Cam-$version.apk" not in sync:
        errors.append(".github/workflows/update-readme-download.yml: canonical exact release asset pattern is missing")

    # The site uses absolute language links so the same selector works reliably
    # from the root page and every localized subdirectory. Validate the actual
    # language navigation block rather than requiring a particular relative-URL style.
    site_base = f"https://void-man-1.github.io/{NEW_REPO}/"
    for rel in SITE_PAGES:
        text = contents.get(rel, "")
        nav_match = re.search(r'<nav\s+class="langs"[^>]*>(.*?)</nav>', text, re.DOTALL)
        if not nav_match:
            errors.append(f"{rel}: language navigation block is missing")
            continue

        nav = nav_match.group(1)
        for route, flag, native_name in SITE_LANGUAGES:
            expected_href = f'href="{site_base}{route}"'
            if expected_href not in nav:
                errors.append(f"{rel}: missing language navigation {expected_href}")
            if flag not in nav:
                errors.append(f"{rel}: missing language flag {flag}")
            if native_name not in nav:
                errors.append(f"{rel}: missing native language label {native_name!r}")

    if args.post_rename:
        site = contents.get("site/index.html", "")
        if NEW_REPO not in site:
            errors.append("site/index.html: new repository slug missing in post-rename mode")

    if errors:
        print("Public naming validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Public naming validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
