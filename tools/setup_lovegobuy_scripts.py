#!/usr/bin/env python3
"""Clone Kakobuy content scripts to *_lovegobuy.py and fix cross-imports."""

from __future__ import annotations

import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

CLONE_MAP = {
    "pages_kakobuy.py": "pages_lovegobuy.py",
    "trust_pages_kakobuy.py": "trust_pages_lovegobuy.py",
    "i18n_ui_kakobuy.py": "i18n_ui_lovegobuy.py",
    "keyword_articles_kakobuy.py": "keyword_articles_lovegobuy.py",
    "deep_content_kakobuy.py": "deep_content_lovegobuy.py",
    "hub_sections_kakobuy.py": "hub_sections_lovegobuy.py",
    "country_seo_kakobuy.py": "country_seo_lovegobuy.py",
    "promo_banners_kakobuy.py": "promo_banners_lovegobuy.py",
    "reddit_insights_kakobuy.py": "reddit_insights_lovegobuy.py",
    "shipping_data_kakobuy.py": "shipping_data_lovegobuy.py",
    "renderer_kakobuy.py": "renderer_lovegobuy.py",
    "link_helpers_kakobuy.py": "link_helpers_lovegobuy.py",
    "fetch_kakobuy_activities.py": "fetch_lovegobuy_activities.py",
}

REMAP = {k.replace("_kakobuy", ""): v.replace("_kakobuy", "") for k, v in CLONE_MAP.items()}
REMAP = {f"{k}_kakobuy": f"{k}_lovegobuy" for k in [
    "pages", "trust_pages", "i18n_ui", "keyword_articles", "deep_content",
    "hub_sections", "country_seo", "promo_banners", "reddit_insights",
    "shipping_data", "renderer", "link_helpers", "fetch_kakobuy_activities",
]}
REMAP["fetch_kakobuy_activities"] = "fetch_lovegobuy_activities"


def fix_imports(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        mod = match.group(1)
        if mod in REMAP:
            return f"from scripts.{REMAP[mod]} import"
        return match.group(0)

    text = re.sub(r"from scripts\.(\w+) import", repl, text)
    text = text.replace(
        "from scripts.domains_kakobuy import HREFLANG_KAKOBUY, KAKOBUY_DOMAINS",
        "from scripts.domains_lovegobuy import HREFLANG_LOVEGOBUY, LOVEGOBUY_DOMAINS",
    )
    text = text.replace("HREFLANG_KAKOBUY", "HREFLANG_LOVEGOBUY")
    text = text.replace("KAKOBUY_DOMAINS", "LOVEGOBUY_DOMAINS")
    text = text.replace(
        'CONFIG_PATH = ROOT / "site.kakobuy.config.json"',
        'CONFIG_PATH = ROOT / "site.lovegobuy.config.json"',
    )
    text = text.replace(
        "from scripts.link_helpers_kakobuy import",
        "from scripts.link_helpers_lovegobuy import",
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
