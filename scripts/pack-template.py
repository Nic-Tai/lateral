#!/usr/bin/env python3
"""Build a clean ZIP of the live Demo08 landing page (without the promo banner)."""

from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "lateral-html" / "Demo08"
LICENSE = ROOT / "license.txt"
README = ROOT / "template-package" / "README.md"
OUT = SRC / "downloads" / "qm-salon-landing-page-template.zip"

EXCLUDE_NAMES = {
    "vercel.json",
    "404.html",
}
EXCLUDE_DIRS = {
    "downloads",
}
EXCLUDE_FILES = {
    "js/template-banner.js",
    "css/template-banner.css",
}

BANNER_BLOCK = re.compile(
    r"\n?[ \t]*<!-- TEMPLATE-BANNER:START -->.*?<!-- TEMPLATE-BANNER:END -->\n?",
    re.DOTALL,
)
BANNER_SCRIPT = re.compile(
    r"\n?[ \t]*<!-- TEMPLATE-BANNER-SCRIPT:START -->.*?<!-- TEMPLATE-BANNER-SCRIPT:END -->\n?",
    re.DOTALL,
)
BANNER_HEAD = re.compile(
    r"\n?[ \t]*<!-- TEMPLATE-BANNER-HEAD:START -->.*?<!-- TEMPLATE-BANNER-HEAD:END -->\n?",
    re.DOTALL,
)
BANNER_FOOTER = re.compile(
    r"\n?[ \t]*<!-- TEMPLATE-BANNER-FOOTER:START -->.*?<!-- TEMPLATE-BANNER-FOOTER:END -->\n?",
    re.DOTALL,
)
HTML_CLASS = re.compile(r'(<html\b[^>]*class=")([^"]*)(")')
BODY_CLASS = re.compile(r'(<body\b[^>]*class=")([^"]*)(")')
BANNER_CSS_LINK = re.compile(
    r"\n?[ \t]*<link rel=\"stylesheet\" href=\"css/template-banner.css\">\n?"
)
BANNER_JS_TAG = re.compile(
    r"\n?[ \t]*<script src=\"js/template-banner.js\"></script>\n?"
)


def strip_banner_classes(value: str) -> str:
    parts = [part for part in value.split() if part not in {"has-template-banner"}]
    return " ".join(parts)


def clean_html(text: str) -> str:
    text = BANNER_BLOCK.sub("\n", text)
    text = BANNER_SCRIPT.sub("\n", text)
    text = BANNER_HEAD.sub("\n", text)
    text = BANNER_FOOTER.sub("\n", text)
    text = BANNER_CSS_LINK.sub("\n", text)
    text = BANNER_JS_TAG.sub("\n", text)

    def drop_html_class(match: re.Match[str]) -> str:
        cleaned = strip_banner_classes(match.group(2))
        if not cleaned:
            return match.group(0).replace(f' class="{match.group(2)}"', "", 1)
        return f"{match.group(1)}{cleaned}{match.group(3)}"

    def drop_body_class(match: re.Match[str]) -> str:
        cleaned = strip_banner_classes(match.group(2))
        if not cleaned:
            tag = match.group(0)
            return re.sub(r"\sclass=\"[^\"]*\"", "", tag, count=1)
        return f"{match.group(1)}{cleaned}{match.group(3)}"

    text = HTML_CLASS.sub(drop_html_class, text)
    text = BODY_CLASS.sub(drop_body_class, text)
    text = re.sub(r"<html class=\"has-template-banner\">", "<html>", text)
    text = re.sub(r"<body class=\"has-template-banner\">", "<body>", text)
    return text


def should_skip(path: Path) -> bool:
    rel = path.relative_to(SRC).as_posix()
    if path.name in EXCLUDE_NAMES:
        return True
    if rel in EXCLUDE_FILES:
        return True
    return any(part in EXCLUDE_DIRS for part in path.relative_to(SRC).parts)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing template source: {SRC}")
    if not README.exists():
        raise SystemExit(f"Missing package README: {README}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(README, "qm-salon-landing-page-template/README.md")
        if LICENSE.exists():
            zf.write(LICENSE, "qm-salon-landing-page-template/license.txt")

        for path in sorted(SRC.rglob("*")):
            if not path.is_file() or should_skip(path):
                continue
            arcname = f"qm-salon-landing-page-template/{path.relative_to(SRC).as_posix()}"
            if path.suffix.lower() in {".html", ".htm"}:
                zf.writestr(arcname, clean_html(path.read_text(encoding="utf-8")))
            else:
                zf.write(path, arcname)

    OUT.write_bytes(buffer.getvalue())
    size_mb = OUT.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
