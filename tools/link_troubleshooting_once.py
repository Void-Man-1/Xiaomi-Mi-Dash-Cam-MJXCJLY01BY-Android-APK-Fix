from pathlib import Path

p = Path("README.md")
text = p.read_text(encoding="utf-8")

needle = "- [Common problems and FAQ](#common-problems-and-faq) — installation, Android 15/16, black preview, Wi-Fi, Poco F6, Mi account, and model compatibility.\n"
addition = needle + "- [Troubleshooting guide](docs/TROUBLESHOOTING.md) — symptom-by-symptom help for installation, connection, black preview, freezes, account/login, and recordings.\n"
if needle in text and "[Troubleshooting guide](docs/TROUBLESHOOTING.md)" not in text:
    text = text.replace(needle, addition, 1)

anchor = "The final 2.0.0 release was hardware-tested with the European `MJXCJLY01BY` on a **Poco F6 running Android 16 / HyperOS 3**, including connection and reconnection, live preview, recording thumbnails, download, and playback. It is not a compatibility claim for the similarly named Mi Dash Cam 1S (`MJXCJLY02BY`)."
append = anchor + "\n\nFor symptom-by-symptom diagnosis, see the dedicated [Mi Dash Cam MJXCJLY01BY troubleshooting guide](docs/TROUBLESHOOTING.md)."
if anchor in text and "dedicated [Mi Dash Cam MJXCJLY01BY troubleshooting guide]" not in text:
    text = text.replace(anchor, append, 1)

p.write_text(text, encoding="utf-8")
