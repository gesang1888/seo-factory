#!/usr/bin/env python3
"""Clone BBDBuy content scripts to *_kakobuy.py and fix cross-imports."""

from __future__ import annotations

import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

CLONE_MAP = {
    "pages_bbdbuy.py": "pages_kakobuy.py",
    "trust_pages_bbdbuy.py": "trust_pages_kakobuy.py",
    "i18n_ui_bbdbuy.py": "i18n_ui_kakobuy.py",
    "keyword_articles_bbdbuy.py": "keyword_articles_kakobuy.py",
    "deep_content_bbdbuy.py": "deep_content_kakobuy.py",
    "hub_sections_bbdbuy.py": "hub_sections_kakobuy.py",
    "country_seo_bbdbuy.py": "country_seo_kakobuy.py",
    "promo_banners_bbdbuy.py": "promo_banners_kakobuy.py",
    "reddit_insights_bbdbuy.py": "reddit_insights_kakobuy.py",
    "shipping_data_bbdbuy.py": "shipping_data_kakobuy.py",
    "renderer_bbdbuy.py": "renderer_kakobuy.py",
}

REMAP = {
    "pages_bbdbuy": "pages_kakobuy",
    "trust_pages_bbdbuy": "trust_pages_kakobuy",
    "i18n_ui_bbdbuy": "i18n_ui_kakobuy",
    "keyword_articles_bbdbuy": "keyword_articles_kakobuy",
    "deep_content_bbdbuy": "deep_content_kakobuy",
    "hub_sections_bbdbuy": "hub_sections_kakobuy",
    "country_seo_bbdbuy": "country_seo_kakobuy",
    "promo_banners_bbdbuy": "promo_banners_kakobuy",
    "reddit_insights_bbdbuy": "reddit_insights_kakobuy",
    "shipping_data_bbdbuy": "shipping_data_kakobuy",
    "renderer_bbdbuy": "renderer_kakobuy",
}


def fix_imports(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        mod = match.group(1)
        if mod in REMAP:
            return f"from scripts.{REMAP[mod]} import"
        return match.group(0)

    text = re.sub(r"from scripts\.(\w+) import", repl, text)
    text = text.replace(
        "from scripts.domains_bbdbuy import HREFLANG_BBDBUY, BBDBUY_DOMAINS",
        "from scripts.domains_kakobuy import HREFLANG_KAKOBUY, KAKOBUY_DOMAINS",
    )
    text = text.replace("HREFLANG_BBDBUY", "HREFLANG_KAKOBUY")
    text = text.replace("BBDBUY_DOMAINS", "KAKOBUY_DOMAINS")
    text = text.replace(
        'CONFIG_PATH = ROOT / "site.bbdbuy.config.json"',
        'CONFIG_PATH = ROOT / "site.kakobuy.config.json"',
    )
    text = text.replace(
        "from scripts.link_helpers import",
        "from scripts.link_helpers_kakobuy import",
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
