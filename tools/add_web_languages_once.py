from pathlib import Path

BASE = "https://void-man-1.github.io/Mi-Dash-cam-Android-8.1-16-fix-MJXCJLY01BY/"

# README: add a visible website button immediately under the canonical APK block.
readme = Path("README.md")
text = readme.read_text(encoding="utf-8")
if "Open project website" not in text:
    marker = "<!-- latest-apk-download:end -->"
    block = '''<!-- latest-apk-download:end -->

<p align="center">
  <a href="https://void-man-1.github.io/Mi-Dash-cam-Android-8.1-16-fix-MJXCJLY01BY/">
    <img src="https://img.shields.io/badge/Open-Project%20Website-2563EB?style=for-the-badge&logo=githubpages&logoColor=white" alt="Open project website">
  </a>
</p>'''
    if marker not in text:
        raise SystemExit("README download marker missing")
    text = text.replace(marker, block, 1)
    readme.write_text(text, encoding="utf-8")

# English site: add hreflang alternates and language selector.
site = Path("site/index.html")
body = site.read_text(encoding="utf-8")
if 'hreflang="ru"' not in body:
    canonical = f'<link rel="canonical" href="{BASE}">'
    alternates = canonical + f'''\n  <link rel="alternate" hreflang="en" href="{BASE}">
  <link rel="alternate" hreflang="ru" href="{BASE}ru/">
  <link rel="alternate" hreflang="pl" href="{BASE}pl/">
  <link rel="alternate" hreflang="x-default" href="{BASE}">'''
    if canonical not in body:
        raise SystemExit("English canonical link missing")
    body = body.replace(canonical, alternates, 1)

if 'class="langs"' not in body:
    css = '''\n    .langs{display:flex;justify-content:flex-end;gap:8px;padding-top:18px}.langs a{border:1px solid var(--line);border-radius:999px;padding:5px 10px;text-decoration:none;font-weight:700}.langs .active{background:var(--accent);color:#08120d;border-color:var(--accent)}\n'''
    body = body.replace("  </style>", css + "  </style>", 1)
    body = body.replace('<main class="wrap">', '<main class="wrap">\n    <nav class="langs" aria-label="Language"><a class="active" href="./">EN</a><a href="ru/" lang="ru">RU</a><a href="pl/" lang="pl">PL</a></nav>', 1)
    body = body.replace('@media(max-width:760px){.hero{padding-top:48px}.grid,.checks{grid-template-columns:1fr}.btn{width:100%;max-width:420px}}', '@media(max-width:760px){.hero{padding-top:48px}.grid,.checks{grid-template-columns:1fr}.btn{width:100%;max-width:420px}.langs{justify-content:center}}', 1)
site.write_text(body, encoding="utf-8")

# Sitemap: expose all crawlable language variants.
sitemap = Path("site/sitemap.xml")
sitemap.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE}</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
  <url><loc>{BASE}ru/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>{BASE}pl/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
</urlset>
''', encoding="utf-8")

# Permanent release updater: synchronize all language landing pages.
wf = Path(".github/workflows/update-readme-download.yml")
w = wf.read_text(encoding="utf-8")
old = """          site = Path('site/index.html')
          if site.exists():
              body = site.read_text(encoding='utf-8')
              button = f'<!-- latest-apk-site:start --><a class=\"btn primary\" href=\"{apk_url}\">Download {apk_name}</a><!-- latest-apk-site:end -->'
              site_pattern = re.compile(
                  r'<!-- latest-apk-site:start -->.*?<!-- latest-apk-site:end -->',
                  re.DOTALL,
              )
              if not site_pattern.search(body):
                  raise SystemExit('Site APK marker block not found')
              body = site_pattern.sub(button, body, count=1)
              body = re.sub(r'\"softwareVersion\":\\s*\"[^\"]+\"', f'\"softwareVersion\": \"{version}\"', body, count=1)
              body = re.sub(r'\"downloadUrl\":\\s*\"[^\"]+\"', f'\"downloadUrl\": \"{apk_url}\"', body, count=1)
              body = re.sub(
                  r'\"releaseNotes\":\\s*\"[^\"]+\"',
                  f'\"releaseNotes\": \"https://github.com/{os.environ[\"GITHUB_REPOSITORY\"]}/releases/tag/{tag}\"',
                  body,
                  count=1,
              )
              site.write_text(body, encoding='utf-8')
"""
new = """          site_pages = [
              (Path('site/index.html'), 'Download'),
              (Path('site/ru/index.html'), 'Скачать'),
              (Path('site/pl/index.html'), 'Pobierz'),
          ]
          site_pattern = re.compile(
              r'<!-- latest-apk-site:start -->.*?<!-- latest-apk-site:end -->',
              re.DOTALL,
          )
          for site, label in site_pages:
              if not site.exists():
                  continue
              body = site.read_text(encoding='utf-8')
              button = f'<!-- latest-apk-site:start --><a class=\"btn primary\" href=\"{apk_url}\">{label} {apk_name}</a><!-- latest-apk-site:end -->'
              if not site_pattern.search(body):
                  raise SystemExit(f'Site APK marker block not found in {site}')
              body = site_pattern.sub(button, body, count=1)
              body = re.sub(r'\"softwareVersion\":\\s*\"[^\"]+\"', f'\"softwareVersion\": \"{version}\"', body, count=1)
              body = re.sub(r'\"downloadUrl\":\\s*\"[^\"]+\"', f'\"downloadUrl\": \"{apk_url}\"', body, count=1)
              body = re.sub(
                  r'\"releaseNotes\":\\s*\"[^\"]+\"',
                  f'\"releaseNotes\": \"https://github.com/{os.environ[\"GITHUB_REPOSITORY\"]}/releases/tag/{tag}\"',
                  body,
                  count=1,
              )
              site.write_text(body, encoding='utf-8')
"""
if old in w:
    w = w.replace(old, new, 1)
elif "site_pages = [" not in w:
    raise SystemExit("Could not patch release site updater")
w = w.replace("README.md docs/README.ru.md docs/README.pl.md site/index.html; then", "README.md docs/README.ru.md docs/README.pl.md site/index.html site/ru/index.html site/pl/index.html; then")
w = w.replace("git add README.md docs/README.ru.md docs/README.pl.md site/index.html", "git add README.md docs/README.ru.md docs/README.pl.md site/index.html site/ru/index.html site/pl/index.html")
wf.write_text(w, encoding="utf-8")
