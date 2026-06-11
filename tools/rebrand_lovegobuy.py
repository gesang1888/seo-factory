#!/usr/bin/env python3
"""Rebrand cloned *_lovegobuy.py modules from Kakobuy → Lovegobuy."""

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
    "kakobuy.com",
    "ikako.vip",
    "kakobuy-theme.css",
    "kb-site",
    "kb-promo",
]

TARGETS = [
    "scripts/pages_lovegobuy.py",
    "scripts/trust_pages_lovegobuy.py",
    "scripts/i18n_ui_lovegobuy.py",
    "scripts/keyword_articles_lovegobuy.py",
    "scripts/deep_content_lovegobuy.py",
    "scripts/hub_sections_lovegobuy.py",
    "scripts/country_seo_lovegobuy.py",
    "scripts/promo_banners_lovegobuy.py",
    "scripts/reddit_insights_lovegobuy.py",
    "scripts/shipping_data_lovegobuy.py",
    "scripts/renderer_lovegobuy.py",
    "scripts/link_helpers_lovegobuy.py",
    "scripts/fetch_lovegobuy_activities.py",
]


def rebrand(text: str) -> str:
    holders: dict[str, str] = {}
    for i, s in enumerate(PROTECT):
        key = f"__PROTECT_{i}__"
        holders[key] = s
        text = text.replace(s, key)
    text = text.replace("KakobuySpreadsheetBuilder", "LovegobuySpreadsheetBuilder")
    text = text.replace("Kakobuy", "Lovegobuy")
    text = text.replace("kakobuy", "lovegobuy")
    text = text.replace("lg-site", "kb-site")  # restore if double-replaced later
    for key, s in holders.items():
        text = text.replace(key, s)
    text = text.replace("kb-site", "lg-site")
    text = text.replace("kb-promo", "lg-promo")
    text = text.replace("kakobuy-theme.css", "lovegobuy-theme.css")
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
