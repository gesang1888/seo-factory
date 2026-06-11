#!/usr/bin/env python3
"""Rebrand cloned *_kakobuy.py modules from BBDBuy → Kakobuy."""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

PROTECT = [
    "w2clinks.com/public/typesense-search.php",
    "w2clinks.com/spreadsheet/",
    "w2clinks.com",
    "wa.me/447856544534",
    "orientdig-theme.css",
    "orientdig-help.php",
    "orientdig-logo.png",
    "assets/images/orientdig-logo.png",
    "orientdig.com",
]

TARGETS = [
    "scripts/pages_kakobuy.py",
    "scripts/trust_pages_kakobuy.py",
    "scripts/i18n_ui_kakobuy.py",
    "scripts/keyword_articles_kakobuy.py",
    "scripts/deep_content_kakobuy.py",
    "scripts/hub_sections_kakobuy.py",
    "scripts/country_seo_kakobuy.py",
    "scripts/promo_banners_kakobuy.py",
    "scripts/reddit_insights_kakobuy.py",
    "scripts/shipping_data_kakobuy.py",
    "scripts/renderer_kakobuy.py",
]


def rebrand(text: str) -> str:
    holders: dict[str, str] = {}
    for i, s in enumerate(PROTECT):
        key = f"__PROTECT_{i}__"
        holders[key] = s
        text = text.replace(s, key)
    text = text.replace("BBDBuySpreadsheetBuilder", "KakobuySpreadsheetBuilder")
    text = text.replace("BBDBuy", "Kakobuy")
    text = text.replace("bbdbuy", "kakobuy")
    for key, s in holders.items():
        text = text.replace(key, s)
    return text


def main() -> None:
    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            print(f"skip (missing): {rel}")
            continue
        p.write_text(rebrand(p.read_text(encoding="utf-8")), encoding="utf-8")
        print("rebranded", rel)


if __name__ == "__main__":
    main()
