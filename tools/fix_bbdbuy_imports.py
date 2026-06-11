#!/usr/bin/env python3
"""Fix cross-imports in *_bbdbuy.py to use bbdbuy clones."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

REMAP = {
    "pages": "pages_bbdbuy",
    "trust_pages": "trust_pages_bbdbuy",
    "i18n_ui": "i18n_ui_bbdbuy",
    "keyword_articles": "keyword_articles_bbdbuy",
    "deep_content": "deep_content_bbdbuy",
    "hub_sections": "hub_sections_bbdbuy",
    "country_seo": "country_seo_bbdbuy",
    "promo_banners": "promo_banners_bbdbuy",
    "reddit_insights": "reddit_insights_bbdbuy",
    "shipping_data": "shipping_data_bbdbuy",
    "renderer": "renderer_bbdbuy",
}

KEEP = {"link_helpers", "hub_icons", "domains", "domains_bbdbuy", "fetch_live_data"}


def fix_file(path: pathlib.Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    def repl(match: re.Match[str]) -> str:
        mod = match.group(1)
        if mod in REMAP:
            return f"from scripts.{REMAP[mod]} import"
        return match.group(0)

    text = re.sub(r"from scripts\.(\w+) import", repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    for path in sorted((ROOT / "scripts").glob("*_bbdbuy.py")):
        if fix_file(path):
            print("fixed imports:", path.name)


if __name__ == "__main__":
    main()
