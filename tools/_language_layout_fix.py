from pathlib import Path

path = Path("site/styles.css")
text = path.read_text(encoding="utf-8")
old = '.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:51px;padding:13px 18px;border-radius:13px;border:1px solid var(--line);text-decoration:none;font-weight:850;transition:'
new = '.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-width:0;max-width:100%;min-height:51px;padding:13px 18px;border-radius:13px;border:1px solid var(--line);text-align:center;white-space:normal;overflow-wrap:anywhere;text-decoration:none;font-weight:850;transition:'
if old not in text:
    raise SystemExit('Expected .btn rule not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print('LANGUAGE_LAYOUT_FIX_OK')
