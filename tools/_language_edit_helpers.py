from pathlib import Path


def apply(path: str, replacements: list[tuple[str, str]]) -> None:
    p = Path(path)
    if p.name == "README.md" or p.name.startswith("README."):
        raise SystemExit(f"README edit refused: {path}")
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"Expected text not found in {path}: {old[:120]!r}")
        text = text.replace(old, new)
    if text == original:
        raise SystemExit(f"No changes produced for {path}")
    p.write_text(text, encoding="utf-8")
    print(f"edited {path}")
