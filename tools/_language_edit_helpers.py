from pathlib import Path


def apply(path: str, replacements: list[tuple[str, str]]) -> None:
    p = Path(path)
    if p.name == "README.md" or p.name.startswith("README."):
        raise SystemExit(f"README edit refused: {path}")
    text = p.read_text(encoding="utf-8")
    original = text
    missing = []
    for old, new in replacements:
        if old not in text:
            missing.append(old[:120])
            continue
        text = text.replace(old, new)
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"edited {path}")
    else:
        print(f"NO_MATCHED_EDITS {path}")
    for item in missing:
        print(f"SOURCE_DRIFT {path}: {item!r}")
