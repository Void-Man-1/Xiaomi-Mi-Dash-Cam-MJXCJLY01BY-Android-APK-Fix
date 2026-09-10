from pathlib import Path
import re

VIDEO_RAW = "https://raw.githubusercontent.com/Void-Man-1/Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix/main/assets/evidence/poco-f6-android16-v2.0.0-full-camera-test.mp4"
POSTER_RAW = "https://raw.githubusercontent.com/Void-Man-1/Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix/main/assets/evidence/poco-f6-android16-v2.0.0-video-poster.jpg"
VIDEO_GITHUB = "https://github.com/Void-Man-1/Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix/blob/main/assets/evidence/poco-f6-android16-v2.0.0-full-camera-test.mp4"

COPY = {
    "site/index.html": ("Full physical-camera acceptance test", "Poco F6 · Android 16 / HyperOS 3 · physical MJXCJLY01BY EU camera", "Full physical-camera acceptance test video", "Your browser cannot play this MP4. Open the original video on GitHub.", "Open original video →"),
    "site/pl/index.html": ("Pełny test z fizyczną kamerą", "Poco F6 · Android 16 / HyperOS 3 · fizyczna kamera MJXCJLY01BY EU", "Film z pełnego testu z fizyczną kamerą", "Twoja przeglądarka nie może odtworzyć tego pliku MP4. Otwórz oryginalne nagranie na GitHubie.", "Otwórz oryginalne nagranie →"),
    "site/uk/index.html": ("Повний тест із фізичною камерою", "Poco F6 · Android 16 / HyperOS 3 · фізична камера MJXCJLY01BY EU", "Відео повного тесту з фізичною камерою", "Ваш браузер не може відтворити цей MP4-файл. Відкрийте оригінальне відео на GitHub.", "Відкрити оригінальне відео →"),
    "site/de/index.html": ("Vollständiger Test mit echter Kamera", "Poco F6 · Android 16 / HyperOS 3 · physische MJXCJLY01BY-EU-Kamera", "Video des vollständigen Tests mit echter Kamera", "Ihr Browser kann diese MP4-Datei nicht abspielen. Öffnen Sie das Originalvideo auf GitHub.", "Originalvideo öffnen →"),
    "site/ru/index.html": ("Полный тест с реальной камерой", "Poco F6 · Android 16 / HyperOS 3 · физическая камера MJXCJLY01BY EU", "Видео полного теста с реальной камерой", "Ваш браузер не может воспроизвести этот MP4-файл. Откройте оригинальное видео на GitHub.", "Открыть оригинальное видео →"),
}

for rel, (title, note, aria, fallback, open_label) in COPY.items():
    path = Path(rel)
    html = path.read_text(encoding="utf-8")
    proof = html.index('<section class="section proof-section">')
    gallery = html.index('<div class="gallery">', proof)
    if 'class="evidence-video"' in html[proof:gallery]:
        raise SystemExit(f"{rel}: evidence video already present")
    block = (
        '<figure class="evidence-video">\n'
        f'<div class="video-stage"><video controls playsinline preload="metadata" poster="{POSTER_RAW}" aria-label="{aria}"><source src="{VIDEO_RAW}" type="video/mp4">{fallback}</video></div>\n'
        f'<figcaption class="video-meta"><div><strong>{title}</strong><span>{note}</span></div><a href="{VIDEO_GITHUB}">{open_label}</a></figcaption>\n'
        '</figure>\n'
    )
    html = html[:gallery] + block + html[gallery:]
    html, count = re.subn(r'<div class="evidence-bar">.*?</div>', '', html, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{rel}: expected one evidence bar, found {count}")
    path.write_text(html, encoding="utf-8")

css_path = Path("site/styles.css")
css = css_path.read_text(encoding="utf-8")
old_pattern = re.compile(r'\.proof-section\{.*?\.evidence-bar a\{[^}]*\}', re.S)
new_css = (
    '.proof-section{background:var(--dark);color:#fff}.proof-section .section-head p{color:#bcbcbc}.proof-section .kicker{color:#ffa76d}\n'
    '.evidence-video{margin:0 0 18px;border:1px solid #333;border-radius:22px;background:#161616;overflow:hidden}.video-stage{display:grid;place-items:center;aspect-ratio:16/9;max-height:660px;background:#050505}.video-stage video{display:block;width:100%;height:100%;object-fit:contain;background:#050505}.video-meta{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 18px;border-top:1px solid #303030;background:#1b1b1b}.video-meta strong{display:block;font-size:.96rem}.video-meta span{display:block;margin-top:3px;color:#bdbdbd;font-size:.8rem}.video-meta a{flex:0 0 auto;color:#fff;font-weight:800}\n'
    '.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.shot{margin:0;display:flex;min-width:0;min-height:0;flex-direction:column;border:1px solid #333;border-radius:20px;background:#171717;overflow:hidden}.shot img{display:block;width:100%;height:clamp(340px,38vw,520px);object-fit:contain;object-position:center top;background:#0b0b0b}.shot-caption{position:static;display:block;min-height:64px;padding:11px 13px;border-top:1px solid #303030;background:#1c1c1c}.shot-caption strong{display:block;font-size:.9rem}.shot-caption span{display:block;color:#c5c5c5;font-size:.77rem;margin-top:2px}'
)
css, count = old_pattern.subn(new_css, css, count=1)
if count != 1:
    raise SystemExit(f"styles.css: proof media block replacement count={count}")
css = css.replace('.features{grid-template-columns:1fr 1fr}.gallery{grid-template-columns:1fr 1fr}.shot:first-child{grid-column:1/-1}.steps', '.features{grid-template-columns:1fr 1fr}.steps')
css = css.replace('@media(max-width:820px){.nav{', '@media(max-width:820px){.gallery{grid-template-columns:1fr}.video-meta{align-items:flex-start;flex-direction:column}.nav{')
css = css.replace('.shot,.shot:first-child{grid-column:auto;min-height:480px}', '.shot,.shot:first-child{grid-column:auto;min-height:0}.shot img{height:min(72vh,560px)}')
css_path.write_text(css, encoding="utf-8")

for path in map(Path, COPY):
    s = path.read_text(encoding="utf-8")
    assert s.count('class="evidence-video"') == 1
    assert s.count('<video controls playsinline preload="metadata"') == 1
    assert s.count('type="video/mp4"') == 1
    assert 'poco-f6-android16-v2.0.0-video-poster.jpg' in s
    assert 'poco-f6-android16-v2.0.0-full-camera-test.mp4' in s
    assert 'class="evidence-bar"' not in s
    assert s.count('class="shot"') == 3
css = css_path.read_text(encoding="utf-8")
assert 'grid-template-columns:repeat(3,minmax(0,1fr))' in css
assert 'object-fit:contain' in css
assert '.shot:first-child{min-height:560px}' not in css
print("PROOF GALLERY PATCH VALIDATED")
