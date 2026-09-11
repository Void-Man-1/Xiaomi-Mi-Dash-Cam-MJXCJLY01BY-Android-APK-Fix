#!/usr/bin/env python3
"""Repository-wide static integrity checks for the Mi Dash Cam project.

This validator is intentionally dependency-free so it can run on GitHub-hosted
runners and contributor machines with only Python 3.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REPO = "Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix"
PAGES_BASE = f"https://void-man-1.github.io/{REPO}/"
RELEASE_SHA256 = "2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887"
ORIGINAL_SHA256 = "3AC4C02EF5D43A0F9636637B1359073818C6799F3BFE3A7E2A38633F653D95A8"
SOCIAL_IMAGE = f"{PAGES_BASE}social-preview.png"
RAW_REPO_ASSET_PREFIX = f"https://raw.githubusercontent.com/Void-Man-1/{REPO}/main/assets/"
SITE_PAGES = {
    "site/index.html": "en",
    "site/pl/index.html": "pl",
    "site/uk/index.html": "uk",
    "site/de/index.html": "de",
    "site/ru/index.html": "ru",
}
LOCALE_ROUTES = {"en": "", "pl": "pl/", "uk": "uk/", "de": "de/", "ru": "ru/"}
EXPECTED_LANGUAGE_ORDER = ["en", "pl", "uk", "de", "ru"]
TEXT_SUFFIXES = {".md", ".txt", ".html", ".yml", ".yaml", ".ps1", ".py", ".json", ".xml"}
EXCLUDED_STALE_PREFIXES = ("docs/superpowers/", "docs/AUDIT_2026-09-11.md")
PRIVATE_KEY_SUFFIXES = {".p12", ".pfx", ".p8", ".pk8", ".pkcs8", ".jks", ".keystore", ".pem", ".key"}


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang: str | None = None
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.scripts: list[tuple[dict[str, str], str]] = []
        self._script_attrs: dict[str, str] | None = None
        self._script_chunks: list[str] = []
        self.lang_nav_links: list[dict[str, str]] = []
        self._in_lang_nav = False
        self._nav_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        data = dict(attrs)
        if tag == "html":
            self.html_lang = data.get("lang")
        elif tag == "meta":
            self.metas.append(data)
        elif tag == "link":
            self.links.append(data)
        elif tag == "script":
            self._script_attrs = data
            self._script_chunks = []
        elif tag == "nav":
            classes = set(data.get("class", "").split())
            if "langs" in classes:
                self._in_lang_nav = True
                self._nav_depth = 1
            elif self._in_lang_nav:
                self._nav_depth += 1
        elif tag == "a" and self._in_lang_nav:
            self.lang_nav_links.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script_attrs is not None:
            self.scripts.append((self._script_attrs, "".join(self._script_chunks)))
            self._script_attrs = None
            self._script_chunks = []
        elif tag == "nav" and self._in_lang_nav:
            self._nav_depth -= 1
            if self._nav_depth <= 0:
                self._in_lang_nav = False

    def handle_data(self, data: str) -> None:
        if self._script_attrs is not None:
            self._script_chunks.append(data)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def meta_value(parser: HeadParser, *, prop: str | None = None, name: str | None = None) -> str | None:
    for meta in parser.metas:
        if prop is not None and meta.get("property") == prop:
            return meta.get("content")
        if name is not None and meta.get("name") == name:
            return meta.get("content")
    return None


def canonical_value(parser: HeadParser) -> str | None:
    for link in parser.links:
        if link.get("rel") == "canonical":
            return link.get("href")
    return None


def staged_media_source(clean: str) -> Path | None:
    normalized = clean.replace("\\", "/")
    while normalized.startswith("../"):
        normalized = normalized[3:]
    if normalized == "media/app-icon.png":
        return ROOT / "assets/app-icon.png"
    if normalized.startswith("media/screenshots/"):
        return ROOT / "assets/screenshots" / Path(normalized).name
    if normalized.startswith("media/"):
        return ROOT / "assets/evidence" / Path(normalized).name
    return None


def local_site_reference_exists(page_path: str, value: str) -> bool:
    if not value or value.startswith(("#", "mailto:", "tel:", "data:")):
        return True
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"}:
        return True
    clean = value.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return True
    page_dir = (ROOT / page_path).parent
    candidate = (page_dir / clean).resolve()
    try:
        candidate.relative_to((ROOT / "site").resolve())
    except ValueError:
        return True
    if candidate.exists():
        return True
    staged = staged_media_source(clean)
    return staged.is_file() if staged is not None else False


def main() -> int:
    errors: list[str] = []

    checksum = read("checksums/SHA256SUMS.txt")
    if not re.search(rf"(?im)^\s*{RELEASE_SHA256}\s+Mi-Dash-Cam-2\.0\.0\.apk\s*$", checksum):
        errors.append("checksums/SHA256SUMS.txt: immutable v2.0.0 APK digest/name mismatch")

    original_checksum = read("source-kit/checksums/original-apk.sha256")
    if not re.search(rf"(?im)^\s*{ORIGINAL_SHA256}\s+\S+\.apk\s*$", original_checksum):
        errors.append("source-kit/checksums/original-apk.sha256: stock input digest mismatch")

    try:
        manifest = json.loads(read("source-kit/patches/2.0.0/manifest.json"))
    except Exception as exc:
        errors.append(f"source-kit manifest is invalid JSON: {exc}")
        manifest = {}
    if str(manifest.get("releaseVersion")) != "2.0.0":
        errors.append("source-kit manifest: releaseVersion must remain 2.0.0")
    if str(manifest.get("packageName")) != "com.banyac.mijia.app.eu":
        errors.append("source-kit manifest: packageName mismatch")
    if str(manifest.get("originalApkSha256", "")).upper() != ORIGINAL_SHA256:
        errors.append("source-kit manifest: original APK digest disagrees with pinned stock digest")
    if str(manifest.get("apktoolVersion")) != "3.0.3":
        errors.append("source-kit manifest: Apktool version is not pinned to 3.0.3")

    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in PRIVATE_KEY_SUFFIXES:
            rel = path.relative_to(ROOT).as_posix()
            if rel != "source-kit/LICENSES/LGPL-2.1-or-later.txt":
                errors.append(f"{rel}: private-key-like file extension is forbidden in the repository")

    stale_patterns = (
        re.compile(r"\b2\.0\.0\b.{0,100}\brelease candidate\b", re.I | re.S),
        re.compile(r"\bremaining release gate\b", re.I),
    )
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(EXCLUDED_STALE_PREFIXES) or rel == "tools/verify_repository_integrity.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in stale_patterns:
            if pattern.search(text):
                errors.append(f"{rel}: stale release-candidate/pending-gate wording remains")
                break

    for rel in ("docs/README.pl.md", "docs/README.uk.md", "docs/README.de.md", "docs/README.ru.md"):
        if not (ROOT / rel).is_file():
            errors.append(f"{rel}: localized README is missing")

    sync = read(".github/workflows/update-readme-download.yml")
    for rel in (*SITE_PAGES.keys(), "README.md", "docs/README.pl.md", "docs/README.uk.md", "docs/README.de.md", "docs/README.ru.md"):
        if rel not in sync:
            errors.append(f"update-readme-download.yml: release sync does not cover {rel}")

    if not (ROOT / "site/social-preview.png").is_file():
        errors.append("site/social-preview.png: dedicated 1200x630 social preview is missing")

    for page_path, language in SITE_PAGES.items():
        text = read(page_path)
        parser = HeadParser()
        parser.feed(text)

        if RAW_REPO_ASSET_PREFIX in text:
            errors.append(f"{page_path}: repository-owned site media must be served from the Pages origin, not raw.githubusercontent.com")

        if parser.html_lang != language:
            errors.append(f"{page_path}: html lang={parser.html_lang!r}, expected {language!r}")

        expected_url = PAGES_BASE + LOCALE_ROUTES[language]
        if canonical_value(parser) != expected_url:
            errors.append(f"{page_path}: canonical URL mismatch")

        if meta_value(parser, prop="og:image") != SOCIAL_IMAGE:
            errors.append(f"{page_path}: og:image must use the dedicated Pages-hosted social preview")
        if meta_value(parser, name="twitter:image") != SOCIAL_IMAGE:
            errors.append(f"{page_path}: twitter:image must use the dedicated Pages-hosted social preview")
        if meta_value(parser, prop="og:image:width") != "1200":
            errors.append(f"{page_path}: og:image:width must be 1200")
        if meta_value(parser, prop="og:image:height") != "630":
            errors.append(f"{page_path}: og:image:height must be 630")

        title = meta_value(parser, prop="og:title")
        description = meta_value(parser, prop="og:description")
        twitter_title = meta_value(parser, name="twitter:title")
        twitter_description = meta_value(parser, name="twitter:description")
        if not all((title, description, twitter_title, twitter_description)):
            errors.append(f"{page_path}: social title/description metadata is incomplete")

        jsonld_count = 0
        for attrs, payload in parser.scripts:
            if attrs.get("type") == "application/ld+json":
                jsonld_count += 1
                try:
                    json.loads(payload)
                except json.JSONDecodeError as exc:
                    errors.append(f"{page_path}: invalid JSON-LD: {exc}")
        if jsonld_count < 1:
            errors.append(f"{page_path}: JSON-LD metadata is missing")

        order = [link.get("hreflang") for link in parser.lang_nav_links]
        if order != EXPECTED_LANGUAGE_ORDER:
            errors.append(f"{page_path}: language order is {order!r}, expected {EXPECTED_LANGUAGE_ORDER!r}")

        nav_match = re.search(r'<nav\s+class="langs"[^>]*>(.*?)</nav>', text, re.S)
        if not nav_match:
            errors.append(f"{page_path}: language selector is missing")
        else:
            ru = re.search(r'<a\b(?=[^>]*hreflang="ru")[^>]*>(.*?)</a>', nav_match.group(1), re.S)
            if not ru:
                errors.append(f"{page_path}: Russian language link is missing")
            elif "<img" in ru.group(1) or "🇷🇺" in ru.group(1):
                errors.append(f"{page_path}: Russian language link must not render a flag")

        for attr in re.findall(r'\b(?:src|href)="([^"]+)"', text):
            if not local_site_reference_exists(page_path, attr):
                errors.append(f"{page_path}: referenced local asset does not exist: {attr}")

    sitemap = read("site/sitemap.xml")
    for route in LOCALE_ROUTES.values():
        url = PAGES_BASE + route
        if url not in sitemap:
            errors.append(f"site/sitemap.xml: missing {url}")

    robots = read("site/robots.txt")
    if f"Sitemap: {PAGES_BASE}sitemap.xml" not in robots:
        errors.append("site/robots.txt: canonical sitemap URL is missing")

    if errors:
        print("Repository integrity validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository integrity validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
