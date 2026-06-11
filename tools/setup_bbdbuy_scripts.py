#!/usr/bin/env python3
"""Clone OrientDig content scripts to *_bbdbuy.py and fix cross-imports."""

from __future__ import annotations

import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

CLONE_MAP = {
    "pages.py": "pages_bbdbuy.py",
    "trust_pages.py": "trust_pages_bbdbuy.py",
    "i18n_ui.py": "i18n_ui_bbdbuy.py",
    "keyword_articles.py": "keyword_articles_bbdbuy.py",
    "deep_content.py": "deep_content_bbdbuy.py",
    "hub_sections.py": "hub_sections_bbdbuy.py",
    "country_seo.py": "country_seo_bbdbuy.py",
    "promo_banners.py": "promo_banners_bbdbuy.py",
    "reddit_insights.py": "reddit_insights_bbdbuy.py",
    "shipping_data.py": "shipping_data_bbdbuy.py",
    "renderer.py": "renderer_bbdbuy.py",
}

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


def fix_imports(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        mod = match.group(1)
        if mod in REMAP:
            return f"from scripts.{REMAP[mod]} import"
        return match.group(0)

    text = re.sub(r"from scripts\.(\w+) import", repl, text)
    text = text.replace(
        "from scripts.domains_partner import HREFLANG_PARTNER, PARTNER_DOMAINS",
        "from scripts.domains_bbdbuy import HREFLANG_BBDBUY, BBDBUY_DOMAINS",
    )
    text = text.replace("HREFLANG_PARTNER", "HREFLANG_BBDBUY")
    text = text.replace("PARTNER_DOMAINS", "BBDBUY_DOMAINS")
    text = text.replace(
        'CONFIG_PATH = ROOT / "site.config.json"',
        'CONFIG_PATH = ROOT / "site.bbdbuy.config.json"',
    )
    return text


def main() -> None:
    scripts = ROOT / "scripts"
    for src, dst in CLONE_MAP.items():
        src_path = scripts / src
        dst_path = scripts / dst
        shutil.copy2(src_path, dst_path)
        dst_path.write_text(
            fix_imports(dst_path.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        print("cloned", dst)


if __name__ == "__main__":
    main()
